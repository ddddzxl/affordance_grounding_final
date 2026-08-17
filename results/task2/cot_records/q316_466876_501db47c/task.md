# q316_466876_501db47c - visit 466876 / desc 501db47c

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

- `466876/47331560/9902.644`  (1440x1920)
- relaxation level **L0**, chosen from 160 frames (stride 10)
- top-8 alternative frames: `[['47331560', '9902.644'], ['47331558', '9834.954'], ['47331560', '9901.644'], ['47331561', '9781.143'], ['47331560', '9897.646'], ['47331561', '9782.142'], ['47331560', '9898.645'], ['47331558', '9835.954']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `cabinet door` (host): **2**
- `sink cabinet` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
