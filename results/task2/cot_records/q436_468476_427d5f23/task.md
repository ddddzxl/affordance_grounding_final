# q436_468476_427d5f23 - visit 468476 / desc 427d5f23

## Instruction

> Close the door next to the white couch

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
   "name": "couch",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "door",
   "b": "couch"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `468476/45261681/3618.674`  (1440x1920)
- relaxation level **L0**, chosen from 222 frames (stride 10)
- top-8 alternative frames: `[['45261681', '3618.674'], ['45261686', '3789.470'], ['45261686', '3790.469'], ['45261681', '3607.062'], ['45261682', '3535.475'], ['45261686', '3752.069'], ['45261686', '3785.472'], ['45261682', '3564.563']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `door` (host): **4**
- `couch` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
