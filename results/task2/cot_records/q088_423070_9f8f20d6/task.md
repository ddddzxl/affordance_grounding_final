# q088_423070_9f8f20d6 - visit 423070 / desc 9f8f20d6

## Instruction

> Open the trash bin below the sink

## Stage 0 parse

```json
{
 "target": {
  "concept": "pedal",
  "host": "trash bin"
 },
 "entities": [
  {
   "name": "pedal",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "trash bin",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "sink",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "under",
   "a": "trash bin",
   "b": "sink"
  }
 ],
 "select": [],
 "residual": "train: 'open the trash bin' is foot_push in 12/14 annotations — household bins are pedal-operated. 'lid' came from a generic open->pull inference that does not hold for this object class."
}
```

## Selected frame

- `423070/42447202/209424.676`  (1920x1440)
- relaxation level **L1**, chosen from 251 frames (stride 10)
- top-1 alternative frames: `[['42447202', '209424.676']]`

## Candidate counts (after NMS)

- `pedal` (target): **1**
- `trash bin` (host): **2**
- `sink` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
