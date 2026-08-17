# q089_423070_b7c287ec - visit 423070 / desc b7c287ec

## Instruction

> Close the window next to the toilet

## Stage 0 parse

```json
{
 "target": {
  "concept": "window handle",
  "host": "window"
 },
 "entities": [
  {
   "name": "window handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "window",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "toilet",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "window",
   "b": "toilet"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `423070/42447205/209303.077`  (1920x1440)
- relaxation level **L0**, chosen from 251 frames (stride 10)
- top-7 alternative frames: `[['42447205', '209303.077'], ['42447210', '209217.479'], ['42447210', '209222.477'], ['42447205', '209324.784'], ['42447205', '209316.788'], ['42447202', '209403.985'], ['42447205', '209312.789']]`

## Candidate counts (after NMS)

- `window handle` (target): **2**
- `window` (host): **1**
- `toilet` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
