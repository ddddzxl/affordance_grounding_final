# q136_434897_3f2efafa - visit 434897 / desc 3f2efafa

## Instruction

> Open the window to the left of the mirror

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
   "name": "mirror",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "left_of",
   "a": "window",
   "b": "mirror"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `434897/42899163/182686.745`  (1440x1920)
- relaxation level **L0**, chosen from 94 frames (stride 10)
- top-8 alternative frames: `[['42899163', '182686.745'], ['42899163', '182687.745'], ['42899163', '182683.746'], ['42899163', '182682.747'], ['42899163', '182684.746'], ['42899163', '182688.744'], ['42899165', '182812.443'], ['42899163', '182703.738']]`

## Candidate counts (after NMS)

- `window handle` (target): **14**
- `window` (host): **1**
- `mirror` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
