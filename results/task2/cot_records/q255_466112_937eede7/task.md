# q255_466112_937eede7 - visit 466112 / desc 937eede7

## Instruction

> Open the left window part

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
  }
 ],
 "relations": [],
 "select": [
  {
   "on": "window",
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

- `466112/44796521/3976.923`  (1440x1920)
- relaxation level **L0**, chosen from 176 frames (stride 10)
- top-8 alternative frames: `[['44796521', '3976.923'], ['44796520', '4094.826'], ['44796520', '4023.221'], ['44796517', '3883.226'], ['44796517', '3887.225'], ['44796521', '3943.319'], ['44796517', '3920.512'], ['44796520', '4043.213']]`

## Candidate counts (after NMS)

- `window handle` (target): **2**
- `window` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
