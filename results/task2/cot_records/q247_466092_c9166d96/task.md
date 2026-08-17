# q247_466092_c9166d96 - visit 466092 / desc c9166d96

## Instruction

> Turn on the lamp on the table to the left of the red couch

## Stage 0 parse

```json
{
 "target": {
  "concept": "light switch",
  "host": "lamp"
 },
 "entities": [
  {
   "name": "light switch",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "lamp",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "table",
   "role": "container",
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
   "rel": "on_top",
   "a": "lamp",
   "b": "table"
  },
  {
   "rel": "left_of",
   "a": "table",
   "b": "couch"
  }
 ],
 "select": [],
 "residual": "unified with val8's 'light switch'; which lamp it is, is carried by `host`, not by the search term"
}
```

## Selected frame

- `466092/44796562/15962.405`  (1920x1440)
- relaxation level **L2**, chosen from 179 frames (stride 10)
- top-1 alternative frames: `[['44796562', '15962.405']]`

## Candidate counts (after NMS)

- `light switch` (target): **4**
- `lamp` (host): **3**
- `table` (container): **3**
- `couch` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
