# q153_435324_df6ae11d - visit 435324 / desc df6ae11d

## Instruction

> Close the bedroom door

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
  }
 ],
 "relations": [],
 "select": [],
 "residual": "'bedroom' is a room-level locator, not groundable"
}
```

## Selected frame

- `435324/42899216/188223.411`  (1920x1440)
- relaxation level **L0**, chosen from 161 frames (stride 10)
- top-8 alternative frames: `[['42899216', '188223.411'], ['42899220', '188313.107'], ['42899216', '188220.296'], ['42899221', '188344.994'], ['42899216', '188238.605'], ['42899220', '188272.508'], ['42899221', '188350.009'], ['42899221', '188348.993']]`

## Candidate counts (after NMS)

- `door handle` (target): **9**
- `door` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
