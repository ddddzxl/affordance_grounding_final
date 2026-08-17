# q196_438102_60755ffb - visit 438102 / desc 60755ffb

## Instruction

> Open the window behind the miniature flags

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
   "name": "flags",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "behind",
   "a": "window",
   "b": "flags"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `438102/43896247/7598.605`  (1920x1440)
- relaxation level **L0**, chosen from 193 frames (stride 10)
- top-1 alternative frames: `[['43896247', '7598.605']]`

## Candidate counts (after NMS)

- `window handle` (target): **1**
- `window` (host): **9**
- `flags` (landmark): **4**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
