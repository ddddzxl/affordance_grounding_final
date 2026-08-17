# q051_422356_7aed0171 - visit 422356 / desc 7aed0171

## Instruction

> Type using the keyboard on the desk

## Stage 0 parse

```json
{
 "target": {
  "concept": "keyboard",
  "host": null
 },
 "entities": [
  {
   "name": "keyboard",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "desk",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "keyboard",
   "b": "desk"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `422356/42446579/205829.457`  (1920x1440)
- relaxation level **L0**, chosen from 115 frames (stride 10)
- top-8 alternative frames: `[['42446579', '205829.457'], ['42446576', '205880.170'], ['42446579', '205828.458'], ['42446576', '205881.169'], ['42446576', '205874.355'], ['42446576', '205875.355'], ['42446579', '205812.464'], ['42446579', '205827.458']]`

## Candidate counts (after NMS)

- `keyboard` (target): **2**
- `desk` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
