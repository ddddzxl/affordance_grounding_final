# q219_438775_f4c143ab - visit 438775 / desc f4c143ab

## Instruction

> Lock the glass door that leads to the kitchen

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
 "residual": "'leads to the kitchen' is a room-level locator, not groundable; train: 'lock' is a rotate affordance disjoint from the handle (274/274 pairs in train share 0 annotation)"
}
```

## Selected frame

- `438775/44358170/62318.151`  (1920x1440)
- relaxation level **L0**, chosen from 266 frames (stride 10)
- top-8 alternative frames: `[['44358170', '62318.151'], ['44358170', '62369.348'], ['44358176', '62281.449'], ['44358176', '62280.449'], ['44358170', '62334.561'], ['44358170', '62317.152'], ['44358176', '62270.453'], ['44358173', '62545.461']]`

## Candidate counts (after NMS)

- `door lock` (target): **2**
- `door` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
