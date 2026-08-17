# q030_421393_729dc0d8 - visit 421393 / desc 729dc0d8

## Instruction

> Adjust the room's temperature using the radiator dial

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
 "residual": null
}
```

## Selected frame

- `421393/42444924/220963.062`  (1440x1920)
- relaxation level **L0**, chosen from 137 frames (stride 10)
- top-8 alternative frames: `[['42444924', '220963.062'], ['42444924', '220964.062'], ['42444923', '220886.960'], ['42444924', '220958.064'], ['42444923', '220878.064'], ['42444923', '220887.959'], ['42444924', '220965.061'], ['42444924', '220962.063']]`

## Candidate counts (after NMS)

- `radiator knob` (target): **3**
- `radiator` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
