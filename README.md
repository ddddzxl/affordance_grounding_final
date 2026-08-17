# Instruction-Level 3D Affordance Grounding

**Locating the part a hand actually touches, in a scanned room, from one sentence.**

> *"Open the top left drawer of the cabinet located to the left of the TV."*
> → a 3D mask of **that specific handle**, out of four identical ones on the same cabinet.

Independent research project, June–August 2026, single GPU. Benchmark: **SceneFun3D**
(30 rooms / 445 instructions, val split0).

---

## Headline

Mainstream methods on this task run a 7B vision-language model **once per frame over 50
frames** to point at the target. This project replaces that with a **symbolic bottleneck**:
one frame is compressed into a text-only candidate table (boxes, centres, areas,
confidences, containment relations), and the disambiguation becomes **a single text-only
inference that never sees an image**.

| | AP50 | AP25 | image-reading inferences | vision params | vision time / instruction |
|---|---:|---:|---:|---:|---:|
| **This work** (multi-frame th0.7) | **34.8** | 44.1 | **1, text-only** | **860 M** | **28.4 s** |
| UniFunc3D-30B (strongest concurrent training-free) | 31.24 | **51.01** | — | — | — |
| Fun3DU (self-reported) | 16.90 | 33.30 | 50 × 7B VLM | 8.8 G | 273.0 s |
| Fun3DU (reproduced here) | 13.71 | 26.29 | | | |

All 442 instructions (445 minus 3 with disputed ground truth). Timings measured on the same
machine. **AP25 is worse than UniFunc3D-30B, and the language model used here is larger than
30B** — both are discussed in [`REPORT.md`](REPORT.md) §4 and §7 rather than buried.

The structural property matters more than the score: **perception is cached by
(scene, concept), not by instruction**, so asking a room ten questions costs almost the same
vision compute as asking it one.

---

## Two findings that drove the design

**The official "AP50" is precision, not IoU.** From the evaluation source:
`AP50 = fraction(|gt ∩ pred| / |pred| >= 0.5)`. The metric is precision-only, so selecting
one extra candidate adds to the denominator without necessarily adding to the numerator, and
a large mask covering a small ground truth scores *worse*. The correct strategy is to tighten
masks, not to recall more — the opposite of what an IoU reading suggests. This invalidated
every self-evaluation made before it. ([`REPORT.md`](REPORT.md) §5.1)

**A perfect-selection oracle scores only 21.3.** Enumerating every candidate, running a full
projection for each and taking the best by 3D precision gives AP50 21.3 without refinement,
against 34.8 actually achieved. Refinement contributes more than the entire remaining
potential of perfect instance selection — which is where the last two weeks of the project
went. ([`REPORT.md`](REPORT.md) §5.2)

---

## Two lines of work

**Line A — training-free instruction-level grounding** (the main line, above).
Parse → per-concept open-vocabulary segmentation → symbolic candidate table → one text-only
inference → projection and refinement.

**Line B — supervised closed-set functional-part segmentation** (9 classes, no language).
Lifted DINOv2 features → PointTransformerV3 with a semantic head and an offset head.
`per-point MLP 3.13 mAP → PTv3 18.25 mAP (5.8×)`, with two enhancement routes that failed
and are reported as such. ([`docs/task1_closed_set.md`](docs/task1_closed_set.md))

Line B is the evidence behind the first future-work item: training *does* learn the
functional-part granularity that the training-free line structurally cannot reach.

---

## Where to look

| | |
|---|---|
| [`REPORT.md`](REPORT.md) | **Start here.** Method, results, ablations, limitations, future work, and the full list of rejected routes |
| [`index.html`](index.html) | The same material as a one-page visual summary |
| [`docs/method.md`](docs/method.md) | Pipeline details: candidate table format, frame selection, the three refinement tiers |
| [`docs/reasoning_rules.md`](docs/reasoning_rules.md) | The written rule specification the reasoning stage works from — also the prompt for the open-model ablation |
| [`docs/metrics_and_cost.md`](docs/metrics_and_cost.md) | How the official metric actually reads, and how call counts and wall-clock seconds are measured and kept separate |
| [`docs/task1_closed_set.md`](docs/task1_closed_set.md) | Line B in full |
| [`demo_ood/`](demo_ood/) | 13 instructions on three self-scanned rooms, fully out of distribution, with the reasoning chain for each |
| [`results/`](results/) | Per-question metrics as raw `.jsonl`, reasoning records, ablation outputs |
| [`code/`](code/) | Both pipelines. Read [`code/README.md`](code/README.md) first — see the note below |

---

## Two things to know before reading the code

**1. The reasoning stage was executed interactively, not batched.** The 445 reported
reasoning results were produced by a frontier LLM working from
[`docs/reasoning_rules.md`](docs/reasoning_rules.md), one instruction at a time, in 14
batches. The model saw only the candidate table — never an image, never the ground truth
(scoring is a separate step run afterwards). There is consequently **no script here that
reproduces the headline reasoning end to end**; the fully scripted counterpart is the
open-model arm, [`code/task2/s3_reasoning/qwen_cot.py`](code/task2/s3_reasoning/qwen_cot.py),
which is the ablation in [`REPORT.md`](REPORT.md) §7. Running the reasoning by hand is what
made per-question error attribution possible; the Qwen arm exists to price that trade.

**2. The code is published to be read, not run.** It depends on the SceneFun3D dataset
(308 GB), open-vocabulary segmentation weights, and a third-party baseline repository, none
of which are shipped here; paths are centralised in [`code/paths.py`](code/paths.py).
The one exception is the results table, which recomputes from the shipped `.jsonl` files with
no dataset at all:

```bash
python code/task2/eval/mf_agg.py
```
