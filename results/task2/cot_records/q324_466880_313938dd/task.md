# q324_466880_313938dd - visit 466880 / desc 313938dd

## Instruction

> Open the oven door

## Stage 0 parse

```json
{
 "target": {
  "concept": "oven handle",
  "host": "oven"
 },
 "entities": [
  {
   "name": "oven handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "oven",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466880/47331707/11119.534`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-8 alternative frames: `[['47331707', '11119.534'], ['47331707', '11115.035'], ['47331707', '11145.540'], ['47331711', '11260.726'], ['47331710', '11179.626'], ['47331707', '11125.831'], ['47331707', '11126.831'], ['47331710', '11181.642']]`

## Candidate counts (after NMS)

- `oven handle` (target): **2**
- `oven` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
