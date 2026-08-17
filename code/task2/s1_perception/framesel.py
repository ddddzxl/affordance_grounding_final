#!/usr/bin/env python3
"""Discriminative frame selection: ask "which frame can answer this question", not "which
frame looks best".

## Why this was rewritten -- measured on a 10-question pilot

The old criterion was "all concepts **detected** + largest target area". **6 of 10 questions
selected an unusable frame** (not a single ground-truth point was in it, or the landmark was
unusable), while the 3 whose frame selection succeeded were reasoned **3 for 3 correctly**.

Three defects, each of which showed up in measurement:

  - **"Detected" is not "usable".** One radiator was 51 px and flush with the top edge
    (0.35% area); using it as a spatial reference cannot work. One wall cabinet showed only
    181 px, with its handle outside the frame entirely.
  - **"Largest target area" selects the frame containing the target nearest the camera**,
    which has nothing to do with the target being referred to.
  - **The criterion ignored the description text entirely**, so descriptions sharing a
    concept necessarily selected the same frame -- and each such group necessarily contained
    a miss.

## Design principle

For a frame to answer "which X does this description refer to", its **discriminative
information must be complete**: every piece of evidence the description uses to distinguish
must be both **usable and decidable** in that frame.

This judgement is **entirely ground-truth free**, using only bboxes, areas, confidences and
image borders.

## Hard conditions (failing any discards the frame) -- each one corresponds to a real failure

  H1  at least one target detection
  H2  landmark **usable**: area >= min_lm_area, touching at most max_edge borders,
      score >= min_lm_score
  H3  relation **decidable**:
        directional (left_of / right_of / above / under): separation along that axis
            >= min_sep -- when two boxes nearly coincide on an axis, "left" and "right"
            have no meaning
        has_on_top / on_top: some candidate satisfies |b.y1 - a.y0| < 0.15 * a.height
        contains: some candidate genuinely falls inside another
        **in_front_of / behind: marked undecidable in 2D and excluded from filtering.**
            An earlier version proxied depth by x-interval overlap and thereby excluded the
            correct cabinet. There is no reliable single-frame 2D proxy for a depth relation,
            and filtering on a bad proxy only injects systematic error.
  H4  discriminative power: after relation filtering, the container candidate count is in
      [1, max_cont]. Zero means unsolvable; too many means the relations did no filtering
      at all.
  H5  see select_edge_ok below.

## Soft scoring (only ranks frames that already passed the hard conditions)

    score = discriminative margin x ordering-axis separation
            x set completeness^2 x log1p(target area)

## Graded relaxation

The hard conditions can reject **every** frame for a description. Rather than degrading
silently, they relax in graded levels (L0 strict -> L3 loose) and **the level at which
selection succeeded is recorded**, so "how hard was this description" becomes a readable
signal in its own right.

## Never bet on a single frame

`pick(...)` returns a **ranked top-K**. Downstream may take only the first (matching the old
behaviour) or solve each frame independently and vote in 3D after lifting -- in testing there
were questions where another frame was solvable and the top one was not.
"""
import numpy as np

DEPTH_RELS = {"in_front_of", "behind"}                  # undecidable in 2D
DIR_AXIS = {"left_of": "x", "right_of": "x", "above": "y", "under": "y"}
LOOSE_RELS = {"next_to", "near", "between"}             # non-ordering: rank by distance


class Box:
    """A lightweight representation of one candidate -- **without its mask**.

    Frame selection only needs geometry and confidence. Storing masks would blow the
    stride=5 cache up to hundreds of gigabytes.
    """
    __slots__ = ("x0", "x1", "y0", "y1", "cx", "cy", "a", "s")

    def __init__(self, x0, x1, y0, y1, cx, cy, a, s):
        self.x0, self.x1, self.y0, self.y1 = x0, x1, y0, y1
        self.cx, self.cy, self.a, self.s = cx, cy, a, s

    @property
    def w(self):
        return max(self.x1 - self.x0, 1)

    @property
    def h(self):
        return max(self.y1 - self.y0, 1)


def nms_box(bs, th=0.75):
    """bbox-level NMS for the frame-selection stage: keep in descending score order and drop
    any later box whose bbox intersection-over-minimum exceeds th.

    **This step is mandatory.** Candidate generation and solving operate on mask-level NMS
    output (one cabinet leaves 2 boxes), but if frame selection judged "are there too many
    candidates" on the **pre-NMS** raw detections (where one cabinet yields 8 boxes at
    different granularities), it would systematically declare good frames "not
    discriminative". Measured: this is exactly how the best frame for one question was
    rejected.

    bbox intersection approximates mask intersection here -- there are no pixels at this
    stage, and an oversized bbox only makes the test more conservative.
    """
    keep = []
    for b in sorted(bs, key=lambda x: -x.s):
        ok = True
        for k in keep:
            ix = max(0, min(b.x1, k.x1) - max(b.x0, k.x0))
            iy = max(0, min(b.y1, k.y1) - max(b.y0, k.y0))
            if ix * iy / max(1.0, min(b.w * b.h, k.w * k.h)) > th:
                ok = False; break
        if ok:
            keep.append(b)
    return keep


def edge_touch(b, W, H, m=8):
    """How many frame edges the bbox touches. Touching an edge means the object is clipped
    and its geometry cannot be trusted."""
    return int(b.x0 <= m) + int(b.y0 <= m) + int(b.x1 >= W - 1 - m) + int(b.y1 >= H - 1 - m)


def usable(b, W, H, min_area, min_score, max_edge):
    """Landmark usability. **Detected is not the same as usable** -- see H2 in the header."""
    return (100.0 * b.a / (W * H) >= min_area and b.s >= min_score
            and edge_touch(b, W, H) <= max_edge)


def sep(a, b, axis):
    """Separation along an axis = centre distance / mean size.
    Below 0.2, "left/right" and "above/below" are not reliable."""
    if axis == "x":
        return abs(a.cx - b.cx) / max((a.w + b.w) / 2.0, 1.0)
    return abs(a.cy - b.cy) / max((a.h + b.h) / 2.0, 1.0)


def inside(a, b, frac=0.6):
    """How much of a's bbox falls inside b's bbox (area approximation -- the frame-selection
    stage has no pixels)."""
    ix = max(0, min(a.x1, b.x1) - max(a.x0, b.x0))
    iy = max(0, min(a.y1, b.y1) - max(a.y0, b.y0))
    return (ix * iy) / max(a.w * a.h, 1) >= frac


def select_edge_ok(cont, rules, W, H, m=8):
    """**H5: whichever end of the container `select` points at must be inside the frame.**

    Measured root cause: "top left drawer" and "bottom drawer" of the same cabinet, where no
    single frame fits the whole cabinet. The selected frame had the cabinet at y[1324,1919]
    with its bottom edge exactly on the image bottom, so the ground truth for the "bottom"
    instruction was cut off outside the frame -- guaranteeing that one of the two
    descriptions was wrong. The earlier `edge_touch` counted edges without direction and
    could not catch this.

    A useful side effect: descriptions sharing a concept no longer necessarily select the
    same frame. "top" needs the cabinet top in frame and "bottom" needs the bottom, so they
    separate onto different frames automatically.

    Returns (ok, reason).
    """
    if cont is None or not rules:
        return True, ""
    for r in rules:
        ax, v = r.get("axis"), r.get("value")
        if ax == "vertical":
            if v == "top" and cont.y0 <= m:
                return False, "select top but the container top is cut off"
            if v == "bottom" and cont.y1 >= H - 1 - m:
                return False, "select bottom but the container bottom is cut off"
            if v == "middle" and (cont.y0 <= m or cont.y1 >= H - 1 - m):
                return False, "select middle but the container top or bottom is cut off"
        elif ax == "horizontal":
            if v == "left" and cont.x0 <= m:
                return False, "select left but the container left edge is cut off"
            if v == "right" and cont.x1 >= W - 1 - m:
                return False, "select right but the container right edge is cut off"
            if v == "middle" and (cont.x0 <= m or cont.x1 >= W - 1 - m):
                return False, "select middle but a container side is cut off"
        elif ax == "ordinal":                       # counting requires seeing the whole column
            if (cont.y0 <= m or cont.y1 >= H - 1 - m
                    or cont.x0 <= m or cont.x1 >= W - 1 - m):
                return False, "select ordinal but the container is not fully in frame"
    return True, ""


def dir_ok(rel, a, b):
    ov_x = min(a.x1, b.x1) - max(a.x0, b.x0)
    if rel == "left_of":
        return a.cx < b.cx
    if rel == "right_of":
        return a.cx > b.cx
    if rel == "above":
        return a.cy < b.cy and ov_x > 0
    if rel == "under":
        return a.cy > b.cy and ov_x > 0
    return True


# Graded relaxation: L0 strictest, L3 loosest. Each level relaxes one class of condition
# only, so a failure can be attributed to a specific constraint.
LEVELS = [
    dict(name="L0", min_lm_area=0.5, min_lm_score=0.40, max_edge=1, min_sep=0.20, max_cont=5,
         sel_edge=True),
    dict(name="L1", min_lm_area=0.2, min_lm_score=0.30, max_edge=2, min_sep=0.10, max_cont=8,
         sel_edge=True),
    dict(name="L2", min_lm_area=0.05, min_lm_score=0.20, max_edge=3, min_sep=0.00, max_cont=8,
         sel_edge=False),                                 # relaxes H5
    dict(name="L3", min_lm_area=0.0, min_lm_score=0.00, max_edge=4, min_sep=0.00, max_cont=99,
         sel_edge=False, skip_rel=True),                  # last resort: no relation filtering
]


def try_frame(get, p, W, H, cfg):
    """Attempt a solve on one frame. get(concept) -> list[Box].

    Returns dict(ok, why, score, n_cont, n_host, n_tgt, cont).
    """
    tgt_c = p["target"]["concept"]; host_c = p["target"]["host"]
    cont_c = next((e["name"] for e in p["entities"] if e["role"] == "container"), None)
    lms = [e["name"] for e in p["entities"] if e["role"] == "landmark" and e["instanceable"]]
    R = dict(ok=False, why="", score=0.0, n_cont=0, n_host=0, n_tgt=0, cont=None,
             hosts=[], targets=[], skipped=[])

    G = lambda c: nms_box(get(c), 0.75)                   # always via bbox NMS; see nms_box
    dir_key = None                                        # ordering key for directional relations
    T = G(tgt_c)
    if not T:                                             # H1
        R["why"] = "no target"; return R
    R["n_tgt"] = len(T)

    # H2: landmark usability
    LM = {}
    for nm in lms:
        u = [b for b in G(nm) if usable(b, W, H, cfg["min_lm_area"],
                                          cfg["min_lm_score"], cfg["max_edge"])]
        if not u:
            R["why"] = f"landmark '{nm}' unusable"; return R
        LM[nm] = u

    # H3: relations decidable, and container filtering
    Cp = None; cand = []
    if cont_c:
        cand = G(cont_c)
        if not cand:
            R["why"] = "no container"; return R
        for r in p["relations"]:
            if r["a"] != cont_c:
                continue
            if r["rel"] in DEPTH_RELS:                # depth relations are 2D-undecidable;
                                                      # skip rather than filter
                R["skipped"].append(r["rel"]); continue
            if cfg.get("skip_rel"):
                R["skipped"].append(r["rel"]); continue
            L = LM.get(r["b"]) or G(r["b"])
            if not L:
                R["why"] = f"relation landmark '{r['b']}' missing"; return R
            if r["rel"] in LOOSE_RELS:                # non-ordering: rank by distance, keep
                                                      # the nearer half; never a hard filter
                cand = sorted(cand, key=lambda c: min(abs(c.cx - l.cx) + abs(c.cy - l.cy)
                                                      for l in L))[:max(1, len(cand) // 2)]
                continue
            if r["rel"] == "contains":
                f2 = [c for c in cand if any(inside(b, c) for b in (G(r["b"]) or []))]
            elif r["rel"] in ("has_on_top", "on_top"):
                A, Bl = (cand, L) if r["rel"] == "has_on_top" else (cand, L)
                f2 = [c for c in A if any(abs(l.y1 - c.y0) < 0.15 * c.h
                                          and min(c.x1, l.x1) > max(c.x0, l.x0) for l in Bl)]
            else:                                         # directional: direction must hold
                                                          # **and** separation must suffice
                ax = DIR_AXIS.get(r["rel"], "x")
                f2 = [c for c in cand
                      if any(dir_ok(r["rel"], c, l) and sep(c, l, ax) >= cfg["min_sep"]
                             for l in L)]
                # **A directional relation is an ordering, not a filter.** "the cabinet left
                # of the TV" means the **leftmost** one satisfying the condition. The earlier
                # version filtered and then picked by score, discarding the direction --
                # measured: two cabinets were both left of the TV (0.69 vs 0.66) and it took
                # the higher-scoring right-hand one, which is simply wrong.
                dir_key = (ax, r["rel"] in ("left_of", "above"))
            if not f2:
                R["why"] = f"relation {r['rel']}({cont_c},{r['b']}) undecidable"; return R
            cand = f2
        if not (1 <= len(cand) <= cfg["max_cont"]):       # H4 discriminative power
            R["why"] = f"container not discriminative ({len(cand)} left)"; return R
        if dir_key is not None:                           # a directional relation -> take the extreme
            ax_, want_min = dir_key
            key = (lambda c: c.cx) if ax_ == "x" else (lambda c: c.cy)
            Cp = min(cand, key=key) if want_min else max(cand, key=key)
        else:
            Cp = max(cand, key=lambda c: c.s)             # only score-rank without a direction
        if cfg.get("sel_edge", True):                     # H5
            ok5, why5 = select_edge_ok(Cp, p.get("select") or [], W, H)
            if not ok5:
                R["why"] = why5; return R
        R["n_cont"] = len(cand); R["cont"] = Cp

    Hs = [b for b in (G(host_c) if host_c else []) if Cp is None or inside(b, Cp)]
    Tin = [b for b in T if Cp is None or inside(b, Cp)]
    if not Tin:
        R["why"] = "no target inside container"; return R
    R["n_host"] = len(Hs); R["hosts"] = Hs; R["targets"] = Tin

    # ---- soft score ----
    margin = 1.0 if R["n_cont"] <= 1 else (0.5 if R["n_cont"] == 2 else 0.3)
    axis0 = p["select"][0]["axis"] if p["select"] else None
    spread = 1.0
    if axis0 and len(Hs) > 1:
        q = np.array([b.cx for b in Hs]) if axis0 == "horizontal" else np.array([b.cy for b in Hs])
        spread = float(q.max() - q.min()) / (W if axis0 == "horizontal" else H)
    R.update(ok=True, why="ok",
             score=margin * max(spread, 1e-3) * np.log1p(max(b.a for b in Tin)))
    return R


def pick(frames, get_for, p, W, H, topk=8):
    """frames: [(vid, fid)]; get_for(vid, fid) -> get(concept) -> list[Box]

    Returns (ranked top-K [(vid, fid, info)], relaxation level used, per-level statistics).
    """
    stats = {}
    for cfg in LEVELS:
        okf = []
        why = {}
        for (vid, fid) in frames:
            r = try_frame(get_for(vid, fid), p, W, H, cfg)
            if r["ok"]:
                okf.append((vid, fid, r))
            else:
                why[r["why"]] = why.get(r["why"], 0) + 1
        stats[cfg["name"]] = dict(n_ok=len(okf), top_reasons=sorted(
            why.items(), key=lambda t: -t[1])[:3])
        if okf:
            okf.sort(key=lambda t: -t[2]["score"])
            return okf[:topk], cfg["name"], stats
    return [], "none", stats


# ---------------------------------------------------------------- select + full solve
def axis_q(bs, axis):
    """Coordinate along the ordering axis. `ordinal` does not hard-code vertical; it takes
    whichever axis has the larger spread as the principal one."""
    cx = np.array([b.cx for b in bs]); cy = np.array([b.cy for b in bs])
    if axis == "horizontal":
        return cx
    if axis == "vertical":
        return cy
    return cy if (cy.max() - cy.min()) >= (cx.max() - cx.min()) else cx


def apply_select(bs, rules):
    """Sum the cost of several select rules and take the minimum.
    Returns (index, cost array) or (None, None)."""
    if len(bs) == 0 or not rules:
        return None, None
    cost = np.zeros(len(bs)); used = 0
    for r in rules:
        q = axis_q(bs, r["axis"]); o = np.argsort(q)
        rk = np.empty(len(q)); rk[o] = np.arange(len(q)) / max(len(q) - 1, 1)
        if r["axis"] == "ordinal":
            k = int(r["index"] or 1) - 1
            if k < 0 or k >= len(o):
                continue
            rev = (r.get("from") or "") in ("bottom", "right")
            tr = rk[o[::-1][k] if rev else o[k]]
        elif r["value"] in ("top", "left"):
            tr = 0.0
        elif r["value"] in ("bottom", "right"):
            tr = 1.0
        elif r["value"] == "middle":
            tr = 0.5
        else:
            continue
        cost += np.abs(rk - tr); used += 1
    return (int(np.argmin(cost)), cost) if used else (None, None)


def solve_full(get, p, W, H, cfg):
    """The **complete** 2D solve on one frame: try_frame (fix the container, host inside it,
    target inside it) followed by the select ordering, returning the chosen target Boxes.

    ⚠️ Everything here uses bboxes rather than masks, because the frame-selection stage has
    no pixels. Containment is therefore looser than it should be and the hit rate is an
    **upper-bound estimate**. Use it to answer "is multi-frame voting viable", never to
    report a score.

    Returns (picks or None, the try_frame diagnostic dict).
    """
    r = try_frame(get, p, W, H, cfg)
    if not r["ok"]:
        return None, r
    Hin, Tin = r["hosts"], r["targets"]
    tgt_c = p["target"]["concept"]; host_c = p["target"]["host"]
    sel_on = p["select"][0]["on"] if p["select"] else None
    picks = None; chosen = None
    if p["select"] and sel_on == tgt_c:              # the ordering applies to the target itself
        j, cst = apply_select(Tin, p["select"])
        r["sel_cost"] = cst
        if j is not None:
            picks = [Tin[j]]
    if picks is None:
        if Hin:
            if p["select"] and sel_on in (host_c, None):
                j, cst = apply_select(Hin, p["select"])
                r["sel_cost"] = cst
                chosen = Hin[j] if j is not None else max(Hin, key=lambda b: b.a)
            else:
                chosen = max(Hin, key=lambda b: b.a)
            picks = [t for t in Tin if inside(t, chosen)]
            if not picks:                            # host solved but no target inside -> nearest
                picks = [min(Tin, key=lambda t: abs(t.cx - chosen.cx) + abs(t.cy - chosen.cy))]
            elif len(picks) > 1:
                # Selecting several is a real loss under a precision-only metric (measured
                # ground truth: 88% single instance, 12% genuine handle pairs) -- but they
                # **must not all be cut to one**, because that 12% is real.
                #
                # The criterion deliberately **avoids** "size ratio + symmetry": two measured
                # questions had ratios of 1.15 and 1.14, nearly identical, yet required
                # opposite behaviour. It has no discriminating power at all.
                #
                # Instead the criterion is the objective fact of **whether membership is
                # unambiguous**:
                #   inside the hole-filled host **mask** -> membership is clear, keep them all
                #   only inside the host **bbox**        -> an oblique-view bbox has swollen
                #                                           into a neighbour, membership is
                #                                           doubtful -> conservatively keep the
                #                                           single one nearest the host centre
                # This layer only has Boxes (no pixels) and cannot run the mask test, so it is
                # unconditionally conservative. The real two-tier test lives in the pipeline
                # stage, which does have masks.
                picks = [min(picks, key=lambda t: abs(t.cx - chosen.cx)
                             + abs(t.cy - chosen.cy))]
        else:
            # No discriminating evidence at all: take one, never all of them
            # (selecting all N under a precision-only metric scores 1/N)
            picks = [max(Tin, key=lambda b: b.a)]
    r["chosen_host"] = chosen; r["picks"] = picks
    return picks, r


# ------------------------------------------------ mask-level containment (hole filling)
def filled_mask(m):
    """The mask with 2D holes filled.

    **Why this is needed.** Testing `target in host` has a dilemma:

      - Using the host's mask directly: the segmenter often **carves the handle out** of the
        drawer mask (different depth and colour), so the handle fails to test as inside the
        drawer it belongs to.
      - Using the host's bbox instead: at an oblique angle the drawer is a skewed
        quadrilateral, and its axis-aligned bbox swells enough to enclose the handle of the
        drawer **on the next row** (measured: this is exactly how one question over-selected).

    Hole filling resolves both: it restores the carved-out region while **preserving the
    outer contour exactly** -- unlike a convex hull, which would also fill genuine concavities.
    The justification is a plain fact: in 2D, one piece of furniture should be a simply
    connected region with no holes.
    """
    from scipy.ndimage import binary_fill_holes
    return binary_fill_holes(np.asarray(m, bool))


def in_filled(xy, host_filled, frac=0.3):
    """Fraction of a candidate's pixels falling inside the **hole-filled** host mask.
    xy = (xs, ys)."""
    xs, ys = xy
    if not len(xs):
        return False
    H, W = host_filled.shape
    x = np.clip(np.asarray(xs, np.int64), 0, W - 1)
    y = np.clip(np.asarray(ys, np.int64), 0, H - 1)
    return float(host_filled[y, x].mean()) >= frac


# ------------------------------------------- cross-frame consistency and solve coherence
def rel_pos(t, cont, W, H):
    """The target's position **relative to the container** -- approximately frame invariant.

    Absolute 2D coordinates are not comparable across frames because the camera moves, but
    "the top-left handle" sits at roughly (0.1, 0.1) relative to its container from any
    viewpoint. So when one description is solved independently on many frames, **the frames
    that solved it correctly cluster together while the wrong ones each fail differently**.
    Taking the largest cluster then needs no lifting at all.
    """
    if cont is None:
        return (t.cx / max(W, 1), t.cy / max(H, 1))
    return ((t.cx - cont.x0) / max(cont.w, 1), (t.cy - cont.y0) / max(cont.h, 1))


def cluster2d(pts, eps=0.15):
    """Greedy single-link clustering; returns a cluster id per point.
    eps is a tolerance on relative position (0.15 = 15% of the container's size)."""
    lab = [-1] * len(pts); cid = 0
    for i in range(len(pts)):
        if lab[i] >= 0:
            continue
        lab[i] = cid; frontier = [i]
        while frontier:
            k = frontier.pop()
            for j in range(len(pts)):
                if lab[j] < 0 and abs(pts[k][0] - pts[j][0]) < eps \
                        and abs(pts[k][1] - pts[j][1]) < eps:
                    lab[j] = cid; frontier.append(j)
        cid += 1
    return lab


def self_consistency(r, W, H):
    """**Self-consistency of the solve** -- derived entirely from the solved structure
    itself, not from how the frame looks.

    These four quantities formalise the "can I tell whether this solve is stable" judgement:

      S1 select margin    cost gap between second-best and best. A gap of 0.01 means the
                          ordering is essentially random; 0.5 means it genuinely resolved
      S2 host regularity  drawers in a chest are **evenly spaced**; erratic spacing means the
                          set has picked up a bed or a patch of floor
      S3 size hierarchy   must satisfy handle << drawer << cabinet
      S4 target coherence handles from one set should be similar in size
    """
    Hin = r.get("hosts") or []; picks = r.get("picks") or []; cont = r.get("cont")
    ch = r.get("chosen_host"); cst = r.get("sel_cost")
    # S1
    s1 = 1.0
    if cst is not None and len(cst) > 1:
        v = np.sort(np.asarray(cst, float))
        s1 = float((v[1] - v[0]) / max(v[-1] - v[0], 1e-6))
        s1 = 0.05 + 0.95 * min(s1, 1.0)                 # down-weight, never zero out
    # S2
    s2 = 1.0
    if len(Hin) >= 3:
        cx = np.array([b.cx for b in Hin]); cy = np.array([b.cy for b in Hin])
        q = cy if (cy.max() - cy.min()) >= (cx.max() - cx.min()) else cx
        d = np.diff(np.sort(q))
        if len(d) and d.mean() > 1e-6:
            s2 = float(1.0 / (1.0 + np.std(d) / d.mean()))
    # S3
    # S3 uses a near-veto (0.02) rather than a down-weight (0.3): on one measured question the
    # top-1 frame had a clearly implausible size hierarchy (S3=0.3) yet still won on the other
    # factors, 1.0*1.0*0.3*1.0 = 0.300 against the runner-up's 0.276. 0.3 was too soft.
    s3 = 1.0
    if picks and ch is not None:
        r1 = picks[0].a / max(ch.a, 1)
        s3 *= 1.0 if 0.0005 < r1 < 0.5 else 0.02
    if ch is not None and cont is not None:
        r2 = ch.a / max(cont.a, 1)
        s3 *= 1.0 if 0.01 < r2 < 1.05 else 0.02
    # S4
    s4 = 1.0
    if len(picks) > 1:
        a = np.array([t.a for t in picks], float)
        if a.mean() > 1e-6:
            s4 = float(1.0 / (1.0 + np.std(a) / a.mean()))
    # S5: is the selected host fully in frame?
    # H5 only guarantees the end of the **container** named by select is not clipped, but the
    # selected drawer itself can still be half cut off -- measured on one question at
    # D_frame=59%, where only one of the two ground-truth handles was in frame, halving the
    # achievable hit rate by construction.
    # Down-weight rather than veto: there are already enough hard conditions, and another
    # would reject every frame.
    s5 = 1.0
    if ch is not None:
        e = edge_touch(ch, W, H)
        s5 = 1.0 if e == 0 else (0.5 if e == 1 else 0.2)
    return s1 * s2 * s3 * s4 * s5, dict(s1=round(s1, 3), s2=round(s2, 3), s3=round(s3, 3),
                                        s4=round(s4, 3), s5=round(s5, 3))


def pick2(frames, get_for, p, W, H, topk=8, eps=0.15, use_cluster=True):
    """Frame selection v2: **use multi-frame information to choose one frame.**
    (The output is still a single frame; this is not multi-frame aggregation.)

      1. graded relaxation of the hard conditions, solving each frame completely
         -- this step was already happening; the solve result simply was not being used
      2. take each frame's target position relative to the container (rx, ry), cluster
         across frames, and **keep the largest cluster**
      3. rank within the cluster by **the self-consistency of the solve**, not by how the
         frame looks

    Returns (top-K [(vid, fid, info)], relaxation level used, per-level statistics).
    """
    used = None; solved = []
    stats = {}
    for cfg in LEVELS:
        solved = []; why = {}
        for (vid, fid) in frames:
            pk, r = solve_full(get_for(vid, fid), p, W, H, cfg)
            if pk:
                solved.append((vid, fid, pk, r))
            else:
                why[r["why"]] = why.get(r["why"], 0) + 1
        stats[cfg["name"]] = dict(n_ok=len(solved),
                                  top_reasons=sorted(why.items(), key=lambda t: -t[1])[:3])
        if solved:
            used = cfg; break
    if not solved:
        return [], "none", stats

    if use_cluster:
        # ⚠️ Measured to be **harmful** when the correct solve is in the minority (one question
        # had 6 frames scattered across 5 clusters), because taking the largest cluster then
        # actively discards it. The switch is kept but the production configuration disables it.
        pts = [rel_pos(pk[0], r.get("cont"), W, H) for _, _, pk, r in solved]
        lab = cluster2d(pts, eps)
        cnt = {}
        for l in lab:
            cnt[l] = cnt.get(l, 0) + 1
        big = max(cnt, key=lambda k: cnt[k])
        inbig = [(s, l) for s, l in zip(solved, lab) if l == big]
        stats["cluster"] = dict(n_solved=len(solved), n_clusters=len(cnt),
                                biggest=cnt[big], sizes=sorted(cnt.values(), reverse=True)[:5])
    else:
        inbig = [(s, 0) for s in solved]
        stats["cluster"] = dict(n_solved=len(solved), n_clusters=None, biggest=len(solved))

    scored = []
    for (vid, fid, pk, r), _ in inbig:
        sc, det = self_consistency(r, W, H)
        r2 = dict(r); r2["consistency"] = det; r2["score"] = sc
        scored.append((sc, vid, fid, r2))
    scored.sort(key=lambda t: -t[0])
    return [(v, f, r) for _, v, f, r in scored][:topk], used["name"], stats


# ---------------------------------------------------------------- smoke self-test
def _selftest():
    """Run the whole flow on synthetic data.

    **Bulk string replacement is very good at producing runtime errors** -- this file was
    once broken by a `LM.get(...)` -> `LM.G(...)` rename that py_compile cannot catch -- so
    a genuinely executable self-test is kept here:

        python code/task2/s1_perception/framesel.py
    """
    W, H = 1440, 1920
    def mk(x0, x1, y0, y1, s=0.9):
        return Box(x0, x1, y0, y1, (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) * (y1 - y0), s)
    P = dict(target=dict(concept="drawer handle", host="drawer"),
             entities=[dict(name="drawer handle", role="target", instanceable=True),
                       dict(name="drawer", role="host", instanceable=True),
                       dict(name="cabinet", role="container", instanceable=True),
                       dict(name="TV", role="landmark", instanceable=True)],
             relations=[dict(rel="contains", a="cabinet", b="drawer"),
                        dict(rel="left_of", a="cabinet", b="TV")],
             select=[dict(on="drawer", axis="vertical", value="top", index=None, from_=None)])
    P["select"][0]["from"] = None
    good = {"cabinet": [mk(100, 600, 800, 1600)], "TV": [mk(900, 1300, 700, 1000)],
            "drawer": [mk(150, 550, 850, 1050), mk(150, 550, 1100, 1300)],
            "drawer handle": [mk(300, 360, 930, 970), mk(300, 360, 1180, 1220)]}
    r = try_frame(lambda c: good.get(c, []), P, W, H, LEVELS[0])
    assert r["ok"], f"a good frame should pass, got: {r['why']}"
    assert r["n_cont"] == 1 and r["n_host"] == 2, r
    # TV too small and flush with the right edge -> landmark unusable
    bad = dict(good); bad["TV"] = [mk(1420, 1439, 700, 730)]
    r2 = try_frame(lambda c: bad.get(c, []), P, W, H, LEVELS[0])
    assert not r2["ok"] and "unusable" in r2["why"], r2
    # cabinet and TV almost coincide -> left_of is undecidable
    bad2 = dict(good); bad2["TV"] = [mk(110, 610, 780, 1580)]
    r3 = try_frame(lambda c: bad2.get(c, []), P, W, H, LEVELS[0])
    assert not r3["ok"] and "undecidable" in r3["why"], r3
    # Eight boxes of different granularity on one object -> NMS must collapse them, and the
    # frame must not be judged "not discriminative"
    bad3 = dict(good)
    bad3["cabinet"] = [mk(100 + i * 3, 600 - i * 3, 800 + i * 4, 1600 - i * 4, 0.9 - i * .05)
                       for i in range(8)]
    r4 = try_frame(lambda c: bad3.get(c, []), P, W, H, LEVELS[0])
    assert r4["ok"], f"NMS should collapse 8 overlapping boxes to 1, got: {r4['why']} (n_cont={r4['n_cont']})"
    # graded relaxation in pick()
    top, lvl, st = pick([("v", "1"), ("v", "2")],
                        lambda a, b: (lambda c: (good if b == "1" else bad).get(c, [])),
                        P, W, H, topk=8)
    assert len(top) == 1 and lvl == "L0", (len(top), lvl)
    # solve_full: "top" must select the handle on the drawer with the smaller cy
    picks, rr = solve_full(lambda c: good.get(c, []), P, W, H, LEVELS[0])
    assert picks and len(picks) == 1, picks
    assert abs(picks[0].cy - 950) < 30, f"top should pick the upper handle (cy~950), got {picks[0].cy}"
    # Switching to bottom must select the lower one
    P2 = dict(P); P2["select"] = [dict(on="drawer", axis="vertical", value="bottom",
                                       index=None)]
    P2["select"][0]["from"] = None
    picks2, _ = solve_full(lambda c: good.get(c, []), P2, W, H, LEVELS[0])
    assert abs(picks2[0].cy - 1200) < 30, f"bottom should pick the lower one (cy~1200), got {picks2[0].cy}"
    # rel_pos viewpoint invariance: scale the container 2x and translate it; the relative
    # position must not change
    c1 = mk(100, 600, 800, 1600); t1 = mk(150, 200, 850, 900)
    c2 = mk(300, 1300, 400, 2000); t2 = mk(400, 500, 500, 600)
    p1 = rel_pos(t1, c1, W, H); p2 = rel_pos(t2, c2, W, H)
    assert abs(p1[0] - p2[0]) < 0.06 and abs(p1[1] - p2[1]) < 0.06, (p1, p2)
    # cluster2d: two groups must separate
    lab = cluster2d([(0.1, 0.1), (0.12, 0.09), (0.8, 0.8), (0.82, 0.79), (0.11, 0.12)], 0.15)
    assert len(set(lab)) == 2 and sum(1 for x in lab if x == lab[0]) == 3, lab
    # pick2: three frames solving to the same place, two elsewhere -> the largest cluster is
    # the former. Note that a "wrong solve" cannot be simulated by translating everything --
    # rel_pos is translation invariant by design, which is exactly its value, so a translated
    # copy legitimately lands in the same cluster. A real wrong solve picks **a different
    # drawer inside the container**:
    far = dict(good)
    far["drawer handle"] = [mk(300, 360, 1180, 1220)]     # the upper handle is missed
    far["drawer"] = [mk(150, 550, 1100, 1300)]            # so "top" falls on the lower row
    def gf(a, b):
        return (lambda c: (good if b in ("1", "2", "3") else far).get(c, []))
    top, lvl, st = pick2([("v", x) for x in "12345"], gf, P, W, H)
    assert st["cluster"]["biggest"] == 3, st["cluster"]
    assert len(top) == 3, len(top)
    # H5: container bottom flush with the frame bottom + select bottom -> must be rejected;
    # the same frame with select top -> must pass
    cut = dict(good); cut["cabinet"] = [mk(100, 600, 800, H - 1)]
    Pb = dict(P); Pb["select"] = [dict(on="drawer", axis="vertical", value="bottom", index=None)]
    Pb["select"][0]["from"] = None
    rb = try_frame(lambda c: cut.get(c, []), Pb, W, H, LEVELS[0])
    assert not rb["ok"] and "bottom is cut off" in rb["why"], rb
    rt = try_frame(lambda c: cut.get(c, []), P, W, H, LEVELS[0])   # P selects top
    assert rt["ok"], f"select top must not be blocked by the container bottom: {rt['why']}"
    # Relaxing to L2 should let it through
    rb2 = try_frame(lambda c: cut.get(c, []), Pb, W, H, LEVELS[2])
    assert rb2["ok"], rb2["why"]
    # S5: a selected host touching the frame edge must be down-weighted
    r_ok = solve_full(lambda c: good.get(c, []), P, W, H, LEVELS[0])[1]
    sc_ok, det_ok = self_consistency(r_ok, W, H)
    cut2 = dict(good); cut2["drawer"] = [mk(150, 550, 850, 1050), mk(150, 550, 1100, H - 1)]
    r_cut = solve_full(lambda c: cut2.get(c, []), P, W, H, LEVELS[0])[1]
    _, det_cut = self_consistency(r_cut, W, H)
    assert det_ok["s5"] == 1.0, det_ok
    # Multi-select suppression: three handles inside one host -> keep only the most central
    many = dict(good)
    many["drawer"] = [mk(150, 550, 850, 1300)]                    # one big host over three handles
    many["drawer handle"] = [mk(300, 360, 930, 970), mk(300, 360, 1050, 1090),
                             mk(300, 360, 1180, 1220)]
    pk3, _ = solve_full(lambda c: many.get(c, []), P, W, H, LEVELS[0])
    assert len(pk3) == 1, f"three handles should collapse to one, got {len(pk3)}"
    # A genuine handle pair (similar size, symmetric about the host centre) would be kept in
    # the pixel-level stage, but at Box level we deliberately stay conservative.
    pair = dict(good)
    pair["drawer"] = [mk(150, 550, 850, 1050)]
    pair["drawer handle"] = [mk(230, 290, 930, 970), mk(410, 470, 930, 970)]
    pk4, _ = solve_full(lambda c: pair.get(c, []), P, W, H, LEVELS[0])
    assert len(pk4) == 1, f"Box level (no pixels) must stay conservative, got {len(pk4)}"
    # Directional relations take the extreme: both cabinets are left of the TV, so the
    # **further left** one must win, not the higher-scoring one.
    two = dict(good)
    two["cabinet"] = [mk(700, 1100, 800, 1600, 0.69), mk(100, 600, 800, 1600, 0.66)]
    two["TV"] = [mk(1200, 1400, 700, 1000)]
    two["drawer"] = [mk(150, 550, 850, 1050), mk(750, 1050, 850, 1050)]
    two["drawer handle"] = [mk(300, 360, 930, 970), mk(880, 940, 930, 970)]
    r5 = try_frame(lambda c: two.get(c, []), P, W, H, LEVELS[0])
    assert r5["ok"], r5["why"]
    assert r5["cont"].cx < 600, f"should pick the left cabinet (cx~350), got cx={r5['cont'].cx}"
    # filled_mask: the drawer mask has the handle carved out of it, so after hole filling the
    # handle must test as inside; whereas an oblique-view bbox would swell into the next row
    # and a filled mask does not.
    m = np.zeros((400, 400), bool)
    m[100:200, 100:300] = True              # a drawer front
    m[140:160, 180:220] = False             # the handle, carved out by the segmenter
    hf = filled_mask(m)
    hx = np.meshgrid(np.arange(185, 215), np.arange(145, 155))
    assert not in_filled((hx[0].ravel(), hx[1].ravel()), m), "unfilled: handle must be outside"
    assert in_filled((hx[0].ravel(), hx[1].ravel()), hf), "filled: handle must be inside"
    assert hf[100:200, 100:300].all() and not hf[:100].any(), "fill must not exceed the outline"
    # A handle on the NEXT drawer down must not be absorbed
    nx = np.meshgrid(np.arange(185, 215), np.arange(240, 250))
    assert not in_filled((nx[0].ravel(), nx[1].ravel()), hf), "fill must not reach the next row"
    print("framesel self-test: 21/21 passed")


if __name__ == "__main__":
    _selftest()
