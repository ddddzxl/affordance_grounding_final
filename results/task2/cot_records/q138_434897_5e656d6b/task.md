# q138_434897_5e656d6b - visit 434897 / desc 5e656d6b

## Instruction

> Open the top left drawer of the wooden closet

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
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `434897/42899163/182721.131`  (1440x1920)
- relaxation level **L0**, chosen from 94 frames (stride 10)
- top-5 alternative frames: `[['42899163', '182721.131'], ['42899165', '182808.545'], ['42899165', '182874.434'], ['42899165', '182809.544'], ['42899163', '182681.730']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **7**
- `drawer` (host): **4**
- `closet` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
