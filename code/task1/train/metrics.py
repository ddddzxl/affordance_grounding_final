"""metrics.py — point-level metrics + v0 go/no-go gate (baseline.md §6).

v0 is judged at the POINT level (per-class P/R, fg mIoU, affordance-vs-bg recall), NOT
instance AP: a point-independent head + DBSCAN fragments instances and would tank AP even
with perfect points. Instance AP is predict.py's job (v1 onward).
"""
from __future__ import annotations
import numpy as np

CLASS_NAMES = {1: "rotate", 2: "key_press", 3: "tip_push", 4: "hook_pull", 5: "pinch_pull",
               6: "hook_turn", 7: "foot_push", 8: "plug_in", 9: "unplug"}
# go gate keys on point-rich AND cross-site-stable classes (low rec there => features bad).
# EXCLUDE key_press(2)/unplug(9): point-rich-ish but instance-poor + cross-site hard (probe
# holdout recall ~0) -> low rec means "hard to generalize", NOT "features unseparable".
MAIN_CLASSES = (1, 4, 5, 6)  # rotate, hook_pull, pinch_pull, hook_turn


def point_metrics(pred: np.ndarray, y: np.ndarray, n_cls: int = 10) -> dict:
    per_class, ious = {}, []
    for c in range(1, n_cls):
        gt, pp = y == c, pred == c
        n_gt = int(gt.sum())
        tp = int((gt & pp).sum()); fp = int((~gt & pp).sum()); fn = int((gt & ~pp).sum())
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        iou = tp / (tp + fp + fn) if tp + fp + fn else 0.0
        per_class[CLASS_NAMES[c]] = {"prec": round(prec, 4), "rec": round(rec, 4),
                                     "iou": round(iou, 4), "n_gt": n_gt}
        if n_gt > 0:                                   # present-class mIoU: classes absent from
            ious.append(iou)                           # this val set don't count as IoU=0
    fg_gt, fg_pred = y > 0, pred > 0
    tp = int((fg_gt & fg_pred).sum()); fp = int((~fg_gt & fg_pred).sum()); fn = int((fg_gt & ~fg_pred).sum())
    aff = {"recall": round(tp / (tp + fn), 4) if tp + fn else 0.0,
           "precision": round(tp / (tp + fp), 4) if tp + fp else 0.0}
    miou = float(np.mean(ious)) if ious else 0.0
    return {"per_class": per_class, "miou_fg": round(miou, 4), "affordance": aff}


def go_no_go(m: dict, recall_go: float = 0.40) -> dict:
    """v0 gate: affordance-overall recall >= recall_go AND main classes clearly above random."""
    aff_rec = m["affordance"]["recall"]
    main_ok = all(m["per_class"][CLASS_NAMES[c]]["rec"] > 0.1 for c in MAIN_CLASSES)
    if aff_rec >= recall_go and main_ok:
        verdict = "go"
    elif aff_rec < 0.1:
        verdict = "no-go? (features not separable -> check lift §6(a)/(d))"
    else:
        verdict = "gray (diagnose: head capacity / imbalance / sampling)"
    return {"verdict": verdict, "affordance_recall": aff_rec,
            "main_class_rec": {CLASS_NAMES[c]: m["per_class"][CLASS_NAMES[c]]["rec"] for c in MAIN_CLASSES}}
