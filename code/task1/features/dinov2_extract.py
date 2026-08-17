"""
lift/dinov2_extract.py — single-frame RGB -> DINOv2 dense features, with
bilinear sampling at arbitrary pixel coordinates (Phase 1, step 2).

Design (single responsibility): given one RGB frame, produce a dense feature
grid, and let the caller (lift_to_pointcloud) query features at the projected
pixel coords (u,v) of visible 3D points. We deliberately do NOT loop frames or
touch the point cloud here.

Two implementation decisions you can't see in the DINOv2 paper:
  1) DINOv2 patch size = 14. Inputs whose H/W are not multiples of 14 get their
     remainder cropped. We resize to the nearest multiple of 14 and record the
     EXACT scale factor (orig_px -> resized_px), so sampling maps (u,v) correctly
     even when the original size isn't divisible by 14 (don't assume it is).
  2) Bilinear sampling via F.grid_sample: normalize (u,v) to [-1,1] and sample
     all visible points of a frame in one vectorized GPU call.

The model is frozen (eval + no_grad): we only read features, never train it.
"""

import torch
import torch.nn.functional as F

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import SCENEFUN3D  # noqa: E402

PATCH = 14  # DINOv2 ViT patch size


class DINOv2Extractor:
    def __init__(self, model_name="dinov2_vitl14", device="cuda",
                 target_long_side=924):
        """
        target_long_side: resize the frame's long side to ~this (multiple of 14)
            before the ViT. 924 = 66*14. Trades feature-grid resolution vs compute;
            larger = finer grid (better for small handles) but more memory/time.
            Phase-1 default is modest; bump later when chasing performance.
        """
        self.device = device
        self.model_name = model_name        # kept for cache provenance metadata
        # torch.hub validates the repo via a GitHub API call (api.github.com), rate-limited
        # to 60 req/hr per IP -> "HTTP 403: rate limit exceeded" on shared compute nodes.
        # skip_validation=True drops that call; repo zip + weights still download normally.
        self.model = torch.hub.load("facebookresearch/dinov2", model_name,
                                    trust_repo=True, skip_validation=True)
        self.model.eval().to(device)
        self.feat_dim = self.model.embed_dim  # 1024 for ViT-L/14
        self.target_long_side = (target_long_side // PATCH) * PATCH

        # ImageNet normalization (DINOv2 was trained with it).
        self.mean = torch.tensor([0.485, 0.456, 0.406], device=device).view(1, 3, 1, 1)
        self.std = torch.tensor([0.229, 0.224, 0.225], device=device).view(1, 3, 1, 1)

    def _resize_hw(self, H, W):
        """Pick a (H',W') that are multiples of PATCH, long side ~= target."""
        scale = self.target_long_side / max(H, W)
        Hr = max(PATCH, round(H * scale / PATCH) * PATCH)
        Wr = max(PATCH, round(W * scale / PATCH) * PATCH)
        return Hr, Wr

    @torch.no_grad()
    def extract(self, rgb):
        """One RGB frame -> dense feature grid.

        Args:
            rgb: (H,W,3) uint8 numpy (as read by the toolkit), original size.
        Returns dict:
            feat   : (Df, Hp, Wp) on device, fp16 under CUDA autocast (fp32 on CPU) --
                     per-patch features laid out as a grid (Hp=Hr/14, Wp=Wr/14).
            H, W   : original frame size (for mapping (u,v) back).
        """
        H, W = rgb.shape[:2]
        Hr, Wr = self._resize_hw(H, W)

        x = torch.from_numpy(rgb).to(self.device).float().permute(2, 0, 1)[None] / 255.0  # (1,3,H,W)
        x = F.interpolate(x, size=(Hr, Wr), mode="bilinear", align_corners=False)
        x = (x - self.mean) / self.std

        # Patch tokens only (drop CLS + register tokens), reshape to a grid.
        # fp16 autocast on CUDA: ~2-3x faster ViT-L forward, negligible feature change
        # (DINOv2 inference is fp16-robust; features are stored fp16 anyway). CPU stays fp32.
        if "cuda" in str(self.device):
            with torch.autocast("cuda", dtype=torch.float16):
                tokens = self.model.forward_features(x)["x_norm_patchtokens"]  # (1, Hp*Wp, Df)
        else:
            tokens = self.model.forward_features(x)["x_norm_patchtokens"]
        Hp, Wp = Hr // PATCH, Wr // PATCH
        feat = tokens[0].transpose(0, 1).reshape(self.feat_dim, Hp, Wp).contiguous()  # (Df,Hp,Wp)
        return dict(feat=feat, H=H, W=W)

    @torch.no_grad()
    def sample(self, fdict, u, v):
        """Bilinearly sample features at original-image pixel coords (u,v).

        Args:
            fdict: output of extract().
            u, v : (M,) torch/numpy, pixel coords in the ORIGINAL frame.
        Returns:
            (M, Df) on device in feat's dtype (fp16 under autocast, else fp32) per pixel.
        """
        feat, H, W = fdict["feat"], fdict["H"], fdict["W"]
        Df, Hp, Wp = feat.shape

        u = torch.as_tensor(u, device=self.device, dtype=torch.float32)
        v = torch.as_tensor(v, device=self.device, dtype=torch.float32)

        # Map original pixel (u,v) -> normalized [-1,1] grid coords for the FEATURE
        # grid using the pixel-EDGE convention (align_corners=False): (u+0.5)/W is a
        # pixel center's fractional position in [0,1], *2-1 -> [-1,1]. This matches the
        # align_corners=False resize in extract(), so there is NO half-cell offset at
        # the image borders. grid_sample's [-1,1] spans the whole feature tensor, so
        # the 14x patch downscale is handled automatically (no manual /14 needed).
        gx = ((u + 0.5) / W) * 2 - 1
        gy = ((v + 0.5) / H) * 2 - 1
        grid = torch.stack([gx, gy], dim=-1).view(1, -1, 1, 2).to(feat.dtype)  # (1,M,1,2);
        # match feat dtype (fp16 under autocast) so grid_sample never dtype-errors on stricter torch

        out = F.grid_sample(feat[None], grid, mode="bilinear",
                            align_corners=False, padding_mode="border")  # (1,Df,M,1)
        return out[0, :, :, 0].transpose(0, 1).contiguous()  # (M, Df)


if __name__ == "__main__":
    # Smoke test: one frame -> feature grid + PCA-RGB visualization of the grid,
    # to eyeball that DINOv2 features are spatially coherent (same object = same
    # color) BEFORE we lift them to 3D.
    import os, sys, argparse
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from data_io import load_scene  # our lift/data_io.py

    ap = argparse.ArgumentParser()
    ap.add_argument("--data_root", default=SCENEFUN3D)
    ap.add_argument("--visit_id", default="420683")
    ap.add_argument("--video_id", default="42445137")
    ap.add_argument("--frame", type=int, default=0)
    ap.add_argument("--out", default="./debug_lift")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    S = load_scene(args.data_root, args.visit_id, args.video_id)
    fr = S["frames"][args.frame]
    rgb = S["parser"].read_rgb_frame(fr["rgb"])  # (H,W,3) uint8

    ext = DINOv2Extractor(device="cuda" if torch.cuda.is_available() else "cpu")
    fd = ext.extract(rgb)
    Df, Hp, Wp = fd["feat"].shape
    print(f"[dinov2] frame {rgb.shape} -> feature grid ({Df}, {Hp}, {Wp})  "
          f"(orig {fd['H']}x{fd['W']}, patch {PATCH})")

    # PCA the feature grid to 3 channels -> RGB, upsample to frame size, show.
    feat = fd["feat"].permute(1, 2, 0).reshape(-1, Df).float().cpu().numpy()  # (Hp*Wp, Df)
    feat = feat - feat.mean(0, keepdims=True)
    U, Sg, Vt = np.linalg.svd(feat, full_matrices=False)
    pca = feat @ Vt[:3].T                       # (Hp*Wp, 3)
    pca = (pca - pca.min(0)) / (np.ptp(pca, axis=0) + 1e-8)
    pca_img = pca.reshape(Hp, Wp, 3)

    fig, ax = plt.subplots(1, 2, figsize=(13, 8))
    ax[0].imshow(rgb); ax[0].set_title("RGB"); ax[0].axis("off")
    ax[1].imshow(pca_img); ax[1].set_title(f"DINOv2 feature PCA ({Hp}x{Wp})"); ax[1].axis("off")
    png = os.path.join(args.out, f"dinov2_pca_{args.visit_id}_{fr['ts']}.png")
    fig.savefig(png, dpi=120, bbox_inches="tight"); print(f"[saved] {png}")

    # Sanity: sample at a few pixels, check output shape.
    uu = np.array([fd["W"] * 0.5, fd["W"] * 0.25])
    vv = np.array([fd["H"] * 0.5, fd["H"] * 0.75])
    s = ext.sample(fd, uu, vv)
    print(f"[sample] queried {len(uu)} px -> features {tuple(s.shape)}  (expect (2,{Df}))")