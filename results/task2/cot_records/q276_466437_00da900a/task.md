# q276_466437_00da900a - visit 466437 / desc 00da900a

## Instruction

> Open the top right drawer of the cabinet with the mirror and beauty products on top

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
   "value": "top",
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

- `466437/45260952/6024.117`  (1440x1920)
- relaxation level **L2**, chosen from 257 frames (stride 10)
- top-2 alternative frames: `[['45260952', '6024.117'], ['45260951', '6108.217']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **21**
- `drawer` (host): **9**
- `cabinet` (container): **2**
- `mirror` (landmark): **3**
- `beauty products` (landmark): **18**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
