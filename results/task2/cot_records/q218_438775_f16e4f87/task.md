# q218_438775_f16e4f87 - visit 438775 / desc f16e4f87

## Instruction

> Lock the white door next to the radiator

## Stage 0 parse

```json
{
 "target": {
  "concept": "door lock",
  "host": "door"
 },
 "entities": [
  {
   "name": "door lock",
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
 "residual": "train: 'lock' is a rotate affordance disjoint from the handle (274/274 pairs in train share 0 annotation)"
}
```

## Selected frame

- `438775/44358170/62318.151`  (1920x1440)
- relaxation level **L0**, chosen from 266 frames (stride 10)
- top-8 alternative frames: `[['44358170', '62318.151'], ['44358170', '62317.152'], ['44358176', '62254.460'], ['44358176', '62255.459'], ['44358170', '62316.152'], ['44358176', '62278.450'], ['44358173', '62391.755'], ['44358176', '62272.453']]`

## Candidate counts (after NMS)

- `door lock` (target): **2**
- `door` (host): **1**
- `radiator` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
