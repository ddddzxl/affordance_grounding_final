# q179_437294_2f45cfc1 - visit 437294 / desc 2f45cfc1

## Instruction

> Open the left chest on the vanity table

## Stage 0 parse

```json
{
 "target": {
  "concept": "chest knob",
  "host": "chest"
 },
 "entities": [
  {
   "name": "chest knob",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "chest",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "vanity table",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "chest",
   "b": "vanity table"
  }
 ],
 "select": [
  {
   "on": "chest",
   "axis": "horizontal",
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": "'chest' is a small box standing on the table; the interactable part is its lid/latch"
}
```

## Selected frame

- `437294/43649762/52528.854`  (1920x1440)
- relaxation level **L0**, chosen from 203 frames (stride 10)
- top-8 alternative frames: `[['43649762', '52528.854'], ['43649762', '52529.854'], ['43649762', '52500.150'], ['43649762', '52501.149'], ['43649762', '52530.853'], ['43649762', '52496.151'], ['43649762', '52479.158'], ['43649762', '52480.158']]`

## Candidate counts (after NMS)

- `chest knob` (target): **2**
- `chest` (host): **0**
- `vanity table` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
