# q340_466880_a8e1ee54 - visit 466880 / desc a8e1ee54

## Instruction

> Open the left glass cabinet door above the coffee machine

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
   "value": "left",
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
- top-2 alternative frames: `[['47331711', '11318.836'], ['47331711', '11319.835']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `cabinet door` (host): **7**
- `cabinet` (container): **5**
- `coffee machine` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
