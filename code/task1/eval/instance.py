"""instance.py — per-point class predictions -> instances (DBSCAN) + full-scan RLE.

For each affordance class, DBSCAN on the 3D coords of points predicted as that class;
each cluster = one instance (full-scan binary mask via observed_idx, class,
confidence = mean class-prob over the cluster). Known failure mode (baseline §8):
adjacent same-class instances merge — eps can't fix it at the root; v1's offset /
connected-components is the cure. RLE reuses the official toolkit rle.py.

Deps: scikit-learn (DBSCAN). Complexity: DBSCAN ~O(n log n) per class via KD-tree;
n = points predicted as that class in one scene (a few k typically), fine for 30 val scenes.
"""
from __future__ import annotations
import numpy as np
from sklearn.cluster import DBSCAN


def cluster_instances(pred: np.ndarray, prob: np.ndarray, observed_idx: np.ndarray,
                      xyz: np.ndarray, n_full: int, *, eps: float = 0.05,
                      min_samples: int = 10, min_cluster: int = 20,
                      prob_thresh: float = 0.0) -> list[dict]:
    """pred (K,) class 0..9; prob (K,) class-prob; observed_idx (K,) full-scan idx;
    xyz (K,3) coords of the observed points; n_full = full laser-scan length.
    prob_thresh: only cluster points with class-prob > thresh -> drops low-confidence
    false-positive points that otherwise inflate instances (low IoU) + spawn FP instances.
    Returns list of dict(mask (n_full,) uint8, cls int, conf float)."""
    instances: list[dict] = []
    for c in range(1, 10):
        sel = np.nonzero((pred == c) & (prob > prob_thresh))[0]   # high-conf points of class c
        if sel.size < min_cluster:
            continue
        labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(xyz[sel])
        for lab in np.unique(labels):
            if lab == -1:                              # DBSCAN noise
                continue
            members = sel[labels == lab]
            if members.size < min_cluster:
                continue
            mask = np.zeros(n_full, dtype=np.uint8)
            mask[observed_idx[members]] = 1            # scatter to full-scan indices
            instances.append({"mask": mask, "cls": int(c),
                              "conf": float(prob[members].mean())})  # cross-scene-comparable
    return instances
