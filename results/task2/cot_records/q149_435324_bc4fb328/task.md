# q149_435324_bc4fb328 - visit 435324 / desc bc4fb328

## Instruction

> Open the closet door between the cabinet and the door

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "closet door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "closet door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "cabinet",
   "role": "landmark",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "between",
   "a": "closet door",
   "b": "cabinet"
  },
  {
   "rel": "between",
   "a": "closet door",
   "b": "door"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `435324/42899216/188220.296`  (1920x1440)
- relaxation level **L0**, chosen from 161 frames (stride 10)
- top-8 alternative frames: `[['42899216', '188220.296'], ['42899216', '188223.411'], ['42899220', '188313.107'], ['42899221', '188348.993'], ['42899221', '188350.009'], ['42899220', '188272.508'], ['42899216', '188245.002'], ['42899216', '188222.295']]`

## Candidate counts (after NMS)

- `door handle` (target): **7**
- `closet door` (host): **2**
- `cabinet` (landmark): **2**
- `door` (landmark): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
