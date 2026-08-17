# q123_434888_40d4f283 - visit 434888 / desc 40d4f283

## Instruction

> Turn on the lamp on the nightstand to the right of the bed

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
   "name": "nightstand",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "bed",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "lamp",
   "b": "nightstand"
  },
  {
   "rel": "right_of",
   "a": "nightstand",
   "b": "bed"
  }
 ],
 "select": [],
 "residual": "unified with val8's 'light switch'; which lamp it is, is carried by `host`, not by the search term"
}
```

## Selected frame

- `434888/42899185/184280.606`  (1440x1920)
- relaxation level **L0**, chosen from 105 frames (stride 10)
- top-1 alternative frames: `[['42899185', '184280.606']]`

## Candidate counts (after NMS)

- `light switch` (target): **2**
- `lamp` (host): **1**
- `nightstand` (container): **4**
- `bed` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
