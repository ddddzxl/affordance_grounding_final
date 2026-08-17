# q099_423452_3d6028fe - visit 423452 / desc 3d6028fe

## Instruction

> Close the door next to the red armchair

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
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "door",
   "b": "armchair"
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

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
