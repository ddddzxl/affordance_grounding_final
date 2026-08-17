# q037_421657_035527b5 - visit 421657 / desc 035527b5

## Instruction

> Open the bottom drawer of the nightstand next to the closet

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
  },
  {
   "name": "closet",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "nightstand",
   "b": "drawer"
  },
  {
   "rel": "next_to",
   "a": "nightstand",
   "b": "closet"
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

- `421657/42445639/58352.092`  (1920x1440)
- relaxation level **L0**, chosen from 165 frames (stride 10)
- top-5 alternative frames: `[['42445639', '58352.092'], ['42445642', '58236.490'], ['42445633', '58091.300'], ['42445642', '58279.688'], ['42445639', '58300.996']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **2**
- `drawer` (host): **2**
- `nightstand` (container): **1**
- `closet` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
