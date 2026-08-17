# q297_466437_e7121d04 - visit 466437 / desc e7121d04

## Instruction

> Open the bottom right drawer of the cabinet with the mirror and beauty products on top

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
   "name": "mirror",
   "role": "landmark",
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
   "b": "mirror"
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

- `466437/45260951/6108.217`  (1440x1920)
- relaxation level **L2**, chosen from 257 frames (stride 10)
- top-2 alternative frames: `[['45260951', '6108.217'], ['45260952', '6024.117']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **5**
- `drawer` (host): **6**
- `cabinet` (container): **6**
- `mirror` (landmark): **2**
- `beauty products` (landmark): **6**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
