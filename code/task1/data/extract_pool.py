#!/usr/bin/env python3
"""extract_pool.py -- build the balanced point pool for func_seg v0 training (COMPUTE node).

v0 treats points independently, so we pre-extract ONE balanced pool from the TRAIN
split (split1, 200 scenes) and never touch the 1.6TB feature cache again during training:
  - ALL affordance points (cls 1..9)         -- the scarce signal, keep every one
  - bg_mult x bg points PER SCENE (cls==0)    -- per-scene sampling keeps each room's
                                                 background represented (-> ~30:1 global)
  - exclude points (cls==255) dropped entirely (they are ignore_index at train time)

Output (cache/pools/func_seg/):
  pool_X.npy     (N,1024) fp16  -- features, .npy so training can np.load(mmap_mode='r')
  pool_y.npy     (N,)     uint8 -- class 0=bg, 1..9
  pool_xyz.npy   (N,3)    fp32  -- world xyz = P_full[observed_idx]; v1/v2 coords, v0 ignores it
                                   (kept SEPARATE from feat: PTv3 takes coord & feat as distinct
                                    inputs, not a concatenated 1027-vector). Skip with --skip_xyz.
  pool_scene.npy (N,)     uint16 -- index into meta['visits'] (provenance / per-scene split)
  pool_meta.json                -- provenance + per-class counts (sanity vs probe_stats)

Memory: host ~792GB RAM, max scene feat ~24GB -> just load each scene, take the subset,
concatenate in RAM. Peak is during np.concatenate (X_list + X coexist ~= 2x pool ~86GB),
still far below RAM, so no open_memmap gymnastics needed here.
Read-only on the feature/label cache; writes only under --out_dir.
"""
from __future__ import annotations
import os, sys, json, argparse, time
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import CODE, FEATURE_CACHE, LABEL_CACHE, POOL_CACHE, SCENEFUN3D  # noqa: E402
sys.path.insert(0, os.path.join(CODE, "task1", "features"))
from data_io import load_pointcloud   # noqa: E402 — reuse lift loader; observed_idx is FULL-scan space

CLASS_NAMES = {1: "rotate", 2: "key_press", 3: "tip_push", 4: "hook_pull", 5: "pinch_pull",
               6: "hook_turn", 7: "foot_push", 8: "plug_in", 9: "unplug"}


def read_visits(bfl: str, csv_name: str) -> list[str]:
    with open(os.path.join(bfl, csv_name)) as f:
        return sorted({ln.split(",")[0] for ln in f if ln.strip()})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_root", default=SCENEFUN3D)
    ap.add_argument("--feat_dir", default=FEATURE_CACHE)
    ap.add_argument("--label_dir", default=LABEL_CACHE)
    ap.add_argument("--out_dir", default=POOL_CACHE)
    ap.add_argument("--split", default="train", choices=["train", "val", "all"],
                    help="train=split1(200); v0 trains on TRAIN only, val is held for eval")
    ap.add_argument("--bg_mult", type=int, default=30, help="bg:fg ratio per scene")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--overwrite", action="store_true", help="rebuild even if pool files exist")
    ap.add_argument("--skip_xyz", action="store_true",
                    help="feat-only pool; skip reading laser-scan ply for per-point xyz (v1/v2 need xyz)")
    args = ap.parse_args()

    bfl = os.path.join(args.data_root, "benchmark_file_lists")
    csv = {"train": "train_set.csv", "val": "val_set.csv", "all": "train_val_set.csv"}[args.split]
    visits = read_visits(bfl, csv)
    rng = np.random.default_rng(args.seed)
    os.makedirs(args.out_dir, exist_ok=True)
    pool_X_path = os.path.join(args.out_dir, "pool_X.npy")
    if os.path.exists(pool_X_path) and not args.overwrite:
        raise SystemExit(f"[abort] {pool_X_path} exists; pass --overwrite to rebuild "
                         f"(don't clobber a pool a training run may be mmap-reading)")
    print(f"[extract_pool] split={args.split} ({len(visits)} scenes) bg_mult={args.bg_mult} "
          f"seed={args.seed} xyz={not args.skip_xyz}", flush=True)

    X_list, y_list, s_list, xyz_list = [], [], [], []
    per_cls = {c: 0 for c in range(1, 10)}
    n_bg_total = 0
    n_nofg = 0
    used_visits: list[str] = []
    feat_prov: dict | None = None
    t0 = time.time()
    for i, v in enumerate(visits):
        fp = os.path.join(args.feat_dir, f"{v}.npz")
        lp = os.path.join(args.label_dir, f"{v}.npz")
        if not (os.path.exists(fp) and os.path.exists(lp)):
            print(f"  [skip {v}] missing feat or label"); continue
        with np.load(lp) as ld:                                # read small label first
            cls = ld["cls"]                                    # (K,) uint8
        fg = np.nonzero((cls >= 1) & (cls <= 9))[0]            # affordance only
        if fg.size == 0:                                       # functional parts fully unobserved
            n_nofg += 1
            print(f"  [no-fg {v}] 0 affordance points -> skipped from pool")
            continue
        t_load = time.time()
        with np.load(fp) as fd:                                # only now pay the ~24GB feat load
            feat = fd["feat"]                                  # (K,1024) fp16, materialized
            obs = None if args.skip_xyz else fd["observed_idx"]  # (K,) FULL-scan idx, row i <-> feat[i]
            prov = {k: fd[k].item() for k in ("model", "stride", "target_long_side") if k in fd.files}
        # guard: label cache must align 1:1 with the CURRENT lift (we re-ran lift --overwrite before);
        # a K mismatch means labels were built against a stale lift -> rebuild labels, do NOT train.
        assert feat.shape[0] == cls.shape[0], \
            f"{v}: feat K={feat.shape[0]} != label K={cls.shape[0]} -- the label cache disagrees with the current lift; rebuild labels"
        if feat_prov is None:
            feat_prov = prov
        elif prov != feat_prov:                               # don't silently mix backbones/strides
            raise ValueError(f"{v}: feat provenance {prov} != {feat_prov} -- the cache mixes different backbones or strides")
        bg = np.nonzero(cls == 0)[0]                           # exclude (255) dropped
        n_bg = min(bg.size, args.bg_mult * fg.size)
        bg_s = rng.choice(bg, size=n_bg, replace=False) if n_bg < bg.size else bg
        idx = np.sort(np.concatenate([fg, bg_s]))             # sorted -> sequential gather on the 24GB array
        si = len(used_visits)
        X_list.append(feat[idx])                              # fancy index already returns a fresh array
        y_list.append(cls[idx])
        s_list.append(np.full(idx.size, si, dtype=np.uint16))
        ply_dt = 0.0
        if not args.skip_xyz:                                 # xyz = P_full[obs[idx]] (v1/v2 coords)
            t_ply = time.time()
            P_full = load_pointcloud(args.data_root, v)["P_full"]   # (N_full,3); reads laser-scan ply
            ply_dt = time.time() - t_ply
            assert int(obs.max()) < P_full.shape[0], \
                f"{v}: observed_idx max {int(obs.max())} >= ply N {P_full.shape[0]} — lift/ply mismatch"
            xyz_list.append(P_full[obs[idx]].astype(np.float32))    # same points/order as feat[idx]
            del P_full
        used_visits.append(v)
        cl = cls[fg]
        for c in range(1, 10):
            per_cls[c] += int((cl == c).sum())
        n_bg_total += int(bg_s.size)
        del feat                                               # release the (K,1024) array
        print(f"  [{i + 1}/{len(visits)}] {v}  K={len(cls):,} fg={fg.size:,}  "
              f"scene {time.time() - t_load:.1f}s (ply {ply_dt:.1f}s)  cum {time.time() - t0:.0f}s",
              flush=True)

    X = np.concatenate(X_list); del X_list
    y = np.concatenate(y_list); del y_list
    s = np.concatenate(s_list); del s_list
    N = int(X.shape[0])
    n_fg = int((y >= 1).sum())

    np.save(pool_X_path, X)
    np.save(os.path.join(args.out_dir, "pool_y.npy"), y)
    np.save(os.path.join(args.out_dir, "pool_scene.npy"), s)
    xyz_nbytes = 0
    if not args.skip_xyz:
        XYZ = np.concatenate(xyz_list); del xyz_list          # (N,3) fp32, aligned to pool_X rows
        assert XYZ.shape[0] == N, f"xyz rows {XYZ.shape[0]} != pool rows {N}"
        np.save(os.path.join(args.out_dir, "pool_xyz.npy"), XYZ)
        xyz_nbytes = XYZ.nbytes
    meta = {"split": args.split, "bg_mult": args.bg_mult, "seed": args.seed,
            "n_points": N, "n_fg": n_fg, "n_bg": int(n_bg_total),
            "bg_fg_ratio": round(n_bg_total / max(n_fg, 1), 2),
            "feat_dim": int(X.shape[1]), "feat_dtype": str(X.dtype), "has_xyz": not args.skip_xyz,
            "per_class": {CLASS_NAMES[c]: per_cls[c] for c in range(1, 10)},
            "n_scenes": len(used_visits), "n_scenes_nofg": n_nofg, "visits": used_visits,
            "feat_provenance": feat_prov,
            "feat_dir": args.feat_dir, "label_dir": args.label_dir}
    with open(os.path.join(args.out_dir, "pool_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    gb = (X.nbytes + y.nbytes + s.nbytes + xyz_nbytes) / 1e9
    print(f"\n=== pool built ({time.time() - t0:.0f}s) ===")
    print(f"  scenes {len(used_visits)} used, {n_nofg} skipped (0 fg) | points {N:,} "
          f"(fg {n_fg:,} + bg {n_bg_total:,}, ratio {n_bg_total / max(n_fg, 1):.1f}:1) | {gb:.1f} GB on disk")
    print(f"  {'class':<12}{'points':>13}")
    for c in range(1, 10):
        print(f"  {CLASS_NAMES[c]:<12}{per_cls[c]:>13,}")
    print(f"  -> {args.out_dir}")


if __name__ == "__main__":
    main()
