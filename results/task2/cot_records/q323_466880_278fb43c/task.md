# q323_466880_278fb43c - visit 466880 / desc 278fb43c

## Instruction

> Open the cabinet door directly above and to the left of the oven

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
   "name": "oven",
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
   "b": "oven"
  },
  {
   "rel": "left_of",
   "a": "cabinet door",
   "b": "oven"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466880/47331707/11127.830`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-3 alternative frames: `[['47331707', '11127.830'], ['47331710', '11229.239'], ['47331711', '11260.726']]`

## Candidate counts (after NMS)

- `door handle` (target): **7**
- `cabinet door` (host): **11**
- `cabinet` (container): **2**
- `oven` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
