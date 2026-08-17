# q034_421393_ca7efe7c - visit 421393 / desc ca7efe7c

## Instruction

> Close the wooden bedroom door

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
 "residual": "'bedroom' room-level locator; 'wooden' colour/material - both ignored"
}
```

## Selected frame

- `421393/42444924/220959.064`  (1440x1920)
- relaxation level **L0**, chosen from 137 frames (stride 10)
- top-8 alternative frames: `[['42444924', '220959.064'], ['42444923', '220925.261'], ['42444924', '220969.060'], ['42444924', '220973.058'], ['42444923', '220935.257'], ['42444923', '220938.256'], ['42444923', '220903.253'], ['42444923', '220937.256']]`

## Candidate counts (after NMS)

- `door handle` (target): **6**
- `door` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
