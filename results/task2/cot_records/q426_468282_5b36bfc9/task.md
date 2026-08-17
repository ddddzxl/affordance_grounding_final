# q426_468282_5b36bfc9 - visit 468282 / desc 5b36bfc9

## Instruction

> Close the bathroom door

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
 "residual": "'bathroom' is a room-level locator, not groundable"
}
```

## Selected frame

- `468282/47331279/14318.317`  (1440x1920)
- relaxation level **L0**, chosen from 215 frames (stride 10)
- top-8 alternative frames: `[['47331279', '14318.317'], ['47331279', '14310.704'], ['47331279', '14321.316'], ['47331281', '14152.019'], ['47331279', '14315.318'], ['47331279', '14262.707'], ['47331281', '14150.019'], ['47331281', '14143.006']]`

## Candidate counts (after NMS)

- `door handle` (target): **1**
- `door` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
