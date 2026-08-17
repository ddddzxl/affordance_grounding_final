# q292_466437_cd6ad92a - visit 466437 / desc cd6ad92a

## Instruction

> Open the window next to the closet

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
   "name": "closet",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "window",
   "b": "closet"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466437/45260951/6121.312`  (1440x1920)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-7 alternative frames: `[['45260951', '6121.312'], ['45260957', '5940.117'], ['45260952', '6004.908'], ['45260952', '6005.907'], ['45260957', '5936.018'], ['45260951', '6139.121'], ['45260951', '6138.122']]`

## Candidate counts (after NMS)

- `window handle` (target): **8**
- `window` (host): **1**
- `closet` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
