# q146_435324_7f4d658e - visit 435324 / desc 7f4d658e

## Instruction

> Open the bottom drawer of the wooden cabinet in the corner

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
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "cabinet",
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
 "residual": "'in the corner' is a room-level locator, not groundable"
}
```

## Selected frame

- `435324/42899221/188385.194`  (1920x1440)
- relaxation level **L0**, chosen from 161 frames (stride 10)
- top-8 alternative frames: `[['42899221', '188385.194'], ['42899216', '188221.295'], ['42899220', '188313.107'], ['42899216', '188245.002'], ['42899216', '188222.295'], ['42899221', '188369.201'], ['42899220', '188273.507'], ['42899220', '188315.107']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **1**
- `drawer` (host): **1**
- `cabinet` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
