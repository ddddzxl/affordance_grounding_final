# Replacing Fifty Visual Inferences with One Text-Only Inference

### A method study on instruction-level affordance grounding in SceneFun3D

> Independent research project · June–August 2026 · single GPU
>
> This report keeps the main line and the successful path, plus the ablations and failures
> that actually changed a decision. Every number traces back to a raw `.jsonl` under
> [`results/`](results/) and can be recomputed offline without the dataset.

---

## 1. Problem

Given a natural-language instruction and a scanned 3D room, output the 3D mask of the
**functional element** the instruction refers to:

> *"Open the top left drawer of the cabinet located to the left of the TV."*

The hard part is not finding the cabinet. It is deciding **which of the four identical
drawer handles on it** is meant. The instruction disambiguates with spatial language
("the top one", "the one to the left of the TV"), while the target itself is a few
centimetres across, occluded in most views, and often covers only a few dozen pixels.

SceneFun3D val split0: 30 rooms / 445 instructions. The official metrics are AP25 / AP50.

**One hidden property of this task**, used repeatedly below: it is **precision-only**.

---

## 2. Starting point: mainstream methods put the reasoning inside the pixels

Fun3DU (CVPR 2025) is the first dedicated method on this line, and the baseline I
reproduced myself. Reading its *code* rather than its paper is what revealed the actual
mechanism:

```
1. An LLM parses the instruction   -> functional-element name + context-object name
2. OWLv2 + SAM detect the context object in every frame, scored by a polar-coordinate
   KL divergence, keeping the top-50 frames
3. Molmo-7B does per-frame pointing on those 50 frames -- one 1920x1440 image read per frame
4. SAM turns each point into a mask; masks are accumulated unconditionally
5. After normalisation, a 0.7 threshold is applied and the result is lifted to a 3D mask
```

The `0.7` in step 5 is **not** "hit in 70% of the frames". It is a point-level *relative
peak* threshold — the accumulator is normalised by its maximum first, then thresholded.
The paper is vague here, and the literal reading yields a completely wrong model of the
baseline's behaviour.

**Reproduction result: AP50 13.71** (officially self-reported: 16.9). With two additions of
my own — a global fallback for the case where context detection returns nothing (+1.57) and
a learned row scorer (+1.12) — it reaches 16.85.

A relevant external data point: AffordBot (NeurIPS 2025) independently reproduces Fun3DU at
**12.6**. Two independent reproductions both land below the self-reported number, and my
13.71 already uses a *stronger* LLM prompt than the official one (the Molmo-side prompt is
verbatim identical). **The official 16.9 is most likely optimistic.**

### Key observation

In this pipeline, **the only place that actually looks at an image is Molmo's 50 pointing
calls**, and the question they answer is: *"in this image, which pixel is that drawer
handle?"*

But the disambiguating information the instruction demands — who is left of whom, who is
inside whom, which one is topmost — is **entirely geometric**. Compress a frame into
"every detection's box, area, confidence, and containment relations" and none of that
information is lost.

**So why read the image fifty times?**

---

## 3. Method: a symbolic bottleneck

```
instruction ---LLM parse---> constraint graph
                             (target concept / host / container / landmark /
                              spatial relations / ordering constraint)
                                     |
RGB frames of the room ---SAM3---> per-concept instance segmentation,
                                   cached by (scene, concept)
                                     |
                                     v
                   +-------------------------------------+
                   |  symbolic candidate table (text)    |  per detection:
                   |  + containment table                |  id / bbox / centre /
                   +-------------------------------------+  area% / confidence
                                     |
                              LLM inference x1        <- no image input
                                     |
                              selected instance id
                                     |
          project to point cloud + refinement
          (2D erosion / camera-frame front layer / multi-frame parallax voting)
                                     v
                                 3D mask
```

Three design points:

**(1) The reasoning input is symbols, not pixels.**
A candidate table looks like this (excerpt from a real instance):

```
target concept = "drawer handle"      host = 'drawer'
relation: contains(a='cabinet', b='drawer')
relation: has_on_top(a='cabinet', b='cup')
select  : on='drawer' axis=vertical value='top'

INSTANCES
  drawer handle   0   x[865,914]  y[1360,1412]  cx=889.0  cy=1387.3  0.071%  0.923
  drawer handle   1   x[870,919]  y[1167,1219]  cx=894.1  cy=1190.7  0.070%  0.921
  drawer          0   x[525,1184] y[1012,1368]  ...
  cabinet         3   x[471,1185] y[1011,1919]  17.458%  0.533
  cup             0   x[640,824]  y[787,959]    0.962%  0.968

CONTAINMENT
  drawer #0 contains drawer handle [1]
  drawer #1 contains drawer handle [0]
```

The resulting reasoning is fully readable: *three cups sit at y ≈ 800; only cabinet #3 lies
directly beneath them, so the target container is #3; it contains drawers 0/1/2/3, and
sorting them by cy, the topmost one contains handle 1.*

**(2) Perception is cached by (scene, concept), not by instruction.**
Multiple instructions in the same room share one set of detections. This is not an
engineering optimisation but a **structural consequence** of the design: the reasoning
never looks at an image, so each image only needs to be read into symbols once.

**(3) Refinement happens on the 3D side, not the 2D side.**
Once an instance is selected, its 2D mask is projected onto the point cloud and three
operations follow (quantified in §6).

### How the reasoning step was executed — stated plainly

The 445 reported reasoning results were produced by a **frontier LLM** working from a
written rule specification ([`docs/reasoning_rules.md`](docs/reasoning_rules.md)), run
**interactively, one instruction at a time, in 14 batches** — not as a batched API job.
The model saw only the candidate table; it never saw an image and never saw ground truth
(scoring is a separate step, [`code/task2/eval/score_cot.py`](code/task2/eval/score_cot.py),
run after the answers were fixed).

There is therefore **no script in this repository that reproduces the headline reasoning
results end to end**. The fully scripted counterpart is the open-model arm,
[`code/task2/s3_reasoning/qwen_cot.py`](code/task2/s3_reasoning/qwen_cot.py), which runs
Qwen3.5-9B over the same tables with the same rules; it is the ablation in §7.

Two consequences worth being explicit about:

- The cost claim in §4 ("one text-only inference per instruction") is a claim about the
  **method's call structure**, which is exactly countable, not about a measured API latency.
  See [`docs/metrics_and_cost.md`](docs/metrics_and_cost.md) for how calls and seconds are
  separated.
- Running the reasoning by hand is what made the per-question error attribution in §6.3 and
  the rule set in §7 possible. It is a deliberate trade of automation for diagnosability,
  and the Qwen arm exists to price that trade.

---

## 4. Results

SceneFun3D val split0, **all 442 instructions** (445 minus 3 with disputed ground truth,
each with a written reason).

| Method | Type | AP50 | AP25 |
|---|---|---:|---:|
| **This work · multi-frame th0.7** | training-free | **34.8** | 44.1 |
| This work · single frame + refinement | training-free | 29.9 | 44.3 |
| This work · single frame, no refinement | training-free | 19.5 | 38.0 |
| UniFunc3D-30B | training-free | 31.24 | **51.01** |
| UniFunc3D-8B | training-free | 23.82 | 44.04 |
| AffordMEM | training-free | 20.13 | 41.66 |
| Fun3DU (self-reported) | training-free | 16.90 | 33.30 |
| Fun3DU (reproduced here) | — | 13.71 | 26.29 |

**Cost** (measured on the same machine):

| | image-reading inferences | vision-side parameters | vision-side time / instruction |
|---|---:|---:|---:|
| This work | **1, text-only** | **860 M** | **28.4 s** |
| Fun3DU | 50 × 7B VLM | 8.8 G | 273.0 s |

The conversion uses the **mean**, not the median: the expected total for 50 calls is
`50 × E[one call]`. Molmo is autoregressive, and its mean is 46% above its median
(long tail, 856–8777 ms); using the median would understate the cost by a third.

**A property that is not in the table but matters more**: on the self-collected demo
scenes, 13 instructions share 1365 segmentation calls; re-running per instruction would
need 2728 — **a 50% saving**. Four of those instructions in the same scene
(top / 2nd / 3rd / bottom drawer) share **the same frame and the same detections**,
differing only in the parsed ordering constraint. **More instructions do not mean more
vision compute.**

### Three things that must be said clearly

1. **AP25 is worse than UniFunc3D-30B (44.1 vs 51.01).** The reason is the granularity
   analysis in §6.3.
2. **The language model used here is larger than 30B.** Part of the 34.8 comes from a
   stronger language model; this is not a size-matched comparison. The only data point
   close to size-matched is in §7.
3. **The method is not a new paradigm.** "Candidate generation + selector" is an existing
   idea; the differentiation I originally intended (explicit 3D spatial disambiguation) was
   found to be already occupied by AffordMEM / UniFunc3D in week two of the project.

---

## 5. Two findings that changed the direction

### 5.1 The official "AP50" is precision, not IoU

From reading the official evaluation source:

```python
precision = |gt & pred| / |pred|           # denominator is pred
AP50      = fraction(precision >= 0.50)    # not IoU > 0.5
recall    = |gt & pred| / |gt|             # -> AR50 / AR25
mIoU      = the only column that truly uses IoU
```

Once this is established, the optimisation direction inverts:

- **Selecting one extra candidate adds to the denominator** without necessarily adding to
  the numerator ⇒ **prefer fewer over more**
- **A large mask covering a small GT**: high recall, low precision ⇒ AP gets *worse*
- **Tightening a mask pays better than recalling more of it**

Under an IoU reading, the natural strategy would be "improve recall, cover the whole
object" — exactly backwards. This finding invalidated every self-evaluation I had done up
to that point, and every subsequent decision rests on it.

### 5.2 The oracle is only 21.3 — so the gain has to come from the mask side

My first oracle implementation gave 29.9, **identical to the actual score**, and its AR50
was *below* the upper bound it was supposed to define. That is not consistent. Rebuilt as
"**enumerate every candidate, run a full projection for each, and take the best by 3D
precision**":

```
oracle (perfect instance selection, no refinement)  = AP50 21.3
what was actually achieved                          = AP50 34.8
```

**Even with the optimal candidate selected on every question, without refinement the score
is only 21.3.**

⇒ The disambiguation layer is saturated; **refinement contributes more than the entire
remaining potential of perfect instance selection.** This judgement determined where all
the effort went in the last two weeks of the project.

---

## 6. Three tiers of gain on the mask side, and the source of the AP50/AP25 gap

The three rows below use **the same reasoning results with instance selection held
completely fixed**; only the post-projection processing changes:

| | AP50 | AP25 | AR50 | median points |
|---|---:|---:|---:|---:|
| no refinement | 19.5 | 38.0 | ~30 | — |
| + 2D erosion 5px + camera-frame front layer | 29.9 (+10.4) | 44.3 | 18.6 | 117 |
| + multi-frame parallax voting th0.7 | **34.8** (+4.9) | 44.1 | 11.8 | 58 |

### 6.1 A counter-intuitive localisation of the error

Splitting the +10.4: **2D mask edges account for +9.2, depth bleed-through for only +1.2.**

Intuition blames "points punching through into the background". Measurement says the
segmenter's mask is about 5 pixels **fatter** than the true object, and that rim of pixels
projects onto **the cabinet face behind the handle**. Hence:

- **2D erosion**: shrink the mask by 5 px before projecting
- **Camera-frame front layer**: keep only points with `z <= median(z) + 5 cm`.
  The band is an absolute distance in metres rather than a quantile, because handle
  thickness is a **fixed physical quantity**.

  The median must be taken over **the target point set**. Taking it over all visible
  points in the scene (the depth median of the whole room) shreds points inside the mask —
  the single-frame baseline drops from 28.7 to 21.5. This bug was caught only because the
  old baseline was kept around as a control.

### 6.2 Multi-frame fixes precision, not a wrong instance

Multi-frame works as follows: **the reasoning still runs once, on the top-1 frame**; the
remaining frames only vote on **the same instance** (taking the candidate with the largest
3D overlap with the seed point cloud), and the accumulated votes are thresholded by
relative peak. Parallax makes "bleed-through" points inconsistent across viewpoints, so
voting eliminates them.

It **cannot** change instance selection. There is direct evidence — stratifying by the
reasoning's self-reported confidence:

```
high    n=115   47.0 -> 55.7   (+8.7)
medium  n=168   31.5 -> 37.5   (+6.0)
low     n= 73    9.6 -> 11.0   (+1.4)   <- barely moves
```

Refinement is only meaningful once the right instance is selected; if it is wrong, no
amount of multi-frame voting recovers it.

The threshold is 0.7 rather than 0.9: th0.9 buys 0.7 more AP50 but costs 1.6 AP25 and
5.0 AR50, and leaves a median of 23 points — a mask that thin does not stand up.

### 6.3 What the 9.3 points between AP50 and AP25 are

The gap between 34.8 and 44.1 comes from a **granularity mismatch** diagnosed early in the
project by per-image manual review:

- GT annotates the **switch button**; the segmenter outlines the **whole switch plate**
- GT annotates the **whole remote control**; the segmenter extracts a **single button** on it
- GT annotates **part of a socket**; the segmenter outlines the **entire white socket plate**
  (recall 1.0, precision ≈ 1/3)

**This is not "failure to find", it is "outlining at a granularity inconsistent with the
annotation convention" — no amount of better candidate coverage fixes it.**

It also explains why every training-free method has AP25 crammed into 44–51: "finding the
right object" is close to saturated for everyone, and the remaining spread is granularity.
**Granularity is a labelling convention of the dataset. It cannot be inferred, only
learned.** (See §8.)

---

## 7. Ablation: swapping in a 9B open model gives opposite conclusions for the two stages

Each of the two pipeline stages is swapped for Qwen3.5-9B in turn, everything else held
fixed.

**Reasoning stage (97 questions, side by side)**

```
                        frontier   Qwen-9B    delta
2D accuracy (all)         52.5%      46.5%     -6.1
2D accuracy (in-pool)     88.1%      78.0%    -10.2
AP50                      28.9       24.7      -4.1
```

Qwen is **never uniquely correct** (both correct 45 / frontier only 7 / Qwen only 1 /
both wrong 46). Extrapolating to full-val single-frame gives ≈ 25.7. ⇒ **9B holds up on
the reasoning stage.**

The source of the gap shows up in the self-reported "criterion type": the frontier model
used 26 distinct criteria, Qwen only 7, and it forced 45 of 99 questions into the same
"ordering constraint" template. A label I had added specifically for "the host mask spans
several objects" was **never used once** by Qwen. ⇒ **When the evidence itself is
unreliable, it does not switch strategies — it keeps forcing the template.**

**Parsing stage (444 instructions)**

```
ordering constraint (ignoring naming differences)   91.7%   <- transcription; 9B can do it
target concept correct at part level                49.5%   <- requires inference
spatial relation F1                                 49.0%   (55.0% after name canonicalisation,
                                                             i.e. 45% are genuine extraction errors)
```

**A counter-intuitive conclusion: the common assumption is that structured extraction is
easy and reasoning is hard. Measurement says the opposite.**

Two instructions in the same prompt are equally explicit; the only difference is whether
the model must **infer against the literal reading**. `select` is transcription ("top left"
is written in the sentence) and reaches 91.7%; `concept` requires inference (the target of
"open the drawer" is the **handle**, not the drawer front) and reaches only 49.5%.

The errors are also highly structured: `socket -> plug` is **wrong in all 24 cases, in the
same direction** — "plug" is perfectly reasonable English, and the model has no way to know
this dataset labels the socket on the wall. **This class of "annotation convention" can be
learned but not inferred.**

⇒ a wrong concept ⇒ the segmenter detects the wrong thing ⇒ the rate at which the candidate
pool contains the answer drops from 64.3% to roughly 32%. **The parsing stage cannot be
swapped for 9B.**

**Therefore, on "would this be stronger than UniFunc3D-8B at matched scale", the honest
answer is: I do not have that data point, and inferring from the measured parsing stage, it
most likely would not be.** Part of the reported score is bought with a stronger language
model; UniFunc3D-8B is a self-contained 8B system and this is not.

Both arms use different prompts (the Qwen arm uses the compact English rule set, the
frontier arm the full specification), so this is **not a pure model comparison** and is not
presented as one.

---

## 8. OOD demo: self-collected scenes

Three household scenes were scanned on site with an iPhone (a chest of drawers, a kitchen,
a sofa corner), yielding 13 instructions. **Fully out of distribution**: different capture
device, scenes, lighting, and objects. **All 13 are correct under per-question manual
review** (no ground truth, so no automatic scoring; what is presented is the reasoning
chain itself).

Per question, the demo ships: the selected frame, the candidate table (the sole input to
the reasoning), two visualisations, the parse, the reasoning transcript, and the answer.
See [`demo_ood/`](demo_ood/).

### A geometry trap

The iPhone exports 1920×1440 jpgs stored **landscape** with EXIF orientation=6, while the
intrinsics are given relative to the landscape original. My first version tried to fold the
orientation **into the intrinsics matrix** — this is wrong:

**K can express per-axis scaling and translation, but it cannot express an axis swap.**

Result: 3D points still project in the landscape frame while the image has been rotated
upright, leaving a 90° discrepancy — yet the projected points "look like they land on the
image" and the visible-point statistics look normal. **The numbers alone will not reveal
it.**

What caught it was a self-check on the **correlation between the point cloud's own colour
and the colour sampled at its projected pixel**:

```
before the fix   -0.23
after the fix    +0.89 / +0.84 / +0.91   (three scenes; frames with corr >= 0.5: 100% / 98% / 100%)
```

The correct approach is to project in the original landscape frame first, then apply a pure
2D transform to the pixel coordinates. See
[`code/demo/iphone_io.py`](code/demo/iphone_io.py).

### Three failure modes recorded as observed

**(1) The open-vocabulary segmenter does not recognise branded, oddly shaped small
appliances.** The blender is detected in only 2 of 89 frames, at confidence 0.466;
`food processor` / `juicer` / `mixer` all return zero; only the generic term
`kitchen appliance` detects anything (5.7 per frame on average) but cannot tell which
appliance it is. The controls `air fryer` / `pressure cooker` / `socket` / `cabinet knob`
all behave normally — the difference is **whether the object has a stable generic shape**.

**(2) Automatic frame selection: each relation holding individually ≠ the whole reasoning
chain holding.** On one question, automatic selection returned the frame with the most
target detections; in that frame `above(cabinet, refrigerator)` does hold when checked
individually (some cabinet is above the refrigerator), but **that cabinet is not the door
the target knob is on** — the chain breaks in the middle. The frame was specified manually
with the reason written down. A real fix requires upgrading the criterion from
"each relation individually" to "target → host → container → landmark all land on the same
set of instances".

**(3) When the instruction itself is underdetermined, the method can only answer as a
group.** "the switch near the sofa" corresponds to a three-gang switch plate; the
instruction gives no basis for distinguishing within the plate, so nothing in the detections
can single one out and all three are returned.

---

## 9. A second line: closed-set functional-part segmentation

Before the training-free line, the same data was attacked as a supervised closed-set
segmentation task (9 functional classes, no language). It is reported in full in
[`docs/task1_closed_set.md`](docs/task1_closed_set.md); the two results that matter here:

```
per-point MLP on lifted DINOv2 features     mAP  3.13
PointTransformerV3, dual-head                    18.25   (5.8x)
```

This is the evidence behind Future Work §10.1: **training on this data does learn the
functional-part granularity** that the training-free line structurally cannot reach.

---

## 10. Limitations

1. **Granularity ceiling.** The 9.3 points in §6.3 are a structural limit of this approach.
   The segmenter's granularity prior is fixed by its training data and does not match this
   dataset's annotation convention; a training-free route cannot change it.
2. **High sensitivity to parse quality.** §7 shows the hardest stage to replace with a small
   model is the very first one, language understanding. Get the concept wrong and everything
   downstream is wrong.
3. **Single-frame decision.** The reasoning sees one frame. If the target is occluded or
   indistinguishable in every candidate frame, the method has no recovery path; multi-frame
   only refines, it does not re-select.
4. **Dependent on open-vocabulary detector coverage.** It fails silently on objects outside
   the detector's distribution (branded small appliances).
5. **The reported score uses a language model stronger than the competition's**; it is not a
   size-matched comparison.
6. **Low AR is a deliberate trade-off** (prefer fewer over more under a precision-only
   metric). If a downstream task needs complete coverage, this configuration is unsuitable.
7. **The headline reasoning results were produced interactively, not by a batch script**
   (§3). The scripted arm is the Qwen ablation.

---

## 11. Future work

### 11.1 Training-free front end + a trained granularity refinement head (first priority)

This is the only path that directly consumes the 9.3 points from §6.3, and the clearest
next step for this project.

**Basis**: the only method so far that has absorbed the granularity problem is TASA —
a VLM/CLIP/SAM front end plus a **trained Point Transformer back end doing geometric
refinement**, which lifts Fun3DU's AP50 from 16.9 to 26.9. And the second line of this
project (§9) already verified that training on this data does learn functional-part
granularity (per-point MLP 3.13 → PTv3 18.25, 5.8×).

**The interface already exists**: this method outputs "the selected instance and its host".
Feeding both point clouds to a refinement head trained on SceneFun3D preserves the
training-free nature and the efficiency advantage of the front end.

One honest regret: the two lines of this project **each proved half of this and were then
deliberately separated**. In week four, "task2 may not reuse task1" was set as a
loss-cutting rule; it was correct at the time, but it also closed this door.

### 11.2 Motion parameter estimation — the dataset's third annotation, a natural downstream

The dataset ships a motion annotation for every functional element (424 across 30 visits):

```
motion_type    trans(249) / rot(175)          binary classification
motion_dir     unit direction vector          direction regression on S^2
motion_origin  a point on the point cloud     a point on the rotation axis (redundant for trans)
viz_orient     inwards(210) / outwards(214)   binary classification
```

It answers "**which way does it move when touched**", which together with this report's
"**where should it be touched**" forms the complete manipulability description.
The official `eval/` covers only the first two tasks — **there is no evaluation script for
this one**, so the protocol must be defined.

**Why this method is a good front end for it**: motion is a property of the **host**, not of
the handle (a drawer translates outward, a door rotates about its hinge), and the parse here
already carries the `target -> host` relation explicitly. Taking the host point cloud and
fitting a dominant plane plus boundary detection already gives a training-free baseline:
the drawer front's normal ≈ the translation direction, the seam between door and carcass ≈
the rotation axis.

**Parameterisation suggestion (from the data)**: `[0,0,±1]` accounts for 142/424 ≈ **33%** of
`motion_dir`, so the gravity-aligned prior is very strong. **Classify into a few
gravity-aligned principal directions first, then regress the residual** — far more stable
than regressing directly on S². The genuinely hard part is the **axis position** for `rot`
(4 degrees of freedom, and hinges are usually occluded); per-point Hough voting fits there,
letting the visible door-panel points jointly vote out the invisible hinge.

### 11.3 Upgrade frame selection to chain satisfiability

Replace the §8-(2) criterion "does each spatial relation hold individually" with
"do target → host → container → landmark land on **the same set of instances**".

### 11.4 Replace the parsing stage with a small model plus a domain mapping table

§7 shows parsing failures concentrate in a few "annotation convention" classes
(socket / flush button / radiator knob). Covering six retrieval terms would hit 354 of the
444 instructions (79.7%). But **the 45% genuine extraction errors on spatial relations
cannot be rescued by a mapping table**, so this mitigates rather than solves.

---

## 12. Beyond the method: what this project actually established

Scores get superseded by the next SOTA; the following do not.

**Measure the ceiling before committing effort.** A two-hour oracle experiment decided
whether to spend two days writing a module (the instantiation paradigm in §9); the rebuilt
oracle at 21.3 decided where the last two weeks went.

**Split a gap into non-overlapping segments and quantify each separately.** 100 → 71 → 3 on
the closed-set line; 19.5 → 29.9 → 34.8 here; 9.2 : 1.2 for 2D edge versus depth bleed
inside the precision loss.

**Attribution requires a controlled variable.** The argument "AP25 ties with the competition,
therefore the entire lead comes from mask precision" was **withdrawn** once it was pointed
out that a cross-method comparison has no controlled variable. Only the internal three tiers
(same reasoning results throughout) support attribution.

**Manual review may overturn an automatic metric.** An automated scan reported segmenter
recall of 0.65, suggesting a serious candidate-generation problem; per-image manual review
overturned it — the projection and the metric were wronging it, and 12 of 14 drawer handles
were in fact all present.

**When a metric points at "the benchmark is broken", suspect yourself first.** About six
rounds went into investigating "20–60 cm registration defects in 44% of samples", briefly
concluding "this benchmark's ceiling is 56%". The root cause was one hard-coded line of my
own.

**Read the source, not the paper.** The official AP50 is precision, not IoU; Fun3DU's 0.7 is
a point-level relative peak, not a frame hit rate; the officially reported score is probably
optimistic. All three are obtainable only from code.

**Keep every failure on record, with the reason it failed.** Appendix B lists 20 rejected
routes, 5 of which are self-refutations — the most typical being "replace the VLM's spatial
reasoning with an explicit geometric solver", measured at AP50 7.19 against a baseline of
16.85 and demoted the same day. One entry is deliberately marked **"untested, not
falsified"**, because that line was never cleanly re-run after its bugs were fixed.

**Turn mistakes you have made into mistakes a script can block.** Changing the frame
selection strategy reordered instance ids while answers still referenced the old table; the
fix stamps every answer with its frame, and the visualiser refuses to render — and demands a
redo — when that stamp disagrees with the current selection.

---

## Appendix A — Reproducing the numbers

```bash
# The results table only. No dataset and no weights required.
python code/task2/eval/mf_agg.py       # reads results/task2/per_question/mf_s*.jsonl
```

Per-question, per-configuration precision / recall for every experiment is in
[`results/task2/per_question/`](results/task2/per_question/); the reasoning records are in
[`results/task2/cot_records/`](results/task2/cot_records/); the OOD demo is in
[`demo_ood/`](demo_ood/).

The rest of the code requires the SceneFun3D dataset (308 GB) and model weights that are not
shipped here — see [`code/README.md`](code/README.md).

---

## Appendix B — Rejected and falsified routes

Kept in full, including the five self-refutations. "Basis" is the measurement that killed it.

| Rejected | Basis |
|---|---|
| Offset head (closed-set line) | Oracle promised +18 AP; training never delivered it — **an upper bound is not attainability** |
| `la_scale` prior calibration (closed-set line) | No longer a lever on v1; balanced-softmax already corrects the prior during training |
| "Proposal generation is the only bottleneck" | Marginal analysis: fixing context alone +24.8 ≫ fixing proposals alone +8.8 |
| Heavy mask refinement as the main engine | The official metric has no AP75; refining to 0.75 does not move the headline score |
| "Build-once deployment" as the headline claim | The novelty was already occupied by AffordMEM / UniFunc3D |
| Swapping the feature backbone (C-RADIOv4) as a way out | At most 26% of the −37.8 gap is feature-related |
| Reusing the 3D-native closed-set route inside the training-free line | Measured as unworkable; separated deliberately to cut losses |
| Replacing Molmo with Qwen for pointing | Gate C: 0.306 vs 0.500 hit rate |
| "Segmenter recall is only 0.65" | Per-image manual review: a metric/projection artefact, not a detection failure |
| **Geometric solver as a standalone selector** | AP50 7.19 / 24% selection accuracy / ordinal indexing collapses on large cabinets |
| Every self-evaluation protocol before the metric correction | AP50 is precision, not IoU (§5.1) |
| "Registration defects in 44% of samples / benchmark ceiling 56%" | Six rounds of investigation; root cause was one hard-coded line of my own |
| "AP25 ties ⇒ the lead comes entirely from mask precision" | Cross-method comparison without a controlled variable |
| Rescuing `blender` detection by changing the query term | Four synonyms all return zero; only a generic term detects, and cannot disambiguate |
| Off-the-shelf 3D open-vocabulary features (Mosaic3D) | Granularity too coarse: cabinet and cabinet handle land in the same cluster |
| Colour / material fields in the parse schema | 19 instructions mention colour; every one has an independent geometric cue ⇒ 0% load-bearing |
| Early "multi-frame aggregation for candidate selection" | The correct viewpoint is usually a minority (1/8 vs 4/6); voting drowns it |
| Training a selector | Requires training and scale; conflicts with the training-free positioning |
| End-to-end VLM on Set-of-Mark images | **Untested, not falsified** — never cleanly re-run after two bugs were fixed |
| "Stronger than UniFunc3D-8B at matched scale" | The reported score includes the contribution of a stronger language model |
