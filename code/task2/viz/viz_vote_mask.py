#!/usr/bin/env python3
"""Project the predicted mask and the ground truth back onto an RGB frame to see *where*
precision (the official AP50 criterion) is being lost.

## Three ways this figure used to lie, all now fixed -- read before editing

**1. Occlusion filtering is mandatory.** A bare projection paints points that are
*behind* an object onto the surface in front of it. Measured case: the ground truth for
"Unplug the TV" (label `unplug`, 208 points, the socket behind the television) projected
onto the television screen, and the figure appeared to show "the GT is inside the screen".
Entirely an artefact. This version resolves visibility against the frame's depth map
(`|z_proj - depth| < eps`).

**2. The point counts in the legend are 2D counts, not 3D counts.** Projection drops
out-of-frame and back-facing points and collapses several points onto one pixel, so the
proportions do not match the 3D proportions that actually determine precision. The true 3D
counts go in the title; the 2D numbers are explicitly annotated "(2D proj)".

**3. Histograms were unreadable.** Replaced with precision/recall as a function of the
threshold, which answers the question that was actually being asked -- would tightening
gain anything?

## Four panels

    A  clean RGB, no overlay at all (the reference)
    B  the same frame with the overlay: green = correct, red = spilled out, blue = missed
    C  depth profile in camera coordinates (horizontal vs depth), showing whether the red
       points genuinely lie on a different surface
    D  precision / recall against the voting threshold

    python code/task2/viz/viz_vote_mask.py --exp <experiment> --n 8
"""
import os, sys, glob, argparse
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
from frame_utils import best_frame, build_rgb_index, lookup_rgb    # noqa: E402

OUT = os.path.join(RESULTS, "viz_vote")
DEPTH_EPS = 0.10   # metres. Looser than the lift's 0.03: this only has to reject points seen
                   # through a wall, it is not attempting a faithful reconstruction.


def project_visible(pts3, K, c2w, depth, eps=DEPTH_EPS):
    """3D -> pixels, **discarding occluded points using the depth map**.

    Without the depth test, things behind an object get painted onto the surface in front of
    it, which is failure mode 1 in the module docstring.

    Returns ``(uv (M,2), n_in_frame, n_visible)``.
    """
    if len(pts3) == 0:
        return np.zeros((0, 2)), 0, 0
    w2c = np.linalg.inv(np.asarray(c2w, float))
    pc = (w2c[:3, :3] @ pts3.T).T + w2c[:3, 3]                  # (N,3) in camera coordinates
    z = pc[:, 2]
    K = np.asarray(K, float)
    u = K[0, 0] * pc[:, 0] / z + K[0, 2]
    v = K[1, 1] * pc[:, 1] / z + K[1, 2]
    Hd, Wd = depth.shape
    # RGB and depth may differ in resolution -> rescale uv onto the depth grid using the
    # image size the intrinsics were given for.
    Himg, Wimg = (1920, 1440)
    ok = (z > 1e-6) & (u >= 0) & (u < Wimg) & (v >= 0) & (v < Himg)
    n_in = int(ok.sum())
    if n_in == 0:
        return np.zeros((0, 2)), 0, 0
    du = np.clip((u[ok] * Wd / Wimg).astype(int), 0, Wd - 1)
    dv = np.clip((v[ok] * Hd / Himg).astype(int), 0, Hd - 1)
    dz = depth[dv, du]
    vis = (dz > 1e-6) & (np.abs(z[ok] - dz) < eps)              # <- the occlusion test
    uv = np.stack([u[ok][vis], v[ok][vis]], 1)
    return uv, n_in, int(vis.sum())


def cam_frame(pts3, c2w):
    """World -> camera coordinates (x right, z depth), for the depth-profile panel."""
    if len(pts3) == 0:
        return np.zeros((0, 3))
    w2c = np.linalg.inv(np.asarray(c2w, float))
    return (w2c[:3, :3] @ pts3.T).T + w2c[:3, 3]


def scat(ax, uv, c, lab, s=7):
    if len(uv):
        ax.scatter(uv[:, 0], uv[:, 1], s=s, c=c, alpha=0.75, label=f"{lab} {len(uv)} (2D proj)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=FUN3DU_DATA)
    ap.add_argument("--exp_root", default=FUN3DU_EXPS)
    ap.add_argument("--exp", required=True); ap.add_argument("--pool", default="clean_pool_d03")
    ap.add_argument("--split", default="val"); ap.add_argument("--th", type=float, default=0.7)
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--only", default=None, help="comma-separated desc_id prefixes; draw only these")
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    parser = DataParser(args.root, args.split); v2v = io.get_visit_to_videos(args.root, args.split)
    npzs = sorted(glob.glob(os.path.join(args.exp_root, args.exp, "pcds", "*.npz")))
    only = set(args.only.split(",")) if args.only else None
    print(f"[viz] {args.exp}: {len(npzs)} point clouds -> {OUT}/", flush=True)

    cur, xyz, done = None, None, 0
    for f in npzs:
        if done >= args.n:
            break
        base = os.path.basename(f)[:-4]; v, did = base.split("_", 1)
        if only and not any(did.startswith(o) for o in only):
            continue
        d = np.load(f)
        acc, nv = np.asarray(d["acc_f"], np.float32), float(np.asarray(d["n_views"]).ravel()[0])
        if acc.max() <= 0:
            continue
        if v != cur:
            p = parser.get_laser_scan(v); p = parser.get_cropped_laser_scan(v, p)
            xyz = np.asarray(p.points); cur = v
        gt = np.asarray(parser.get_grouped_annotation(v, did)).astype(bool)
        if not gt.sum():
            continue

        frac = acc / max(nv, 1.0); frac = frac / max(frac.max(), 1e-9)
        pred = frac > args.th
        inter = pred & gt
        prc = inter.sum() / max(pred.sum(), 1)                  # = the official AP50 criterion
        rec = inter.sum() / max(gt.sum(), 1)                    # = the official AR50 criterion

        md = get_prediction(args.exp_root, args.pool, parser, v, "frames", did,
                            get_visit_stuff(parser, v, v2v[v]))
        bf = best_frame(md, xyz[gt]) if md is not None else None
        if bf is None:
            continue
        K, c2w, vid, fid = bf
        dpath = next((md["depth_paths"][i] for i in range(len(md["frame_ids"]))
                      if str(md["video_ids"][i]) == vid and str(md["frame_ids"][i]) == fid), None)
        rp = lookup_rgb(build_rgb_index(SCENEFUN3D, v, vid), fid)
        if rp is None or dpath is None:
            continue
        rgb = np.asarray(Image.open(rp).convert("RGB"))
        depth = parser.read_depth_frame(dpath)

        sets = {"correct": xyz[inter], "SPILL": xyz[pred & ~gt], "GT missed": xyz[gt & ~pred]}
        proj = {k: project_visible(p3, K, c2w, depth) for k, p3 in sets.items()}

        fig = plt.figure(figsize=(20, 5.6))
        axA, axB, axC, axD = (fig.add_subplot(1, 4, i) for i in range(1, 5))

        allp = np.vstack([uv for uv, _, _ in proj.values() if len(uv)]) if any(
            len(uv) for uv, _, _ in proj.values()) else None
        zoom = None
        if allp is not None:
            x0, x1, y0, y1 = allp[:, 0].min(), allp[:, 0].max(), allp[:, 1].min(), allp[:, 1].max()
            pad = max(110, 0.5 * max(x1 - x0, y1 - y0))
            zoom = (x0 - pad, x1 + pad, y0 - pad, y1 + pad)

        for ax, title in ((axA, "A: clean RGB (reference)"), (axB, "B: overlay (occlusion-filtered)")):
            ax.imshow(rgb); ax.set_autoscale_on(False); ax.axis("off"); ax.set_title(title, fontsize=11)
            if zoom:
                ax.set_xlim(zoom[0], zoom[1]); ax.set_ylim(zoom[3], zoom[2])
        scat(axB, proj["GT missed"][0], "deepskyblue", "GT missed")
        scat(axB, proj["correct"][0], "lime", "correct")
        scat(axB, proj["SPILL"][0], "red", "SPILL")
        axB.legend(fontsize=8, loc="upper right", framealpha=0.85)

        # Panel C, depth profile in camera x-z: red points separated in depth from the green
        # ones means they genuinely landed on a different surface.
        for k, c in (("correct", "lime"), ("SPILL", "red"), ("GT missed", "deepskyblue")):
            P = cam_frame(sets[k], c2w)
            if len(P):
                axC.scatter(P[:, 0], P[:, 2], s=8, c=c, alpha=0.7, label=f"{k} {len(P)} (3D)")
        axC.set_xlabel("camera x / right (m)"); axC.set_ylabel("camera z / depth (m)")
        axC.set_title("C: depth profile - same surface?", fontsize=11)
        axC.legend(fontsize=8); axC.grid(alpha=0.25)

        # Panel D, precision / recall against threshold: does tightening gain anything?
        ths = np.linspace(0.05, 0.99, 40)
        pr = [(frac > t) for t in ths]
        pv = [float((m & gt).sum()) / max(int(m.sum()), 1) for m in pr]
        rv = [float((m & gt).sum()) / max(int(gt.sum()), 1) for m in pr]
        axD.plot(ths, pv, "-o", ms=3, c="tab:purple", label="precision (= AP50 criterion)")
        axD.plot(ths, rv, "-s", ms=3, c="tab:orange", label="recall (= AR50 criterion)")
        axD.axhline(0.5, color="gray", ls=":", lw=1, label="0.5 (AP50/AR50 pass line)")
        axD.axvline(args.th, color="k", ls="--", lw=1.5, label=f"current th={args.th}")
        axD.set_xlabel("vote-fraction threshold"); axD.set_ylabel("value"); axD.set_ylim(0, 1.02)
        axD.set_title("D: does tightening help?", fontsize=11)
        axD.legend(fontsize=7); axD.grid(alpha=0.25)

        n3 = {k: len(p3) for k, p3 in sets.items()}
        fig.suptitle(f"{v} {did[:8]}   3D pts: correct={n3['correct']} SPILL={n3['SPILL']} "
                     f"missed={n3['GT missed']}  |  precision={prc:.2f} (official AP50 crit.) "
                     f"recall={rec:.2f}  |pred|={int(pred.sum())} |gt|={int(gt.sum())}", fontsize=12)
        fig.tight_layout()
        out = f"{OUT}/{v}_{did[:8]}_prc{prc:.2f}.png"
        fig.savefig(out, dpi=100, bbox_inches="tight"); plt.close(fig)
        print(f"  [{done+1}] {v} {did[:8]} prc={prc:.2f} rec={rec:.2f} "
              f"3D(ok={n3['correct']} spill={n3['SPILL']} miss={n3['GT missed']}) "
              f"-> {os.path.basename(out)}", flush=True)
        done += 1

    print(f"\n[done] {done} figures -> {OUT}/")
    print("  A clean RGB reference | B overlay (occlusion-filtered: points behind a surface")
    print("    are no longer painted onto the surface in front of it)")
    print("  C depth profile: if red (SPILL) separates in depth from green (correct), the mask")
    print("    genuinely smeared onto another surface; if they sit at the same depth it is only")
    print("    the handle's own rim -- a slightly loose mask, a completely different problem")
    print("  D whether the purple precision curve rises as the threshold tightens: rising means")
    print("    tightening is a free gain; flat means voting already removed the fringe and the")
    print("    fix has to happen in candidate generation instead")


if __name__ == "__main__":
    main()
