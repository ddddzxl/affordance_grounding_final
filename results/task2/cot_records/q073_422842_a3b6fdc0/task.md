# q073_422842_a3b6fdc0 - visit 422842 / desc a3b6fdc0

## Instruction

> Open the bottom left drawer of the dressing table

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
   "name": "dressing table",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "dressing table",
   "b": "drawer"
  }
 ],
 "select": [
  {
   "on": "drawer",
   "axis": "vertical",
   "value": "bottom",
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

- `422842/42897547/473234.613`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-4 alternative frames: `[['42897547', '473234.613'], ['42897547', '473186.816'], ['42897547', '473260.719'], ['42897547', '473185.817']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **8**
- `drawer` (host): **8**
- `dressing table` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
