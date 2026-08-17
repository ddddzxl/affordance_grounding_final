# q115_423957_cc2257dd - visit 423957 / desc cc2257dd

## Instruction

> Open the top window above the nightstand

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
   "name": "nightstand",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "above",
   "a": "window",
   "b": "nightstand"
  }
 ],
 "select": [
  {
   "on": "window",
   "axis": "vertical",
   "value": "top",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `423957/42898343/508297.415`  (1920x1440)
- relaxation level **L0**, chosen from 106 frames (stride 10)
- top-7 alternative frames: `[['42898343', '508297.415'], ['42898340', '508448.820'], ['42898340', '508425.313'], ['42898343', '508305.412'], ['42898343', '508299.415'], ['42898340', '508424.313'], ['42898340', '508423.314']]`

## Candidate counts (after NMS)

- `window handle` (target): **4**
- `window` (host): **3**
- `nightstand` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
