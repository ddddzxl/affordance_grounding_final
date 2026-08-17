# q310_466841_a2dd9263 - visit 466841 / desc a2dd9263

## Instruction

> Open the left cabinet door with the bird cage and the toys on top

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
   "name": "bird cage",
   "role": "landmark",
   "instanceable": true
  },
  {
   "name": "toys",
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
   "rel": "has_on_top",
   "a": "cabinet",
   "b": "bird cage"
  },
  {
   "rel": "has_on_top",
   "a": "cabinet",
   "b": "toys"
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

- `466841/47331587/15986.198`  (1920x1440)
- relaxation level **L1**, chosen from 135 frames (stride 10)
- top-2 alternative frames: `[['47331587', '15986.198'], ['47331589', '15931.004']]`

## Candidate counts (after NMS)

- `door handle` (target): **1**
- `cabinet door` (host): **3**
- `cabinet` (container): **5**
- `bird cage` (landmark): **1**
- `toys` (landmark): **18**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
