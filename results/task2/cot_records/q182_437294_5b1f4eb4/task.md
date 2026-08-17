# q182_437294_5b1f4eb4 - visit 437294 / desc 5b1f4eb4

## Instruction

> Turn on the right mirror light on the vanity table

## Stage 0 parse

```json
{
 "target": {
  "concept": "light switch",
  "host": "mirror light"
 },
 "entities": [
  {
   "name": "light switch",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "mirror light",
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
   "a": "mirror light",
   "b": "vanity table"
  }
 ],
 "select": [
  {
   "on": "mirror light",
   "axis": "horizontal",
   "value": "right",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `437294/43649762/52490.154`  (1920x1440)
- relaxation level **L0**, chosen from 203 frames (stride 10)
- top-6 alternative frames: `[['43649762', '52490.154'], ['43649767', '52367.055'], ['43649762', '52473.244'], ['43649767', '52368.054'], ['43649767', '52369.054'], ['43649762', '52501.149']]`

## Candidate counts (after NMS)

- `light switch` (target): **2**
- `mirror light` (host): **0**
- `vanity table` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
