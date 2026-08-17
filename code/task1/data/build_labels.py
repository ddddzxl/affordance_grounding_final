#!/usr/bin/env python3
"""build_labels.py — functionality-segmentation training labels, aligned 1:1 with the
DINOv2 feature cache (cache/features_3d/dinov2/<visit>.npz).

For each scene it reads only the small <visit>_annotations.json + the feature cache's
`observed_idx`, and produces a per-OBSERVED-point label. Mirrors the eval GT builder
(eval/functionality_segmentation/prepare_gt_val_data.py):
  - each functional-element annotation -> its points get that affordance class (1..9)
  - an "exclude" annotation -> those points get 255 (ignored in loss / dropped by eval)
  - everything else -> 0 (background / no affordance)
Overlapping annotations: last-one-wins; exclude is applied last (same as prepare_gt).

Light I/O (json + the index array only; NOT feat / NOT the laser scan). Plain json+numpy,
no cv2. RUN ON A COMPUTE NODE.

Output per scene: <out_dir>/<visit>.npz, aligned to the feature cache's observed_idx order:
  cls  : (K,) uint8   0=background, 1..9=affordance, 255=exclude
  inst : (K,) uint16  0=background/exclude, else 1-based per-scene instance id
Also prints an affordance-label-coverage stat: of all annotated (functional) points,
how many are actually observed (have a feature) -- unobserved ones are unlabelable.
"""
import argparse
import json
import os
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import FEATURE_CACHE, LABEL_CACHE, SCENEFUN3D  # noqa: E402

# fixed by the benchmark -- eval/functionality_segmentation/eval_utils/benchmark_labels.py
CLASS_LABELS = ["rotate", "key_press", "tip_push", "hook_pull", "pinch_pull",
                "hook_turn", "foot_push", "plug_in", "unplug"]
CLS_ID = {name: i + 1 for i, name in enumerate(CLASS_LABELS)}   # 1..9
EXCLUDE = 255


def read_visits(bfl, csv):
    with open(os.path.join(bfl, csv)) as f:
        next(f)  # header visit_id,video_id
        return sorted({ln.split(",")[0] for ln in f if ln.strip()})


def build_one(visit_id, data_root, feat_dir, out_dir):
    obs = np.load(os.path.join(feat_dir, f"{visit_id}.npz"))["observed_idx"]  # (K,) full-scan idx
    K = obs.shape[0]
    cls = np.zeros(K, dtype=np.uint8)
    inst = np.zeros(K, dtype=np.uint16)
    ann = json.load(open(os.path.join(data_root, visit_id,
                                      f"{visit_id}_annotations.json")))["annotations"]
    n_inst, excl = 0, []
    ann_pts = []                                  # union of functional (non-exclude) points
    for a in ann:
        if a["label"] == "exclude":
            excl.append(np.asarray(a["indices"], dtype=np.int64))  # collect ALL exclude annotations
            continue
        idx = np.asarray(a["indices"], dtype=np.int64)
        ann_pts.append(idx)
        n_inst += 1
        m = np.isin(obs, idx)                     # observed points belonging to this annotation
        cls[m] = CLS_ID[a["label"]]
        inst[m] = n_inst
    if excl:                                      # union ALL exclude annotations, applied last --
        excl = np.unique(np.concatenate(excl))    # matches get_annotations(group_excluded_points=True)
        m = np.isin(obs, excl)
        cls[m] = EXCLUDE
        inst[m] = 0

    os.makedirs(out_dir, exist_ok=True)
    np.savez(os.path.join(out_dir, f"{visit_id}.npz"), cls=cls, inst=inst)

    aff = int(((cls >= 1) & (cls <= 9)).sum())
    ann_all = np.unique(np.concatenate(ann_pts)) if ann_pts else np.zeros(0, np.int64)
    n_ann = ann_all.size
    n_ann_obs = int(np.isin(ann_all, obs).sum())  # annotated points that are observed (labelable)
    return dict(K=K, n_inst=n_inst, aff=aff, n_ann=n_ann, n_ann_obs=n_ann_obs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["val", "train", "all"], default="all")
    ap.add_argument("--data_root", default=SCENEFUN3D)
    ap.add_argument("--feat_dir", default=FEATURE_CACHE)
    ap.add_argument("--out_dir", default=LABEL_CACHE)
    args = ap.parse_args()

    bfl = os.path.join(args.data_root, "benchmark_file_lists")
    val, train = read_visits(bfl, "val_set.csv"), read_visits(bfl, "train_set.csv")
    visits = {"val": val, "train": train, "all": sorted(set(val + train))}[args.split]

    tot = dict(K=0, aff=0, n_inst=0, n_ann=0, n_ann_obs=0)
    low = []
    for i, v in enumerate(visits):
        if not os.path.exists(os.path.join(args.feat_dir, f"{v}.npz")):
            print(f"[skip {v}] no feature cache"); continue
        r = build_one(v, args.data_root, args.feat_dir, args.out_dir)
        for k in tot:
            tot[k] += r[k]
        cov = 100.0 * r["n_ann_obs"] / max(r["n_ann"], 1)
        if cov < 80:
            low.append((v, round(cov, 1)))
        if (i + 1) % 25 == 0 or i + 1 == len(visits):
            print(f"[{i+1}/{len(visits)}] {v}: K={r['K']:,} inst={r['n_inst']} "
                  f"aff_pts={r['aff']:,} ann_obs_cov={cov:.1f}%", flush=True)

    aff_frac = 100.0 * tot["aff"] / max(tot["K"], 1)
    ann_cov = 100.0 * tot["n_ann_obs"] / max(tot["n_ann"], 1)
    print(f"\n=== {args.split}: {len(visits)} scenes ===")
    print(f"affordance points: {tot['aff']:,} / {tot['K']:,} observed ({aff_frac:.3f}% -- tiny, as expected)")
    print(f"instances total: {tot['n_inst']}")
    print(f"affordance-label coverage (annotated pts that are OBSERVED): {ann_cov:.1f}%")
    if low:
        print(f"scenes with <80% label coverage ({len(low)}): {low[:12]}")
    print(f"labels -> {args.out_dir}")


if __name__ == "__main__":
    main()
