#!/usr/bin/env python3
"""Build the instance pool with the open-vocabulary segmenter instead of Molmo pointing + SAM,
and store it in the baseline's npz format.

This is the swap experiment that replaced the baseline's perception stage. To keep it
apples-to-apples, it reuses **the same frames** the Molmo reproduction used, isolating the
segmentation step as the only variable:

    read repro_molmo/frames/{desc}.npz -> frame_ids / video_ids
      -> construct the RGB path ({visit}/{video}/hires_wide/{video}_{fid}.jpg)
      -> segmenter with the canonical concept -> instance masks
      -> one candidate row per instance (frame / video / mask / centroid / score)
      -> save in the baseline's npz format

The oracle script then rebuilds depth and pose from those frame_ids to lift, which measures
the **segmenter's oracle ceiling** against the Molmo pool's.

Canonical concept mapping: the parsed acted-on object is reduced to a term the segmenter
responds well to (drawer/door/window handle -> handle; plug -> socket; dimmer or thermostat
knob -> knob; otherwise the last word). A separate union gate confirmed these terms work,
and `socket` rather than `plug` is the load-bearing one.

    python code/task2/s1_perception/run_sam3.py --root <root> --exp_root <exp> --sam3 <weights>
"""
import os, sys, json, glob, argparse
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import SCENEFUN3D  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sam3_util import init_sam3, sam3_masks                       # noqa: E402

DATA = SCENEFUN3D


def canonical(obj):
    o = obj.lower()
    if "handle" in o:
        return "handle"
    if "plug" in o or "socket" in o:
        return "socket"
    if "knob" in o:
        return "knob"
    if "switch" in o:
        return "switch"
    if "button" in o:
        return "button"
    return o.split()[-1]                                    # otherwise the last word


def nms_masks(masks, iou_th, ds=4):
    """Within-frame NMS, removing the redundant overlapping masks the segmenter emits on one
    object (around three per item at a low detection threshold). Largest mask wins.

    IoU is computed on a ``ds``-fold downsample to save compute. ``iou_th=None`` disables it.
    """
    if not masks or iou_th is None:
        return masks
    dm = [m[::ds, ::ds].astype(bool) for m in masks]
    keep = []
    for i in sorted(range(len(masks)), key=lambda k: -int(dm[k].sum())):
        if all(np.logical_and(dm[i], dm[j]).sum() / max(1, int(np.logical_or(dm[i], dm[j]).sum())) <= iou_th
               for j in keep):
            keep.append(i)
    return [masks[i] for i in keep]


def uniform_frames(visit, n_per_video):
    """Frame selection that does not depend on Molmo: n evenly spaced frames per video.

    Keeps only frames where rgb, depth and intrinsics all exist -- downstream lookups index
    depth_paths / intrinsics / poses by frame_id (pose via nearest-pose interpolation), so
    all three being present is exactly the safety condition.
    """
    fids, vids = [], []
    vdir = f"{DATA}/{visit}"
    for vid in sorted(d for d in os.listdir(vdir) if d.isdigit()):
        def ids(sub, ext):
            return {os.path.basename(p)[len(vid) + 1:-len(ext)]
                    for p in glob.glob(f"{vdir}/{vid}/{sub}/{vid}_*{ext}")}
        common = ids("hires_wide", ".jpg") & ids("hires_depth", ".png") & ids("hires_wide_intrinsics", ".pincam")
        if not common:
            continue
        keys = sorted(common, key=float)
        take = keys if len(keys) <= n_per_video else [
            keys[i] for i in np.linspace(0, len(keys) - 1, n_per_video).astype(int)]
        fids += take; vids += [vid] * len(take)
    return np.asarray(fids), np.asarray(vids)


def build_rgb_index(visit, video):
    """{frame_id_str: path}, parsed from hires_wide/{video}_{fid}.jpg."""
    idx = {}
    for p in glob.glob(f"{DATA}/{visit}/{video}/hires_wide/{video}_*.jpg"):
        fid = os.path.basename(p)[len(video) + 1:-4]        # strip the "{video}_" prefix and ".jpg"
        idx[fid] = p
    return idx


def lookup_rgb(idx, fid):
    """Exact match if present, otherwise the nearest timestamp."""
    if fid in idx:
        return idx[fid]
    if not idx:
        return None
    try:
        keys = np.array([float(k) for k in idx])
        klist = list(idx)
        j = int(np.argmin(np.abs(keys - float(fid))))
        return idx[klist[j]]
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="workdir/data (containing val)")
    ap.add_argument("--exp_root", required=True)
    ap.add_argument("--sam3", required=True, help="segmenter weights directory")
    ap.add_argument("--src_exp", default="repro_molmo")
    ap.add_argument("--dst_exp", default="repro_sam3")
    ap.add_argument("--det_th", type=float, default=0.3)
    ap.add_argument("--n_desc", type=int, default=0, help="0 = all; >0 = subset for a fast signal")
    ap.add_argument("--max_frames", type=int, default=0,
                    help="0 = every Molmo frame; >0 = cap frames per description to save time")
    ap.add_argument("--concept", default=None,
                    help="force a concept (e.g. 'drawer'), overriding the parsed one")
    ap.add_argument("--nms_iou", type=float, default=0.5,
                    help="2D-IoU threshold for within-frame NMS; None disables deduplication")
    ap.add_argument("--visits", default=None,
                    help="comma-separated visit allowlist, to regenerate only those scenes")
    ap.add_argument("--frames", default="src",
                    help="frame source. src = reuse --src_exp's frames (i.e. the ones the "
                         "baseline selected -- note its context gate rules ~17%% of "
                         "descriptions down to zero frames, so the segmenter never runs on "
                         "them at all). **uniform:N drops the Molmo dependency entirely**: N "
                         "evenly spaced frames per video, restricted to those with rgb, depth "
                         "and intrinsics all present. This script only takes frame_ids and "
                         "video_ids from src and never its points, so swapping the source is "
                         "sufficient to remove the dependency.")
    args = ap.parse_args()
    vset = set(args.visits.split(",")) if args.visits else None

    from PIL import Image
    predictor = init_sam3(args.sam3)
    src_frames = os.path.join(args.exp_root, args.src_exp, "frames")
    dst_frames = os.path.join(args.exp_root, args.dst_exp, "frames")
    os.makedirs(dst_frames, exist_ok=True)

    npzs = sorted(glob.glob(f"{src_frames}/*.npz"))
    stat = {"desc": 0, "empty": 0, "inst_total": 0}
    dumped = False

    for src in npzs:
        base = os.path.basename(src)
        dst = os.path.join(dst_frames, base)
        if os.path.exists(dst):
            continue
        visit = base.split("_")[0]
        desc_id = base[len(visit) + 1:-4]
        if vset is not None and visit not in vset:             # regenerate allowlisted scenes only
            continue
        if args.n_desc and stat["desc"] >= args.n_desc:
            break
        if args.frames.startswith("uniform:"):                 # Molmo-free: choose frames ourselves
            fids, vids = uniform_frames(visit, int(args.frames.split(":")[1]))
        else:
            d = np.load(src, allow_pickle=True)
            fids, vids = d["frame_ids"], d["video_ids"]
        if args.max_frames and len(fids) > args.max_frames:    # cap frames, evenly spaced
            keep = np.linspace(0, len(fids) - 1, args.max_frames).astype(int)
            fids, vids = fids[keep], vids[keep]
        if len(fids) <= 1:            # no source frames -> nothing to segment; store empty
                                      # (should not happen in uniform mode)
            np.savez_compressed(dst, frame_ids=np.asarray([0]), video_ids=np.asarray([0]),
                                masks_f=np.asarray([0]), scores_f=np.asarray([0]),
                                points=np.asarray([0]), orig_dims=np.asarray([0]))
            stat["empty"] += 1; continue

        # Canonical concept, read from this description's parse
        cot = json.load(open(f"{args.root}/val/{visit}/{visit}_qwen_cot.json"))
        descs = json.load(open(f"{DATA}/{visit}/{visit}_descriptions.json"))["descriptions"]
        di = next((i for i, dd in enumerate(descs) if dd["desc_id"] == desc_id), None)
        obj = cot[di].get("acted_on_object") if di is not None and di < len(cot) else None
        if isinstance(obj, list):
            obj = obj[0] if obj else None
        precise = args.concept or (obj.strip() if obj else "handle")   # e.g. "drawer handle"
        generic = canonical(obj) if obj else "handle"                  # last-word fallback

        rgb_idx = {}

        def collect(cpt):        # run one concept over all fids, then within-frame NMS -> rows
            ff, vv, mm, ss, pp, oo = [], [], [], [], [], []
            for fid, vid in zip(fids, vids):
                vid = str(vid)
                if vid not in rgb_idx:
                    rgb_idx[vid] = build_rgb_index(visit, vid)
                rp = lookup_rgb(rgb_idx[vid], str(fid))
                if rp is None:
                    continue
                rgb = np.asarray(Image.open(rp).convert("RGB"))
                masks = sam3_masks(predictor, rgb.astype(np.uint8), cpt, det_th=args.det_th)
                masks = nms_masks(masks, args.nms_iou)     # drop overlapping duplicates of one item
                for m in masks:
                    ys, xs = np.where(m)
                    if len(xs) == 0:
                        continue
                    ff.append(str(fid)); vv.append(vid); mm.append(m.astype(np.uint8)); ss.append(1)
                    pp.append([float(xs.mean()), float(ys.mean())]); oo.append(list(m.shape))
            return ff, vv, mm, ss, pp, oo

        concept = precise
        m_frame_ids, m_video_ids, m_masks, m_scores, m_points, m_orig = collect(precise)
        if not m_masks and generic != precise:             # precise term found nothing -> fall back
            concept = generic
            m_frame_ids, m_video_ids, m_masks, m_scores, m_points, m_orig = collect(generic)
        if not dumped:
            print(f"  [dump] {base} concept='{concept}'(precise='{precise}', nms={args.nms_iou}) "
                  f"-> {len(m_masks)} instances", flush=True)
            dumped = True
        stat["desc"] += 1; stat["inst_total"] += len(m_masks)
        if not m_masks:                                     # segmenter found nothing -> store empty
            np.savez_compressed(dst, frame_ids=np.asarray([0]), video_ids=np.asarray([0]),
                                masks_f=np.asarray([0]), scores_f=np.asarray([0]),
                                points=np.asarray([0]), orig_dims=np.asarray([0]))
            stat["empty"] += 1
        else:
            np.savez_compressed(
                dst, frame_ids=np.asarray(m_frame_ids), video_ids=np.asarray(m_video_ids),
                masks_f=np.stack(m_masks, axis=0), scores_f=np.asarray(m_scores),
                points=np.asarray(m_points), orig_dims=np.asarray(m_orig))
        print(f"  {base[:30]} concept={concept} inst={len(m_masks)}", flush=True)

    print(f"\n[run_sam3] desc={stat['desc']} empty={stat['empty']} instances={stat['inst_total']} "
          f"(mean {stat['inst_total']/max(stat['desc'],1):.1f} per description)")
    print(f"  output: {dst_frames}")
    print(f"\nNext: run the baseline's lifting on exp_name=repro_sam3, then oracle_disambig")
    print(f"  with --src_exp repro_sam3, to measure this pool's ceiling.")


if __name__ == "__main__":
    main()
