# q161_435357_8582201f - visit 435357 / desc 8582201f

## Instruction

> Unplug the space heater under the window

## Stage 0 parse

```json
{
 "target": {
  "concept": "plug",
  "host": "space heater"
 },
 "entities": [
  {
   "name": "plug",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "space heater",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "window",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "under",
   "a": "space heater",
   "b": "window"
  }
 ],
 "select": [],
 "residual": "the plug sits at the socket end, not on the heater"
}
```

## Selected frame

- `435357/42899624/230016.385`  (1440x1920)
- relaxation level **L0**, chosen from 191 frames (stride 10)
- top-1 alternative frames: `[['42899624', '230016.385']]`

## Candidate counts (after NMS)

- `plug` (target): **1**
- `space heater` (host): **0**
- `window` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
