# q183_437294_6cb1585b - visit 437294 / desc 6cb1585b

## Instruction

> Unplug the table lamp on the nightstand

## Stage 0 parse

```json
{
 "target": {
  "concept": "plug",
  "host": "table lamp"
 },
 "entities": [
  {
   "name": "plug",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "table lamp",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "nightstand",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "table lamp",
   "b": "nightstand"
  }
 ],
 "select": [],
 "residual": "the plug sits at the socket end, not on the lamp"
}
```

## Selected frame

- `437294/43649762/52550.845`  (1920x1440)
- relaxation level **L0**, chosen from 203 frames (stride 10)
- top-3 alternative frames: `[['43649762', '52550.845'], ['43649763', '52440.258'], ['43649763', '52439.258']]`

## Candidate counts (after NMS)

- `plug` (target): **3**
- `table lamp` (host): **2**
- `nightstand` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
