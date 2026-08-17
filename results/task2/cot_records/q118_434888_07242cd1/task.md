# q118_434888_07242cd1 - visit 434888 / desc 07242cd1

## Instruction

> Open the bottom left drawer of the closet next to the door

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
   "name": "closet",
   "role": "container",
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
   "rel": "contains",
   "a": "closet",
   "b": "drawer"
  },
  {
   "rel": "next_to",
   "a": "closet",
   "b": "door"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "vertical",
   "value": "bottom",
   "index": null,
   "from": null
  },
  {
   "on": "drawer",
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

- `434888/42899185/184292.701`  (1440x1920)
- relaxation level **L0**, chosen from 105 frames (stride 10)
- top-1 alternative frames: `[['42899185', '184292.701']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **3**
- `drawer` (host): **4**
- `closet` (container): **1**
- `door` (landmark): **4**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
