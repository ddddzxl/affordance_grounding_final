# q13 - Turn on the light using the switch near the sofa

## Reasoning

The three `light switch` bboxes abut one another along x (215-279 | 275-334 | 340-389), share
almost the same y interval, and have comparable areas (0.141 / 0.153 / 0.158) -- these are
**three rockers on one three-gang switch plate**, not three switches in different places.

`sofa` covers 37.9% of the frame (x 342-1439), and the three switches' distances to it (832 /
897 / 863) barely differ, so `near` cannot discriminate within the plate.

The instruction "the switch near the sofa" supplies only a regional constraint, with no
left/right or ordinal cue to separate the rockers, so nothing in the detections can single one
out. Treated under "components of one physical device are emitted together": all three.

```json
{"final": [0, 1, 2], "confidence": "medium", "kind": "relation"}
```

> This is one of the three limitations recorded for this demo: when the instruction itself is
> underdetermined, the method can only answer as a group.
