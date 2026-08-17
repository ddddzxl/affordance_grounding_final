# q063_422842_4f6d1470 - visit 422842 / desc 4f6d1470

## Instruction

> Open the right door of the closet located next to the curtains

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
   "name": "curtains",
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
   "rel": "next_to",
   "a": "closet",
   "b": "curtains"
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

- `422842/42897547/473255.605`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-8 alternative frames: `[['42897547', '473255.605'], ['42897547', '473186.816'], ['42897547', '473215.904'], ['42897547', '473264.717'], ['42897547', '473254.605'], ['42897547', '473187.816'], ['42897547', '473179.819'], ['42897547', '473280.811']]`

## Candidate counts (after NMS)

- `door handle` (target): **12**
- `closet door` (host): **5**
- `closet` (container): **3**
- `curtains` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
