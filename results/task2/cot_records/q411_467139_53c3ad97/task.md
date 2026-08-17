# q411_467139_53c3ad97 - visit 467139 / desc 53c3ad97

## Instruction

> Open the left door of the sink cabinet

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
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `467139/47333293/26463.248`  (1920x1440)
- relaxation level **L0**, chosen from 366 frames (stride 10)
- top-8 alternative frames: `[['47333293', '26463.248'], ['47333298', '26574.453'], ['47333298', '26596.943'], ['47333293', '26476.060'], ['47333293', '26478.059'], ['47333292', '26417.351'], ['47333292', '26411.353'], ['47333293', '26479.059']]`

## Candidate counts (after NMS)

- `door handle` (target): **3**
- `cabinet door` (host): **3**
- `sink cabinet` (container): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
