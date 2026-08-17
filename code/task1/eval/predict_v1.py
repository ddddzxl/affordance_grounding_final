#!/usr/bin/env python3
"""predict_v1.py — v1 (PTv3) inference -> instances -> official instance AP.

Per val scene: GridSample (same grid as training) -> PTv3 forward (eval-safe: convs in train()
for spconv Native, BN/dropout off, see scene_train) -> per-VOXEL sem logits + offset -> per-class
DBSCAN -> map voxels back to observed points (GridSample inverse) -> scatter to full scan -> RLE
-> official evaluate.

Two calibrations (like v0 la_scale): cal = argmax(z+logπ) (== v0 best convention, the 0.53/0.39
protocol), raw = argmax(z). Two instancing modes: raw-xyz DBSCAN (default — USE for step2, where the
offset head is untrained) vs offset-shift DBSCAN (--use_offset, for step3 once offset is trained).

  python src/eval/predict_v1.py --run A_g01p64 --device cuda:0               # step2: raw-DBSCAN, both cals
  python src/eval/predict_v1.py --run <step3run> --device cuda:0 --use_offset

Forward is full-scene (PT needs the neighborhood). If a val scene OOMs -> tiling is the fix (TODO,
flagged, not yet implemented).
"""
from __future__ import annotations
import os, sys, argparse, subprocess
import numpy as np
import torch
from sklearn.cluster import DBSCAN

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import CODE, FEATURE_CACHE, GT_VAL, RUNS, SCENEFUN3D, TASK1, TOOLKIT  # noqa: E402
sys.path.insert(0, os.path.join(CODE, "task1"))
sys.path.insert(0, os.path.join(CODE, "task1", "features"))
sys.path.insert(0, TOOLKIT)
from data.scene_io import grid_sample                                       # noqa: E402
from data_io import load_pointcloud                                         # noqa: E402
from models import build_model                                              # noqa: E402
from eval.functionality_segmentation.eval_utils.rle import rle_encode       # noqa: E402

FEAT_DIR = FEATURE_CACHE
DATA_ROOT = SCENEFUN3D
RESULTS = os.path.join(TASK1, "v1")   # v1 eval outputs


def read_val_visits():
    return sorted(f[:-4] for f in os.listdir(GT_VAL) if f.endswith(".txt"))


def eval_safe(model):
    """spconv Native (train-mode conv) but BN frozen (running stats) + dropout off — same as
    scene_train.eval_pointwise (eval() picks implicit_gemm which fails on PTv3 xCPE)."""
    model.train()
    for m in model.modules():
        if isinstance(m, (torch.nn.BatchNorm1d, torch.nn.Dropout)) or type(m).__name__ == "DropPath":
            m.eval()                                     # freeze BN + dropout + PTv3 backbone DropPath(0.3)
    model.sem_head.eval(); model.offset_head.eval()


@torch.no_grad()
def forward_scene(model, visit, dev, grid_size):
    """Returns (sem (V,10) f32, off (V,3) f32, xyz_vox (V,3), inv (K,), obs (K,), n_full)."""
    with np.load(os.path.join(FEAT_DIR, f"{visit}.npz")) as fd:
        feat, obs = fd["feat"], fd["observed_idx"]
    P_full = load_pointcloud(DATA_ROOT, visit)["P_full"]
    n_full = P_full.shape[0]
    xyz = P_full[obs].astype(np.float32)
    K = feat.shape[0]
    vox = grid_sample(xyz, feat, np.zeros(K, np.uint8), np.zeros(K, np.uint16), grid_size)
    coord = torch.from_numpy(vox["xyz"] - vox["xyz"].mean(0)).float().to(dev)
    f = torch.from_numpy(vox["feat"].astype(np.float32)).to(dev)
    off_t = torch.tensor([coord.shape[0]], device=dev)
    with torch.amp.autocast("cuda", enabled=True):
        sem, pred_off = model(coord, f, off_t)
    return (sem.float().cpu().numpy(), pred_off.float().cpu().numpy(),
            vox["xyz"], vox["inv"], obs, n_full)


def cluster(pred_vox, prob_vox, cluster_xyz, inv, obs, n_full,
            eps, min_samples, min_cluster, prob_thresh):
    """Per-class DBSCAN on voxels -> map each voxel instance back to observed points via `inv`.
    min_cluster gates on OBSERVED-point count (comparable to oracle/v0). conf = mean voxel prob."""
    voxel_inst = np.full(pred_vox.shape[0], -1, np.int64)
    meta = []; gid = 0
    for c in range(1, 10):
        sel = np.nonzero((pred_vox == c) & (prob_vox > prob_thresh))[0]
        if sel.size < 1:
            continue
        labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(cluster_xyz[sel])
        for lab in np.unique(labels):
            if lab == -1:
                continue
            members = sel[labels == lab]
            voxel_inst[members] = gid
            meta.append((gid, c, float(prob_vox[members].mean()))); gid += 1
    point_inst = voxel_inst[inv]                          # observed point -> instance id
    out = []
    for g, c, conf in meta:
        pts = np.nonzero(point_inst == g)[0]
        if pts.size < min_cluster:
            continue
        mask = np.zeros(n_full, np.uint8); mask[obs[pts]] = 1
        out.append({"mask": mask, "cls": c, "conf": conf})
    return out


def softmax_max(logits):
    z = logits - logits.max(1, keepdims=True)
    e = np.exp(z); p = e / e.sum(1, keepdims=True)
    return p.max(1), p.argmax(1)


def run_eval(sub_dir):
    res = subprocess.run([sys.executable, "-m", "eval.functionality_segmentation.evaluate",
                          "--pred_dir", sub_dir, "--gt_dir", GT_VAL],
                         cwd=TOOLKIT, capture_output=True, text=True)
    return res.stdout + ("\n=== stderr ===\n" + res.stderr if res.stderr.strip() else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--ckpt", default="best.pt")
    ap.add_argument("--eps", type=float, default=0.05)
    ap.add_argument("--min_samples", type=int, default=10)
    ap.add_argument("--min_cluster", type=int, default=20)
    ap.add_argument("--prob_thresh", type=float, default=0.0)
    ap.add_argument("--use_offset", action="store_true", help="offset-shift DBSCAN (step3); else raw-xyz")
    ap.add_argument("--cals", default="cal,raw", help="comma list: cal (z+log prior) / raw (z)")
    args = ap.parse_args()
    dev = torch.device(args.device)

    ck = torch.load(os.path.join(RUNS, args.run, args.ckpt), map_location=dev, weights_only=False)
    a = ck["args"]; grid_size = a["grid_size"]
    log_prior = np.array(ck["log_prior"], np.float32)
    model = build_model("v1_ptv3", grid_size=grid_size, proj_dim=a.get("proj_dim", 64),
                        enable_flash=a.get("enable_flash", True)).to(dev)
    model.load_state_dict(ck["model"]); eval_safe(model)
    print(f"[predict_v1] {args.run} ep{ck['epoch']} grid {grid_size} proj {a.get('proj_dim',64)} "
          f"use_offset={args.use_offset}", flush=True)

    visits = read_val_visits()
    out_root = os.path.join(RESULTS, args.run); os.makedirs(out_root, exist_ok=True)
    cals = [c.strip() for c in args.cals.split(",")]

    scene_cache = {}                                       # forward ONCE per scene (expensive), cluster per cal
    for vi, v in enumerate(visits):
        scene_cache[v] = forward_scene(model, v, dev, grid_size)
        print(f"  [{vi+1}/{len(visits)}] {v}  {scene_cache[v][0].shape[0]:,} vox", flush=True)

    suffix = "_off" if args.use_offset else ""
    for cal in cals:
        sub_dir = os.path.join(out_root, f"submission_v1_{cal}{suffix}")
        mask_dir = os.path.join(sub_dir, "predicted_masks"); os.makedirs(mask_dir, exist_ok=True)
        n_inst = 0
        for v in visits:
            sem, off, xyz_vox, inv, obs, n_full = scene_cache[v]
            logits = sem + log_prior if cal == "cal" else sem
            prob, pred = softmax_max(logits)
            cxyz = xyz_vox + off if args.use_offset else xyz_vox
            inst = cluster(pred, prob, cxyz, inv, obs, n_full,
                           args.eps, args.min_samples, args.min_cluster, args.prob_thresh)
            lines = []
            for k, ins in enumerate(inst):
                mf = f"{v}_{k:03d}.txt"
                with open(os.path.join(mask_dir, mf), "w") as fh:
                    fh.write(rle_encode(ins["mask"]))
                lines.append(f"predicted_masks/{mf} {ins['cls']} {ins['conf']:.4f}")
            if not lines:                                  # zero-instance scene -> dummy empty mask
                mf = f"{v}_000.txt"
                with open(os.path.join(mask_dir, mf), "w") as fh:
                    fh.write("")
                lines.append(f"predicted_masks/{mf} 1 0.0")
            with open(os.path.join(sub_dir, f"{v}.txt"), "w") as fh:
                fh.write("\n".join(lines))
            n_inst += len(inst)
        out = run_eval(sub_dir)
        with open(os.path.join(out_root, f"eval_v1_{cal}{suffix}.txt"), "w") as fh:
            fh.write(out)
        avg = [l for l in out.splitlines() if l.strip().startswith("average")]
        print(f"[{cal}{suffix}] {n_inst} inst | {avg[0].strip() if avg else '(no average line)'}", flush=True)


if __name__ == "__main__":
    main()
