# q190_437294_c5361095 - visit 437294 / desc c5361095

## Instruction

> Control the temperature using the dial under the window

## Stage 0 parse

```json
{
 "target": {
  "concept": "radiator knob",
  "host": null
 },
 "entities": [
  {
   "name": "radiator knob",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "window",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "under",
   "a": "radiator knob",
   "b": "window"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `437294/43649762/52525.856`  (1920x1440)
- relaxation level **L0**, chosen from 203 frames (stride 10)
- top-2 alternative frames: `[['43649762', '52525.856'], ['43649762', '52549.846']]`

## Candidate counts (after NMS)

- `radiator knob` (target): **2**
- `window` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
