# q143_434897_e9b99bb3 - visit 434897 / desc e9b99bb3

## Instruction

> Open the second drawer of the wooden closet

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

- `434897/42899165/182817.441`  (1440x1920)
- relaxation level **L2**, chosen from 94 frames (stride 10)
- top-8 alternative frames: `[['42899165', '182817.441'], ['42899165', '182850.544'], ['42899163', '182724.146'], ['42899163', '182725.146'], ['42899163', '182723.147'], ['42899165', '182807.545'], ['42899163', '182719.132'], ['42899165', '182867.137']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **5**
- `drawer` (host): **2**
- `closet` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
