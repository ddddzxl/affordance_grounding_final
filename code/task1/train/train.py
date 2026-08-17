#!/usr/bin/env python3
"""train.py — shared trainer for the func_seg heads (v0 now; v1/v2 later via --config).

Loads the balanced pool, splits in-train val BY SCENE, trains the chosen head with
weighted CE + AdamW(cosine + warmup) + AMP, logs per-epoch point-level metrics + the v0
go/no-go gate, checkpoints best/last. Single-GPU (head is ~0.3M params; DDP comes later).

  python src/train/train.py --config src/train/configs/v0.py --run v0mlp_s0 --device cuda:0
"""
from __future__ import annotations
import os, sys, json, time, math, argparse, importlib.util
import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))    # src/train
sys.path.insert(0, HERE)                             # dataset, losses, metrics
sys.path.insert(0, os.path.dirname(HERE))            # src/ -> models package
from models import build_model                        # noqa: E402
import dataset, losses, metrics                        # noqa: E402

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import RUNS  # noqa: E402



def load_config(path: str) -> dict:
    spec = importlib.util.spec_from_file_location("v_cfg", os.path.expanduser(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CONFIG


@torch.no_grad()
def evaluate(model, X, y, idx, dev, chunk=1_000_000):
    model.eval()
    preds = []
    for i in range(0, idx.shape[0], chunk):
        bi = idx[i:i + chunk]
        xb = torch.from_numpy(np.asarray(X[bi])).to(dev).float()
        preds.append(model(xb).argmax(1).cpu().numpy())
    pred = np.concatenate(preds) if preds else np.empty(0, np.int64)
    return metrics.point_metrics(pred, y[idx])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--run", required=True, help="run name -> runs/func_seg/<run>/")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--epochs", type=int, default=None, help="override config epochs")
    ap.add_argument("--weight_scheme", default=None, choices=["none", "inv", "inv_sqrt"],
                    help="override config weight scheme; 'none' to cut over-prediction / false positives")
    ap.add_argument("--val_split", dest="val_split", action="store_true", default=None,
                    help="override config -> validate on real val split (needs val pool)")
    ap.add_argument("--no_val_split", dest="val_split", action="store_false",
                    help="override config -> in-train val (no val pool; good for smoke)")
    args = ap.parse_args()

    cfg = load_config(args.config)
    if args.epochs is not None:
        cfg["epochs"] = args.epochs
    if args.val_split is not None:
        cfg["use_val_split"] = args.val_split
    if args.weight_scheme is not None:
        cfg["weight_scheme"] = args.weight_scheme
    dev = torch.device(args.device)
    seed = cfg["seed"]
    np.random.seed(seed); torch.manual_seed(seed)
    rng = np.random.default_rng(seed)

    run_dir = os.path.join(RUNS, args.run)
    os.makedirs(run_dir, exist_ok=True)
    print(f"[train] run={args.run} dev={dev} cfg={args.config}", flush=True)

    # --- data: load train pool; val source = in-train (by-scene split) OR real val split ---
    X, y, scene = dataset.load_pool(cfg["pool_dir"])
    y = y.astype(np.int64)
    if cfg["use_val_split"]:
        # early-stop on the REAL val split (split0). NOTE: selecting on val LEAKS the test set
        # (only the picked epoch); fine for v0 (not reported), but v1/v2 that REPORT AP should
        # switch back to in-train val + report val separately.
        train_idx = np.arange(X.shape[0])
        vX, vy, _ = dataset.load_pool(cfg["val_pool_dir"])
        vy = vy.astype(np.int64)
        vidx, val_scenes = np.arange(vX.shape[0]), "val_split(split0)"
        print(f"[data] train ALL {train_idx.size:,} pts | val = REAL val split {vX.shape[0]:,} pts "
              f"(⚠ selecting on test = leak)", flush=True)
    else:
        train_idx, vidx, val_scenes = dataset.scene_split(scene, cfg["n_val_scenes"], seed)
        vX, vy = X, y                                    # in-val indexes the same train pool
        print(f"[data] pool {X.shape[0]:,} pts | train {train_idx.size:,} | "
              f"in-val {vidx.size:,} ({len(val_scenes)} scenes held out)", flush=True)

    # --- model / loss / optim ---
    model = build_model(cfg["model"], **cfg["model_kwargs"]).to(dev)
    crit, w = losses.build_loss(y[train_idx], cfg["weight_scheme"], cfg["focal_gamma"])
    crit = crit.to(dev)                               # moves weight buffer too
    opt = torch.optim.AdamW(model.parameters(), lr=cfg["lr"], weight_decay=cfg["weight_decay"])
    warm, epochs = cfg["warmup_epochs"], cfg["epochs"]

    def lr_mult(ep: int) -> float:
        if ep < warm:
            return (ep + 1) / max(1, warm)
        prog = (ep - warm) / max(1, epochs - warm)
        return 0.5 * (1 + math.cos(math.pi * prog))   # cosine to 0
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_mult)
    scaler = torch.amp.GradScaler("cuda")

    # provenance + config snapshot
    pmp = os.path.join(os.path.expanduser(cfg["pool_dir"]), "pool_meta.json")
    pool_meta = json.load(open(pmp)) if os.path.exists(pmp) else {}
    json.dump({**cfg, "val_scenes": val_scenes, "class_weights": w.tolist(),
               "feat_provenance": pool_meta.get("feat_provenance")},
              open(os.path.join(run_dir, "config.json"), "w"), indent=2)

    steps = max(1, train_idx.size // cfg["batch"])
    mlog = open(os.path.join(run_dir, "metrics.jsonl"), "w")
    best, best_ep, patience = -1.0, -1, 0
    t0 = time.time()
    for ep in range(epochs):
        model.train()
        running = 0.0
        for _ in range(steps):
            bi = train_idx[rng.integers(0, train_idx.size, cfg["batch"])]
            xb = torch.from_numpy(np.asarray(X[bi])).to(dev).float()
            yb = torch.from_numpy(y[bi]).to(dev)
            with torch.amp.autocast("cuda", dtype=torch.float16):
                loss = crit(model(xb), yb)
            scaler.scale(loss).backward()
            scaler.step(opt); scaler.update(); opt.zero_grad(set_to_none=True)
            running += loss.item()
        sched.step()
        rec = {"epoch": ep, "lr": opt.param_groups[0]["lr"], "train_loss": running / steps}

        if vidx.size and ep % cfg["eval_every"] == 0:
            m = evaluate(model, vX, vy, vidx, dev)
            gate = metrics.go_no_go(m)
            rec.update({"val": m, "gate": gate})
            score = m[cfg["select_metric"]]
            if score > best:
                best, best_ep, patience = score, ep, 0
                torch.save({"model": model.state_dict(), "epoch": ep, "score": score,
                            "config": cfg, "class_weights": w.tolist(),
                            "feat_provenance": pool_meta.get("feat_provenance")},
                           os.path.join(run_dir, "best.pt"))
            else:
                patience += 1
            print(f"  ep{ep:02d} loss {rec['train_loss']:.4f}  fg-mIoU {m['miou_fg']:.3f}  "
                  f"aff-rec {m['affordance']['recall']:.3f}  [{gate['verdict']}]  "
                  f"best {best:.3f}@{best_ep}  ({time.time() - t0:.0f}s)", flush=True)
        mlog.write(json.dumps(rec) + "\n"); mlog.flush()
        torch.save({"model": model.state_dict(), "epoch": ep}, os.path.join(run_dir, "last.pt"))
        if patience >= cfg["early_stop_patience"]:
            print(f"[early-stop] no {cfg['select_metric']} gain for {patience} evals", flush=True)
            break
    mlog.close()
    print(f"[done] best {cfg['select_metric']}={best:.3f} @ep{best_ep}  -> {run_dir}", flush=True)


if __name__ == "__main__":
    main()
