# q433_468476_0910cdb0 - visit 468476 / desc 0910cdb0

## Instruction

> Plug the device in one of the power strip outlets on the floor

## Stage 0 parse

```json
{
 "target": {
  "concept": "power strip outlet",
  "host": "power strip"
 },
 "entities": [
  {
   "name": "power strip outlet",
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
 "residual": "'on the floor' — floor is not an instanceable object; 'one of the outlets' — any instance is acceptable"
}
```

## Selected frame

- `468476/45261686/3769.961`  (1440x1920)
- relaxation level **L0**, chosen from 222 frames (stride 10)
- top-8 alternative frames: `[['45261686', '3769.961'], ['45261681', '3632.668'], ['45261686', '3770.961'], ['45261682', '3546.471'], ['45261686', '3823.472'], ['45261686', '3821.473'], ['45261686', '3820.474'], ['45261686', '3766.963']]`

## Candidate counts (after NMS)

- `power strip outlet` (target): **2**
- `power strip` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
