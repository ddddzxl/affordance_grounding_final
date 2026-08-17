#!/usr/bin/env python3
"""Geometry self-check on the demo data: **verify the projection before running any model.**

The effort the closed-set demo spent here was worthwhile (its projection self-check put
8770 of 8770 points in frame). The instruction-level demo adds an EXIF rotation on top, and
its failure mode is more insidious: with the intrinsics and the image 90 degrees apart, the
projected points still "look like they land on the image" while being uniformly displaced,
and no summary statistic reveals it. So this **must** render figures for visual confirmation.

Writes `<out>/<scan>/selfcheck/`:
  proj_f####.png   RGB | projected cloud (depth coloured) | overlay -- a triptych, to see
                   whether the points sit on the objects
  cover.png        visible-point count per frame, for picking the most complete view
  stats.txt        numeric summary

  python src/demo/task2_selfcheck.py --scan Drawer_Cups
  python src/demo/task2_selfcheck.py --scan all --nviz 4
"""
import os, sys, argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _CODE_ROOT)
from paths import PROJECT_ROOT  # noqa: E402
ROOT = PROJECT_ROOT
sys.path.insert(0, os.path.join(ROOT, "src/demo"))
from iphone_io import read_ply, read_frames, read_rgb, project_frame, visible   # noqa: E402

DATA = os.path.join(ROOT, "data/iphone_3dscanner")
OUT = os.path.join(ROOT, "viz/func_seg/demo_task2")
SCANS = ["Drawer_Cups", "Kitchen_Task2", "Sofa_Switch"]


def triptych(path, rgb, u, v, z, vis, title):
    fig, axs = plt.subplots(1, 3, figsize=(21, 8))
    axs[0].imshow(rgb); axs[0].set_title("RGB (EXIF-corrected)")
    axs[1].imshow(np.full_like(rgb, 255))
    if vis.any():
        sc = axs[1].scatter(u[vis], v[vis], s=1.2, c=z[vis], cmap="viridis", linewidths=0)
        plt.colorbar(sc, ax=axs[1], fraction=0.03, label="depth (m)")
    axs[1].set_xlim(0, rgb.shape[1]); axs[1].set_ylim(rgb.shape[0], 0)
    axs[1].set_title("projected cloud (depth)")
    axs[2].imshow(rgb)
    if vis.any():
        axs[2].scatter(u[vis], v[vis], s=1.0, c=z[vis], cmap="viridis", alpha=.55, linewidths=0)
    axs[2].set_title("overlay — points must sit ON the objects")
    for a in axs:
        a.axis("off")
    fig.suptitle(title, fontsize=13)
    fig.savefig(path, dpi=110, bbox_inches="tight"); plt.close(fig)


def run(scan, args):
    sd = os.path.join(DATA, scan)
    od = os.path.join(OUT, scan, "selfcheck")
    os.makedirs(od, exist_ok=True)
    xyz, _ = read_ply(os.path.join(sd, "colored.ply"))
    frames = read_frames(sd, upright=not args.raw)
    lines = [f"=== {scan} ===",
             f"cloud {len(xyz):,} points   frames {len(frames)}   "
             f"coordinate system {'original landscape' if args.raw else 'EXIF-corrected upright'}",
             f"cloud bounding box (m): min={np.round(xyz.min(0), 2).tolist()}  "
             f"max={np.round(xyz.max(0), 2).tolist()}  "
             f"size={np.round(xyz.max(0) - xyz.min(0), 2).tolist()}"]

    ncov, nvis0 = [], []
    for fr in frames:
        u, v, z = project_frame(xyz, fr)
        vis = visible(u, v, z, fr["W"], fr["H"], zbuf_tol=args.zbuf)
        v0 = visible(u, v, z, fr["W"], fr["H"], zbuf_tol=0)
        ncov.append(int(vis.sum())); nvis0.append(int(v0.sum()))
    ncov, nvis0 = np.array(ncov), np.array(nvis0)
    lines += [f"visible points per frame: median {np.median(ncov):.0f}  max {ncov.max()}  "
              f"min {ncov.min()}  ({100*np.median(ncov)/len(xyz):.1f}% of the cloud)"]
    if args.zbuf > 0:
        occ = 100 * (1 - ncov.sum() / max(nvis0.sum(), 1))
        lines += [f"z-buffer (tol={args.zbuf} m) rejected {occ:.1f}% of in-frustum points as occluded"]
    seen = np.zeros(len(xyz), bool)
    for fr in frames:
        u, v, z = project_frame(xyz, fr)
        seen |= visible(u, v, z, fr["W"], fr["H"], zbuf_tol=args.zbuf)
    lines += [f"all frames together cover {100*seen.mean():.1f}% of the points "
              f"-- a low value means the scan has blind spots; those points project into no "
              f"frame at all and lifting cannot reach them"]

    # Render the frames with the most visible points.
    # ⚠️ This choice has a **selection bias**: a frame with a wrong pose projects large
    #    numbers of points into view and therefore scores the highest visible count, so the
    #    self-check preferentially shows bad frames. Use --frames to inspect good ones.
    if args.frames:
        pick = np.array([int(x) for x in args.frames.split(",")])
    else:
        pick = np.argsort(-ncov)[:args.nviz]
    for i in sorted(pick.tolist()):
        fr = frames[i]
        rgb = read_rgb(fr["rgb"], upright=not args.raw)
        if rgb.shape[1] != fr["W"] or rgb.shape[0] != fr["H"]:
            lines += [f"⚠️ frame {i}: image {rgb.shape[1]}x{rgb.shape[0]} disagrees with the "
                      f"intrinsics frame size {fr['W']}x{fr['H']} -- EXIF and intrinsics "
                      f"are out of step"]
        u, v, z = project_frame(xyz, fr)
        vis = visible(u, v, z, fr["W"], fr["H"], zbuf_tol=args.zbuf)
        triptych(os.path.join(od, f"proj_f{i:04d}.png"), rgb, u, v, z, vis,
                 f"{scan}  frame {i}  ({int(vis.sum()):,} / {len(xyz):,} pts visible)")

    fig, ax = plt.subplots(figsize=(11, 3.2))
    ax.plot(ncov, lw=1.4, label="visible (with z-buffer)" if args.zbuf > 0 else "visible")
    if args.zbuf > 0:
        ax.plot(nvis0, lw=1.0, ls="--", alpha=.6, label="in-frustum only")
    ax.set_xlabel("frame"); ax.set_ylabel("# points"); ax.legend(fontsize=8)
    ax.set_title(f"{scan} — per-frame point coverage")
    fig.savefig(os.path.join(od, "cover.png"), dpi=120, bbox_inches="tight"); plt.close(fig)

    open(os.path.join(od, "stats.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"  figures -> {od}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", default="all")
    ap.add_argument("--nviz", type=int, default=3, help="how many triptychs to render")
    ap.add_argument("--zbuf", type=float, default=0.0,
                    help="z-buffer occlusion tolerance in metres; 0 = frustum test only")
    ap.add_argument("--frames", default="",
                    help="explicit frame indices to render, comma separated")
    ap.add_argument("--raw", action="store_true",
                    help="use the original landscape coordinate system (for comparison "
                         "only) -- do not enable for a normal run")
    args = ap.parse_args()
    for s in (SCANS if args.scan == "all" else [args.scan]):
        run(s, args)


if __name__ == "__main__":
    main()
