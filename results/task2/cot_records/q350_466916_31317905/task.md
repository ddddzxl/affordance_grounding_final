# q350_466916_31317905 - visit 466916 / desc 31317905

## Instruction

> Open the right door of the wooden display cabinet to the left of the paintings

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
   "name": "display cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "paintings",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "display cabinet",
   "b": "cabinet door"
  },
  {
   "rel": "left_of",
   "a": "display cabinet",
   "b": "paintings"
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

- `466916/47331617/18140.593`  (1920x1440)
- relaxation level **L0**, chosen from 306 frames (stride 10)
- top-3 alternative frames: `[['47331617', '18140.593'], ['47331617', '18141.593'], ['47331615', '18104.092']]`

## Candidate counts (after NMS)

- `door handle` (target): **1**
- `cabinet door` (host): **9**
- `display cabinet` (container): **4**
- `paintings` (landmark): **7**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
