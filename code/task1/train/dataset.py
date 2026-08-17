"""dataset.py — load the balanced pool + split in-train val BY SCENE.

v0 is point-independent, so we do NOT use a torch Dataset/DataLoader (per-point
__getitem__ over 17M points is slow); train.py samples index batches directly. This
module loads the pool into RAM and produces train/val index sets split BY pool_scene:
same-scene points are highly correlated, so a per-point split would leak and inflate
val metrics. (v1's PointTransformer will add a SceneDataset here.)
"""
from __future__ import annotations
import os
import numpy as np


def load_pool(pool_dir: str, ram: bool = True):
    """Returns (X (N,1024) fp16, y (N,) int, scene (N,) uint16). ram=True loads X fully
    into RAM (~36GB; host ~792GB); ram=False mmaps (page cache fills during epoch 1)."""
    pool_dir = os.path.expanduser(pool_dir)
    X = np.load(os.path.join(pool_dir, "pool_X.npy"), mmap_mode=None if ram else "r")
    y = np.load(os.path.join(pool_dir, "pool_y.npy"))
    scene = np.load(os.path.join(pool_dir, "pool_scene.npy"))
    return X, y, scene


def scene_split(scene: np.ndarray, n_val_scenes: int, seed: int):
    """Hold out `n_val_scenes` WHOLE scenes (by pool_scene id) as in-train val.
    Returns (train_idx, val_idx, val_scene_ids). n_val_scenes<=0 -> all-train, empty val."""
    n = scene.shape[0]
    if n_val_scenes <= 0:
        return np.arange(n), np.empty(0, dtype=np.int64), []
    uniq = np.unique(scene)
    rng = np.random.default_rng(seed)
    val_scenes = rng.choice(uniq, size=min(n_val_scenes, uniq.size), replace=False)
    is_val = np.isin(scene, val_scenes)
    val_idx = np.nonzero(is_val)[0]
    train_idx = np.nonzero(~is_val)[0]
    return train_idx, val_idx, sorted(int(s) for s in val_scenes)
