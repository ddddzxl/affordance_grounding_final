# q210_438775_59fb2537 - visit 438775 / desc 59fb2537

## Instruction

> Turn on the lamp on the side table next to the telephone

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
   "name": "side table",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "telephone",
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
   "b": "telephone"
  }
 ],
 "select": [],
 "residual": "unified with val8's 'light switch'; which lamp it is, is carried by `host`, not by the search term"
}
```

## Selected frame

- `438775/44358173/62503.161`  (1920x1440)
- relaxation level **POOL-T**, chosen from 266 frames (stride 10)
- top-8 alternative frames: `[['44358173', '62503.161'], ['44358173', '62495.947'], ['44358173', '62408.749'], ['44358173', '62500.146'], ['44358173', '62494.948'], ['44358173', '62504.161'], ['44358173', '62501.162'], ['44358173', '62493.948']]`

## Candidate counts (after NMS)

- `light switch` (target): **1**
- `lamp` (host): **0**
- `side table` (container): **2**
- `telephone` (landmark): **0**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
