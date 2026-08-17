# q213_438775_71d4f099 - visit 438775 / desc 71d4f099

## Instruction

> Open the drawer of the wooden table with the picture frame and lamp on top

## Stage 0 parse

```json
{
 "target": {
  "concept": "drawer handle",
  "host": "drawer"
 },
 "entities": [
  {
   "name": "drawer handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "drawer",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "table",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "picture frame",
   "role": "landmark",
   "instanceable": true
  },
  {
   "name": "lamp",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "table",
   "b": "drawer"
  },
  {
   "rel": "has_on_top",
   "a": "table",
   "b": "picture frame"
  },
  {
   "rel": "has_on_top",
   "a": "table",
   "b": "lamp"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `438775/44358173/62402.751`  (1920x1440)
- relaxation level **L0**, chosen from 266 frames (stride 10)
- top-1 alternative frames: `[['44358173', '62402.751']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **1**
- `drawer` (host): **1**
- `table` (container): **2**
- `picture frame` (landmark): **1**
- `lamp` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
