#!/usr/bin/env python3
"""Lift the selected 2D mask into 3D and compute AP50 / AR50 under the **official protocol**.

## Why this step is necessary

The reasoning stage's answers are statements about *which 2D candidate was selected*, while
the baseline's published number is an **AP50 on the 3D point cloud**. The two are not
comparable at all. This script is what converts our results into the official quantity.

## The official protocol (SceneFun3D)

    precision = |GT & pred| / |pred|      recall = |GT & pred| / |GT|      (both in 3D)
    AP50 = frac(precision >= 0.5)         AR50 = frac(recall >= 0.5)

Note that **AP only looks at precision**, so prefer fewer over more. One extra artefact --
a mirror reflection, say -- does not affect whether the target was hit, but it directly
lowers precision.

## How the single-frame lift works

Project the point cloud into the selected frame, resolve visibility against depth, and take
the points landing inside the predicted mask as the 3D prediction:

    u, v, visible = project(xyz, K, pose, depth, vis_thres)
    pred_3d       = visible AND pred_mask_2d[v, u]

The difference from the baseline is that it accumulates 50 frames unconditionally before
thresholding, whereas this uses **one frame**. These numbers are therefore the single-frame
lift; multi-frame aggregation is a separate script.

## Four arms sharing one lift, differing only in the 2D selection

    cot        the reasoning stage's answer                                  <- main result
    geom       the hard-coded geometric solution stored in meta.json         <- control arm
    oracle     **a full lift per candidate, keeping the highest 3D precision** <- AP50 bound
    oracle_r   the same but keeping the highest recall                        <- AR50 bound

The oracle arm is the important one: it answers "what score is available if disambiguation
were perfect".

⚠️ **The first oracle implementation was wrong.** Recorded here so the mistake is not
   repeated:

     old: r = |GT_projected & candidate| / |GT_projected|, maximised, one candidate only

   Two errors. (1) That is **recall**-oriented while AP50 measures precision; the candidate
   covering the most ground truth is usually the largest mask, which has the worst
   precision, so it systematically picked the option most harmful to AP50. (2) It could
   select only one candidate while the reasoning arm may select several, so the "upper
   bound" had an AR50 of 40.3 against the reasoning arm's 51.9 -- and an upper bound below
   the thing it bounds is conclusive proof of a broken definition.

   The old version returned oracle AP50 = cot AP50 = 29.9, which led to the incorrect
   conclusion that disambiguation was already saturated. The corrected version returns 21.3,
   which reverses that conclusion.

    python code/task2/s4_lift/lift.py
    python code/task2/s4_lift/lift.py --vis_thres 0.05,0.10   # sweep visibility tolerance
"""
import os, sys, json, glob, argparse, collections
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import FUN3DU, FUN3DU_DATA, LIFT, SOLVED  # noqa: E402
sys.path.insert(0, FUN3DU); os.chdir(FUN3DU)
from run_lifting import get_visit_stuff                            # noqa: E402
from utils import io                                               # noqa: E402
from utils.sun3d.data_parser import DataParser                     # noqa: E402

OUT = LIFT


def project(xyz, K, c2w, depth, W, H, vis_thres):
    """Point cloud -> frame. Returns (indices of visible points, their u, their v).

    **Independent of any mask, so it is computed once per frame.** Splitting it out is what
    lets the oracle enumerate every candidate without re-projecting the whole cloud each
    time: projecting is O(1M points) while testing a mask is O(visible points), an order of
    magnitude apart.

    ``vis_thres`` is a **relative** tolerance: |z_proj - depth| <= vis_thres * z_proj.
    0.02 allows 2 cm of error at 1 m. Too small a value starts classifying points on the
    front face of a handle as occluded.
    """
    w2c = np.linalg.inv(np.asarray(c2w, float))
    pc = (w2c[:3, :3] @ xyz.T).T + w2c[:3, 3]
    z = pc[:, 2]
    K = np.asarray(K, float)
    u = K[0, 0] * pc[:, 0] / z + K[0, 2]
    v = K[1, 1] * pc[:, 1] / z + K[1, 2]
    ok = (z > 1e-6) & (u >= 0) & (u < W) & (v >= 0) & (v < H)
    if not ok.any():
        return np.array([], np.int64), np.array([], np.int64), np.array([], np.int64)
    ui = np.clip(u[ok].astype(np.int64), 0, W - 1)
    vi = np.clip(v[ok].astype(np.int64), 0, H - 1)
    # Depth is usually lower resolution than RGB; sample proportionally
    dh, dw = depth.shape
    du = np.clip((ui * dw / W).astype(np.int64), 0, dw - 1)
    dv = np.clip((vi * dh / H).astype(np.int64), 0, dh - 1)
    dz = depth[dv, du]
    vis = (dz > 0) & (np.abs(z[ok] - dz) <= vis_thres * z[ok])
    return np.where(ok)[0][vis], ui[vis], vi[vis]


def lift(xyz_n, idx, ui, vi, mask2d):
    """Apply a 2D mask to one projection result, giving the 3D prediction as a bool array."""
    out = np.zeros(xyz_n, bool)
    if len(idx):
        out[idx[mask2d[vi, ui]]] = True
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=FUN3DU_DATA)
    ap.add_argument("--split", default="val")
    ap.add_argument("--batches", default="", help="comma separated; default is every batch*")
    ap.add_argument("--vis_thres", default="0.02")
    ap.add_argument("--arms", default="cot,geom,oracle,oracle_r")
    # 445 questions means reading 30 laser scans and projecting each one: half an hour at
    # minimum. Losing that to a crash is expensive, so every question appends a jsonl line
    # as soon as it is done and a restart skips what is already there. Delete the .jsonl to
    # force a full recomputation.
    ap.add_argument("--resume", type=int, default=1)
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    bs = ([b.strip() for b in args.batches.split(",") if b.strip()]
          or sorted(os.path.basename(x) for x in glob.glob(os.path.join(SOLVED, "batch*"))))
    qs = [d for b in bs for d in sorted(glob.glob(os.path.join(SOLVED, b, "q*_*")))
          if os.path.exists(os.path.join(d, "answer.json"))]
    print(f"[lift] {len(qs)} questions  batches={bs}")

    parser = DataParser(args.root, args.split)
    v2v = io.get_visit_to_videos(args.root, args.split)
    VT = [float(x) for x in args.vis_thres.split(",")]
    arms = [a.strip() for a in args.arms.split(",")]
    ckpt = os.path.join(OUT, "lift_partial.jsonl")
    done = {}
    if args.resume and os.path.exists(ckpt):
        for line in open(ckpt):
            try:
                r = json.loads(line)
                done[r["q"]] = r
            except Exception:
                pass
        print(f"[resume] {len(done)} questions already computed, skipping")
    fh = open(ckpt, "a")
    cur_v, xyz, vs = None, None, None
    R = []
    for d in qs:
        k = os.path.basename(d)
        if k in done:
            R.append(done[k]); continue
        m = json.load(open(os.path.join(d, "meta.json")))
        a = json.load(open(os.path.join(d, "answer.json")))
        v, did = m["visit"], m["desc_id"]
        tgt = m["parse"]["target"]["concept"]
        vid, fid = m["frame"]["video"], m["frame"]["fid"]
        W, H = m["frame"]["W"], m["frame"]["H"]
        if v != cur_v:
            pc = parser.get_laser_scan(v); pc = parser.get_cropped_laser_scan(v, pc)
            xyz = np.asarray(pc.points); vs = get_visit_stuff(parser, v, v2v[v]); cur_v = v
            print(f"  -- visit {v}", flush=True)
        gt = np.asarray(parser.get_grouped_annotation(v, did)).astype(bool)
        K = parser.read_camera_intrinsics(vs[vid]["intrinsics"][fid], format="matrix")
        po = parser.get_nearest_pose(fid, vs[vid]["poses"])
        depth = parser.read_depth_frame(vs[vid]["depth_paths"][fid])
        z = np.load(os.path.join(d, "cands.npz"))
        keys = m["mask_keys"].get(tgt, [])

        def mask_of(ids):
            mm = np.zeros((H, W), bool)
            for i in ids:
                kk = f"{tgt}|{i}"
                if kk in z:
                    f = np.asarray(z[kk], np.int64)
                    mm[f // W, f % W] = True
            return mm

        # ---- oracle: run a full lift for **every candidate**, then take the best by 3D
        #      precision and, separately, by 3D recall.
        #      This is what "how much is available if 2D selection were perfect" means.
        #      The earlier version selected by GT-projection coverage and allowed only one
        #      candidate -- recall-oriented, and it understated AP50. See the file header.
        orc = {}
        if ("oracle" in arms or "oracle_r" in arms) and len(keys):
            ngt = max(int(gt.sum()), 1)
            for vt in VT:
                idx_, ui_, vi_ = project(xyz, K, po, depth, W, H, vt)
                bp = (-1.0, None); br = (-1.0, None)
                for i in range(len(keys)):
                    p3 = lift(len(xyz), idx_, ui_, vi_, mask_of([i]))
                    npd = int(p3.sum())
                    if npd == 0:
                        continue
                    inter = int((p3 & gt).sum())
                    pr, rc = inter / npd, inter / ngt
                    if pr > bp[0]:
                        bp = (pr, i)
                    if rc > br[0]:
                        br = (rc, i)
                orc[("oracle", vt)] = [bp[1]] if bp[1] is not None else []
                orc[("oracle_r", vt)] = [br[1]] if br[1] is not None else []

        picks = dict(cot=a.get("final", []),
                     geom=m.get("geom_pick", {}).get("target", []))
        row = dict(q=k, batch=os.path.basename(os.path.dirname(d)), visit=v, desc=did,
                   text=m["text"], concept=tgt, n_gt=int(gt.sum()),
                   conf=a.get("confidence"), excluded=bool(a.get("excluded")))
        for arm in arms:
            for vt in VT:
                # Oracle arms depend on vis_thres -- the best candidate can differ per
                # tolerance -- so the selection is looked up inside this loop.
                ids = orc.get((arm, vt), []) if arm.startswith("oracle") else (picks.get(arm) or [])
                if not ids:
                    row[f"{arm}@{vt}"] = dict(n_pred=0, prec=0.0, rec=0.0, pick=list(ids))
                    continue
                idx_, ui_, vi_ = project(xyz, K, po, depth, W, H, vt)
                p3 = lift(len(xyz), idx_, ui_, vi_, mask_of(ids))
                inter = int((p3 & gt).sum()); npd = int(p3.sum())
                row[f"{arm}@{vt}"] = dict(n_pred=npd,
                                          prec=inter / max(npd, 1),
                                          rec=inter / max(int(gt.sum()), 1), pick=list(ids))
        R.append(row)
        fh.write(json.dumps(row, ensure_ascii=False) + "\n"); fh.flush()
        c = row.get(f"cot@{VT[0]}", {})
        print(f"  {k:<28} |pred|={c.get('n_pred',0):>6} /{row['n_gt']:<5} "
              f"prec={c.get('prec',0):.3f} rec={c.get('rec',0):.3f}", flush=True)

    if not R:
        print("[!] nothing to compute"); return
    keep = [r for r in R if not r["excluded"]]
    print(f"\n{'='*88}\n### Official protocol  {len(keep)} questions "
          f"({len(R)-len(keep)} excluded for disputed ground truth)")
    for vt in VT:
        print(f"\n  vis_thres = {vt}")
        print(f"    {'arm':<18}{'AP50':>7}{'AR50':>7}{'AP25':>7}{'medPrec':>10}"
              f"{'medRec':>9}{'med|pred|':>11}{'|pred|/|GT|':>13}")
        for arm in arms:
            lbl = {"oracle": "oracle (AP bound)", "oracle_r": "oracle_r (AR bound)"}.get(arm, arm)
            P = np.array([r[f"{arm}@{vt}"]["prec"] for r in keep])
            Rc = np.array([r[f"{arm}@{vt}"]["rec"] for r in keep])
            N = np.array([r[f"{arm}@{vt}"]["n_pred"] for r in keep], float)
            G = np.array([r["n_gt"] for r in keep], float)
            print(f"    {lbl:<18}{100*(P>=.5).mean():>7.1f}{100*(Rc>=.5).mean():>7.1f}"
                  f"{100*(P>=.25).mean():>7.1f}{np.median(P):>10.3f}{np.median(Rc):>9.3f}"
                  f"{np.median(N):>11.0f}{np.median(N/np.maximum(G,1)):>13.2f}")
    vt0 = VT[0]
    print(f"\n  Published comparisons (official protocol, full val):"
          f"\n        Fun3DU (self-reported)  AP50 16.90 / AP25 33.30;"
          f"\n        Fun3DU reproduced here, with our fallback and scorer, 16.85 / 28.99;"
          f"\n        AffordMEM 20.13 / 41.66;  UniFunc3D-8B 23.82 / 44.04.")
    if len(keep) >= 400:
        print(f"        This run covers the **full val set, {len(keep)} instructions** "
              f"(445 minus the disputed ones),"
              f"\n        unfiltered, and is therefore directly comparable with the above.")
        print(f"        Note: this is a **single-frame** lift with no refinement (no connected"
              f"\n        components, no radius crop, no multi-frame voting), whereas the "
              f"baseline's 16.9\n        accumulates 50 frames before thresholding. That "
              f"comparison is against us here.")
    else:
        print(f"        ⚠️ Only {len(keep)} instructions -- **not the full val set**. "
              f"Not comparable with the above.")
    if "oracle" in arms:
        same = [r for r in keep if sorted(r[f"cot@{vt0}"]["pick"]) ==
                sorted(r[f"oracle@{vt0}"]["pick"])]
        print(f"\n  questions where the reasoning matched the oracle: {len(same)}/{len(keep)} "
              f"= {100*len(same)/len(keep):.1f}%   <- the direct measure of remaining "
              f"disambiguation headroom")
    print(f"\n  by reasoning confidence (cot arm, vis_thres={vt0}):")
    for cf in ["high", "medium", "low", "forced"]:
        g = [r for r in keep if r["conf"] == cf]
        if g:
            P = np.array([r[f"cot@{vt0}"]["prec"] for r in g])
            print(f"    {cf:<8}{len(g):>3} q   AP50 {100*(P>=.5).mean():>5.1f}"
                  f"   median prec {np.median(P):.3f}")
    json.dump(R, open(os.path.join(OUT, "lift.json"), "w"), indent=1, ensure_ascii=False)
    print(f"\ndetail -> {OUT}/lift.json")


if __name__ == "__main__":
    main()
