# q441_468476_a8be6d90 - visit 468476 / desc a8be6d90

## Instruction

> Unplug the floor lamp next to the couch

## Stage 0 parse

```json
{
 "target": {
  "concept": "plug",
  "host": "floor lamp"
 },
 "entities": [
  {
   "name": "plug",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "floor lamp",
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
   "a": "floor lamp",
   "b": "couch"
  }
 ],
 "select": [],
 "residual": "the plug sits at the socket end, not on the lamp"
}
```

## Selected frame

- `468476/45261682/3547.470`  (1440x1920)
- relaxation level **L0**, chosen from 222 frames (stride 10)
- top-8 alternative frames: `[['45261682', '3547.470'], ['45261682', '3542.472'], ['45261681', '3622.672'], ['45261686', '3770.961'], ['45261681', '3632.668'], ['45261686', '3768.962'], ['45261682', '3543.472'], ['45261682', '3545.471']]`

## Candidate counts (after NMS)

- `plug` (target): **3**
- `floor lamp` (host): **1**
- `couch` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
