# q397_467115_9004bfb6 - visit 467115 / desc 9004bfb6

## Instruction

> Adjust the stovetop's heat

## Stage 0 parse

```json
{
 "target": {
  "concept": "stovetop knob",
  "host": "stovetop"
 },
 "entities": [
  {
   "name": "stovetop knob",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "stovetop",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467115/47333310/28303.762`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-8 alternative frames: `[['47333310', '28303.762'], ['47333319', '28385.662'], ['47333308', '28037.154'], ['47333319', '28374.666'], ['47333308', '28033.156'], ['47333319', '28381.664'], ['47333310', '28301.763'], ['47333319', '28382.663']]`

## Candidate counts (after NMS)

- `stovetop knob` (target): **11**
- `stovetop` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
