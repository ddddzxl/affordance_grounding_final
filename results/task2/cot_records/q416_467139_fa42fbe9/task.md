# q416_467139_fa42fbe9 - visit 467139 / desc fa42fbe9

## Instruction

> Open the window above the bathtub

## Stage 0 parse

```json
{
 "target": {
  "concept": "handle",
  "host": "window"
 },
 "entities": [
  {
   "name": "handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "window",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "bathtub",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "above",
   "a": "window",
   "b": "bathtub"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467139/47333298/26568.455`  (1920x1440)
- relaxation level **L0**, chosen from 366 frames (stride 10)
- top-6 alternative frames: `[['47333298', '26568.455'], ['47333298', '26567.455'], ['47333293', '26455.252'], ['47333298', '26566.456'], ['47333292', '26439.358'], ['47333292', '26347.146']]`

## Candidate counts (after NMS)

- `handle` (target): **3**
- `window` (host): **1**
- `bathtub` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
