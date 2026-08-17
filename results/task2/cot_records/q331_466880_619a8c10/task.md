# q331_466880_619a8c10 - visit 466880 / desc 619a8c10

## Instruction

> Select an oven setting

## Stage 0 parse

```json
{
 "target": {
  "concept": "oven knob",
  "host": "oven"
 },
 "entities": [
  {
   "name": "oven knob",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "oven",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": "no disambiguating cue — any of the oven controls is acceptable"
}
```

## Selected frame

- `466880/47331707/11119.534`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-8 alternative frames: `[['47331707', '11119.534'], ['47331707', '11115.035'], ['47331711', '11260.726'], ['47331710', '11179.626'], ['47331707', '11125.831'], ['47331707', '11126.831'], ['47331710', '11181.642'], ['47331711', '11259.727']]`

## Candidate counts (after NMS)

- `oven knob` (target): **8**
- `oven` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
