# q232_455342_b98f04ed - visit 455342 / desc b98f04ed

## Instruction

> Plug the device in the left socket behind the armchair

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
   "name": "armchair",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "behind",
   "a": "socket",
   "b": "armchair"
  }
 ],
 "select": [
  {
   "on": "socket",
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

- `455342/44358471/46591.298`  (1920x1440)
- relaxation level **L0**, chosen from 97 frames (stride 10)
- top-3 alternative frames: `[['44358471', '46591.298'], ['44358471', '46589.299'], ['44358471', '46590.299']]`

## Candidate counts (after NMS)

- `socket` (target): **2**
- `armchair` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
