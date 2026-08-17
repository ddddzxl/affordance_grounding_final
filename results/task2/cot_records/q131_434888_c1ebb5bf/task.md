# q131_434888_c1ebb5bf - visit 434888 / desc c1ebb5bf

## Instruction

> Open the drawer of the nightstand between the bed and the window

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
   "name": "nightstand",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "bed",
   "role": "landmark",
   "instanceable": true
  },
  {
   "name": "window",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "nightstand",
   "b": "drawer"
  },
  {
   "rel": "between",
   "a": "nightstand",
   "b": "bed"
  },
  {
   "rel": "between",
   "a": "nightstand",
   "b": "window"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `434888/42899184/184437.808`  (1440x1920)
- relaxation level **L0**, chosen from 105 frames (stride 10)
- top-2 alternative frames: `[['42899184', '184437.808'], ['42899184', '184485.005']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **1**
- `drawer` (host): **1**
- `nightstand` (container): **1**
- `bed` (landmark): **2**
- `window` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
