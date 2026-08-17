# q035_421393_d481bb45 - visit 421393 / desc d481bb45

## Instruction

> Open the second drawer of the nightstand

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
   "name": "nightstand",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "nightstand",
   "b": "drawer"
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

- `421393/42444923/220905.152`  (1440x1920)
- relaxation level **L0**, chosen from 137 frames (stride 10)
- top-1 alternative frames: `[['42444923', '220905.152']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **6**
- `drawer` (host): **4**
- `nightstand` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
