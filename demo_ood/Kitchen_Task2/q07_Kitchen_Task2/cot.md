# q07 - Open the left door of the cabinet above the refrigerator

## Reasoning

**The frame for this question was specified manually** (reasoning in task.md): automatic
selection prefers the frame with the most knob detections, but in that frame the refrigerator
shows only a strip at the far left and there is no knob above it.

In frame 0019 the refrigerator is detected as two halves (`refrigerator #1` x 8-648 and `#0`
x 639-1369, scores 0.919 / 0.952), and the two wall-cabinet doors `cabinet door #1`
(x 12-764, cx=390) and `#0` (x 785-1439, cx=1116) sit directly above them respectively, so
`above(cabinet, refrigerator)` holds. The two knobs at cx=727 and 832 belong to one door each.

`select horizontal=left` -> `door #1` -> **knob 0**.

```json
{"final": [0], "confidence": "high", "kind": "select"}
```
