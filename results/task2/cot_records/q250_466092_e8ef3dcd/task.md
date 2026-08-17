# q250_466092_e8ef3dcd - visit 466092 / desc e8ef3dcd

## Instruction

> Control the temperature using the radiator dial next to the office desk

## Stage 0 parse

```json
{
 "target": {
  "concept": "radiator knob",
  "host": null
 },
 "entities": [
  {
   "name": "radiator knob",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "desk",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "radiator knob",
   "b": "desk"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466092/44796568/16171.202`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-8 alternative frames: `[['44796568', '16171.202'], ['44796568', '16102.497'], ['44796568', '16111.993'], ['44796562', '15943.296'], ['44796562', '15951.293'], ['44796568', '16165.188'], ['44796562', '15992.393'], ['44796562', '15944.296']]`

## Candidate counts (after NMS)

- `radiator knob` (target): **2**
- `desk` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
