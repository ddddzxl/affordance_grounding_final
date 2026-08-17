# q105_423957_0cc63848 - visit 423957 / desc 0cc63848

## Instruction

> Open the bottom drawer of the nightstand

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
   "name": "nightstand",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "nightstand",
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
  }
 ],
 "residual": null
}
```

## Selected frame

- `423957/42898340/508427.312`  (1920x1440)
- relaxation level **L0**, chosen from 106 frames (stride 10)
- top-8 alternative frames: `[['42898340', '508427.312'], ['42898340', '508423.314'], ['42898340', '508428.312'], ['42898340', '508424.313'], ['42898343', '508305.412'], ['42898340', '508396.325'], ['42898340', '508397.324'], ['42898340', '508422.314']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **2**
- `drawer` (host): **2**
- `nightstand` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
