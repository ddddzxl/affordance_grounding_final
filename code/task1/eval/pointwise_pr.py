#!/usr/bin/env python3
"""pointwise_pr.py — natural-distribution point-level P/R of model preds (eval diagnostic).

Reads cached per-point preds (predict.py --save_pred) + gt_val, on the OBSERVED points
(natural ~1300:1 bg:fg — NOT the balanced pool). This is the prior-shift diagnostic: a model
trained on a 30:1 prior has its precision crater here vs the balanced-pool ~0.87. Numbers only;
viz lives in src/viz/viz_scene.py.

  python src/eval/pointwise_pr.py --run v0mlp_none             # P/R over all val (the money number)
  python src/eval/pointwise_pr.py --run v0mlp_none --visit 421254
"""
import os, argparse
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import GT_VAL, TASK1  # noqa: E402
RESULTS = TASK1
CLASS_NAMES = {1: "rotate", 2: "key_press", 3: "tip_push", 4: "hook_pull", 5: "pinch_pull",
               6: "hook_turn", 7: "foot_push", 8: "plug_in", 9: "unplug"}


def load_scene(run: str, visit: str):
    d = np.load(os.path.join(RESULTS, run, "preds", f"{visit}.npz"))
    g = np.loadtxt(os.path.join(GT_VAL, f"{visit}.txt"), dtype=np.uint32)
    gobs = g[d["obs"]]
    gt = np.where(gobs >= 1000, gobs // 1000, np.where(gobs == 255, 255, 0)).astype(np.int64)
    return d["pred"], gt


def pr_natural(pred: np.ndarray, gt: np.ndarray):
    """Per-class + affordance-vs-bg P/R on the NATURAL distribution (drop gt==255 exclude)."""
    keep = gt != 255
    pred, gt = pred[keep], gt[keep]
    rows = {}
    for c in range(1, 10):
        gtc, pp = gt == c, pred == c
        tp = int((gtc & pp).sum()); fp = int((~gtc & pp).sum()); fn = int((gtc & ~pp).sum())
        rows[CLASS_NAMES[c]] = {"prec": tp / (tp + fp) if tp + fp else 0.0,
                                "rec": tp / (tp + fn) if tp + fn else 0.0, "n_gt": int(gtc.sum())}
    fg_gt, fg_pp = gt > 0, pred > 0
    tp = int((fg_gt & fg_pp).sum()); fp = int((~fg_gt & fg_pp).sum()); fn = int((fg_gt & ~fg_pp).sum())
    aff = {"prec": tp / (tp + fp) if tp + fp else 0.0, "rec": tp / (tp + fn) if tp + fn else 0.0,
           "n_pred_fg": int(fg_pp.sum()), "n_gt_fg": int(fg_gt.sum())}
    return rows, aff


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--visit", default=None, help="one visit; omit -> all val")
    args = ap.parse_args()
    visits = ([args.visit] if args.visit
              else sorted(f[:-4] for f in os.listdir(GT_VAL) if f.endswith(".txt")))
    all_pred, all_gt = [], []
    for v in visits:
        pred, gt = load_scene(args.run, v)
        all_pred.append(pred); all_gt.append(gt)
        _, aff = pr_natural(pred, gt)
        ratio = aff["n_pred_fg"] / max(aff["n_gt_fg"], 1)
        print(f"[{v}] aff prec {aff['prec']:.3f} rec {aff['rec']:.3f} | "
              f"pred_fg {aff['n_pred_fg']:,} vs gt_fg {aff['n_gt_fg']:,} ({ratio:.1f}x)")
    P, G = np.concatenate(all_pred), np.concatenate(all_gt)
    rows, aff = pr_natural(P, G)
    print(f"\n=== ALL {len(visits)} val scenes (NATURAL ~1300:1) ===")
    print(f"  affordance-vs-bg: prec {aff['prec']:.4f}  rec {aff['rec']:.4f}  "
          f"(pred_fg {aff['n_pred_fg']:,} vs gt_fg {aff['n_gt_fg']:,})")
    for c in range(1, 10):
        r = rows[CLASS_NAMES[c]]
        print(f"    {CLASS_NAMES[c]:<12} P{r['prec']:.4f} R{r['rec']:.4f} n_gt{r['n_gt']:,}")


if __name__ == "__main__":
    main()
