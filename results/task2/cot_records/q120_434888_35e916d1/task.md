# q120_434888_35e916d1 - visit 434888 / desc 35e916d1

## Instruction

> Open the drawer of the nightstand located to the left of the bed

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
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "nightstand",
   "b": "drawer"
  },
  {
   "rel": "left_of",
   "a": "nightstand",
   "b": "bed"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `434888/42899187/184356.808`  (1440x1920)
- relaxation level **L0**, chosen from 105 frames (stride 10)
- top-4 alternative frames: `[['42899187', '184356.808'], ['42899184', '184437.808'], ['42899184', '184485.005'], ['42899187', '184408.903']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **1**
- `drawer` (host): **1**
- `nightstand` (container): **1**
- `bed` (landmark): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
