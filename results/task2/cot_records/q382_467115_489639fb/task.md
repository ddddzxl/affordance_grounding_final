# q382_467115_489639fb - visit 467115 / desc 489639fb

## Instruction

> Control the temperature using the radiator dial next to the TV

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
   "name": "TV",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "radiator dial",
   "b": "TV"
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
- `TV` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
