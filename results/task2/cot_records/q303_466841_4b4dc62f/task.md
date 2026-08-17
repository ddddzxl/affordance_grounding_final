# q303_466841_4b4dc62f - visit 466841 / desc 4b4dc62f

## Instruction

> Open the cabinet door behind the bird cage located next to the bed

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
   "name": "bed",
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
   "rel": "behind",
   "a": "cabinet door",
   "b": "bird cage"
  },
  {
   "rel": "next_to",
   "a": "bird cage",
   "b": "bed"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466841/47331589/15948.997`  (1920x1440)
- relaxation level **L1**, chosen from 135 frames (stride 10)
- top-2 alternative frames: `[['47331589', '15948.997'], ['47331587', '16003.208']]`

## Candidate counts (after NMS)

- `door handle` (target): **1**
- `cabinet door` (host): **4**
- `cabinet` (container): **2**
- `bird cage` (landmark): **1**
- `bed` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
