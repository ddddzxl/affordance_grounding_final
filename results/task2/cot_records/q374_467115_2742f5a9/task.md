# q374_467115_2742f5a9 - visit 467115 / desc 2742f5a9

## Instruction

> Open the counter drawer directly under the dish drainer

## Stage 0 parse

```json
{
 "target": {
  "concept": "drawer handle",
  "host": "drawer"
 },
 "entities": [
  {
   "name": "drawer handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "drawer",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "counter",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "dish drainer",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "counter",
   "b": "drawer"
  },
  {
   "rel": "under",
   "a": "drawer",
   "b": "dish drainer"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467115/47333319/28399.656`  (1440x1920)
- relaxation level **L1**, chosen from 608 frames (stride 10)
- top-1 alternative frames: `[['47333319', '28399.656']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **1**
- `drawer` (host): **2**
- `counter` (container): **1**
- `dish drainer` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
