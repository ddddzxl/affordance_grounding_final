# Code

Two pipelines, sharing nothing but the path module.

- [`task2/`](task2/) — the training-free instruction-level grounding line (the main line)
- [`task1/`](task1/) — the supervised closed-set functional-part segmentation line
- [`demo/`](demo/) — the out-of-distribution demos, on self-scanned iPhone rooms
- [`paths.py`](paths.py) — every filesystem location, in one place

---

## Read this before trying to run anything

**This code is published to be read, not run.** It depends on assets that are not shipped
here and, in one case, cannot be shipped:

| Dependency | Size | Needed by |
|---|---|---|
| SceneFun3D val split (30 visits) | 308 GB | everything except the aggregation scripts |
| Open-vocabulary segmentation weights | ~3.4 GB | all perception stages |
| The reference baseline's repository | — | anything that lifts to 3D (its data parser and lifting utilities are imported directly) |
| Molmo-7B / SAM-H / OWLv2 | ~31 GB | only the baseline reproduction and the latency measurement |
| PointTransformerV3 (vendored) | — | the closed-set line only |

Set `AFFORDANCE_ROOT` to a working copy holding those; everything else derives from it.
Without it, `paths.py` falls back to this repository, which is what makes the one
no-dependency entry point work:

```bash
python code/task2/eval/mf_agg.py       # reproduces the main results table from shipped .jsonl
```

There is also one executable self-test, requiring only numpy and scipy:

```bash
python code/task2/s1_perception/framesel.py    # 21 assertions on synthetic data
```

**There is no script here that reproduces the headline reasoning results.** They were
produced by a frontier LLM working from [`../docs/reasoning_rules.md`](../docs/reasoning_rules.md),
interactively, one instruction at a time. The fully scripted counterpart is the open-model
arm, [`task2/s3_reasoning/qwen_cot.py`](task2/s3_reasoning/qwen_cot.py), which is the
ablation in [`../REPORT.md`](../REPORT.md) §7. This is discussed in the report rather than
left to be discovered.

---

## task2 — training-free instruction-level grounding

Stages run in order; each directory is one stage of
[`../docs/method.md`](../docs/method.md).

| Path | What it does |
|---|---|
| `s0_parse/parse.py` | instruction → constraint graph, via constrained JSON decoding |
| `s1_perception/sam3_util.py` | minimal segmenter wrapper, deliberately dependency-free (see the shadowing note below) |
| `s1_perception/framesel.py` | discriminative frame selection: hard conditions, graded relaxation, self-consistency ranking. **Has a runnable self-test.** |
| `s1_perception/run_sam3.py` | the swap experiment that replaced the baseline's perception stage |
| `s2_candidates/dump_candidates.py` | builds the ground-truth-free candidate table per instruction |
| `s3_reasoning/qwen_cot.py` | the scripted open-model reasoning arm |
| `s4_lift/lift.py` | single-frame projection to 3D, plus the corrected oracle |
| `s4_lift/refine_sweep.py` | the erosion × 3D post-processing sweep |
| `s4_lift/multiframe_lift.py` | multi-frame parallax voting |
| `eval/score_cot.py` | per-question scoring and review figures; **the only place ground truth enters** |
| `eval/mf_agg.py` | aggregates into the official table. **Runs with no dataset.** |
| `eval/oracle_disambig.py` | the baseline-side disambiguation oracle |
| `ablation/qwen_parse.py`, `qwen_parse_cmp.py` | the parsing-stage ablation and its comparison |
| `ablation/qwen_cot_cmp.py` | the reasoning-stage ablation comparison |
| `ablation/latency.py` | measured single-frame latency for both pipelines |
| `viz/viz_candidates.py` | candidate granularity versus ground truth — the figure behind the granularity finding |
| `viz/viz_vote_mask.py` | where precision is lost, with occlusion filtering |
| `viz/viz_detections.py` | 2D detection review — the figure that overturned an automated recall number |

## task1 — supervised closed-set segmentation

See [`../docs/task1_closed_set.md`](../docs/task1_closed_set.md) for the results and the
architecture constraints.

| Path | What it does |
|---|---|
| `models/` | the per-point MLP baseline and the PointTransformerV3 dual-head model |
| `features/` | DINOv2 extraction and the 2D→3D feature lift |
| `data/` | label construction, pooling, and voxel/coordinate precaching |
| `train/` | training loop, losses, metrics |
| `eval/` | prediction, official AP, the offset oracle, and the sweeps behind the negative results |

## demo

The iPhone capture pipeline, shared by both lines. `iphone_io.py` holds the EXIF-orientation
fix described in [`../REPORT.md`](../REPORT.md) §8; the `task2_*` scripts run geometry
self-checks, detection, packing, and answer visualisation.

---

## Two traps worth knowing about

**1. The baseline's `utils` package shadows ours.** Any script needing the baseline's data
parser must `sys.path.insert(0, FUN3DU)` and `os.chdir(FUN3DU)`, because that repository
resolves resources relative to its own directory. Doing so puts its top-level `utils` package
on the path, where it shadows any same-named package of ours, and every module doing
`from utils.data_parser import ...` then fails with `ModuleNotFoundError`. This is why
`sam3_util.py` imports nothing from the rest of the project, and why several scripts import
it *before* chdir'ing. Modules that must live on both sides of that boundary are inlined
rather than shared.

**2. Never hard-code `CUDA_VISIBLE_DEVICES` in a script on a cluster.** The scheduler sets it
from the resource request; overwriting it sends the job onto someone else's GPU and OOMs
there. Request more devices through the scheduler and index *within* the allocation with
`--device cuda:i`. Relatedly, when sharding across devices, do not combine `wait $PID` with
`set -e`: one failing shard then takes down the healthy ones with it.
