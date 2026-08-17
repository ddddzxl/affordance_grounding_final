# q125_434888_5233b292 - visit 434888 / desc 5233b292

## Instruction

> Close the bedroom door

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": "'bedroom' is a room-level locator, not groundable"
}
```

## Selected frame

- `434888/42899184/184414.800`  (1440x1920)
- relaxation level **L0**, chosen from 105 frames (stride 10)
- top-8 alternative frames: `[['42899184', '184414.800'], ['42899187', '184392.710'], ['42899187', '184387.612'], ['42899187', '184385.613'], ['42899187', '184386.612'], ['42899185', '184294.717'], ['42899185', '184277.607'], ['42899185', '184274.609']]`

## Candidate counts (after NMS)

- `door handle` (target): **1**
- `door` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
