# q098_423452_24ced3e5 - visit 423452 / desc 24ced3e5

## Instruction

> Unplug the floor lamp next to the dining table

## Stage 0 parse

```json
{
 "target": {
  "concept": "plug",
  "host": null
 },
 "entities": [
  {
   "name": "plug",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "floor lamp",
   "role": "landmark",
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
   "rel": "near",
   "a": "plug",
   "b": "floor lamp"
  },
  {
   "rel": "next_to",
   "a": "floor lamp",
   "b": "dining table"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `423452/42897426/104088.641`  (1920x1440)
- relaxation level **L0**, chosen from 309 frames (stride 10)
- top-2 alternative frames: `[['42897426', '104088.641'], ['42897426', '104101.636']]`

## Candidate counts (after NMS)

- `plug` (target): **7**
- `floor lamp` (landmark): **3**
- `dining table` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
