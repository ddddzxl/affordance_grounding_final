# q263_466162_58d4ab4f - visit 466162 / desc 58d4ab4f

## Instruction

> Open the bottom blue closet drawer to the right of the fireplace

## Stage 0 parse

```json
{
 "target": {
  "concept": "drawer handle",
  "host": "drawer"
 },
 "entities": [
  {
   "name": "drawer handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "drawer",
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
   "b": "drawer"
  },
  {
   "rel": "right_of",
   "a": "closet",
   "b": "fireplace"
  }
 ],
 "select": [
  {
   "on": "drawer",
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

- `466162/44796576/16702.292`  (1920x1440)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-5 alternative frames: `[['44796576', '16702.292'], ['44796579', '16777.594'], ['44796575', '16865.991'], ['44796576', '16701.292'], ['44796576', '16704.291']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **3**
- `drawer` (host): **2**
- `closet` (container): **2**
- `fireplace` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
