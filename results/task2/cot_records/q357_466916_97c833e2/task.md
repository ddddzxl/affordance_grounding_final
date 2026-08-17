# q357_466916_97c833e2 - visit 466916 / desc 97c833e2

## Instruction

> Open the left door of the display cabinet with the lamp and printer on top

## Stage 0 parse

```json
{
 "target": {
  "concept": "door handle",
  "host": "cabinet door"
 },
 "entities": [
  {
   "name": "door handle",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "cabinet door",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "display cabinet",
   "role": "container",
   "instanceable": true
  },
  {
   "name": "lamp",
   "role": "landmark",
   "instanceable": true
  },
  {
   "name": "printer",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "contains",
   "a": "display cabinet",
   "b": "cabinet door"
  },
  {
   "rel": "has_on_top",
   "a": "display cabinet",
   "b": "lamp"
  },
  {
   "rel": "has_on_top",
   "a": "display cabinet",
   "b": "printer"
  }
 ],
 "select": [
  {
   "on": "cabinet door",
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

- `466916/47331615/18099.094`  (1920x1440)
- relaxation level **POOL-T**, chosen from 306 frames (stride 10)
- top-8 alternative frames: `[['47331615', '18099.094'], ['47331617', '18153.705'], ['47331617', '18135.595'], ['47331618', '17971.196'], ['47331617', '18149.590'], ['47331617', '18141.593'], ['47331615', '18104.092'], ['47331618', '17972.195']]`

## Candidate counts (after NMS)

- `door handle` (target): **5**
- `cabinet door` (host): **11**
- `display cabinet` (container): **3**
- `lamp` (landmark): **0**
- `printer` (landmark): **0**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
