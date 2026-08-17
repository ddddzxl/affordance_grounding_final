# q126_434888_72b1df3a - visit 434888 / desc 72b1df3a

## Instruction

> Open the window to the left of the vanity table

## Stage 0 parse

```json
{
 "target": {
  "concept": "window handle",
  "host": "window"
 },
 "entities": [
  {
   "name": "window handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "window",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "vanity table",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "left_of",
   "a": "window",
   "b": "vanity table"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `434888/42899185/184290.602`  (1440x1920)
- relaxation level **L0**, chosen from 105 frames (stride 10)
- top-8 alternative frames: `[['42899185', '184290.602'], ['42899185', '184281.606'], ['42899184', '184437.808'], ['42899184', '184455.300'], ['42899184', '184438.807'], ['42899184', '184456.300'], ['42899185', '184291.602'], ['42899187', '184382.614']]`

## Candidate counts (after NMS)

- `window handle` (target): **3**
- `window` (host): **1**
- `vanity table` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
