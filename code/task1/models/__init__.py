"""models/ — trainable HEADS on top of frozen DINOv2 features (the backbone is in
src/lift/, not trained). One file per version: v0_mlp (now), v1_ptv3 / v2_* (future).
Shared training/eval code (src/train, src/eval) picks an architecture via build_model().
"""
from .v0_mlp import V0MLP

_REGISTRY = {"v0_mlp": V0MLP}


def build_model(name: str, **kwargs):
    # v1_ptv3 pulls spconv/torch_scatter at import -> lazy-register so the v0/eval path
    # (e.g. predict.py `from models import build_model`) stays spconv-free.
    if name == "v1_ptv3" and name not in _REGISTRY:
        from .v1_ptv3 import V1PTv3
        _REGISTRY["v1_ptv3"] = V1PTv3
    if name not in _REGISTRY:
        raise KeyError(f"unknown model {name!r}; registered: {list(_REGISTRY)}")
    return _REGISTRY[name](**kwargs)
