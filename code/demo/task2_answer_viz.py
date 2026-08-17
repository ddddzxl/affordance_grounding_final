#!/usr/bin/env python3
"""Render each question's answer.png: highlight the selected target on the chosen frame.

The demo has no ground truth, so this figure scores nothing; it presents **what the method
produced**:
  left  = the original frame
  right = every candidate of the target concept, the selection filled and outlined in white,
          the rest desaturated to grey.
The title carries final / confidence / kind and the note goes underneath -- one figure is the
whole conclusion for that question.

  python src/demo/task2_answer_viz.py
"""
import os, sys, json, glob, argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _CODE_ROOT)
from paths import PROJECT_ROOT  # noqa: E402
ROOT = PROJECT_ROOT
sys.path.insert(0, os.path.join(ROOT, "src/demo"))
from iphone_io import read_frames, read_rgb                        # noqa: E402

DATA = os.path.join(ROOT, "data/iphone_3dscanner")
OUT = os.path.join(ROOT, "viz/func_seg/demo_task2")
PICK = np.array([1.0, 0.23, 0.19])          # selected: vermilion
GREY = np.array([0.55, 0.57, 0.60])         # not selected: grey


def outline(mask):
    """4-neighbour boundary: shift one cell each way; a pixel with any neighbour outside the
    mask is a boundary pixel."""
    e = np.zeros_like(mask)
    e[1:, :] |= mask[1:, :] & ~mask[:-1, :]
    e[:-1, :] |= mask[:-1, :] & ~mask[1:, :]
    e[:, 1:] |= mask[:, 1:] & ~mask[:, :-1]
    e[:, :-1] |= mask[:, :-1] & ~mask[:, 1:]
    return e


def ctx_overlay(m, store, names, H, W, alpha=0.38):
    """Draw the non-target concepts as instance masks -- one figure showing the segmentation
    quality of the evidence the localisation rests on."""
    ov = np.zeros((H, W, 4), float)
    cm = plt.cm.tab20(np.linspace(0, 1, 20))[:, :3]
    k = 0
    for c in names:
        for d in m["det"].get(c, []):
            flat = store[f"{c}|{d['i']}"].astype(np.int64)
            yy, xx = np.divmod(flat, W)
            ov[yy, xx, :3] = cm[k % 20]; ov[yy, xx, 3] = alpha
            k += 1
    return ov


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", default="all")
    args = ap.parse_args()
    T = json.load(open(os.path.join(OUT, "tasks.json")))
    scans = [s for s in T if not s.startswith("_")] if args.scan == "all" else [args.scan]

    for scan in scans:
        frames = read_frames(os.path.join(DATA, scan), upright=True)
        cd = os.path.join(OUT, scan, "cache")
        for qd in sorted(glob.glob(os.path.join(OUT, scan, "q*_*"))):
            af = os.path.join(qd, "answer.json")
            if not os.path.exists(af):
                print(f"  {os.path.basename(qd)}: no answer.json yet, skipping"); continue
            a = json.load(open(af))
            m = json.load(open(os.path.join(qd, "meta.json")))
            # ⚠️ Changing the frame-selection strategy changes a question's frame and
            #    reorders its instance ids, while answer.json was written against **one
            #    particular frame's candidate table**. Two questions were answered wrongly
            #    exactly this way: the frame moved from 0023 to 0008, the table was not
            #    re-read, and left and right came out swapped. This is a hard check --
            #    on a mismatch it refuses to render.
            if a.get("based_on_frame") not in (None, m["frame"]):
                print(f"  FAIL {m['id']}: answer.json was written against frame "
                      f"{a['based_on_frame']}, but the current selection is {m['frame']} "
                      f"-- candidate ids have been reordered, so this question's reasoning "
                      f"**must be redone**")
                continue
            tgt = m["parse"]["target"]["concept"]
            W, H = m["W"], m["H"]
            store = np.load(os.path.join(cd, f"det_f{m['frame']}.npz"))
            rgb = read_rgb(frames[int(m["frame"])]["rgb"], upright=True)

            ov = np.zeros((H, W, 4), float)
            for d in m["det"].get(tgt, []):
                flat = store[f"{tgt}|{d['i']}"].astype(np.int64)
                mk = np.zeros(H * W, bool); mk[flat] = True; mk = mk.reshape(H, W)
                sel = d["i"] in a["final"]
                col, al = (PICK, 0.70) if sel else (GREY, 0.38)
                ov[mk, :3] = col; ov[mk, 3] = al
                if sel:
                    ed = outline(mk)
                    ov[ed, :3] = 1.0; ov[ed, 3] = 1.0

            fig, axs = plt.subplots(1, 2, figsize=(13.4, 9.4))
            axs[0].imshow(rgb); axs[0].set_title("selected frame", fontsize=11)
            axs[1].imshow(rgb); axs[1].imshow(ov)
            for d in m["det"].get(tgt, []):
                sel = d["i"] in a["final"]
                axs[1].text(d["cx"], d["cy"], str(d["i"]), fontsize=13 if sel else 10,
                            color="white", ha="center", va="center", weight="bold",
                            bbox=dict(fc=tuple(PICK) if sel else tuple(GREY),
                                      ec="white" if sel else "none", lw=1.2, pad=1.6, alpha=.95))
            axs[1].set_title(f"answer: {tgt} {a['final']}   "
                             f"[{a['confidence']} · {a['kind']}]", fontsize=11, color="darkred")
            for ax in axs:
                ax.axis("off")
            fig.suptitle(f"{m['id']} · {scan} · frame {m['frame']} — {m['text']}", fontsize=12)
            # ⚠️ The default matplotlib font has no CJK glyphs and would render them as
            #    boxes, so **all on-figure text is English**; any longer commentary lives in
            #    answer.json / cot.md instead.
            fig.text(0.5, 0.055, a.get("note_en", ""), ha="center", fontsize=9.5,
                     wrap=True, color="#333")
            fig.savefig(os.path.join(qd, "answer.png"), dpi=100, bbox_inches="tight")
            plt.close(fig)

            # ---- all-mask variant: every concept drawn as a mask, low opacity, no ids ----
            cons = [tgt] + [c for c in m["parse"]["entities"]
                            if c.get("instanceable", True) and c["name"] != tgt]
            names = [tgt] + [c["name"] for c in m["parse"]["entities"]
                             if c.get("instanceable", True) and c["name"] != tgt]
            fig, axs = plt.subplots(1, 2, figsize=(13.4, 9.4))
            axs[0].imshow(rgb); axs[0].imshow(ctx_overlay(m, store, names[1:], H, W))
            axs[0].set_title("context concepts (instance masks)", fontsize=11)
            axs[1].imshow(rgb); axs[1].imshow(ov)
            axs[1].set_title(f"answer: {tgt} {a['final']}   "
                             f"[{a['confidence']} · {a['kind']}]", fontsize=11, color="darkred")
            for ax in axs:
                ax.axis("off")
            fig.suptitle(f"{m['id']} · {scan} · frame {m['frame']} — {m['text']}", fontsize=12)
            fig.text(0.5, 0.055, a.get("note_en", ""), ha="center", fontsize=9.5,
                     wrap=True, color="#333")
            fig.savefig(os.path.join(qd, "answer_mask.png"), dpi=100, bbox_inches="tight")
            plt.close(fig)
            print(f"  {m['id']}  final={a['final']}  [{a['confidence']}/{a['kind']}]  -> answer.png")


if __name__ == "__main__":
    main()
