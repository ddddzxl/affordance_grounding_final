# q121_434888_35fbce64 - visit 434888 / desc 35fbce64

## Instruction

> Open the left closet door next to the door

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
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `434888/42899185/184274.609`  (1440x1920)
- relaxation level **L0**, chosen from 105 frames (stride 10)
- top-8 alternative frames: `[['42899185', '184274.609'], ['42899185', '184277.607'], ['42899185', '184292.701'], ['42899187', '184350.810'], ['42899187', '184351.810'], ['42899184', '184481.906'], ['42899185', '184291.602'], ['42899187', '184388.611']]`

## Candidate counts (after NMS)

- `door handle` (target): **1**
- `closet door` (host): **2**
- `closet` (container): **2**
- `door` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
