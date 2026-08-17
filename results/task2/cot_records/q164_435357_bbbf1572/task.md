# q164_435357_bbbf1572 - visit 435357 / desc bbbf1572

## Instruction

> Open the left drawer of the TV stand

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
   "name": "TV stand",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "TV stand",
   "b": "drawer"
  }
 ],
 "select": [
  {
   "on": "drawer",
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

- `435357/42899624/230071.479`  (1440x1920)
- relaxation level **L0**, chosen from 191 frames (stride 10)
- top-8 alternative frames: `[['42899624', '230071.479'], ['42899630', '229933.284'], ['42899632', '229969.886'], ['42899624', '230073.479'], ['42899624', '230072.479'], ['42899630', '229908.677'], ['42899624', '230069.480'], ['42899624', '230070.480']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **1**
- `drawer` (host): **2**
- `TV stand` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
