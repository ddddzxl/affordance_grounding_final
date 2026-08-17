#!/usr/bin/env python3
"""Quantify per-frame pose alignment quality objectively, without relying on visual
inspection.

## The criterion

Every point in colored.ply carries an RGB value, fused across frames during scanning. Project
a point into a given frame and sample the image at that pixel: if the pose is correct, the
sampled colour should agree closely with the point's own colour. If the pose is wrong, the
sample comes from somewhere else entirely and the agreement collapses.

Three numbers are reported:

    dRGB     mean |sampled colour - point colour| (0-255); lower is better
    corr     Pearson correlation of the two luminances; closer to 1 is better
    shuffle  dRGB recomputed after shuffling the point order -- the reference level for
             "completely unaligned". The real dRGB must be substantially below the shuffle
             value, or that frame's pose carries no information.

⚠️ The point colours are a multi-frame fusion and a single frame differs in lighting and
   exposure, so dRGB will never be 0. What matters is its **gap** from the shuffle baseline,
   not its absolute value.

  python src/demo/task2_align_check.py --scan all
"""
import os, sys, json, glob, argparse
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


def frame_align(xyz, pc_rgb, fr, rng, sub):
    rgb = read_rgb(fr["rgb"], upright=True)
    H, W = rgb.shape[:2]
    if (W, H) != (fr["W"], fr["H"]):
        return None
    u, v, z = project_frame(xyz, fr)
    vis = visible(u, v, z, W, H, zbuf_tol=0.05)
    n = int(vis.sum())
    if n < 200:
        return None
    idx = np.nonzero(vis)[0]
    if len(idx) > sub:
        idx = rng.choice(idx, sub, replace=False)
    uu = np.clip(u[idx].astype(int), 0, W - 1)
    vv = np.clip(v[idx].astype(int), 0, H - 1)
    samp = rgb[vv, uu].astype(np.float64)
    ref = pc_rgb[idx].astype(np.float64)
    d = float(np.abs(samp - ref).mean())
    ls, lr = samp.mean(1), ref.mean(1)
    corr = float(np.corrcoef(ls, lr)[0, 1]) if ls.std() > 1e-6 and lr.std() > 1e-6 else 0.0
    shuf = float(np.abs(samp - ref[rng.permutation(len(ref))]).mean())
    return dict(n=n, dRGB=d, corr=corr, shuffle=shuf, gain=shuf - d)


def run(scan, args):
    sd = os.path.join(DATA, scan)
    od = os.path.join(OUT, scan, "selfcheck")
    os.makedirs(od, exist_ok=True)
    xyz, pc_rgb = read_ply(os.path.join(sd, "colored.ply"))
    frames = read_frames(sd, upright=True)
    rng = np.random.default_rng(0)
    rows = []
    for i, fr in enumerate(frames):
        r = frame_align(xyz, pc_rgb, fr, rng, args.sub)
        if r is not None:
            r["frame"] = i
            r["mq"] = json.load(open(fr["rgb"].replace(".jpg", ".json"))).get("motionQuality")
            rows.append(r)
    if not rows:
        print(f"{scan}: no evaluable frames"); return

    d = np.array([r["dRGB"] for r in rows]); s = np.array([r["shuffle"] for r in rows])
    c = np.array([r["corr"] for r in rows]); g = np.array([r["gain"] for r in rows])
    print(f"\n=== {scan} ===  {len(rows)} frames")
    print(f"  dRGB      median {np.median(d):>6.1f}   (shuffle baseline {np.median(s):>6.1f})")
    print(f"  gain      median {np.median(g):>6.1f}   -- larger is better aligned; near 0 "
          f"means the pose carries no information")
    print(f"  corr      median {np.median(c):>6.3f}   best {c.max():.3f}   worst {c.min():.3f}")
    good = [r for r in rows if r["corr"] >= args.corr_th]
    print(f"  corr >= {args.corr_th}: {len(good)}/{len(rows)} frames "
          f"({100*len(good)/len(rows):.0f}%)")
    if good:
        top = sorted(good, key=lambda r: -r["corr"])[:8]
        print(f"  best frames: {[(r['frame'], round(r['corr'], 2)) for r in top]}")
    mq = [r["mq"] for r in rows if r["mq"] is not None]
    if mq:
        print(f"  motionQuality: median {np.median(mq):.2f}  range [{min(mq):.2f}, {max(mq):.2f}]")
        if len(set(mq)) > 1:
            print(f"  corr vs motionQuality correlation: "
                  f"{np.corrcoef(c, np.array(mq, float))[0,1]:+.2f}")

    fig, axs = plt.subplots(2, 1, figsize=(11, 5.4), sharex=True)
    axs[0].plot([r["frame"] for r in rows], c, lw=1.5)
    axs[0].axhline(args.corr_th, color="r", ls="--", lw=1, label=f"threshold {args.corr_th}")
    axs[0].set_ylabel("colour corr"); axs[0].legend(fontsize=8)
    axs[0].set_title(f"{scan} — per-frame pose alignment quality")
    axs[1].plot([r["frame"] for r in rows], d, lw=1.4, label="dRGB (actual)")
    axs[1].plot([r["frame"] for r in rows], s, lw=1.0, ls="--", alpha=.6, label="shuffle baseline")
    axs[1].set_xlabel("frame"); axs[1].set_ylabel("|dRGB|"); axs[1].legend(fontsize=8)
    fig.savefig(os.path.join(od, "align.png"), dpi=120, bbox_inches="tight"); plt.close(fig)
    json.dump(rows, open(os.path.join(od, "align.json"), "w"), indent=1)
    print(f"  -> {od}/align.png")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", default="all")
    ap.add_argument("--sub", type=int, default=20000, help="points sampled per frame")
    ap.add_argument("--corr_th", type=float, default=0.5)
    args = ap.parse_args()
    for s in (SCANS if args.scan == "all" else [args.scan]):
        run(s, args)


if __name__ == "__main__":
    main()
