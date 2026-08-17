# q058_422842_167174e2 - visit 422842 / desc 167174e2

## Instruction

> Open the top drawer of the nightstand to the left of the bed

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
   "name": "bed",
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
   "rel": "left_of",
   "a": "nightstand",
   "b": "bed"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "vertical",
   "value": "top",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `422842/42897547/473203.909`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-1 alternative frames: `[['42897547', '473203.909']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **7**
- `drawer` (host): **2**
- `nightstand` (container): **2**
- `bed` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
