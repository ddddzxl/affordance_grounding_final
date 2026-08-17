# q406_467115_e0a55b57 - visit 467115 / desc e0a55b57

## Instruction

> Open the top middle cabinet door located to the left of the dining table

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "cabinet door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "cabinet door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "dining table",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "cabinet",
   "b": "cabinet door"
  },
  {
   "rel": "left_of",
   "a": "cabinet",
   "b": "dining table"
  }
 ],
 "select": [
  {
   "on": "cabinet door",
   "axis": "vertical",
   "value": "top",
   "index": null,
   "from": null
  },
  {
   "on": "cabinet door",
   "axis": "horizontal",
   "value": "middle",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `467115/47333310/28241.654`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-1 alternative frames: `[['47333310', '28241.654']]`

## Candidate counts (after NMS)

- `door handle` (target): **10**
- `cabinet door` (host): **6**
- `cabinet` (container): **2**
- `dining table` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
