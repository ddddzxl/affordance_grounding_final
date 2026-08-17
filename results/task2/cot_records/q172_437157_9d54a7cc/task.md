# q172_437157_9d54a7cc - visit 437157 / desc 9d54a7cc

## Instruction

> Turn on the ceiling light using the switch near the blue coats

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
   "name": "coats",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "near",
   "a": "light switch",
   "b": "coats"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `437157/43649692/36061.471`  (1440x1920)
- relaxation level **L0**, chosen from 239 frames (stride 10)
- top-4 alternative frames: `[['43649692', '36061.471'], ['43649686', '36127.578'], ['43649692', '36060.471'], ['43649686', '36126.578']]`

## Candidate counts (after NMS)

- `light switch` (target): **5**
- `coats` (landmark): **4**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
