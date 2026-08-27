#!/usr/bin/env python3
"""Compose the demo banner: one scene, one frame, one set of detections, four instructions.

The four Drawer_Cups questions differ only in the parsed ordering constraint, so laying their
answers side by side is the most direct picture of both halves of the claim -- that the hard
part is choosing among identical parts, and that asking the same room another question costs
no additional perception.

Reads only the per-question `answer.png` and `answer.json` already in `demo_ood/`, so it runs
with no dataset and no weights:

  python code/demo/task2_banner.py
"""
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

_CODE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _CODE_ROOT)
from paths import DEMO_TASK2  # noqa: E402

SCAN = "Drawer_Cups"
QS = [("q01", "top drawer"), ("q02", "second from top"),
      ("q03", "third from top"), ("q04", "bottom drawer")]
SHARED = ("Self-scanned kitchen, out of distribution.  "
          '"Open the [ top | second | third | bottom ] drawer of the cabinet with cups directly on top."')
PAD, GAP, CAP, HEAD = 26, 18, 76, 148


def font(size, bold=False):
    for p in ("/System/Library/Fonts/Supplemental/Helvetica.ttc",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/Library/Fonts/Arial.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size, index=1 if bold and p.endswith(".ttc") else 0)
            except Exception:
                pass
    return ImageFont.load_default()


def _runs(mask, minlen):
    """Contiguous True runs of at least `minlen`, as (start, stop) pairs."""
    out, s = [], None
    for i, v in enumerate(np.append(mask, False)):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if i - s >= minlen:
                out.append((s, i))
            s = None
    return out


def answer_panel(path):
    """Crop the right-hand 'answer' photo out of a per-question answer.png.

    The panel is located rather than hard-coded. The figure is two photos on white with a
    title above and a caption below, so the photo band is the *longest contiguous* run of
    rows and columns that are non-white over most of their extent -- taking min/max instead
    would swallow the title and the caption.
    """
    a = np.asarray(Image.open(path).convert("RGB"))
    nonwhite = (a < 245).any(axis=2)
    cols = _runs(nonwhite.sum(axis=0) > a.shape[0] * 0.5, 100)
    if len(cols) < 2:
        raise RuntimeError(f"expected two photo panels in {path}, found {len(cols)}")
    x0, x1 = cols[-1]
    band = nonwhite[:, x0:x1]
    rows = _runs(band.sum(axis=1) > (x1 - x0) * 0.9, 100)
    if not rows:
        raise RuntimeError(f"no photo band found in {path}")
    y0, y1 = max(rows, key=lambda r: r[1] - r[0])
    return Image.fromarray(a[y0:y1, x0:x1])


def main():
    panels, picks = [], []
    for qid, _ in QS:
        d = os.path.join(DEMO_TASK2, SCAN, f"{qid}_{SCAN}")
        panels.append(answer_panel(os.path.join(d, "answer.png")))
        picks.append(json.load(open(os.path.join(d, "answer.json")))["final"])

    w, h = panels[0].size
    W = PAD * 2 + w * len(panels) + GAP * (len(panels) - 1)
    H = PAD + HEAD + CAP + h + PAD
    out = Image.new("RGB", (W, H), "white")
    dr = ImageDraw.Draw(out)

    f_head, f_sub, f_cap, f_pick = font(42, True), font(25), font(30, True), font(28, True)
    dr.text((PAD, PAD), "One room, one frame, one set of detections - four instructions",
            font=f_head, fill=(17, 17, 17))
    dr.text((PAD, PAD + 56), SHARED, font=f_sub, fill=(60, 60, 60))
    dr.text((PAD, PAD + 92),
            "Each answer is a single text-only inference over the same candidate table; "
            "no vision model re-reads the image.",
            font=f_sub, fill=(120, 120, 120))

    for i, (p, (qid, phrase)) in enumerate(zip(panels, QS)):
        x = PAD + i * (w + GAP)
        y = PAD + HEAD
        dr.text((x, y), f'"{phrase}"', font=f_cap, fill=(17, 17, 17))
        dr.text((x, y + 40), f"-> drawer handle {picks[i]}", font=f_pick, fill=(198, 40, 40))
        out.paste(p, (x, y + CAP))

    dst = os.path.join(DEMO_TASK2, "four_instructions_one_frame.png")
    out.save(dst, optimize=True)
    print(f"banner -> {dst}  {out.size}  {os.path.getsize(dst)//1024} KB")


if __name__ == "__main__":
    main()
