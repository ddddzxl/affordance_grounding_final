#!/usr/bin/env python3
"""iphone_demo.py — run the v1 PTv3 functionality head on an iPhone 3D-Scanner capture (Route B).

No depth needed: the app already reconstructed the cloud (colored.ply). We project that cloud back
into each captured RGB frame, sample DINOv2 features (matching the training protocol: vitl14 / long-side 924, L2-norm
per frame, mean-of-units aggregation — same as the SceneFun3D lift), then run the SAME head:
GridSample -> PTv3 -> per-class DBSCAN -> functional-element instances.

Coordinate convention: ARKit camera (+y up, -z forward) -> OpenCV pinhole (+y down, +z forward) by
flipping Y,Z (180° about x) — verified by the projection self-check (8770/8770 pts in-view).
Occlusion is skipped (planar wall, no depth, no self-occlusion).

⚠️ OOD: the head is trained on dense (~1M-pt) 3D rooms; an ~8.7k-pt planar wall is far OOD — the
hope rides on DINOv2 feats (a switch still looks like a switch) overcoming the geometry degeneracy.

  python src/demo/iphone_demo.py --scan wall_with_switch --run C_g01p128_v2
Outputs to viz/func_seg/demo/iphone_3dscanner/<scan>/: pred.ply + p{k}_pred.png + stdout.
"""
import os, sys, json, glob, argparse
import numpy as np
import torch
import torch.nn.functional as F
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _CODE_ROOT)
from paths import CODE, DEMO_TASK1, IPHONE_DATA  # noqa: E402
sys.path.insert(0, os.path.join(CODE, "task1"))
sys.path.insert(0, os.path.join(CODE, "task1", "features"))
from data.scene_io import grid_sample                                  # noqa: E402
from eval.predict_v1 import cluster, softmax_max, eval_safe, RUNS      # noqa: E402
from models import build_model                                        # noqa: E402
from dinov2_extract import DINOv2Extractor                            # noqa: E402

CLASS_NAMES = {1: "rotate", 2: "key_press", 3: "tip_push", 4: "hook_pull", 5: "pinch_pull",
               6: "hook_turn", 7: "foot_push", 8: "plug_in", 9: "unplug"}
DATA = IPHONE_DATA
OUT = DEMO_TASK1
CMAP = (plt.cm.tab20(np.linspace(0, 1, 20))[:, :3] * 255).astype(np.uint8)
ARKIT2CV = np.array([1, -1, -1], np.float64)   # ARKit cam (+y up,-z fwd) -> OpenCV (+y down,+z fwd)


def read_ply_xyz(path):
    """ASCII PLY -> (N,3) float64 vertex xyz (ignores the trailing 'element camera')."""
    raw = open(path).read().split("\n")
    hi = next(i for i, l in enumerate(raw) if l.strip() == "end_header")
    nv = int(next(l for l in raw if l.startswith("element vertex")).split()[-1])
    return np.array([[float(x) for x in raw[hi + 1 + i].split()[:3]] for i in range(nv)], np.float64)


def read_frames(scan_dir):
    """frame_*.json + frame_*.jpg -> [dict(K(3x3), cam2world(4x4), rgb path)]."""
    out = []
    for jf in sorted(glob.glob(os.path.join(scan_dir, "frame_*.json"))):
        jpg = jf.replace(".json", ".jpg")
        if not os.path.exists(jpg):
            continue
        d = json.load(open(jf))
        out.append(dict(K=np.array(d["intrinsics"], np.float64).reshape(3, 3),
                        cam2world=np.array(d["cameraPoseARFrame"], np.float64).reshape(4, 4),
                        rgb=jpg))
    return out


def project(xyz, K, cam2world):
    """world xyz -> (u, v, z) for one frame (ARKit->OpenCV flip; no depth/occlusion)."""
    w2c = np.linalg.inv(cam2world)
    Pc = (w2c[:3, :3] @ xyz.T + w2c[:3, 3:4]).T * ARKIT2CV
    z = Pc[:, 2]
    u = K[0, 0] * Pc[:, 0] / z + K[0, 2]
    v = K[1, 1] * Pc[:, 1] / z + K[1, 2]
    return u, v, z


def _read_rgb(path):
    rgb = plt.imread(path)
    if rgb.dtype != np.uint8:
        rgb = (rgb * 255).astype(np.uint8)
    return rgb


def lift_features(xyz, frames, ext, dev):
    """Route B: project cloud into each frame, sample DINOv2, aggregate (L2-norm per frame, mean of
    units, no renorm — matches the SceneFun3D lift). Returns (feat (N,1024) f32, observed (N,) bool)."""
    N = len(xyz)
    accum = torch.zeros(N, ext.feat_dim, device=dev)
    count = torch.zeros(N, device=dev)
    for fr in frames:
        rgb = _read_rgb(fr["rgb"]); H, W = rgb.shape[:2]
        u, v, z = project(xyz, fr["K"], fr["cam2world"])
        vis = (z > 1e-6) & (u >= 0) & (u < W) & (v >= 0) & (v < H)
        if not vis.any():
            continue
        fd = ext.extract(rgb)
        idx = torch.from_numpy(np.nonzero(vis)[0]).to(dev)
        f = F.normalize(ext.sample(fd, u[vis], v[vis]).float(), dim=1)
        accum.index_add_(0, idx, f)
        count.index_add_(0, idx, torch.ones(idx.numel(), device=dev))
    obs = count > 0
    feat = torch.zeros(N, ext.feat_dim, device=dev)
    feat[obs] = accum[obs] / count[obs].unsqueeze(1)
    return feat.cpu().numpy(), obs.cpu().numpy()


def write_ply(path, xyz, rgb):
    n = len(xyz)
    header = (f"ply\nformat binary_little_endian 1.0\nelement vertex {n}\n"
              "property float x\nproperty float y\nproperty float z\n"
              "property uchar red\nproperty uchar green\nproperty uchar blue\nend_header\n")
    arr = np.empty(n, np.dtype([("x", "<f4"), ("y", "<f4"), ("z", "<f4"),
                                ("r", "u1"), ("g", "u1"), ("b", "u1")]))
    arr["x"], arr["y"], arr["z"] = xyz[:, 0], xyz[:, 1], xyz[:, 2]
    arr["r"], arr["g"], arr["b"] = rgb[:, 0], rgb[:, 1], rgb[:, 2]
    with open(path, "wb") as fh:
        fh.write(header.encode()); fh.write(arr.tobytes())


def colorize(n, instances):
    rgb = np.full((n, 3), 185, np.uint8)
    for i, ins in enumerate(instances):
        rgb[ins["mask"] > 0] = CMAP[i % 20]
    return rgb


def feat_to_rgb(feat):
    """(M,1024) DINOv2 feats -> (M,3) uint8 via PCA-to-3 + robust per-channel normalize. A good lift
    shows semantic structure (switch vs wall differ in color); uniform noise = a lift problem."""
    X = feat - feat.mean(0)
    Vt = np.linalg.svd(X, full_matrices=False)[2]
    proj = X @ Vt[:3].T
    lo, hi = np.percentile(proj, 2, 0), np.percentile(proj, 98, 0)
    return (np.clip((proj - lo) / (hi - lo + 1e-9), 0, 1) * 255).astype(np.uint8)


def overlay_feat(path, rgb_path, xyz, feat_rgb, K, cam2world, title):
    """RGB | DINOv2-PCA side by side: shows whether the lifted features carry semantic structure."""
    rgb = _read_rgb(rgb_path); H, W = rgb.shape[:2]
    u, v, z = project(xyz, K, cam2world)
    vis = (z > 1e-6) & (u >= 0) & (u < W) & (v >= 0) & (v < H)
    fig, axs = plt.subplots(1, 2, figsize=(18, 6))
    axs[0].imshow(rgb); axs[0].set_title("RGB"); axs[0].axis("off")
    axs[1].imshow(rgb)
    axs[1].scatter(u[vis], v[vis], s=12, c=feat_rgb[vis] / 255.0, linewidths=0)
    axs[1].set_title("DINOv2 feature (PCA -> RGB)"); axs[1].axis("off")
    fig.suptitle(title, fontsize=12); fig.savefig(path, dpi=130, bbox_inches="tight"); plt.close(fig)


def patch_feat_rgb(ext, rgb_path, out_path, title):
    """DINOv2 dense per-patch features -> PCA-RGB, upsampled to image size (RGB | patch-PCA side by
    side). Pure 2D DINOv2 quality on this RGB — no point cloud / projection / aggregation involved."""
    rgb = _read_rgb(rgb_path); H, W = rgb.shape[:2]
    feat = ext.extract(rgb)["feat"].float().cpu().numpy()              # (Df, Hp, Wp)
    Df, Hp, Wp = feat.shape
    pca = feat_to_rgb(feat.reshape(Df, -1).T).reshape(Hp, Wp, 3)       # per-patch PCA-RGB
    fig, axs = plt.subplots(1, 2, figsize=(18, 6))
    axs[0].imshow(rgb); axs[0].set_title("RGB"); axs[0].axis("off")
    axs[1].imshow(pca, extent=[0, W, H, 0], interpolation="bilinear")  # upsample patch grid to image
    axs[1].set_title("DINOv2 dense patch feature (PCA -> RGB)"); axs[1].axis("off")
    fig.suptitle(title, fontsize=12); fig.savefig(out_path, dpi=130, bbox_inches="tight"); plt.close(fig)


def overlay(path, rgb_path, xyz, instances, K, cam2world, title, labels=True):
    """Pred instances projected onto the RGB frame. labels=True annotates class/conf (-> labels_2D);
    labels=False is points-only (-> points_2D)."""
    rgb = _read_rgb(rgb_path); H, W = rgb.shape[:2]
    u, v, z = project(xyz, K, cam2world)
    vis = (z > 1e-6) & (u >= 0) & (u < W) & (v >= 0) & (v < H)
    fig, ax = plt.subplots(figsize=(10, 7)); ax.imshow(rgb)
    for i, ins in enumerate(instances):
        m = (ins["mask"] > 0) & vis
        if not m.any():
            continue
        col = CMAP[i % 20] / 255.0
        ax.scatter(u[m], v[m], s=10, color=col, alpha=0.6, linewidths=0)
        if labels:
            ax.annotate(f"{CLASS_NAMES[ins['cls']]} {ins['conf']:.2f}", (float(u[m].mean()), float(v[m].mean())),
                        color="white", fontsize=11, ha="center",
                        bbox=dict(boxstyle="round,pad=0.2", fc=col, ec="white", alpha=0.9))
    ax.axis("off"); ax.set_title(title, fontsize=11)
    fig.savefig(path, dpi=130, bbox_inches="tight"); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", default="wall_with_switch")
    ap.add_argument("--run", default="C_g01p128_v2")
    ap.add_argument("--ckpt", default="best.pt")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--eps", type=float, default=0.05)
    ap.add_argument("--min_samples", type=int, default=10)
    ap.add_argument("--min_cluster", type=int, default=20)
    ap.add_argument("--la_scale", type=float, default=1.0,
                    help="logit-adjust strength: 1=cal (SceneFun3D sparse prior), 0=raw. OOD scenes "
                         "with DENSE affordances need <1 — cal's sparse prior over-suppresses them")
    ap.add_argument("--conf_thresh", type=float, default=0.0,
                    help="drop instances with mean-conf below this (la=0 + conf_thresh = full recall, "
                         "then cut low-conf false positives on walls/pictures)")
    args = ap.parse_args()
    dev = torch.device(args.device)
    scan_dir = os.path.join(DATA, args.scan)
    out_dir = os.path.join(OUT, args.scan); os.makedirs(out_dir, exist_ok=True)

    xyz = read_ply_xyz(os.path.join(scan_dir, "colored.ply"))
    frames = read_frames(scan_dir)
    print(f"[iphone] {args.scan}: {len(xyz)} pts, {len(frames)} frames", flush=True)

    ext = DINOv2Extractor(device=str(dev))
    feat, obs = lift_features(xyz, frames, ext, dev)
    print(f"[lift] {int(obs.sum())}/{len(xyz)} points got DINOv2 features", flush=True)

    ck = torch.load(os.path.join(RUNS, args.run, args.ckpt), map_location=dev, weights_only=False)
    a = ck["args"]; gs = a["grid_size"]; log_prior = np.array(ck["log_prior"], np.float32)
    model = build_model("v1_ptv3", grid_size=gs, proj_dim=a.get("proj_dim", 64),
                        enable_flash=a.get("enable_flash", True)).to(dev)
    model.load_state_dict(ck["model"]); eval_safe(model)

    xyz_o, feat_o = xyz[obs].astype(np.float32), feat[obs].astype(np.float32)
    K = feat_o.shape[0]
    vox = grid_sample(xyz_o, feat_o, np.zeros(K, np.uint8), np.zeros(K, np.uint16), gs)
    coord = torch.from_numpy(vox["xyz"] - vox["xyz"].mean(0)).float().to(dev)
    ft = torch.from_numpy(vox["feat"].astype(np.float32)).to(dev)
    off_t = torch.tensor([coord.shape[0]], device=dev)
    with torch.no_grad(), torch.amp.autocast("cuda", enabled=True):
        sem, _ = model(coord, ft, off_t)
    sem = sem.float().cpu().numpy()
    cal_pred = (sem + log_prior).argmax(1); raw_pred = sem.argmax(1)
    rawc = {CLASS_NAMES[c]: int((raw_pred == c).sum()) for c in range(1, 10) if (raw_pred == c).any()}
    print(f"[diag] {len(sem)} voxels | cal fg {int((cal_pred > 0).sum())} | raw fg {int((raw_pred > 0).sum())}"
          f" | raw per-class {rawc}", flush=True)
    prob, pred = softmax_max(sem + args.la_scale * log_prior)          # la=1 cal / 0 raw; OOD needs <1
    obs_idx = np.nonzero(obs)[0]                                        # full-scan idx of observed pts
    inst = cluster(pred, prob, vox["xyz"], vox["inv"], obs_idx, len(xyz),
                   args.eps, args.min_samples, args.min_cluster, 0.0)
    if args.conf_thresh > 0:
        n0 = len(inst); inst = [i for i in inst if i["conf"] >= args.conf_thresh]
        print(f"[conf] kept {len(inst)}/{n0} instances (conf >= {args.conf_thresh})", flush=True)
    inst.sort(key=lambda i: -i["conf"])                                 # high-conf first
    print(f"[pred] {len(inst)} instances: "
          + (", ".join(f"{CLASS_NAMES[i['cls']]}({i['conf']:.2f})" for i in inst) or "(none)"), flush=True)

    write_ply(os.path.join(out_dir, "pred.ply"), xyz.astype(np.float32), colorize(len(xyz), inst))
    feat_rgb = np.full((len(xyz), 3), 185, np.uint8)
    feat_rgb[obs] = feat_to_rgb(feat[obs])                              # DINOv2 PCA->RGB (lift quality)
    write_ply(os.path.join(out_dir, "feat_pca.ply"), xyz.astype(np.float32), feat_rgb)
    ldir, pdir, fdir = (os.path.join(out_dir, d) for d in ("labels_2D", "points_2D", "feat_2D"))
    for d in (ldir, pdir, fdir):
        os.makedirs(d, exist_ok=True)
    for k, fr in enumerate(frames):
        ttl = f"{args.scan} frame{k} — {len(inst)} pred"
        overlay(os.path.join(ldir, f"p{k}_pred.png"), fr["rgb"], xyz, inst, fr["K"], fr["cam2world"], ttl, labels=True)
        overlay(os.path.join(pdir, f"p{k}_pred.png"), fr["rgb"], xyz, inst, fr["K"], fr["cam2world"], ttl, labels=False)
        overlay_feat(os.path.join(fdir, f"p{k}.point-feat-pca-rgb.png"), fr["rgb"], xyz, feat_rgb,
                     fr["K"], fr["cam2world"], f"{args.scan} frame{k} — point DINOv2 feature (PCA->RGB)")
        patch_feat_rgb(ext, fr["rgb"], os.path.join(fdir, f"p{k}.patch-feat-pca-rgb.png"),
                       f"{args.scan} frame{k} — dense patch DINOv2 feature")
    print(f"[saved] {out_dir}", flush=True)


if __name__ == "__main__":
    main()
