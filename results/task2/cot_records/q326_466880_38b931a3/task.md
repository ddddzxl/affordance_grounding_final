# q326_466880_38b931a3 - visit 466880 / desc 38b931a3

## Instruction

> Open the second drawer of the counter to the left of the oven

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

- `466880/47331707/11125.831`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-1 alternative frames: `[['47331707', '11125.831']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **8**
- `drawer` (host): **11**
- `counter` (container): **4**
- `oven` (landmark): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
