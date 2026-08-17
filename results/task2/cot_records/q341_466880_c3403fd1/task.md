# q341_466880_c3403fd1 - visit 466880 / desc c3403fd1

## Instruction

> Open the bread bin next to the water bottles

## Stage 0 parse

```json
{
 "target": {
  "concept": "bread bin lid",
  "host": "bread bin"
 },
 "entities": [
  {
   "name": "bread bin lid",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "bread bin",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "water bottles",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "bread bin",
   "b": "water bottles"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466880/47331707/11132.828`  (1920x1440)
- relaxation level **L1**, chosen from 179 frames (stride 10)
- top-2 alternative frames: `[['47331707', '11132.828'], ['47331707', '11143.540']]`

## Candidate counts (after NMS)

- `bread bin lid` (target): **3**
- `bread bin` (host): **0**
- `water bottles` (landmark): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
