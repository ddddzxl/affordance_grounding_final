"""v1_ptv3.py — v1 head: PTv3 backbone + dual head (semantic + offset).

PTv3 (Pointcept detached, third_party/PointTransformerV3) does SPATIAL aggregation on frozen
DINOv2 features (it does not re-learn geometry -> base config is fine, no need to go deeper).
Two heads on its per-point output:
  - semantic: per-point 10-class logits (0=bg, 1..9 affordance)  -> the 68-pt main lever
  - offset:   per-point 3-vec toward its instance centroid (PointGroup-style; shift+cluster
              solves adjacent-same-class merge -> offset_oracle measured +18 AP)

Interface red lines (verified by reading model.py):
  - coord & feat are DISTINCT Point fields -> xyz is NOT concatenated into the 1024-d feat,
    so it cannot be drowned (it drives serialization + sparse-conv + xCPE geometry paths).
  - feat gets a LayerNorm BEFORE PT -> scale-match against the metric-coord positional path.
  - enc_channels[0] raised 32->64 so the input SubMConv3d(1024->.) is not an extreme bottleneck.
"""
from __future__ import annotations
import os, sys, warnings
import torch
import torch.nn as nn

# spconv (pulled by PTv3) spams FutureWarning about torch.cuda.amp.custom_fwd/bwd at import; mute it.
warnings.filterwarnings("ignore", category=FutureWarning,
                        message=r".*torch\.cuda\.amp\.custom_(fwd|bwd).*")

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import THIRD_PARTY  # noqa: E402
_PTV3_PARENT = THIRD_PARTY   # so `PointTransformerV3` imports as a package
if _PTV3_PARENT not in sys.path:
    sys.path.insert(0, _PTV3_PARENT)
from PointTransformerV3.model import PointTransformerV3       # noqa: E402 (pulls spconv/torch_scatter)


class V1PTv3(nn.Module):
    def __init__(self, in_dim: int = 1024, n_cls: int = 10, proj_dim: int = 64,
                 enc_channels: tuple[int, ...] = (64, 64, 128, 256, 512),
                 head_hidden: int = 128, dropout: float = 0.1,
                 enable_flash: bool = False, grid_size: float = 0.01, **ptv3_kwargs):
        super().__init__()
        self.grid_size = grid_size
        self.feat_norm = nn.LayerNorm(in_dim)                 # red line ③: scale-match before PT
        # Dense projection 1024 -> proj_dim BEFORE PTv3's input SubMConv3d. Two reasons:
        #  (1) red line ①: don't let SubMConv3d(1024->.) be an extreme bottleneck;
        #  (2) spconv 2.x indice_conv GEMM is int32-indexed: operand ~ (total_active_pairs,
        #      in_channels) fp16; in_channels=1024 with ~1.4M voxels (pairs ~2e7) overflows
        #      int32 (>2.1e9). proj to 64 shrinks in_channels 16x. (Still crop large scenes.)
        self.feat_proj = nn.Linear(in_dim, proj_dim)
        self.backbone = PointTransformerV3(
            in_channels=proj_dim, enc_channels=enc_channels,
            enable_flash=enable_flash, cls_mode=False, **ptv3_kwargs)
        c = (ptv3_kwargs.get("dec_channels") or (64, 64, 128, 256))[0]   # per-point feat width out of PTv3
        self.sem_head = nn.Sequential(
            nn.Linear(c, head_hidden), nn.GELU(), nn.Dropout(dropout), nn.Linear(head_hidden, n_cls))
        self.offset_head = nn.Sequential(
            nn.Linear(c, head_hidden), nn.GELU(), nn.Linear(head_hidden, 3))

    def forward(self, coord: torch.Tensor, feat: torch.Tensor, offset: torch.Tensor):
        """coord (N,3) centered xyz; feat (N,in_dim); offset (B,) batch boundaries (cumsum of
        per-scene point counts). Returns (sem_logits (N,n_cls), pred_offset (N,3))."""
        data = dict(coord=coord, feat=self.feat_proj(self.feat_norm(feat)),
                    grid_size=self.grid_size, offset=offset)
        point = self.backbone(data)
        f = point.feat                                        # (N, c)
        return self.sem_head(f), self.offset_head(f)
