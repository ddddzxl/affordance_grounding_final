# q155_435324_fde29153 - visit 435324 / desc fde29153

## Instruction

> Adjust the room's temperature using the radiator dial next to the bed

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
   "name": "bed",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "radiator knob",
   "b": "bed"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `435324/42899221/188372.200`  (1920x1440)
- relaxation level **L1**, chosen from 161 frames (stride 10)
- top-1 alternative frames: `[['42899221', '188372.200']]`

## Candidate counts (after NMS)

- `radiator knob` (target): **1**
- `bed` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
