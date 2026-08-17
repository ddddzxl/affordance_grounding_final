#!/usr/bin/env python3
"""Sweep every refinement available once the instance has already been selected.

## Why this exists

Full-val official score: AP50 **19.5**, against a 2D selection accuracy of **58.6%** -- a
conversion rate of only 33%. The oracle (perfect 2D selection plus a single-frame lift) is
only 21.3, so **disambiguation is already saturated** and the 37 points that evaporate are
entirely precision loss.

More pointedly: on the 115 high-confidence questions, where 2D selection is almost always
right, AP50 is still 34.8 with a median precision of **0.327**. **Selecting correctly is not
enough to pass 0.5.** So this is not about rescuing the questions that were answered wrongly;
it is about pushing the already-correct ones from 0.327 past 0.5, which benefits all 442.

## What is swept -- all of it after instance selection

Nothing here re-runs the segmenter, regenerates candidates, or invokes the reasoning stage.

### 2D side, before the lift

    E   erode the mask by k pixels. The segmenter's mask edge is not clean, and projection
        drags background points in with it. Shrinking inward removes exactly the ring most
        likely to bleed through.

### 3D side, after the lift

    C1  largest connected component   KD-tree radius connectivity, keep the biggest blob
                                      -> targets bleeding into a neighbouring object
    C2  depth front layer             keep only the frontmost layer in camera-frame z
                                      -> targets bleeding through to the back surface
                                         (the handle is in front, the cabinet face behind)
    C3  physical radius crop          keep points within r metres of the medoid
                                      -> targets spreading too wide overall

These combine freely; the script sweeps the Cartesian product of (erosion x 3D combination)
and reports official AP50 / AR50 for each.

## Implementation notes

- **The projection is computed once.** project() does not depend on the mask, so it runs once
  per question; different erosion radii and post-processing are lookups and filters over that
  result, making 20+ combinations nearly free.
- **C3 deliberately uses a physical radius rather than "keep the nearest N points".** Any N
  would have to come either from the ground-truth point count (reading the answer) or from a
  prior table keyed by affordance class -- and affordance is also a ground-truth attribute.
  A radius is pure geometry and leaks nothing.
- Supports --resume, appending one jsonl record per question.

    python code/task2/s4_lift/refine_sweep.py --limit 8        # smoke test
"""
import os, sys, json, glob, argparse, itertools
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import FUN3DU, FUN3DU_DATA, PROJECT_ROOT, TASK2  # noqa: E402
sys.path.insert(0, FUN3DU); os.chdir(FUN3DU)
from run_lifting import get_visit_stuff                            # noqa: E402
from utils import io                                               # noqa: E402
from utils.sun3d.data_parser import DataParser                     # noqa: E402

BASE = TASK2
SOLVED = os.path.join(BASE, "cot_records")
OUT = os.path.join(BASE, "per_question")


def project(xyz, K, c2w, depth, W, H, vis_thres):
    """Point cloud -> frame. Returns (visible indices, pixel u, pixel v, camera-frame z).

    **Independent of any mask, so it is computed once per question** -- which is what makes
    sweeping 20+ refinement combinations nearly free.
    """
    w2c = np.linalg.inv(np.asarray(c2w, float))
    pc = (w2c[:3, :3] @ xyz.T).T + w2c[:3, 3]
    z = pc[:, 2]
    K = np.asarray(K, float)
    u = K[0, 0] * pc[:, 0] / z + K[0, 2]
    v = K[1, 1] * pc[:, 1] / z + K[1, 2]
    ok = (z > 1e-6) & (u >= 0) & (u < W) & (v >= 0) & (v < H)
    if not ok.any():
        e = np.array([], np.int64)
        return e, e, e, np.array([])
    ui = np.clip(u[ok].astype(np.int64), 0, W - 1)
    vi = np.clip(v[ok].astype(np.int64), 0, H - 1)
    dh, dw = depth.shape
    du = np.clip((ui * dw / W).astype(np.int64), 0, dw - 1)
    dv = np.clip((vi * dh / H).astype(np.int64), 0, dh - 1)
    dz = depth[dv, du]
    vis = (dz > 0) & (np.abs(z[ok] - dz) <= vis_thres * z[ok])
    idx = np.where(ok)[0][vis]
    return idx, ui[vis], vi[vis], z[ok][vis]


def erode(mask, k):
    """Erode a binary mask inward by k pixels. k=0 returns it unchanged."""
    if k <= 0:
        return mask
    from scipy.ndimage import binary_erosion
    st = np.ones((2 * k + 1, 2 * k + 1), bool)
    out = binary_erosion(mask, structure=st, border_value=0)
    # If erosion consumed the mask entirely, fall back to the original rather than
    # throwing the question away for nothing.
    return out if out.any() else mask


def biggest_cluster(P, eps=0.03, min_n=5):
    """Radius-graph connected components via a KD-tree; returns a mask for the largest.

    Equivalent to finding connected components of the graph joining points closer than eps.
    """
    from scipy.spatial import cKDTree
    n = len(P)
    if n < min_n:
        return np.ones(n, bool)
    t = cKDTree(P)
    pairs = t.query_pairs(eps, output_type="ndarray")
    par = np.arange(n)

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            par[ra] = rb
    root = np.array([find(i) for i in range(n)])
    lab, cnt = np.unique(root, return_counts=True)
    return root == lab[np.argmax(cnt)]


def front_layer(zc, band=0.05):
    """Keep only the frontmost layer in camera-frame z: z <= median(z) + band metres.

    Bleed-through shows up as a bimodal z distribution -- one peak at the handle, one at the
    door panel behind it -- and this cuts off the far peak.

    The band is an absolute distance in metres because handle thickness is a fixed physical
    quantity and does not scale with viewing distance.

    ⚠️ The median must be taken over **the target point set** passed in here. Taking it over
    all visible points in the scene (the depth median of the whole room) shreds points inside
    the mask: the single-frame baseline drops from 28.7 to 21.5.
    """
    if len(zc) == 0:
        return np.zeros(0, bool)
    return zc <= np.percentile(zc, 50) + band


def keep_radius(P, r):
    """Keep points within r metres of the medoid (approximated by the coordinate-wise
    median, which is robust to outliers)."""
    if len(P) == 0:
        return np.zeros(0, bool)
    return np.linalg.norm(P - np.median(P, axis=0), axis=1) <= r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=FUN3DU_DATA)
    ap.add_argument("--split", default="val")
    ap.add_argument("--vis_thres", type=float, default=0.02)
    ap.add_argument("--erode", default="0,1,2,3,5", help="2D erosion radius in pixels")
    ap.add_argument("--eps", type=float, default=0.03, help="C1 connectivity radius in metres")
    ap.add_argument("--band", type=float, default=0.05, help="C2 front-layer thickness in metres")
    ap.add_argument("--radius", default="0.15", help="C3 radius in metres")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--resume", type=int, default=1)
    ap.add_argument("--answers", default="",
                    help="override answer.json with the `final` field from another jsonl "
                         "(one record per line, with q and final), and run **only the "
                         "questions present in that file** -- used for the reasoning ablation")
    ap.add_argument("--tag", default="",
                    help="checkpoint filename suffix. Changing arm without changing tag "
                         "would resume from the previous arm's checkpoint")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    EK = [int(x) for x in args.erode.split(",")]
    RR = [float(x) for x in args.radius.split(",")]
    # 3D combinations: name -> (use C1, use C2, C3 radius or None)
    C3D = [("none", (0, 0, None)), ("C1", (1, 0, None)), ("C2", (0, 1, None)),
           ("C1+C2", (1, 1, None))]
    for r in RR:
        C3D += [(f"C3r{r}", (0, 0, r)), (f"C1+C2+C3r{r}", (1, 1, r))]
    COMBOS = [(e, cn) for e in EK for cn, _ in C3D]
    cfg = {cn: c for cn, c in C3D}

    # ---- optional: take answers from an external jsonl (the open-model arm) ----
    ALT = None
    if args.answers:
        ALT = {}
        # ⚠️ This script does os.chdir(FUN3DU) at import time (see the file header), so cwd
        #    is **not** the project root. Relative paths must be rejoined to the project root
        #    explicitly, or the glob silently returns nothing and the run covers 0 questions.
        pat = (args.answers if os.path.isabs(args.answers)
               else os.path.join(PROJECT_ROOT, args.answers))
        for f in sorted(glob.glob(pat)):
            for line in open(f):
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("final") is not None:
                    ALT[r["q"]] = r["final"]        # on duplicates, the last record wins
        print(f"[answers] {len(ALT)} external answers <- {pat}")
        if not ALT:
            sys.exit("[abort] external answers are empty -- check the path "
                     "(remember cwd has been chdir'd into the baseline repo)")

    ckpt = os.path.join(OUT, f"refine_partial{args.tag}.jsonl")
    done = {}
    if args.resume and os.path.exists(ckpt):
        for line in open(ckpt):
            try:
                r = json.loads(line); done[r["q"]] = r
            except Exception:
                pass
        print(f"[resume] {len(done)} questions already computed")
    fh = open(ckpt, "a")

    qs = [d for d in sorted(glob.glob(os.path.join(SOLVED, "batch*", "q*_*")))
          if os.path.exists(os.path.join(d, "answer.json"))]
    if ALT is not None:
        qs = [d for d in qs if os.path.basename(d) in ALT]
    parser = DataParser(args.root, args.split)
    v2v = io.get_visit_to_videos(args.root, args.split)
    cur_v, xyz, vs = None, None, None
    R = []
    print(f"[refine] {len(qs)} questions  erode={EK}  3D={[c for c,_ in C3D]}  "
          f"{len(COMBOS)} combinations")
    for d in qs:
        k = os.path.basename(d)
        if k in done:
            R.append(done[k]); continue
        a = json.load(open(os.path.join(d, "answer.json")))
        if a.get("excluded"):
            continue
        ids = a.get("final") or []
        if ALT is not None:
            ids = ALT[k]                            # external arm: replace the answer wholesale
        m = json.load(open(os.path.join(d, "meta.json")))
        v, did = m["visit"], m["desc_id"]
        vid, fid = m["frame"]["video"], m["frame"]["fid"]
        W, H = m["frame"]["W"], m["frame"]["H"]
        tgt = m["parse"]["target"]["concept"]
        if v != cur_v:
            pc = parser.get_laser_scan(v); pc = parser.get_cropped_laser_scan(v, pc)
            xyz = np.asarray(pc.points); vs = get_visit_stuff(parser, v, v2v[v]); cur_v = v
            print(f"  -- visit {v}", flush=True)
        gt = np.asarray(parser.get_grouped_annotation(v, did)).astype(bool)
        ngt = max(int(gt.sum()), 1)
        row = dict(q=k, n_gt=int(gt.sum()), conf=a.get("confidence"))
        if not ids:
            for e, cn in COMBOS:
                row[f"e{e}|{cn}"] = dict(n=0, prec=0.0, rec=0.0)
            R.append(row); fh.write(json.dumps(row) + "\n"); fh.flush(); continue

        K = parser.read_camera_intrinsics(vs[vid]["intrinsics"][fid], format="matrix")
        po = parser.get_nearest_pose(fid, vs[vid]["poses"])
        depth = parser.read_depth_frame(vs[vid]["depth_paths"][fid])
        z = np.load(os.path.join(d, "cands.npz"))
        base = np.zeros((H, W), bool)
        for i in ids:
            kk = f"{tgt}|{i}"
            if kk in z:
                f = np.asarray(z[kk], np.int64)
                base[f // W, f % W] = True
        idx, ui, vi, zc = project(xyz, K, po, depth, W, H, args.vis_thres)

        for e in EK:
            mk = erode(base, e)
            hit = mk[vi, ui] if len(idx) else np.zeros(0, bool)
            ii = idx[hit]; zz = zc[hit] if len(idx) else np.zeros(0)
            P = xyz[ii]
            k1 = biggest_cluster(P, args.eps) if len(P) else np.zeros(0, bool)
            k2 = front_layer(zz, args.band) if len(P) else np.zeros(0, bool)
            for cn, (u1, u2, r3) in C3D:
                keep = np.ones(len(P), bool)
                if u1:
                    keep &= k1
                if u2:
                    keep &= k2
                if r3 is not None and keep.any():
                    sub = np.where(keep)[0]
                    k3 = np.zeros(len(P), bool)
                    k3[sub[keep_radius(P[keep], r3)]] = True
                    keep = k3
                s = np.zeros(len(xyz), bool); s[ii[keep]] = True
                n = int(keep.sum()); inter = int((s & gt).sum())
                row[f"e{e}|{cn}"] = dict(n=n, prec=inter / max(n, 1), rec=inter / ngt)
        R.append(row); fh.write(json.dumps(row) + "\n"); fh.flush()
        # Progress line: compare the **first** and **last** combination of this sweep.
        # Must not hard-code e0 -- a sweep that does not include erosion 0 would then
        # silently report against a key that does not exist.
        b = row[f"e{EK[0]}|{COMBOS[0][1]}"]; g = row[f"e{EK[-1]}|{COMBOS[-1][1]}"]
        print(f"  {k:<28} raw n={b['n']:>5} prec={b['prec']:.3f} -> "
              f"best combo n={g['n']:>5} prec={g['prec']:.3f}", flush=True)
        if args.limit and len(R) >= args.limit:
            break

    if not R:
        print("[!] no data"); return
    n = len(R)
    print(f"\n{'='*96}\n### Refinement sweep  ({n} questions, official protocol)\n")
    print(f"  {'erode':<7}{'3D post-processing':<20}{'AP50':>7}{'AR50':>7}{'AP25':>7}"
          f"{'medPrec':>10}{'medRec':>9}{'med|pred|':>11}")
    best = None
    for e, cn in COMBOS:
        key = f"e{e}|{cn}"
        P = np.array([r[key]["prec"] for r in R])
        Rc = np.array([r[key]["rec"] for r in R])
        N = np.array([r[key]["n"] for r in R], float)
        ap = 100 * (P >= .5).mean()
        print(f"  {e:<6}{cn:<16}{ap:>7.1f}{100*(Rc>=.5).mean():>7.1f}"
              f"{100*(P>=.25).mean():>7.1f}{np.median(P):>10.3f}{np.median(Rc):>9.3f}"
              f"{np.median(N):>11.0f}")
        if best is None or ap > best[0]:
            best = (ap, e, cn)
    bkey = f"e{EK[0]}|none"
    b0 = 100 * (np.array([r[bkey]["prec"] for r in R]) >= .5).mean()
    tag = "no refinement" if EK[0] == 0 else f"erode {EK[0]}px + none"
    print(f"\n  baseline for this run ({tag}) AP50 {b0:.1f}  ->  best {best[0]:.1f}  "
          f"(erode {best[1]}px + {best[2]})   **{best[0]-b0:+.1f}**")
    if EK[0] != 0:
        print(f"  ⚠️ erosion 0 was not swept, so the delta above is relative to {tag}, not to")
        print(f"     the raw lift. The raw figure (erode 0 + none) is AP50 19.5.")
    print(f"\n  gain of the best combination, by reasoning confidence:")
    for c in ("high", "medium", "low", "forced"):
        g = [r for r in R if r["conf"] == c]
        if not g:
            continue
        p0 = np.array([r[bkey]["prec"] for r in g])
        p1 = np.array([r[f"e{best[1]}|{best[2]}"]["prec"] for r in g])
        print(f"    {c:<8}{len(g):>4} q   AP50 {100*(p0>=.5).mean():>5.1f} -> "
              f"{100*(p1>=.5).mean():>5.1f}   median prec {np.median(p0):.3f} -> {np.median(p1):.3f}")
    fo = os.path.join(OUT, "refine.json")
    json.dump(R, open(fo, "w"), indent=1, ensure_ascii=False)
    print(f"\ndetail -> {fo}")


if __name__ == "__main__":
    main()
