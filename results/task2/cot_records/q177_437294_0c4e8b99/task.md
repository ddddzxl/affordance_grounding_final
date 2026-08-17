# q177_437294_0c4e8b99 - visit 437294 / desc 0c4e8b99

## Instruction

> Open the top drawer of the nightstand to the right of the bed

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
   "name": "bed",
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
   "rel": "right_of",
   "a": "nightstand",
   "b": "bed"
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

- `437294/43649762/52525.856`  (1920x1440)
- relaxation level **L0**, chosen from 203 frames (stride 10)
- top-2 alternative frames: `[['43649762', '52525.856'], ['43649763', '52437.259']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **1**
- `drawer` (host): **3**
- `nightstand` (container): **1**
- `bed` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
