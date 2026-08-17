# q008_421254_71e753ae - visit 421254 / desc 71e753ae

## Instruction

> Open the top right drawer of the cabinet with the TV on top

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

- `421254/42444754/81018.476`  (1440x1920)
- relaxation level **L0**, chosen from 170 frames (stride 10)
- top-3 alternative frames: `[['42444754', '81018.476'], ['42444758', '80953.586'], ['42444755', '80884.481']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **16**
- `drawer` (host): **11**
- `cabinet` (container): **3**
- `TV` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
