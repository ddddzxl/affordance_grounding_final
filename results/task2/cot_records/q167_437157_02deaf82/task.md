# q167_437157_02deaf82 - visit 437157 / desc 02deaf82

## Instruction

> Open the bottom drawer of the closet next to the nightstand

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
   "value": "bottom",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `437157/43649688/36008.075`  (1440x1920)
- relaxation level **L0**, chosen from 239 frames (stride 10)
- top-7 alternative frames: `[['43649688', '36008.075'], ['43649692', '36069.467'], ['43649686', '36212.278'], ['43649686', '36150.569'], ['43649692', '36070.467'], ['43649688', '36009.075'], ['43649688', '36010.074']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **5**
- `drawer` (host): **6**
- `closet` (container): **2**
- `nightstand` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
