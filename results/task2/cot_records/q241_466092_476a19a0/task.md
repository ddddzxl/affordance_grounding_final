# q241_466092_476a19a0 - visit 466092 / desc 476a19a0

## Instruction

> Open the right cabinet door with the picture frames on top

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "cabinet door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "cabinet door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "picture frames",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "cabinet",
   "b": "cabinet door"
  },
  {
   "rel": "has_on_top",
   "a": "cabinet",
   "b": "picture frames"
  }
 ],
 "select": [
  {
   "on": "cabinet door",
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

- `466092/44796568/16169.203`  (1920x1440)
- relaxation level **POOL-T**, chosen from 179 frames (stride 10)
- top-8 alternative frames: `[['44796568', '16169.203'], ['44796568', '16167.204'], ['44796568', '16168.203'], ['44796568', '16181.198'], ['44796562', '16001.406'], ['44796568', '16117.991'], ['44796568', '16170.202'], ['44796568', '16166.204']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `cabinet door` (host): **3**
- `cabinet` (container): **2**
- `picture frames` (landmark): **0**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
