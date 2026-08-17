# q231_455342_b91e7c76 - visit 455342 / desc b91e7c76

## Instruction

> Open the top right window

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
   "axis": "vertical",
   "value": "top",
   "index": null,
   "from": null
  },
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

- `455342/44358472/46641.095`  (1920x1440)
- relaxation level **L0**, chosen from 97 frames (stride 10)
- top-8 alternative frames: `[['44358472', '46641.095'], ['44358472', '46649.392'], ['44358471', '46551.397'], ['44358471', '46569.990'], ['44358472', '46608.091'], ['44358471', '46570.990'], ['44358472', '46610.091'], ['44358472', '46620.087']]`

## Candidate counts (after NMS)

- `window handle` (target): **3**
- `window` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
