# q147_435324_822f3aca - visit 435324 / desc 822f3aca

## Instruction

> Open the top drawer of the wooden cabinet in the corner

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
   "value": "top",
   "index": null,
   "from": null
  }
 ],
 "residual": "'in the corner' is a room-level locator, not groundable"
}
```

## Selected frame

- `435324/42899220/188313.107`  (1920x1440)
- relaxation level **L0**, chosen from 161 frames (stride 10)
- top-8 alternative frames: `[['42899220', '188313.107'], ['42899216', '188224.411'], ['42899221', '188391.208'], ['42899216', '188225.410'], ['42899221', '188392.208'], ['42899221', '188348.993'], ['42899216', '188220.296'], ['42899216', '188223.411']]`

## Candidate counts (after NMS)

- `drawer handle` (target): **13**
- `drawer` (host): **5**
- `cabinet` (container): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
