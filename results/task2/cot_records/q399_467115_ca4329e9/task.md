# q399_467115_ca4329e9 - visit 467115 / desc ca4329e9

## Instruction

> Open the cabinet door above the sink

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
   "name": "sink",
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
   "b": "sink"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467115/47333308/28038.270`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-3 alternative frames: `[['47333308', '28038.270'], ['47333308', '28043.268'], ['47333319', '28396.657']]`

## Candidate counts (after NMS)

- `door handle` (target): **7**
- `cabinet door` (host): **4**
- `cabinet` (container): **4**
- `sink` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
