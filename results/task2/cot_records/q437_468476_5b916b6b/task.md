# q437_468476_5b916b6b - visit 468476 / desc 5b916b6b

## Instruction

> Unplug the power strip on the floor

## Stage 0 parse

```json
{
 "target": {
  "concept": "plug",
  "host": "power strip"
 },
 "entities": [
  {
   "name": "plug",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "power strip",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": "'on the floor' — floor is not an instanceable object; the plug sits at the socket end"
}
```

## Selected frame

- `468476/45261686/3769.961`  (1440x1920)
- relaxation level **L0**, chosen from 222 frames (stride 10)
- top-8 alternative frames: `[['45261686', '3769.961'], ['45261681', '3632.668'], ['45261682', '3582.672'], ['45261686', '3770.961'], ['45261686', '3819.474'], ['45261682', '3546.471'], ['45261681', '3634.667'], ['45261686', '3823.472']]`

## Candidate counts (after NMS)

- `plug` (target): **2**
- `power strip` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
