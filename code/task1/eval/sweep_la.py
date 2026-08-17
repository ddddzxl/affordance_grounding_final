#!/usr/bin/env python3
"""sweep_la.py — forward the model ONCE over the 30 GT_VAL scenes, then sweep calibration
strength la_scale on the logits: pred = argmax(z + la·logπ).

la=1.0 == cal (natural posterior), la=0.0 == raw (aggressive, no prior). Rare classes
that cal over-suppresses (plug_in confirmed: cal 80% -> bg, raw 85% -> plug_in) should recover
recall as la drops, while common classes may lose precision. Per-class AP is printed so the
trade-off is visible — and so we can later pick a PER-CLASS la (low for rare, 1 for common).
raw-xyz DBSCAN (no offset), default cluster params. Writes eval_v1_la<la>.txt per setting.

  python src/eval/sweep_la.py --run C_g01p128_v2
  python src/eval/sweep_la.py --run C_g01p128_v2 --las 1.0,0.8,0.6,0.4,0.2,0.0
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

# columns to print: rare/long-tail first (the ones la is meant to help), then a couple healthy
SHOW = ["plug_in", "tip_push", "unplug", "foot_push", "key_press", "rotate", "pinch_pull"]


def parse_perclass(out: str) -> dict:
    """Official evaluate stdout -> {class_name: AP}; 'average' key holds the mean AP."""
    d = {}
    for line in out.splitlines():
        p = line.split()
        if len(p) >= 3 and p[1] == ":":
            try:
                d[p[0]] = float(p[2])                # AP (first of AP/AP50/AP25)
            except ValueError:
                pass
    return d


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="C_g01p128_v2")
    ap.add_argument("--ckpt", default="best.pt")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--las", default="1.0,0.7,0.5,0.3,0.0", help="comma list of la_scale")
    ap.add_argument("--eps", type=float, default=0.05)
    ap.add_argument("--min_samples", type=int, default=10)
    ap.add_argument("--min_cluster", type=int, default=20)
    args = ap.parse_args()
    dev = torch.device(args.device)

    ck = torch.load(os.path.join(RUNS, args.run, args.ckpt), map_location=dev, weights_only=False)
    a = ck["args"]; gs = a["grid_size"]; logp = np.array(ck["log_prior"], np.float32)
    model = build_model("v1_ptv3", grid_size=gs, proj_dim=a.get("proj_dim", 64),
                        enable_flash=a.get("enable_flash", True)).to(dev)
    model.load_state_dict(ck["model"]); eval_safe(model)

    visits = read_val_visits()
    print(f"[sweep_la] {args.run}/{args.ckpt} | forwarding {len(visits)} scenes once...", flush=True)
    cache = {}
    for i, v in enumerate(visits):
        cache[v] = forward_scene(model, v, dev, gs)
        print(f"  [{i+1}/{len(visits)}] {v}", flush=True)

    out_root = os.path.join(RESULTS, args.run); os.makedirs(out_root, exist_ok=True)
    las = [float(x) for x in args.las.split(",")]
    print(f"\n[sweep_la] pred = argmax(z + la·logπ), raw-xyz DBSCAN  (AP per class)\n", flush=True)
    print(f"{'la':>5} {'avgAP':>7}  " + " ".join(f"{c[:9]:>9}" for c in SHOW), flush=True)
    for la in las:
        sub_dir = os.path.join(out_root, f"submission_la{la}")
        mask_dir = os.path.join(sub_dir, "predicted_masks"); os.makedirs(mask_dir, exist_ok=True)
        for v in visits:
            sem, off, xyz_vox, inv, obs, n_full = cache[v]
            prob, pred = softmax_max(sem + la * logp)               # la·logπ calibration
            inst = cluster(pred, prob, xyz_vox, inv, obs, n_full,
                           args.eps, args.min_samples, args.min_cluster, 0.0)
            lines = []
            for k, ins in enumerate(inst):
                mf = f"{v}_{k:03d}.txt"
                with open(os.path.join(mask_dir, mf), "w") as fh:
                    fh.write(rle_encode(ins["mask"]))
                lines.append(f"predicted_masks/{mf} {ins['cls']} {ins['conf']:.4f}")
            if not lines:
                mf = f"{v}_000.txt"
                open(os.path.join(mask_dir, mf), "w").write("")
                lines.append(f"predicted_masks/{mf} 1 0.0")
            open(os.path.join(sub_dir, f"{v}.txt"), "w").write("\n".join(lines))
        out = run_eval(sub_dir)
        with open(os.path.join(out_root, f"eval_v1_la{la}.txt"), "w") as fh:
            fh.write(out)
        d = parse_perclass(out)
        row = " ".join(f"{d.get(c, float('nan')):>9.2f}" for c in SHOW)
        print(f"{la:>5} {d.get('average', float('nan')):>7.2f}  {row}", flush=True)


if __name__ == "__main__":
    main()
