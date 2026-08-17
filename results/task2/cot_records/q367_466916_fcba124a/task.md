# q367_466916_fcba124a - visit 466916 / desc fcba124a

## Instruction

> Open the right window above the couch

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
   "name": "couch",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "above",
   "a": "window",
   "b": "couch"
  }
 ],
 "select": [
  {
   "on": "window",
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

- `466916/47331615/18075.003`  (1920x1440)
- relaxation level **L0**, chosen from 306 frames (stride 10)
- top-5 alternative frames: `[['47331615', '18075.003'], ['47331615', '18073.004'], ['47331617', '18210.398'], ['47331617', '18211.398'], ['47331615', '18046.898']]`

## Candidate counts (after NMS)

- `window handle` (target): **1**
- `window` (host): **1**
- `couch` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
