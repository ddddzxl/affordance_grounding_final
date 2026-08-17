#!/usr/bin/env python3
"""sweep_cluster.py — forward the model ONCE over the 30 GT_VAL scenes, then sweep DBSCAN params
(min_cluster, eps) cheaply WITHOUT re-running the network per setting.

Motivation: min_cluster=20 drops small instances (e.g. pinch_pull had 45/147 GT instances with
<20 voxels) — check whether relaxing min_cluster / eps recovers AP, or whether 20 is already best.
cal calibration only, raw-xyz DBSCAN (no offset; use predict_v1 --use_offset for the offset model).
Writes one eval_v1_cal_sweep_<tag>.txt per setting under results/func_seg/v1/<run>/.

  python src/eval/sweep_cluster.py --run C_g01p128_v2                       # min_cluster 10/15/20/30
  python src/eval/sweep_cluster.py --run C_g01p128_v2 --epss 0.03,0.05,0.08 --min_clusters 20
"""
from __future__ import annotations
import os, sys, argparse
import numpy as np
import torch

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import CODE  # noqa: E402
sys.path.insert(0, os.path.join(CODE, "task1"))
from eval.predict_v1 import (forward_scene, eval_safe, cluster, softmax_max,    # noqa: E402
                             run_eval, read_val_visits, rle_encode, RUNS, RESULTS)
from models import build_model                                                  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="C_g01p128_v2")
    ap.add_argument("--ckpt", default="best.pt")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--min_clusters", default="10,15,20,30", help="comma list of min_cluster")
    ap.add_argument("--epss", default="0.05", help="comma list of DBSCAN eps")
    ap.add_argument("--min_samples", type=int, default=10)
    args = ap.parse_args()
    dev = torch.device(args.device)

    ck = torch.load(os.path.join(RUNS, args.run, args.ckpt), map_location=dev, weights_only=False)
    a = ck["args"]; gs = a["grid_size"]; logp = np.array(ck["log_prior"], np.float32)
    model = build_model("v1_ptv3", grid_size=gs, proj_dim=a.get("proj_dim", 64),
                        enable_flash=a.get("enable_flash", True)).to(dev)
    model.load_state_dict(ck["model"]); eval_safe(model)

    visits = read_val_visits()
    print(f"[sweep] {args.run}/{args.ckpt} | forwarding {len(visits)} scenes once...", flush=True)
    cache = {}
    for i, v in enumerate(visits):
        cache[v] = forward_scene(model, v, dev, gs)
        print(f"  [{i+1}/{len(visits)}] {v} {cache[v][0].shape[0]:,} vox", flush=True)

    out_root = os.path.join(RESULTS, args.run); os.makedirs(out_root, exist_ok=True)
    mcs = [int(x) for x in args.min_clusters.split(",")]
    epss = [float(x) for x in args.epss.split(",")]
    print(f"\n[sweep] grid min_cluster={mcs} eps={epss} (cal, raw-xyz DBSCAN)\n", flush=True)
    print(f"{'eps':>6} {'min_cl':>7} {'#inst':>7}  {'AP':>8} {'AP50':>8} {'AP25':>8}", flush=True)
    for eps in epss:
        for mc in mcs:
            tag = f"mc{mc}_eps{eps}"
            sub_dir = os.path.join(out_root, f"submission_sweep_{tag}")
            mask_dir = os.path.join(sub_dir, "predicted_masks"); os.makedirs(mask_dir, exist_ok=True)
            n_inst = 0
            for v in visits:
                sem, off, xyz_vox, inv, obs, n_full = cache[v]
                prob, pred = softmax_max(sem + logp)                # cal
                inst = cluster(pred, prob, xyz_vox, inv, obs, n_full,
                               eps, args.min_samples, mc, 0.0)
                lines = []
                for k, ins in enumerate(inst):
                    mf = f"{v}_{k:03d}.txt"
                    with open(os.path.join(mask_dir, mf), "w") as fh:
                        fh.write(rle_encode(ins["mask"]))
                    lines.append(f"predicted_masks/{mf} {ins['cls']} {ins['conf']:.4f}")
                if not lines:                                        # zero-instance -> dummy
                    mf = f"{v}_000.txt"
                    open(os.path.join(mask_dir, mf), "w").write("")
                    lines.append(f"predicted_masks/{mf} 1 0.0")
                open(os.path.join(sub_dir, f"{v}.txt"), "w").write("\n".join(lines))
                n_inst += len(inst)
            out = run_eval(sub_dir)
            with open(os.path.join(out_root, f"eval_v1_cal_sweep_{tag}.txt"), "w") as fh:
                fh.write(out)
            avg = [l for l in out.splitlines() if l.strip().startswith("average")]
            ap = avg[0].split()[-3:] if avg else ["?", "?", "?"]
            print(f"{eps:>6} {mc:>7} {n_inst:>7}  {ap[0]:>8} {ap[1]:>8} {ap[2]:>8}", flush=True)


if __name__ == "__main__":
    main()
