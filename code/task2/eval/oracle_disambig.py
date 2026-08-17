#!/usr/bin/env python3
"""Disambiguation oracle: measure the ceiling available to a target-instance selector.

**The problem.** The reproduced baseline scores AP50 13.71 (16.9 self-reported), and 78 of
445 descriptions end up with an empty 3D mask after voting. The hypothesis was ambiguity
among sibling instances of the same class: different frames point at different siblings, so
the vote never converges.

**What this oracle answers.** If the "pick the right target instance" step were perfect, what
would AP50 be? The gap is the headroom available to any selector.

**Method** -- without re-running the VLM, reusing the stored per-frame predictions. For every
candidate row of every description (frame, point, mask), project that frame's visible GT
points into the mask; if most of them land inside, the mask is sitting on the target instance
and is kept, otherwise it is sitting on a sibling and is discarded. Only the "sitting on the
target" candidates survive into a re-run of the voting stage.

The projection uses the pipeline's own point-cloud-to-image mapper, so there is zero
convention drift against the voting code, and the ground truth uses the same grouped
annotation the official evaluation uses. **Mask quality is left untouched -- this is a
disambiguation oracle, not a mask oracle.**

**Reading the result.** Oracle far above 13.71 means selection is the dominant bottleneck and
a selector is worth building. Oracle close to 13.71 means selection is not the bottleneck
(the candidates themselves are poor, or mask quality caps the score), and effort should go
elsewhere. Descriptions still empty after the oracle are candidate-generation failures --
the VLM never produced a mask covering the target at all -- which is a pool problem no
selector can touch. The log counts those two classes separately, which is the point.

    python code/task2/eval/oracle_disambig.py \\
        --root <fun3du data root> --exp_root <fun3du experiment root>
"""
import os, sys, argparse, json
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import FUN3DU  # noqa: E402
import torch

# The baseline package must be importable (it does `from utils...` internally), so run from
# its directory or put it on the path. chdir is required by its relative resource loading.
sys.path.insert(0, FUN3DU)
os.chdir(FUN3DU)

from run_lifting import get_prediction, post_process_pcd, get_visit_stuff, save_record  # noqa: E402
from utils import io                                                       # noqa: E402
from utils.sun3d.data_parser import DataParser                             # noqa: E402
from utils.sun3d.fusion_util import PointCloudToImageMapper                # noqa: E402
from utils.misc import sort_alphanumeric                                   # noqa: E402

FRAC_TH = 0.5    # a candidate whose mask contains more than this fraction of the frame's
                 # visible GT points is sitting on the target instance
MIN_VIS = 5      # a frame needs at least this many visible GT points to be judged at all;
                 # below it, the frame simply cannot see the target


def gt_covers(mapper, pose, intrinsic, depth, mask_f, gt_xyz):
    """Fraction of this frame's visible GT points that fall inside candidate ``mask_f``.

    Returns ``(frac, n_visible)``.

    The projection deliberately reuses the lifting code's own mapping call, in the same
    form, so there is zero convention drift between the oracle and the pipeline it bounds.
    A whole-image mask is passed alongside as the visibility reference.
    """
    if mask_f.shape != depth.shape:                    # defensive: RGB masks are 1920x1440,
                                                       # depth is not; resize as lifting does
        mask_f = (torch.nn.functional.interpolate(
            torch.tensor(mask_f).unsqueeze(0).unsqueeze(0).float(), depth.shape,
            mode="nearest").squeeze().numpy().astype(mask_f.dtype))
    whole = np.ones(depth.shape)
    m = mapper.compute_multi_masked_mapping(
        pose, gt_xyz, np.stack([mask_f, whole], axis=0), depth, intrinsic, "cuda")
    in_mask = int((m[0, :, -1] == 1).sum())            # GT points inside mask_f
    visible = int((m[1, :, -1] == 1).sum())            # GT points visible in this frame
    return (in_mask / visible if visible else 0.0), visible


def filter_rows(mask_data, keep):
    """Drop candidate rows by index, keeping every parallel array the lifting code needs
    aligned with one another."""
    out = dict(mask_data)
    out["frame_ids"] = np.asarray(mask_data["frame_ids"])[keep]
    out["video_ids"] = np.asarray(mask_data["video_ids"])[keep]
    out["masks_f"] = [mask_data["masks_f"][i] for i in keep]
    for k in ("depth_paths", "poses", "intrinsics"):
        out[k] = [mask_data[k][i] for i in keep]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="dataset.root (workdir/data)")
    ap.add_argument("--exp_root", required=True)
    ap.add_argument("--split", default="val")
    ap.add_argument("--src_exp", default="repro_molmo")
    ap.add_argument("--dst_exp", default="repro_molmo_oracle")
    ap.add_argument("--frame_folder", default="frames")
    ap.add_argument("--pcds_folder", default="pcds")
    args = ap.parse_args()

    parser = DataParser(args.root, args.split)
    visits = sort_alphanumeric(parser.get_visits())
    visits2videos = io.get_visit_to_videos(args.root, args.split)
    dst_pcds = os.path.join(args.exp_root, args.dst_exp, args.pcds_folder)
    os.makedirs(dst_pcds, exist_ok=True)

    # Diagnostic counters
    stat = {"n_desc": 0, "base_empty": 0, "oracle_empty": 0,
            "recovered": 0,          # baseline empty -> oracle non-empty: a pure selection win
            "gen_fail": 0,           # baseline empty -> oracle still empty: generation failed,
                                     # which no selector can fix
            "cand_total": 0, "cand_kept": 0}
    per_desc = []

    for visit_id in visits:
        if visit_id not in visits2videos:
            continue
        video_list = visits2videos[visit_id]
        pcd = parser.get_laser_scan(visit_id)
        pcd = parser.get_cropped_laser_scan(visit_id, pcd)
        scene_xyz = np.asarray(pcd.points)
        proc_pcd = torch.tensor(scene_xyz).cuda()
        visit_data = get_visit_stuff(parser, visit_id, video_list)
        desc_data = parser.get_descriptions_list(visit_id)

        for desc_id in desc_data.keys():
            out_path = os.path.join(dst_pcds, f"{visit_id}_{desc_id}.npz")
            if os.path.exists(out_path):
                continue
            stat["n_desc"] += 1

        # Ground truth is a boolean mask over the cropped cloud -> GT xyz as a cuda tensor
            # (the mapper does not convert coords internally)
            gt_mask = np.asarray(parser.get_grouped_annotation(visit_id, desc_id)).astype(bool)
            gt_xyz = torch.tensor(scene_xyz[gt_mask]).cuda() if gt_mask.sum() > 0 else None

            mask_data = get_prediction(args.exp_root, args.src_exp, parser,
                                       visit_id, args.frame_folder, desc_id, visit_data)
            base_empty = mask_data is None
            if base_empty:
                stat["base_empty"] += 1

            keep = []
            if mask_data is not None and gt_xyz is not None and len(gt_xyz) > 0:
                n = len(mask_data["masks_f"])
                stat["cand_total"] += n
                h, w = None, None
                mapper = None
                for i in range(n):
                    depth = parser.read_depth_frame(mask_data["depth_paths"][i])
                    if mapper is None or depth.shape != (h, w):
                        h, w = depth.shape
                        mapper = PointCloudToImageMapper((w, h))
                    frac, vis = gt_covers(mapper, mask_data["poses"][i],
                                          mask_data["intrinsics"][i], depth,
                                          mask_data["masks_f"][i], gt_xyz)
                    if vis >= MIN_VIS and frac > FRAC_TH:
                        keep.append(i)
                stat["cand_kept"] += len(keep)

            if keep:
                pred = post_process_pcd(parser, proc_pcd, filter_rows(mask_data, keep))
            else:
                pred = None

            if pred is None:
                stat["oracle_empty"] += 1
                if base_empty:
                    stat["gen_fail"] += 1
            elif base_empty:
                stat["recovered"] += 1

            save_record(out_path, scene_xyz.shape[0], pred)
            per_desc.append({"visit": visit_id, "desc": desc_id,
                             "base_empty": base_empty,
                             "n_cand": 0 if mask_data is None else len(mask_data["masks_f"]),
                             "n_kept": len(keep), "oracle_empty": pred is None})
            print(f"  {visit_id} {desc_id[:8]} cand={per_desc[-1]['n_cand']:2d} "
                  f"kept={len(keep):2d} {'BASE_EMPTY ' if base_empty else ''}"
                  f"{'→still_empty' if pred is None else '→ok'}", flush=True)

    log_path = os.path.join(args.exp_root, args.dst_exp, "oracle_filter_stats.json")
    with open(log_path, "w") as f:
        json.dump({"summary": stat, "per_desc": per_desc}, f, indent=2)

    print("\n" + "=" * 60)
    print("[disambiguation oracle] filter statistics:")
    print(f"  descriptions:              {stat['n_desc']}")
    print(f"  candidate rows kept/total: {stat['cand_kept']} / {stat['cand_total']}  "
          f"({stat['cand_kept']/max(stat['cand_total'],1)*100:.1f}%)")
    print(f"  baseline empty predictions: {stat['base_empty']}")
    print(f"    - recovered by oracle:    {stat['recovered']}   "
          f"(a pure selection win -- what a selector could gain)")
    print(f"    - still empty:            {stat['gen_fail']}   "
          f"(candidate generation failed; a selector cannot reach these)")
    print(f"  oracle empty predictions:  {stat['oracle_empty']}")
    print(f"\n  statistics -> {log_path}")
    print("=" * 60)
    print("\nNext: run the official evaluation for the oracle AP50 and compare against the")
    print("reproduced baseline at 13.71:")
    print(f"  python evaluate.py dataset.root={args.root} dataset.split={args.split} \\")
    print(f"      exp_name={args.dst_exp} exp_root={args.exp_root} threshold=0.7")


if __name__ == "__main__":
    main()
