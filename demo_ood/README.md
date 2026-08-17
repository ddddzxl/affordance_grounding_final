# Out-of-distribution demo: referring affordance grounding on self-scanned rooms

> Three household scenes scanned on site with an iPhone (3D Scanner App), 13 instructions.
> **Fully out of distribution**: the method was fixed on SceneFun3D, and this changes the
> capture device, the scenes, the lighting and the objects.
> There is no ground truth, so nothing is scored -- what is presented is **the reasoning chain
> itself**. All 13 are correct under per-question manual review.

## The vision side runs once

```
scene              frames   concepts   seg calls   instr.   if re-run per instruction
Drawer_Cups            32          4         128        4                         512
Kitchen_Task2          89         12        1068        8                        2047
Sofa_Switch            40          2          80        1                          80
total                                       1276       13                        2639
```

Instructions in the same scene **share one set of detections**, so adding instructions adds no
segmentation calls at all -- a **52% saving** after deduplication. The four Drawer_Cups
questions are the clearest case: they share one frame and one set of detections, and differ
only in the parsed ordering constraint.

Each instruction additionally costs **one text-only LLM inference** (reading the candidate
table to select an instance). No VLM ever reads an image.

## The 13 instructions

| # | scene | instruction | frame | target concept | selected | conf. | criterion |
|---|---|---|---|---|---|---|---|
| [q01](Drawer_Cups/q01_Drawer_Cups/) | Drawer_Cups | Open the top drawer of the cabinet with cups directly on top | 0017 | `drawer handle` | **[1]** | high | select |
| [q02](Drawer_Cups/q02_Drawer_Cups/) | Drawer_Cups | Open the second drawer from the top of the cabinet with cups directly on top | 0017 | `drawer handle` | **[0]** | high | ordinal |
| [q03](Drawer_Cups/q03_Drawer_Cups/) | Drawer_Cups | Open the third drawer from the top of the cabinet with cups directly on top | 0017 | `drawer handle` | **[2]** | high | ordinal |
| [q04](Drawer_Cups/q04_Drawer_Cups/) | Drawer_Cups | Open the bottom drawer of the cabinet with cups directly on top | 0017 | `drawer handle` | **[3]** | high | select |
| [q05](Kitchen_Task2/q05_Kitchen_Task2/) | Kitchen_Task2 | Open the left door of the refrigerator | 0008 | `refrigerator door handle` | **[1]** | high | select |
| [q06](Kitchen_Task2/q06_Kitchen_Task2/) | Kitchen_Task2 | Open the right door of the refrigerator | 0008 | `refrigerator door handle` | **[0]** | high | select |
| [q07](Kitchen_Task2/q07_Kitchen_Task2/) | Kitchen_Task2 | Open the left door of the cabinet above the refrigerator | 0019 | `cabinet knob` | **[0]** | high | select |
| [q08](Kitchen_Task2/q08_Kitchen_Task2/) | Kitchen_Task2 | Open the right door of the cabinet above the refrigerator | 0019 | `cabinet knob` | **[1]** | high | select |
| [q09](Kitchen_Task2/q09_Kitchen_Task2/) | Kitchen_Task2 | Open the door of the pantry to the left of the refrigerator | 0011 | `door handle` | **[2]** | high | relation |
| [q10](Kitchen_Task2/q10_Kitchen_Task2/) | Kitchen_Task2 | Plug in the air fryer using the nearest socket | 0081 | `socket` | **[1]** | medium | relation |
| [q11](Kitchen_Task2/q11_Kitchen_Task2/) | Kitchen_Task2 | Plug in the Ninja blender using the nearest socket | 0039 | `socket` | **[0]** | low | detection_quality |
| [q12](Kitchen_Task2/q12_Kitchen_Task2/) | Kitchen_Task2 | Plug in the Instant Pot using the nearest socket | 0074 | `socket` | **[0]** | medium | relation |
| [q13](Sofa_Switch/q13_Sofa_Switch/) | Sofa_Switch | Turn on the light using the switch near the sofa | 0014 | `light switch` | **[0, 1, 2]** | medium | relation |

### Corrections

- **q05** was originally answered [0], and **q06** originally [1]. Both answers had been
  written against the candidate table from before the frame changed (frame 0023); after the
  frame-selection strategy improved, these questions moved to frame 0008 and the instance ids
  were reordered, and the table was not re-read -- so left and right came out swapped. Caught
  on review against `answer.png`.

  The fix was turned into something a script can block: every answer now carries a frame stamp,
  and the visualiser refuses to render when that stamp disagrees with the current frame
  selection.

## What is in each question directory

```
frame.jpg              the selected frame
candidates.txt         the candidate table -- the sole reasoning input (symbolic, no image)
candidates.png         candidates: mask on the target, instance boxes + ids on the rest
candidates_mask.png    candidates: instance masks for every concept, low opacity, colour coded
task.md                instruction + parse + frame-selection notes
cot.md                 the reasoning
answer.json            final / confidence / kind / note
answer.png             the selected target highlighted, the rest greyed out
answer_mask.png        left = instance masks per concept, right = the selection
```

## Geometry self-check, done before any model was run

The exported jpgs are 1920x1440 stored landscape with EXIF orientation=6, while the intrinsics
are given relative to the landscape original. Folding the orientation into the intrinsics
matrix is **wrong** -- K cannot express an axis swap, so the 3D points still project in the
landscape frame while the image has been rotated upright: a 90 degree discrepancy in which the
projected points still "look like they land on the image", and which no summary statistic
reveals.

The correct approach is to project in the original frame first, then apply a pure 2D transform
to the pixel coordinates. Verified by correlating the point cloud's own colour against the
colour sampled at its projected pixel: **-0.23 before the fix, +0.89 after**.

```
                dRGB   shuffle baseline   median corr   frames with corr >= 0.5
Drawer_Cups     14.8               67.9         0.899   32/32 (100%)
Kitchen_Task2   22.8               67.9         0.837   87/89 ( 98%)
Sofa_Switch     15.4               63.5         0.911   40/40 (100%)
```

The shuffle baseline is dRGB recomputed after shuffling the point order, i.e. the level
corresponding to "completely unaligned". See `selfcheck/` in each scene.

## Known limitations, recorded as observed

**1. The segmenter does not recognise branded, oddly shaped small appliances.** `blender` is
detected in only 2 of 89 frames, at score 0.466; `food processor` / `juicer` / `mixer` all
return zero; only the generic term `kitchen appliance` detects anything (5.7 per frame on
average), and it cannot tell which appliance is which. q11 is therefore recorded as
`low` / `detection_quality`. Controls: `air fryer`, `pressure cooker`, `socket` and
`cabinet knob` all behave normally -- the difference is that the former is a branded, irregular
product while the latter have a stable generic shape.

**2. Automatic frame selection: each relation holding individually is not the whole chain
holding.** For q07 and q08, automatic selection returned the frame with the most knob
detections, and in that frame `above(cabinet, refrigerator)` does hold when checked
individually (some cabinet is above the refrigerator) -- but that cabinet is not the door the
target knob is on, so the chain breaks in the middle. Frame 0019 was specified manually, with
the reason written into `q07/task.md`. A real fix requires upgrading the criterion from "each
relation individually" to "target -> host -> container -> landmark all land on the same set of
instances".

**3. No ground truth.** This demo produces no score and does not lift to 3D -- without ground
truth a 3D mask cannot be verified, whereas a reasoning chain can be checked step by step. All
quantitative results come from the 442 SceneFun3D val instructions; see
[`../results/main_table.md`](../results/main_table.md).

Related: when the instruction itself is underdetermined, the method can only answer as a group.
q13's "the switch near the sofa" corresponds to a three-gang switch plate, and the instruction
gives no basis for distinguishing within it, so all three rockers are returned.

## Not shipped here

The per-frame detection caches (`cache/*.npz`) and the raw point clouds are omitted; they are
intermediate tensors, and everything needed to read the demo is text and figures. The pipeline
that produced this directory is in [`../code/demo/`](../code/demo/).
