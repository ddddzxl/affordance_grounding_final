#!/usr/bin/env python3
"""Build the question material from the detection cache: frame selection, candidate table,
and visualisations, in the same per-question format the val pipeline uses.

## Differences from the val version, and why

- **Frame selection**: the val pipeline scores frames by a polar KL divergence on the
  container, because it has to choose among 203 frames. Each demo scene has only 32-89
  frames, so "target detection count + concept completeness + confidence" is enough and that
  machinery is unnecessary. **Instructions in one scene each select their own frame** but
  share one detection cache.
- **No lifting**: the demo has no ground truth, so a 3D mask cannot be verified either way.
  What is on show is the reasoning chain.
- The target concept is drawn as a **mask** and the other concepts as **instance boxes** --
  the former is what gets output, the latter is only the evidence used to locate it.

## Per-question output (matching the val format)

  frame.jpg        the selected frame
  candidates.txt   the candidate table = the **sole input** to the reasoning (symbolic, no image)
  candidates.png   the candidates visualised on that frame
  task.md          instruction + parse
  meta.json        frame selection result + candidate geometry, reused by scoring and viz

  python src/demo/task2_pack.py --scan all
"""
import os, sys, json, glob, shutil, argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _CODE_ROOT)
from paths import PROJECT_ROOT  # noqa: E402
ROOT = PROJECT_ROOT
sys.path.insert(0, os.path.join(ROOT, "src/demo"))
from iphone_io import read_frames, read_rgb                       # noqa: E402

DATA = os.path.join(ROOT, "data/iphone_3dscanner")
OUT = os.path.join(ROOT, "viz/func_seg/demo_task2")
COLORS = (plt.cm.tab20(np.linspace(0, 1, 20))[:, :3] * 255).astype(np.uint8)


def instanceable(parse):
    return [e["name"] for e in parse["entities"] if e.get("instanceable", True)]


def rel_ok(d, r, W, H):
    """Whether this relation is **actually satisfied** by some pair of instances in this
    frame, judged on bboxes.

    Checking that "a and b were both detected" is not enough: in one frame the refrigerator
    showed only a strip at the far left (x 0-184) while every knob had cx > 500 -- both
    entities present, the relation false. Folding this into frame selection is what makes it
    choose a frame with the refrigerator front and the two cabinet doors above it, which is a
    frame the chain can actually be reasoned on.
    """
    A, B = d.get(r["a"], []), d.get(r["b"], [])
    if not A or not B:
        return False
    rel = r["rel"]
    xov = lambda a, b: a["x1"] >= b["x0"] and a["x0"] <= b["x1"]
    yov = lambda a, b: a["y1"] >= b["y0"] and a["y0"] <= b["y1"]
    inside = lambda o, c: (o["x0"] >= c["x0"] - 5 and o["x1"] <= c["x1"] + 5
                           and o["y0"] >= c["y0"] - 5 and o["y1"] <= c["y1"] + 5)
    diag = (W ** 2 + H ** 2) ** .5
    for a in A:
        for b in B:
            if rel == "contains" and inside(b, a): return True
            if rel in ("above",) and a["cy"] < b["cy"] and xov(a, b): return True
            if rel in ("below", "under") and a["cy"] > b["cy"] and xov(a, b): return True
            if rel == "left_of" and a["cx"] < b["cx"] and yov(a, b): return True
            if rel == "right_of" and a["cx"] > b["cx"] and yov(a, b): return True
            if rel == "has_on_top" and b["y1"] <= a["y0"] + 40 and xov(a, b): return True
            if rel == "on_top" and a["y1"] <= b["y0"] + 40 and xov(a, b): return True
            if rel in ("near", "next_to") and \
               ((a["cx"] - b["cx"]) ** 2 + (a["cy"] - b["cy"]) ** 2) ** .5 < .35 * diag:
                return True
            if rel in ("behind", "in_front_of", "between"):
                return True                       # undecidable in 2D; not used for selection
    return False


def pick_frame(meta, parse):
    """Score and select a frame. Hard condition: the target has at least one detection.
    Concept completeness and confidence enter the soft score.

    Prefers frames with **more** target detections -- a disambiguation question
    (top/2nd/3rd/bottom) can only be ordered if a whole group of same-class targets is
    visible in one frame.
    """
    tgt = parse["target"]["concept"]
    others = [c for c in instanceable(parse) if c != tgt]
    best = None
    for fi, v in sorted(meta.items()):
        d = v["det"]
        td = d.get(tgt, [])
        if not td:
            continue
        miss = [c for c in others if not d.get(c)]
        # ⚠️ Scoring on detection count alone selects the wrong frame: in the frame with the
        #    most knob detections, the refrigerator may show only a sliver at the image edge
        #    (score 0.5), while a relation like `above(cabinet, refrigerator)` requires the
        #    reference object itself to be **clearly seen**. So the **highest confidence**
        #    among the entities a relation involves is folded into the score too.
        rel_ent = {r["a"] for r in parse["relations"]} | {r["b"] for r in parse["relations"]}
        conf = sum(max((x["score"] for x in d.get(c, [])), default=0.0)
                   for c in others if c in rel_ent)
        nrel = len(parse["relations"])
        nsat = sum(rel_ok(d, r, v["W"], v["H"]) for r in parse["relations"])
        sc = (len(td)
              + 0.5 * sum(min(len(d.get(c, [])), 3) for c in others)
              + float(np.mean([x["score"] for x in td]))
              + 1.5 * conf                        # the clearer the reference object, the better
              + 6.0 * nsat                        # relations genuinely holding: highest weight
              - 3.0 * len(miss))                  # missing concepts penalised hard, but not
                                                  # excluded outright
        if best is None or sc > best[1]:
            best = (fi, sc, len(miss), nsat, nrel)
    return best


def containment(store, meta_f, tgt, host, W, H):
    """host instance -> the target ids inside it. Falls back to bbox when the mask test finds
    nothing, and flags that it did so."""
    rows = []
    hd = meta_f["det"].get(host, [])
    td = meta_f["det"].get(tgt, [])
    if not hd or not td:
        return rows
    for h in hd:
        hm = set(store[f"{host}|{h['i']}"].tolist())
        inside, via = [], ""
        for t in td:
            tm = store[f"{tgt}|{t['i']}"]
            if len(hm & set(tm.tolist())) / max(len(tm), 1) >= 0.5:
                inside.append(t["i"])
        if not inside:                            # mask test found nothing -> bbox fallback
            for t in td:
                if (t["x0"] >= h["x0"] - 5 and t["x1"] <= h["x1"] + 5
                        and t["y0"] >= h["y0"] - 5 and t["y1"] <= h["y1"] + 5):
                    inside.append(t["i"])
            via = "  [via bbox]"
        rows.append((h["i"], inside, via))
    return rows


def write_txt(path, task, parse, meta_f, store, W, H):
    tgt = parse["target"]["concept"]
    L = [f'TASK: "{task["text"]}"', "", "PARSE:",
         f'  target concept = "{tgt}"   <- the thing that must be output',
         f'  host           = {parse["target"]["host"]!r}   <- countable object the target sits on']
    for e in parse["entities"]:
        mark = "" if e.get("instanceable", True) else "   (not instanceable: not a countable object in the image)"
        L.append(f"  entity  : {e['name']!r}  role={e['role']}{mark}")
    for r in parse["relations"]:
        L.append(f"  relation: {r['rel']}(a={r['a']!r}, b={r['b']!r})")
    for s in parse["select"]:
        L.append(f"  select  : on={s['on']!r} axis={s['axis']} value={s.get('value')!r} "
                 f"index={s.get('index')} from={s.get('from')!r}")
    if parse.get("residual"):
        L.append(f"  residual: {parse['residual']}")
    L += ["", "IMAGE COORDINATE SYSTEM (read carefully):",
          f"  image is {W} wide (x) by {H} tall (y).  (PORTRAIT)",
          "  x increases to the RIGHT.  y increases DOWNWARD.",
          '  => "top" = SMALL y,  "bottom" = LARGE y,  "left" = SMALL x,  "right" = LARGE x',
          '  => "A above B" means A.cy < B.cy.',
          "  area% = mask pixels as % of the whole image.  score = SAM3 confidence.",
          "  NOTE: detections are imperfect. A box covering a large fraction of the image",
          "        is usually several objects merged, not one piece of furniture.",
          "", "INSTANCES (after score-ranked NMS, sorted by score):",
          f"  {'class':<26}{'id':>3}{'xmin':>6}{'xmax':>6}{'ymin':>6}{'ymax':>6}"
          f"{'cx':>8}{'cy':>8}{'area%':>8}{'score':>7}"]
    for c in instanceable(parse):
        for d in meta_f["det"].get(c, []):
            L.append(f"  {c:<26}{d['i']:>3}{d['x0']:>6}{d['x1']:>6}{d['y0']:>6}{d['y1']:>6}"
                     f"{d['cx']:>8.1f}{d['cy']:>8.1f}{100*d['n']/(W*H):>8.3f}{d['score']:>7.3f}")
    host = parse["target"]["host"]
    if host:
        rows = containment(store, meta_f, tgt, host, W, H)
        L += ["", f"CONTAINMENT ({tgt} ids inside each {host}):"]
        if rows:
            for hi, ins, via in rows:
                L.append(f"  {host} #{hi}  contains {tgt} {ins}{via}")
        else:
            L.append(f"  (none — no {host} detected, or no overlap)")
    L += ["", f'QUESTION: which "{tgt}" id(s) does the instruction refer to?']
    open(path, "w").write("\n".join(L) + "\n")


def draw_mask(path, rgb, meta_f, store, parse, title, alpha=0.42):
    """All-mask variant: every concept as an instance mask, no boxes and no ids, with colour
    distinguishing instances.

    A box can only give the axis-aligned bounding rectangle, which distorts badly for thin or
    surface-hugging targets like handles and switches; the mask is what the segmenter actually
    produced, so the shape is more informative than the box. Opacity is kept at 0.42 so the
    object underneath stays visible -- this figure is for a human checking how well the
    segmentation fits, not for reading ids off.
    """
    tgt = parse["target"]["concept"]
    cons = [tgt] + [c for c in instanceable(parse) if c != tgt]
    H, W = rgb.shape[:2]
    n = len(cons) + 1
    fig, axs = plt.subplots(1, n, figsize=(5.4 * n, 8.6))
    axs = np.atleast_1d(axs)
    axs[0].imshow(rgb); axs[0].set_title("selected frame", fontsize=11); axs[0].axis("off")
    for ci, c in enumerate(cons):
        ax = axs[ci + 1]; ax.imshow(rgb)
        dets = meta_f["det"].get(c, [])
        ov = np.zeros((H, W, 4), float)
        for d in dets:
            col = COLORS[d["i"] % 20] / 255.0
            flat = store[f"{c}|{d['i']}"].astype(np.int64)
            yy, xx = np.divmod(flat, W)
            ov[yy, xx, :3] = col; ov[yy, xx, 3] = alpha
        ax.imshow(ov)
        tag = "  (TARGET)" if ci == 0 else ""
        ax.set_title(f"{c}{tag}  n={len(dets)}", fontsize=11,
                     color="darkred" if ci == 0 else "black")
        ax.axis("off")
    fig.suptitle(title, fontsize=12)
    fig.savefig(path, dpi=95, bbox_inches="tight"); plt.close(fig)


def draw(path, rgb, meta_f, store, parse, title):
    """Draw the target concept as a mask and the others as instance boxes: the former is what
    gets output, the latter is only the evidence used to locate it."""
    tgt = parse["target"]["concept"]
    cons = [tgt] + [c for c in instanceable(parse) if c != tgt]
    H, W = rgb.shape[:2]
    n = len(cons) + 1
    fig, axs = plt.subplots(1, n, figsize=(5.4 * n, 8.6))
    axs = np.atleast_1d(axs)
    axs[0].imshow(rgb); axs[0].set_title("selected frame", fontsize=11); axs[0].axis("off")
    for ci, c in enumerate(cons):
        ax = axs[ci + 1]; ax.imshow(rgb)
        dets = meta_f["det"].get(c, [])
        if ci == 0:                                        # target -> mask
            ov = np.zeros((H, W, 4), float)
            for d in dets:
                col = COLORS[d["i"] % 20] / 255.0
                flat = store[f"{c}|{d['i']}"]
                yy, xx = np.divmod(flat.astype(np.int64), W)
                ov[yy, xx, :3] = col; ov[yy, xx, 3] = 0.62
                ax.text(d["cx"], d["cy"], str(d["i"]), color="white", fontsize=13,
                        ha="center", va="center", weight="bold",
                        bbox=dict(fc=col, ec="none", alpha=.85, pad=1.4))
            ax.imshow(ov)
            ax.set_title(f"{c}  (TARGET — mask, n={len(dets)})", fontsize=11, color="darkred")
        else:                                              # everything else -> instance boxes
            for d in dets:
                col = COLORS[d["i"] % 20] / 255.0
                ax.add_patch(mp.Rectangle((d["x0"], d["y0"]), d["x1"] - d["x0"],
                                          d["y1"] - d["y0"], fill=False, ec=col, lw=2.0))
                ax.text(d["x0"] + 4, d["y0"] + 26, str(d["i"]), color="white", fontsize=11,
                        bbox=dict(fc=col, ec="none", alpha=.85, pad=1.2))
            ax.set_title(f"{c}  (box, n={len(dets)})", fontsize=11)
        ax.axis("off")
    fig.suptitle(title, fontsize=12)
    fig.savefig(path, dpi=95, bbox_inches="tight"); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", default="all")
    ap.add_argument("--only", default="", help="only these question ids, comma separated")
    args = ap.parse_args()
    T = json.load(open(os.path.join(OUT, "tasks.json")))
    only = {x.strip() for x in args.only.split(",") if x.strip()}
    scans = [s for s in T if not s.startswith("_")] if args.scan == "all" else [args.scan]

    for scan in scans:
        cd = os.path.join(OUT, scan, "cache")
        meta = json.load(open(os.path.join(cd, "det.json")))
        frames = read_frames(os.path.join(DATA, scan), upright=True)
        for task in T[scan]:
            if only and task["id"] not in only:
                continue
            parse = task["parse"]
            if task.get("frame"):               # manually specified in tasks.json
                                                # (the reason is recorded in frame_why)
                fi0 = task["frame"]
                d0 = meta[fi0]["det"]
                others0 = [c for c in instanceable(parse) if c != parse["target"]["concept"]]
                got = (fi0, 0.0, len([c for c in others0 if not d0.get(c)]),
                       sum(rel_ok(d0, r, meta[fi0]["W"], meta[fi0]["H"])
                           for r in parse["relations"]), len(parse["relations"]))
            else:
                got = pick_frame(meta, parse)
            if got is None:
                print(f"  {task['id']}  FAIL: no frame detects the target "
                      f"{parse['target']['concept']!r} -- skipping"); continue
            fi, sc, miss, nsat, nrel = got
            mf = meta[fi]
            W, H = mf["W"], mf["H"]
            store = np.load(os.path.join(cd, f"det_f{fi}.npz"))
            qd = os.path.join(OUT, scan, f"{task['id']}_{scan}")
            os.makedirs(qd, exist_ok=True)
            fr = frames[int(fi)]
            rgb = read_rgb(fr["rgb"], upright=True)
            plt.imsave(os.path.join(qd, "frame.jpg"), rgb)
            write_txt(os.path.join(qd, "candidates.txt"), task, parse, mf, store, W, H)
            ttl = f"{task['id']} · {scan} · frame {fi} — {task['text']}"
            draw(os.path.join(qd, "candidates.png"), rgb, mf, store, parse, ttl)
            draw_mask(os.path.join(qd, "candidates_mask.png"), rgb, mf, store, parse,
                      ttl + "   [all concepts as instance masks]")
            open(os.path.join(qd, "task.md"), "w").write(
                f"# {task['id']} - {scan} / frame {fi}\n\n## Instruction\n\n> {task['text']}\n\n"
                f"## Stage 0 parse\n\n```json\n{json.dumps(parse, indent=1)}\n```\n\n"
                f"## Frame selection\n\nChosen from {len(meta)} frames by "
                f"\"target detection count + concept completeness + confidence\": "
                f"frame {fi}; {miss} concepts missing, and {nsat} of the {nrel} spatial "
                f"relations in the parse genuinely hold in this frame.\n"
                + (f"\n> ⚠️ The frame for this question was **specified manually**. "
                   f"{task['frame_why']}\n"
                   if task.get("frame") else ""))
            json.dump(dict(scan=scan, id=task["id"], frame=fi, rgb=mf["rgb"], W=W, H=H,
                           text=task["text"], parse=parse, det=mf["det"], n_miss=miss,
                           n_rel_sat=nsat, n_rel=nrel),
                      open(os.path.join(qd, "meta.json"), "w"), ensure_ascii=False, indent=1)
            nt = len(mf["det"].get(parse["target"]["concept"], []))
            print(f"  {task['id']}  frame {fi}  target x{nt}  missing concepts {miss}  "
                  f"relations satisfied {nsat}/{nrel}  -> {os.path.basename(qd)}")


if __name__ == "__main__":
    main()
