# q086_423070_5e1f672d - visit 423070 / desc 5e1f672d

## Instruction

> Control the water flow in the bathtub using the drain control dial

## Stage 0 parse

```json
{
 "target": {
  "concept": "drain control dial",
  "host": "bathtub"
 },
 "entities": [
  {
   "name": "drain control dial",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "bathtub",
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

- `423070/42447210/209212.481`  (1920x1440)
- relaxation level **L0**, chosen from 251 frames (stride 10)
- top-7 alternative frames: `[['42447210', '209212.481'], ['42447202', '209397.988'], ['42447205', '209347.175'], ['42447202', '209392.873'], ['42447202', '209398.987'], ['42447202', '209383.294'], ['42447210', '209252.581']]`

## Candidate counts (after NMS)

- `drain control dial` (target): **2**
- `bathtub` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
