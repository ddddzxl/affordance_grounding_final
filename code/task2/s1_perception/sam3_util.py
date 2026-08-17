#!/usr/bin/env python3
"""Minimal wrapper around the open-vocabulary segmenter (init + text -> masks).

**This module deliberately imports nothing from the rest of the project.**

The reason is an import shadowing conflict. Any script that needs the reference baseline's
data parser must do ``sys.path.insert(0, FUN3DU)`` and ``chdir(FUN3DU)``, because that
repository resolves resources relatively. Doing so puts its top-level ``utils`` package on
the path, where it **shadows** our own ``utils`` package -- and every one of our modules
that does ``from utils.data_parser import ...`` then dies with
``ModuleNotFoundError: No module named 'utils.data_parser'``.

Keeping the segmenter wrapper dependent only on transformers/torch/PIL/numpy sidesteps the
conflict at the root instead of patching sys.path around it at each call site.
"""
import numpy as np
import torch
from PIL import Image


def init_sam3(weights_dir, device="cuda"):
    """Load the segmenter through transformers directly.

    Going through transformers rather than a higher-level package avoids a tokenizer bug in
    the latter; it requires transformers >= 5.12.
    """
    from transformers import Sam3Processor, Sam3Model
    proc = Sam3Processor.from_pretrained(weights_dir)
    model = Sam3Model.from_pretrained(weights_dir).to(device).eval()
    return (model, proc)


def sam3_masks(predictor, rgb, text, det_th=0.4, mask_th=0.5, with_scores=False):
    """rgb (np HxWx3 uint8) + a text concept -> list of 2D bool masks, one per instance.

    With ``with_scores=True`` the return is ``[(mask, score)]``.

    **Downstream NMS must sort by score, not by area.** Sorting by area keeps the huge boxes
    first -- a whole cabinet run, or half the room -- which then suppress the genuinely
    correct small cabinet box underneath them. The default stays False for call-site
    compatibility.
    """
    model, proc = predictor
    H, W = rgb.shape[:2]
    inputs = proc(images=Image.fromarray(rgb), text=text, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model(**inputs)
    res = proc.post_process_instance_segmentation(
        outputs, threshold=det_th, mask_threshold=mask_th, target_sizes=[(H, W)])
    r = res[0] if isinstance(res, (list, tuple)) else res
    mk = r.get("masks") if isinstance(r, dict) else getattr(r, "masks", None)
    sc = r.get("scores") if isinstance(r, dict) else getattr(r, "scores", None)
    out = []
    if mk is not None and len(mk) > 0:
        for i, m in enumerate(mk):
            m = m.cpu().numpy() if hasattr(m, "cpu") else np.asarray(m)
            m = m.astype(bool)
            if not with_scores:
                out.append(m); continue
            v = 1.0
            if sc is not None and i < len(sc):
                x = sc[i]
                v = float(x.item() if hasattr(x, "item") else x)
            out.append((m, v))
    return out
