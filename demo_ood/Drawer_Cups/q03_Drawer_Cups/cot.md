# q03 - Open the third drawer from the top of the cabinet with cups directly on top

## Reasoning

**Step 1 - use the landmark to fix the container.**
The three `cup` detections have cy between 765 and 873, all at worktop height.
`has_on_top(cabinet, cup)` requires the carcass to be directly below them and to span them in
x: `cabinet #3` (x 471-1185, y 1011-1919) satisfies this; `cabinet #2` (x 1111-1439) does not
overlap the cups' x range (485-1039) at all and is excluded; `cabinet #0/#1` (y 0-132) are at
the top of the frame and are wall units.
**Target container = cabinet #3.**

**Step 2 - which drawers are in that container.**
`contains(cabinet #3, drawer)`: the bboxes of drawers 0/1/2/3 all fall inside #3;
drawer #4 (x 1185-1439) belongs to cabinet #2 on the right and is excluded. Sorting the four by
cy: `#0` (1184) -> `#1` (1379) -> `#2` (1547) -> `#3` (1737), matching the four physical layers.

**Step 3 - which handle each drawer yields.**
Every CONTAINMENT row is tagged `[via bbox]` (the segmenter cut the metal handles out of the
drawer fronts, so the mask test found nothing), and `drawer #3 contains [2, 3]` because
drawers #2 and #3 overlap in y and handle 2 falls in the intersection.
So **do not rely on containment here**; judge from the handles' own geometry instead:
`handle 1/0/2/3` all have cx between 875 and 894, with cy at 1191 / 1387 / 1554 / 1759, evenly
spaced -- one column of four, top to bottom. Excluded: `handle 4` (cx 1226) is in a different
column to the right; `handle 5/7` (cy ~ 60) are at the top of the frame and belong to the wall
units; `handle 6` has area 0.005% at score 0.525 and is an edge fragment.

**Step 4 - select.**
`on='drawer' -> 3rd` applies to that column, giving **handle 2** (third from the top,
cy=1554).

```json
{"final": [2], "confidence": "high", "kind": "ordinal"}
```
