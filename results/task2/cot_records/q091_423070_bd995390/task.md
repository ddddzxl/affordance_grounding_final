# q091_423070_bd995390 - visit 423070 / desc bd995390

## Instruction

> Close the bathroom door

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": "'bathroom' room-level locator - ignored"
}
```

## Selected frame

- `423070/42447205/209355.188`  (1920x1440)
- relaxation level **L0**, chosen from 251 frames (stride 10)
- top-8 alternative frames: `[['42447205', '209355.188'], ['42447202', '209401.986'], ['42447205', '209334.181'], ['42447202', '209461.178'], ['42447210', '209256.579'], ['42447210', '209189.690'], ['42447202', '209477.788'], ['42447202', '209428.675']]`

## Candidate counts (after NMS)

- `door handle` (target): **1**
- `door` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
