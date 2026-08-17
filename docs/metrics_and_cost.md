# Metric Protocol and Cost Accounting

Two separate things are documented here, because they are established in completely
different ways and mixing them is how misleading claims get made:

- **§1 — what the official metric actually computes.** Obtained by reading the evaluation
  source, and verified digit-for-digit against an official score.
- **§2 — cost.** Split into **call counts** (a property of the method, exactly countable)
  and **wall-clock seconds** (measured on one machine, on one day, with a stated protocol).

---

## 1. The official "AP50" is precision ≥ 0.5, not IoU > 0.5

From the SceneFun3D evaluation source (`utils/metrics.py`, `utils/evaluator.py`):

```python
precision = |gt & pred| / |pred|          # compute_3d_ap
AP50      = fraction(precision >= 0.50)   # AP25 likewise, >= 0.25
recall    = |gt & pred| / |gt|            # compute_3d_ar -> AR50 / AR25
mAP       = mean pass rate of precision over linspace(0.5, 0.95, 10)
mIoU      = the only column that genuinely uses IoU
```

The reported column order is `exp & mAP & AP50 & AP25 & mAR & AR50 & AR25 & mIoU`.

**Verification.** Four hand-computed instances give precision 0.56 / 0.63 / 0.51 / 0.00
→ three pass the 0.5 threshold → 3/117 = **2.564%**, matching the official **2.56**
digit for digit.

### Three consequences

**(1) Precision does not penalise incomplete coverage at all.** A small, accurate mask
scores full marks. "The single-frame lift does not recover all the points" costs nothing on
the headline metric, whereas enlarging a mask directly dilutes precision.

**(2) The AP family can be gamed by shrinking the prediction.** In the limit, predicting a
single point that lands on the ground truth gives precision 1.0 and therefore full
mAP / AP50 / AP25, with only AR and mIoU collapsing. **Any AP must therefore be reported
alongside AR**, and the operating point (the voting threshold) is a conscious trade-off
that has to be stated. This is why every threshold tier is reported in
[`results/main_table.md`](../results/main_table.md) rather than only the best AP50.

**(3) "AP25 ≫ AP50" is not an IoU-threshold phenomenon.** It is precision ≥ 0.25 versus
precision ≥ 0.5. Any historical reading of these numbers as IoU is wrong.

### Why this inverted the optimisation direction

Under an IoU reading, the sensible strategy is "improve recall, cover the whole object".
Under the actual metric:

- selecting one extra candidate adds to the denominator without necessarily adding to the
  numerator ⇒ **prefer fewer over more**
- a large mask covering a small ground truth has high recall and low precision ⇒ AP is
  *worse*, not better
- **tightening a mask pays better than recalling more of it**

Every self-evaluation protocol used before this finding was discarded and redone. The low
AR50 in the headline configuration is a deliberate consequence of this, not an oversight;
if a downstream task needs complete coverage, a lower voting threshold is the correct
operating point and the full curve is published for that reason.

### One internal-only diagnostic

For internal error analysis, AP10 / AP15 were also computed — the same precision quantity
at looser thresholds — to separate "found the right part" from "cut it tightly".
**These are diagnostics only and are never placed alongside published numbers**, which use
the official AP50 / AP25 / mAP / mIoU exclusively.

---

## 2. Cost

Scope: the point cloud is already scanned and the video already recorded. What is counted
is inference cost **from one instruction to one 3D mask**.

Setting: SceneFun3D val, 30 visits / 445 descriptions, median 203 frames per visit
(stride 10), median 13 descriptions per visit.

### 2.1 Model calls per instruction — exact counts

**This work**

| Stage | Model | Calls | Note |
|---|---|---:|---|
| Frame scoring | open-vocab segmenter | **13.7** | 203 frames ÷ 14.8 instructions — container scoring is reused across a visit |
| Candidate detection | open-vocab segmenter | ~30 | one pass per concept in the pool, cached per visit |
| **Reasoning** | **LLM (text only)** | **1** | reads the candidate table, selects instances |
| Lift | — | 0 | pure CPU projection |
| **Total** | | **~44 detections + 1 LLM call** | |

**Fun3DU** (counted from its code, so also exact)

| Stage | Model | Calls | Source |
|---|---|---:|---|
| Instruction CoT | LLM (text only) | 1 | `run_llm.py` |
| Context detection | OWLv2 + SAM | **13.7** | `run_detection.py`, also reused per visit |
| **Pointing** | **Molmo-7B (VLM, reads images)** | **50** | `run_molmo.py`, `frame_sampling.n: 50` |
| Mask generation | SAM | 50 | one prompt per Molmo point |
| Lift | — | 0 | `run_lifting.py` |
| **Total** | | **~114 detections + 50 VLM + 1 LLM** | |

**The core difference is 1 : 50 on image-reading inferences** — and the 1 here is a
text-only LLM call, while the 50 there are 7B VLM forward passes each reading a 1920×1440
image.

**Other concurrent methods** (no code available; estimated from paper descriptions, and
therefore **not quotable as measurements**):

| Method | Reasoning backbone | Per-instruction re-invocation | Basis |
|---|---|---|---|
| AffordMEM | MLLM + scene graph | undisclosed; at least 1 MLLM call plus graph construction | paper |
| UniFunc3D-8B | 8B MLLM, training-free | per-instruction frame count undisclosed | paper |
| AffordBot | Mask3D + Qwen2.5-VL-72B | 360° multi-view rendering + active view selection, **multiple 72B VLM calls** | paper, Table 4 |

AffordBot explicitly reports that a stronger MLLM raises its score (Qwen 23.3 → GPT-o1
33.4), which indicates its cost is tightly bound to MLLM invocation; a single 72B forward
pass is roughly an order of magnitude more expensive than Molmo-7B.

### 2.2 Measured wall-clock time

Same machine, same GPU, the same 20 real SceneFun3D frames (1920×1440), 3 warm-up
iterations each, `torch.cuda.synchronize()` before and after every timed call.
Raw output: [`results/task2/ablations/latency.json`](../results/task2/ablations/latency.json),
produced by [`code/task2/ablation/latency.py`](../code/task2/ablation/latency.py).

| Model | median | **mean** | min | max |
|---|---:|---:|---:|---:|
| Open-vocab segmenter (detection + segmentation in one, this work) | 653 ms | **646 ms** | 596 | 682 |
| Molmo-7B-D pointing (Fun3DU) | 3242 ms | 3385 ms | 819 | 7290 |
| **Molmo + SAM in series** (Fun3DU's true per-frame unit cost) | 3748 ms | **5460 ms** | 856 | 8777 |

**The conversion must use the mean, not the median.** The expected total for 50 calls is
`50 × E[one call]`; a median describes "a typical single call" and multiplying it by a count
has no statistical meaning. This matters asymmetrically:

- the segmenter's mean 646 ≈ its median 653 — a single forward pass whose cost barely
  depends on image content (596–682, a 14% spread)
- Molmo + SAM's mean 5460 is **46% above** its median 3748 — autoregressive generation emits
  more tokens on frames with more points, and SAM then runs once per point, giving a heavy
  tail (856–8777, a **10×** spread)

Using the median would understate Fun3DU's cost by a third.

**Vision-side total per instruction**

```
This work    segmenter x 44        =  28.4 s
Fun3DU       (Molmo + SAM) x 50    = 273.0 s      <- excluding its 13.7 OWLv2+SAM calls
--------------------------------------------------
vision-side ratio ~ 9.6x   (a lower bound)
```

Both sides have already been amortised per instruction at the visit level (the 13.7 frame
scoring calls here and the 13.7 context detections there are both reused across
instructions), so the ratio is like-for-like. The 273 s does not yet include the OWLv2+SAM
stage, which is why **9.6× is a lower bound, not an upper one**.

**One-off startup cost** (not part of per-query latency, but it shapes any interactive demo):

| | weight loading |
|---|---|
| Open-vocab segmenter (860 M) | < 10 s |
| Molmo-7B-D (30 GB, 7 shards) | **6 min 44 s** |

**Other measurements from this project, same machine**

| Item | Measured | Source |
|---|---|---|
| Full candidate generation (frame selection + detection + figure output) | median **93 s** per instruction | n=32; ⚠️ this batch's 33 instructions were spread over 21 visits, so visit-level cost was barely amortised — treat as an upper bound |
| Lift (pure CPU projection + scoring) | 445 instructions in ~30 min = **~4 s each** | |
| Multi-frame (top-8 frames) | 442 instructions on 2 GPUs in ~40 min = **~11 s each** | |
| Qwen3.5-9B CoT (thinking mode) | **~1.9 min** per instruction | 100 instructions in 3 h 49 m; ⚠️ the `flash-linear-attention` kernel was missing, so linear-attention layers ran a naive implementation |

### 2.3 What these numbers do and do not support

**Supported directly (counts, exact):** one text-only LLM inference per instruction here
versus 50 7B-VLM forward passes there, each reading a 1920×1440 image. Detector calls are of
the same order on both sides (~44 vs ~114).

**Supported directly (seconds, measured on one machine):** 28.4 s versus 273 s on the vision
side, about **9.6×**, and that is a lower bound since it omits Fun3DU's OWLv2 stage. The gap
does not come from model size — the vision side here is a single 860 M segmenter against a
combined 8.8 G of OWLv2 + SAM-H + Molmo — but from **how many times an image is read**.

**Requires qualification:** running the reasoning stage locally with Qwen3.5-9B takes about
1.9 min per instruction, but that was without the linear-attention acceleration kernel; via
an API, or with the kernel installed, it should be substantially lower. **LLM call latency is
excluded from both sides** — Fun3DU also makes one LLM call of comparable magnitude, so the
two cancel.

**Not supported:** any "end-to-end N× faster" claim that folds in LLM latency. What is solid
is the **9.6× on the vision side** and the **1 : 50 ratio of image reads**, one measured
like-for-like and the other counted exactly.
