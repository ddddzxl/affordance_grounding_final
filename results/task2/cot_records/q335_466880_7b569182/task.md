# q335_466880_7b569182 - visit 466880 / desc 7b569182

## Instruction

> Open the wooden door next to the telephone mounted on the wall

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
   "name": "telephone",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "door",
   "b": "telephone"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466880/47331707/11162.133`  (1920x1440)
- relaxation level **L2**, chosen from 179 frames (stride 10)
- top-1 alternative frames: `[['47331707', '11162.133']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `door` (host): **4**
- `telephone` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
