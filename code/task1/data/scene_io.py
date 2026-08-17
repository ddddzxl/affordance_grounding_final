"""scene_io.py — per-scene loading + GridSampling for v1 (PTv3, per-scene, needs neighborhood).

Unlike v0's balanced pool (point-independent, pre-sampled once), v1 STREAMS one scene at a
time — PT needs the full neighborhood, so we can't point-sample. Per scene:
  load feat(K,1024 fp16)+observed_idx + cls/inst(K,) + xyz=P_full[observed_idx]   (row-aligned)
  -> GridSampling to grid_size voxels (downsample; PTv3 does NOT dedupe internally -> this is
     what actually controls point count / GPU memory)
  -> per-fg-instance centroid offset target (PointGroup-style).

Streaming keeps RAM peak at ONE scene (max ~24GB feat), never the full 1.7TB. Read-only on
the feature/label cache.
"""
from __future__ import annotations
import os, sys
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import CODE, FEATURE_CACHE, LABEL_CACHE, SCENEFUN3D, XYZ_CACHE  # noqa: E402
sys.path.insert(0, os.path.join(CODE, "task1", "features"))
from data_io import load_pointcloud   # noqa: E402 — reuse lift loader; observed_idx is FULL-scan space

FEAT_DIR = FEATURE_CACHE
LABEL_DIR = LABEL_CACHE
DATA_ROOT = SCENEFUN3D
XYZ_CACHE = XYZ_CACHE   # precache_xyz.py output


def load_scene(visit: str, data_root: str = DATA_ROOT, feat_dir: str = FEAT_DIR,
               label_dir: str = LABEL_DIR, xyz_dir: str = XYZ_CACHE) -> dict:
    """Returns dict(feat (K,1024) fp16, xyz (K,3) fp32, cls (K,) uint8, inst (K,) uint16),
    all row-aligned: feat[i] <-> xyz[i] <-> cls[i] <-> inst[i] (observed-point order).
    xyz from the precache (precache_xyz.py) if present, else from the laser-scan ply."""
    with np.load(os.path.join(label_dir, f"{visit}.npz")) as ld:
        cls, inst = ld["cls"], ld["inst"]
    with np.load(os.path.join(feat_dir, f"{visit}.npz")) as fd:
        feat = fd["feat"]                                   # (K,1024) fp16, materialized
        obs = fd["observed_idx"]
    assert feat.shape[0] == cls.shape[0] == inst.shape[0], \
        f"{visit}: K mismatch feat {feat.shape[0]} / cls {cls.shape[0]} / inst {inst.shape[0]}"
    xyz_path = os.path.join(xyz_dir, f"{visit}.npy")
    if os.path.exists(xyz_path):                            # fast path: precached observed-xyz
        xyz = np.load(xyz_path)
        assert xyz.shape[0] == feat.shape[0], f"{visit}: xyz cache K {xyz.shape[0]} != feat {feat.shape[0]}"
    else:                                                   # fallback: read ply (slow over NFS)
        P_full = load_pointcloud(data_root, visit)["P_full"]
        assert int(obs.max()) < P_full.shape[0], f"{visit}: observed_idx OOB vs ply"
        xyz = P_full[obs].astype(np.float32)
    return dict(feat=feat, xyz=xyz, cls=cls, inst=inst)


def grid_sample(xyz: np.ndarray, feat: np.ndarray, cls: np.ndarray, inst: np.ndarray,
                grid_size: float) -> dict:
    """Voxel downsample by keeping ONE representative point per grid_size voxel (Pointcept
    train-mode style: no feat/label mixing). Returns voxelized arrays + inverse map
    (orig point -> voxel row) for inference map-back.

    PTv3's forward does NOT dedupe points, so this is what controls point count / memory.
    """
    gc = np.floor((xyz - xyz.min(0)) / grid_size).astype(np.int64)   # voxel index, >=0
    # pack 3D voxel index into one int64 key (each dim < 2^21 = 2M voxels @1cm -> 20km, safe)
    key = (gc[:, 0] << 42) | (gc[:, 1] << 21) | gc[:, 2]
    _, rep, inv = np.unique(key, return_index=True, return_inverse=True)
    return dict(xyz=xyz[rep], feat=feat[rep], cls=cls[rep], inst=inst[rep], inv=inv)


def offset_target(xyz: np.ndarray, cls: np.ndarray, inst: np.ndarray) -> np.ndarray:
    """Per-point offset to its instance centroid (PointGroup); 0 for bg/exclude.
    Instance key = (cls,inst) -> unique whether inst is scene-global or per-class.
    NOTE: centroid over the (voxelized) points the model sees -> self-consistent with the
    shift+cluster at inference. (offset_oracle's 89.2 is over un-voxelized observed points;
    voxelization is a separate, small resolution loss — re-anchor later if needed.)
    """
    gt = np.zeros_like(xyz, dtype=np.float32)
    fg = (cls >= 1) & (cls <= 9)
    key = cls.astype(np.int64) * 1000 + inst.astype(np.int64)
    for k in np.unique(key[fg]):
        m = (key == k) & fg
        gt[m] = xyz[m].mean(0) - xyz[m]
    return gt
