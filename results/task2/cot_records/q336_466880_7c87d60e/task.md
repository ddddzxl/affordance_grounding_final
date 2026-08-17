# q336_466880_7c87d60e - visit 466880 / desc 7c87d60e

## Instruction

> Open the bottom drawer of the counter to the right of the oven

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
   "axis": "vertical",
   "value": "bottom",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `466880/47331707/11127.830`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-2 alternative frames: `[['47331707', '11127.830'], ['47331707', '11126.831']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **4**
- `drawer` (host): **9**
- `counter` (container): **1**
- `oven` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
