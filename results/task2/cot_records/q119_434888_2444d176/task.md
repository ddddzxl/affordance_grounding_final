# q119_434888_2444d176 - visit 434888 / desc 2444d176

## Instruction

> Open the drawer of the white vanity table

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
   "name": "vanity table",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "vanity table",
   "b": "drawer"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `434888/42899184/184459.299`  (1440x1920)
- relaxation level **L0**, chosen from 105 frames (stride 10)
- top-8 alternative frames: `[['42899184', '184459.299'], ['42899184', '184455.300'], ['42899187', '184383.613'], ['42899184', '184442.805'], ['42899184', '184461.314'], ['42899185', '184318.307'], ['42899187', '184381.614'], ['42899184', '184477.908']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **2**
- `drawer` (host): **1**
- `vanity table` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
