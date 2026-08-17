# q305_466841_5d7d51da - visit 466841 / desc 5d7d51da

## Instruction

> Open the left window behind the potted plant

## Stage 0 parse

```json
{
 "target": {
  "concept": "window handle",
  "host": "window"
 },
 "entities": [
  {
   "name": "window handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "window",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "potted plant",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "behind",
   "a": "window",
   "b": "potted plant"
  }
 ],
 "select": [
  {
   "on": "window",
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

- `466841/47331587/15990.197`  (1920x1440)
- relaxation level **L0**, chosen from 135 frames (stride 10)
- top-5 alternative frames: `[['47331587', '15990.197'], ['47331591', '16038.894'], ['47331589', '15937.001'], ['47331589', '15939.001'], ['47331591', '16039.893']]`

## Candidate counts (after NMS)

- `window handle` (target): **11**
- `window` (host): **3**
- `potted plant` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
