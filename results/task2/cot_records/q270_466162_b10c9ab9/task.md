# q270_466162_b10c9ab9 - visit 466162 / desc b10c9ab9

## Instruction

> Open the second drawer of the cabinet with the beauty products on top

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
   "name": "beauty products",
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
   "rel": "has_on_top",
   "a": "cabinet",
   "b": "beauty products"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "ordinal",
   "value": null,
   "index": 2,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `466162/44796576/16751.688`  (1920x1440)
- relaxation level **L1**, chosen from 257 frames (stride 10)
- top-1 alternative frames: `[['44796576', '16751.688']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **12**
- `drawer` (host): **9**
- `cabinet` (container): **2**
- `beauty products` (landmark): **18**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
