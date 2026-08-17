# q031_421393_76c3cde8 - visit 421393 / desc 76c3cde8

## Instruction

> Open the right part of the window

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
  }
 ],
 "relations": [],
 "select": [
  {
   "on": "window",
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

- `421393/42444923/220879.063`  (1440x1920)
- relaxation level **L0**, chosen from 137 frames (stride 10)
- top-8 alternative frames: `[['42444923', '220879.063'], ['42444924', '220960.063'], ['42444923', '220881.062'], ['42444923', '220897.256'], ['42444924', '220959.064'], ['42444924', '220975.057'], ['42444923', '220901.254'], ['42444924', '220985.053']]`

## Candidate counts (after NMS)

- `window handle` (target): **6**
- `window` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
