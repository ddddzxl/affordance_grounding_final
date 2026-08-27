# Results, and where each number comes from

Every figure below traces to a file in this directory. The headline table recomputes offline
from the shipped `.jsonl` with no dataset and no weights:

```bash
python code/task2/eval/mf_agg.py
```

**Reporting discipline used throughout.** All published numbers cover **the full val set, 442
instructions** (445 minus 3 with disputed ground truth, each with a written reason in its
`answer.json`). Subset numbers are diagnostics and are never placed alongside published
results. 2D selection accuracy and 3D AP50 are two different metrics and are never mixed in
one statement.

---

## 1. Headline table

SceneFun3D val split0, 442 instructions, official protocol
(`AP50 = fraction(precision >= 0.5)`; see [`../docs/metrics_and_cost.md`](../docs/metrics_and_cost.md)).
The official test split is withheld, so these are **val-selected numbers** — the erosion radius
and the voting threshold were chosen on the same split, as they are for every published
comparison in this table.

| Configuration | AP50 | AP25 | AR50 | median points |
|---|---:|---:|---:|---:|
| single frame, no refinement | 19.5 | 38.0 | 39.6 | 278 |
| single frame + erosion 5px + camera front layer | 29.9 | 44.3 | 18.6 | 117 |
| multi-frame th0.3 | 28.3 | 41.9 | 33.0 | 178 |
| multi-frame th0.5 | 31.2 | 43.7 | 20.8 | 135 |
| **multi-frame th0.7 — reported configuration** | **34.8** | **44.1** | 11.8 | 58 |
| multi-frame th0.9 | 35.5 | 42.5 | 6.8 | 23 |
| oracle (best candidate enumerated, no refinement) | 21.3 | — | 39.1 | — |

Source: [`task2/per_question/mf_s0.jsonl`](task2/per_question/mf_s0.jsonl) and
[`mf_s1.jsonl`](task2/per_question/mf_s1.jsonl), one record per instruction with precision,
recall and point count at every threshold.

**Why 0.7 and not 0.9.** th0.9 buys 0.7 more AP50 at a cost of 1.6 AP25 and 5.0 AR50, and
leaves a median of 23 points. Every tier is published rather than only the maximum, because
under a precision-only metric selecting the highest-AP50 tier is not a valid selection
procedure — see [`../docs/metrics_and_cost.md`](../docs/metrics_and_cost.md) §1.

### Published comparisons

| Method | Type | AP50 | AP25 |
|---|---|---:|---:|
| **This work, multi-frame th0.7** | training-free | **34.8** | 44.1 |
| UniFunc3D-30B | training-free | 31.24 | **51.01** |
| UniFunc3D-8B | training-free | 23.82 | 44.04 |
| AffordMEM | training-free | 20.13 | 41.66 |
| Fun3DU (self-reported) | training-free | 16.90 | 33.30 |
| Fun3DU (reproduced here) | — | 13.71 | 26.29 |
| Fun3DU (reproduced, plus our fallback and row scorer) | — | 16.85 | 28.99 |

Two things this table must not be used to claim:

- **The reproduction figure is 13.71, not 16.85.** The latter includes two additions of our own
  (a global fallback when context detection returns nothing, +1.57; a learned row scorer,
  +1.12). "Reproduced" may only refer to 13.71; 16.85 must be described as an improved variant.
- **Not a size-matched comparison.** The language model used here is larger than 30B. See §4.

---

## 2. The three tiers of mask-side gain

Same reasoning results throughout, instance selection held completely fixed; only the
post-projection processing changes. This is the one place in the report where attribution has a
controlled variable.

```
no refinement                                 AP50 19.5
+ 2D erosion 5px + camera-frame front layer        29.9  (+10.4)
+ multi-frame parallax voting th0.7                34.8  (+4.9)
```

Splitting the +10.4: **2D mask edge accounts for +9.2, depth bleed-through for +1.2.**

Source: [`task2/per_question/refine.jsonl`](task2/per_question/refine.jsonl), one record per
instruction per (erosion × 3D post-processing) combination.

**Cross-validated**: the chosen configuration yields 29.9 along two independent code paths,
`refine_sweep.py` and `multiframe_lift.py`.

### Multi-frame gain stratified by reasoning confidence

Read at th0.9, the tier where voting is fully engaged; the reported operating point is 0.7.

```
single -> multi th0.9, AP50
high    n=115   47.0 -> 55.7   (+8.7)
medium  n=168   31.5 -> 37.5   (+6.0)
low     n= 73    9.6 -> 11.0   (+1.4)   <- barely moves
```

This is the direct evidence that multi-frame voting refines precision but cannot repair a
wrongly selected instance. Reproduce with `python code/task2/eval/mf_agg.py --by_conf 1`.

---

## 3. Selection-stage quantities

```
2D selection accuracy, like for like    this work 58.6%   ·  Fun3DU 12.0%
D_pool                                  64.5%   the rate at which the candidate pool contains
                                                the answer, i.e. the ceiling on reasoning
in-pool disambiguation                  90.2%   where the pool holds the answer, the reasoning
                                                picks it 257 times out of 285
oracle, perfect selection, no refinement  AP50 21.3
```

The Fun3DU column is not a published figure: its stored per-frame masks were re-scored under
the criterion used here — a candidate counts as a hit when it covers at least 5% of the
projected ground truth — so both sides are measured with the same ruler.

Source: [`task2/cot_records/_index.json`](task2/cot_records/_index.json) for the three rates,
and [`task2/scored/batch*/score.json`](task2/scored/) for the per-question breakdown, which
separates `miss_pick` (the answer was in the pool and the wrong one was chosen — attributable
to reasoning) from `miss_pool` (the answer was never in the pool — attributable to candidate
generation).

---

## 4. Model-scale ablation

**Reasoning stage** (97 questions side by side)

```
                        frontier   Qwen-9B    delta
2D accuracy (all)         52.5%      46.5%     -6.1
2D accuracy (in-pool)     88.1%      78.0%    -10.2
AP50                      28.9       24.7      -4.1
AP25                      42.3       38.1      -4.1
```

The 9B model is never uniquely correct (both correct 45 / frontier only 7 / Qwen only 1 / both
wrong 46). Extrapolating to full-val single-frame gives ≈ 25.7.

**Parsing stage** (444 instructions)

```
ordering constraint (ignoring naming)          91.7%   transcription; 9B handles it
target concept correct at part level           49.5%   requires inference against the literal
spatial relation F1                            49.0%   (55.0% after name canonicalisation, so
                                                        45% are genuine extraction errors)
```

⇒ a wrong concept ⇒ the segmenter searches for the wrong thing ⇒ the candidate-pool hit rate
falls from 64.5% to roughly 32%.

Sources: [`task2/ablations/qwen_cot_cmp.json`](task2/ablations/qwen_cot_cmp.json),
[`qwen_parse_cmp.json`](task2/ablations/qwen_parse_cmp.json), with the raw per-question outputs
in the accompanying `.jsonl` files, and the AP50 cost of the Qwen reasoning arm in
[`refine_qwen.jsonl`](task2/ablations/refine_qwen.jsonl).

⚠️ **The two arms use different prompts** (the 9B arm gets the compact English rule set, the
frontier arm a longer version of the same rules), so this is not a pure model comparison and is
not presented as one.

**What the frontier model is load-bearing for.** At the reasoning stage it is worth 4.1 AP50
and nothing structural — the candidate table comes from the segmenter, and the refinement
tiers of §2 operate on the already-selected instance, so they apply to either arm unchanged.
The 25.7 extrapolation is the 9B reasoning arm on full val before any multi-frame voting,
against 23.82 for UniFunc3D-8B. Parsing is the stage that is genuinely sensitive, and its
failures concentrate on dataset-specific naming conventions rather than on reasoning: six
retrieval terms cover 354 of 444 instructions.

⚠️ The reported 34.8 uses a language model larger than 30B, so it is not a size-matched
comparison; the 25.7 extrapolation still takes its parse from the frontier model.

---

## 5. Measured cost

```
                     image-reading inferences   vision params   vision time / instruction
this work            1 (text only)              860 M           28.4 s
Fun3DU               50 x 7B VLM                8.8 G           273.0 s
                                                                = 9.6x, a lower bound
```

Single-call latency, same machine, 20 real frames, 3 warm-ups, synchronised:

| Model | median | mean | min | max |
|---|---:|---:|---:|---:|
| open-vocab segmenter | 653 ms | **646 ms** | 596 | 682 |
| Molmo-7B pointing | 3242 ms | 3385 ms | 819 | 7290 |
| Molmo + SAM in series | 3748 ms | **5460 ms** | 856 | 8777 |

Source: [`task2/ablations/latency.json`](task2/ablations/latency.json).

**The conversion uses the mean, not the median** — Molmo's mean runs 46% above its median, so a
median-based conversion understates the baseline by about a third. Full protocol in
[`../docs/metrics_and_cost.md`](../docs/metrics_and_cost.md) §2.

---

## 6. Closed-set line

| Model | mAP | AP50 | AP25 |
|---|---:|---:|---:|
| per-point MLP on lifted features | 3.13 | 8.25 | 28.1 |
| PointTransformerV3, dual head | **18.25** | 32.2 | 44.5 |

Measured ceilings, all under ground-truth per-point classes, isolating the instantiation
paradigm:

| Mode | AP | AP50 | AP25 |
|---|---:|---:|---:|
| perfect instances | 93.25 | 96.74 | 96.99 |
| perfect offset head | 89.23 | 94.91 | 95.16 |
| clustering (what is used) | 71.13 | 84.41 | 85.96 |

The architecture, the per-class breakdown, the two negative results and the full analysis are
in [`../docs/task1_closed_set.md`](../docs/task1_closed_set.md).

---

## 7. Directory contents

| Path | Contents |
|---|---|
| [`task2/per_question/`](task2/per_question/) | precision / recall / point count per instruction, per configuration. `mf_*.jsonl` drives the headline table |
| [`task2/cot_records/`](task2/cot_records/) | all 445 question records; 58 carry a full reasoning transcript. See its README |
| [`task2/scored/`](task2/scored/) | per-batch scoring detail, with `correct` / `pool_ok` / `gt_ids` per question |
| [`task2/ablations/`](task2/ablations/) | both open-model arms and the latency measurement |
| [`task2/figures/`](task2/figures/) | per-question review figures for the 58 curated questions: all candidates thin, the selection thick red, the ground-truth-containing candidate thick green, projected GT points in green |
| [`task1/`](task1/) | closed-set line: the v0 summary, the offset-oracle table, the `eps` / `tau` / `la_scale` sweeps, and the official evaluation output for the oracle modes |
