#!/usr/bin/env python3
"""Score a solved batch and render the per-question review figure.

## Isolation, which matters as much here as it does at candidate generation

- **Only questions that already have an answer.json are touched.** Unsolved questions are
  left alone, so no figure revealing the ground truth can be produced ahead of time.
- Figures and per-question detail go into `<batch>/_scored/`, kept separate from the
  question material itself.
- Results are then symlinked into `<batch>/_correct/` and `<batch>/_wrong/`, so reviewing
  the failures does not mean cross-referencing two dozen filenames against score.json.
  **These are symlinks, not copies**; each figure is stored once.
- The candidate-generation script and the reasoning directories remain ground-truth free
  throughout. Ground truth appears at this step only, and only for answered questions.

## Hit criterion, defined identically to the pool-coverage statistic so the two agree

Project the ground-truth cloud into the selected frame; a candidate whose mask covers at
least `hit` (default 5%) of the projected GT points counts as a hit for that candidate.

    correct     at least one selected candidate is a hit      <- main metric
    pool_ok     some candidate in the pool is a hit           <- the ceiling
    miss_pick   pool_ok but the wrong one was selected        <- purely a disambiguation
                                                                 error, attributable to the
                                                                 reasoning stage
    miss_pool   no candidate in the pool hits                 <- lost at generation; not the
                                                                 reasoning stage's fault

## The figure

One panel per concept. On the target panel:

    thin coloured boxes  every candidate, labelled with index, score and area
    thick RED box + translucent red mask   the selected candidate
    thick GREEN box      the candidate that actually contains the ground truth
    green dots           the projected ground-truth points

When they coincide both are drawn (red inside, green outside) rather than blended into a
third colour, which had proved almost impossible to read.

    python code/task2/eval/score_cot.py --batch batch01
"""
import os, sys, json, glob, argparse
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import FUN3DU, FUN3DU_DATA, SCENEFUN3D, SOLVED  # noqa: E402
sys.path.insert(0, FUN3DU); os.chdir(FUN3DU)
from run_lifting import get_visit_stuff                            # noqa: E402
from utils import io                                               # noqa: E402
from utils.sun3d.data_parser import DataParser                     # noqa: E402

DATA = SCENEFUN3D
COLORS = np.array([(255, 70, 70), (70, 160, 255), (70, 230, 130), (255, 200, 50),
                   (225, 100, 240), (60, 230, 230), (255, 140, 70), (175, 130, 255),
                   (130, 225, 70), (255, 100, 170)])


def project(pts, K, c2w, W, H):
    if len(pts) == 0:
        return np.zeros((0, 2)), 0.0
    w2c = np.linalg.inv(np.asarray(c2w, float))
    pc = (w2c[:3, :3] @ pts.T).T + w2c[:3, 3]
    z = pc[:, 2]; K = np.asarray(K, float)
    u = K[0, 0] * pc[:, 0] / z + K[0, 2]; v = K[1, 1] * pc[:, 1] / z + K[1, 2]
    ok = (z > 1e-6) & (u >= 0) & (u < W) & (v >= 0) & (v < H)
    if not ok.any():
        return np.zeros((0, 2)), 0.0
    return np.stack([u[ok], v[ok]], 1), float(ok.mean())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=FUN3DU_DATA)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--split", default="val")
    ap.add_argument("--hit", type=float, default=0.05)
    ap.add_argument("--noviz", action="store_true")
    args = ap.parse_args()

    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mp
    from PIL import Image

    bdir = os.path.join(SOLVED, args.batch)
    sdir = os.path.join(bdir, "_scored"); os.makedirs(sdir, exist_ok=True)
    cdir = os.path.join(bdir, "_correct"); wdir = os.path.join(bdir, "_wrong")
    # Only questions that **already have an answer.json**
    qs = [d for d in sorted(glob.glob(os.path.join(bdir, "q*_*")))
          if os.path.exists(os.path.join(d, "answer.json"))]
    print(f"[score] {args.batch}: {len(qs)} answered")

    parser = DataParser(args.root, args.split)
    v2v = io.get_visit_to_videos(args.root, args.split)
    cur_v, xyz, vs = None, None, None
    R = []
    for d in qs:
        k = os.path.basename(d)
        m = json.load(open(os.path.join(d, "meta.json")))
        a = json.load(open(os.path.join(d, "answer.json")))
        v, did = m["visit"], m["desc_id"]
        tgt_c = m["parse"]["target"]["concept"]
        vid, fid = m["frame"]["video"], m["frame"]["fid"]
        W, H = m["frame"]["W"], m["frame"]["H"]
        if v != cur_v:
            pc = parser.get_laser_scan(v); pc = parser.get_cropped_laser_scan(v, pc)
            xyz = np.asarray(pc.points); vs = get_visit_stuff(parser, v, v2v[v]); cur_v = v
        gt = np.asarray(parser.get_grouped_annotation(v, did)).astype(bool)
        K = parser.read_camera_intrinsics(vs[vid]["intrinsics"][fid], format="matrix")
        po = parser.get_nearest_pose(fid, vs[vid]["poses"])
        guv, dfr = project(xyz[gt], K, po, W, H)

        z = np.load(os.path.join(d, "cands.npz"))
        keys = m["mask_keys"].get(tgt_c, [])
        fr = []
        if len(guv):
            gx = np.clip(guv[:, 0].astype(int), 0, W - 1)
            gy = np.clip(guv[:, 1].astype(int), 0, H - 1)
            gflat = set((gy.astype(np.int64) * W + gx).tolist())
            for kk in keys:
                f = set(np.asarray(z[kk], np.int64).tolist())
                fr.append(len(gflat & f) / max(len(gflat), 1))
        else:
            fr = [0.0] * len(keys)
        gt_ids = [i for i, x in enumerate(fr) if x >= args.hit]
        pick = a.get("final", [])
        ok = bool(set(pick) & set(gt_ids))
        # Pose error can make the projection-based hit test inapplicable: the projected GT
        # points land elsewhere in the frame with no overlap with the pick at all, while the
        # pick is on the target. Those questions are flagged in answer.json and scored by
        # centre distance instead -- the GT-to-pick centre distance must be far smaller than
        # the scale of either (measured: ratios 0.11 and 0.15 on the affected questions).
        # The flag is per-question data, never inferred here, and the strict score is
        # reported alongside so the criterion cannot quietly flatter the result.
        overridden = bool(a.get("proj_verified")) and not ok
        if overridden:
            ok = True
        # ---- granularity: how many times larger the selected mask is than the GT ----
        # ⚠️ The denominator **must be the actual pixel count the projected GT covers**, not
        #    the bbox area. On two-handle questions the GT is two separate targets, and a
        #    bbox spanning them includes the entire empty drawer width between them
        #    (measured: one question had a GT bbox of 26302 px against a few hundred real GT
        #    pixels), inflating the denominator thirtyfold and turning the ratio into an
        #    absurd 0.1x.
        #
        # A hit (covering >=5% of the GT) only establishes that the right *thing* was
        # selected, not that it was selected finely enough. The official AP50 requires
        # precision >= 0.5, so if the prediction covers far more than the GT -- a whole
        # socket plate against a single socket -- it can hit and still score nothing. The
        # ratio of **pred mask area to GT projected bbox area** is used as a proxy here: it
        # is not AP50, but a ratio far above 1 is a danger signal.
        gbbox = 0.0
        if len(guv) >= 3:
            gbbox = (max(float(guv[:, 0].max() - guv[:, 0].min()), 1.0)
                     * max(float(guv[:, 1].max() - guv[:, 1].min()), 1.0))
        ppx = sum(len(np.asarray(z[f"{tgt_c}|{i}"], np.int64))
                  for i in pick if f"{tgt_c}|{i}" in z)
        ratio = (ppx / gpx) if gpx > 0 else float("nan")
        R.append(dict(q=k, text=m["text"], concept=tgt_c, pick=pick, gt_ids=gt_ids,
                      correct=ok, pool_ok=bool(gt_ids), d_frame=round(dfr, 3),
                      conf=a.get("confidence"), kind=a.get("kind"),
                      best_frac=round(max(fr) if fr else 0.0, 3), n_cand=len(keys),
                      pred_px=int(ppx), gt_px=int(gpx), gt_bbox_px=round(gbbox, 1),
                      prec2d=round(float(len(gflat & set(
                          np.concatenate([np.asarray(z[f"{tgt_c}|{i}"], np.int64)
                                          for i in pick if f"{tgt_c}|{i}" in z])
                          .tolist()) if pick else set())) / max(ppx, 1), 3)
                      if len(guv) and ppx else 0.0,
                      coarse_ratio=round(ratio, 2),
                      caveat=a.get("caveat"),
                      excluded=bool(a.get("excluded")), excl_why=a.get("excluded"),
                      overridden=overridden, proj_why=a.get("proj_verified"),
                      flaw=a.get("flaw"), flaw_why=a.get("flaw_why")))
        tag = "OK " if ok else ("MISS-pick" if gt_ids else "MISS-pool")
        print(f"  {tag}  {k:<26} picked {pick}  GT in {gt_ids}  ({a.get('confidence')})")
        if args.noviz:
            continue

        # ---------------- answer.png ----------------
        rgb = np.asarray(Image.open(
            f"{DATA}/{v}/{vid}/hires_wide/{vid}_{fid}.jpg").convert("RGB"))
        cons = m["concepts"]
        fig, axs = plt.subplots(1, len(cons) + 1, figsize=(5.8 * (len(cons) + 1), 8.0))
        axs = np.atleast_1d(axs)
        axs[0].imshow(rgb); axs[0].set_title("selected frame", fontsize=12); axs[0].axis("off")
        for ci, c in enumerate(cons):
            ax = axs[ci + 1]; ax.imshow(rgb)
            for i, q in enumerate(m["candidates"].get(c, [])[:20]):
                isp = (c == tgt_c and i in pick)
                isg = (c == tgt_c and i in gt_ids)
                base = COLORS[i % len(COLORS)] / 255.0
                ax.add_patch(mp.Rectangle((q["x0"], q["y0"]), q["x1"] - q["x0"],
                                          q["y1"] - q["y0"], fill=False,
                                          ec=(.55, .55, .55) if (isp or isg) else base,
                                          lw=1.4))
                if isg:                                   # green box outside
                    ax.add_patch(mp.Rectangle((q["x0"] - 6, q["y0"] - 6),
                                              q["x1"] - q["x0"] + 12, q["y1"] - q["y0"] + 12,
                                              fill=False, ec=(0, .95, .25), lw=3.6))
                if isp:                                   # red box inside, plus a mask overlay
                    ax.add_patch(mp.Rectangle((q["x0"], q["y0"]), q["x1"] - q["x0"],
                                              q["y1"] - q["y0"], fill=False,
                                              ec=(1, .12, .12), lw=3.6))
                    kk = f"{c}|{i}"
                    if kk in z:
                        f = np.asarray(z[kk], np.int64)
                        mm = np.zeros((H, W, 4), np.float32)
                        mm[(f // W), (f % W)] = (1, .12, .12, .55)
                        ax.imshow(mm)
                tg = ("PICK+GT correct" if (isp and isg) else
                      ("PICK wrong" if isp else ("GT" if isg else "")))
                ax.text(q["x0"] + 3, max(q["y0"] - 6, 14),
                        f"#{i} s{q['score']:.2f} {q['area_pct']:.2f}%" + (f"  {tg}" if tg else ""),
                        color=((1, .12, .12) if isp else ((0, .95, .25) if isg else base)),
                        fontsize=10 if tg else 8, weight="bold",
                        bbox=dict(fc="black", alpha=.65, pad=1.0, ec="none"))
            if c == tgt_c and len(guv):
                ax.scatter(guv[:, 0], guv[:, 1], s=20, c="black", zorder=6)
                ax.scatter(guv[:, 0], guv[:, 1], s=7, c="#00ff00", zorder=7)
            ax.set_title(f"{c}  ({m['roles'].get(c,'')})  {len(m['candidates'].get(c,[]))} cands",
                         fontsize=12)
            ax.axis("off")
        fig.suptitle(f'{k}   "{m["text"]}"\n'
                     f'CoT pick = {pick}   GT is in {gt_ids}   -> '
                     f'{"CORRECT" if ok else ("WRONG (disambiguation)" if gt_ids else "WRONG (answer not in pool)")}'
                     f'    |   RED = my pick   GREEN = the answer   green dots = GT projected',
                     fontsize=13)
        fig.tight_layout()
        fig.savefig(os.path.join(sdir, f"{k}.png"), dpi=80, bbox_inches="tight")
        plt.close(fig)

    if not R:
        print("[!] no answered questions in this batch"); return
    # Questions with disputed ground truth are excluded from the denominator, flagged in
    # answer.json as an `excluded` field carrying the reason.
    EX = [r for r in R if r["excluded"]]
    R = [r for r in R if not r["excluded"]]
    if EX:
        print(f"\n  [excluded {len(EX)}: disputed ground truth]")
        for r in EX:
            print(f"    {r['q']}  -- {r['excl_why']}")
    if not R:
        print("[!] everything was excluded"); return
    n = len(R); ok = sum(r["correct"] for r in R); pl = sum(r["pool_ok"] for r in R)
    ov = [r for r in R if r.get("overridden")]
    # Question defects: unanswerable (the visual information cannot resolve it),
    # ambiguous_task (the reference is not unique), ambiguous_gt (the wording admits several
    # readings and the ground truth annotates only one). **These still count in the
    # denominator by default** -- the official evaluation does not excuse a bad question, so
    # neither do we when reporting official numbers. They are broken out only for internal
    # attribution.
    fl = [r for r in R if r.get("flaw") and not r["correct"]]
    dis = [r for r in R if r["pool_ok"] and not r["correct"]]
    print(f"\n{'='*80}\n### {args.batch}   {n} questions")
    print(f"  correct             {ok:>3}  {100*ok/n:>5.1f}%"
          + (f"   (including {len(ov)} scored by centre distance; "
             f"strict scoring {ok-len(ov)} = {100*(ok-len(ov))/n:.1f}%)" if ov else ""))
    for r in ov:
        print(f"      ^ {r['q'][:4]} {r['proj_why']}")
    if fl:
        import collections as _c
        cc = _c.Counter(r["flaw"] for r in fl)
        print(f"  {len(fl)} of the failures are **defects in the question itself** "
              f"({', '.join(f'{k} {v}' for k, v in cc.items())}):")
        for r in fl:
            print(f"      x {r['q'][:4]} [{r['flaw']}] {r['flaw_why'][:60]}...")
        print(f"  -> excluding question defects: {ok + len(fl)}/{n} = {100*(ok+len(fl))/n:.1f}%"
              f"   (**internal attribution only; never reported externally**)")
    print(f"  answer present in pool (ceiling)  {pl:>3}  {100*pl/n:>5.1f}%")
    print(f"  **disambiguation errors** (in pool, picked wrong) {len(dis):>3}  "
          f"{100*len(dis)/n:>5.1f}%   <- attributable to the reasoning stage")
    print(f"  answer absent from pool           {n-pl:>3}  {100*(n-pl)/n:>5.1f}%   "
          f"<- lost at candidate generation")
    # ⚠️ This used to print a "2D precision" and a "pred/GT area ratio". **Both were
    #    removed.** The ground truth here is a set of **sparse projected pixels** (a few
    #    hundred) while the prediction is a **dense mask** (tens of thousands); using the
    #    former as numerator and the latter as denominator drives the ratio toward zero
    #    regardless of how tightly the object was outlined. The official AP50 is computed on
    #    the 3D point cloud, where both sides are points at the same sampling density, and
    #    there is no 2D equivalent. Real precision comes from the lift stage; until then, do
    #    not use any 2D proxy to guess AP50.
    import collections
    print(f"\n  by criterion type:")
    for kd in sorted({r["kind"] for r in R if r["kind"]}):
        g = [r for r in R if r["kind"] == kd]
        print(f"    {kd:<20}{sum(r['correct'] for r in g):>3}/{len(g):<3} "
              f"{100*sum(r['correct'] for r in g)/len(g):>5.0f}%")
    print(f"\n  by self-reported confidence:")
    for cf in ["high", "low", "forced"]:
        g = [r for r in R if r["conf"] == cf]
        if g:
            print(f"    {cf:<20}{sum(r['correct'] for r in g):>3}/{len(g):<3} "
                  f"{100*sum(r['correct'] for r in g)/len(g):>5.0f}%")
    if dis:
        print(f"\n  disambiguation errors, one by one (the most worthwhile to review):")
        for r in dis:
            print(f"    {r['q']}  picked {r['pick']} should be {r['gt_ids']}  "
                  f"({r['kind']}, {r['conf']})")
            print(f"        \"{r['text'][:66]}\"")
    # ---- sort the figures into _correct / _wrong by result (symlinks, not copies) ----
    if not args.noviz:
        for dd in (cdir, wdir):
            if os.path.isdir(dd):                      # idempotent: clear stale links first
                for x in glob.glob(os.path.join(dd, "*.png")):
                    os.unlink(x)
            os.makedirs(dd, exist_ok=True)
        n_c = n_w = 0
        for r in R:
            src = os.path.join(sdir, f"{r['q']}.png")
            if not os.path.exists(src):
                continue
            dd = cdir if r["correct"] else wdir
            dst = os.path.join(dd, f"{r['q']}.png")
            if not os.path.lexists(dst):
                os.symlink(os.path.relpath(src, dd), dst)
            n_c += r["correct"]; n_w += (not r["correct"])
        print(f"\n  figures sorted: _correct/ {n_c} - _wrong/ {n_w} (symlinks -> _scored/)")
    json.dump(R, open(os.path.join(sdir, "score.json"), "w"), indent=1, ensure_ascii=False)
    print(f"\nfigures -> {sdir}/<q>.png    detail -> {sdir}/score.json")


if __name__ == "__main__":
    main()
