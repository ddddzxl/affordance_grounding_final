# q09 - Open the door of the pantry to the left of the refrigerator

## Reasoning

`refrigerator #0` covers 58.9% of the frame (score 0.963), spanning x 142-1311.

`left_of(door, refrigerator)` requires the door to be left of the refrigerator: `door #0`
(x 0-214, cx=74) satisfies it; `door #1` (cx=1060) is to the right and is excluded; `door #2`
(x 144-909) almost entirely overlaps the refrigerator -- it *is* the refrigerator door, not an
independent one.

`door handle 0/1` (area 2.0 / 1.8, elongated) are the refrigerator's two pulls and are excluded
along with it; `handle 3/4` (area 0.025, cx ~ 1400) are at the right edge of the frame.

That leaves `handle 2` (cx=18.5, area 0.114), which CONTAINMENT also assigns to `door #0`.
-> **handle 2**.

```json
{"final": [2], "confidence": "high", "kind": "relation"}
```
