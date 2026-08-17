# q137_434897_5c0ee8c5 - visit 434897 / desc 5c0ee8c5

## Instruction

> Close the bedroom door

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
  }
 ],
 "relations": [],
 "select": [],
 "residual": "'bedroom' is a room-level locator, not groundable"
}
```

## Selected frame

- `434897/42899163/182721.131`  (1440x1920)
- relaxation level **L0**, chosen from 94 frames (stride 10)
- top-8 alternative frames: `[['42899163', '182721.131'], ['42899163', '182723.147'], ['42899165', '182874.434'], ['42899165', '182868.137'], ['42899165', '182825.438'], ['42899165', '182853.543'], ['42899165', '182816.441'], ['42899163', '182724.146']]`

## Candidate counts (after NMS)

- `door handle` (target): **6**
- `door` (host): **5**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
