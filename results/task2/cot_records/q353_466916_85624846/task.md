# q353_466916_85624846 - visit 466916 / desc 85624846

## Instruction

> Open the left door of the wooden cabinet located directly under the shelf with the picture frames

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
   "name": "shelf",
   "role": "landmark",
   "instanceable": true
  },
  {
   "name": "picture frames",
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
   "rel": "under",
   "a": "cabinet",
   "b": "shelf"
  },
  {
   "rel": "has_on_top",
   "a": "shelf",
   "b": "picture frames"
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

- `466916/47331615/18099.094`  (1920x1440)
- relaxation level **POOL-T**, chosen from 306 frames (stride 10)
- top-8 alternative frames: `[['47331615', '18099.094'], ['47331615', '18096.095'], ['47331617', '18153.705'], ['47331615', '18100.093'], ['47331617', '18135.595'], ['47331618', '17971.196'], ['47331617', '18149.590'], ['47331617', '18141.593']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `cabinet door` (host): **11**
- `cabinet` (container): **7**
- `shelf` (landmark): **9**
- `picture frames` (landmark): **0**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
