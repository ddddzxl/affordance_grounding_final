# q112_423957_7b17da95 - visit 423957 / desc 7b17da95

## Instruction

> Plug the device in the socket next to the nightstand

## Stage 0 parse

```json
{
 "target": {
  "concept": "socket",
  "host": null
 },
 "entities": [
  {
   "name": "socket",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "nightstand",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "socket",
   "b": "nightstand"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `423957/42898340/508423.314`  (1920x1440)
- relaxation level **L0**, chosen from 106 frames (stride 10)
- top-8 alternative frames: `[['42898340', '508423.314'], ['42898340', '508426.313'], ['42898340', '508424.313'], ['42898340', '508425.313'], ['42898340', '508427.312'], ['42898340', '508397.324'], ['42898343', '508299.415'], ['42898340', '508396.325']]`

## Candidate counts (after NMS)

- `socket` (target): **1**
- `nightstand` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
