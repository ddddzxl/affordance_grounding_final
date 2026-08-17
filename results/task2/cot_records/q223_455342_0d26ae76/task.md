# q223_455342_0d26ae76 - visit 455342 / desc 0d26ae76

## Instruction

> Lock the terrace door

## Stage 0 parse

```json
{
 "target": {
  "concept": "door lock",
  "host": "door"
 },
 "entities": [
  {
   "name": "door lock",
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
 "residual": "'terrace' is a room/area-level locator, not groundable; train: 'lock' is a rotate affordance disjoint from the handle (274/274 pairs in train share 0 annotation)"
}
```

## Selected frame

- `455342/44358471/46568.990`  (1920x1440)
- relaxation level **L0**, chosen from 97 frames (stride 10)
- top-8 alternative frames: `[['44358471', '46568.990'], ['44358472', '46641.095'], ['44358472', '46649.392'], ['44358471', '46597.296'], ['44358472', '46642.095'], ['44358471', '46569.990'], ['44358472', '46609.091'], ['44358471', '46574.988']]`

## Candidate counts (after NMS)

- `door lock` (target): **3**
- `door` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
