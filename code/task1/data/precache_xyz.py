"""precache_xyz.py — cache per-scene observed-point xyz to small npy (COMPUTE node, run once).

v1 trains per-scene and needs xyz = P_full[observed_idx] EVERY epoch. Reading the laser-scan
ply each epoch (load_pointcloud) is slow over NFS. observed-xyz is tiny (N×3 fp32, ~140MB for
the largest 11.8M scene; whole 230-scene split is a few GB), so extract it ONCE here.
scene_io.load_scene then reads this cache instead of the ply.

Aligns 1:1 with feat rows (xyz[i] <-> feat[i]) via observed_idx. Read-only on feat/ply caches;
writes only under --out_dir.
  python src/data/precache_xyz.py                 # all scenes present in feat_dir
"""
from __future__ import annotations
import os, sys, time, argparse
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import CODE, FEATURE_CACHE, SCENEFUN3D, XYZ_CACHE  # noqa: E402
sys.path.insert(0, os.path.join(CODE, "task1", "features"))
from data_io import load_pointcloud   # noqa: E402

FEAT_DIR = FEATURE_CACHE
DATA_ROOT = SCENEFUN3D
OUT_DIR = XYZ_CACHE


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--feat_dir", default=FEAT_DIR)
    ap.add_argument("--data_root", default=DATA_ROOT)
    ap.add_argument("--out_dir", default=OUT_DIR)
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    visits = sorted(f[:-4] for f in os.listdir(args.feat_dir) if f.endswith(".npz"))
    print(f"[precache_xyz] {len(visits)} scenes -> {args.out_dir}", flush=True)
    t0 = time.time()
    done = skip = 0
    for i, v in enumerate(visits):
        out = os.path.join(args.out_dir, f"{v}.npy")
        if os.path.exists(out) and not args.overwrite:
            skip += 1
            continue
        with np.load(os.path.join(args.feat_dir, f"{v}.npz")) as fd:   # lazy: only observed_idx
            obs = fd["observed_idx"]
        P_full = load_pointcloud(args.data_root, v)["P_full"]          # reads ply
        assert int(obs.max()) < P_full.shape[0], f"{v}: observed_idx OOB vs ply"
        xyz = P_full[obs].astype(np.float32)                          # (K,3), row-aligned to feat
        np.save(out, xyz)
        done += 1
        print(f"  [{i+1}/{len(visits)}] {v}  K={xyz.shape[0]:,}  cum {time.time()-t0:.0f}s", flush=True)
        del P_full
    print(f"[done] cached {done}, skipped {skip} (existing) in {time.time()-t0:.0f}s -> {args.out_dir}")


if __name__ == "__main__":
    main()
