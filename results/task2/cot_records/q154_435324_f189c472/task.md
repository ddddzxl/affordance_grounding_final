# q154_435324_f189c472 - visit 435324 / desc f189c472

## Instruction

> Open the top left window part between the two beds

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
   "name": "bed",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "between",
   "a": "window",
   "b": "bed"
  }
 ],
 "select": [
  {
   "on": "window",
   "axis": "vertical",
   "value": "top",
   "index": null,
   "from": null
  },
  {
   "on": "window",
   "axis": "horizontal",
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": "'between the two beds' — both anchors are the same concept 'bed', so the relation cannot separate them"
}
```

## Selected frame

- `435324/42899216/188204.302`  (1920x1440)
- relaxation level **L0**, chosen from 161 frames (stride 10)
- top-8 alternative frames: `[['42899216', '188204.302'], ['42899220', '188280.504'], ['42899220', '188284.503'], ['42899220', '188258.497'], ['42899216', '188201.304'], ['42899220', '188259.496'], ['42899221', '188409.201'], ['42899220', '188285.502']]`

## Candidate counts (after NMS)

- `window handle` (target): **7**
- `window` (host): **1**
- `bed` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
