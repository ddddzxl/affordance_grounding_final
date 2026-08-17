# q004_421254_52d91158 - visit 421254 / desc 52d91158

## Instruction

> Open the top left drawer of the cabinet with the TV on top

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
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `421254/42444758/80950.170`  (1440x1920)
- relaxation level **L0**, chosen from 170 frames (stride 10)
- top-6 alternative frames: `[['42444758', '80950.170'], ['42444755', '80884.481'], ['42444754', '81017.476'], ['42444754', '81018.476'], ['42444754', '81016.477'], ['42444755', '80879.483']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **20**
- `drawer` (host): **14**
- `cabinet` (container): **2**
- `TV` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
