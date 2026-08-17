# q424_468282_3eaac799 - visit 468282 / desc 3eaac799

## Instruction

> Open the left cabinet door above the washing machine

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "cabinet door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "cabinet door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "washing machine",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "cabinet",
   "b": "cabinet door"
  },
  {
   "rel": "above",
   "a": "cabinet door",
   "b": "washing machine"
  }
 ],
 "select": [
  {
   "on": "cabinet door",
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

- `468282/47331279/14316.318`  (1440x1920)
- relaxation level **L1**, chosen from 215 frames (stride 10)
- top-1 alternative frames: `[['47331279', '14316.318']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `cabinet door` (host): **2**
- `cabinet` (container): **3**
- `washing machine` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
