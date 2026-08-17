# q106_423957_29c8a6ab - visit 423957 / desc 29c8a6ab

## Instruction

> Plug the device in the left socket next to the door

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
   "name": "door",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "socket",
   "b": "door"
  }
 ],
 "select": [
  {
   "on": "socket",
   "axis": "horizontal",
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `423957/42898343/508277.524`  (1920x1440)
- relaxation level **L0**, chosen from 106 frames (stride 10)
- top-4 alternative frames: `[['42898343', '508277.524'], ['42898340', '508450.819'], ['42898343', '508321.822'], ['42898343', '508276.524']]`

## Candidate counts (after NMS)

- `socket` (target): **1**
- `door` (landmark): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
