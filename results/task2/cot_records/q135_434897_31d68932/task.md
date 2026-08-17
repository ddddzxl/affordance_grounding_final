# q135_434897_31d68932 - visit 434897 / desc 31d68932

## Instruction

> Open the bottom drawer of the wooden closet

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
   "value": "bottom",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `434897/42899165/182850.544`  (1440x1920)
- relaxation level **L0**, chosen from 94 frames (stride 10)
- top-8 alternative frames: `[['42899165', '182850.544'], ['42899165', '182807.545'], ['42899163', '182724.146'], ['42899163', '182723.147'], ['42899163', '182719.132'], ['42899165', '182867.137'], ['42899163', '182718.132'], ['42899163', '182684.746']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **2**
- `drawer` (host): **2**
- `closet` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
