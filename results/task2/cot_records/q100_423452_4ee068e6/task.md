# q100_423452_4ee068e6 - visit 423452 / desc 4ee068e6

## Instruction

> Plug the device in the socket next to the dining table

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
   "name": "dining table",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "socket",
   "b": "dining table"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `423452/42897426/104151.548`  (1920x1440)
- relaxation level **L0**, chosen from 309 frames (stride 10)
- top-8 alternative frames: `[['42897426', '104151.548'], ['42897422', '104038.146'], ['42897434', '104214.139'], ['42897434', '104213.139'], ['42897426', '104147.833'], ['42897426', '104097.638'], ['42897422', '104039.145'], ['42897422', '104045.143']]`

## Candidate counts (after NMS)

- `socket` (target): **4**
- `dining table` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
