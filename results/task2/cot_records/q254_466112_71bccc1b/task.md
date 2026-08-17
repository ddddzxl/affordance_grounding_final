# q254_466112_71bccc1b - visit 466112 / desc 71bccc1b

## Instruction

> Control the heat output of the bathroom radiator

## Stage 0 parse

```json
{
 "target": {
  "concept": "radiator knob",
  "host": "radiator"
 },
 "entities": [
  {
   "name": "radiator knob",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "radiator",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": "'bathroom' is a room-level locator, not groundable"
}
```

## Selected frame

- `466112/44796517/3910.516`  (1440x1920)
- relaxation level **POOL**, chosen from 176 frames (stride 10)
- top-8 alternative frames: `[['44796517', '3910.516'], ['44796521', '3972.924'], ['44796520', '4062.022'], ['44796521', '3971.925'], ['44796517', '3911.515'], ['44796517', '3923.527'], ['44796517', '3909.516'], ['44796517', '3925.526']]`

## Candidate counts (after NMS)

- `radiator knob` (target): **2**
- `radiator` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
