# q264_466162_5a54c80a - visit 466162 / desc 5a54c80a

## Instruction

> Open the window above the radiator

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
   "name": "radiator",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "above",
   "a": "window",
   "b": "radiator"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466162/44796576/16715.286`  (1920x1440)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-8 alternative frames: `[['44796576', '16715.286'], ['44796575', '16892.180'], ['44796579', '16831.788'], ['44796579', '16788.589'], ['44796579', '16782.592'], ['44796576', '16726.282'], ['44796579', '16787.590'], ['44796579', '16783.591']]`

## Candidate counts (after NMS)

- `window handle` (target): **7**
- `window` (host): **1**
- `radiator` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
