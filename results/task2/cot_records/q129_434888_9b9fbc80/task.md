# q129_434888_9b9fbc80 - visit 434888 / desc 9b9fbc80

## Instruction

> Plug the device in the socket next to the chair

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
   "name": "chair",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "socket",
   "b": "chair"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `434888/42899185/184291.602`  (1440x1920)
- relaxation level **L0**, chosen from 105 frames (stride 10)
- top-7 alternative frames: `[['42899185', '184291.602'], ['42899187', '184399.907'], ['42899185', '184290.602'], ['42899187', '184382.614'], ['42899184', '184458.299'], ['42899184', '184460.315'], ['42899184', '184457.299']]`

## Candidate counts (after NMS)

- `socket` (target): **1**
- `chair` (landmark): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
