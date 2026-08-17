# q356_466916_937d51c1 - visit 466916 / desc 937d51c1

## Instruction

> Open the left door of the wooden cabinet located directly to the right of the doorway

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "cabinet door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "cabinet door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "doorway",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "cabinet",
   "b": "cabinet door"
  },
  {
   "rel": "right_of",
   "a": "cabinet",
   "b": "doorway"
  }
 ],
 "select": [
  {
   "on": "cabinet door",
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

- `466916/47331615/18108.090`  (1920x1440)
- relaxation level **L0**, chosen from 306 frames (stride 10)
- top-1 alternative frames: `[['47331615', '18108.090']]`

## Candidate counts (after NMS)

- `door handle` (target): **3**
- `cabinet door` (host): **5**
- `cabinet` (container): **5**
- `doorway` (landmark): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
