# q156_435357_24aba0bb - visit 435357 / desc 24aba0bb

## Instruction

> Open the middle drawer of the TV stand

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
   "value": "middle",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `435357/42899624/230012.386`  (1440x1920)
- relaxation level **L0**, chosen from 191 frames (stride 10)
- top-6 alternative frames: `[['42899624', '230012.386'], ['42899624', '230086.590'], ['42899624', '230130.389'], ['42899624', '230128.390'], ['42899624', '230127.391'], ['42899624', '230129.390']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **4**
- `drawer` (host): **3**
- `TV stand` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
