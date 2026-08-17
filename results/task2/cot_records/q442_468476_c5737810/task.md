# q442_468476_c5737810 - visit 468476 / desc c5737810

## Instruction

> Control the temperature using the thermostatic radiator valve next to the couch

## Stage 0 parse

```json
{
 "target": {
  "concept": "radiator valve",
  "host": null
 },
 "entities": [
  {
   "name": "radiator valve",
   "role": "target",
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
   "a": "radiator valve",
   "b": "couch"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `468476/45261682/3573.676`  (1440x1920)
- relaxation level **L0**, chosen from 222 frames (stride 10)
- top-1 alternative frames: `[['45261682', '3573.676']]`

## Candidate counts (after NMS)

- `radiator valve` (target): **1**
- `couch` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
