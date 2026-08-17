#!/usr/bin/env python3
"""train_ap.py — diagnostic: instance AP on a SAMPLE of TRAIN scenes.

Purpose: decide whether the closed-set line's val 18.25 is "the method cannot learn this"
(an instance-segmentation bottleneck) or "it does not generalise" (too little data). That
determines whether the next step is a new backend or something else entirely:

    train AP ~= 18            -> even train cannot be scored highly -> the instance method
                                 itself is the bottleneck -> a new backend is justified
    train AP >> val (35-45+)  -> train learns fine and val falls away -> a generalisation gap
                                 (200 scenes is few) -> a new backend will not help; the
                                 problem is data

This reuses predict_v1's forward_scene / cluster / eval_safe / softmax_max verbatim (same
grid, same calibration protocol, so it is strictly comparable with val 18.25) and changes
**only the ground-truth scenes** -- from val to freshly built official full-scan GT for
sampled train scenes (cls*1000+inst, the same format as gt_val) -- before calling the
official evaluation. Read-only apart from diagnostic outputs; it does not touch training,
caches, val, or any existing result.

  # 1. verify the construction first (rebuild one val scene's GT and compare against the
  #    shipped gt_val point by point; this must pass before anything else)
  python code/task1/eval/train_ap.py --run <run> --self_check
  # 2. the diagnosis (30 train scenes, calibrated -- the same conditions as val 18.25)
  python code/task1/eval/train_ap.py --run <run> --device cuda:0 --n_scenes 30
"""
from __future__ import annotations
import os, sys, json, argparse, subprocess, random
import numpy as np
import torch

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import CODE, TOOLKIT  # noqa: E402
sys.path.insert(0, os.path.join(CODE, "task1"))
sys.path.insert(0, os.path.join(CODE, "task1", "features"))
sys.path.insert(0, TOOLKIT)

# Reuse the EXACT v1 inference path (forward / cluster / eval-safe / cal) so that train and
# val remain comparable. Sibling modules are imported directly rather than as `eval.predict_v1`
# -- that `eval` would collide with the toolkit's namespace package of the same name.
from predict_v1 import (forward_scene, cluster, softmax_max, eval_safe,
                        FEAT_DIR, DATA_ROOT, RUNS, RESULTS, GT_VAL)
from eval.functionality_segmentation.eval_utils.rle import rle_encode
from data_io import load_pointcloud
from models import build_model

# fixed by the benchmark (same as build_labels.py); gt_val value = CLS_ID*1000 + inst, exclude=255
CLASS_LABELS = ["rotate", "key_press", "tip_push", "hook_pull", "pinch_pull",
                "hook_turn", "foot_push", "plug_in", "unplug"]
CLS_ID = {n: i + 1 for i, n in enumerate(CLASS_LABELS)}
EXCLUDE = 255


def read_train_visits():
    bfl = os.path.join(DATA_ROOT, "benchmark_file_lists", "train_set.csv")
    with open(bfl) as f:
        next(f)  # header
        return sorted({ln.split(",")[0] for ln in f if ln.strip()})


def build_gt_array(visit, n_full):
    """full-scan cls*1000+inst, reproducing how gt_val itself is built:

    - non-exclude annotations take a global 1-based instance number in json order (skipping
      excludes), and their points become CLS*1000+inst
    - overlaps resolve last-one-wins (sequential overwrite); excludes are set to 255 at the end

    The class and instance assignment matches build_labels exactly; the only difference is
    that the output is full-scan (including unobserved points), as gt_val is.
    """
    ann = json.load(open(os.path.join(DATA_ROOT, visit,
                                      f"{visit}_annotations.json")))["annotations"]
    g = np.zeros(n_full, np.int64)
    n_inst, excl = 0, []
    for a in ann:
        if a["label"] == "exclude":
            excl.append(np.asarray(a["indices"], np.int64))
            continue
        n_inst += 1
        g[np.asarray(a["indices"], np.int64)] = CLS_ID[a["label"]] * 1000 + n_inst
    if excl:
        g[np.unique(np.concatenate(excl))] = EXCLUDE
    return g, n_inst


def run_eval(sub_dir, gt_dir):
    """The official evaluation with a parameterised gt_dir (predict_v1.run_eval hard-codes
    the val GT; here it is swapped for the train GT)."""
    res = subprocess.run([sys.executable, "-m", "eval.functionality_segmentation.evaluate",
                          "--pred_dir", sub_dir, "--gt_dir", gt_dir],
                         cwd=TOOLKIT, capture_output=True, text=True)
    return res.stdout + ("\n=== stderr ===\n" + res.stderr if res.stderr.strip() else "")


def self_check():
    """Rebuild one val scene's GT and verify it is evaluate-equivalent to the shipped gt_val.

    Equivalence is necessary and sufficient on four counts (the official evaluation looks only
    at class, instance partition and exclusions, never at the instance numbers themselves):
    (1) identical foreground point set, (2) identical per-point class, (3) identical instance
    partition, (4) identical exclusion set.

    Also checks that load_pointcloud's n_full matches the gt_val row count, which is what
    guarantees the train GT lines up with the prediction.
    """
    v = sorted(f[:-4] for f in os.listdir(GT_VAL) if f.endswith(".txt"))[0]
    ref = np.loadtxt(os.path.join(GT_VAL, f"{v}.txt")).astype(np.int64)
    n_lp = load_pointcloud(DATA_ROOT, v)["P_full"].shape[0]
    mine, n_inst = build_gt_array(v, ref.shape[0])
    print(f"[self_check] scene {v}: gt_val {ref.shape[0]:,} pts | load_pointcloud n_full {n_lp:,} "
          f"| {n_inst} inst")
    assert n_lp == ref.shape[0], ("load_pointcloud n_full != gt_val row count -> "
                                  "train GT would be misaligned with the prediction")

    exact = bool(np.array_equal(ref, mine))
    ref_fg = (ref > 0) & (ref != EXCLUDE)
    mine_fg = (mine > 0) & (mine != EXCLUDE)
    fg_ok = bool(np.array_equal(ref_fg, mine_fg))
    cls_ok = bool(np.array_equal(ref[ref_fg] // 1000, mine[mine_fg] // 1000)) if fg_ok else False
    excl_ok = bool(np.array_equal(ref == EXCLUDE, mine == EXCLUDE))
    # instance partition: relabel both foreground value sets to 0..n-1 and compare the
    # partitions, allowing the instance numbers themselves to differ
    part_ok = False
    if fg_ok and int(ref_fg.sum()) > 0:
        _, ri = np.unique(ref[ref_fg], return_inverse=True)
        _, mi = np.unique(mine[mine_fg], return_inverse=True)
        part_ok = bool(np.array_equal(ri, mi))
    print(f"[self_check] exact-equal={exact} | fg-set={fg_ok} | cls={cls_ok} | "
          f"instance-partition={part_ok} | exclude={excl_ok}")
    ok = fg_ok and cls_ok and part_ok and excl_ok
    print("[self_check] " + ("PASS: construction is evaluate-equivalent, train diagnosis can run"
                             if ok else
                             "FAIL: not equivalent -- fix build_gt_array before running"))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--ckpt", default="best.pt")
    ap.add_argument("--n_scenes", type=int, default=30,
                    help="number of train scenes to sample (0 = all)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--cals", default="cal",
                    help="comma separated: cal (z+log prior, the same protocol as val 18.25) / raw")
    ap.add_argument("--eps", type=float, default=0.05)
    ap.add_argument("--min_samples", type=int, default=10)
    ap.add_argument("--min_cluster", type=int, default=20)
    ap.add_argument("--prob_thresh", type=float, default=0.0)
    ap.add_argument("--tag", default="",
                    help="output subdirectory suffix, to isolate parallel jobs: "
                         "train_diag[_<tag>]")
    ap.add_argument("--gt_dir", default="",
                    help="train GT directory (default <out_root>/gt_train; point it at fast "
                         "local storage to keep the full-scan GT off a network filesystem)")
    ap.add_argument("--self_check", action="store_true",
                    help="verify the GT construction only; do not run the model")
    args = ap.parse_args()

    if args.self_check:
        sys.exit(0 if self_check() else 1)

    dev = torch.device(args.device)
    ck = torch.load(os.path.join(RUNS, args.run, args.ckpt), map_location=dev, weights_only=False)
    a = ck["args"]; grid_size = a["grid_size"]
    log_prior = np.array(ck["log_prior"], np.float32)
    model = build_model("v1_ptv3", grid_size=grid_size, proj_dim=a.get("proj_dim", 64),
                        enable_flash=a.get("enable_flash", True)).to(dev)
    model.load_state_dict(ck["model"]); eval_safe(model)

    # sample TRAIN scenes that have a feature cache (annotations always exist)
    cand = [v for v in read_train_visits()
            if os.path.exists(os.path.join(FEAT_DIR, f"{v}.npz"))]
    random.seed(args.seed)
    visits = sorted(random.sample(cand, args.n_scenes)) if 0 < args.n_scenes < len(cand) else cand
    print(f"[train_ap] {args.run} ep{ck['epoch']} grid {grid_size} proj {a.get('proj_dim',64)} "
          f"| {len(visits)}/{len(cand)} train scenes | seed {args.seed}", flush=True)

    cals = [c.strip() for c in args.cals.split(",")]
    multi = len(cals) > 1                                  # several protocols -> one output dir
                                                           # each; still a single forward pass
    run_dir = os.path.join(RESULTS, args.run)
    base = "train_diag" + (f"_{args.tag}" if args.tag else "")
    gt_dir = args.gt_dir or os.path.join(run_dir, base + "_gt")   # GT is protocol independent,
                                                                  # so cal and raw share one copy
    os.makedirs(gt_dir, exist_ok=True)

    # forward ONCE per scene (expensive), building that scene's train GT on the fly
    scene_cache = {}
    for vi, v in enumerate(visits):
        try:
            out = forward_scene(model, v, dev, grid_size)
        except RuntimeError as e:                          # OOM and friends -> skip rather than
                                                           # contaminate the mean
            print(f"  [{vi+1}/{len(visits)}] {v}  SKIP ({type(e).__name__}: {str(e)[:60]})", flush=True)
            continue
        n_full = out[5]
        g, n_inst = build_gt_array(v, n_full)
        np.savetxt(os.path.join(gt_dir, f"{v}.txt"), g, fmt="%i")
        scene_cache[v] = out
        print(f"  [{vi+1}/{len(visits)}] {v}  {out[0].shape[0]:,} vox | {n_inst} gt inst", flush=True)
    done = list(scene_cache)
    if not done:
        print("[train_ap] no usable scenes"); sys.exit(1)

    for cal in cals:
        # one protocol: train_diag_<tag>;  several: train_diag_<tag>_<cal>
        out_root = os.path.join(run_dir, base + (f"_{cal}" if multi else ""))
        sub_dir = os.path.join(out_root, "submission")
        mask_dir = os.path.join(sub_dir, "predicted_masks"); os.makedirs(mask_dir, exist_ok=True)
        n_inst = 0
        for v in done:
            sem, off, xyz_vox, inv, obs, n_full = scene_cache[v]
            logits = sem + log_prior if cal == "cal" else sem
            prob, pred = softmax_max(logits)
            inst = cluster(pred, prob, xyz_vox, inv, obs, n_full,
                           args.eps, args.min_samples, args.min_cluster, args.prob_thresh)
            lines = []
            for k, ins in enumerate(inst):
                mf = f"{v}_{k:03d}.txt"
                with open(os.path.join(mask_dir, mf), "w") as fh:
                    fh.write(rle_encode(ins["mask"]))
                lines.append(f"predicted_masks/{mf} {ins['cls']} {ins['conf']:.4f}")
            if not lines:                                  # zero-instance scene -> dummy, as in predict_v1
                mf = f"{v}_000.txt"
                with open(os.path.join(mask_dir, mf), "w") as fh:
                    fh.write("")
                lines.append(f"predicted_masks/{mf} 1 0.0")
            with open(os.path.join(sub_dir, f"{v}.txt"), "w") as fh:
                fh.write("\n".join(lines))
            n_inst += len(inst)
        report = run_eval(sub_dir, gt_dir)
        with open(os.path.join(out_root, f"eval_train_{cal}.txt"), "w") as fh:
            fh.write(report)
        avg = [l for l in report.splitlines() if l.strip().startswith("average")]
        print(f"[{cal}] {len(done)} scenes | {n_inst} pred inst -> {os.path.basename(out_root)} | "
              f"{avg[0].strip() if avg else '(no average line)'}", flush=True)
    print(f"[train_ap] gt -> {gt_dir}  (diagnostic intermediate, safe to delete) | "
          f"compare against val C_v2 cal = 18.25 / 32.2 / 44.5")


if __name__ == "__main__":
    main()
