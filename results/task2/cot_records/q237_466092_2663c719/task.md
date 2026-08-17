# q237_466092_2663c719 - visit 466092 / desc 2663c719

## Instruction

> Turn on the table lamp on the desk

## Stage 0 parse

```json
{
 "target": {
  "concept": "light switch",
  "host": "table lamp"
 },
 "entities": [
  {
   "name": "light switch",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "table lamp",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "desk",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "table lamp",
   "b": "desk"
  }
 ],
 "select": [],
 "residual": "unified with val8's 'light switch'; which lamp it is, is carried by `host`, not by the search term"
}
```

## Selected frame

- `466092/44796568/16109.994`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-2 alternative frames: `[['44796568', '16109.994'], ['44796568', '16141.198']]`

## Candidate counts (after NMS)

- `light switch` (target): **1**
- `table lamp` (host): **0**
- `desk` (container): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
