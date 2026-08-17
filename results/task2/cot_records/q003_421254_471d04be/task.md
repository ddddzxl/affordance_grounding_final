# q003_421254_471d04be - visit 421254 / desc 471d04be

## Instruction

> Open the top left drawer of the cabinet located to the left of the TV

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

- `421254/42444754/81016.477`  (1440x1920)
- relaxation level **L0**, chosen from 170 frames (stride 10)
- top-4 alternative frames: `[['42444754', '81016.477'], ['42444754', '81017.476'], ['42444755', '80879.483'], ['42444755', '80881.482']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **21**
- `drawer` (host): **15**
- `cabinet` (container): **2**
- `TV` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
