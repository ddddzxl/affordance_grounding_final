# q162_435357_ae4a0b1c - visit 435357 / desc ae4a0b1c

## Instruction

> Close the door next to the blue couch

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
   "name": "couch",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "door",
   "b": "couch"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `435357/42899632/229993.177`  (1440x1920)
- relaxation level **L0**, chosen from 191 frames (stride 10)
- top-8 alternative frames: `[['42899632', '229993.177'], ['42899630', '229881.688'], ['42899632', '229954.892'], ['42899624', '230008.388'], ['42899632', '229953.793'], ['42899624', '230094.287'], ['42899630', '229937.283'], ['42899630', '229884.687']]`

## Candidate counts (after NMS)

- `door handle` (target): **1**
- `door` (host): **2**
- `couch` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
