# q101_423452_78fb6192 - visit 423452 / desc 78fb6192

## Instruction

> Adjust the intensity of the floor lamp light next to the dining table

## Stage 0 parse

```json
{
 "target": {
  "concept": "dimmer switch",
  "host": "floor lamp"
 },
 "entities": [
  {
   "name": "dimmer switch",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "floor lamp",
   "role": "host",
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
   "a": "floor lamp",
   "b": "dining table"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `423452/42897434/104193.148`  (1920x1440)
- relaxation level **L1**, chosen from 309 frames (stride 10)
- top-2 alternative frames: `[['42897434', '104193.148'], ['42897426', '104144.735']]`

## Candidate counts (after NMS)

- `dimmer switch` (target): **3**
- `floor lamp` (host): **2**
- `dining table` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
