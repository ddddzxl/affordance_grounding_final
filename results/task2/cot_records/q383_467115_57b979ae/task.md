# q383_467115_57b979ae - visit 467115 / desc 57b979ae

## Instruction

> Open the bottom, right cabinet drawer located to the left of the dining table

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
   "b": "drawer"
  },
  {
   "rel": "left_of",
   "a": "cabinet",
   "b": "dining table"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "vertical",
   "value": "bottom",
   "index": null,
   "from": null
  },
  {
   "on": "drawer",
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

- `467115/47333310/28241.654`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-1 alternative frames: `[['47333310', '28241.654']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **10**
- `drawer` (host): **6**
- `cabinet` (container): **2**
- `dining table` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
