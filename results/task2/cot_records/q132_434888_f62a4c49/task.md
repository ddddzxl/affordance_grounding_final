# q132_434888_f62a4c49 - visit 434888 / desc f62a4c49

## Instruction

> Open the right closet door next to the door

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "closet door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "closet door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "closet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "closet",
   "b": "closet door"
  },
  {
   "rel": "next_to",
   "a": "closet",
   "b": "door"
  }
 ],
 "select": [
  {
   "on": "closet door",
   "axis": "horizontal",
   "value": "right",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `434888/42899187/184392.710`  (1440x1920)
- relaxation level **L0**, chosen from 105 frames (stride 10)
- top-8 alternative frames: `[['42899187', '184392.710'], ['42899187', '184385.613'], ['42899187', '184387.612'], ['42899185', '184274.609'], ['42899185', '184277.607'], ['42899187', '184350.810'], ['42899187', '184351.810'], ['42899187', '184386.612']]`

## Candidate counts (after NMS)

- `door handle` (target): **4**
- `closet door` (host): **2**
- `closet` (container): **1**
- `door` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
