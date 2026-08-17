"""
lift/lift_to_pointcloud.py — multi-view DINOv2 feature lift onto the laser-scan
point cloud (Phase 1, step 3). One sparse feature cache file per scene.

Pipeline, per scene (the scan is read ONCE and pooled over ALL videos of the visit,
which share one laser-scan world frame):
    load_pointcloud(visit)               # scan + crop mask, once
    for each video, for each frame:
        project_gpu(P, K, cam2world, depth) -> visible mask + (u,v)   # all on GPU
        DINOv2 dense features (fp16 autocast); bilinearly sample at the visible (u,v)
        L2-normalize each obs; accumulate (sum + count) per point IN CHUNKS so the
        per-frame sample tensor can never blow up VRAM
    per point: mean of its unit observations; keep only points seen >= 1 time.

Aggregation (Phase 1): per-obs L2-norm then MEAN (OpenScene-style). NOT re-normalized,
so ||feat|| in (0,1] is a free multi-view-coherence signal (->1 views agree, ->0
scattered), complementing the integer view_count.

Cache schema (sparse .npz per visit; unobserved points absent):
    observed_idx : (K,)    int32   indices into the FULL laser scan
    feat         : (K, Df) float16 mean (unit) DINOv2 feature; Df=1024 for ViT-L/14
    view_count   : (K,)    uint16  #frames each point was visible in
    + provenance scalars: model, stride, target_long_side, feat_dim, eps, agg

Deferred (orthogonal, both lossy, NOT here): PCA dim-reduction (cut feature COLUMNS;
fit on the cache first) and voxel downsampling (cut point ROWS). Only when storage forces it.
"""

import os
import sys
import numpy as np
import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_io import load_pointcloud, load_frames   # noqa: E402
from dinov2_extract import DINOv2Extractor          # noqa: E402

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import FEATURE_CACHE, SCENEFUN3D  # noqa: E402

EPS = 0.03            # occlusion tolerance (m); MUST match data_io.project default
CHUNK = 256_000       # max visible points sampled at once -> caps the per-frame VRAM transient.
                      # The sample -> .float() -> normalize chain makes ~3 copies, so at 1M this
                      # peaked ~12GB and OOMed mid-frame even on a dedicated 48GB card (a 17.5GB
                      # accum still died); 256k -> ~3GB transient AND fragments the allocator far
                      # less. More chunks/frame but each is cheap -> negligible time cost.
AGG = "mean_unit_noRenorm"   # provenance tag for the aggregation scheme


def discover_videos(data_root, visit_id):
    """All video_ids under a visit (numeric subdirs). A scene may have several iPad
    captures, all registered to the same laser-scan frame, so pooling is valid.
    Non-video subdirs (e.g. translated_jsons) are skipped by the isdigit() filter."""
    vis_dir = os.path.join(data_root, visit_id)
    return [d for d in sorted(os.listdir(vis_dir))
            if d.isdigit() and os.path.isdir(os.path.join(vis_dir, d))]


def _pick_accum_device(M, feat_dim, model_device, want):
    """Device for the (M, feat_dim) fp32 accumulator. GPU is faster (no per-frame H2D
    copy + fast index_add_) but the buffer is 16-53GB and OOMs a 48GB card on the
    biggest scenes. 'auto': GPU when buffer + headroom fits free VRAM, else CPU.
    'cpu'/'cuda' force it. (GPU index_add_ is NOT bit-deterministic; use 'cpu' for
    bit-exact reproducibility, e.g. on the val/eval split.)"""
    if want == "cpu" or str(model_device) == "cpu":
        return torch.device("cpu")
    if want == "cuda":
        return torch.device(model_device)
    torch.cuda.empty_cache()              # free torch's cached blocks so 'free' is real
    free, _ = torch.cuda.mem_get_info()   # (else every scene after #1 mis-reads free -> CPU)
    # 14GB headroom: the chunked per-frame transient (~4GB) + ViT-L activations + GPU-projection
    # intermediates + allocator fragmentation empirically cost ~14GB on big scenes (a 35GB accum
    # OOMed at frame 4000 with only 8GB). So accum >~32GB (M>~8.4M) -> CPU UPFRONT, never wasting
    # thousands of GPU frames before an OOM-then-CPU-restart. (run_lift.sh's expandable_segments
    # further cuts fragmentation.) The ViT-L forward stays on GPU regardless of accum device.
    return torch.device(model_device) if M * feat_dim * 4 + 14 * 1024**3 < free else torch.device("cpu")


@torch.no_grad()
def project_gpu(P, K, cam2world, depth, eps, device):
    """GPU port of data_io.project: world points -> (visible mask, u, v) for one frame.
    Mirrors the numpy reference EXACTLY (world2cam=inv(cam2world); pinhole u=fx*X/Z+cx;
    round; in-image bounds; |z-d|<eps occlusion). Cross-checked against the numpy version
    frame-by-frame in the D2 verification (float32 vs float64 -> sub-pixel diffs only).

    Args:
        P    : (M,3) float32 world coords already ON `device` (loaded once per scene).
        depth: (H,W) numpy GT depth in metres.
    Returns dict(visible (M,) bool, u (M,) float, v (M,) float), all on `device`.
    """
    H, W = depth.shape
    depth_t = torch.from_numpy(np.ascontiguousarray(depth)).to(device).float()
    c2w = torch.as_tensor(np.asarray(cam2world), device=device, dtype=torch.float32)
    w2c = torch.linalg.inv(c2w)
    R, t = w2c[:3, :3], w2c[:3, 3]
    Pc = P @ R.T + t
    z = Pc[:, 2]
    fx, fy, cx, cy = float(K[0, 0]), float(K[1, 1]), float(K[0, 2]), float(K[1, 2])
    u = fx * Pc[:, 0] / z + cx
    v = fy * Pc[:, 1] / z + cy
    ui = torch.round(u).long()
    vi = torch.round(v).long()
    in_view = (z > 1e-6) & (ui >= 0) & (ui < W) & (vi >= 0) & (vi < H)
    visible = torch.zeros(P.shape[0], dtype=torch.bool, device=device)
    idx = torch.nonzero(in_view, as_tuple=True)[0]
    if idx.numel():
        d = depth_t[vi[idx], ui[idx]]
        ok = (d > 1e-6) & ((z[idx] - d).abs() < eps)
        visible[idx[ok]] = True
    return dict(visible=visible, u=u, v=v)


@torch.no_grad()
def lift_scene(data_root, visit_id, ext, video_ids=None, accum_device="auto",
               stride=1, verbose=True):
    """Lift DINOv2 features onto the cropped laser scan for one scene.

    Returns dict(observed_idx (K,) int32, feat (K,Df) float16, view_count (K,) uint16,
                 n_kept, n_frames) -- or None if the visit has no video dirs.
    """
    if video_ids is None:
        video_ids = discover_videos(data_root, visit_id)
    if not video_ids:
        return None

    # --- geometry: read the laser scan + crop mask ONCE per scene (not per video) ---
    pc = load_pointcloud(data_root, visit_id)
    kept_idx = pc["kept_idx"]
    M = kept_idx.shape[0]
    P_gpu = torch.from_numpy(np.ascontiguousarray(pc["P_keep"])).to(ext.device).float()

    adev = _pick_accum_device(M, ext.feat_dim, ext.device, accum_device)
    accum = torch.zeros((M, ext.feat_dim), dtype=torch.float32, device=adev)
    count = torch.zeros(M, dtype=torch.float32, device=adev)
    if verbose:
        print(f"  [accum] M={M:,} kept -> {accum.numel()*4/1e9:.1f}GB on {adev} "
              f"(cpu=>RAM / cuda=>VRAM)")

    n_frames = 0
    for vid in video_ids:
        fdat = load_frames(data_root, visit_id, vid)
        parser, frames = fdat["parser"], fdat["frames"][::stride]
        for i, fr in enumerate(frames):
            depth = parser.read_depth_frame(fr["depth"])            # (H,W) metres
            pr = project_gpu(P_gpu, fr["K"], fr["cam2world"], depth, EPS, ext.device)
            vis = torch.nonzero(pr["visible"], as_tuple=True)[0]    # (n_vis,) on GPU
            if vis.numel() == 0:
                continue
            rgb = parser.read_rgb_frame(fr["rgb"])                  # (H,W,3) uint8
            fd = ext.extract(rgb)
            u, v = pr["u"], pr["v"]
            # chunk the visible points so the per-frame sample tensor stays bounded.
            for s in range(0, vis.numel(), CHUNK):
                sub = vis[s:s + CHUNK]
                f = F.normalize(ext.sample(fd, u[sub], v[sub]).float(), dim=1).to(adev)
                sa = sub.to(adev)
                accum.index_add_(0, sa, f)
                count.index_add_(0, sa, torch.ones(sub.numel(), device=adev))
            n_frames += 1
            if verbose and (n_frames % 100 == 0):
                print(f"  [{visit_id}/{vid}] frame {i+1}/{len(frames)} "
                      f"(total {n_frames})", flush=True)

    # Reduce on CPU: doing accum[obs] (gather) + the division ON the GPU needs ~3x the accum
    # size in VRAM (a 17.5GB accum OOMed needing ~48GB at scene end). Moving accum/count to CPU
    # first frees the GPU and caps VRAM at the per-frame peak; the one ~accum-size copy is cheap.
    accum, count = accum.cpu(), count.cpu()
    obs = torch.nonzero(count > 0, as_tuple=True)[0]
    mean = accum[obs] / count[obs].unsqueeze(1)                     # mean of unit vecs
    return dict(
        observed_idx=kept_idx[obs.numpy()].astype(np.int32),
        feat=mean.half().numpy(),
        view_count=count[obs].clamp(max=65535).numpy().astype(np.uint16),
        n_kept=M, n_frames=n_frames,
    )


def read_split_visits(data_root, split):
    """Unique visit_ids (scenes) for a split. split in {val, train, all}:
    val = split0 (30), train = split1 (200), all = train+val (230). The *_set.csv files
    (visit_id,video_id pairs) are generated by scenefun3d make_video_list.py; we dedupe
    to scenes (the lift pools all videos)."""
    bfl = os.path.join(data_root, "benchmark_file_lists")
    csv = {"val": "val_set.csv", "train": "train_set.csv", "all": "train_val_set.csv"}[split]
    with open(os.path.join(bfl, csv)) as f:
        next(f)  # skip "visit_id,video_id" header
        visits = [ln.split(",")[0] for ln in f if ln.strip()]
    return sorted(set(visits))


def load_cache(path, **expect):
    """Load a feature cache .npz. If `expect` is given (e.g. model="dinov2_vitl14",
    stride=1), assert the cache was produced with those params -> catch silent train/val
    or config mismatches at load time. Returns the NpzFile."""
    z = np.load(path, allow_pickle=False)
    for k, want in expect.items():
        got = z[k].item() if z[k].ndim == 0 else z[k]
        if got != want:
            raise ValueError(f"{path}: cache {k}={got!r} != expected {want!r}")
    return z


def _write_pca_ply(data_root, visit_id, R, out_dir):
    """PCA the lifted per-point features -> RGB, write a colored point cloud (the lift's
    decisive 3D sanity: same object -> same color). Re-reads the scan once (viz only).
    PCA is fit on a subsample to avoid SVD-ing the full (K x 1024) matrix."""
    import open3d as o3d
    P_obs = load_pointcloud(data_root, visit_id)["P_full"][R["observed_idx"]]
    f = R["feat"].astype(np.float32)
    f = f - f.mean(0, keepdims=True)
    sub = f[np.random.default_rng(0).choice(len(f), min(50000, len(f)), replace=False)]
    Vt = np.linalg.svd(sub, full_matrices=False)[2]
    pca = f @ Vt[:3].T
    pca = (pca - pca.min(0)) / (np.ptp(pca, axis=0) + 1e-8)
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(P_obs)
    pc.colors = o3d.utility.Vector3dVector(pca)
    ply = os.path.join(out_dir, f"{visit_id}_pca.ply")
    o3d.io.write_point_cloud(ply, pc)
    print(f"  [saved] {ply}  (open in meshlab/viser; same object -> same color)")


def process_scene(data_root, visit_id, ext, out_dir, video_ids=None, viz_ply=False,
                  accum_device="auto", stride=1):
    """Lift one scene, print stats, write its sparse .npz (+ provenance). Returns bytes."""
    R = lift_scene(data_root, visit_id, ext, video_ids=video_ids,
                   accum_device=accum_device, stride=stride)
    if R is None:
        print(f"  [warn] {visit_id}: no video dirs found -> skipped")
        return 0
    K, vc = len(R["observed_idx"]), R["view_count"]
    cov = 100.0 * K / max(R["n_kept"], 1)
    fnorm = np.linalg.norm(R["feat"].astype(np.float32), axis=1)
    print(f"[lift {visit_id}] frames={R['n_frames']} kept={R['n_kept']:,} "
          f"observed={K:,} ({cov:.1f}%)  view_count mean={vc.mean():.1f} max={vc.max()}  "
          f"feat-norm mean={fnorm.mean():.2f} (coherence ->1=agree)")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{visit_id}.npz")
    # np.savez (NOT _compressed): fp16 features are high-entropy -> near-zero compression
    # for ~minutes/scene of CPU; uncompressed is faster and still fits the disk budget.
    np.savez(out_path, observed_idx=R["observed_idx"], feat=R["feat"],
             view_count=R["view_count"],
             # provenance (C1): stamp the extraction config so caches can't silently mix.
             model=ext.model_name, stride=stride, target_long_side=ext.target_long_side,
             feat_dim=ext.feat_dim, eps=EPS, agg=AGG)
    sz = os.path.getsize(out_path)
    print(f"  [saved] {out_path}  ({sz/1e9:.2f} GB)")
    if viz_ply:
        _write_pca_ply(data_root, visit_id, R, out_dir)
    return sz


if __name__ == "__main__":
    import argparse
    import time
    import traceback

    ap = argparse.ArgumentParser()
    sel = ap.add_mutually_exclusive_group(required=True)
    sel.add_argument("--visit_id", help="single scene")
    sel.add_argument("--split", choices=["val", "train", "all"],
                     help="batch: val=split0(30), train=split1(200), all(230)")
    ap.add_argument("--data_root", default=SCENEFUN3D)
    ap.add_argument("--video_id", default=None, help="single-scene only; default = ALL videos")
    ap.add_argument("--out_dir", default=FEATURE_CACHE)
    ap.add_argument("--model", default="dinov2_vitl14")
    ap.add_argument("--accum_device", choices=["auto", "cuda", "cpu"], default="auto",
                    help="accumulator location: auto=GPU when it fits VRAM else CPU; "
                         "cpu=safe+bit-deterministic; cuda=force")
    ap.add_argument("--stride", type=int, default=1,
                    help="process every Nth frame (1=ALL frames; >1 only for speed tests)")
    ap.add_argument("--viz_ply", action="store_true", help="also write a PCA-RGB .ply per scene")
    ap.add_argument("--overwrite", action="store_true", help="re-lift scenes already cached")
    ap.add_argument("--max_cache_gb", type=float, default=2300.0,
                    help="stop batch if out_dir grows past this (disk guard; ~2.5TB hard cap)")
    ap.add_argument("--shard", default=None, metavar="i/N",
                    help="process only scene-shard i of N (e.g. 0/4); used by run_lift.sh per-GPU worker")
    ap.add_argument("--device", default=None,
                    help="cuda:g to pin ONE GPU (multi-GPU workers); default = auto. Does NOT touch "
                         "CUDA_VISIBLE_DEVICES -- just selects among the GPUs SLURM already gave the job.")
    args = ap.parse_args()

    if args.device:
        device = args.device
        if device.startswith("cuda"):
            torch.cuda.set_device(torch.device(device))  # make mem_get_info/empty_cache target THIS gpu
    else:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[init] device={device}  model={args.model}  stride={args.stride}")
    ext = DINOv2Extractor(model_name=args.model, device=device)

    if args.visit_id:
        visits, video_ids = [args.visit_id], ([args.video_id] if args.video_id else None)
    else:
        visits, video_ids = read_split_visits(args.data_root, args.split), None
        print(f"[batch] split={args.split}  {len(visits)} scenes")
    if args.shard:
        si, sn = (int(x) for x in args.shard.split("/"))
        visits = visits[si::sn]   # strided -> each shard gets a size-balanced mix of scenes
        print(f"[shard {args.shard}] this job runs {len(visits)} scenes")

    # disk guard: scan once at start, then track with `cur` (no O(n^2) re-scan).
    cur = (sum(os.path.getsize(os.path.join(args.out_dir, f)) for f in os.listdir(args.out_dir))
           if os.path.isdir(args.out_dir) else 0)
    cap = args.max_cache_gb * 1e9

    t0, failed = time.time(), []
    for i, v in enumerate(visits):
        if os.path.exists(os.path.join(args.out_dir, f"{v}.npz")) and not args.overwrite:
            print(f"[skip {i+1}/{len(visits)}] {v} (cached)")
            continue
        if cur >= cap:
            print(f"[STOP] cache {cur/1e12:.2f}TB >= cap {args.max_cache_gb/1000:.2f}TB; "
                  f"{len(visits)-i} scenes left. Free space or raise --max_cache_gb.")
            break
        print(f"[scene {i+1}/{len(visits)}] {v}")
        err = None
        try:
            cur += process_scene(args.data_root, v, ext, args.out_dir,
                                 video_ids=video_ids, viz_ply=args.viz_ply,
                                 accum_device=args.accum_device, stride=args.stride)
        except RuntimeError as e:
            err = str(e)
            # The exception traceback pins the failed scene's GPU accum; clear the frame
            # locals so empty_cache() can actually release that VRAM before the retry.
            traceback.clear_frames(e.__traceback__)
        if err is not None:
            if device.startswith("cuda"):
                torch.cuda.empty_cache()
            if "out of memory" in err.lower():
                print(f"  [OOM] {v} -> retry on CPU :: {err.strip()[:260]}", flush=True)
                try:
                    cur += process_scene(args.data_root, v, ext, args.out_dir,
                                         video_ids=video_ids, viz_ply=args.viz_ply,
                                         accum_device="cpu", stride=args.stride)
                except Exception as e2:
                    print(f"  [FAIL] {v}: {e2}", flush=True); failed.append(v)
            else:
                print(f"  [FAIL] {v}: {err[:200]}", flush=True); failed.append(v)
    msg = f"[done] {time.time()-t0:.0f}s; cache now {cur/1e12:.2f}TB"
    if failed:
        msg += f"; FAILED {len(failed)}: {failed} -> rerun: --visit_id <id> --accum_device cpu"
    print(msg)
