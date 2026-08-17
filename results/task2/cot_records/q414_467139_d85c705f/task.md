# q414_467139_d85c705f - visit 467139 / desc d85c705f

## Instruction

> Turn on the bathroom light

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
 "residual": "'bathroom' is a room-level locator, not groundable"
}
```

## Selected frame

- `467139/47333298/26683.957`  (1920x1440)
- relaxation level **L0**, chosen from 366 frames (stride 10)
- top-8 alternative frames: `[['47333298', '26683.957'], ['47333298', '26658.651'], ['47333293', '26526.056'], ['47333298', '26681.642'], ['47333293', '26533.053'], ['47333293', '26459.250'], ['47333293', '26507.047'], ['47333292', '26370.953']]`

## Candidate counts (after NMS)

- `light switch` (target): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
