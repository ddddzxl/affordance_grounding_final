# q184_437294_77b04e39 - visit 437294 / desc 77b04e39

## Instruction

> Turn on the left mirror light on the vanity table

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
   "value": "left",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `437294/43649767/52367.055`  (1920x1440)
- relaxation level **L0**, chosen from 203 frames (stride 10)
- top-4 alternative frames: `[['43649767', '52367.055'], ['43649762', '52473.244'], ['43649767', '52368.054'], ['43649762', '52501.149']]`

## Candidate counts (after NMS)

- `light switch` (target): **3**
- `mirror light` (host): **0**
- `vanity table` (container): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
