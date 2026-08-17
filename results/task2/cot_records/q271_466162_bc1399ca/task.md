# q271_466162_bc1399ca - visit 466162 / desc bc1399ca

## Instruction

> Open the bottom blue closet door to the right of the fireplace

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
   "name": "fireplace",
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
   "rel": "right_of",
   "a": "closet",
   "b": "fireplace"
  }
 ],
 "select": [
  {
   "on": "closet door",
   "axis": "vertical",
   "value": "bottom",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `466162/44796575/16856.994`  (1920x1440)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-8 alternative frames: `[['44796575', '16856.994'], ['44796575', '16865.991'], ['44796576', '16702.292'], ['44796576', '16704.291'], ['44796575', '16859.993'], ['44796576', '16701.292'], ['44796575', '16866.990'], ['44796579', '16777.594']]`

## Candidate counts (after NMS)

- `door handle` (target): **3**
- `closet door` (host): **3**
- `closet` (container): **3**
- `fireplace` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
