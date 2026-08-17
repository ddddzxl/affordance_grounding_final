# q261_466162_34a155cd - visit 466162 / desc 34a155cd

## Instruction

> Plug the device in one of the sockets next to the fireplace

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
   "name": "fireplace",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "socket",
   "b": "fireplace"
  }
 ],
 "select": [],
 "residual": "'one of the sockets' — any instance satisfying the relation is acceptable"
}
```

## Selected frame

- `466162/44796576/16713.287`  (1920x1440)
- relaxation level **L0**, chosen from 257 frames (stride 10)
- top-8 alternative frames: `[['44796576', '16713.287'], ['44796576', '16737.694'], ['44796575', '16951.489'], ['44796579', '16780.593'], ['44796576', '16712.288'], ['44796579', '16779.593'], ['44796579', '16778.593'], ['44796579', '16781.592']]`

## Candidate counts (after NMS)

- `socket` (target): **1**
- `fireplace` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
