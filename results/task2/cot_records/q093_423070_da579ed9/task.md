# q093_423070_da579ed9 - visit 423070 / desc da579ed9

## Instruction

> Open the right door of the wood and glass display cabinet next to the pet transport box

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
   "name": "display cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "pet transport box",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "display cabinet",
   "b": "cabinet door"
  },
  {
   "rel": "next_to",
   "a": "display cabinet",
   "b": "pet transport box"
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
 "residual": "'wood and glass' material - ignored"
}
```

## Selected frame

- `423070/42447210/209236.587`  (1920x1440)
- relaxation level **POOL-T**, chosen from 251 frames (stride 10)
- top-7 alternative frames: `[['42447210', '209236.587'], ['42447202', '209406.984'], ['42447205', '209286.883'], ['42447205', '209284.884'], ['42447202', '209427.675'], ['42447205', '209315.788'], ['42447202', '209428.675']]`

## Candidate counts (after NMS)

- `door handle` (target): **3**
- `cabinet door` (host): **3**
- `display cabinet` (container): **1**
- `pet transport box` (landmark): **0**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
