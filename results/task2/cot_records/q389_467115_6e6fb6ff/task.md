# q389_467115_6e6fb6ff - visit 467115 / desc 6e6fb6ff

## Instruction

> Open the cabinet door above the teacups

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
   "name": "teacups",
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
   "b": "teacups"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467115/47333310/28294.766`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-3 alternative frames: `[['47333310', '28294.766'], ['47333319', '28396.657'], ['47333319', '28362.655']]`

## Candidate counts (after NMS)

- `door handle` (target): **1**
- `cabinet door` (host): **3**
- `cabinet` (container): **4**
- `teacups` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
