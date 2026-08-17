# q325_466880_386d2681 - visit 466880 / desc 386d2681

## Instruction

> Control the temperature using the radiator dial next to the window

## Stage 0 parse

```json
{
 "target": {
  "concept": "dial",
  "host": null
 },
 "entities": [
  {
   "name": "dial",
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
   "rel": "next_to",
   "a": "dial",
   "b": "window"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466880/47331711/11278.935`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-1 alternative frames: `[['47331711', '11278.935']]`

## Candidate counts (after NMS)

- `dial` (target): **3**
- `window` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
