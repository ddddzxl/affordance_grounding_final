# q095_423452_10829eca - visit 423452 / desc 10829eca

## Instruction

> Close the door located between the armchair and the small table

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
  },
  {
   "name": "armchair",
   "role": "landmark",
   "instanceable": true
  },
  {
   "name": "table",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "between",
   "a": "door",
   "b": "armchair"
  },
  {
   "rel": "between",
   "a": "door",
   "b": "table"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `423452/42897422/104033.148`  (1920x1440)
- relaxation level **L0**, chosen from 309 frames (stride 10)
- top-8 alternative frames: `[['42897422', '104033.148'], ['42897422', '104059.137'], ['42897434', '104333.839'], ['42897422', '104058.137'], ['42897426', '104130.740'], ['42897426', '104129.741'], ['42897434', '104161.261'], ['42897434', '104337.937']]`

## Candidate counts (after NMS)

- `door handle` (target): **6**
- `door` (host): **1**
- `armchair` (landmark): **2**
- `table` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
