# q012_421254_ae0b0b18 - visit 421254 / desc ae0b0b18

## Instruction

> Open the second drawer of the cabinet with the TV on top

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
   "name": "TV",
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
   "b": "TV"
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

- `421254/42444755/80884.481`  (1440x1920)
- relaxation level **L0**, chosen from 170 frames (stride 10)
- top-2 alternative frames: `[['42444755', '80884.481'], ['42444754', '81018.476']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **17**
- `drawer` (host): **11**
- `cabinet` (container): **2**
- `TV` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
