# Method Detail

Stage-by-stage description of the training-free instruction-level grounding pipeline.
The high-level argument is in [`../REPORT.md`](../REPORT.md) §3; this document covers the
parts that only matter if you intend to read the code or reimplement it.

```
instruction --> [S0] parse --> constraint graph
RGB frames  --> [S1] frame selection + open-vocabulary segmentation
                     --> [S2] symbolic candidate table
                              --> [S3] one text-only inference --> instance ids
                                       --> [S4] projection + refinement --> 3D mask
```

Code for each stage lives under the correspondingly named directory in
[`../code/task2/`](../code/task2/).

---

## S0 — Parsing the instruction into a constraint graph

Implementation: [`../code/task2/s0_parse/parse.py`](../code/task2/s0_parse/parse.py).

Output schema, one JSON object per instruction:

```
target      { concept, host }
entities[]  { name, role, instanceable }        role ∈ target | host | container | landmark
relations[] { rel, a, b }                       rel  ∈ contains | on_top | has_on_top |
                                                       next_to | near | left_of | right_of |
                                                       above | under | behind | in_front_of |
                                                       between
select[]    { on, axis, value, index, from }    axis ∈ vertical | horizontal | ordinal
residual                                        anything that could not be grounded
```

Four schema decisions, each fixing a concrete failure of the previous iteration. All four are
**missing-field** problems rather than parse-quality problems:

**`target.concept` is the single source of truth.** The earlier schema had a generic
`target` ("handle") while the precise concept actually fed to the segmenter
("drawer handle") lived in a different file. Two sources of truth for the same quantity is
a bug generator.

**`target.host` is produced by language understanding, not derived.** Deriving the host by
stripping the last word gives `"power button" -> "power"`, which is not an object. The real
host (the remote control) is stated in the instruction; asking for it directly needs no
exception list.

**Roles and relations are separate fields.** A single `anchor` field previously served two
incompatible purposes — "inside what does the ordinal count" (the container) and "what should
be visible in the same frame" (the framing reference). A table lamp is a good reference and a
bad container: the switch is not on the lamp. Splitting into `entities[].role` and
`relations[].rel` resolves this.

**`instanceable` marks nouns that are not countable objects in an image.** "Wall" segments to
something covering everything. This is a general property, not a special case for one word.

Coverage measured over all 445 raw instructions is ≈94% expressible, with an honest ≈6%
residual (room-level or semantic localisation 23, colour-unique ~3, egocentric 1). **Colour is
deliberately not a schema field**: colour appears in 18% of instructions but is the unique
disambiguating cue in under 1% — measured, not assumed.

Two properties carried over from the previous iteration and verified: a closed enumeration
plus constrained decoding gives **zero parse failures**, where free generation fails 50% of
the time. And the `affordance` field was **removed** — it is a ground-truth label, which the
parse stage cannot and should not see.

---

## S1 — Frame selection

Implementation: [`../code/task2/s1_perception/framesel.py`](../code/task2/s1_perception/framesel.py).

The question is **"which frame can answer this question"**, not "which frame looks best".
This distinction was forced by measurement: under the earlier criterion (all concepts
detected + largest target area), 6 of 10 test instructions selected an unusable frame — the
ground truth had no point in the chosen frame at all, or the landmark was unusable — while
the 3 instructions whose frame selection succeeded were reasoned correctly 3 for 3.

Three specific defects, each of which showed up in measurement:

- **"detected" ≠ "usable".** One radiator was detected at 51 px hugging the image border
  (0.35% area); using it as a spatial reference is guaranteed to be wrong. One wall cabinet
  showed only 181 px, with its handle outside the frame entirely.
- **"largest target area" selects the frame containing the target nearest the camera**, which
  has nothing to do with the target being referred to.
- **The criterion ignored the instruction text**, so instructions sharing a concept
  necessarily selected the same frame — and each such group necessarily contained misses.

### Hard conditions (a frame failing any of these is discarded)

Every one of these is **ground-truth-free**, using only boxes, areas, confidences, and image
borders.

| | Condition |
|---|---|
| H1 | at least one target detection |
| H2 | the landmark is *usable*: area ≥ threshold, touching at most one image border, score ≥ threshold |
| H3 | every relation is *decidable* in this frame (see below) |
| H4 | after relation filtering, the number of container candidates is in `[1, max]` — zero means unsolvable, too many means the relations did no filtering at all |

Decidability rules for H3:

- **Directional** (`left_of` / `right_of` / `above` / `under`): separation along that axis
  must exceed a threshold. When two boxes almost coincide on an axis, "left" and "right" have
  no meaning on that axis.
- **`has_on_top` / `on_top`**: some candidate must satisfy `|b.y1 - a.y0| < 0.15 * a.height`.
- **`contains`**: some candidate must genuinely fall inside another.
- **`in_front_of` / `behind` are marked undecidable in 2D and take no part in filtering.**
  An earlier version proxied depth by x-interval overlap, which excluded the correct cabinet
  on a test instruction. There is no reliable single-frame 2D proxy for a depth relation, and
  filtering on a bad proxy only injects systematic error.

### Soft scoring, graded relaxation, and top-K

Frames passing the hard conditions are ranked by

```
score = discriminative margin x ordering-axis separation x set completeness^2 x log1p(target area)
```

The hard conditions can reject **every** frame for an instruction. Rather than degrading
silently, the constraints are relaxed in graded levels (L0 strict → L3 loose) and **the level
at which selection succeeded is recorded**, so "how hard was this instruction" becomes a
readable signal.

Selection returns a **ranked top-K**, not a single frame. Downstream may take only the first
(the single-frame configuration) or use the rest for multi-frame voting — and in testing there
were instructions where a different frame was solvable and the top one was not.

### Open-vocabulary segmentation

Implementation: [`../code/task2/s1_perception/sam3_util.py`](../code/task2/s1_perception/sam3_util.py)
and [`run_sam3.py`](../code/task2/s1_perception/run_sam3.py).

One 860 M open-vocabulary model performs detection and segmentation in a single pass, queried
per concept name from the parse. **Results are cached by `(scene, concept)`**, so multiple
instructions in the same room reuse the same detections — this is the structural efficiency
property in [`../REPORT.md`](../REPORT.md) §4, not an implementation optimisation.

The wrapper is deliberately dependency-free (it imports nothing from the rest of the project)
because the third-party baseline repository ships a `utils` package that **shadows** the
project's own; see [`../code/README.md`](../code/README.md).

---

## S2 — The symbolic candidate table

Implementation: [`../code/task2/s2_candidates/dump_candidates.py`](../code/task2/s2_candidates/dump_candidates.py).

Per instruction, this produces a directory containing:

| File | Contents |
|---|---|
| `task.md` | the instruction, the parse, and the frame-selection diagnostics |
| `candidates.txt` | **the only thing the reasoning stage reads** |
| `candidates.png` | the same content visualised, for human review only |
| `meta.json` | machine-readable: frame id, candidate geometry, frame-selection diagnostics |
| `cands.npz` | the target and host masks, so the lift stage need not re-run segmentation |

The table itself contains, per detection: `id, xmin, xmax, ymin, ymax, cx, cy, area%, score`,
with ids restarting from 0 within each class, plus a **containment table** listing which target
ids fall inside each host's mask. Containment rows tagged `[via bbox]` fell back to
bounding-box containment because the mask test found nothing, and are marked as less reliable.

Three isolation properties that make the evaluation honest:

- **The generation stage never reads ground truth.** It does not import the annotation loader,
  and no answer file can appear in the directory. Scoring is a separate step run afterwards
  ([`../code/task2/eval/score_cot.py`](../code/task2/eval/score_cot.py)).
- **Sharding is by visit, not by instruction**, because the segmentation cache is per visit.
- A hard-coded geometric solution is recorded in `meta.json` as a **control arm** but is
  deliberately **never written into `candidates.txt`** — otherwise the reasoning would be
  anchored by it and the two arms would no longer be independent.

---

## S3 — One text-only inference

Rules: [`reasoning_rules.md`](reasoning_rules.md).
Scripted arm: [`../code/task2/s3_reasoning/qwen_cot.py`](../code/task2/s3_reasoning/qwen_cot.py).

Input is `candidates.txt` and nothing else — no image, no ground truth. Output is a JSON
object: the selected ids, a confidence tier, a criterion type, and a one-sentence note naming
the decisive evidence.

The criterion type is not decoration. It is what made the model-scale ablation in
[`../REPORT.md`](../REPORT.md) §7 legible: the frontier model used 26 distinct criteria while
the 9B model used 7 and forced 45 of 99 questions into a single "ordering constraint"
template, never once using the `merged_host` label. The confidence tier is what made the
stratified multi-frame analysis in §6.2 possible.

**How the reported results were produced** is stated in
[`../REPORT.md`](../REPORT.md) §3 and in the repository README: interactively, one instruction
at a time, across 14 batches. The scripted arm exists to price that choice, not to reproduce it.

---

## S4 — Projection and refinement

### Projection (single frame)

Implementation: [`../code/task2/s4_lift/lift.py`](../code/task2/s4_lift/lift.py).

```
u, v, visible = project(xyz, K, pose, depth, vis_thres)
pred_3d       = visible AND pred_mask_2d[v, u]
```

The point cloud is projected into the selected frame, visibility is resolved against depth,
and points landing inside the predicted mask become the 3D prediction. The contrast with the
baseline is that it accumulates 50 frames unconditionally before thresholding, whereas this is
**one frame**.

The same file also implements three arms sharing one lift path, differing only in the 2D
selection: the reasoning answer (the main result), the hard-coded geometric solution (the
control), and an **oracle**.

> **The oracle definition, and how the first version was wrong.** The first implementation
> took `r = |GT_projected ∩ candidate| / |GT_projected|`, maximised it, and allowed only one
> candidate. Two errors: (1) that is **recall**-oriented while AP50 measures precision — the
> candidate covering the most ground truth is usually the largest mask, which has the *worst*
> precision, so this systematically picked the option most harmful to AP50; (2) allowing only
> one candidate while the reasoning arm may select several meant the "upper bound" had a lower
> AR50 (40.3) than the thing it was supposed to bound (51.9). An upper bound below its own
> subject is conclusive proof of a broken definition.
>
> The broken version returned oracle AP50 = 29.9 = the actual score, which led to the
> incorrect conclusion "disambiguation is already saturated". The corrected version —
> **enumerate every candidate, run a full lift for each, take the highest 3D precision** —
> returns 21.3, which reverses the conclusion into the one that shaped the rest of the
> project ([`../REPORT.md`](../REPORT.md) §5.2).

### Refinement sweep

Implementation: [`../code/task2/s4_lift/refine_sweep.py`](../code/task2/s4_lift/refine_sweep.py).

Everything here operates **after the instance is selected**: no re-segmentation, no
regenerated candidates, no additional reasoning.

**2D side, before projection**

- **E — erode the mask by k pixels.** The segmenter's mask edge is not clean, and the rim
  drags background points in during projection. Shrinking inward removes precisely the ring
  most likely to bleed through.

**3D side, after projection**

- **C1 — largest connected component.** A radius-based connectivity test keeping only the
  largest cluster; targets "bled into a neighbouring object".
- **C2 — depth front layer.** Keep only the frontmost layer in camera-frame z; targets
  "bled through to the back surface" (the handle is in front, the cabinet face behind).
- **C3 — physical radius crop.** Keep points within r metres of the medoid; targets
  "spread too wide overall".

The script sweeps the Cartesian product of `(erosion × 3D combination)` and reports official
AP50 / AR50 for each. Two implementation notes:

- **The projection is computed once per instruction**, since it does not depend on the mask.
  Different erosion radii and post-processing combinations are lookups and filters over that
  result, so 20+ combinations cost almost nothing extra.
- **C3 uses a physical radius rather than "keep the nearest N points"** on purpose. Any N
  would have to come from the ground-truth point count (reading the answer) or from a prior
  table keyed by affordance class (also a ground-truth attribute). A radius is pure geometry.

**The chosen configuration is erosion 5 px + C2**, at AP50 29.9. Two facts about it:

- Splitting the +10.4 gain: **2D edge accounts for +9.2, depth bleed-through for +1.2.**
- The C2 band is an absolute distance (`z ≤ median(z) + 5 cm`) rather than a quantile, because
  handle thickness is a fixed physical quantity. **The median must be taken over the target
  point set**; taking it over all visible points in the scene shreds points inside the mask and
  drops the single-frame baseline from 28.7 to 21.5. That bug was caught only because the old
  baseline was retained as a control.

This configuration is cross-validated: it yields 29.9 along two independent code paths
(`refine_sweep.py` and `multiframe_lift.py`).

### Multi-frame parallax voting

Implementation: [`../code/task2/s4_lift/multiframe_lift.py`](../code/task2/s4_lift/multiframe_lift.py).

**This solves a different problem from refinement.** Refinement removes points that *look*
suspicious (the edge ring, the depth back-peak) using priors available within a single frame.
Multi-frame uses **parallax as evidence** — something a single frame cannot provide in
principle. Genuine handle points hit the mask from many viewpoints; bleed-through points on
the cabinet face fall outside it after two or three degrees of rotation.

**The reasoning is never re-run.** Instance identity is carried across frames by 3D position,
not by re-inference:

```
1. lift the top-1 frame's reasoning result into a seed point cloud
2. run the segmenter once per remaining frame (same concept)
3. per frame, take the candidate with the largest 3D overlap with the seed
   = the same instance as seen in that frame
4. accumulate its 3D points, then threshold by relative peak
```

The relative-peak threshold follows the baseline's convention exactly:
`normalize(acc / n_views) > th` applied **per 3D point**, meaning "this point received at
least th of the scene-wide peak vote" — **not** "th of the frames hit it". That reading of the
baseline is only obtainable from its code.

Frames come from the `framesel.topk` already stored in `meta.json` — the top-8 that already
passed the hard conditions, which is both higher quality than global sampling and already
computed. Frame 0 is the frame already in use, whose masks are cached, so it does not need
re-segmenting.

Cost: 445 instructions × at most 7 new frames, deduplicated by
`(visit, video, frame, concept)`, gives roughly 2000–2500 segmentation calls — about 15
minutes on one GPU.

**Threshold selection is 0.7, not the AP50-maximising 0.9.** th0.9 buys 0.7 more AP50 while
costing 1.6 AP25 and 5.0 AR50 and leaving a median of 23 points. Every tier is reported in
[`../results/main_table.md`](../results/main_table.md); picking the maximum-AP50 tier without
looking at AR would be exactly the failure mode that
[`metrics_and_cost.md`](metrics_and_cost.md) §1 warns about.

---

## Scoring and per-question diagnosis

Implementation: [`../code/task2/eval/score_cot.py`](../code/task2/eval/score_cot.py).

Ground truth enters here and **only** here, and only for questions that already have a fixed
answer. Questions without one are not touched, so no answer-revealing figure can be generated
ahead of time.

The 2D hit criterion is defined identically to the pool-coverage statistic, so the two never
disagree: project the ground-truth cloud into the selected frame; a candidate whose mask
covers at least 5% of the projected GT points counts as a hit.

```
correct     at least one selected candidate is a hit      <- main metric
pool_ok     some candidate in the pool is a hit           <- ceiling (64.3%)
miss_pick   pool_ok but the wrong one was selected        <- purely a disambiguation error
miss_pool   no candidate in the pool hits                 <- failed at generation, not reasoning
```

Separating `miss_pick` from `miss_pool` is what makes the reasoning stage's own accuracy
(89.1% in-pool disambiguation) separable from candidate-generation coverage, and is why the
model-scale ablation can attribute its loss correctly.

The per-question figure draws all candidates as thin coloured boxes, the **selected** one as a
thick red box with a translucent mask, the candidate **actually containing ground truth** as a
thick green box, and the projected GT points in green. When they coincide both are drawn (red
inside, green outside) rather than blended into a third colour, which had proved almost
impossible to read.
