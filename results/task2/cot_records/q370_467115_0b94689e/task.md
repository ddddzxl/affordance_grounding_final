# q370_467115_0b94689e - visit 467115 / desc 0b94689e

## Instruction

> Control the temperature using the radiator dial under the kitchen window

## Stage 0 parse

```json
{
 "target": {
  "concept": "radiator dial",
  "host": null
 },
 "entities": [
  {
   "name": "radiator dial",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "window",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "under",
   "a": "radiator dial",
   "b": "window"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467115/47333319/28534.151`  (1440x1920)
- relaxation level **L1**, chosen from 608 frames (stride 10)
- top-1 alternative frames: `[['47333319', '28534.151']]`

## Candidate counts (after NMS)

- `radiator dial` (target): **1**
- `window` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
