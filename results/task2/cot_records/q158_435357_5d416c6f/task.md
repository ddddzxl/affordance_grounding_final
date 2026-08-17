# q158_435357_5d416c6f - visit 435357 / desc 5d416c6f

## Instruction

> Turn on the lamp on the side table next to the Christmas tree

## Stage 0 parse

```json
{
 "target": {
  "concept": "light button",
  "host": "lamp"
 },
 "entities": [
  {
   "name": "light button",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "lamp",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "side table",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "Christmas tree",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "lamp",
   "b": "side table"
  },
  {
   "rel": "next_to",
   "a": "side table",
   "b": "Christmas tree"
  }
 ],
 "select": [],
 "residual": "unified with val8's 'light switch'; which lamp it is, is carried by `host`, not by the search term"
}
```

## Selected frame

- `435357/42899624/230107.282`  (1440x1920)
- relaxation level **POOL-T**, chosen from 191 frames (stride 10)
- top-2 alternative frames: `[['42899624', '230107.282'], ['42899624', '230109.281']]`

## Candidate counts (after NMS)

- `light button` (target): **6**
- `lamp` (host): **0**
- `side table` (container): **1**
- `Christmas tree` (landmark): **0**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
