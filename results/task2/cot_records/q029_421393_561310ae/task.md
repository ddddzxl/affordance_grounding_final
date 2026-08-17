# q029_421393_561310ae - visit 421393 / desc 561310ae

## Instruction

> Turn on the ceiling light using the switch next to the door

## Stage 0 parse

```json
{
 "target": {
  "concept": "light switch",
  "host": null
 },
 "entities": [
  {
   "name": "light switch",
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
   "a": "light switch",
   "b": "door"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `421393/42444923/220941.254`  (1440x1920)
- relaxation level **L0**, chosen from 137 frames (stride 10)
- top-8 alternative frames: `[['42444923', '220941.254'], ['42444924', '220961.063'], ['42444924', '220959.064'], ['42444924', '220962.063'], ['42444923', '220939.255'], ['42444923', '220885.960'], ['42444923', '220879.063'], ['42444924', '220960.063']]`

## Candidate counts (after NMS)

- `light switch` (target): **3**
- `door` (landmark): **6**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
