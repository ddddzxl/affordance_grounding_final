# q114_423957_aff7d288 - visit 423957 / desc aff7d288

## Instruction

> Open the bottom window above the radiator

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
   "name": "radiator",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "above",
   "a": "window",
   "b": "radiator"
  }
 ],
 "select": [
  {
   "on": "window",
   "axis": "vertical",
   "value": "bottom",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `423957/42898343/508273.525`  (1920x1440)
- relaxation level **L0**, chosen from 106 frames (stride 10)
- top-8 alternative frames: `[['42898343', '508273.525'], ['42898343', '508318.823'], ['42898340', '508436.825'], ['42898340', '508401.323'], ['42898343', '508278.523'], ['42898343', '508319.823'], ['42898343', '508303.413'], ['42898340', '508402.322']]`

## Candidate counts (after NMS)

- `window handle` (target): **4**
- `window` (host): **3**
- `radiator` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
