"""losses.py — class-weighted CE (+ optional focal) for the imbalanced affordance head.

Probe finding (two rounds): UNWEIGHTED CE collapses 7/9 classes to 0 on train; 1/sqrt(freq)
weighting recovers all 9. So v0 starts WEIGHTED. Scheme is configurable. The pool carries
no exclude points (255), but ignore_index is kept for label-convention consistency.
"""
from __future__ import annotations
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def class_weights(y: np.ndarray, n_cls: int = 10, scheme: str = "inv_sqrt") -> torch.Tensor:
    cnt = np.bincount(y[(y >= 0) & (y < n_cls)], minlength=n_cls).astype(np.float64)
    if scheme == "none":
        w = np.ones(n_cls)
    elif scheme == "inv":
        w = 1.0 / np.maximum(cnt, 1.0)
    elif scheme == "inv_sqrt":
        w = 1.0 / np.sqrt(np.maximum(cnt, 1.0))
    else:
        raise ValueError(f"unknown weight scheme {scheme!r}")
    w = w / w.sum() * n_cls                            # normalize so mean weight ~= 1
    return torch.tensor(w, dtype=torch.float32)


class FocalLoss(nn.Module):
    """Multiclass focal loss; gamma=0 reduces to weighted CE. weight is a buffer so
    .to(device) moves it with the module."""
    def __init__(self, weight: torch.Tensor | None, gamma: float = 2.0, ignore_index: int = 255):
        super().__init__()
        self.register_buffer("weight", weight)
        self.gamma = gamma
        self.ignore_index = ignore_index

    def forward(self, logits: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        # pt (focal modulation) must use the UNWEIGHTED true-class prob; the class weight
        # multiplies AFTER. exp(-weighted_ce) = p_true^w_c would be wrong.
        logp = F.log_softmax(logits, dim=1)
        ce = F.nll_loss(logp, target, weight=self.weight,
                        ignore_index=self.ignore_index, reduction="none")    # weighted CE
        valid = target != self.ignore_index
        tgt = target.clamp(min=0)                       # clamp so gather never OOB on ignore
        pt = logp.gather(1, tgt[:, None]).squeeze(1).exp()                   # unweighted p_true
        loss = (1 - pt) ** self.gamma * ce
        return loss[valid].mean() if valid.any() else (loss * 0.0).sum()


def build_loss(y_train: np.ndarray, scheme: str = "inv_sqrt", focal_gamma: float = 0.0,
               ignore_index: int = 255):
    """Returns (criterion, weight_tensor). Weights come from y_train ONLY (never val ->
    no leakage). focal_gamma>0 -> focal, else weighted CE."""
    w = class_weights(y_train, scheme=scheme)
    if focal_gamma > 0:
        return FocalLoss(w, gamma=focal_gamma, ignore_index=ignore_index), w
    return nn.CrossEntropyLoss(weight=w, ignore_index=ignore_index), w


# ----------------------------------------------------------------------------------------------
# v1 (PTv3, per-scene, natural distribution) losses
# ----------------------------------------------------------------------------------------------
def balanced_softmax_ce(logits: torch.Tensor, target: torch.Tensor,
                        log_prior: torch.Tensor, ignore_index: int = 255) -> torch.Tensor:
    """Add log π_train to logits BEFORE CE -> learn the prior-corrected posterior so the 0.077%
    affordance is not drowned under per-scene (natural) training. NOTE (v1_design §2): v1 trains
    on the NATURAL distribution -> NO v0-style 30:1/1300:1 mismatch; this fixes LONG-TAIL
    imbalance, not a prior shift. logits (N,C), target (N,) long, log_prior (C,). CE in fp32."""
    return F.cross_entropy(logits.float() + log_prior, target, ignore_index=ignore_index)


def offset_loss(pred_off: torch.Tensor, gt_off: torch.Tensor, fg_mask: torch.Tensor,
                l1_weight: float = 1.0, eps: float = 1e-8):
    """PointGroup-style offset loss on foreground points only: L1 magnitude + (1-cos) direction.
    pred_off/gt_off (N,3), fg_mask (N,) bool. Returns (loss, l1, ldir); grad-safe 0 if no fg.
    ⚠️ l1 is metric (~0.0x m) while ldir is in [0,2] -> l1 easily drowned. `l1_weight` rebalances
    (step3: print l1/ldir magnitudes and raise l1_weight, else offsets learn direction-only and
    points don't shrink to the centroid -> DBSCAN still merges)."""
    if int(fg_mask.sum()) == 0:
        z = pred_off.sum() * 0.0
        return z, z.detach(), z.detach()
    p, g = pred_off[fg_mask], gt_off[fg_mask]
    l1 = F.l1_loss(p, g)                                          # magnitude (metric, can be small)
    pn = p / (p.norm(dim=1, keepdim=True) + eps)
    gn = g / (g.norm(dim=1, keepdim=True) + eps)
    ldir = (1.0 - (pn * gn).sum(1)).mean()                       # direction in [0,2]
    return l1_weight * l1 + ldir, l1.detach(), ldir.detach()
