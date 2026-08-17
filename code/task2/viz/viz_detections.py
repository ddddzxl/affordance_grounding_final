#!/usr/bin/env python3
"""2D-RGB diagnostic: overlay the segmenter's instance masks and the ground truth on the
original frame, and judge by eye whether the detection is usable.

## The question it answers

An automated sweep reported a large class of failures of the form "no hit, yet the frame is
full of handles". Two very different causes produce that:

  (a) the segmenter never segmented that particular ground-truth handle
      -- the red GT region has no coloured contour anywhere near it
  (b) the mask exists but is smeared or offset, covering less than 50%
      -- there is a contour, but it is not highlighted or is visibly displaced

A top-down point cloud view cannot distinguish these. The 2D RGB view can, immediately.
**This visualiser is what overturned the automated recall number**: the metric had reported
0.65 segmenter recall, and per-image review showed the projection and the metric were
wronging it -- 12 of 14 drawer handles were in fact all present.

## What it draws

Per description: pick the frame where the ground truth is most visible, run the segmenter
with the canonical concept term, then draw the RGB base image, the projected GT pixels as
red dots, every instance mask as a coloured contour, and the best-covering instance as a
yellow highlighted fill. The filename records hit/miss so a directory listing is already a
summary; ``--only_miss`` narrows the output to the failures.

    python code/task2/viz/viz_detections.py --n_desc 40 --sam3 <weights dir>
"""
import os, sys, json, argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import CODE, FUN3DU_DATA, FUN3DU_EXPS, SCENEFUN3D  # noqa: E402
PERCEPTION = os.path.join(_CODE_ROOT, "task2", "s1_perception")
sys.path.insert(0, os.path.join(CODE, "task1", "features"))
sys.path.insert(0, PERCEPTION)
from data_io import load_pointcloud, load_frames, project          # noqa: E402
from sam3_util import init_sam3, sam3_masks                        # noqa: E402
from frame_utils import coverage                                   # noqa: E402

ROOT = os.path.join(FUN3DU_DATA, "val")
DATA = SCENEFUN3D


def canonical(obj):
    """Collapse a parsed object phrase onto the generic term the segmenter responds to best."""
    o = obj.lower()
    if "handle" in o: return "handle"
    if "plug" in o or "socket" in o: return "socket"
    if "knob" in o: return "knob"
    if "switch" in o: return "switch"
    if "button" in o: return "button"
    return o.split()[-1]


def render(rgb, masks, gt_uv, best_i, path, title):
    H, W = rgb.shape[:2]
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.imshow(rgb)
    cmap = plt.get_cmap("tab10")
    for k, m in enumerate(masks):
        col = "yellow" if k == best_i else cmap(k % 10)
        ax.contour(m.astype(float), levels=[0.5], colors=[col],
                   linewidths=2.5 if k == best_i else 1.0)
        if k == best_i:
            ov = np.zeros((H, W, 4)); ov[m.astype(bool)] = (1, 1, 0, 0.35)
            ax.imshow(ov)
    ax.scatter(gt_uv[:, 0], gt_uv[:, 1], s=5, c="red", marker="o", zorder=5, label="GT points")
    ax.set_title(title, fontsize=11); ax.axis("off")
    ax.legend(loc="upper right", fontsize=9)
    fig.savefig(path, dpi=90, bbox_inches="tight"); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n_desc", type=int, default=40)
    ap.add_argument("--n_frames", type=int, default=12)
    ap.add_argument("--sam3", required=True)
    ap.add_argument("--det_th", type=float, default=0.3)
    ap.add_argument("--cov_th", type=float, default=0.5)
    ap.add_argument("--only_miss", action="store_true")
    ap.add_argument("--out_dir", default=os.path.join(FUN3DU_EXPS, "viz_sam3_2d"))
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    predictor = init_sam3(args.sam3)
    visits = sorted(d for d in os.listdir(ROOT) if d.isdigit())
    n_tot = n_drawn = n_hit = 0
    for v in visits:
        if n_tot >= args.n_desc: break
        cot_p = os.path.join(ROOT, v, f"{v}_qwen_cot.json")
        if not os.path.exists(cot_p): continue
        cot = json.load(open(cot_p))
        descs = json.load(open(f"{DATA}/{v}/{v}_descriptions.json"))["descriptions"]
        ann = {a["annot_id"]: np.asarray(a["indices"], np.int64)
               for a in json.load(open(f"{DATA}/{v}/{v}_annotations.json"))["annotations"]
               if a["label"] != "exclude"}
        P = load_pointcloud(DATA, v); Pf = P["P_full"]
        vdirs = [d for d in os.listdir(f"{DATA}/{v}") if d.isdigit() and os.path.isdir(f"{DATA}/{v}/{d}")]
        frames, parser = [], None
        for vid in vdirs:
            fd = load_frames(DATA, v, vid, parser=parser); parser = fd["parser"]
            frames += [(parser, fr) for fr in fd["frames"]]
        idxs = np.linspace(0, len(frames) - 1, min(args.n_frames, len(frames))).astype(int)

        for desc, c in zip(descs, cot):
            if n_tot >= args.n_desc: break
            obj = c.get("acted_on_object")
            if isinstance(obj, list): obj = obj[0] if obj else None
            tgt = [t for t in desc["annot_id"] if t in ann]
            if not obj or not tgt: continue
            gt_idx = ann[tgt[0]]
            best = (-1, None, None)
            for fi in idxs:
                prs, fr = frames[fi]
                depth = prs.read_depth_frame(fr["depth"]); rgb = prs.read_rgb_frame(fr["rgb"])
                o = project(Pf[gt_idx], fr["K"], fr["cam2world"], depth)
                vis = o["visible"]; nv = int(vis.sum())
                if nv > best[0]:
                    best = (nv, rgb, np.stack([o["u"][vis], o["v"][vis]], 1))
            nv, rgb, gt_uv = best
            if nv < 10: continue
            n_tot += 1
            concept = canonical(obj)
            masks = sam3_masks(predictor, rgb.astype(np.uint8), concept, det_th=args.det_th)
            covs = [coverage(m, gt_uv) for m in masks]
            best_i = int(np.argmax(covs)) if covs else -1
            best_cov = max(covs, default=0.0)
            hit = best_cov >= args.cov_th
            n_hit += int(hit)
            if args.only_miss and hit: continue
            title = f"{v} {obj}->{concept} | {'HIT' if hit else 'MISS'} best_cov={best_cov:.2f} n_inst={len(masks)}"
            render(rgb, masks, gt_uv, best_i,
                   os.path.join(args.out_dir, f"{v}_{desc['desc_id'][:8]}_{'hit' if hit else 'miss'}.png"), title)
            n_drawn += 1

    print(f"\n[viz_detections] scanned {n_tot} descriptions (hit {n_hit}), drew {n_drawn} -> {args.out_dir}")
    print("  Reading a MISS figure: is there a coloured contour on the red GT region?")
    print("    No contour  = the segmenter never segmented that handle. A recall dead spot;")
    print("                  only a different concept term or a spatial prompt can help.")
    print("    Contour but no yellow highlight, or visibly offset = the mask is smeared,")
    print("                  covering under 50%. Mask refinement can recover this one.")


if __name__ == "__main__":
    main()
