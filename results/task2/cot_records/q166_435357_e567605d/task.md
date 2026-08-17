# q166_435357_e567605d - visit 435357 / desc e567605d

## Instruction

> Open the right drawer of the TV stand

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
   "name": "TV stand",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "TV stand",
   "b": "drawer"
  }
 ],
 "select": [
  {
   "on": "drawer",
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

- `435357/42899630/229935.283`  (1440x1920)
- relaxation level **L0**, chosen from 191 frames (stride 10)
- top-8 alternative frames: `[['42899630', '229935.283'], ['42899624', '230012.386'], ['42899624', '230013.386'], ['42899624', '230086.590'], ['42899624', '230130.389'], ['42899624', '230128.390'], ['42899624', '230132.389'], ['42899624', '230127.391']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **1**
- `drawer` (host): **2**
- `TV stand` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
