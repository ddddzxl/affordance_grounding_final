# q014_421254_af0b7790 - visit 421254 / desc af0b7790

## Instruction

> Open the bottom drawer of the cabinet located to the left of the TV

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
   "rel": "left_of",
   "a": "cabinet",
   "b": "TV"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "vertical",
   "value": "bottom",
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
- top-6 alternative frames: `[['42444758', '80950.170'], ['42444754', '81017.476'], ['42444754', '81016.477'], ['42444754', '81018.476'], ['42444755', '80884.481'], ['42444755', '80879.483']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **20**
- `drawer` (host): **14**
- `cabinet` (container): **2**
- `TV` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
