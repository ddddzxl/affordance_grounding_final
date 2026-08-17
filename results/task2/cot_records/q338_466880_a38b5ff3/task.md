# q338_466880_a38b5ff3 - visit 466880 / desc a38b5ff3

## Instruction

> Open the right glass cabinet door above the coffee machine

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
   "name": "coffee machine",
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
   "rel": "above",
   "a": "cabinet door",
   "b": "coffee machine"
  }
 ],
 "select": [
  {
   "on": "cabinet door",
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

- `466880/47331711/11318.836`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-4 alternative frames: `[['47331711', '11318.836'], ['47331711', '11319.835'], ['47331710', '11229.239'], ['47331710', '11228.239']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `cabinet door` (host): **7**
- `cabinet` (container): **5**
- `coffee machine` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
