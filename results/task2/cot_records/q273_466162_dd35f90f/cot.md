# q273

**Instruction**: Open the top right drawer of the cabinet with the beauty products on top

**target**: `drawer handle`   **host**: `drawer`

## select applies to the **host (drawer)**, not to the handles

| drawer | cx | cy | note |
|---|---|---|---|
| #3 | 655.0 | **664.1** | upper |
| #0 | 625.6 | 732.2 | upper |
| #1 | 600.4 | 797.1 | |
| #2 | 1076.5 | 951.5 | w=838, 23.4% of the image, score 0.217 -- a merged block, excluded |

- `vertical top` -> the two upper ones: `#3` (664) and `#0` (732)
- `horizontal right` -> the larger cx of those = **`drawer#3`** (655 > 626)

Both select clauses resolve without conflicting.

## Output

Containment: `drawer#3 contains #0` -> **handle #0**.
(`drawer#0 contains #0` points at the same handle -- `#0` and `#3` overlap heavily in x and y
and are two detections of one drawer.)

## Confidence low

The drawer detections are poor overall: 0.458 / 0.255 / 0.217 / 0.151, none above 0.5, and `#2`
merges most of the cabinet into one box. The top/right reasoning above rests on the cx and cy
of those weak boxes, which is not solid.

There are also only two handles in the whole frame (`#0` cy 653 and `#1` cy 1027), whereas "top
right" implies a cabinet of at least 2x2 -- which suggests **the drawer corresponding to the
ground truth probably had no handle detected at all**.

## Why the handle layer is not the place to compare

Comparing cy **between the two handles** reaches the same answer by an invalid route.
`select` may only apply to the host -- left/right and up/down have no meaning at the handle
layer, only at the host layer.

**FINAL: #0**   confidence **low**
