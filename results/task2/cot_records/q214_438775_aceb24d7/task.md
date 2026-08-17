# q214_438775_aceb24d7 - visit 438775 / desc aceb24d7

## Instruction

> Open the top left window next to the window doors

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
   "name": "window door",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "window",
   "b": "window door"
  }
 ],
 "select": [
  {
   "on": "window",
   "axis": "vertical",
   "value": "top",
   "index": null,
   "from": null
  },
  {
   "on": "window",
   "axis": "horizontal",
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `438775/44358170/62369.348`  (1920x1440)
- relaxation level **L0**, chosen from 266 frames (stride 10)
- top-8 alternative frames: `[['44358170', '62369.348'], ['44358173', '62388.756'], ['44358170', '62328.147'], ['44358176', '62261.457'], ['44358170', '62327.148'], ['44358176', '62244.447'], ['44358173', '62525.252'], ['44358173', '62527.252']]`

## Candidate counts (after NMS)

- `window handle` (target): **6**
- `window` (host): **1**
- `window door` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
