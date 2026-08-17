# q329_466880_57f1817c - visit 466880 / desc 57f1817c

## Instruction

> Open the second drawer of the counter to the right of the oven

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
   "name": "oven",
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
   "rel": "right_of",
   "a": "counter",
   "b": "oven"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "ordinal",
   "value": null,
   "index": 2,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `466880/47331707/11127.830`  (1920x1440)
- relaxation level **L2**, chosen from 179 frames (stride 10)
- top-6 alternative frames: `[['47331707', '11127.830'], ['47331711', '11259.727'], ['47331707', '11126.831'], ['47331707', '11125.831'], ['47331711', '11272.338'], ['47331711', '11263.742']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **4**
- `drawer` (host): **9**
- `counter` (container): **1**
- `oven` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
