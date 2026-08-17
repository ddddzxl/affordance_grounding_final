# q175_437157_f5c001bd - visit 437157 / desc f5c001bd

## Instruction

> Open the top drawer of the closet next to the nightstand

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
   "name": "closet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "nightstand",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "closet",
   "b": "drawer"
  },
  {
   "rel": "next_to",
   "a": "closet",
   "b": "nightstand"
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

- `437157/43649688/36012.073`  (1440x1920)
- relaxation level **L0**, chosen from 239 frames (stride 10)
- top-2 alternative frames: `[['43649688', '36012.073'], ['43649692', '36068.468']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **3**
- `drawer` (host): **2**
- `closet` (container): **1**
- `nightstand` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
