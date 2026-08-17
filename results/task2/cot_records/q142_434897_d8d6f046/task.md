# q142_434897_d8d6f046 - visit 434897 / desc d8d6f046

## Instruction

> Open the top right drawer of the wooden closet

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
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "closet",
   "b": "drawer"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "vertical",
   "value": "top",
   "index": null,
   "from": null
  },
  {
   "on": "drawer",
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

- `434897/42899165/182809.544`  (1440x1920)
- relaxation level **L0**, chosen from 94 frames (stride 10)
- top-8 alternative frames: `[['42899165', '182809.544'], ['42899165', '182868.137'], ['42899163', '182718.132'], ['42899163', '182683.746'], ['42899165', '182817.441'], ['42899163', '182687.745'], ['42899165', '182808.545'], ['42899163', '182682.747']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **5**
- `drawer` (host): **3**
- `closet` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
