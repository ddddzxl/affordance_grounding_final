# q067_422842_78fe7d26 - visit 422842 / desc 78fe7d26

## Instruction

> Open the top left drawer of the white cabinet in front of the radiator

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
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `422842/42897547/473181.818`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-8 alternative frames: `[['42897547', '473181.818'], ['42897547', '473186.816'], ['42897547', '473256.604'], ['42897560', '473386.917'], ['42897560', '473393.614'], ['42897547', '473187.816'], ['42897547', '473188.815'], ['42897547', '473189.815']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **8**
- `drawer` (host): **7**
- `cabinet` (container): **6**
- `radiator` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
