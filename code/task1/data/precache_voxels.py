"""precache_voxels.py — GridSample all scenes to 0.01 voxels, cache to a (job-scratch) dir.

v1 trains per-scene; reading 1.7TB raw feat from NFS each epoch is THE bottleneck. GridSample
ONCE here (1cm voxels) into a local-NVMe scratch dir, then training reads the small voxel cache
(local, fast) instead of NFS. Per scene -> npz(xyz f32, feat f16, cls u8, inst u16). Supports any
training grid >= 0.01 (training re-GridSamples the 0.01 voxels down to a coarser grid, cheap).

Run inside a long-lived 'precache_voxel' SLURM job that writes to ITS OWN scratch and then holds
(sleep), so same-node training jobs read /scratch/zixian/<that_jobid>/voxels. CPU-only (no GPU).
A `DONE` marker is touched at the end so training jobs can check readiness. Read-only on NFS caches.

  python src/data/precache_voxels.py --out_dir /scratch/zixian/$SLURM_JOB_ID/voxels --grid_size 0.01
"""
from __future__ import annotations
import os, sys, time, argparse
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import CODE  # noqa: E402
sys.path.insert(0, os.path.join(CODE, "task1"))
from data.scene_io import load_scene, grid_sample, FEAT_DIR   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_dir", required=True, help="scratch dir, e.g. /scratch/zixian/$SLURM_JOB_ID/voxels")
    ap.add_argument("--feat_dir", default=FEAT_DIR)
    ap.add_argument("--grid_size", type=float, default=0.01)
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    visits = sorted(f[:-4] for f in os.listdir(args.feat_dir) if f.endswith(".npz"))
    print(f"[precache_voxels] {len(visits)} scenes @ {args.grid_size}m -> {args.out_dir}", flush=True)
    t0 = time.time(); done = skip = 0
    for i, v in enumerate(visits):
        out = os.path.join(args.out_dir, f"{v}.npz")
        if os.path.exists(out) and not args.overwrite:
            skip += 1; continue
        s = load_scene(v)                                     # reads raw feat (~24GB peak) + labels + xyz
        vox = grid_sample(s["xyz"], s["feat"], s["cls"], s["inst"], args.grid_size)
        np.savez(out, xyz=vox["xyz"].astype(np.float32), feat=vox["feat"],      # feat already f16
                 cls=vox["cls"], inst=vox["inst"])
        done += 1
        print(f"  [{i+1}/{len(visits)}] {v}  {s['cls'].shape[0]:,}->{vox['cls'].shape[0]:,} vox  "
              f"cum {time.time()-t0:.0f}s", flush=True)
        del s, vox
    open(os.path.join(args.out_dir, "DONE"), "w").close()     # readiness marker for training jobs
    print(f"[done] cached {done}, skipped {skip} in {time.time()-t0:.0f}s -> {args.out_dir} (DONE touched)")


if __name__ == "__main__":
    main()
