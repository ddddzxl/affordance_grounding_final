# q057_422842_09409a8f - visit 422842 / desc 09409a8f

## Instruction

> Open the right door of the closet next to the radiator

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
   "name": "radiator",
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
   "b": "radiator"
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
- top-8 alternative frames: `[['42897547', '473255.605'], ['42897547', '473186.816'], ['42897547', '473180.819'], ['42897547', '473215.904'], ['42897547', '473217.104'], ['42897547', '473264.717'], ['42897547', '473254.605'], ['42897547', '473179.819']]`

## Candidate counts (after NMS)

- `door handle` (target): **12**
- `closet door` (host): **5**
- `closet` (container): **3**
- `radiator` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
