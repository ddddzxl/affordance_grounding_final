# q359_466916_b2802405 - visit 466916 / desc b2802405

## Instruction

> Turn on the table lamp next to the printer

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
   "name": "printer",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "table lamp",
   "b": "printer"
  }
 ],
 "select": [],
 "residual": "unified with val8's 'light switch'; which lamp it is, is carried by `host`, not by the search term"
}
```

## Selected frame

- `466916/47331617/18145.591`  (1920x1440)
- relaxation level **L0**, chosen from 306 frames (stride 10)
- top-1 alternative frames: `[['47331617', '18145.591']]`

## Candidate counts (after NMS)

- `light switch` (target): **1**
- `table lamp` (host): **1**
- `printer` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
