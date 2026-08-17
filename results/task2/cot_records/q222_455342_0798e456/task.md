# q222_455342_0798e456 - visit 455342 / desc 0798e456

## Instruction

> Unplug the table lamp to the right of the couch

## Stage 0 parse

```json
{
 "target": {
  "concept": "plug",
  "host": "table lamp"
 },
 "entities": [
  {
   "name": "plug",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "table lamp",
   "role": "host",
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
   "rel": "right_of",
   "a": "table lamp",
   "b": "couch"
  }
 ],
 "select": [],
 "residual": "the plug sits at the socket end, not on the lamp"
}
```

## Selected frame

- `455342/44358472/46645.093`  (1920x1440)
- relaxation level **L0**, chosen from 97 frames (stride 10)
- top-4 alternative frames: `[['44358472', '46645.093'], ['44358471', '46570.990'], ['44358471', '46572.989'], ['44358472', '46616.088']]`

## Candidate counts (after NMS)

- `plug` (target): **3**
- `table lamp` (host): **1**
- `couch` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
