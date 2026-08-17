# q169_437157_0e6999a8 - visit 437157 / desc 0e6999a8

## Instruction

> Open the window next to the chair

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
   "name": "chair",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "window",
   "b": "chair"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `437157/43649686/36110.268`  (1440x1920)
- relaxation level **L0**, chosen from 239 frames (stride 10)
- top-8 alternative frames: `[['43649686', '36110.268'], ['43649686', '36111.267'], ['43649692', '36047.476'], ['43649686', '36241.266'], ['43649686', '36116.565'], ['43649686', '36115.566'], ['43649688', '35986.067'], ['43649688', '35987.067']]`

## Candidate counts (after NMS)

- `window handle` (target): **2**
- `window` (host): **2**
- `chair` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
