# q104_423452_fad84426 - visit 423452 / desc fad84426

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

- `423452/42897434/104182.436`  (1920x1440)
- relaxation level **L0**, chosen from 309 frames (stride 10)
- top-8 alternative frames: `[['42897434', '104182.436'], ['42897422', '104034.147'], ['42897434', '104192.148'], ['42897426', '104146.734'], ['42897426', '104145.734'], ['42897426', '104142.735'], ['42897422', '104058.137'], ['42897434', '104327.842']]`

## Candidate counts (after NMS)

- `window handle` (target): **1**
- `window` (host): **1**
- `couch` (landmark): **4**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
