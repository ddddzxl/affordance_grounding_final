# q415_467139_eeb550dc - visit 467139 / desc eeb550dc

## Instruction

> Control the temperature using the bathroom radiator dial

## Stage 0 parse

```json
{
 "target": {
  "concept": "radiator knob",
  "host": "radiator"
 },
 "entities": [
  {
   "name": "radiator knob",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "radiator",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": "'bathroom' is a room-level locator, not groundable"
}
```

## Selected frame

- `467139/47333298/26596.943`  (1920x1440)
- relaxation level **L0**, chosen from 366 frames (stride 10)
- top-8 alternative frames: `[['47333298', '26596.943'], ['47333298', '26597.943'], ['47333298', '26622.249'], ['47333293', '26492.053'], ['47333292', '26406.355'], ['47333298', '26618.251'], ['47333293', '26488.055'], ['47333292', '26398.358']]`

## Candidate counts (after NMS)

- `radiator knob` (target): **2**
- `radiator` (host): **0**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
