# q413_467139_90693ddd - visit 467139 / desc 90693ddd

## Instruction

> Open the right door of the sink cabinet

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
   "name": "sink cabinet",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "sink cabinet",
   "b": "cabinet door"
  }
 ],
 "select": [
  {
   "on": "cabinet door",
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

- `467139/47333292/26410.354`  (1920x1440)
- relaxation level **L0**, chosen from 366 frames (stride 10)
- top-8 alternative frames: `[['47333292', '26410.354'], ['47333293', '26476.060'], ['47333298', '26596.943'], ['47333293', '26478.059'], ['47333292', '26417.351'], ['47333293', '26481.058'], ['47333292', '26411.353'], ['47333293', '26479.059']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `cabinet door` (host): **2**
- `sink cabinet` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
