"""scene_train.py — v1 per-scene training (PTv3 dual-head). COMPUTE node, single GPU.

STEP2 = semantic-only (lambda_offset=0): does PTv3 + balanced-softmax beat v0's natural
point-level prec/rec (0.53 / 0.39)? Offset head exists but is trained only when --lambda_offset>0
(step3). One scene = one batch (PT needs the full neighborhood). Large scenes are CROPPED to a
fixed voxel budget — both for spconv's int32 GEMM limit AND for GPU memory (1cm 1.4M voxel ~48.6GB).

  # quick loop check (few scenes, 1 epoch)
  python src/train/scene_train.py --run v1_smoke --device cuda:0 --epochs 1 --max_scenes 8
  # real run
  python src/train/scene_train.py --run v1_ptv3_sem --device cuda:0 --epochs 40

Reads train_set.csv (200 train scenes); holds out --val_scenes WHOLE scenes for in-train val
(point-level, by scene -> no leak). Final instance AP is a separate step (predict.py).
"""
from __future__ import annotations
import os, sys, math, json, time, argparse
import numpy as np
import torch

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import CODE, LABEL_CACHE, RUNS, SCENEFUN3D  # noqa: E402
sys.path.insert(0, os.path.join(CODE, "task1"))
from data.scene_io import load_scene, grid_sample, offset_target, FEAT_DIR   # noqa: E402
from models import build_model                                      # noqa: E402
from losses import balanced_softmax_ce, offset_loss                 # noqa: E402 — flat: this file's dir (src/train) is on sys.path; `train.losses` would hit v0's train.py module

DATA_ROOT = SCENEFUN3D
BFL = os.path.join(DATA_ROOT, "benchmark_file_lists")
LABEL_DIR = LABEL_CACHE
CLASS_NAMES = {1: "rotate", 2: "key_press", 3: "tip_push", 4: "hook_pull", 5: "pinch_pull",
               6: "hook_turn", 7: "foot_push", 8: "plug_in", 9: "unplug"}


def read_visits(csv_name: str) -> list[str]:
    with open(os.path.join(BFL, csv_name)) as f:
        return sorted({ln.split(",")[0] for ln in f if ln.strip()})


def scan_train(visits: list[str]):
    """One cheap pass over train LABELS (cls only): global class counts -> natural log-prior;
    and which scenes have >=1 affordance point (skip all-bg scenes in training)."""
    cnt = np.zeros(10, dtype=np.float64)
    with_fg = []
    for v in visits:
        lp = os.path.join(LABEL_DIR, f"{v}.npz")
        fp = os.path.join(FEAT_DIR, f"{v}.npz")
        if not (os.path.exists(lp) and os.path.exists(fp)):
            continue                                     # CSV header ("visit_id") / missing scene -> skip
        with np.load(lp) as ld:
            cls = ld["cls"]
        c = cls[cls != 255]
        cnt += np.bincount(c, minlength=10)
        if ((cls >= 1) & (cls <= 9)).any():
            with_fg.append(v)
    pi = cnt / cnt.sum()
    log_prior = np.log(pi + 1e-12).astype(np.float32)
    return log_prior, with_fg


def crop(vox: dict, budget: int, rng) -> dict:
    """If voxels > budget, keep the `budget` nearest to a random seed (a contiguous spatial
    blob -> PT neighborhood intact). Random seed -> different crop each epoch (augmentation)."""
    n = vox["cls"].shape[0]
    if n <= budget:
        return vox
    xyz = vox["xyz"]
    seed = int(rng.integers(n))
    d = ((xyz - xyz[seed]) ** 2).sum(1)
    keep = np.argpartition(d, budget)[:budget]
    return {k: (val[keep] if k != "inv" else val) for k, val in vox.items()}


def augment_xyz(xyz: np.ndarray, rng) -> np.ndarray:
    """Train-only geometric augmentation on COORD ONLY — feat is DINOv2 (view-invariant), never
    touched (red line). z-rotation (indoor gravity-aligned) + uniform scale + x/y flip + jitter."""
    x = xyz.astype(np.float32, copy=True)
    t = rng.uniform(0, 2 * np.pi); c, s = np.cos(t), np.sin(t)
    x[:, :2] = x[:, :2] @ np.array([[c, -s], [s, c]], np.float32).T   # rotate about gravity (z)
    x *= rng.uniform(0.9, 1.1)                                        # global scale
    if rng.random() < 0.5: x[:, 0] = -x[:, 0]                         # flip x
    if rng.random() < 0.5: x[:, 1] = -x[:, 1]                         # flip y
    x += rng.normal(0.0, 0.01, x.shape).astype(np.float32)           # jitter (~1cm)
    return x


def to_tensors(vox: dict, dev, want_offset: bool, augment: bool = False, rng=None):
    xyz = augment_xyz(vox["xyz"], rng) if augment else vox["xyz"]    # train-only; eval keeps augment=False
    coord = torch.from_numpy(xyz - xyz.mean(0)).float().to(dev)
    feat = torch.from_numpy(vox["feat"].astype(np.float32)).to(dev)
    cls = torch.from_numpy(vox["cls"].astype(np.int64)).to(dev)
    off_t = torch.tensor([coord.shape[0]], device=dev)
    gt_off = None
    if want_offset:
        gt_off = torch.from_numpy(offset_target(xyz, vox["cls"], vox["inst"])).to(dev)
    return coord, feat, cls, gt_off, off_t


def load_voxels(v: str, grid_size: float, budget: int, rng, voxel_dir: str = "") -> dict:
    """ONE scene -> voxels -> crop. With voxel_dir: read the 0.01 voxel cache (local scratch, fast),
    coarsen further if grid_size>0.01; else read raw scene from NFS (load_scene ~24GB feat)."""
    if voxel_dir:
        d = np.load(os.path.join(voxel_dir, f"{v}.npz"))
        vox = dict(xyz=d["xyz"], feat=d["feat"], cls=d["cls"], inst=d["inst"], inv=None)
        if grid_size > 0.0101:                              # cache is 0.01; re-GridSample to coarser
            vox = grid_sample(vox["xyz"], vox["feat"], vox["cls"], vox["inst"], grid_size)
    else:
        s = load_scene(v)
        vox = grid_sample(s["xyz"], s["feat"], s["cls"], s["inst"], grid_size)
    return crop(vox, budget, rng)


@torch.no_grad()
def eval_pointwise(model, visits, log_prior, args, dev):
    """Point-level affordance prec/rec at TWO calibrations (so a single one doesn't misjudge PT;
    calibration is a sweepable knob, cf. v0 la_scale):
      cal = argmax(z + log π_nat) -> calibrated natural posterior; SAME convention as v0 best
            (logit_adjust la=1 -> the 0.53/0.39 numbers). <- PRIMARY go/no-go vs v0.
      raw = argmax(z)             -> aggressive / high-recall (over-predicts); == v0 la=0.
    per-class recall reported under `cal`. Val crops use a FIXED rng -> stable across epochs."""
    # spconv picks the Native conv under module.training=True but implicit_gemm under .eval(), and
    # the latter's tuner fails on PTv3's xCPE SubMConv3d (train used Native, worked). So eval with
    # convs in TRAIN mode (Native) but BN frozen (running stats, no update -> no val leakage) and
    # head dropout off. @torch.no_grad already keeps memory low.
    model.train()
    for mod in model.modules():
        if isinstance(mod, (torch.nn.BatchNorm1d, torch.nn.Dropout)) or type(mod).__name__ == "DropPath":
            mod.eval()                                   # freeze BN + dropout + PTv3 backbone DropPath(0.3)
    model.sem_head.eval(); model.offset_head.eval()
    rng = np.random.default_rng(0)
    acc = {"cal": [0, 0, 0], "raw": [0, 0, 0]}                    # [tp, fp, fn]
    cls_tp = np.zeros(10); cls_gt = np.zeros(10)
    for v in visits:
        vox = load_voxels(v, args.grid_size, args.crop_voxels, rng, args.voxel_dir)
        coord, feat, cls, _, off_t = to_tensors(vox, dev, want_offset=False)
        with torch.amp.autocast("cuda", enabled=args.amp):
            sem, _ = model(coord, feat, off_t)
        z = sem.float()
        m = cls != 255
        gt = cls[m]; fg_gt = gt >= 1
        for name, logits in (("cal", z + log_prior), ("raw", z)):
            fg_pp = (logits.argmax(1)[m]) >= 1
            acc[name][0] += int((fg_gt & fg_pp).sum())
            acc[name][1] += int((fg_pp & ~fg_gt).sum())
            acc[name][2] += int((fg_gt & ~fg_pp).sum())
        predc = (z + log_prior).argmax(1)[m]                     # per-class recall under `cal`
        for c in range(1, 10):
            gc = gt == c; cls_gt[c] += int(gc.sum()); cls_tp[c] += int((gc & (predc == c)).sum())
    model.train()
    out = {}
    for name, (tp, fp, fn) in acc.items():
        p = tp / max(tp + fp, 1); r = tp / max(tp + fn, 1)
        out[name] = {"prec": p, "rec": r, "f1": 2 * p * r / max(p + r, 1e-9)}
    out["per_class_rec_cal"] = {CLASS_NAMES[c]: (cls_tp[c] / cls_gt[c] if cls_gt[c] else float("nan"))
                                for c in range(1, 10)}
    return out


@torch.no_grad()
def eval_instance_ap(model, log_prior_np, grid_size, dev, tmp_dir):
    """In-training instance AP on the OFFICIAL val (gt_val 30): cal calibration, raw-xyz DBSCAN,
    full-scene forward (no crop) — the SAME metric/path as predict_v1, so best.pt is selected on
    the number we actually report (not point-f1). ~1-2 min/call; restores model.train() on exit."""
    from eval.predict_v1 import (forward_scene, cluster, run_eval, read_val_visits,
                                 rle_encode, softmax_max, eval_safe)
    torch.cuda.empty_cache()
    eval_safe(model)                                          # spconv Native + BN/dropout/DropPath frozen
    sub_dir = os.path.join(tmp_dir, "val_inst_ap"); mask_dir = os.path.join(sub_dir, "predicted_masks")
    os.makedirs(mask_dir, exist_ok=True)
    for v in read_val_visits():
        sem, _off, xyz_vox, inv, obs, n_full = forward_scene(model, v, dev, grid_size)
        prob, pred = softmax_max(sem + log_prior_np)          # cal = argmax(z + logπ)
        inst = cluster(pred, prob, xyz_vox, inv, obs, n_full, 0.05, 10, 20, 0.0)
        lines = []
        for k, ins in enumerate(inst):
            mf = f"{v}_{k:03d}.txt"
            with open(os.path.join(mask_dir, mf), "w") as fh:
                fh.write(rle_encode(ins["mask"]))
            lines.append(f"predicted_masks/{mf} {ins['cls']} {ins['conf']:.4f}")
        if not lines:
            mf = f"{v}_000.txt"; open(os.path.join(mask_dir, mf), "w").write("")
            lines.append(f"predicted_masks/{mf} 1 0.0")
        with open(os.path.join(sub_dir, f"{v}.txt"), "w") as fh:
            fh.write("\n".join(lines))
    out = run_eval(sub_dir)
    model.train()                                             # restore training mode
    for ln in out.splitlines():
        if ln.strip().startswith("average"):
            return float(ln.split()[2])
    return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--weight_decay", type=float, default=1e-2)
    ap.add_argument("--grad_clip", type=float, default=1.0, help="max grad norm (divergence guard; 0=off)")
    ap.add_argument("--warmup_frac", type=float, default=0.03)
    ap.add_argument("--grid_size", type=float, default=0.01)
    ap.add_argument("--crop_voxels", type=int, default=1_000_000, help="int32+memory budget (~1.4M=48.6GB)")
    ap.add_argument("--voxel_dir", default="", help="precache_voxels output (job scratch); empty=read NFS raw")
    ap.add_argument("--proj_dim", type=int, default=64, help="1024->proj_dim before PTv3; the capacity knob, and what keeps spconv's "
                         "int32 GEMM from overflowing")
    ap.add_argument("--lambda_offset", type=float, default=0.0, help="0 = step2 sem-only; >0 = step3")
    ap.add_argument("--l1_weight", type=float, default=1.0, help="offset l1 vs directional loss weight; l1 is in metres and is "
                         "easily drowned out")
    ap.add_argument("--init", default="", help="step3: warm-start model weights from a step2 ckpt")
    ap.add_argument("--freeze_backbone", action="store_true", help="step3: train ONLY offset_head (keep sem exact)")
    ap.add_argument("--val_scenes", type=int, default=0, help="0=train all 200, select best by official-val instance AP; >0 also keeps N in-val scenes for a point-f1 monitor")
    ap.add_argument("--eval_every", type=int, default=2)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--amp", action="store_true", default=True)
    ap.add_argument("--no_amp", dest="amp", action="store_false")
    ap.add_argument("--no_flash", dest="enable_flash", action="store_false", default=True)
    ap.add_argument("--max_scenes", type=int, default=0, help=">0 caps scenes/epoch (loop check)")
    ap.add_argument("--augment", type=int, default=0, help="1=train-time coord aug (rot/scale/flip/jitter); 0=reproduce C_v2 no-aug")
    args = ap.parse_args()
    dev = torch.device(args.device)
    torch.manual_seed(args.seed)
    rng = np.random.default_rng(args.seed)
    out_dir = os.path.join(RUNS, args.run); os.makedirs(out_dir, exist_ok=True)

    all_train = read_visits("train_set.csv")
    log_prior_np, with_fg = scan_train(all_train)
    log_prior = torch.from_numpy(log_prior_np).to(dev)
    val_visits = with_fg[:args.val_scenes]                       # held out by SCENE (no leak)
    train_visits = with_fg[args.val_scenes:]
    print(f"[split] {len(with_fg)} train-with-fg | train {len(train_visits)} / in-val {len(val_visits)} "
          f"| prior(bg {log_prior_np[0]:.2f}, aff mean {log_prior_np[1:].mean():.2f})", flush=True)

    if args.voxel_dir and not os.path.exists(os.path.join(args.voxel_dir, "DONE")):
        raise SystemExit(f"[abort] {args.voxel_dir}/DONE missing — precache not ready or wrong node")
    model = build_model("v1_ptv3", grid_size=args.grid_size, proj_dim=args.proj_dim,
                        enable_flash=args.enable_flash).to(dev)
    if args.init:                                             # step3: warm-start sem from a step2 ckpt
        ic = torch.load(args.init, map_location=dev, weights_only=False)
        model.load_state_dict(ic["model"]); print(f"[init] warm-start from {args.init}", flush=True)
    if args.freeze_backbone:                                  # step3: keep sem EXACT, train only offset_head
        for p in model.parameters(): p.requires_grad_(False)
        for p in model.offset_head.parameters(): p.requires_grad_(True)
        print("[freeze] backbone+sem frozen; training offset_head only", flush=True)
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],
                            lr=args.lr, weight_decay=args.weight_decay)
    n_per_epoch = args.max_scenes or len(train_visits)
    total = args.epochs * n_per_epoch
    warm = max(1, int(args.warmup_frac * total))
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: s / warm if s < warm
                                              else 0.5 * (1 + math.cos(math.pi * (s - warm) / max(1, total - warm))))
    scaler = torch.amp.GradScaler("cuda", enabled=args.amp)
    print(f"[model] {sum(p.numel() for p in model.parameters())/1e6:.1f}M | flash={args.enable_flash} "
          f"amp={args.amp} | total_steps {total} warmup {warm}", flush=True)

    mlog = open(os.path.join(out_dir, "metrics.jsonl"), "w")
    best_ap = -1.0
    step = 0
    for ep in range(args.epochs):
        order = rng.permutation(len(train_visits))
        if args.max_scenes:
            order = order[:args.max_scenes]
        model.train()
        run_loss = run_sem = run_off = run_l1 = run_ldir = 0.0
        t0 = time.time()
        for j, vi in enumerate(order):
            v = train_visits[vi]
            vox = load_voxels(v, args.grid_size, args.crop_voxels, rng, args.voxel_dir)
            coord, feat, cls, gt_off, off_t = to_tensors(vox, dev, want_offset=args.lambda_offset > 0,
                                                         augment=bool(args.augment), rng=rng)
            opt.zero_grad()
            with torch.amp.autocast("cuda", enabled=args.amp):
                sem, pred_off = model(coord, feat, off_t)
                lsem = balanced_softmax_ce(sem, cls, log_prior)
                loff = torch.zeros((), device=dev); l1 = ldir = 0.0
                if args.lambda_offset > 0:
                    loff, l1, ldir = offset_loss(pred_off, gt_off, (cls >= 1) & (cls <= 9),
                                                 l1_weight=args.l1_weight)
                loss = lsem + args.lambda_offset * loff
            scaler.scale(loss).backward()
            if args.grad_clip > 0:                              # divergence guard: two configs blew up numerically at epoch 9 -> index OOB
                scaler.unscale_(opt)
                torch.nn.utils.clip_grad_norm_(model.parameters(), args.grad_clip)
            scaler.step(opt); scaler.update(); sched.step(); step += 1
            run_loss += float(loss); run_sem += float(lsem); run_off += float(loff)
            run_l1 += float(l1); run_ldir += float(ldir)
        nb = len(order)
        print(f"[ep {ep:3d}] loss {run_loss/nb:.4f} (sem {run_sem/nb:.4f} off {run_off/nb:.4f} "
              f"l1 {run_l1/nb:.4f} dir {run_ldir/nb:.4f}) lr {sched.get_last_lr()[0]:.2e} {time.time()-t0:.0f}s", flush=True)

        rec = {"epoch": ep, "train_loss": run_loss / nb, "train_sem": run_sem / nb, "train_off": run_off / nb}
        if (ep + 1) % args.eval_every == 0 or ep == args.epochs - 1:
            ap_inst = eval_instance_ap(model, log_prior_np, args.grid_size, dev, out_dir)
            rec["val_inst_ap"] = ap_inst
            msg = f"        [val] instance AP {ap_inst:.3f} (official val 30) | vs C_v2 18.25"
            if val_visits:                                      # optional in-val point-f1 monitor
                m = eval_pointwise(model, val_visits, log_prior, args, dev)
                rec.update(m); msg += f" | in-val cal f1 {m['cal']['f1']:.3f}"
            print(msg, flush=True)
            ckpt = {"model": model.state_dict(), "optimizer": opt.state_dict(), "epoch": ep,
                    "val_inst_ap": ap_inst, "args": vars(args), "log_prior": log_prior_np.tolist()}
            torch.save(ckpt, os.path.join(out_dir, "last.pt"))
            if ap_inst > best_ap:                               # best by INSTANCE AP on official val
                best_ap = ap_inst
                torch.save(ckpt, os.path.join(out_dir, "best.pt"))
                print(f"        [best] instance AP {best_ap:.3f} -> best.pt", flush=True)
        mlog.write(json.dumps(rec) + "\n"); mlog.flush()
    mlog.close()
    print(f"[done] best instance AP {best_ap:.3f} -> {out_dir}", flush=True)


if __name__ == "__main__":
    main()
