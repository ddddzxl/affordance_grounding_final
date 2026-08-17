# q279_466437_1bca5d90 - visit 466437 / desc 1bca5d90

## Instruction

> Open the bottom drawer of the wooden nightstand with the books on top

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
   "name": "books",
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
   "rel": "has_on_top",
   "a": "nightstand",
   "b": "books"
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

- `466437/45260952/6047.108`  (1440x1920)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-8 alternative frames: `[['45260952', '6047.108'], ['45260951', '6183.321'], ['45260951', '6186.319'], ['45260951', '6184.320'], ['45260951', '6182.321'], ['45260951', '6187.319'], ['45260952', '6048.107'], ['45260951', '6178.106']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **3**
- `drawer` (host): **5**
- `nightstand` (container): **1**
- `books` (landmark): **7**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
