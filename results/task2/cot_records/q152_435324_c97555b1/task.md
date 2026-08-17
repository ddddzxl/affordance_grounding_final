# q152_435324_c97555b1 - visit 435324 / desc c97555b1

## Instruction

> Plug the device in the socket next to the cabinet

## Stage 0 parse

```json
{
 "target": {
  "concept": "socket",
  "host": null
 },
 "entities": [
  {
   "name": "socket",
   "role": "target",
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
   "rel": "next_to",
   "a": "socket",
   "b": "cabinet"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `435324/42899221/188392.208`  (1920x1440)
- relaxation level **L0**, chosen from 161 frames (stride 10)
- top-3 alternative frames: `[['42899221', '188392.208'], ['42899221', '188391.208'], ['42899221', '188350.009']]`

## Candidate counts (after NMS)

- `socket` (target): **1**
- `cabinet` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
