# q206_438775_321eea14 - visit 438775 / desc 321eea14

## Instruction

> Plug the device in the socket to the left of the leather couch

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
   "name": "couch",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "left_of",
   "a": "socket",
   "b": "couch"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `438775/44358176/62249.945`  (1920x1440)
- relaxation level **L0**, chosen from 266 frames (stride 10)
- top-7 alternative frames: `[['44358176', '62249.945'], ['44358170', '62311.154'], ['44358170', '62357.352'], ['44358173', '62387.757'], ['44358170', '62369.348'], ['44358176', '62241.448'], ['44358173', '62385.758']]`

## Candidate counts (after NMS)

- `socket` (target): **3**
- `couch` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
