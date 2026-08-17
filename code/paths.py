#!/usr/bin/env python3
"""Centralised filesystem locations.

Every script in this repository resolves its inputs and outputs through this module rather
than hard-coding absolute paths. Override the root with the ``AFFORDANCE_ROOT`` environment
variable; everything else is derived from it.

None of the large external assets are shipped with this repository (the dataset alone is
308 GB). See ``code/README.md`` for what has to be present before any given script can run.

    export AFFORDANCE_ROOT=/scratch/affordance_grounding
"""
import os

# --------------------------------------------------------------------------------------
# Roots
# --------------------------------------------------------------------------------------

# Defaults to this repository, so that anything computable from the shipped result files
# works with no configuration at all -- `python code/task2/eval/mf_agg.py` is the case that
# matters. Point AFFORDANCE_ROOT at a working copy that also holds the dataset, the
# weights and the caches to run anything else.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.environ.get("AFFORDANCE_ROOT", _REPO_ROOT)

CODE = os.path.join(PROJECT_ROOT, "code")
DATA = os.path.join(PROJECT_ROOT, "data")
RESULTS = os.path.join(PROJECT_ROOT, "results")
THIRD_PARTY = os.path.join(PROJECT_ROOT, "third_party")

# --------------------------------------------------------------------------------------
# External dependencies (not shipped)
# --------------------------------------------------------------------------------------

# SceneFun3D val split. Per visit: *_laser_scan.ply, hires_wide/, hires_wide_intrinsics/,
# hires_poses.traj, descriptions.json, annotations.json.
SCENEFUN3D = os.path.join(DATA, "scenefun3d")

# The reference baseline's repository. Several scripts import its data parser and lifting
# utilities directly, and must chdir into it because it resolves resources relatively.
# Note that it ships a top-level `utils` package which SHADOWS any same-named package of
# ours -- see code/README.md.
FUN3DU = os.path.join(THIRD_PARTY, "fun3du")

# The working tree the baseline expects: <FUN3DU_DATA>/<split>/<visit>/... plus an
# experiment root it writes predictions into. Built by a setup helper, not by hand.
FUN3DU_DATA = os.path.join(DATA, "fun3du_repro", "data")
FUN3DU_EXPS = os.path.join(RESULTS, "fun3du_repro", "exps")

# PointTransformerV3 (vendored), used by the closed-set line only.
PTV3 = os.path.join(THIRD_PARTY, "PointTransformerV3")

# Open-vocabulary segmentation weights.
SEGMENTER_WEIGHTS = os.path.join(THIRD_PARTY, "sam3_weights")

# --------------------------------------------------------------------------------------
# Result locations, instruction-level line
# --------------------------------------------------------------------------------------

TASK2 = os.path.join(RESULTS, "task2")

# One directory per instruction: task.md / candidates.txt / meta.json / cands.npz.
# Produced by s2_candidates/dump_candidates.py, and ground-truth free by construction.
CANDIDATES = os.path.join(TASK2, "candidates")

# The same directories after answers were added, grouped into the batches they were
# solved in. Scoring writes into <batch>/_scored/.
SOLVED = os.path.join(TASK2, "cot_records")

# Per-question, per-configuration precision / recall for every lift experiment.
LIFT = os.path.join(TASK2, "per_question")

# Parse output, one entry per description.
PARSE = os.path.join(TASK2, "parse")

# Open-model ablation arms.
ABLATION = os.path.join(TASK2, "ablations")

# --------------------------------------------------------------------------------------
# Result locations, closed-set line
# --------------------------------------------------------------------------------------

TASK1 = os.path.join(RESULTS, "task1")

# Caches produced by the feature-lift and label-construction stages, one file per scene.
CACHE = os.path.join(PROJECT_ROOT, "cache")
FEATURE_CACHE = os.path.join(CACHE, "features_3d", "dinov2")
LABEL_CACHE = os.path.join(CACHE, "labels")
POOL_CACHE = os.path.join(CACHE, "pools")
XYZ_CACHE = os.path.join(CACHE, "xyz")
GT_VAL = os.path.join(CACHE, "eval", "gt_val")

RUNS = os.path.join(PROJECT_ROOT, "runs")
CHECKPOINTS = os.path.join(TASK1, "checkpoints")
SUBMISSIONS = os.path.join(TASK1, "submissions")

# The official dataset toolkit, used for the closed-set line's evaluation.
TOOLKIT = os.path.join(THIRD_PARTY, "scenefun3d")

# --------------------------------------------------------------------------------------
# Self-collected iPhone scans (3D Scanner App), used by both demos
# --------------------------------------------------------------------------------------

IPHONE_DATA = os.path.join(DATA, "iphone_3dscanner")
DEMO_TASK2 = os.path.join(PROJECT_ROOT, "demo_ood")
DEMO_TASK1 = os.path.join(PROJECT_ROOT, "demo_task1_ood")


def ensure(path: str) -> str:
    """Create ``path`` if missing and return it, so callers can inline it into an open()."""
    os.makedirs(path, exist_ok=True)
    return path
