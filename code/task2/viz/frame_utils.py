#!/usr/bin/env python3
"""Small frame-lookup and projection helpers shared by the diagnostic visualisers.

These are inlined here rather than imported from the perception modules on purpose: those
modules pull in the baseline repository's `utils` package, which shadows our own (see
``code/README.md``). Keeping the visualisers dependent only on numpy and the data parser
avoids the conflict.
"""
import os, glob
import numpy as np

_IMG_H, _IMG_W = 1920, 1440          # hires_wide frames, as stored (portrait)


def build_rgb_index(data_root, visit, video):
    """Map frame id -> jpg path for one video of one visit."""
    idx = {}
    for p in glob.glob(f"{data_root}/{visit}/{video}/hires_wide/{video}_*.jpg"):
        idx[os.path.basename(p)[len(video) + 1:-4]] = p
    return idx


def lookup_rgb(idx, fid):
    """Exact frame id if present, otherwise the numerically nearest one.

    Frame ids are float-valued timestamps and the depth and RGB streams do not always carry
    byte-identical strings for the same instant, so an exact-match-only lookup silently
    drops usable frames.
    """
    if fid in idx:
        return idx[fid]
    if not idx:
        return None
    try:
        keys = np.array([float(k) for k in idx]); klist = list(idx)
        return idx[klist[int(np.argmin(np.abs(keys - float(fid))))]]
    except ValueError:
        return None


def to_px(pt, K, c2w):
    """A single world-space point -> pixel coordinates, or None if it is behind the camera."""
    w2c = np.linalg.inv(np.asarray(c2w, float)); pc = w2c[:3, :3] @ pt + w2c[:3, 3]
    if pc[2] <= 0:
        return None
    uv = np.asarray(K, float) @ pc
    return uv[:2] / uv[2]


def best_frame(md, gt_xyz):
    """The frame in ``md`` containing the most projected ground-truth points.

    Returns ``(K, c2w, video_id, frame_id)``, or None when there are no frames.
    Subsamples to at most 200 ground-truth points, since this only ranks frames.
    """
    seen = {}
    for i in range(len(md["frame_ids"])):
        key = (str(md["video_ids"][i]), str(md["frame_ids"][i]))
        if key in seen:
            continue
        K, c2w = md["intrinsics"][i], md["poses"][i]
        cnt = 0
        for p in gt_xyz[np.linspace(0, len(gt_xyz) - 1, min(200, len(gt_xyz))).astype(int)]:
            px = to_px(p, K, c2w)
            if px is not None and 0 <= px[0] < _IMG_W and 0 <= px[1] < _IMG_H:
                cnt += 1
        seen[key] = (cnt, K, c2w)
    if not seen:
        return None
    key = max(seen, key=lambda k: seen[k][0])
    return seen[key][1], seen[key][2], key[0], key[1]


def coverage(mask, gt_uv):
    """Fraction of projected ground-truth pixels that fall inside ``mask``."""
    if len(gt_uv) == 0 or mask is None:
        return 0.0
    H, W = mask.shape
    u = np.clip(gt_uv[:, 0].astype(int), 0, W - 1)
    v = np.clip(gt_uv[:, 1].astype(int), 0, H - 1)
    return float(mask[v, u].mean())


def nms_2d(masks_f, sel, iou_th, ds=4):
    """Within-frame NMS over a list of masks; returns the kept indices.

    The segmenter emits several overlapping masks on the same object when the detection
    threshold is low -- around three per handle. This keeps the largest and discards
    anything overlapping a kept mask by more than ``iou_th``.

    IoU is computed on a ``ds``-fold downsample, which is exact enough for a redundancy test
    and far cheaper at full frame resolution.

    ⚠️ This ranks by area, which is correct for *deduplication within one object*. Ranking
    candidates for *selection* must sort by score instead -- see sam3_util.sam3_masks.
    """
    dm = {i: masks_f[i][::ds, ::ds].astype(bool) for i in sel}

    def iou2d(a, b):
        inter = np.logical_and(a, b).sum(); uni = np.logical_or(a, b).sum()
        return inter / uni if uni else 0.0

    keep = []
    for i in sorted(sel, key=lambda k: -int(dm[k].sum())):
        if all(iou2d(dm[i], dm[j]) <= iou_th for j in keep):
            keep.append(i)
    return keep
