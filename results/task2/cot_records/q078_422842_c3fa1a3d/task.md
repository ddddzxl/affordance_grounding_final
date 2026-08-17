# q078_422842_c3fa1a3d - visit 422842 / desc c3fa1a3d

## Instruction

> Open the left door of the closet located to the right of the mirror

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "closet door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "closet door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "closet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "mirror",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "closet",
   "b": "closet door"
  },
  {
   "rel": "right_of",
   "a": "closet",
   "b": "mirror"
  }
 ],
 "select": [
  {
   "on": "closet door",
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

- `422842/42897547/473180.819`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-7 alternative frames: `[['42897547', '473180.819'], ['42897547', '473271.715'], ['42897547', '473256.604'], ['42897547', '473254.605'], ['42897547', '473241.610'], ['42897547', '473273.714'], ['42897547', '473149.815']]`

## Candidate counts (after NMS)

- `door handle` (target): **11**
- `closet door` (host): **5**
- `closet` (container): **5**
- `mirror` (landmark): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
