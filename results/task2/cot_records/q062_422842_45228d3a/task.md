# q062_422842_45228d3a - visit 422842 / desc 45228d3a

## Instruction

> Open the bottom drawer of the nightstand with the books on top

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
   "name": "nightstand",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "books",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "nightstand",
   "b": "drawer"
  },
  {
   "rel": "has_on_top",
   "a": "nightstand",
   "b": "books"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "vertical",
   "value": "bottom",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `422842/42897547/473169.806`  (1440x1920)
- relaxation level **L1**, chosen from 236 frames (stride 10)
- top-4 alternative frames: `[['42897547', '473169.806'], ['42897560', '473472.715'], ['42897547', '473168.807'], ['42897547', '473204.909']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **3**
- `drawer` (host): **2**
- `nightstand` (container): **1**
- `books` (landmark): **4**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
