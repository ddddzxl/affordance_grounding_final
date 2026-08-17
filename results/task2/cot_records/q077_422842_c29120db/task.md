# q077_422842_c29120db - visit 422842 / desc c29120db

## Instruction

> Open the right middle drawer of the dressing table

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
   "value": "middle",
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

- `422842/42897547/473258.703`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-5 alternative frames: `[['42897547', '473258.703'], ['42897547', '473254.605'], ['42897547', '473185.817'], ['42897547', '473186.816'], ['42897547', '473260.719']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **12**
- `drawer` (host): **10**
- `dressing table` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
