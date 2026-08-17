# q202_438102_df499dfc - visit 438102 / desc df499dfc

## Instruction

> Close the bedroom door

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
 "residual": "'bedroom' is a room-level locator, not groundable"
}
```

## Selected frame

- `438102/43896249/7551.108`  (1920x1440)
- relaxation level **L0**, chosen from 193 frames (stride 10)
- top-8 alternative frames: `[['43896249', '7551.108'], ['43896244', '7698.797'], ['43896244', '7696.797'], ['43896244', '7695.798'], ['43896244', '7703.794'], ['43896244', '7694.798'], ['43896244', '7740.696'], ['43896247', '7612.599']]`

## Candidate counts (after NMS)

- `door handle` (target): **3**
- `door` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
