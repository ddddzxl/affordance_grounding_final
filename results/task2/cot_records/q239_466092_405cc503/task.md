# q239_466092_405cc503 - visit 466092 / desc 405cc503

## Instruction

> Open the left cabinet door with the TV on top

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
   "name": "TV",
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
   "b": "TV"
  }
 ],
 "select": [
  {
   "on": "cabinet door",
   "axis": "horizontal",
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `466092/44796562/15985.396`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-8 alternative frames: `[['44796562', '15985.396'], ['44796568', '16181.198'], ['44796562', '15986.395'], ['44796562', '16001.406'], ['44796568', '16176.200'], ['44796562', '15961.406'], ['44796562', '15950.294'], ['44796562', '15951.293']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `cabinet door` (host): **3**
- `cabinet` (container): **2**
- `TV` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
