# q298_466841_01e9957b - visit 466841 / desc 01e9957b

## Instruction

> Open the window door that leads to the balcony

## Stage 0 parse

```json
{
 "target": {
  "concept": "window handle",
  "host": "window door"
 },
 "entities": [
  {
   "name": "window handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "window door",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": "'leads to the balcony' is an area-level locator, not groundable"
}
```

## Selected frame

- `466841/47331587/15968.006`  (1920x1440)
- relaxation level **L0**, chosen from 135 frames (stride 10)
- top-8 alternative frames: `[['47331587', '15968.006'], ['47331587', '15989.197'], ['47331587', '15990.197'], ['47331589', '15924.406'], ['47331587', '16001.192'], ['47331587', '16010.205'], ['47331589', '15935.002'], ['47331589', '15934.003']]`

## Candidate counts (after NMS)

- `window handle` (target): **1**
- `window door` (host): **0**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
