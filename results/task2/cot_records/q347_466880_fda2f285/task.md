# q347_466880_fda2f285 - visit 466880 / desc fda2f285

## Instruction

> Open the top drawer of the counter to the left of the oven

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
   "rel": "left_of",
   "a": "counter",
   "b": "oven"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "vertical",
   "value": "top",
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
- top-6 alternative frames: `[['47331707', '11127.830'], ['47331707', '11125.831'], ['47331707', '11132.828'], ['47331711', '11260.726'], ['47331710', '11179.626'], ['47331710', '11181.642']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **4**
- `drawer` (host): **9**
- `counter` (container): **1**
- `oven` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
