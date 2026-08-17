# q041_421657_80f7ad39 - visit 421657 / desc 80f7ad39

## Instruction

> Open the top drawer of the nightstand next to the closet

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
   "value": "top",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `421657/42445642/58279.688`  (1920x1440)
- relaxation level **L0**, chosen from 165 frames (stride 10)
- top-2 alternative frames: `[['42445642', '58279.688'], ['42445639', '58300.996']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **6**
- `drawer` (host): **3**
- `nightstand` (container): **1**
- `closet` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
