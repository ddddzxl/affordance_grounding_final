# q207_438775_333a0512 - visit 438775 / desc 333a0512

## Instruction

> Control the room's temperature using the radiator dial next to the potted plant

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
   "name": "potted plant",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "radiator knob",
   "b": "potted plant"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `438775/44358170/62317.152`  (1920x1440)
- relaxation level **L0**, chosen from 266 frames (stride 10)
- top-5 alternative frames: `[['44358170', '62317.152'], ['44358173', '62391.755'], ['44358170', '62318.151'], ['44358173', '62392.755'], ['44358170', '62337.560']]`

## Candidate counts (after NMS)

- `radiator knob` (target): **1**
- `potted plant` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
