#!/usr/bin/env python3
"""Generate the demo's index README: all 13 questions, the method points, and the known
limitations.

Scripted rather than hand-written so that changing an answer or adding a question only
requires a re-run -- the index cannot drift out of step with what was actually produced.

  python src/demo/task2_index.py
"""
import os, sys, json, glob
import numpy as np

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _CODE_ROOT)
from paths import DEMO_TASK2  # noqa: E402
OUT = DEMO_TASK2
NFRAME = {"Drawer_Cups": 32, "Kitchen_Task2": 89, "Sofa_Switch": 40}


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
                             tgt=m["parse"]["target"]["concept"], **a,
                             rel=f"{m.get('n_rel_sat')}/{m.get('n_rel')}",
                             dirname=f"{scan}/{t['id']}_{scan}"))

    L = ["# Out-of-distribution demo: referring affordance grounding on self-scanned rooms", "",
         "> Three household scenes scanned on site with an iPhone (3D Scanner App), "
         "13 instructions.",
         "> **Fully out of distribution**: the method was fixed on SceneFun3D, and this "
         "changes the capture device, the scenes, the lighting and the objects.",
         "> There is no ground truth, so nothing is scored -- what is presented is "
         "**the reasoning chain itself**.", "",
         "## The vision side runs once", "",
         "```",
         f"{'scene':<16}{'frames':>7}{'concepts':>10}{'seg calls':>11}"
         f"{'instr.':>8}{'if re-run per instr.':>22}"]
    for s in scans:
        n_f, n_c, n_call = cover[s]
        L.append(f"{s:<16}{n_f:>7}{n_c:>10}{n_call:>11}{len(T[s]):>8}"
                 f"{n_call * len(T[s]) // max(n_c, 1):>22}")
    tot_c = sum(cover[s][2] for s in scans)
    tot_n = sum(cover[s][2] * len(T[s]) // max(cover[s][1], 1) for s in scans)
    L += [f"{'total':<16}{'':>7}{'':>10}{tot_c:>11}"
          f"{sum(len(T[s]) for s in scans):>8}{tot_n:>22}",
          "```", "",
          f"Instructions in the same scene **share one set of detections**, so adding "
          f"instructions adds no segmentation calls at all -- a {100*(1-tot_c/tot_n):.0f}% "
          f"saving after deduplication.",
          "Each instruction additionally costs **one text-only LLM inference** (reading the "
          "candidate table to select an instance). No VLM ever reads an image.", "",
          "## The 13 instructions", "",
          "| # | scene | instruction | frame | target concept | selected | conf. | criterion |",
          "|---|---|---|---|---|---|---|---|"]
    L += rows
    if fixed:
        L += ["", "### Corrections", ""]
        L += fixed
    L += ["", "Each question directory holds:", "", "```",
          "frame.jpg              the selected frame",
          "candidates.txt         the candidate table -- the sole reasoning input "
          "(symbolic, no image)",
          "candidates.png         candidates: mask on the target, instance boxes + ids "
          "on the rest",
          "candidates_mask.png    candidates: instance masks for **every** concept, low "
          "opacity, colour coded",
          "task.md                instruction + parse + frame-selection notes",
          "cot.md                 the reasoning",
          "answer.json            final / confidence / kind / note",
          "answer.png             the selected target highlighted, the rest greyed out",
          "answer_mask.png        left = instance masks per concept, right = the selection",
          "```", "",
          "## Geometry self-check, done before any model was run", "",
          "The exported jpgs are 1920x1440 stored landscape with EXIF orientation=6, while "
          "the intrinsics are given relative to the landscape original.",
          "Folding the orientation into the intrinsics matrix is **wrong** -- K cannot "
          "express an axis swap, so the 3D points still project in the landscape frame while "
          "the image has been rotated upright,",
          "a 90 degree discrepancy in which the projected points still \"look like they land "
          "on the image\" and no summary statistic reveals it.",
          "The correct approach is to project in the original frame first, then apply a pure "
          "2D transform to the pixel coordinates.",
          "Verified by correlating the point cloud\'s own colour against the colour sampled "
          "at its projected pixel: **-0.23 before the fix, +0.89 after**.", "",
          "```",
          "                dRGB   shuffle baseline   median corr   frames with corr>=0.5"]
    for s in scans:
        a = ALIGN.get(s)
        if a:
            L.append(f"{s:<16}{a['drgb']:>6.1f}{a['shuffle']:>19.1f}"
                     f"{a['corr']:>14.3f}   {a['ok']}")
    L += ["```", "", "See `selfcheck/` in each scene.", "",
          "## Known limitations, recorded as observed", "",
          "**1. The segmenter does not recognise branded, oddly shaped small appliances.** "
          "The blender is detected in only 2 of 89 frames (score 0.466);",
          "`food processor` / `juicer` / `mixer` all return zero; only the generic term "
          "`kitchen appliance` detects anything",
          "(5.7 per frame on average), and it cannot tell which appliance is which. q11 is "
          "therefore recorded as `low` / `detection_quality`.",
          "Controls: `air fryer`, `pressure cooker`, `socket` and `cabinet knob` all behave "
          "normally -- the difference is that the former is a branded, irregular product "
          "while the latter have a stable generic shape.", "",
          "**2. Automatic frame selection: each relation holding individually is not the "
          "whole chain holding.** For q07 and q08 automatic selection returned the frame with "
          "the most knob detections,",
          "and in that frame `above(cabinet, refrigerator)` does hold when checked "
          "individually (some cabinet is above the refrigerator),",
          "but that cabinet is not the door the target knob is on -- the chain breaks in the "
          "middle. Frame 0019 was specified manually,",
          "with the reason written into `q07/task.md`. A real fix requires upgrading the "
          "criterion from \"each relation individually\" to",
          "\"target -> host -> container -> landmark all land on the same set of "
          "instances\".", "",
          "**3. No ground truth.** This demo produces no score and does not lift to 3D -- "
          "without ground truth a 3D mask cannot be verified,",
          "whereas a reasoning chain can be checked step by step. All quantitative results "
          "come from the 442 SceneFun3D val instructions.", ""]
    open(os.path.join(OUT, "README.md"), "w").write("\n".join(L) + "\n")
    print(f"index written -> {OUT}/README.md   ({len(rows)} questions, {len(fixed)} corrections)")
    for r in rows:
        print(f"  {r['qid']}  {r['tgt']:<26}{str(r['final']):<10}{r['confidence']:<8}{r['kind']}")


if __name__ == "__main__":
    main()
