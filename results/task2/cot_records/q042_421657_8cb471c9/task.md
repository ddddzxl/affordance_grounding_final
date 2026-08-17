# q042_421657_8cb471c9 - visit 421657 / desc 8cb471c9

## Instruction

> Plug the device in the socket next to the door

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
   "name": "door",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "socket",
   "b": "door"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `421657/42445639/58314.291`  (1920x1440)
- relaxation level **L0**, chosen from 165 frames (stride 10)
- top-4 alternative frames: `[['42445639', '58314.291'], ['42445642', '58249.484'], ['42445633', '58090.300'], ['42445633', '58121.487']]`

## Candidate counts (after NMS)

- `socket` (target): **3**
- `door` (landmark): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
