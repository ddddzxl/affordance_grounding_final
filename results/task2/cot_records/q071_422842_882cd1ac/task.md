# q071_422842_882cd1ac - visit 422842 / desc 882cd1ac

## Instruction

> Open the right door of the closet located to the right of the mirror

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
   "value": "right",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `422842/42897547/473149.815`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-3 alternative frames: `[['42897547', '473149.815'], ['42897547', '473254.605'], ['42897547', '473151.814']]`

## Candidate counts (after NMS)

- `door handle` (target): **6**
- `closet door` (host): **5**
- `closet` (container): **3**
- `mirror` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
