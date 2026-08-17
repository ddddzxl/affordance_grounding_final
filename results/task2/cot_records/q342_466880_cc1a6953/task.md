# q342_466880_cc1a6953 - visit 466880 / desc cc1a6953

## Instruction

> Plug the device in one of the sockets behind the bread bin

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
   "name": "bread bin",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "behind",
   "a": "socket",
   "b": "bread bin"
  }
 ],
 "select": [],
 "residual": "'one of the sockets' — any instance satisfying the relation is acceptable"
}
```

## Selected frame

- `466880/47331711/11257.727`  (1920x1440)
- relaxation level **L1**, chosen from 179 frames (stride 10)
- top-1 alternative frames: `[['47331711', '11257.727']]`

## Candidate counts (after NMS)

- `socket` (target): **2**
- `bread bin` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
