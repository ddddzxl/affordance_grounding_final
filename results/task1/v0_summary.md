# Closed-set v0 — instance AP summary

Official instance AP / AP50 / AP25 on the val split (30 scenes, split0). Task: functionality
segmentation, 9 affordance classes, instance segmentation.

## Headline

| Run | AP | AP50 | AP25 | Meaning |
|---|---:|---:|---:|---|
| perfect GT instances | 100 | 100 | 100 | harness self-check |
| **oracle** (GT per-point class -> our clustering) | **71.1** | 84.4 | 86.0 | **pipeline ceiling** (lift, labels and clustering all correct) |
| **v0 best** (no reweighting + logit adjust la=1.0) | **3.13** | 8.25 | 28.1 | **v0 ceiling**, after correcting the prior |
| v0 raw (inverse-sqrt weighting, uncorrected) | 1.06 | 1.94 | 22.6 | starting point |
| inverse-sqrt sampling + logit adjust (la=1.0) | 2.28 | 4.97 | 34.0 | the sampling reweighting leaves the adjustment under-corrected, so it lands below the row above |

## The three-segment gap, and what each segment is

- **100 -> 71**: the unobserved-point ceiling (ground-truth instance points never seen by a
  camera are permanent false negatives) plus clustering merging adjacent same-class instances
  (`plug_in` / `unplug` reach only 39 / 38 even under the oracle).
- **71 -> 3**: **a per-point independent MLP with no spatial consistency.** Even at its optimum
  it gives per-point precision 0.53 and recall 0.39 (against 1.0 / 1.0 for ground truth), so
  instantiation must collapse. **These 68 points are what v1 is designed to take.**
- **Prior mismatch** (training pool 30:1 against an evaluation distribution of 1300:1):
  4.3x over-prediction, with precision falling from 0.875 in-pool to **0.187** under the natural
  distribution. Fixable: logit adjustment lifts AP from 1 to 3; the proper fix is
  balanced-softmax at training time.

## Sweeps

- **eps**: not a lever (flat at ~0.76). This **excludes** fragmentation as the explanation.
- **tau (probability threshold)**: ceiling at ~2.1 — high-confidence false positives cannot be
  filtered away, which **confirms** the prior mismatch is a training problem, not a
  thresholding one.
- **la_scale**: peaks at la=1.0 with AP 3.13 — correcting the prior works, but is then capped by
  the per-point quality of the MLP.

## Diagnostic conclusion

v0 is exhausted. Four things are separated by measurement: **the features are viable** (oracle
71), **the prior mismatch is fixable** (logit adjust takes 1 to 3), **clustering is adequate**
(71 on clean classes), and **the binding constraint is the MLP's lack of spatial consistency**
(ceiling AP 3).

**Next step = v1: a point transformer for spatial consistency, plus balanced-softmax to correct
the prior during training.** All of the infrastructure carries over — evaluation, oracle, logit
adjustment, visualisation, and the ability to save and reload logits for second-scale
hyperparameter sweeps.
