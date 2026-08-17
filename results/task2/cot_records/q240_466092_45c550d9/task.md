# q240_466092_45c550d9 - visit 466092 / desc 45c550d9

## Instruction

> Unplug the lamp on the desk

## Stage 0 parse

```json
{
 "target": {
  "concept": "plug",
  "host": "lamp"
 },
 "entities": [
  {
   "name": "plug",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "lamp",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "desk",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "lamp",
   "b": "desk"
  }
 ],
 "select": [],
 "residual": "the plug sits at the socket end, not on the lamp"
}
```

## Selected frame

- `466092/44796562/16011.402`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-6 alternative frames: `[['44796562', '16011.402'], ['44796568', '16143.197'], ['44796568', '16122.989'], ['44796568', '16109.994'], ['44796568', '16121.989'], ['44796568', '16124.205']]`

## Candidate counts (after NMS)

- `plug` (target): **3**
- `lamp` (host): **1**
- `desk` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
