# q110_423957_718a57d9 - visit 423957 / desc 718a57d9

## Instruction

> Plug the device in the right socket next to the bed

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
   "name": "bed",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "socket",
   "b": "bed"
  }
 ],
 "select": [
  {
   "on": "socket",
   "axis": "horizontal",
   "value": "right",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `423957/42898343/508292.418`  (1920x1440)
- relaxation level **L0**, chosen from 106 frames (stride 10)
- top-2 alternative frames: `[['42898343', '508292.418'], ['42898340', '508450.819']]`

## Candidate counts (after NMS)

- `socket` (target): **1**
- `bed` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
