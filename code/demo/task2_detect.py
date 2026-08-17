#!/usr/bin/env python3
"""The demo's **vision side**: run the segmenter once per (scan, concept, frame) and cache it.

## Why the cache is keyed by concept rather than by instruction

Instructions in one scene share almost all of the visual work. The four Drawer_Cups
instructions ("top / 2nd / 3rd / bottom drawer of the cabinet with cups on top") use
**exactly the same** four concept detections and differ only in the parsed ordering
constraint and the reasoning that follows. Running per `(scan, concept)` therefore means
adding instructions **adds no segmenter calls at all**.

This is the structural difference from the baseline (50 VLM image reads per instruction), and
the demo exists in part to make it visible.

## Output format

  `<out>/<scan>/cache/det_f####.npz`   key "<concept>|<i>" -> flat mask indices (int32)
  `<out>/<scan>/cache/det.json`        per detection: bbox / score / area, for frame
                                       selection and candidate generation

With --resume, frames already present are skipped, so an interrupted run can continue.

  python src/demo/task2_detect.py --scan Drawer_Cups --device cuda:0
"""
import os, sys, json, glob, argparse
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _CODE_ROOT)
from paths import PROJECT_ROOT  # noqa: E402
ROOT = PROJECT_ROOT
sys.path.insert(0, os.path.join(ROOT, "src/demo"))
sys.path.insert(0, os.path.join(ROOT, "scripts/checks"))
from iphone_io import read_frames, read_rgb                    # noqa: E402
from sam3_util import init_sam3, sam3_masks                    # noqa: E402

DATA = os.path.join(ROOT, "data/iphone_3dscanner")
OUT = os.path.join(ROOT, "viz/func_seg/demo_task2")


def concepts_of(tasks, scan):
    """Every concept used by this scene's instructions, deduplicated, in stable order."""
    seen = []
    for t in tasks.get(scan, []):
        p = t["parse"]
        for e in p["entities"]:
            n = e["name"]
            if e.get("instanceable", True) and n not in seen:
                seen.append(n)
    return seen


def nms(dets, iou_th):
    """Greedy NMS in descending score order.

    ⚠️ Sorting must be by **score**, not area. Sorting by area keeps a box covering the whole
       cabinet and suppresses the small handle that was actually wanted.
    """
    keep = []
    for d in sorted(dets, key=lambda x: -x["score"]):
        ok = True
        for k in keep:
            inter = len(np.intersect1d(d["flat"], k["flat"], assume_unique=True))
            if inter == 0:
                continue
            if inter / min(len(d["flat"]), len(k["flat"])) > iou_th:
                ok = False; break
        if ok:
            keep.append(d)
    return keep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", default="all")
    ap.add_argument("--device", default="cuda:0",
                    help="index relative to the scheduler's allocation; do NOT touch "
                         "CUDA_VISIBLE_DEVICES")
    ap.add_argument("--det_th", type=float, default=0.15)
    ap.add_argument("--nms", type=float, default=0.75,
                    help="overlap suppression threshold within one concept")
    ap.add_argument("--resume", type=int, default=1)
    ap.add_argument("--scan", default="all")
    ap.add_argument("--concepts", default="",
                    help="comma separated; if given, detect **only** these concepts and "
                         "**merge** them into the existing cache -- used when swapping a "
                         "retrieval term (trying a synonym for something undetectable) "
                         "without re-running every concept")
    ap.add_argument("--frames", default="", help="comma-separated frame ids; empty = all")
    args = ap.parse_args()

    tasks = json.load(open(os.path.join(OUT, "tasks.json")))
    scans = [s for s in tasks if not s.startswith("_")] if args.scan == "all" else [args.scan]

    predictor = init_sam3(os.path.join(ROOT, "third_party/sam3_weights"), device=args.device)
    for scan in scans:
        cons = ([c.strip() for c in args.concepts.split(",") if c.strip()]
                if args.concepts else concepts_of(tasks, scan))
        sd = os.path.join(DATA, scan)
        cd = os.path.join(OUT, scan, "cache")
        os.makedirs(cd, exist_ok=True)
        frames = read_frames(sd, upright=True)
        print(f"\n=== {scan} ===  {len(frames)} frames x {len(cons)} concepts "
              f"= {len(frames)*len(cons)} segmenter calls", flush=True)
        print(f"  concepts: {cons}", flush=True)
        meta_path = os.path.join(cd, "det.json")
        meta = json.load(open(meta_path)) if (args.resume and os.path.exists(meta_path)) else {}

        only = {int(x) for x in args.frames.split(",") if x.strip()} if args.frames else None
        for fi, fr in enumerate(frames):
            if only is not None and fi not in only:
                continue
            key = f"{fi:04d}"
            npz = os.path.join(cd, f"det_f{key}.npz")
            # With --concepts this is a top-up for new terms, so an existing frame must be
            # **merged into** rather than skipped
            if args.resume and not args.concepts and key in meta and os.path.exists(npz):
                continue
            rgb = read_rgb(fr["rgb"], upright=True)
            H, W = rgb.shape[:2]
            store, info = {}, {}
            if args.concepts and os.path.exists(npz):   # keep existing concepts, add new ones
                old = np.load(npz)
                store = {k: old[k] for k in old.files}
                info = dict(meta.get(key, {}).get("det", {}))
            for c in cons:
                dets = []
                for m, s in sam3_masks(predictor, rgb, c, det_th=args.det_th, with_scores=True):
                    if not m.any():
                        continue
                    dets.append(dict(flat=np.nonzero(m.reshape(-1))[0].astype(np.int32), score=float(s)))
                dets = nms(dets, args.nms)[:args.max_per_concept]
                info[c] = []
                for i, d in enumerate(dets):
                    yy, xx = np.divmod(d["flat"].astype(np.int64), W)
                    store[f"{c}|{i}"] = d["flat"]
                    info[c].append(dict(i=i, score=round(d["score"], 4), n=int(len(d["flat"])),
                                        x0=int(xx.min()), x1=int(xx.max()),
                                        y0=int(yy.min()), y1=int(yy.max()),
                                        cx=float(xx.mean()), cy=float(yy.mean())))
            np.savez_compressed(npz, **store)
            meta[key] = dict(W=int(W), H=int(H), rgb=os.path.basename(fr["rgb"]), det=info)
            json.dump(meta, open(meta_path, "w"))
            tot = sum(len(v) for v in info.values())
            print(f"  [{fi+1}/{len(frames)}] f{key}  detections {tot}  "
                  f"({', '.join(f'{c}:{len(info[c])}' for c in cons)})", flush=True)
        print(f"  -> {cd}", flush=True)


if __name__ == "__main__":
    main()
