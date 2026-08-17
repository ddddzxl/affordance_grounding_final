# q256_466112_a33e9853 - visit 466112 / desc a33e9853

## Instruction

> Open the door to the left of the bathtub

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
   "name": "bathtub",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "left_of",
   "a": "door",
   "b": "bathtub"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466112/44796521/3958.413`  (1440x1920)
- relaxation level **L0**, chosen from 176 frames (stride 10)
- top-6 alternative frames: `[['44796521', '3958.413'], ['44796521', '3957.414'], ['44796517', '3896.221'], ['44796521', '3988.918'], ['44796517', '3886.225'], ['44796520', '4026.220']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `door` (host): **2**
- `bathtub` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
