# Line B — Supervised Closed-Set Functional-Part Segmentation

> 9 affordance classes, instance segmentation on the point cloud. **No language, no VLM.**
>
> This is the first of the project's two lines, and the evidence behind the first future-work
> item of [`../REPORT.md`](../REPORT.md): **training on this data does learn the
> functional-part granularity** that the training-free line structurally cannot reach.

**Data.** Official split: `train_set.csv` = **200** scenes for training, `val_set.csv` =
`gt_val` = **30** scenes for evaluation, train ∩ val = ∅ (no leakage). The official test
split is hidden (split1) and was not downloaded, so what is reported is **val-selected**
numbers — standard val usage, not a held-out test.

**Status.** v1 (PointTransformerV3) completed and capped out as semantic-only; the two
enhancement routes (offset head, prior calibration) **both failed** and are reported as
negative results; the line was then deliberately closed in favour of the training-free line.

---

## 1. Results

| Model | Setting | mAP | AP50 | AP25 |
|---|---|---:|---:|---:|
| v0 (per-point MLP on lifted features) | closed-set | 3.13 | 8.25 | 28.1 |
| **v1 (PointTransformerV3, proj128)** | **closed-set** | **18.25** | **32.2** | **44.5** |

v1 is **5.8×** v0.

**On external comparison — important.** Closed-set functionality segmentation **has no
comparable benchmark**. The official SceneFun3D report gives only an open-vocabulary
zero-shot baseline, which is a different setting from training on 9 class labels and does
not constitute a comparison; and results from the instruction-level line (e.g. Fun3DU) are a
different task entirely. The reference points used here are therefore strictly **internal
progress (v0 → v1, 5.8×) and the measured ceilings (§3)**. External comparison was left to
the training-free line, where the setting genuinely matches.

---

## 2. The starting point, and a three-segment gap decomposition

v0 was a per-point MLP (`1024 → 256 → 128 → 10`) on lifted DINOv2 features. Its purpose was
**not to score** but to test whether the lifted features separate the 9 classes at the point
level at all.

```
perfect GT instances               AP 100      harness self-check
oracle (GT per-point class)             71.1   pipeline ceiling (lift/label/DBSCAN all correct)
v0 best (with prior correction)          3.13   v0 ceiling
v0 raw                                   1.06   starting point
```

The methodologically important step was splitting 100 → 3.13 into **three non-overlapping
causes, each quantified by a separate experiment**:

```
100 -> 71   unobserved-point ceiling (+6.75) and DBSCAN merging adjacent same-class
            instances -- plug_in / unplug score only 39 / 38 even under a perfect oracle
 71 ->  3   per-point independent MLP with no spatial consistency;
            per-point precision 0.53 / recall 0.39 even at its optimum
prior mismatch   training pool 30:1 vs natural evaluation distribution 1300:1
                 -> 4.3x over-prediction; precision 0.875 (in-pool) -> 0.187 (natural)
```

The prior mismatch is fixable: inference-time logit adjustment lifts AP from 1 to 3;
the proper fix is balanced-softmax at training time.

Two sweeps also **excluded** the two most plausible-sounding alternative explanations:
`eps` is not a lever (flat at ~0.76, so fragmentation is not the problem), and the
probability threshold caps out at ~2.1 (high-confidence false positives cannot be filtered
away, which confirms the prior mismatch is a *training* problem). That left "the MLP has no
spatial consistency" as the sole remaining explanation, and it is what v1 attacks.

---

## 3. Measure the ceiling before committing: the offset oracle

Under the oracle, DBSCAN scores only 39 / 38 AP on `plug_in` / `unplug`, because adjacent
same-class instances get merged. The natural response is to build an offset head (predict
each point's offset to its instance centroid) — but that means writing a training loop and
tuning it.

So the upper bound was measured first, in about two hours. All modes use **GT per-point
class**, so the AP differences are a pure signal about the *instantiation paradigm*:

| Mode | AP | AP50 | AP25 | What it isolates |
|---|---:|---:|---:|---|
| `perfect_inst` | 93.25 | 96.74 | 96.99 | observed-only ceiling (100 → gap is unobserved-point FN) |
| `offset` | 89.23 | 94.91 | 95.16 | **upper bound of a perfect offset head** |
| `dbscan` | 71.13 | 84.41 | 85.96 | current instantiation, the baseline to beat |

```
100          -> perfect_inst   +6.75    unobserved points; not fixable here
perfect_inst -> offset         -4.02    residual: adjacent centroids closer than eps
offset       -> dbscan        -18.10    <- what an offset head would buy
```

Per class, the gain concentrates exactly where predicted: `unplug` +58.6, `plug_in` +34.5,
`key_press` +23.8, `hook_pull` +20.1. **Verdict: worth building.**

This "spend two hours measuring the ceiling before spending two days implementing" pattern
was reused throughout the project — most consequentially for the oracle in
[`../REPORT.md`](../REPORT.md) §5.2, which decided how the final two weeks were spent.

---

## 4. v1 — PointTransformerV3 with two heads

Backbone: PointTransformerV3-base (U-Net mode), a semantic head (9 classes + background) and
an offset head, then offset-shifted clustering, then the official AP.

```python
sem_head    = Linear(64,128) -> GELU -> Dropout -> Linear(128,10)
offset_head = Linear(64,128) -> GELU -> Linear(128,3)
```

### Implementation constraints, all of them learned the hard way

- **`proj_dim` bottleneck.** A `Linear(1024 -> 128)` projection runs *before* the backbone.
  Feeding 1024 channels straight in **overflows spconv's int32 GEMM at ~1.4 M voxels**.
  The projection width is also the main capacity knob: proj64 → 17.1, **proj128 → 18.25**,
  proj256 → 16.1 (over-parameterised, and clustering gets more fragmented).
- **`feat` and `xyz` travel separately and are never concatenated.** They are two independent
  fields of the backbone's input; concatenating would drown 3 geometric channels in 1024
  feature channels. Normalisation is LayerNorm, which does not depend on batch statistics.
- **`grid_size = 0.01`.** At 2 cm, a small handle collapses to 1–2 voxels.
- **`lr = 5e-4`.** At 1e-3 the full backbone diverges (spconv int32 + AMP → NaN).
- **`enable_flash=True` is a scale requirement, not a speed option.** Without it the
  `(patch, heads, K, K)` attention tensor is materialised; at 97 k voxels with AMP that
  already costs 20 GB.
- **Model selection is by official instance AP, not point F1.** These disagree: the proj256
  configuration has the best point F1 (0.646) and the *worst* instance AP (16.1). Point F1 as
  logged during training is binary foreground and computed on an internal subset, so it is
  the wrong selection criterion.
- Loss: **balanced-softmax** cross-entropy (`logits += log π_train`) for semantics,
  PointGroup-style offset loss (L1 + directional cosine, foreground points only).

---

## 5. Per-class results and the four distinct tail causes

| Class | GT inst | AP | AP25 | Cause |
|---|---:|---:|---:|---|
| pinch_pull | 147 | 46.1 | 84.0 | healthy |
| hook_turn | 66 | 33.3 | 68.8 | healthy |
| hook_pull | 145 | 27.8 | 59.8 | healthy |
| key_press | 26 | 21.3 | 64.8 | healthy (coarse cuts) |
| rotate | 58 | 18.0 | 36.9 | medium |
| unplug | 31 | 13.3 | 48.3 | AP ≪ AP25 ⇒ imprecise cutting (instantiation) |
| tip_push | 51 | 4.4 | 31.1 | AP ≪ AP25 ⇒ imprecise cutting (instantiation) |
| plug_in | 36 | 0.11 | 6.6 | recall collapse under prior suppression |
| foot_push | 1 | 0.0 | 0.0 | **not evaluable — a single val instance** |

**The four tail classes have four different causes and must not be lumped together as
"fix the tail":**

- **`foot_push`** has exactly one val instance, so AP is a 0-or-1 quantity. Train AP is 40.5
  (AP50 76.9 / AP25 81.8), which proves the class *was* learned. Reported as
  "learned; not evaluable on a single val instance", not as a failure.
- **`plug_in`** is a **recall** problem, not a separability or size problem. Two pieces of
  evidence: (1) size — `pinch_pull` at 4.2 cm scores AP 46 while `plug_in` at 4.1 cm scores
  0.1, so size is not the variable; (2) confusion — under calibrated inference 80% is missed
  as background with only 0.2% misclassified, while raw inference recovers 85% recall. The
  model learned it; the calibration prior (`log π ≈ −9.68`) suppresses it.
- **`tip_push` / `unplug`** have AP ≪ AP25, meaning the class is right and the IoU is not —
  a cutting/instantiation problem.
- Excluding `foot_push` and `plug_in`, the remaining **seven classes all sit near 23.5**.

---

## 6. Two negative results

### 6.1 The offset head — failed

The oracle in §3 said it was worth +18 AP. The trained head never delivered it.

- **Frozen backbone, offset head only**: directional loss only reaches ~0.55–0.69 (direction
  correct 30–45%), and instance AP lands at **16.6, below the 18.25 baseline** — an
  inaccurate offset pushes points to the wrong place and actively hurts.
- **Joint training** (warm start, unfrozen, lr 3e-4, λ 0.1): the offset gradient dominates
  the backbone by roughly **340×** (at epoch 0, `sem 0.0009` versus `λ·off 0.31`), and
  **one epoch drags semantic quality from 0.62 down to 0.42**.
- **Root cause**: frozen DINOv2 features cannot support accurate centroid regression, and the
  configuration that *could* learn it destroys the semantic head. The offset target itself
  was verified correct (centroid definition, not a bug). A genuine dilemma, not an
  implementation error.

**The transferable lesson: an oracle upper bound tells you where the ceiling is, not whether
it is reachable.** The correct next attempt would be two-stage (frozen as stage 1, then
unfrozen with grouped learning rates and a small λ), but there is no evidence the ceiling is
within reach of 18+.

### 6.2 Prior recalibration at inference — failed

Motivated by the `plug_in` confusion above. Sweeping `pred = argmax(z + la·log π)`:
**la = 1 (fully calibrated) is optimal at average AP 18.25, and lowering `la` decays
monotonically to 2.4** as raw over-prediction destroys precision. `plug_in` instance AP stays
at ~0 throughout — point-level recall comes back but never forms clean instances.

**Conclusion: calibration is already prior-optimal; there is no free lunch on the prediction
side.** Rescuing `plug_in` at the instance level requires training-side changes (resampling,
focal loss) with uncertain return, so it was descoped.

A related sanity check confirms the same thing from the other direction: on train scenes, raw
average AP is **2.21 against 18.25 calibrated** — raw `argmax(z)` implicitly assumes a uniform
prior, over-predicts a 1300:1 rare foreground, and collapses instance precision. Consequently
**raw instance AP cannot be used to read off "the semantic ceiling"**; that has to be read at
the point level.

---

## 7. v0 versus v1, qualitatively — why per-point quality decides instantiation

Same scene, same protocol:

| Model | GT | Pred | matched | FP | FN | forward | clustering |
|---|---:|---:|---:|---:|---:|---:|---:|
| v0 MLP | 31 | 27 | 15 | **12** | 16 | 164 ms | 1370 ms |
| v1 PTv3 | 31 | 26 | **23** | **3** | 8 | 1249 ms | 174 ms |

**The mechanism behind v0's instance AP collapse is under-segmentation, not just point
quality.** v0's point recall is high (0.80 — it "does not appear to miss anything"), but its
over-prediction produces one large blob, and DBSCAN then merges adjacent instances, so
several ground-truth instances match a single large prediction — giving **FN 16 through
merging, not through genuine misses**. v1 is precise, so points do not smear, so DBSCAN
separates them: matched 23 / FN 8.

This closes the gap in an otherwise confusing pair of numbers: v0 has point mIoU 0.66 but
instance AP 3.13, while v1 reaches 18.25. **Per-point precision directly determines whether
clustering can separate adjacent instances.**

The two models' FNs are also qualitatively different: v0's are under-segmentation
(smeared into a blob), v1's are conservative genuine misses (weak or small objects not
recalled). The timings corroborate the mechanism — v0's clustering takes 1370 ms because
there are far more points to cluster, v1's only 174 ms.

---

## 8. Train-versus-val diagnosis: method bottleneck versus generalisation

The question this answers: is the gap between val 18.25 and the oracle's 71 caused by
**"instance segmentation cannot learn this"** or by **"the model does not generalise"**?
The answer determines whether the next step is a new backbone or something else entirely.

Method: reuse the inference path line for line (same calibration, same clustering, same
forward) and change **only the ground-truth scenes** — from val to freshly built official
full-scan GT for sampled train scenes, verified exact-equal against `gt_val` in format
(including exclusions), then call the official evaluation. The only difference between the
two columns is which scenes the GT covers.

| | TRAIN (200) | TRAIN (30) | VAL (30) |
|---|---:|---:|---:|
| AP25 (coarse match) | 61.1 | 58.2 | 44.5 |
| AP (strict, = mAP) | 28.3 | 30.3 | 18.3 |
| **AP/AP25 ratio** (high-IoU mask precision) | **0.46** | 0.52 | **0.41** |

A correction worth recording: at 30 samples, the argument used the **absolute** AP25 → AP
drop (train 27.9 ≈ val 26.2). The full 200-scene run **broke that equality** (train 32.8 >
val 26.3, because a higher train AP25 widens the absolute drop). **The ratio is the stable
statistic**, and it gives:

- train **0.46–0.52** versus val **0.41** — close. High-IoU mask precision is a
  **method/instantiation bottleneck present on train as well as val** (1 cm voxels plus
  under-segmenting clustering, with IoU stuck between 0.25 and 0.5). This is attackable with
  a query-based backend or mask refinement.
- AP25 itself falls from train 61 to val 44.5, a **16.6-point coarse-localisation and
  semantic generalisation gap**. Changing the backend does not address this; it is a data
  problem (200 scenes is not many).

Two per-class corrections also came out of this run: `foot_push` is confirmed learned
(train AP 40.5) rather than unlearned, and `plug_in` is confirmed a genuine instantiation
failure rather than a tunable prior issue (train AP 0.15 calibrated and 0.000 raw — 200
scenes of exposure do not rescue it).

**Decomposition of the 53-point gap between val 18.25 and the oracle's 71:**
about **27 points of method bottleneck** (instance cutting, pinned down on train as well),
about **14 points of generalisation** (data), and the remainder in instantiation collapses
like `plug_in`.

---

## 9. Zero-shot demo on phone scans

The trained head was run directly on iPhone scans (3D Scanner App), reusing the lift pipeline
unchanged: the app's reconstructed point cloud is projected back into the RGB frames, DINOv2
features are sampled, and the head runs on top. No depth is used, so occlusion is not handled.
ARKit camera convention (+y up, −z forward) is converted to OpenCV (+y down, +z forward) by
flipping Y and Z; the projection was self-checked at 8770/8770 points in frame.

- **Poor input** (8770 points, untextured flat wall): **0 instances.** DINOv2 features on a
  uniform wall are grid noise with nothing semantic to grasp, and the geometric head is out of
  distribution on a sparse plane.
- **Good input** (185 k points, textured, 17 frames, door + switch + socket + piano):
  plausible predictions at roughly **80% visual precision** — including piano keys →
  `key_press`, which the model had never seen, socket → `plug_in`, switch → `tip_push`
  (right family, confused within it).

Findings: **the feature backbone transfers** (phone RGB is close enough to the training RGB),
**the geometric head is the bottleneck** (training clouds are 5 mm laser scans; iPhone LiDAR
is nominally 5 mm but materially worse). Capture quality decides the outcome — density,
texture, multiple frames, close range. And the OOD prior mismatch is severe: SceneFun3D's
extremely sparse foreground prior (1300:1) crushes a household scene dense in functional
parts (88 foreground points calibrated versus 5561 raw), so OOD inference uses raw logits plus
a confidence threshold instead.

Outputs are in [`../demo_task1_ood/`](../demo_task1_ood/).

---

## 10. Why this line was closed

The closed-set line reached a solid result (5.8× over v0) and both enhancement routes were
falsified, so further squeezing had diminishing returns. The instruction-level line had a
matching-setting SOTA to compare against, was the project's main line, and was measurable.

The quantified bottleneck structure above is what set the direction: the 14 generalisation
points cannot be bought with a new backend, whereas a language link was an untouched lever.

**And the number that matters for the main line**: per-point MLP 3.13 → PTv3 18.25 shows that
**training on this data does learn functional-part granularity**. That is exactly what the
training-free line cannot do (see [`../REPORT.md`](../REPORT.md) §6.3), which is why
"training-free front end + trained granularity refinement head" is the first future-work item.

One honest regret, recorded in the main report as well: "the training-free line may not
reuse this one" was set as a loss-cutting rule. It was correct at the time, and it
also closed that door.
