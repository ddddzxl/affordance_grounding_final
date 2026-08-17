"""v0_mlp.py — v0 head: a per-point MLP on frozen DINOv2 features.

The probe showed DINOv2 features are 9/9-class linearly separable given a fair head,
so this head only needs to TRANSLATE features -> affordance class + lightly regularize.
Intentionally shallow (1024 -> 256 -> 128 -> 10); points are treated independently
(no spatial context — that is v1's PointTransformer).
"""
from __future__ import annotations
import torch
import torch.nn as nn


class V0MLP(nn.Module):
    def __init__(self, in_dim: int = 1024, hidden: tuple[int, ...] = (256, 128),
                 n_cls: int = 10, dropout: float = 0.1):
        super().__init__()
        dims = [in_dim, *hidden]
        layers: list[nn.Module] = []
        for a, b in zip(dims[:-1], dims[1:]):
            layers += [nn.Linear(a, b), nn.LayerNorm(b), nn.GELU(), nn.Dropout(dropout)]
        layers += [nn.Linear(dims[-1], n_cls)]            # logits, 0=bg, 1..9 affordance
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:   # (B,in_dim) -> (B,n_cls)
        return self.net(x)
