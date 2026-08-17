# q439_468476_728de1bf - visit 468476 / desc 728de1bf

## Instruction

> Open the middle window behind the blue armchair

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
   "name": "armchair",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "behind",
   "a": "window",
   "b": "armchair"
  }
 ],
 "select": [
  {
   "on": "window",
   "axis": "horizontal",
   "value": "middle",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `468476/45261682/3533.476`  (1440x1920)
- relaxation level **L0**, chosen from 222 frames (stride 10)
- top-8 alternative frames: `[['45261682', '3533.476'], ['45261682', '3532.476'], ['45261686', '3756.267'], ['45261681', '3600.065'], ['45261681', '3599.065'], ['45261681', '3598.066'], ['45261681', '3597.066'], ['45261682', '3528.478']]`

## Candidate counts (after NMS)

- `window handle` (target): **4**
- `window` (host): **4**
- `armchair` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
