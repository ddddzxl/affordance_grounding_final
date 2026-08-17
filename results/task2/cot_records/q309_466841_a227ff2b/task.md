# q309_466841_a227ff2b - visit 466841 / desc a227ff2b

## Instruction

> Open the small white storage box on the desk

## Stage 0 parse

```json
{
 "target": {
  "concept": "storage box lid",
  "host": "storage box"
 },
 "entities": [
  {
   "name": "storage box lid",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "storage box",
   "role": "host",
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
   "a": "storage box",
   "b": "desk"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466841/47331589/15935.002`  (1920x1440)
- relaxation level **L0**, chosen from 135 frames (stride 10)
- top-8 alternative frames: `[['47331589', '15935.002'], ['47331591', '16027.898'], ['47331589', '15939.001'], ['47331587', '15993.195'], ['47331587', '15992.196'], ['47331591', '16034.895'], ['47331589', '15930.004'], ['47331591', '16037.894']]`

## Candidate counts (after NMS)

- `storage box lid` (target): **5**
- `storage box` (host): **6**
- `desk` (container): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
