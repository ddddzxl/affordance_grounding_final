# q066_422842_77dcd360 - visit 422842 / desc 77dcd360

## Instruction

> Open the top right drawer of the white cabinet in front of the radiator

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
   "name": "cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "radiator",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "cabinet",
   "b": "drawer"
  },
  {
   "rel": "in_front_of",
   "a": "cabinet",
   "b": "radiator"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "vertical",
   "value": "top",
   "index": null,
   "from": null
  },
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

- `422842/42897547/473256.604`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-6 alternative frames: `[['42897547', '473256.604'], ['42897547', '473188.815'], ['42897547', '473181.818'], ['42897547', '473217.104'], ['42897560', '473393.614'], ['42897547', '473215.904']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **3**
- `drawer` (host): **1**
- `cabinet` (container): **3**
- `radiator` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
