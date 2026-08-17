# q082_422842_def5de81 - visit 422842 / desc def5de81

## Instruction

> Open the top right drawer of the dressing table

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

- `422842/42897560/473431.815`  (1440x1920)
- relaxation level **L0**, chosen from 236 frames (stride 10)
- top-8 alternative frames: `[['42897560', '473431.815'], ['42897547', '473233.614'], ['42897547', '473186.816'], ['42897547', '473229.615'], ['42897547', '473255.605'], ['42897547', '473258.703'], ['42897547', '473260.719'], ['42897547', '473257.604']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **4**
- `drawer` (host): **7**
- `dressing table` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
