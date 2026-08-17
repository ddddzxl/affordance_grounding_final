# q053_422356_a54ff5a7 - visit 422356 / desc a54ff5a7

## Instruction

> Lower the room's temperature using the radiator thermostat

## Stage 0 parse

```json
{
 "target": {
  "concept": "dial",
  "host": "radiator"
 },
 "entities": [
  {
   "name": "dial",
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
 "residual": null
}
```

## Selected frame

- `422356/42446576/205903.960`  (1920x1440)
- relaxation level **L0**, chosen from 115 frames (stride 10)
- top-2 alternative frames: `[['42446576', '205903.960'], ['42446579', '205784.459']]`

## Candidate counts (after NMS)

- `dial` (target): **1**
- `radiator` (host): **0**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
