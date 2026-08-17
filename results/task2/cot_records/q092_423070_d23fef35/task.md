# q092_423070_d23fef35 - visit 423070 / desc d23fef35

## Instruction

> Close the door located directly next to the vacuum cleaner

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "vacuum cleaner",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "door",
   "b": "vacuum cleaner"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `423070/42447210/209189.690`  (1920x1440)
- relaxation level **L0**, chosen from 251 frames (stride 10)
- top-5 alternative frames: `[['42447210', '209189.690'], ['42447202', '209445.185'], ['42447202', '209449.183'], ['42447202', '209452.182'], ['42447205', '209292.881']]`

## Candidate counts (after NMS)

- `door handle` (target): **1**
- `door` (host): **3**
- `vacuum cleaner` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
