# q198_438102_a65c425a - visit 438102 / desc a65c425a

## Instruction

> Open the bottom drawer of the nightstand in front of the window

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
   "rel": "in_front_of",
   "a": "nightstand",
   "b": "window"
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

- `438102/43896249/7546.110`  (1920x1440)
- relaxation level **L0**, chosen from 193 frames (stride 10)
- top-7 alternative frames: `[['43896249', '7546.110'], ['43896249', '7549.109'], ['43896247', '7590.608'], ['43896247', '7592.607'], ['43896249', '7572.099'], ['43896249', '7545.110'], ['43896247', '7621.712']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **5**
- `drawer` (host): **2**
- `nightstand` (container): **2**
- `window` (landmark): **4**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
