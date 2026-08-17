# q352_466916_7dd39359 - visit 466916 / desc 7dd39359

## Instruction

> Open the glass door that leads to the patio

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
  }
 ],
 "relations": [],
 "select": [],
 "residual": "'leads to the patio' is an area-level locator, not groundable"
}
```

## Selected frame

- `466916/47331617/18250.299`  (1920x1440)
- relaxation level **L0**, chosen from 306 frames (stride 10)
- top-8 alternative frames: `[['47331617', '18250.299'], ['47331618', '17972.195'], ['47331615', '18096.095'], ['47331617', '18176.795'], ['47331615', '18100.093'], ['47331617', '18180.894'], ['47331617', '18146.591'], ['47331617', '18136.595']]`

## Candidate counts (after NMS)

- `door handle` (target): **3**
- `door` (host): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
