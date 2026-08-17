#!/usr/bin/env python3
"""Look directly at an RGB frame: the segmenter's candidates versus the ground-truth
annotation -- which is larger, and larger in what way.

## The question, which the numbers cannot separate but which have different fixes

Among the cases where a candidate has `cover > 0.5` but `contain < 0.5` -- the position is
right and the mask is roughly 1.9x the size of the ground truth -- what is the excess?

  (a) **A uniform ring of overspill.** The segmenter's boundary is coarse. Erosion or
      negative-point refinement fixes it.
  (b) **Smeared over the whole drawer front.** The concept is at the wrong granularity: the
      ground truth is the handle or the recess, the segmenter returned the entire panel.
      This needs a different concept term or a subdivision step, and no amount of erosion
      helps.
  (c) **The ground truth itself is extremely sparse**, only a few dozen annotated points.
      Nothing is wrong with the prediction; this is an annotation-convention artefact.

**This is the figure behind the granularity finding** reported in REPORT.md section 6.3 --
case (b) is the one that turned out to be the structural ceiling of the training-free route.

## Three panels, all on the anchor-best frame, all cropped to the GT neighbourhood

    A  clean RGB          -- reference, to see what the furniture actually is
    B  RGB + GT points    -- what shape and size the annotation actually is
    C  RGB + all masks    -- handle or whole panel; GT points drawn on top

    python code/task2/viz/viz_candidates.py --pool <pool> --from_json <experiment> --n 6
"""
import os, sys, glob, json, argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import FUN3DU, FUN3DU_DATA, FUN3DU_EXPS, RESULTS, SCENEFUN3D  # noqa: E402
sys.path.insert(0, FUN3DU); os.chdir(FUN3DU)
from run_lifting import get_prediction, get_visit_stuff            # noqa: E402
from utils import io                                               # noqa: E402
from utils.sun3d.data_parser import DataParser                     # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frame_utils import build_rgb_index, lookup_rgb, nms_2d        # noqa: E402

DATA = SCENEFUN3D
OUT = os.path.join(RESULTS, "viz_cand")
COLORS = [(255, 60, 60), (60, 160, 255), (60, 230, 120), (255, 190, 40), (220, 90, 240),
          (40, 230, 230), (255, 130, 60), (170, 120, 255), (120, 220, 60), (255, 90, 160)]
DEPTH_EPS = 0.10


def project_visible(pts3, K, c2w, depth, H, W):
    """3D -> pixels, with occluded points removed via the depth map.

    Without this, points behind a piece of furniture get painted onto its front face.
    """
    if len(pts3) == 0:
        return np.zeros((0, 2))
    w2c = np.linalg.inv(np.asarray(c2w, float))
    pc = (w2c[:3, :3] @ pts3.T).T + w2c[:3, 3]
    z = pc[:, 2]; K = np.asarray(K, float)
    u = K[0, 0] * pc[:, 0] / z + K[0, 2]; v = K[1, 1] * pc[:, 1] / z + K[1, 2]
    ok = (z > 1e-6) & (u >= 0) & (u < W) & (v >= 0) & (v < H)
    if not ok.any():
        return np.zeros((0, 2))
    Hd, Wd = depth.shape
    du = np.clip((u[ok] * Wd / W).astype(int), 0, Wd - 1)
    dv = np.clip((v[ok] * Hd / H).astype(int), 0, Hd - 1)
    dz = depth[dv, du]
    vis = (dz > 1e-6) & (np.abs(z[ok] - dz) < DEPTH_EPS)
    return np.stack([u[ok][vis], v[ok][vis]], 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=FUN3DU_DATA)
    ap.add_argument("--exp_root", default=FUN3DU_EXPS)
    ap.add_argument("--pool", default="clean_pool_fb")
    ap.add_argument("--anchor_exp", default="sam3_anchor")
    ap.add_argument("--from_json", default="som_fb_oracle",
                    help="pick cases from this experiment's per-question detail file")
    ap.add_argument("--bucket", default="big",
                    choices=["big", "miss", "hit", "all"],
                    help="big = right place but oversized mask (cover>.5 & contain<.5); "
                         "miss = no overlap at all; hit = contain>.5")
    ap.add_argument("--split", default="val"); ap.add_argument("--sf_nms", type=float, default=0.5)
    ap.add_argument("--n", type=int, default=6)
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    parser = DataParser(args.root, args.split); v2v = io.get_visit_to_videos(args.root, args.split)
    J = json.load(open(os.path.join(RESULTS, f"{args.from_json}.json")))
    ok = [r for r in J["recs"] if r["status"] == "OK" and "pick_contain" in r]
    sel = {"big":  lambda r: r["pick_cover"] > 0.5 and r["pick_contain"] <= 0.5,
           "miss": lambda r: r["pick_cover"] <= 0.1 and r["pick_contain"] <= 0.1,
           "hit":  lambda r: r["pick_contain"] > 0.5,
           "all":  lambda r: True}[args.bucket]
    cases = [r for r in ok if sel(r)][:args.n]
    print(f"[viz] bucket={args.bucket}: {len(cases)} cases -> {OUT}/", flush=True)

    cur, xyz = None, None
    for k, r in enumerate(cases, 1):
        v, did = r["visit"], r["desc"]
        if v != cur:
            p = parser.get_laser_scan(v); p = parser.get_cropped_laser_scan(v, p)
            xyz = np.asarray(p.points); cur = v
        gt = np.asarray(parser.get_grouped_annotation(v, did)).astype(bool)
        vs = get_visit_stuff(parser, v, v2v[v])
        md = get_prediction(args.exp_root, args.pool, parser, v, "frames", did, vs)
        md_a = get_prediction(args.exp_root, args.anchor_exp, parser, v, "frames", did, vs)
        if md is None or not len(md["masks_f"]):
            continue

        # Anchor-best frame plus within-frame NMS, matched exactly to the selection stage, so
        # that what is drawn is the same candidate set that carried those ids at the time.
        a_area = {}
        if md_a is not None:
            for i in range(len(md_a["masks_f"])):
                dp = md_a["depth_paths"][i]; a_area[dp] = a_area.get(dp, 0) + int(md_a["masks_f"][i].sum())
        by_frame = {}
        for i in range(len(md["masks_f"])):
            by_frame.setdefault(md["depth_paths"][i], []).append(i)
        best_dp = max(by_frame, key=lambda dp: (a_area.get(dp, 0), len(by_frame[dp])))
        rows = nms_2d(md["masks_f"], by_frame[best_dp], args.sf_nms)
        i0 = rows[0]
        rp = lookup_rgb(build_rgb_index(DATA, v, str(md["video_ids"][i0])), str(md["frame_ids"][i0]))
        if rp is None:
            continue
        rgb = np.asarray(Image.open(rp).convert("RGB")); H, W = rgb.shape[:2]
        depth = parser.read_depth_frame(best_dp)
        gt_uv = project_visible(xyz[gt], md["intrinsics"][i0], md["poses"][i0], depth, H, W)
        if len(gt_uv) < 3:
            print(f"  [skip] {v} {did[:8]} GT not visible in this frame"); continue

        over = rgb.astype(np.float32).copy()
        for j, ri in enumerate(rows):
            m = np.asarray(md["masks_f"][ri], bool)
            if m.shape != (H, W):
                m = np.asarray(Image.fromarray(m.astype(np.uint8) * 255).resize((W, H), Image.NEAREST)) > 127
            over[m] = 0.55 * over[m] + 0.45 * np.array(COLORS[j % len(COLORS)], np.float32)

        # ⚠️ The crop box was once computed from the GT alone, which cut off candidates lying
        # outside it -- so the figure showed fewer coloured blobs than the candidate count in
        # its own title. Candidate centroids are now included in the box, and the title
        # reports "how many are inside the crop / how many there are".
        cxs, cys = [], []
        for ri in rows:
            m_ = np.asarray(md["masks_f"][ri], bool)
            ys_, xs_ = np.where(m_)
            if len(xs_):
                cxs.append(xs_.mean() * W / m_.shape[1]); cys.append(ys_.mean() * H / m_.shape[0])
        ax_all = np.concatenate([gt_uv[:, 0], np.asarray(cxs)]) if cxs else gt_uv[:, 0]
        ay_all = np.concatenate([gt_uv[:, 1], np.asarray(cys)]) if cys else gt_uv[:, 1]
        x0, x1 = ax_all.min(), ax_all.max(); y0, y1 = ay_all.min(), ay_all.max()
        pad = max(120, 0.25 * max(x1 - x0, y1 - y0))
        box = (max(0, x0 - pad), min(W, x1 + pad), max(0, y0 - pad), min(H, y1 + pad))
        n_in = int(sum(1 for a, b in zip(cxs, cys) if box[0] <= a <= box[1] and box[2] <= b <= box[3]))

        fig, axs = plt.subplots(1, 3, figsize=(19, 6.2))
        for ax, im, title in ((axs[0], rgb, "A: clean RGB"),
                              (axs[1], rgb, f"B: GT annotation only ({int(gt.sum())} 3D pts)"),
                              (axs[2], np.clip(over, 0, 255).astype(np.uint8),
                               f"C: candidates {n_in}/{len(rows)} in view + GT")):
            ax.imshow(im); ax.set_autoscale_on(False); ax.axis("off"); ax.set_title(title, fontsize=11)
            ax.set_xlim(box[0], box[1]); ax.set_ylim(box[3], box[2])
        for ax in (axs[1], axs[2]):
            ax.scatter(gt_uv[:, 0], gt_uv[:, 1], s=14, c="black", zorder=5)
            ax.scatter(gt_uv[:, 0], gt_uv[:, 1], s=5, c="white", zorder=6)
        fig.suptitle(f"{v} {did[:8]}  \"{r['text'][:70]}\"\n"
                     f"picked candidate: cover={r['pick_cover']:.2f} contain={r['pick_contain']:.2f} "
                     f"-> |cand| ~ {r['pick_cover']/max(r['pick_contain'],1e-6):.1f}x |gt|   "
                     f"(black/white dots = GT, colours = candidates)", fontsize=11)
        fig.tight_layout()
        out = f"{OUT}/{args.bucket}_{v}_{did[:8]}.png"
        fig.savefig(out, dpi=100, bbox_inches="tight"); plt.close(fig)
        print(f"  [{k}] {v} {did[:8]} cov={r['pick_cover']:.2f} ct={r['pick_contain']:.2f} "
              f"cands={len(rows)} -> {os.path.basename(out)}", flush=True)

    print(f"\n[done] -> {OUT}/")
    print("  Panel B shows how large and what shape the annotation itself is; panel C shows")
    print("  whether the coloured candidates hug the handle or cover the entire panel.")
    print("  (a) blob only slightly larger than GT -> coarse boundary; erosion fixes it")
    print("  (b) blob covers the whole drawer front -> wrong concept granularity; needs a")
    print("      different concept term or a subdivision step, not erosion")
    print("  (c) GT itself is only a few dozen scattered points -> an annotation-convention")
    print("      artefact; the prediction is not wrong")


if __name__ == "__main__":
    main()
