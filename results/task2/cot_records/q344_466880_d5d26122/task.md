# q344_466880_d5d26122 - visit 466880 / desc d5d26122

## Instruction

> Open the right kitchen counter door with the sink on top

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "counter door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "counter door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "counter",
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
   "a": "counter",
   "b": "counter door"
  },
  {
   "rel": "has_on_top",
   "a": "counter",
   "b": "sink"
  }
 ],
 "select": [
  {
   "on": "counter door",
   "axis": "horizontal",
   "value": "right",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `466880/47331711/11307.840`  (1920x1440)
- relaxation level **L3**, chosen from 179 frames (stride 10)
- top-8 alternative frames: `[['47331711', '11307.840'], ['47331711', '11254.729'], ['47331711', '11252.729'], ['47331707', '11137.826'], ['47331710', '11215.228'], ['47331711', '11313.838'], ['47331711', '11248.731'], ['47331710', '11217.227']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `counter door` (host): **0**
- `counter` (container): **3**
- `sink` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
