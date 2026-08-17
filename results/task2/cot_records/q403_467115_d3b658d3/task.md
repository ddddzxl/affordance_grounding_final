# q403_467115_d3b658d3 - visit 467115 / desc d3b658d3

## Instruction

> Open the cabinet door above the dish dryer

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
   "name": "dish dryer",
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
   "b": "dish dryer"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467115/47333308/28043.268`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-8 alternative frames: `[['47333308', '28043.268'], ['47333308', '28030.157'], ['47333310', '28306.761'], ['47333308', '28059.861'], ['47333310', '28241.654'], ['47333319', '28373.667'], ['47333308', '28029.157'], ['47333319', '28407.653']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `cabinet door` (host): **5**
- `cabinet` (container): **5**
- `dish dryer` (landmark): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
