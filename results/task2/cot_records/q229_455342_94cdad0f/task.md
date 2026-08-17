# q229_455342_94cdad0f - visit 455342 / desc 94cdad0f

## Instruction

> Open the glass door that leads to the terrace

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
 "residual": "'leads to the terrace' is a room/area-level locator, not groundable"
}
```

## Selected frame

- `455342/44358471/46568.990`  (1920x1440)
- relaxation level **L0**, chosen from 97 frames (stride 10)
- top-8 alternative frames: `[['44358471', '46568.990'], ['44358472', '46641.095'], ['44358472', '46649.392'], ['44358472', '46620.087'], ['44358472', '46626.101'], ['44358472', '46642.095'], ['44358471', '46569.990'], ['44358471', '46574.988']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `door` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
