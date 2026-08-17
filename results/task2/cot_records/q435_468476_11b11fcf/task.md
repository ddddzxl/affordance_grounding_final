# q435_468476_11b11fcf - visit 468476 / desc 11b11fcf

## Instruction

> Open the door of the wood stove

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "stove door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "stove door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "wood stove",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "wood stove",
   "b": "stove door"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `468476/45261681/3608.062`  (1440x1920)
- relaxation level **POOL-T**, chosen from 222 frames (stride 10)
- top-8 alternative frames: `[['45261681', '3608.062'], ['45261682', '3553.568'], ['45261682', '3536.475'], ['45261682', '3535.475'], ['45261686', '3829.470'], ['45261686', '3835.467'], ['45261686', '3839.466'], ['45261686', '3788.470']]`

## Candidate counts (after NMS)

- `door handle` (target): **3**
- `stove door` (host): **0**
- `wood stove` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
