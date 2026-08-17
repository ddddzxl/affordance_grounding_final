# q380_467115_4768a52c - visit 467115 / desc 4768a52c

## Instruction

> Turn on the kitchen light

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
  }
 ],
 "relations": [],
 "select": [],
 "residual": "'kitchen' is a room-level locator, not groundable"
}
```

## Selected frame

- `467115/47333310/28318.756`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-8 alternative frames: `[['47333310', '28318.756'], ['47333310', '28317.756'], ['47333310', '28322.754'], ['47333310', '28324.753'], ['47333310', '28325.753'], ['47333319', '28351.659'], ['47333319', '28352.659'], ['47333310', '28282.754']]`

## Candidate counts (after NMS)

- `light switch` (target): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
