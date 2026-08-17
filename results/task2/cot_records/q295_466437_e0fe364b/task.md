# q295_466437_e0fe364b - visit 466437 / desc e0fe364b

## Instruction

> Open the window next to the nightstand

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
   "name": "nightstand",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "window",
   "b": "nightstand"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466437/45260957/5981.517`  (1440x1920)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-8 alternative frames: `[['45260957', '5981.517'], ['45260952', '6033.113'], ['45260951', '6164.111'], ['45260951', '6163.112'], ['45260952', '6032.114'], ['45260951', '6162.112'], ['45260951', '6159.113'], ['45260957', '5965.107']]`

## Candidate counts (after NMS)

- `window handle` (target): **4**
- `window` (host): **2**
- `nightstand` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
