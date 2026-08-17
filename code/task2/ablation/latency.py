#!/usr/bin/env python3
"""Measured single-frame inference latency: our open-vocabulary segmenter versus the
baseline's Molmo-7B + SAM pointing stage.

## Why this exists

The call *counts* in docs/metrics_and_cost.md are exactly countable (1 text-only LLM call
here against 50 VLM calls there), but "how many seconds faster" was an estimate. These two
measurements are what turn a ratio of counts into a ratio of seconds.

## Protocol -- it must match the baseline's real call path or the numbers mean nothing

    Molmo       through the baseline's own `inference_molmo`, bf16, max_new_tokens=200,
                do_sample -- byte for byte the path `run_molmo.py` takes when benchmarking.
    SAM         through `process_sam_prompts`, chained onto Molmo's point prompts, because
                the baseline runs both on every frame.
    Segmenter   through our own `sam3_util.sam3_masks`, with the same parameters the
                candidate-generation stage uses.

## Timing discipline

- Warm up every model (3 iterations by default) before timing. The first call includes CUDA
  context creation and kernel autotuning, and mixing it in inflates the median severalfold.
- `torch.cuda.synchronize()` before and after every timed call. Without it you measure
  kernel launch time, not execution time.
- Report the median primarily, with the mean alongside. Single-frame latency has a heavy
  tail (image size and detection count both matter), so a mean is easily dragged by a few
  slow frames.

  ⚠️ **But the conversion to per-instruction cost must use the mean, not the median.**
  The expected total of 50 calls is `50 x E[one call]`; a median describes a typical single
  call and multiplying it by a count has no statistical meaning. This matters asymmetrically
  -- Molmo's mean runs 46% above its median, so a median-based conversion understates the
  baseline's cost by about a third. The summary printed below uses medians as a
  conservative floor; the published figure uses means. See docs/metrics_and_cost.md.

Timing only; nothing is written under results/ apart from the latency record itself.

    python code/task2/ablation/latency.py --n 20 --device cuda:0
    python code/task2/ablation/latency.py --skip molmo        # segmenter only
"""
import os, sys, json, glob, time, argparse
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import ABLATION, CANDIDATES, FUN3DU, SCENEFUN3D, SEGMENTER_WEIGHTS  # noqa: E402
PERCEPTION = os.path.join(_CODE_ROOT, "task2", "s1_perception")

DUMP = CANDIDATES
DATA = SCENEFUN3D


def pick_frames(n):
    """Take real frames from already-generated questions.

    Synthetic images would understate the cost: neither the resolution nor the content
    matches, and detection count drives a large part of the latency.
    """
    out = []
    for d in sorted(glob.glob(os.path.join(DUMP, "q*_*"))):
        try:
            m = json.load(open(os.path.join(d, "meta.json")))
        except Exception:
            continue
        f = m.get("frame") or {}
        p = os.path.join(DATA, m["visit"], f["video"], "hires_wide",
                         f"{f['video']}_{f['fid']}.jpg")
        if os.path.exists(p):
            out.append((p, m["parse"]["target"]["concept"], m["text"]))
        if len(out) >= n:
            break
    return out


def timeit(fn, frames, warmup, tag):
    import torch
    for p, c, t in frames[:warmup]:
        try:
            fn(p, c, t)
        except Exception as e:
            print(f"  [{tag}] warmup failed: {type(e).__name__}: {e}")
            return None
    ts = []
    for p, c, t in frames:
        torch.cuda.synchronize()
        t0 = time.perf_counter()
        try:
            fn(p, c, t)
        except Exception as e:
            print(f"  [{tag}] call failed: {type(e).__name__}: {e}")
            return None
        torch.cuda.synchronize()
        ts.append(time.perf_counter() - t0)
    a = np.array(ts)
    print(f"  {tag:<32}median {np.median(a)*1000:>8.0f} ms   mean {a.mean()*1000:>8.0f} ms   "
          f"min {a.min()*1000:>7.0f}  max {a.max()*1000:>7.0f}   n={len(a)}")
    return dict(median_ms=float(np.median(a) * 1000), mean_ms=float(a.mean() * 1000),
                min_ms=float(a.min() * 1000), max_ms=float(a.max() * 1000), n=len(a))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--warmup", type=int, default=3)
    ap.add_argument("--device", default="cuda:0",
                    help="index relative to the scheduler's allocation; do NOT touch "
                         "CUDA_VISIBLE_DEVICES -- see code/README.md")
    ap.add_argument("--skip", default="", help="comma separated: sam3,molmo,sam")
    ap.add_argument("--out", default=os.path.join(ABLATION, "latency.json"))
    args = ap.parse_args()
    skip = {x.strip() for x in args.skip.split(",") if x.strip()}

    import torch
    frames = pick_frames(args.n + args.warmup)
    if len(frames) < args.warmup + 5:
        sys.exit(f"too few usable frames ({len(frames)}) -- is {DATA} mounted?")
    print(f"[frames] {len(frames)} real frames; timing {args.n}, warmup {args.warmup}")
    print(f"[gpu] {torch.cuda.device_count()} visible, using {args.device}  "
          f"(CUDA_VISIBLE_DEVICES={os.environ.get('CUDA_VISIBLE_DEVICES', '<unset>')})")
    res = {}

    # ---------------- ours: the open-vocabulary segmenter ----------------
    if "sam3" not in skip:
        sys.path.insert(0, PERCEPTION)
        from sam3_util import init_sam3, sam3_masks
        from PIL import Image
        print("\n=== ours: open-vocab segmenter (detection + segmentation in one) ===")
        pred = init_sam3(SEGMENTER_WEIGHTS, device=args.device)

        def run_sam3(p, c, t):
            rgb = np.asarray(Image.open(p).convert("RGB"), dtype=np.uint8)
            return sam3_masks(pred, rgb, c)

        res["sam3"] = timeit(run_sam3, frames[args.warmup:], args.warmup,
                             "segmenter, one frame one concept")
        del pred
        torch.cuda.empty_cache()

    # ---------------- baseline: Molmo + SAM ----------------
    if "molmo" not in skip or "sam" not in skip:
        cwd = os.getcwd()
        sys.path.insert(0, FUN3DU)
        os.chdir(FUN3DU)                       # its imports resolve relative to cwd
        from utils.hf_models import (init_molmo, inference_molmo, init_sam_model,
                                     process_sam_prompts, extract_points)
        from PIL import Image

        if "molmo" not in skip:
            print("\n=== baseline: Molmo-7B-D pointing (once per frame, 50 frames per question) ===")
            mm, mp = init_molmo()             # device_map='auto', uses the allocated GPU

            def run_molmo(p, c, t):
                img = Image.open(p)
                return inference_molmo(mm, mp, img, f"Point to all the {c}s in order to {t}")

            res["molmo"] = timeit(run_molmo, frames[args.warmup:], args.warmup,
                                  "Molmo-7B pointing, one frame")
            if "sam" not in skip:
                print("\n=== baseline: SAM turning Molmo's points into masks (once per frame) ===")
                sm, sp = init_sam_model(args.device)

                def run_sam(p, c, t):
                    img = Image.open(p)
                    r = inference_molmo(mm, mp, img, f"Point to all the {c}s")
                    pts = extract_points(r, img.size)
                    if pts is None:
                        return None
                    return process_sam_prompts(sm, sp, img, pts, batch=1)

                res["molmo+sam"] = timeit(run_sam, frames[args.warmup:], args.warmup,
                                          "Molmo + SAM in series, one frame")
            del mm, mp
            torch.cuda.empty_cache()
        os.chdir(cwd)

    # The segmenter needs a recent transformers, while Molmo's trust_remote_code module
    # demands tensorflow on recent versions. The two therefore run in separate environments,
    # so this **merges** into any existing record rather than overwriting it.
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    old = {}
    if os.path.exists(args.out):
        try:
            old = json.load(open(args.out))
        except Exception:
            pass
    old.update({k: v for k, v in res.items() if v})
    json.dump(old, open(args.out, "w"), indent=1)
    res = old

    # ---------------- conversion, using the merged record ----------------
    print(f"\n{'='*76}")
    print("Vision-side cost per instruction (medians above x the call counts from the docs)")
    print(f"{'='*76}")
    if res.get("sam3"):
        s = res["sam3"]["median_ms"] / 1000
        print(f"  ours      segmenter x ~44    = {44*s:>7.1f} s"
              f"   (frame scoring 13.7 + candidate detection ~30)")
        print(f"            the ~30 detections are cacheable per (visit, concept)")
    if res.get("molmo+sam"):
        m = res["molmo+sam"]["median_ms"] / 1000
        print(f"  baseline  (Molmo+SAM) x 50   = {50*m:>7.1f} s   <- dominant cost")
    elif res.get("molmo"):
        m = res["molmo"]["median_ms"] / 1000
        print(f"  baseline  Molmo x 50         = {50*m:>7.1f} s   (SAM not included)")
    if res.get("sam3") and (res.get("molmo+sam") or res.get("molmo")):
        a = 44 * res["sam3"]["median_ms"]
        b = 50 * (res.get("molmo+sam") or res["molmo"])["median_ms"]
        print(f"\n  vision-side ratio ~ {b/a:.1f}x   (median-based, a conservative floor)")
        print(f"  ⚠️ vision side only; both pipelines additionally make one text LLM call,")
        print(f"     which is excluded from both sides.")

    print(f"\ndetail -> {args.out}")


if __name__ == "__main__":
    main()
