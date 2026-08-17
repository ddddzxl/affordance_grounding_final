#!/usr/bin/env python3
"""Generate the candidate table for every val instruction: a purely numeric, ground-truth
free question directory, ready for the reasoning stage.

## Design properties

- Full val: **30 visits / 445 descriptions**, with no sampling.
- **Ground truth is never read.** The annotation loader is not imported, and no answer file
  can appear in the output directory. Scoring is a separate step run afterwards, so the
  generation stage cannot see the answer -- which is what makes the reasoning honest.
- Sharded by visit with multi-GPU support (`--shard i --nshard 4`). The segmentation cache is
  reused within a visit, so **the shard key must be the visit**, not the description.
- Each question writes `cands.npz` (compressed target/host masks) plus `meta.json`
  (machine readable), so once the reasoning has chosen an instance id, the lift stage can
  take the mask directly **without re-running the segmenter**.
- The hard-coded geometric solution is recorded in meta.json as a **control arm**, but is
  **never written into candidates.txt** -- exposing it would anchor the reasoning and the two
  arms would stop being independent.

## Output layout

    <candidates root>/
      INDEX.md                  index of all questions (merged with --merge_index)
      q001_<visit>_<desc8>/
        task.md                 instruction + parse + frame-selection diagnostics (GT-free)
        candidates.txt          **the only thing the reasoning stage may read**
        candidates.png          the same content, visualised, for human review
        meta.json               machine readable: frame id, candidate geometry, diagnostics,
                                and the geometric control arm
        cands.npz               target + host masks (flat indices, compressed)

## Usage

    python code/task2/s2_candidates/dump_candidates.py --shard 0 --nshard 4
    python code/task2/s2_candidates/dump_candidates.py --merge_index    # after all shards
"""
import os, sys, json, glob, argparse, time
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import CANDIDATES, FUN3DU, FUN3DU_DATA, PARSE, SCENEFUN3D, SEGMENTER_WEIGHTS  # noqa: E402
PERCEPTION = os.path.join(_CODE_ROOT, "task2", "s1_perception")
sys.path.insert(0, FUN3DU); os.chdir(FUN3DU)
from utils import io                                               # noqa: E402
from utils.sun3d.data_parser import DataParser                     # noqa: E402
sys.path.insert(0, PERCEPTION)
from sam3_util import init_sam3, sam3_masks                        # noqa: E402
from framesel import (Box, pick2 as disc_pick2, solve_full, LEVELS,   # noqa: E402
                      filled_mask, in_filled)

DATA = SCENEFUN3D
OUT_DEFAULT = CANDIDATES
PARSE_DEFAULT = os.path.join(PARSE, "parse.json")
# ⚠️ Image dimensions are always read from the image itself. val mixes portrait (1440x1920)
#    and landscape (1920x1440) captures, and hard-coding a constant once misdiagnosed 5
#    landscape visits as having "20-60 cm registration misalignment", costing six rounds.
COLORS = np.array([(255, 70, 70), (70, 160, 255), (70, 230, 130), (255, 200, 50),
                   (225, 100, 240), (60, 230, 230), (255, 140, 70), (175, 130, 255),
                   (130, 225, 70), (255, 100, 170)])


def all_frames(visit, stride):
    out = []
    for vid in sorted(d for d in os.listdir(f"{DATA}/{visit}") if d.isdigit()):
        def ids(sub, ext):
            return {os.path.basename(p)[len(vid) + 1:-len(ext)]
                    for p in glob.glob(f"{DATA}/{visit}/{vid}/{sub}/{vid}_*{ext}")}
        for f in sorted(ids("hires_wide", ".jpg") & ids("hires_depth", ".png"),
                        key=float)[::stride]:
            out.append((vid, f))
    return out


PART_WORDS = ["handle", "knob", "switch", "button", "dial", "lever",
              "lid", "valve", "pull", "keypad", "panel", "pedal", "cord", "chain"]
# Part names grouped by **the affordance label they carry in the training split**, from the
# correspondence measured over 4480 annotations:
#   rotate                          -> dial / knob / valve / lever
#   tip_push / key_press            -> button / switch / panel / keypad
#   pinch_pull / hook_pull / hook_turn -> handle / pull / lid / knob
#   foot_push                       -> pedal
#   pull-cord switches (a kind of pinch_pull) -> cord / chain
# When falling back, **try the same group first** and only then across groups: same-group
# words describe the same manner of operation, so the semantic loss is minimal. Crossing
# groups (swapping dial for lid) has already drifted semantically, and a false detection
# there is worse than none, so it ranks last.
AFF_GROUPS = [["dial", "knob", "valve", "lever"],
              ["button", "switch", "panel", "keypad"],
              ["handle", "pull", "lid", "knob", "cord", "chain"],
              ["pedal"]]


def _ordered_parts(head):
    """**Returns same-group words only; never crosses groups.**

    Measured lesson: for "telephone keypad", none of the same-group words
    (button / switch / panel) were detected, and the chain ran on to the cross-group
    "telephone pull", which then "detected" something in 7 of 12 frames -- a phrase that does
    not exist semantically, which an open-vocabulary detector will nonetheless force-match to
    some region. **This is more insidious than detecting nothing**: a candidate pool gets
    built, and everything in it is the wrong object.

    Crossing groups means changing the manner of operation, so the semantics are already
    wrong; falling back to the host (the whole object, with the ground truth inside it) is
    strictly better.
    """
    seen, out = set(), []
    for w in [w for g in AFF_GROUPS if head in g for w in g if w != head]:
        if w not in seen:
            seen.add(w); out.append(w)
    return out


def concept_variants(concept, host):
    """The retrieval fallback chain -- **a pure lexical transformation applied uniformly to
    every concept**, containing no special case for any particular one.

    ## Why it is needed

    A concept name has to satisfy two constraints at once: **semantically accurate** and
    **present in the detector's vocabulary**. Only the first was being optimised. The measured
    cost: "dimmer dial" is semantically exactly right (all 6 dimmer instances in val are
    annotated as rotate) yet was **detected in 0 of 5 frames**, while the morphologically
    wrong "dimmer switch" at least builds a candidate pool. Across full val, dial-type
    concepts were undetectable in **18 of 22 (82%)** cases and "power button" in 6 of 11 (55%).

    **Being undetectable is the harder failure**: a slightly off concept can still earn
    partial credit, whereas no detection means the question cannot even be generated.

    ## Four tiers, tried in order

      1. the original term
      2. swap the head word for a same-group part name (dimmer dial -> dimmer switch / knob).
         Part names are highly interchangeable in natural language, while an open-vocabulary
         detector's vocabulary coverage is very uneven.
      3. drop the modifier and keep the head word (radiator dial -> dial)
      4. fall back to the host or the modifier itself (radiator dial -> radiator). The whole
         object is usually easy to detect and the ground truth lies inside it, so the lift at
         least overlaps.
    """
    parts = concept.split()
    head, mod = parts[-1].lower(), " ".join(parts[:-1])
    out = [concept]
    if head in PART_WORDS and mod:
        out += [f"{mod} {h}" for h in _ordered_parts(head)]      # swap part names
    if mod and head in PART_WORDS:
        # Drop the modifier, keeping the head word -- **only when the head word is a part
        # name**. Otherwise a legitimate compound noun gets broken: measured, "remote control"
        # was reduced to "control", and what that detects is anyone's guess.
        out.append(parts[-1])
    if host and host not in out:
        out.append(host)
    if mod and mod not in out:
        out.append(mod)
    if head not in PART_WORDS:
        # Reverse fallback: when the whole object is undetectable, try "whole object + part
        # name". **This is a last resort** -- retreating in granularity to a part drops GT
        # coverage from 71-93% down to 1-11%, so it is used only when even the in-pool
        # relaxation cannot rescue the question.
        # Device-level concepts (joystick, telephone, remote control) are single or compound
        # **whole-object nouns**, and every tier above degenerates for them -- the variants of
        # "joystick" are just "joystick". Measured: one frame detected no joystick at all
        # (while "joystick button" detected 20), leaving the candidate pool empty.
        # Retreating in granularity is unsatisfying, but **far better than no pool at all**.
        out += [f"{concept} {w}" for w in ("button", "handle", "panel", "keypad")]
    return out


_POLAR = {}


def _polar(H, W):
    if (H, W) not in _POLAR:
        xs, ys = np.meshgrid(np.arange(W), np.arange(H))
        xs = (xs - W // 2) / (W / 2.); ys = (ys - H // 2) / (H / 2.)
        _POLAR[(H, W)] = (np.sqrt(xs ** 2 + ys ** 2), np.arctan2(ys, xs))
    return _POLAR[(H, W)]

def mask_score(m, n_bins=30):
    """Reimplementation of the baseline's mask score -> (arc, mod). **Lower is better.**

    Map the image to polar coordinates about its centre, then take the KL divergence of two
    histograms of the mask's pixels against a uniform reference:

      arc = KL(angle distribution || uniform)          small = spread around the image centre
      mod = KL(radius distribution || uniform to max)  small = spread outward from the centre

    In effect: "the object is centred in the frame and well spread out". Cross-checked
    against the original (arc identical, mod differing by 5e-6).
    """
    from scipy.stats import entropy
    H, W = m.shape
    mod_map, arc_map = _polar(H, W)
    mm, ma = mod_map[m], arc_map[m]
    if mm.size == 0:
        return 0.0, 0.0
    h_arc, _ = np.histogram(ma, bins=n_bins, range=(-np.pi, np.pi))
    h_mod, b_mod = np.histogram(mm, bins=n_bins, range=(0, np.sqrt(2)))
    ref_mod = np.zeros(n_bins)
    ref_mod[:max(int(np.searchsorted(b_mod, mm.max())), 1)] = 1
    with np.errstate(divide="ignore", invalid="ignore"):
        return float(entropy(h_arc, np.ones(n_bins))), float(entropy(h_mod, ref_mod))


def xy_of(q, W):
    """Invert a flat index back to (xs, ys). f = ys*W + xs, so W must be **that frame's
    actual** width."""
    f = q["f"]
    return (f % W).astype(np.int64), (f // W).astype(np.int64)


def in_bbox_d(q, h, W, frac=0.6):
    """Fraction of q's pixels inside h's **bbox**.

    bbox rather than mask, because the segmenter frequently carves the handle out of the
    drawer mask, and a mask-based containment test would then miss it.
    """
    xs, ys = xy_of(q, W)
    if not len(xs):
        return False
    return float(((xs >= h["x0"]) & (xs <= h["x1"]) &
                  (ys >= h["y0"]) & (ys <= h["y1"])).mean()) >= frac


def rel_dist_d(q, h):
    return abs(q["cx"] - h["cx"]) + abs(q["cy"] - h["cy"])


def nms_score(cs, th=0.75):
    """Keep in descending **score** order; a later candidate whose intersection-over-minimum
    with a kept one exceeds th is suppressed.

    The sort key is score, not area. Sorting by area keeps the box covering half the image
    and suppresses the correct small one -- measured: one cabinet detection covered 24.9% of
    the frame.
    """
    keep = []
    for c in sorted(cs, key=lambda d: -d["score"]):
        if all(np.intersect1d(c["f"], k["f"], assume_unique=True).size
               / max(1, min(c["f"].size, k["f"].size)) <= th for k in keep):
            keep.append(c)
    return keep


def load_cases(parse_path):
    """Returns [(visit, desc_id, parse)] sorted globally by (visit, desc_id).
    The question number is the index + 1."""
    P = json.load(open(parse_path))
    cases = []
    for v in sorted(k for k in P if k != "_meta"):
        for did in sorted(k for k in P[v] if k != "_meta"):
            p = P[v][did]
            if not isinstance(p, dict) or "target" not in p or "_fail" in p:
                continue
            cases.append((v, did, p))
    return cases


def plan_shards(cases, nshard):
    """Shard by visit -- the segmentation cache is reused per visit, so splitting a visit
    across shards invalidates all of it.

    Uses longest-processing-time greedy packing to balance description counts, since a
    visit holds anywhere from 1 to 29 descriptions.
    """
    per = {}
    for v, _, _ in cases:
        per[v] = per.get(v, 0) + 1
    bins, load = [[] for _ in range(nshard)], [0] * nshard
    for v, n in sorted(per.items(), key=lambda t: -t[1]):
        i = int(np.argmin(load)); bins[i].append(v); load[i] += n
    return [sorted(b) for b in bins], load


def merge_index(out_dir):
    rows = []
    for d in sorted(glob.glob(os.path.join(out_dir, "q*_*"))):
        f = os.path.join(d, "meta.json")
        if not os.path.exists(f):
            continue
        m = json.load(open(f))
        cont = next((e["name"] for e in m["parse"]["entities"]
                     if e["role"] == "container"), "-")
        nc = {c: len(v) for c, v in m["candidates"].items()}
        rows.append(f"| q{m['q']:03d} | {m['visit']} | `{m['desc_id'][:8]}` | {m['text']} | "
                    f"{m['parse']['target']['concept']} | {m['parse']['target']['host']} | "
                    f"{cont} | {m['framesel']['level']} | {nc} |")
    hdr = ["# Full-val question set", "",
           f"**{len(rows)}** questions, one directory each. The reasoning stage reads "
           "**only `candidates.txt` / `candidates.png`**.", "",
           "This set contains **no ground truth** -- there is no answer file in any "
           "directory. Scoring is an independent step run after the answers are fixed.", "",
           "| q | visit | desc_id | instruction | target | host | container | level | candidates |",
           "|---|---|---|---|---|---|---|---|---|"]
    open(os.path.join(out_dir, "INDEX.md"), "w").write("\n".join(hdr + rows) + "\n")
    print(f"[merge] {len(rows)} questions -> {out_dir}/INDEX.md")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=FUN3DU_DATA)
    ap.add_argument("--sam3", default=SEGMENTER_WEIGHTS)
    ap.add_argument("--parse", default=PARSE_DEFAULT)
    ap.add_argument("--out", default=OUT_DEFAULT)
    ap.add_argument("--split", default="val")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshard", type=int, default=1)
    ap.add_argument("--stride", type=int, default=10,
                    help="matches the full pipeline run")
    ap.add_argument("--det_th", type=float, default=0.15,
                    help="0.30 discards correct candidates -- measured: one drawer with "
                         "gt_frac=1.0 scored below 0.3")
    ap.add_argument("--nms", type=float, default=0.75)
    ap.add_argument("--max_list", type=int, default=20)
    ap.add_argument("--topk", type=int, default=8)
    ap.add_argument("--viz", type=int, default=1)
    ap.add_argument("--resume", type=int, default=1,
                    help="skip questions that already have a meta.json")
    ap.add_argument("--fallback", type=int, default=1,
                    help="on an undetectable target, walk the lexical fallback chain "
                         "(see concept_variants)")
    ap.add_argument("--n_probe", type=int, default=12, help="frames used to probe the fallback")
    ap.add_argument("--global_fb", type=int, default=1,
                    help="if the fallback chain also fails, revert to global uniform sampling "
                         "as the baseline does, guaranteeing every question has frames")
    ap.add_argument("--n_fb", type=int, default=40, help="frames for the global fallback")
    ap.add_argument("--pool", choices=["all", "fun3du"], default="all",
                    help="all = scan every frame directly; "
                         "fun3du = build a top-N pool by the baseline's score first")
    ap.add_argument("--n_pool", type=int, default=50,
                    help="pool size (the baseline's own setting is 50)")
    ap.add_argument("--redo", default=None,
                    help="comma-separated desc8 ids, or a file path: force regeneration "
                         "(mandatory for any question whose concept changed)")
    ap.add_argument("--limit", type=int, default=0, help=">0 runs only the first N (smoke test)")
    ap.add_argument("--merge_index", action="store_true")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    if args.merge_index:
        merge_index(args.out); return

    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mp
    from PIL import Image

    REDO = set()
    if args.redo:
        if os.path.exists(args.redo):
            REDO = {w for l in open(args.redo) for w in l.split()[:2] if len(w) == 8}
        else:
            REDO = {x.strip()[:8] for x in args.redo.split(",") if x.strip()}
        print(f"[redo] forcing regeneration of {len(REDO)}")

    cases = load_cases(args.parse)
    qno = {(v, d): i + 1 for i, (v, d, _) in enumerate(cases)}
    bins, load = plan_shards(cases, args.nshard)
    mine = set(bins[args.shard])
    todo = [c for c in cases if c[0] in mine]
    if args.limit:
        todo = todo[:args.limit]
    print(f"[shard {args.shard}/{args.nshard}] visits={sorted(mine)}\n"
          f"  {len(todo)} questions in this shard / {len(cases)} in full val   "
          f"per-shard load={load}", flush=True)

    parser = DataParser(args.root, args.split)
    v2v = io.get_visit_to_videos(args.root, args.split)
    predictor = init_sam3(args.sam3)

    probe = {}          # (concept, vid, fid) -> list[Box]. Frame selection needs only
                        # geometry and confidence, so **masks are not stored**.
    fsc = {}            # (concept, vid, fid) -> (score, arc, mod). **Three floats only.**

    def scan(v, c, vid, fid):
        # A concept may be written "A | B" to mean the **union of synonyms**: query each and
        # merge. This is a general mechanism, not a special case -- any concept can be written
        # this way.
        # Purpose: one object may correspond to several names in an open-vocabulary detector's
        # view (joystick / controller), and picking a single term loses recall, while the
        # union **does not change granularity** -- which is what makes it fundamentally
        # different from falling back to "button".
        if "|" in c:
            out = []
            for c1 in [x.strip() for x in c.split("|") if x.strip()]:
                out += scan(v, c1, vid, fid)
            return nms_box_local(out)
        k = (c, vid, fid)
        if k not in probe:
            rgb = np.asarray(Image.open(
                f"{DATA}/{v}/{vid}/hires_wide/{vid}_{fid}.jpg").convert("RGB"))
            out = []
            for m, sc in sam3_masks(predictor, rgb.astype(np.uint8), c,
                                    det_th=args.det_th, with_scores=True):
                ys, xs = np.where(m)
                if len(xs):
                    out.append(Box(int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()),
                                   float(xs.mean()), float(ys.mean()), int(len(xs)), float(sc)))
            probe[k] = out
        return probe[k]

    def nms_box_local(bs, th=0.75):
        """Deduplicate a union by score -- different terms often box the same object.
        Intersection-over-minimum on bboxes is a good enough approximation here."""
        keep = []
        for b in sorted(bs, key=lambda x: -x.s):
            ok = True
            for k2 in keep:
                ix = max(0, min(b.x1, k2.x1) - max(b.x0, k2.x0))
                iy = max(0, min(b.y1, k2.y1) - max(b.y0, k2.y0))
                if ix * iy / max(1, min(b.a, k2.a)) > th:
                    ok = False; break
            if ok:
                keep.append(b)
        return keep

    def full(v, c, vid, fid):
        """Re-run on the selected frame to obtain full candidates including masks."""
        if "|" in c:
            out = []
            for c1 in [x.strip() for x in c.split("|") if x.strip()]:
                out += full(v, c1, vid, fid)
            return nms_score(out, args.nms)          # single NMS pass over the union
        rgb = np.asarray(Image.open(
            f"{DATA}/{v}/{vid}/hires_wide/{vid}_{fid}.jpg").convert("RGB"))
        Hh, Ww = rgb.shape[:2]
        out = []
        for m, s in sam3_masks(predictor, rgb.astype(np.uint8), c,
                               det_th=args.det_th, with_scores=True):
            ys, xs = np.where(m)
            if not len(xs):
                continue
            out.append(dict(m=m, f=(ys.astype(np.int64) * Ww + xs).astype(np.int64),
                            score=round(float(s), 3),
                            x0=int(xs.min()), x1=int(xs.max()),
                            y0=int(ys.min()), y1=int(ys.max()),
                            cx=round(float(xs.mean()), 1), cy=round(float(ys.mean()), 1),
                            npix=int(len(xs)),
                            area_pct=round(100 * len(xs) / (Hh * Ww), 3)))
        return nms_score(out, args.nms)

    cur_v, frames, VW, VH = None, None, None, None
    t0, ndone, nskip, nfail = time.time(), 0, 0, 0
    for v, did, p in todo:
        qi = qno[(v, did)]
        d = os.path.join(args.out, f"q{qi:03d}_{v}_{did[:8]}")
        if (args.resume and os.path.exists(os.path.join(d, "meta.json"))
                and did[:8] not in REDO):
            nskip += 1; continue
        if v != cur_v:
            probe.clear(); fsc.clear()          # caches live for one visit; clear on change
            frames = all_frames(v, args.stride)
            if not frames:
                print(f"  [!] {v} has no usable frames, skipping the whole visit", flush=True)
                cur_v = v; continue
            _v0, _f0 = frames[0]
            VW, VH = Image.open(f"{DATA}/{v}/{_v0}/hires_wide/{_v0}_{_f0}.jpg").size
            # Frame selection uses one (VW, VH) for the whole visit, which assumes every video
            # in the visit shares an image size. Measured: 0 exceptions across the 30 val
            # visits -- but that is an incidental property of the data, so it is locked down
            # with an assertion rather than trusted.
            # (Hard-coding the size was the bug that misdiagnosed 5 landscape visits as having
            # "20-60 cm registration misalignment" and cost six rounds of investigation.)
            _sz = {Image.open(f"{DATA}/{v}/{a}/hires_wide/{a}_{b}.jpg").size
                   for a, b in {(x, y) for x, y in frames[:: max(len(frames)//6, 1)]}}
            assert len(_sz) == 1, (f"{v} has inconsistent image sizes: {_sz} -- frame selection "
                                   f"cannot share one (W, H)")
            cur_v = v
            print(f"  -- visit {v}: {len(frames)} candidate frames, {VW}x{VH} "
                  f"({'landscape' if VW > VH else 'portrait'})", flush=True)
        tgt_c = p["target"]["concept"]
        host_c = p["target"]["host"]

        # ---------------- Retrieval fallback: if the target is detected in no frame at all,
        #                  try another way of naming it ----------------
        # Triggered **only when the primary concept is detected nowhere**, so normal questions
        # pay nothing. The probe asks "is there any detection" over n_probe uniformly sampled
        # frames; it does not run full frame selection.
        fb = None
        if args.fallback:
            sub = frames[:: max(len(frames) // args.n_probe, 1)][:args.n_probe]
            if not any(scan(v, tgt_c, a, b) for a, b in sub):
                for alt in concept_variants(tgt_c, host_c)[1:]:
                    k = sum(1 for a, b in sub if scan(v, alt, a, b))
                    if k:
                        fb = dict(orig=tgt_c, used=alt, probe_hits=k, probe_frames=len(sub))
                        p = json.loads(json.dumps(p))       # deep copy; do not pollute the
                                                            # shared parse
                        p["target"]["concept"] = alt
                        if p["target"]["host"] == alt:      # falling back to the host makes
                                                            # the two names identical
                            p["target"]["host"] = None
                        for e in p["entities"]:
                            if e["name"] == tgt_c:
                                e["name"] = alt
                        for r_ in p["relations"]:
                            for kk in ("a", "b"):
                                if r_[kk] == tgt_c:
                                    r_[kk] = alt
                        for s_ in p["select"]:
                            if s_["on"] == tgt_c:
                                s_["on"] = alt
                        # Deduplicate: after the fallback the target may collide with an
                        # existing entity name
                        seen = set(); ents = []
                        for e in p["entities"]:
                            if e["name"] not in seen:
                                seen.add(e["name"]); ents.append(e)
                        p["entities"] = ents
                        tgt_c = alt; host_c = p["target"]["host"]
                        print(f"  [q{qi:03d}] {v} {did[:8]} retrieval fallback "
                              f"{fb['orig']!r} -> {alt!r} ({k}/{len(sub)} frames)", flush=True)
                        break
                if fb is None:
                    print(f"  [q{qi:03d}] {v} {did[:8]} whole fallback chain exhausted with no "
                          f"detection "
                          f"({len(concept_variants(p['target']['concept'], host_c))} variants)",
                          flush=True)

        concepts, roles = [], {}
        for e in p["entities"]:
            if e["instanceable"] and e["name"] not in concepts:
                concepts.append(e["name"]); roles[e["name"]] = e["role"]
        if tgt_c not in concepts:               # the parse occasionally omits the target
            concepts.insert(0, tgt_c); roles[tgt_c] = "target"

        # ---------------- Frame selection ----------------
        # disc3 = discriminative hard conditions + H5 directional borders + self-consistency,
        # without clustering.
        #
        # A baseline-style candidate pool then ranks by a soft score, **ranking only, never
        # eliminating**. Measured justification, on 90 questions where disc3 had selected
        # the wrong frame:
        #   the frame that actually solves the question ranks **3rd at the median** under the
        #   baseline's ordering; it is first 41.6% of the time and in the top 8 83.1% of the
        #   time -- while our own ordering hit it 0 times on those same 90.
        # The key is to **score the container or host, not the target**: a handle is far too
        # small, so ranking on it is ranking on noise, whereas the cabinet is easy to detect
        # and the handle is attached to it. This is also the root cause of H1 (requiring a
        # target detection) rejecting far too aggressively.
        fpool = None
        if args.pool == "fun3du":
            cont_c0 = next((e["name"] for e in p["entities"]
                            if e["role"] == "container" and e["instanceable"]), None)
            rank_c = cont_c0 or host_c or tgt_c
            rows_ = []
            for a_, b_ in frames:
                k_ = (rank_c, a_, b_)
                if k_ not in fsc:
                    rgb_ = np.asarray(Image.open(
                        f"{DATA}/{v}/{a_}/hires_wide/{a_}_{b_}.jpg").convert("RGB"))
                    best_ = (0.0, 0.0, 0.0)
                    for m_, s_ in sam3_masks(predictor, rgb_.astype(np.uint8), rank_c,
                                             det_th=args.det_th, with_scores=True):
                        if float(s_) > best_[0]:
                            ar_, mo_ = mask_score(np.asarray(m_, bool))
                            best_ = (float(s_), ar_, mo_)
                    fsc[k_] = best_          # three floats only; masks are not cached
                rows_.append(fsc[k_])
            # ⚠️ **Only frames that actually detected the container may take part in the
            # ranking.** mask_score returns (0,0) for an empty mask, and arc/mod are KL
            # divergences where smaller is better, so after normalisation 0 becomes the
            # minimum -> `1 - nz(0) = 1` -> an empty frame scores full marks:
            #     empty frame        S = 0.5*(0.5*(1+1) + 0  ) = 0.50
            #     real but off-centre S = 0.5*(0.5*(0+0) + 0.9) = 0.45   <- lower!
            # Measured: one visit has many frames where the camera faces away entirely; they
            # all scored 0.50, filled the top-50, and pushed out the one frame that detected
            # four joysticks and six TV stands.
            # The baseline's own scored-mask filter returns only frames with detections, so
            # empty frames never enter its ranking either.
            ok_ = [i for i, r in enumerate(rows_) if r[0] > 0]
            if ok_:
                O = np.array([rows_[i][0] for i in ok_])
                A_ = np.array([rows_[i][1] for i in ok_])
                M_ = np.array([rows_[i][2] for i in ok_])

                def _nz(x):
                    r = x.max() - x.min()
                    return (x - x.min()) / r if r > 1e-9 else np.zeros_like(x)
                S_ = 0.5 * (0.5 * ((1 - _nz(M_)) + (1 - _nz(A_))) + O)
                order = [ok_[i] for i in np.argsort(-S_)[:args.n_pool]]
            else:
                order = list(range(min(len(frames), args.n_pool)))   # nothing detected anywhere
            fpool = [frames[i] for i in order]
            print(f"  [q{qi:03d}] {v} {did[:8]} pool: {len(ok_)} of {len(frames)} frames "
                  f"detect {rank_c!r} -> top{len(fpool)}", flush=True)


        def get_for(vid_, fid_, _v=v):
            return lambda c: scan(_v, c, vid_, fid_)
        try:
            top, level, stats = disc_pick2(fpool or frames, get_for, p, VW, VH,
                                           topk=args.topk, use_cluster=False)
        except Exception as e:
            print(f"  [q{qi:03d}] {v} {did[:8]} frame selection raised {type(e).__name__}: {e}",
                  flush=True)
            nfail += 1; continue
        gfb = None
        if not top and fpool:
            # In-pool relaxation, in two tiers. When H1-H5 reject everything, **the pool score
            # alone is not enough**: that score is computed on the container (object centred
            # and well spread), and a high score does **not** imply the target is visible --
            # measured, one question's pool top-1 (a shelf scoring 0.890) had zero detections
            # for either target concept, while another frame of the same video had twenty.
            # So first look inside the pool for frames where **the target is detectable**
            # (H1 alone, relaxing H2-H5), and only fall back to pool top-1 if there are none.
            # scan() already ran the target on every pool frame during the H1 test, so these
            # are all cache hits and cost essentially nothing.
            vis = []
            for a_, b_ in fpool:
                bs_ = scan(v, tgt_c, a_, b_)
                if bs_:
                    vis.append((max(x.a for x in bs_), a_, b_))
            if vis:
                vis.sort(key=lambda t: -t[0])          # largest target area first
                top = [(a_, b_, {}) for _, a_, b_ in vis[:args.topk]]
                level = "POOL-T"
                gfb = dict(kind="pool_target_visible", n_pool=len(fpool), n_vis=len(vis))
                print(f"  [q{qi:03d}] {v} {did[:8]} all hard conditions rejected -> "
                      f"{len(vis)}/{len(fpool)} pool frames have the **target visible**, "
                      f"taking the largest by area, top{len(top)}", flush=True)
            else:
                top = [(a, b, {}) for a, b in fpool[:args.topk]]
                level = "POOL"
                gfb = dict(kind="pool_topk", n_pool=len(fpool), n_vis=0)
                print(f"  [q{qi:03d}] {v} {did[:8]} all hard conditions rejected, and **no "
                      f"frame in the pool** detects {tgt_c!r} -> falling back to pool "
                      f"top{len(top)}", flush=True)
        if not top and args.global_fb:
            # ---------------- Global fallback, following the baseline ----------------
            # "Undetectable means the whole question is dropped" is a failure mode **unique to
            # us**: when the baseline fails to detect its context object it calls a global
            # uniform sampler for 50 frames, so "no frames available" is structurally
            # impossible there. This does the same. Once every question is guaranteed
            # candidate frames, the remaining failures can only be "the thing really is not in
            # the frame" rather than "our mechanism refused to generate the question" -- which
            # is what makes the attribution clean.
            cont_c = next((e["name"] for e in p["entities"]
                           if e["role"] == "container" and e["instanceable"]), None)
            lm_c = next((e["name"] for e in p["entities"]
                         if e["role"] == "landmark" and e["instanceable"]), None)
            pool = frames[:: max(len(frames) // args.n_fb, 1)][:args.n_fb]
            # First look for frames where **the target is detectable** -- the same criterion
            # as the in-pool tier above.
            # This tier used to jump straight to area ranking, so questions with neither host
            # nor container (typically "Unplug the TV", parsed as target=plug / landmark=TV /
            # no host / no container) scored 0.0 on every frame, and sorting an all-zero list
            # is **no sorting at all** -- the result was the first uniformly sampled frame, a
            # completely arbitrary image. Measured: **all 26** full-val questions with zero
            # candidates came from exactly this path.
            # The same idea was already implemented one tier up; this completes it rather than
            # adding a new heuristic.
            gvis = []
            for a, b in pool:
                bs = scan(v, tgt_c, a, b)
                if bs:
                    gvis.append((max(x.a for x in bs), a, b))
            if gvis:
                gvis.sort(key=lambda t: -t[0])
                top = [(a, b, {}) for _, a, b in gvis[:args.topk]]
                level = "GLOBAL-T"
                gfb = dict(kind="global_target_visible", n_pool=len(pool), n_vis=len(gvis))
                print(f"  [q{qi:03d}] {v} {did[:8]} global fallback: {len(gvis)} of "
                      f"{len(pool)} frames have the **target visible** -> top{len(top)}",
                      flush=True)
            else:
                # Only fall back to area ranking when the target is undetectable everywhere.
                # **The landmark must count too**: a locator named in the instruction also
                # brings the camera near the target (the plug for "unplug the TV" is right
                # next to the TV), and omitting it throws away a signal the instruction
                # explicitly provided.
                ranked = []
                for a, b in pool:
                    s = 0.0
                    for c in (host_c, cont_c, lm_c):
                        if c:
                            bs = scan(v, c, a, b)
                            if bs:
                                s = max(s, max(x.a for x in bs) / float(VW * VH))
                    ranked.append((s, a, b))
                ranked.sort(key=lambda t: -t[0])
                top = [(a, b, {}) for _, a, b in ranked[:args.topk]]
                level = "GLOBAL"
                gfb = dict(n_pool=len(pool), ranked_by="host/container/landmark area",
                           best_score=round(ranked[0][0], 5) if ranked else 0.0)
                print(f"  [q{qi:03d}] {v} {did[:8]} global fallback over {len(pool)} frames, "
                      f"target never visible -> ranked by host/container/landmark area, "
                      f"top{len(top)} (largest covers {gfb['best_score']:.4f} of the image)",
                      flush=True)
        if not top:
            print(f"  [q{qi:03d}] {v} {did[:8]} skipped (no qualifying frame, level={level})",
                  flush=True)
            nfail += 1; continue
        vid, fid, _info = top[0]
        fsdiag = dict(mode="disc3", level=level, n_top=len(top),
                      topk=[[a, b] for a, b, _ in top],
                      consistency=[r.get("consistency") for _, _, r in top[:4]],
                      n_frames=len(frames), stride=args.stride, global_fallback=gfb,
                      pool=args.pool, n_pool=(len(fpool) if fpool else None))

        os.makedirs(d, exist_ok=True)
        rgb0 = np.asarray(Image.open(
            f"{DATA}/{v}/{vid}/hires_wide/{vid}_{fid}.jpg").convert("RGB"))
        Himg, Wimg = rgb0.shape[:2]
        cands = {c: full(v, c, vid, fid) for c in concepts}
        # ---- In-place fallback: if the target is still empty on the SELECTED frame, try the
        #      fallback terms right here, on this frame. ----
        # The earlier probe ran over 12 uniformly sampled frames and concluded "no fallback
        # needed" as soon as any one of them had a detection -- but the frame finally selected
        # need not be that one. Measured: on one question the probe over 306 frames reported
        # the concept as detectable and suppressed the fallback, yet the pool-selected frame
        # had zero detections and the candidate pool came out empty.
        # Probe frame != frame used, so the test must be repeated on the frame used.
        if args.fallback and not cands.get(tgt_c):
            for alt in concept_variants(tgt_c, host_c)[1:]:
                got = full(v, alt, vid, fid)
                if got:
                    print(f"  [q{qi:03d}] {v} {did[:8]} in-place fallback on the selected "
                          f"frame: {tgt_c!r} -> {alt!r} ({len(got)} detections)", flush=True)
                    fb = dict(orig=tgt_c, used=alt, n_on_frame=len(got), where="selected_frame")
                    cands.pop(tgt_c, None); cands[alt] = got
                    concepts = [alt if c == tgt_c else c for c in concepts]
                    roles[alt] = roles.pop(tgt_c, "target")
                    p = json.loads(json.dumps(p))
                    p["target"]["concept"] = alt
                    if p["target"]["host"] == alt:
                        p["target"]["host"] = None
                    for e in p["entities"]:
                        if e["name"] == tgt_c:
                            e["name"] = alt
                    for r_ in p["relations"]:
                        for kk in ("a", "b"):
                            if r_[kk] == tgt_c:
                                r_[kk] = alt
                    for s_ in p["select"]:
                        if s_["on"] == tgt_c:
                            s_["on"] = alt
                    tgt_c = alt; host_c = p["target"]["host"]
                    break

        # ---------------- Hard-coded geometric solution: a **control arm**. ----------------
        # It goes into meta.json only and is **never written into candidates.txt** -- exposing
        # it would anchor the reasoning and the two arms would stop being independent.
        #
        # ⚠️ solve_full is **bbox level** (its own comment: "this layer only has Boxes, so it
        #    is unconditionally conservative; the real two-tier test lives in the pipeline
        #    stage"). The mask-level attribution is added back here, reproducing that stage
        #    exactly:
        #      inside the **hole-filled** host mask -> membership is clear, keep them all
        #                                              (genuine handle pairs land here)
        #      only inside the host bbox            -> an oblique-view bbox swelled into a
        #                                              neighbour -> conservatively keep nearest
        #    Without this the geometric arm could never produce a handle pair, and it would no
        #    longer be the same baseline as the reasoning arm.
        geom = {"target": [], "host": None, "why": None, "attrib": None}
        try:
            bx = {c: [Box(q["x0"], q["x1"], q["y0"], q["y1"], q["cx"], q["cy"],
                          q["npix"], q["score"]) for q in cands[c]] for c in concepts}
            lv = next((c for c in LEVELS if c["name"] == level), LEVELS[0])
            pk, rr = solve_full(lambda c: bx.get(c, []), p, Wimg, Himg, lv)

            def idx_of(c, b):                       # Box -> index into cands[c], matched by bbox
                for i2, q in enumerate(cands.get(c, [])):
                    if (q["x0"], q["y0"], q["x1"], q["y1"]) == (b.x0, b.y0, b.x1, b.y1):
                        return i2
                return None
            ch = rr.get("chosen_host")
            hi = idx_of(host_c, ch) if (ch is not None and host_c) else None
            geom["host"] = hi
            Tin = [i for i in (idx_of(tgt_c, t) for t in rr.get("targets", []))
                   if i is not None]
            picks = []
            if hi is not None and Tin:
                hf = filled_mask(cands[host_c][hi]["m"])
                picks = [i for i in Tin
                         if in_filled(xy_of(cands[tgt_c][i], Wimg), hf)]
                if picks:
                    geom["attrib"] = f"filled({len(picks)})"
                else:
                    hb = cands[host_c][hi]
                    inb = [i for i in Tin if in_bbox_d(cands[tgt_c][i], hb, Wimg)]
                    if inb:
                        picks = [min(inb, key=lambda i: rel_dist_d(cands[tgt_c][i], hb))]
                        geom["attrib"] = f"bbox_fallback({len(inb)} candidates, kept 1)"
                    else:
                        picks = [min(Tin, key=lambda i: rel_dist_d(cands[tgt_c][i], hb))]
                        geom["attrib"] = "nearest"
            if not picks:                            # no usable host -> fall back to the
                                                     # bbox-level solve
                picks = [i for i in (idx_of(tgt_c, b) for b in (pk or []))
                         if i is not None]
                geom["attrib"] = "solve_full(bbox level)"
            geom["target"] = sorted(picks)
            geom["why"] = rr.get("why")
        except Exception as e:
            geom["why"] = f"{type(e).__name__}: {e}"

        # ---------------- task.md ----------------
        T = [f"# q{qi:03d} - {v} / {did[:8]}", "", "## Instruction", "", f"> {p['text']}", "",
             "## Stage 0 parse", "", "```json",
             json.dumps({k: p[k] for k in ("target", "entities", "relations", "select", "residual")
                         if k in p}, ensure_ascii=False, indent=1), "```", "",
             "## Selected frame", "", f"- `{v}/{vid}/{fid}`  ({Wimg}x{Himg})",
             f"- selection: **disc3**, relaxation level **{level}**, "
             f"from {len(frames)} frames (stride={args.stride})",
             f"- top-{len(top)} alternative frames: `{[[a, b] for a, b, _ in top]}`", "",
             "## Candidate counts (after NMS)", ""]
        for c in concepts:
            T.append(f"- `{c}` ({roles[c]}): **{len(cands[c])}**")
        T += ["", "> This directory contains **no ground truth**. Reasoning reads only "
                  "`candidates.txt` / `candidates.png`."]
        open(os.path.join(d, "task.md"), "w").write("\n".join(T))

        # ---------------- candidates.txt: the sole input to the reasoning stage ----------------
        L = [f'TASK: "{p["text"]}"', "", "PARSE:",
             f'  target concept = "{tgt_c}"   <- the thing that must be output',
             f'  host           = {host_c!r}   <- countable object the target sits on']
        for e in p["entities"]:
            L.append(f'  entity  : {e["name"]!r}  role={e["role"]}'
                     + ("" if e["instanceable"] else "   (NOT instanceable — not searched)"))
        for r in p.get("relations", []):
            L.append(f'  relation: {r["rel"]}(a={r["a"]!r}, b={r["b"]!r})')
        for s in p.get("select", []):
            L.append(f'  select  : on={s["on"]!r} axis={s["axis"]} value={s["value"]!r} '
                     f'index={s["index"]} from={s["from"]!r}')
        if p.get("residual"):
            L.append(f'  residual: {p["residual"]}')
        L += ["", "IMAGE COORDINATE SYSTEM (read carefully):",
              f"  image is {Wimg} wide (x) by {Himg} tall (y). "
              f" ({'PORTRAIT' if Himg > Wimg else 'LANDSCAPE'})",
              f"  x increases to the RIGHT.  x=0 is the LEFT edge, x={Wimg-1} is the RIGHT edge.",
              f"  y increases DOWNWARD.      y=0 is the TOP edge,  y={Himg-1} is the BOTTOM edge.",
              '  => "top" = SMALL y,   "bottom" = LARGE y',
              '  => "left" = SMALL x,  "right"  = LARGE x',
              '  => "A above B" means A.cy < B.cy.  "A on top of B" means A.y1 <= B.y0.',
              "  area% = mask pixels as % of the whole image.",
              "  score = SAM3 detection confidence.",
              "  NOTE: detections are imperfect. A box covering a large fraction of the image",
              "        is usually several objects merged, not one piece of furniture.", "",
              "INSTANCES (after score-ranked NMS, sorted by score):",
              f"  {'class':<18} {'id':>3} {'xmin':>5} {'xmax':>5} {'ymin':>5} {'ymax':>5} "
              f"{'cx':>7} {'cy':>7} {'area%':>7} {'score':>6}"]
        for c in concepts:
            lst = cands[c]
            if not lst:
                L.append(f"  {c:<18}  (0 detections)")
            for i, q in enumerate(lst[:args.max_list]):
                L.append(f"  {c:<18} {i:>3} {q['x0']:>5} {q['x1']:>5} {q['y0']:>5} {q['y1']:>5} "
                         f"{q['cx']:>7} {q['cy']:>7} {q['area_pct']:>7} {q['score']:>6}")
            if len(lst) > args.max_list:
                L.append(f"  ... ({len(lst)-args.max_list} more {c!r} with lower score omitted)")
        # ---- Containment table: the reasoning stage only sees bboxes and cannot run a mask
        #      test, so it is computed here at generation time. ----
        # Rule (identical to the pipeline's attribution stage): the ordering constraint picks
        # a host, and every target inside that host's **hole-filled mask** is emitted. A
        # narrow host covers one, a wide host covers two; the structural difference follows
        # from the host's actual width, so the reasoner does not have to decide in advance
        # whether "this row splits left/right".
        # Hole filling rather than bbox: at an oblique angle a host's axis-aligned bbox swells
        # into the neighbouring row (measured: one question's bottom drawer bbox covered three
        # handles where only two belonged to it).
        if host_c and host_c in cands and cands.get(tgt_c):
            L += ["", f"CONTAINMENT ({tgt_c} inside the FILLED mask of each {host_c}):"]
            for hi_, hq in enumerate(cands[host_c][:args.max_list]):
                hf_ = filled_mask(hq["m"])
                ins = [ti for ti, tq in enumerate(cands[tgt_c][:args.max_list])
                       if in_filled(xy_of(tq, Wimg), hf_)]
                L.append(f"  {host_c} #{hi_:<3} (cy {hq['cy']:>7}) contains "
                         + (", ".join(f"#{i}" for i in ins) if ins else "(none)"))
            L.append("  -> apply `select` to the HOST, then output EVERY target it contains.")
        L += ["", f'QUESTION: which "{tgt_c}" instance id(s) does the task refer to?',
              "  Reason step by step: resolve container -> host -> target.",
              "  A single referred object may carry MORE THAN ONE target instance",
              "  (e.g. one wide drawer with two handles) — list all of them if so.",
              f'  FINAL ANSWER FORMAT:  FINAL: {tgt_c} #<id>[, #<id> ...]']
        open(os.path.join(d, "candidates.txt"), "w").write("\n".join(L))

        # ---- cands.npz: store only the target/host masks, so the lift stage can take
        #      them directly without re-running the segmenter ----
        store, keys = {}, {}
        for c in [x for x in (tgt_c, host_c) if x and x in cands]:
            keys[c] = []
            for i, q in enumerate(cands[c]):
                k = f"{c}|{i}"
                store[k] = q["f"].astype(np.int32)
                keys[c].append(k)
        store["_shape"] = np.array([Himg, Wimg], np.int32)
        np.savez_compressed(os.path.join(d, "cands.npz"), **store)

        json.dump(dict(
            q=qi, visit=v, desc_id=did, text=p["text"], parse=p,
            frame=dict(video=vid, fid=fid, W=Wimg, H=Himg),
            framesel=fsdiag, concepts=concepts, roles=roles,
            candidates={c: [{k: q[k] for k in ("x0", "x1", "y0", "y1", "cx", "cy",
                                               "npix", "area_pct", "score")}
                            for q in cands[c]] for c in concepts},
            mask_keys=keys, geom_pick=geom, concept_fallback=fb,
            cfg=dict(stride=args.stride, det_th=args.det_th, nms=args.nms,
                     framesel="disc3", topk=args.topk, fallback=bool(args.fallback)),
        ), open(os.path.join(d, "meta.json"), "w"), indent=1, ensure_ascii=False)

        # ---------------- candidates.png (no ground truth shown) ----------------
        if args.viz:
            n = len(concepts)
            fig, axs = plt.subplots(1, n + 1, figsize=(5.8 * (n + 1), 8.0))
            axs = np.atleast_1d(axs)
            axs[0].imshow(rgb0); axs[0].set_title("selected frame", fontsize=12)
            axs[0].axis("off")
            for k, c in enumerate(concepts):
                ax = axs[k + 1]; ax.imshow(rgb0)
                for i, q in enumerate(cands[c][:args.max_list]):
                    col = COLORS[i % len(COLORS)] / 255.0
                    ax.add_patch(mp.Rectangle((q["x0"], q["y0"]), q["x1"] - q["x0"],
                                              q["y1"] - q["y0"], fill=False, ec=col, lw=1.6))
                    ax.text(q["x0"] + 3, max(q["y0"] - 6, 14),
                            f"#{i} s{q['score']:.2f} {q['area_pct']:.1f}%", color=col,
                            fontsize=8, weight="bold",
                            bbox=dict(fc="black", alpha=.65, pad=1.0, ec="none"))
                ax.set_title(f"{c}  ({roles[c]})  {len(cands[c])} candidates", fontsize=12)
                ax.axis("off")
            fig.suptitle(f'q{qi:03d}  "{p["text"]}"\n{v}/{vid}/{fid}   (no GT shown)',
                         fontsize=13)
            fig.tight_layout()
            fig.savefig(os.path.join(d, "candidates.png"), dpi=80, bbox_inches="tight")
            plt.close(fig)

        ndone += 1
        el = (time.time() - t0) / 60
        print(f"  [q{qi:03d}] {v} {did[:8]} frame={vid}/{fid} [{level}] "
              f"cands={ {c: len(cands[c]) for c in concepts} } geom->{geom['target']}  "
              f"({ndone}/{len(todo)-nskip}, {el:.1f}min)", flush=True)

    print(f"\n[shard {args.shard}] generated {ndone} - skipped (already present) {nskip} - "
          f"failed {nfail} - {(time.time()-t0)/60:.1f} min -> {args.out}/")


if __name__ == "__main__":
    main()
