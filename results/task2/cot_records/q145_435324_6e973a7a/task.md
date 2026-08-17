# q145_435324_6e973a7a - visit 435324 / desc 6e973a7a

## Instruction

> Open the bottom closet drawer between the door and the cabinet

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
   "name": "closet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "landmark",
   "instanceable": true
  },
  {
   "name": "cabinet",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "closet",
   "b": "drawer"
  },
  {
   "rel": "between",
   "a": "closet",
   "b": "door"
  },
  {
   "rel": "between",
   "a": "closet",
   "b": "cabinet"
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

- `435324/42899220/188313.107`  (1920x1440)
- relaxation level **L0**, chosen from 161 frames (stride 10)
- top-8 alternative frames: `[['42899220', '188313.107'], ['42899216', '188221.295'], ['42899220', '188271.508'], ['42899221', '188350.009'], ['42899216', '188222.295'], ['42899216', '188245.002'], ['42899220', '188272.508'], ['42899220', '188314.107']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **13**
- `drawer` (host): **5**
- `closet` (container): **2**
- `door` (landmark): **3**
- `cabinet` (landmark): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
