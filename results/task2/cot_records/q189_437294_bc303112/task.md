# q189_437294_bc303112 - visit 437294 / desc bc303112

## Instruction

> Close the door next to the nightstand

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "nightstand",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "door",
   "b": "nightstand"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `437294/43649763/52448.254`  (1920x1440)
- relaxation level **L0**, chosen from 203 frames (stride 10)
- top-5 alternative frames: `[['43649763', '52448.254'], ['43649762', '52534.852'], ['43649763', '52449.254'], ['43649767', '52382.048'], ['43649762', '52535.851']]`

## Candidate counts (after NMS)

- `door handle` (target): **2**
- `door` (host): **1**
- `nightstand` (landmark): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
