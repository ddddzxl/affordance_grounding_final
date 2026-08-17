# q321_466880_0d719672 - visit 466880 / desc 0d719672

## Instruction

> Open the window above the kitchen sink

## Stage 0 parse

```json
{
 "target": {
  "concept": "window handle",
  "host": "window"
 },
 "entities": [
  {
   "name": "window handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "window",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "sink",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "above",
   "a": "window",
   "b": "sink"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466880/47331711/11298.727`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-8 alternative frames: `[['47331711', '11298.727'], ['47331710', '11196.136'], ['47331711', '11275.937'], ['47331710', '11215.228'], ['47331710', '11200.134'], ['47331707', '11143.540'], ['47331711', '11297.728'], ['47331711', '11307.840']]`

## Candidate counts (after NMS)

- `window handle` (target): **6**
- `window` (host): **1**
- `sink` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
