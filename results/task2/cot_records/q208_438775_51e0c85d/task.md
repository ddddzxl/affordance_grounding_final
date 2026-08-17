# q208_438775_51e0c85d - visit 438775 / desc 51e0c85d

## Instruction

> Open the white door next to the radiator

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "radiator",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "door",
   "b": "radiator"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `438775/44358170/62318.151`  (1920x1440)
- relaxation level **L0**, chosen from 266 frames (stride 10)
- top-8 alternative frames: `[['44358170', '62318.151'], ['44358170', '62317.152'], ['44358176', '62254.460'], ['44358176', '62255.459'], ['44358170', '62316.152'], ['44358176', '62278.450'], ['44358173', '62391.755'], ['44358176', '62272.453']]`

## Candidate counts (after NMS)

- `door handle` (target): **3**
- `door` (host): **1**
- `radiator` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
