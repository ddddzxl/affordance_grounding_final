# q180_437294_34fa169a - visit 437294 / desc 34fa169a

## Instruction

> Open the right chest on the vanity table

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
   "value": "right",
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
- top-8 alternative frames: `[['43649762', '52528.854'], ['43649762', '52491.153'], ['43649762', '52529.854'], ['43649762', '52492.153'], ['43649762', '52501.149'], ['43649762', '52530.853'], ['43649763', '52426.147'], ['43649763', '52423.148']]`

## Candidate counts (after NMS)

- `chest knob` (target): **2**
- `chest` (host): **0**
- `vanity table` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
