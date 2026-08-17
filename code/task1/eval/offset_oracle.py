#!/usr/bin/env python3
"""offset_oracle.py — de-risk: is skipping DBSCAN (offset-grouping) worth it? (sprint §4 step0)

ALL modes use GT per-point class (isolates instancing from the semantic head). Only the
instancing differs, so the AP deltas are pure instancing-paradigm signal:

  perfect_inst : group observed points by GT instance id directly (no clustering).
                 -> CEILING given we only predict on observed points; the 100->this gap is
                    the unobserved-point FN ceiling (unfixable by us, baseline §0).
  offset       : shift every point to its GT-instance centroid (= a PERFECT offset head),
                 then the SAME per-class DBSCAN -> UPPER BOUND of the offset-grouping paradigm.
                 Residual failure = two same-class instances whose centroids are < eps apart.
  dbscan       : per-class DBSCAN on RAW xyz (= the current oracle, AP ~71) -> baseline to beat.

DECISION (sprint §1, the 68-vs-9 account):
  offset - dbscan  ~0  -> skipping DBSCAN buys nothing -> DON'T build an offset head (defer to v2).
  offset - dbscan large (esp. plug_in/unplug, the merge victims @ oracle 39/38) -> the ~9-pt
                          instancing gap is real and offset-grouping is the cheap way to take it.

GT encoding (prepare_gt_val_data.py): full-scan uint32 = class_id*1000 + instance_idx + 1, so
the integer value g uniquely identifies an instance (g//1000 = class, g>=1000 = affordance).

Light: NO feat, NO model, NO torch — just observed_idx + ply(P_full) + gt_val per scene + sklearn.
Reads ~30 ply over NFS -> run on a COMPUTE node (env: gs), not the gateway.

Persistent output (NOT just stdout, which is lost):
  results/func_seg/offset_oracle/OFFSET_ORACLE.md   <- the re-readable summary (headline + per-class + verdict)
  results/func_seg/offset_oracle/eval_<mode>.txt    <- raw official evaluate stdout per mode
  results/func_seg/offset_oracle/<mode>_submission/ <- submissions (re-evaluable)

  python src/eval/offset_oracle.py                          # all 3 modes, default postproc
  python src/eval/offset_oracle.py --modes offset,dbscan    # subset
"""
from __future__ import annotations
import os, sys, argparse, subprocess, datetime
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))                  # src/eval
_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _CODE_ROOT)
from paths import FEATURE_CACHE, GT_VAL, SCENEFUN3D, TASK1, TOOLKIT  # noqa: E402
sys.path.insert(0, HERE)                                           # instance
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "lift"))    # data_io
sys.path.insert(0, TOOLKIT)                                        # eval...rle
import instance as inst                                            # noqa: E402
from data_io import load_pointcloud                                # noqa: E402
from eval.functionality_segmentation.eval_utils.rle import rle_encode  # noqa: E402

FEAT_DIR = FEATURE_CACHE  # only observed_idx is read
DATA_ROOT = SCENEFUN3D
RESULTS = TASK1
OUT_DIR = os.path.join(RESULTS, "offset_oracle")
CLASS_NAMES = {1: "rotate", 2: "key_press", 3: "tip_push", 4: "hook_pull", 5: "pinch_pull",
               6: "hook_turn", 7: "foot_push", 8: "plug_in", 9: "unplug"}
ALL_MODES = ("perfect_inst", "offset", "dbscan")


def read_val_visits() -> list[str]:
    # key on the GT dir so submission scenes match exactly what evaluate.py iterates over.
    return sorted(f[:-4] for f in os.listdir(GT_VAL) if f.endswith(".txt"))


def load_oracle_scene(visit: str):
    """Returns (cls (K,), gid (K,), obs (K,), xyz (K,3), n_full) on observed points.
    cls = GT class 1..9 (0 = bg/exclude); gid = full encoded value (unique instance key, 0 = bg)."""
    with np.load(os.path.join(FEAT_DIR, f"{visit}.npz")) as fd:    # lazy: reads ONLY observed_idx
        obs = fd["observed_idx"]
    P_full = load_pointcloud(DATA_ROOT, visit)["P_full"]
    n_full = P_full.shape[0]
    xyz = P_full[obs].astype(np.float32)
    g = np.loadtxt(os.path.join(GT_VAL, f"{visit}.txt"), dtype=np.uint32)
    gobs = g[obs]
    aff = gobs >= 1000                                             # affordance points (exclude/bg drop out)
    cls = np.where(aff, gobs // 1000, 0).astype(np.int64)
    gid = np.where(aff, gobs, 0).astype(np.int64)
    return cls, gid, obs, xyz, n_full


def inst_perfect(cls, gid, obs, xyz, n_full, min_cluster):
    """One instance per GT instance id (no clustering) -> observed-only ceiling."""
    out = []
    for uid in np.unique(gid):
        if uid == 0:
            continue
        members = np.nonzero(gid == uid)[0]
        if members.size < min_cluster:                            # same size gate as DBSCAN modes
            continue
        mask = np.zeros(n_full, dtype=np.uint8)
        mask[obs[members]] = 1
        out.append({"mask": mask, "cls": int(uid // 1000), "conf": 1.0})
    return out


def inst_offset(cls, gid, obs, xyz, n_full, eps, min_samples, min_cluster):
    """Perfect offset: collapse every point onto its GT-instance centroid, then SAME per-class
    DBSCAN. Identical params to `dbscan` mode -> the only difference is raw vs shifted coords."""
    xyz_s = xyz.copy()
    for uid in np.unique(gid):
        if uid == 0:
            continue
        m = gid == uid
        xyz_s[m] = xyz[m].mean(axis=0)
    prob = np.ones(cls.shape[0], dtype=np.float32)
    return inst.cluster_instances(cls, prob, obs, xyz_s, n_full, eps=eps,
                                  min_samples=min_samples, min_cluster=min_cluster)


def inst_dbscan(cls, gid, obs, xyz, n_full, eps, min_samples, min_cluster):
    """Current oracle: per-class DBSCAN on raw xyz."""
    prob = np.ones(cls.shape[0], dtype=np.float32)
    return inst.cluster_instances(cls, prob, obs, xyz, n_full, eps=eps,
                                  min_samples=min_samples, min_cluster=min_cluster)


def write_submission(mode: str, per_scene: dict[str, list]) -> str:
    """Write masks + per-scene txt in official submission format; returns the submission dir.
    Mirrors predict.py incl. the empty-scene dummy row so evaluate.py never crashes on np.loadtxt."""
    sub_dir = os.path.join(OUT_DIR, f"{mode}_submission")
    mask_dir = os.path.join(sub_dir, "predicted_masks")
    os.makedirs(mask_dir, exist_ok=True)
    for v, instances in per_scene.items():
        lines = []
        for k, ins in enumerate(instances):
            mfile = f"{v}_{k:03d}.txt"
            with open(os.path.join(mask_dir, mfile), "w") as f:
                f.write(rle_encode(ins["mask"]))
            lines.append(f"predicted_masks/{mfile} {ins['cls']} {ins['conf']:.4f}")
        if not lines:                                             # zero-instance scene -> dummy empty mask
            mfile = f"{v}_000.txt"
            with open(os.path.join(mask_dir, mfile), "w") as f:
                f.write("")
            lines.append(f"predicted_masks/{mfile} 1 0.0")
        with open(os.path.join(sub_dir, f"{v}.txt"), "w") as f:
            f.write("\n".join(lines))
    return sub_dir


def run_official(sub_dir: str) -> str:
    """Run the official evaluate.py from the toolkit root; return its full stdout (the per-class table)."""
    res = subprocess.run([sys.executable, "-m", "eval.functionality_segmentation.evaluate",
                          "--pred_dir", sub_dir, "--gt_dir", GT_VAL],
                         cwd=TOOLKIT, capture_output=True, text=True)
    return res.stdout + ("\n=== stderr ===\n" + res.stderr if res.stderr.strip() else "")


def parse_official(stdout: str) -> dict[str, tuple[float, float, float]]:
    """Parse print_results() table -> {'average': (ap,ap50,ap25), 'rotate': (...), ...}."""
    want = set(CLASS_NAMES.values()) | {"average"}
    out: dict[str, tuple[float, float, float]] = {}
    for line in stdout.splitlines():
        if ":" not in line:
            continue
        left, _, right = line.partition(":")
        name = left.strip()
        if name not in want:
            continue
        nums = right.split()
        if len(nums) != 3:
            continue
        try:
            out[name] = tuple(float(x) for x in nums)             # (ap, ap50, ap25)
        except ValueError:
            continue
    return out


def fmt(v):
    return f"{v:.3f}" if v is not None else "  -  "


def write_summary(parsed: dict[str, dict], args, n_scenes: int):
    """Write the re-readable markdown summary: headline + gap decomposition + per-class + verdict."""
    ap = {m: parsed.get(m, {}).get("average", (None, None, None))[0] for m in ALL_MODES}
    lines = []
    lines.append("# offset oracle — does skipping DBSCAN buy anything? (sprint §4 step0)\n")
    lines.append(f"> generated {datetime.datetime.now().isoformat(timespec='seconds')} | "
                 f"val scenes {n_scenes} | eps={args.eps} min_samples={args.min_samples} "
                 f"min_cluster={args.min_cluster}")
    lines.append("> ALL modes use GT per-point cls -> AP deltas are pure instancing-paradigm signal.\n")

    lines.append("## Headline (AP / AP50 / AP25)")
    lines.append("| mode | AP | AP50 | AP25 | isolates |")
    lines.append("|---|---|---|---|---|")
    desc = {"perfect_inst": "observed-only ceiling (100→ gap = unobserved-pt FN)",
            "offset": "UPPER BOUND of a perfect offset head",
            "dbscan": "current oracle (raw-xyz DBSCAN), baseline to beat"}
    for m in ALL_MODES:
        a = parsed.get(m, {}).get("average", (None, None, None))
        lines.append(f"| {m} | {fmt(a[0])} | {fmt(a[1])} | {fmt(a[2])} | {desc[m]} |")
    lines.append("")

    # gap decomposition (only if all three present)
    if all(ap[m] is not None for m in ALL_MODES):
        lines.append("## Gap decomposition (AP)")
        lines.append(f"- 100 → perfect_inst : **{100 - ap['perfect_inst']:+.2f}**  "
                     f"(unobserved points; unfixable by us)")
        lines.append(f"- perfect_inst → offset : **{ap['offset'] - ap['perfect_inst']:+.2f}**  "
                     f"(residual: adjacent centroids < eps)")
        lines.append(f"- offset → dbscan : **{ap['dbscan'] - ap['offset']:+.2f}**  "
                     f"← **DECISION**: what offset-grouping buys = -(this)")
        lines.append("")

    lines.append("## Per-class AP (focus: plug_in / unplug = DBSCAN's merge victims @ oracle 39/38)")
    lines.append("| class | perfect_inst | offset | dbscan | offset−dbscan |")
    lines.append("|---|---|---|---|---|")
    for cid in range(1, 10):
        name = CLASS_NAMES[cid]
        pv = {m: parsed.get(m, {}).get(name, (None,))[0] for m in ALL_MODES}
        delta = (pv["offset"] - pv["dbscan"]) if (pv["offset"] is not None and pv["dbscan"] is not None) else None
        d = f"{delta:+.3f}" if delta is not None else "  -  "
        lines.append(f"| {name} | {fmt(pv['perfect_inst'])} | {fmt(pv['offset'])} | {fmt(pv['dbscan'])} | {d} |")
    lines.append("")

    # mechanical verdict (heuristic, clearly labelled)
    if ap["offset"] is not None and ap["dbscan"] is not None:
        d3 = ap["offset"] - ap["dbscan"]
        pi = parsed.get("offset", {}).get("plug_in", (None,))[0]
        pid = parsed.get("dbscan", {}).get("plug_in", (None,))[0]
        un = parsed.get("offset", {}).get("unplug", (None,))[0]
        und = parsed.get("dbscan", {}).get("unplug", (None,))[0]
        hint = ("BUILD offset head" if d3 >= 5 else
                "SKIP (DBSCAN fine; instancing not the lever)" if d3 < 2 else "MARGINAL — judge by demo need")
        lines.append("## Verdict (mechanical heuristic — confirm by eye)")
        lines.append(f"- offset−dbscan overall = **{d3:+.2f}**  → **{hint}**")
        if pi is not None and pid is not None:
            lines.append(f"- plug_in: offset {pi:.3f} vs dbscan {pid:.3f} ({pi - pid:+.3f})")
        if un is not None and und is not None:
            lines.append(f"- unplug: offset {un:.3f} vs dbscan {und:.3f} ({un - und:+.3f})")
        lines.append("> heuristic: ≥5 build · <2 skip · else marginal. The real call also weighs "
                     "plug_in/unplug specifically (that's where DBSCAN merges).")
    lines.append("")

    path = os.path.join(OUT_DIR, "OFFSET_ORACLE.md")
    with open(path, "w") as f:
        f.write("\n".join(lines))
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modes", default=",".join(ALL_MODES),
                    help=f"comma-separated subset of {ALL_MODES}")
    ap.add_argument("--eps", type=float, default=0.05, help="DBSCAN eps (m), same as predict.py")
    ap.add_argument("--min_samples", type=int, default=10)
    ap.add_argument("--min_cluster", type=int, default=20)
    args = ap.parse_args()
    modes = [m.strip() for m in args.modes.split(",") if m.strip()]
    assert all(m in ALL_MODES for m in modes), f"unknown mode in {modes}"

    os.makedirs(OUT_DIR, exist_ok=True)
    visits = read_val_visits()
    print(f"[offset_oracle] {len(visits)} val scenes | modes={modes} | "
          f"eps={args.eps} min_samples={args.min_samples} min_cluster={args.min_cluster}", flush=True)

    # build all requested modes' instances in ONE pass over the scenes (load each scene once)
    per_mode: dict[str, dict[str, list]] = {m: {} for m in modes}
    for vi, v in enumerate(visits):
        cls, gid, obs, xyz, n_full = load_oracle_scene(v)
        for m in modes:
            if m == "perfect_inst":
                per_mode[m][v] = inst_perfect(cls, gid, obs, xyz, n_full, args.min_cluster)
            elif m == "offset":
                per_mode[m][v] = inst_offset(cls, gid, obs, xyz, n_full,
                                             args.eps, args.min_samples, args.min_cluster)
            else:
                per_mode[m][v] = inst_dbscan(cls, gid, obs, xyz, n_full,
                                             args.eps, args.min_samples, args.min_cluster)
        counts = " ".join(f"{m}:{len(per_mode[m][v])}" for m in modes)
        print(f"  [{vi + 1}/{len(visits)}] {v}  {counts}", flush=True)

    parsed: dict[str, dict] = {}
    for m in modes:
        sub_dir = write_submission(m, per_mode[m])
        print(f"[eval:{m}] official evaluate ...", flush=True)
        stdout = run_official(sub_dir)
        with open(os.path.join(OUT_DIR, f"eval_{m}.txt"), "w") as f:    # persist raw stdout per mode
            f.write(stdout)
        parsed[m] = parse_official(stdout)
        avg = parsed[m].get("average", (None, None, None))
        print(f"[eval:{m}] AP {fmt(avg[0])} / AP50 {fmt(avg[1])} / AP25 {fmt(avg[2])}", flush=True)

    summary = write_summary(parsed, args, len(visits))
    print(f"[done] summary -> {summary}", flush=True)
    print(f"        raw per-mode logs -> {OUT_DIR}/eval_<mode>.txt", flush=True)


if __name__ == "__main__":
    main()
