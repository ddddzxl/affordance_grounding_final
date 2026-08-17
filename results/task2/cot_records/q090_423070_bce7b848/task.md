# q090_423070_bce7b848 - visit 423070 / desc bce7b848

## Instruction

> Open the door behind the pet transport box

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
   "name": "pet transport box",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "behind",
   "a": "door",
   "b": "pet transport box"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `423070/42447205/209312.789`  (1920x1440)
- relaxation level **L0**, chosen from 251 frames (stride 10)
- top-2 alternative frames: `[['42447205', '209312.789'], ['42447210', '209190.690']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `door` (host): **5**
- `pet transport box` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
