# q287_466437_9c1810fb - visit 466437 / desc 9c1810fb

## Instruction

> Open the nightstand door with the tablet on top

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "nightstand door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "nightstand door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "nightstand",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "tablet",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "nightstand",
   "b": "nightstand door"
  },
  {
   "rel": "has_on_top",
   "a": "nightstand",
   "b": "tablet"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466437/45260951/6170.109`  (1440x1920)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-4 alternative frames: `[['45260951', '6170.109'], ['45260951', '6171.109'], ['45260951', '6173.108'], ['45260951', '6172.108']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `nightstand door` (host): **1**
- `nightstand` (container): **1**
- `tablet` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
