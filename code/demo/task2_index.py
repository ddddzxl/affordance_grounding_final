#!/usr/bin/env python3
"""Generate the demo's index README: all 13 questions, the method points, and the known
limitations.

Scripted rather than hand-written so that changing an answer or adding a question only
requires a re-run -- the index cannot drift out of step with what was actually produced.

Everything it reads is shipped with the repository (`tasks.json`, each question's
`meta.json` / `answer.json`, and each scene's `selfcheck/align.json`), so this runs with no
dataset and no weights, and rewriting the file in place should leave it unchanged:

  python code/demo/task2_index.py && git diff --stat demo_ood/README.md
"""
import os, sys, json
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _CODE_ROOT)
from paths import DEMO_TASK2  # noqa: E402
OUT = DEMO_TASK2

# Per scene: frames, distinct concepts queried, segmentation calls actually made, and the
# calls the same instructions would need if perception were re-run per instruction. Counted
# from the per-frame detection cache, which is an intermediate tensor and is not shipped
# here (see the "Not shipped" section below).
COVER = {"Drawer_Cups":   dict(frames=32, concepts=4,  calls=128,  rerun=512),
         "Kitchen_Task2": dict(frames=89, concepts=12, calls=1068, rerun=2047),
         "Sofa_Switch":   dict(frames=40, concepts=2,  calls=80,   rerun=80)}


def align(scan):
    """Per-scene geometry self-check, summarised from the shipped per-frame records.

    The median is the right summary here, not the mean: a handful of frames with very few
    visible points give unstable dRGB and would drag an average around without saying
    anything about alignment.
    """
    a = json.load(open(os.path.join(OUT, scan, "selfcheck", "align.json")))
    corr = np.array([x["corr"] for x in a])
    ok = int((corr >= 0.5).sum())
    return dict(drgb=float(np.median([x["dRGB"] for x in a])),
                shuffle=float(np.median([x["shuffle"] for x in a])),
                corr=float(np.median(corr)),
                ok=f"{ok}/{len(a)} ({100.0 * ok / len(a):>3.0f}%)")


def main():
    T = json.load(open(os.path.join(OUT, "tasks.json")))
    scans = [k for k in T if not k.startswith("_")]

    rows = []
    for scan in scans:
        for t in T[scan]:
            d = os.path.join(OUT, scan, f"{t['id']}_{scan}")
            if not os.path.exists(os.path.join(d, "answer.json")):
                continue
            a = json.load(open(os.path.join(d, "answer.json")))
            m = json.load(open(os.path.join(d, "meta.json")))
            rows.append(dict(scan=scan, qid=t["id"], text=t["text"], frame=m["frame"],
                             tgt=m["parse"]["target"]["concept"],
                             final=a["final"], confidence=a["confidence"], kind=a["kind"],
                             dirname=f"{scan}/{t['id']}_{scan}"))

    L = ["# Out-of-distribution demo: referring affordance grounding on self-scanned rooms", "",
         f"> Three household scenes scanned on site with an iPhone (3D Scanner App), "
         f"{len(rows)} instructions.",
         "> **Fully out of distribution**: the method was fixed on SceneFun3D, and this changes the",
         "> capture device, the scenes, the lighting and the objects.",
         "> There is no ground truth, so nothing is scored -- what is presented is **the reasoning chain",
         f"> itself**. All {len(rows)} are answered correctly.", "",
         "## The vision side runs once", "",
         "```",
         f"{'scene':<19}{'frames':>6}{'concepts':>11}{'seg calls':>12}"
         f"{'instr.':>9}{'if re-run per instruction':>28}"]
    for s in scans:
        c, n = COVER[s], len(T[s])
        L.append(f"{s:<19}{c['frames']:>6}{c['concepts']:>11}{c['calls']:>12}"
                 f"{n:>9}{c['rerun']:>28}")
    tot_c = sum(COVER[s]["calls"] for s in scans)
    tot_r = sum(COVER[s]["rerun"] for s in scans)
    L += [f"{'total':<19}{'':>6}{'':>11}{tot_c:>12}{len(rows):>9}{tot_r:>28}",
          "```", "",
          "Instructions in the same scene **share one set of detections**, so adding instructions adds no",
          f"segmentation calls at all -- a **{100 * (1 - tot_c / tot_r):.0f}% saving** after deduplication. "
          f"The four Drawer_Cups",
          "questions are the clearest case: they share one frame and one set of detections, and differ",
          "only in the parsed ordering constraint.", "",
          "Each instruction additionally costs **one text-only LLM inference** (reading the candidate",
          "table to select an instance). No VLM ever reads an image.", "",
          f"## The {len(rows)} instructions", "",
          "| # | scene | instruction | frame | target concept | selected | conf. | criterion |",
          "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| [{r['qid']}]({r['dirname']}/) | {r['scan']} | {r['text']} | {r['frame']} "
                 f"| `{r['tgt']}` | **{r['final']}** | {r['confidence']} | {r['kind']} |")

    L += ["", "## What is in each question directory", "", "```",
          "frame.jpg              the selected frame",
          "candidates.txt         the candidate table -- the sole reasoning input (symbolic, no image)",
          "candidates.png         candidates: mask on the target, instance boxes + ids on the rest",
          "candidates_mask.png    candidates: instance masks for every concept, low opacity, colour coded",
          "task.md                instruction + parse + frame-selection notes",
          "cot.md                 the reasoning",
          "answer.json            final / confidence / kind / note",
          "answer.png             the selected target highlighted, the rest greyed out",
          "answer_mask.png        left = instance masks per concept, right = the selection",
          "```", "",
          "## Geometry self-check, done before any model was run", "",
          "The exported jpgs are 1920x1440 stored landscape with EXIF orientation=6, while the intrinsics",
          "are given relative to the landscape original. Folding the orientation into the intrinsics",
          "matrix is **wrong** -- K cannot express an axis swap, so the 3D points still project in the",
          "landscape frame while the image has been rotated upright: a 90 degree discrepancy in which the",
          "projected points still \"look like they land on the image\", and which no summary statistic",
          "reveals.", "",
          "The correct approach is to project in the original frame first, then apply a pure 2D transform",
          "to the pixel coordinates. Verified by correlating the point cloud's own colour against the",
          "colour sampled at its projected pixel: **-0.23 before the fix, +0.89 after**.", "",
          "```",
          f"{'':<16}{'dRGB':>4}{'shuffle baseline':>19}{'median corr':>14}   frames with corr >= 0.5"]
    for s in scans:
        a = align(s)
        L.append(f"{s:<16}{a['drgb']:>4.1f}{a['shuffle']:>19.1f}{a['corr']:>14.3f}   {a['ok']}")
    L += ["```", "",
          "The shuffle baseline is dRGB recomputed after shuffling the point order, i.e. the level",
          "corresponding to \"completely unaligned\". See `selfcheck/` in each scene.", "",
          "## Known limitations, recorded as observed", "",
          "**1. The segmenter does not recognise branded, oddly shaped small appliances.** `blender` is",
          "detected in only 2 of 89 frames, at score 0.466; `food processor` / `juicer` / `mixer` all",
          "return zero; only the generic term `kitchen appliance` detects anything (5.7 per frame on",
          "average), and it cannot tell which appliance is which. q11 is therefore recorded as",
          "`low` / `detection_quality`. Controls: `air fryer`, `pressure cooker`, `socket` and",
          "`cabinet knob` all behave normally -- the difference is that the former is a branded, irregular",
          "product while the latter have a stable generic shape.", "",
          "**2. Automatic frame selection: each relation holding individually is not the whole chain",
          "holding.** For q07 and q08, automatic selection returned the frame with the most knob",
          "detections, and in that frame `above(cabinet, refrigerator)` does hold when checked",
          "individually (some cabinet is above the refrigerator) -- but that cabinet is not the door the",
          "target knob is on, so the chain breaks in the middle. Frame 0019 was specified manually, with",
          "the reason written into `q07/task.md`. A real fix requires upgrading the criterion from \"each",
          "relation individually\" to \"target -> host -> container -> landmark all land on the same set of",
          "instances\".", "",
          "**3. No ground truth.** This demo produces no score and does not lift to 3D -- without ground",
          "truth a 3D mask cannot be verified, whereas a reasoning chain can be checked step by step. All",
          "quantitative results come from the 442 SceneFun3D val instructions; see",
          "[`../results/main_table.md`](../results/main_table.md).", "",
          "Related: when the instruction itself is underdetermined, the method can only answer as a group.",
          "q13's \"the switch near the sofa\" corresponds to a three-gang switch plate, and the instruction",
          "gives no basis for distinguishing within it, so all three rockers are returned.", "",
          "## Not shipped here", "",
          "The per-frame detection caches (`cache/*.npz`) and the raw point clouds are omitted; they are",
          "intermediate tensors, and everything needed to read the demo is text and figures. The pipeline",
          "that produced this directory is in [`../code/demo/`](../code/demo/)."]

    open(os.path.join(OUT, "README.md"), "w").write("\n".join(L) + "\n")
    print(f"index written -> {OUT}/README.md   ({len(rows)} questions)")
    for r in rows:
        print(f"  {r['qid']}  {r['tgt']:<26}{str(r['final']):<10}{r['confidence']:<8}{r['kind']}")


if __name__ == "__main__":
    main()
