#!/usr/bin/env python3
"""Multi-frame aggregation: use parallax to vote away bleed-through points.

## This solves a different problem from refinement

    refinement (erode + C2)   removes points that *look* suspicious -- the edge ring, the
                              far depth peak. Prior-based, decided within a single frame.
    multi-frame               uses **parallax** to confirm which points are still inside the
                              mask from another viewpoint. Evidence-based, and unobtainable
                              from a single frame in principle.

Genuine handle points hit the mask from viewpoint after viewpoint; a door-panel point that
bled through falls outside it after two or three degrees of rotation.

## The key property: the reasoning stage is never re-run

Instance **identity** is carried across frames by 3D position, not by re-inference:

    1. lift the top-1 frame's answer into a seed point cloud
    2. run the segmenter once per remaining frame, with the same concept
    3. per frame, take the candidate with the largest 3D overlap with the seed
       -- that is the same instance as seen in that frame
    4. accumulate its 3D points, then threshold by **relative peak**

⚠️ The baseline's 0.7 is `np_normalize(acc / n_views) > 0.7` applied **per 3D point**,
   meaning "this point received at least 70% of the scene-wide peak vote". It is **not**
   "hit in 70% of the frames". This follows that convention exactly, and sweeps the
   threshold.

## Where the frames come from

`framesel.topk` in meta.json -- the top-8 that already passed the hard conditions, which is
both better quality than global sampling and **already computed**, so the baseline's context
scoring need not be re-run. Frame 0 is the frame already in use, whose masks are cached in
cands.npz, so it is not re-segmented.

## Cost

445 questions x at most 7 new frames each, deduplicated by (visit, video, frame, concept),
gives roughly 2000-2500 segmenter calls: about 15 minutes on one GPU, 4 on four. Sharding is
by visit, since both the segmentation cache and the laser scan are reused per visit.

    python code/task2/s4_lift/multiframe_lift.py --limit 5      # smoke test
"""
import os, sys, json, glob, argparse
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import (CANDIDATES, FUN3DU, FUN3DU_DATA, SCENEFUN3D,       # noqa: E402
                   SEGMENTER_WEIGHTS, TASK2)
PERCEPTION = os.path.join(_CODE_ROOT, "task2", "s1_perception")
sys.path.insert(0, PERCEPTION)
sys.path.insert(0, FUN3DU)
# Import the segmenter wrapper BEFORE chdir'ing into the baseline repo, whose top-level
# `utils` package would otherwise shadow ours. See code/README.md.
from sam3_util import init_sam3, sam3_masks                        # noqa: E402
os.chdir(FUN3DU)
from run_lifting import get_visit_stuff                            # noqa: E402
from utils import io                                               # noqa: E402
from utils.sun3d.data_parser import DataParser                     # noqa: E402

BASE = TASK2
SOLVED = os.path.join(BASE, "cot_records")
DATA = SCENEFUN3D
OUT = os.path.join(BASE, "per_question")


def project(xyz, K, c2w, depth, W, H, vis_thres):
    """Point cloud -> frame. Returns (visible indices, pixel u, pixel v, camera-frame z).
    Independent of any mask, so it is computed once per frame."""
    w2c = np.linalg.inv(np.asarray(c2w, float))
    pc = (w2c[:3, :3] @ xyz.T).T + w2c[:3, 3]
    z = pc[:, 2]
    K = np.asarray(K, float)
    u = K[0, 0] * pc[:, 0] / z + K[0, 2]
    v = K[1, 1] * pc[:, 1] / z + K[1, 2]
    ok = (z > 1e-6) & (u >= 0) & (u < W) & (v >= 0) & (v < H)
    if not ok.any():
        e = np.array([], np.int64)
        return e, e, e, np.array([])          # four values, matching the normal branch
    ui = np.clip(u[ok].astype(np.int64), 0, W - 1)
    vi = np.clip(v[ok].astype(np.int64), 0, H - 1)
    dh, dw = depth.shape
    du = np.clip((ui * dw / W).astype(np.int64), 0, dw - 1)
    dv = np.clip((vi * dh / H).astype(np.int64), 0, dh - 1)
    dz = depth[dv, du]
    vis = (dz > 0) & (np.abs(z[ok] - dz) <= vis_thres * z[ok])
    return np.where(ok)[0][vis], ui[vis], vi[vis], z[ok][vis]


def all_frames(visit, stride, data_root):
    """Every (video, frame) pair for this visit, matching candidate generation exactly."""
    import glob as _g
    out = []
    for vid in sorted(d for d in os.listdir(f"{data_root}/{visit}") if d.isdigit()):
        def ids(sub, ext):
            return {os.path.basename(x)[len(vid) + 1:-len(ext)]
                    for x in _g.glob(f"{data_root}/{visit}/{vid}/{sub}/{vid}_*{ext}")}
        for f in sorted(ids("hires_wide", ".jpg") & ids("hires_depth", ".png"),
                        key=float)[::stride]:
            out.append((vid, f))
    return out


def front_layer(zc, band):
    """C2: keep only the frontmost layer in camera-frame z.

    Bleed-through shows up as a bimodal z distribution; this removes the far peak.
    """
    if band <= 0 or len(zc) == 0:
        return np.ones(len(zc), bool)
    return zc <= np.percentile(zc, 50) + band


def erode(mask, k):
    if k <= 0:
        return mask
    from scipy.ndimage import binary_erosion
    out = binary_erosion(mask, structure=np.ones((2 * k + 1, 2 * k + 1), bool), border_value=0)
    return out if out.any() else mask


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=FUN3DU_DATA)
    ap.add_argument("--sam3", default=SEGMENTER_WEIGHTS)
    ap.add_argument("--split", default="val")
    ap.add_argument("--dump", default="candidates")
    ap.add_argument("--vis_thres", type=float, default=0.02)
    ap.add_argument("--erode", type=int, default=5, help="matches the best single-frame config")
    # sam3_masks has signature (predictor, rgb, text, det_th, mask_th, with_scores) -- there
    # is **no nms argument**. NMS is applied by the candidate-generation script itself.
    # It is not needed here: we only take the single candidate with the largest 3D overlap
    # with the seed, so redundant overlapping masks lose that comparison anyway.
    # det_th matches candidate generation (0.15).
    ap.add_argument("--det_th", type=float, default=0.15)
    ap.add_argument("--max_frames", type=int, default=8,
                    help="how many of framesel.topk to use")
    # Frame expansion: topk holds only 8 frames, and after removing those where the segmenter
    # found nothing and those with no seed overlap, the median drops to 3 -- 28% of questions
    # degenerate to single-frame. Rebuilding the baseline's 50-frame pool would mean running
    # the segmenter over all frames for every (visit, concept) pair, roughly 45000 calls and
    # four hours on one GPU, which is not worth it. Multi-frame only needs *different
    # viewpoints of the same instance*, and uniform sampling supplies that: frames that
    # cannot see the target simply detect nothing and cast no vote, which is harmless.
    ap.add_argument("--extra_frames", type=int, default=24,
                    help="additional frames sampled uniformly across the visit")
    ap.add_argument("--stride", type=int, default=10, help="matches candidate generation")
    ap.add_argument("--band", type=float, default=0.05,
                    help="C2 front-layer thickness in metres; <=0 disables")
    ap.add_argument("--ths", default="0.3,0.5,0.7,0.9",
                    help="relative-peak thresholds to sweep")
    # Do NOT set CUDA_VISIBLE_DEVICES. The scheduler has already mapped the allocation onto
    # cuda:0..N-1, so indexing **within** the allocation cannot stray onto anyone else's GPU.
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshard", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--resume", type=int, default=1)
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    THS = [float(x) for x in args.ths.split(",")]
    SRC = CANDIDATES if args.dump == "candidates" else os.path.join(os.path.dirname(CANDIDATES), args.dump)

    qs = [d for d in sorted(glob.glob(os.path.join(SOLVED, "batch*", "q*_*")))
          if os.path.exists(os.path.join(d, "answer.json"))]
    # Shard by visit -- the laser scan and the segmentation cache are both reused per visit,
    # so splitting a visit across shards destroys both.
    byv = {}
    for d in qs:
        m = json.load(open(os.path.join(d, "meta.json")))
        byv.setdefault(m["visit"], []).append(d)
    vlist = sorted(byv)
    mine = [v for i, v in enumerate(vlist) if i % args.nshard == args.shard]
    todo = [d for v in mine for d in byv[v]]
    if args.limit:
        todo = todo[:args.limit]
    print(f"[mf] shard {args.shard}/{args.nshard}: {len(mine)} visits, {len(todo)} questions  "
          f"erode={args.erode}  C2band={args.band}  "
          f"frames=topk{args.max_frames}+uniform{args.extra_frames}  thresholds={THS}", flush=True)

    ckpt = os.path.join(OUT, f"mf_s{args.shard}.jsonl")
    done = set()
    if args.resume and os.path.exists(ckpt):
        for line in open(ckpt):
            try:
                done.add(json.loads(line)["q"])
            except Exception:
                pass
        print(f"[resume] {len(done)} questions already computed")
    fh = open(ckpt, "a")

    from PIL import Image
    parser = DataParser(args.root, args.split)
    v2v = io.get_visit_to_videos(args.root, args.split)
    predictor = init_sam3(args.sam3, device=args.device)
    cur_v, xyz, vs = None, None, None
    cache = {}                    # (vid, fid, concept) -> [mask...], lifetime is one visit

    for d in todo:
        k = os.path.basename(d)
        if k in done:
            continue
        a = json.load(open(os.path.join(d, "answer.json")))
        if a.get("excluded"):
            continue
        ids = a.get("final") or []
        m = json.load(open(os.path.join(d, "meta.json")))
        v, did = m["visit"], m["desc_id"]
        tgt = m["parse"]["target"]["concept"]
        W, H = m["frame"]["W"], m["frame"]["H"]
        topk = [tuple(x) for x in (m.get("framesel", {}).get("topk") or [])[:args.max_frames]]
        if v != cur_v:
            pc = parser.get_laser_scan(v); pc = parser.get_cropped_laser_scan(v, pc)
            xyz = np.asarray(pc.points); vs = get_visit_stuff(parser, v, v2v[v])
            cur_v = v; cache.clear()
            allf = all_frames(v, args.stride, DATA) if args.extra_frames > 0 else []
            if allf and args.extra_frames < len(allf):
                step = max(len(allf) // args.extra_frames, 1)
                extra = allf[::step][:args.extra_frames]
            else:
                extra = allf
            print(f"  -- visit {v}  ({len(byv[v])} questions)", flush=True)
        gt = np.asarray(parser.get_grouped_annotation(v, did)).astype(bool)
        ngt = max(int(gt.sum()), 1)

        # ---- step 1: seed from the top-1 frame's answer.
        #      Its masks are already in cands.npz, so the segmenter is not re-run. ----
        seed = np.zeros(len(xyz), bool)
        if ids:
            z = np.load(os.path.join(d, "cands.npz"))
            base = np.zeros((H, W), bool)
            for i in ids:
                kk = f"{tgt}|{i}"
                if kk in z:
                    f = np.asarray(z[kk], np.int64); base[f // W, f % W] = True
            base = erode(base, args.erode)
            vid0, fid0 = m["frame"]["video"], m["frame"]["fid"]
            K0 = parser.read_camera_intrinsics(vs[vid0]["intrinsics"][fid0], format="matrix")
            po0 = parser.get_nearest_pose(fid0, vs[vid0]["poses"])
            dp0 = parser.read_depth_frame(vs[vid0]["depth_paths"][fid0])
            i0, u0, v0, z0 = project(xyz, K0, po0, dp0, W, H, args.vis_thres)
            if len(i0):
                # ⚠️ front_layer's median must be taken over **the target point set**, not
                #    over all visible points in the scene. The latter is the depth median of
                #    the whole room, which says nothing about whether the handle is in the
                #    front layer and shreds points inside the mask. The first version of this
                #    did exactly that, and the single-frame baseline fell from 28.7 to 21.5.
                m0 = base[v0, u0]
                if args.band > 0 and m0.any():
                    sub = np.where(m0)[0]
                    keep = front_layer(z0[m0], args.band)
                    m0 = np.zeros(len(m0), bool); m0[sub[keep]] = True
                seed[i0[m0]] = True
        if not seed.any():
            row = dict(q=k, n_gt=int(gt.sum()), n_frames=0, seed_n=0,
                       conf=a.get("confidence"))
            for t in THS:
                row[f"th{t}"] = dict(n=0, prec=0.0, rec=0.0)
            row["single"] = dict(n=0, prec=0.0, rec=0.0)
            fh.write(json.dumps(row) + "\n"); fh.flush(); continue

        # ---- steps 2 and 3: other frames -> segment -> take the candidate with the
        #      largest 3D overlap with the seed ----
        acc = np.zeros(len(xyz), np.int32)
        acc[seed] += 1                                # the top-1 frame casts a vote too
        n_used = 1
        cand_frames = list(dict.fromkeys(topk + [f for f in extra if f not in topk]))
        for (vid, fid) in cand_frames:
            if vid == m["frame"]["video"] and fid == m["frame"]["fid"]:
                continue
            if vid not in vs or fid not in vs[vid]["poses"]:
                continue
            ck = (vid, fid, tgt)
            if ck not in cache:
                p = f"{DATA}/{v}/{vid}/hires_wide/{vid}_{fid}.jpg"
                if not os.path.exists(p):
                    cache[ck] = []
                else:
                    rgb = np.asarray(Image.open(p).convert("RGB")).astype(np.uint8)
                    cache[ck] = list(sam3_masks(predictor, rgb, tgt, det_th=args.det_th))
            ms = cache[ck]
            if not ms:
                continue
            try:
                K = parser.read_camera_intrinsics(vs[vid]["intrinsics"][fid], format="matrix")
                po = parser.get_nearest_pose(fid, vs[vid]["poses"])
                dp = parser.read_depth_frame(vs[vid]["depth_paths"][fid])
            except Exception:
                continue
            hh, ww = ms[0].shape[:2]
            ii, uu, vv, zz = project(xyz, K, po, dp, ww, hh, args.vis_thres)
            if not len(ii):
                continue
            # Claim "the same instance" by 3D overlap; the reasoning stage is never re-run
            best, bn = None, 0
            for mm in ms:
                mk = erode(np.asarray(mm, bool), args.erode)
                h_ = mk[vv, uu]
                if args.band > 0 and h_.any():          # as above: median over in-mask z only
                    sub = np.where(h_)[0]
                    keep = front_layer(zz[h_], args.band)
                    h_ = np.zeros(len(h_), bool); h_[sub[keep]] = True
                hit = ii[h_]
                ov = int(seed[hit].sum())
                if ov > bn:
                    best, bn = hit, ov
            if best is not None and bn > 0:
                acc[best] += 1
                n_used += 1

        row = dict(q=k, n_gt=int(gt.sum()), n_frames=n_used, seed_n=int(seed.sum()),
                   conf=a.get("confidence"), acc_max=int(acc.max()))
        inter = int((seed & gt).sum())
        row["single"] = dict(n=int(seed.sum()), prec=inter / max(int(seed.sum()), 1),
                             rec=inter / ngt)
        for t in THS:
            pred = acc >= max(int(np.ceil(t * acc.max())), 1)
            n = int(pred.sum()); it = int((pred & gt).sum())
            row[f"th{t}"] = dict(n=n, prec=it / max(n, 1), rec=it / ngt)
        fh.write(json.dumps(row) + "\n"); fh.flush()
        s = row["single"]; b = row[f"th{THS[-1]}"]
        print(f"  {k:<28} frames {n_used:>2}  single n={s['n']:>5} p={s['prec']:.3f} | "
              f"th{THS[-1]} n={b['n']:>5} p={b['prec']:.3f}", flush=True)

    print(f"\n[shard {args.shard}] done. checkpoint -> {ckpt}")


if __name__ == "__main__":
    main()
