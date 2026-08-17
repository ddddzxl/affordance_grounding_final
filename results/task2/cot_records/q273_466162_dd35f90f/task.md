# q273_466162_dd35f90f - visit 466162 / desc dd35f90f

## Instruction

> Open the top right drawer of the cabinet with the beauty products on top

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

- `466162/44796575/16867.990`  (1920x1440)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-1 alternative frames: `[['44796575', '16867.990']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **2**
- `drawer` (host): **4**
- `cabinet` (container): **3**
- `beauty products` (landmark): **17**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
