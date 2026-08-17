# q05 - Open the left door of the refrigerator

## Reasoning

`refrigerator #0` covers 51.8% of the frame (score 0.978). Of the three
`refrigerator door` detections:
`#1` (x 657-1232, cx=915) is the **left door** and `#0` (x 1143-1439, cx=1318) the **right**;
`#2` (x 1109-1217, area 2.59%, score 0.438) has a bbox almost coincident with `handle 1` --
it is a handle misdetected as a door rather than an independent door, and is excluded.

The two pulls, `handle 0` (cx=1252) and `handle 1` (cx=1173), are adjacent, sitting either side
of the seam between the doors. CONTAINMENT agrees with the geometry: right door `#0` contains
handle 0, left door `#1` contains handle 1.

`select horizontal=left` -> **handle 1**.

> ⚠️ **This question was answered wrongly at first.** The answer was written against the
> candidate table from before the frame changed (frame 0023); after the frame-selection
> strategy improved, this question moved to frame 0008 and the instance ids were reordered,
> and the table was not re-read. Caught on review against answer.png.
>
> The fix was turned into something a script can block: every answer now carries a frame stamp,
> and the visualiser refuses to render when that stamp disagrees with the current selection.

```json
{"final": [1], "confidence": "high", "kind": "select"}
```
