# q069_422842_830a03a0 - visit 422842 / desc 830a03a0

## Instruction

> Open the right door of the closet located to the left of the mirror

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
   "rel": "left_of",
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

- `422842/42897547/473186.816`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-4 alternative frames: `[['42897547', '473186.816'], ['42897547', '473239.611'], ['42897547', '473254.605'], ['42897547', '473280.811']]`

## Candidate counts (after NMS)

- `door handle` (target): **10**
- `closet door` (host): **3**
- `closet` (container): **2**
- `mirror` (landmark): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
