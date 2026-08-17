#!/usr/bin/env python3
"""Aggregate the multi-frame voting results into official AP50 / AR50 / AP25.

**This is the one script that runs with no dataset and no weights.** It reads the shipped
per-question jsonl files and reproduces the main results table.

## The official protocol (SceneFun3D)

    precision = |GT & pred| / |pred|      recall = |GT & pred| / |GT|
    AP50 = fraction(precision >= 0.5)     AR50 = fraction(recall >= 0.5)

Only AP25 / AP50 are officially reported -- there is **no** AP75 and no mAP@0.5:0.95.

## Why every threshold tier is printed with its recall

Raising the voting threshold always improves precision and always removes points. At
th=0.9 the prediction is frequently down to single-digit point counts: AP50 goes up, but
that mask is no longer usable for anything. Choosing an operating point requires reading
both columns, so picking the tier with the highest AP50 alone is not a valid selection
procedure.

## The `--frames K` stratification

The multi-frame gain depends entirely on **how many frames actually cast a vote**. For a
question where only one frame voted, multi-frame is identical to single-frame by
construction; mixing those into the total dilutes the measured gain. Stratifying makes it
visible whether the mechanism engaged at all.

⚠️ Stratified subsets are diagnostics. They must never be placed alongside published
numbers, which use the full 442 instructions.

    python code/task2/eval/mf_agg.py
    python code/task2/eval/mf_agg.py --frames 3,5,8      # only questions with enough frames
"""
import os, sys, json, glob, argparse
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from paths import LIFT                                             # noqa: E402


def load():
    R, seen = [], set()
    for f in sorted(glob.glob(os.path.join(LIFT, "mf_s*.jsonl"))):
        for line in open(f):
            try:
                r = json.loads(line)
            except Exception:
                continue
            if "single" not in r or r["q"] in seen:
                continue
            seen.add(r["q"]); R.append(r)
    return R


def arms(R):
    """Return [(display name, key)] -- single frame first, thresholds in numeric order."""
    ths = sorted({k for r in R for k in r if k.startswith("th")},
                 key=lambda x: float(x[2:]))
    return [("single (erode5+C2)", "single")] + [(f"multi {k}", k) for k in ths]


def stat(R, key):
    p = np.array([r[key]["prec"] for r in R])
    rc = np.array([r[key]["rec"] for r in R])
    n = np.array([r[key]["n"] for r in R], float)
    return dict(ap50=100 * (p >= .5).mean(), ap25=100 * (p >= .25).mean(),
                ar50=100 * (rc >= .5).mean(), mprec=100 * p.mean(),
                mrec=100 * rc.mean(), npts=np.median(n),
                empty=100 * (n == 0).mean())


def table(R, title):
    print(f"\n{title}   n={len(R)}")
    print(f"  {'':<20}{'AP50':>7}{'AP25':>7}{'AR50':>7}{'meanP':>8}{'meanR':>8}"
          f"{'medPts':>9}{'empty':>8}")
    for name, k in arms(R):
        if not all(k in r for r in R):
            continue
        s = stat(R, k)
        print(f"  {name:<20}{s['ap50']:>7.1f}{s['ap25']:>7.1f}{s['ar50']:>7.1f}"
              f"{s['mprec']:>8.1f}{s['mrec']:>8.1f}{s['npts']:>9.0f}{s['empty']:>7.1f}%")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", default="2,3,5,8", help="stratification thresholds, comma separated")
    ap.add_argument("--by_conf", type=int, default=1)
    args = ap.parse_args()

    R = load()
    if not R:
        sys.exit(f"no mf_s*.jsonl found under: {LIFT}")

    nf = np.array([r["n_frames"] for r in R])
    print(f"\n{'='*78}")
    print(f"Multi-frame parallax voting - full val, {len(R)} instructions")
    print(f"{'='*78}")
    print(f"  voting frames: median {np.median(nf):.0f}  mean {nf.mean():.1f}  "
          f"max {nf.max()}   single-frame-only questions {100*(nf==1).mean():.1f}%")

    table(R, "=== full val (comparable with published numbers) ===")

    for k in [int(x) for x in args.frames.split(",") if x.strip()]:
        sub = [r for r in R if r["n_frames"] >= k]
        if len(sub) < 20 or len(sub) == len(R):
            continue
        table(sub, f"=== subset: >={k} voting frames (NOT comparable with published numbers) ===")

    if args.by_conf:
        print(f"\n=== by reasoning confidence (single -> multi th0.9, AP50) ===")
        for c in ["high", "medium", "low", "forced"]:
            sub = [r for r in R if r.get("conf") == c]
            if len(sub) < 10:
                continue
            a, b = stat(sub, "single")["ap50"], stat(sub, "th0.9")["ap50"]
            print(f"  {c:<10}n={len(sub):<4}{a:>6.1f} -> {b:>6.1f}  ({b-a:+.1f})")

    print(f"\n--- published comparisons (official val) ---")
    print(f"  UniFunc3D-30B  AP50 31.24   AP25 51.01")
    print(f"  UniFunc3D-8B   AP50 23.82   AP25 44.04")
    print(f"  AffordMEM      AP50 20.13   AP25 41.66")
    print(f"  Fun3DU         AP50 16.90   AP25 33.30")


if __name__ == "__main__":
    main()
