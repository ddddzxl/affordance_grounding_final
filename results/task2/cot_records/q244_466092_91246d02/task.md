# q244_466092_91246d02 - visit 466092 / desc 91246d02

## Instruction

> Open the window on the right behind the chair

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
   "name": "chair",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "behind",
   "a": "window",
   "b": "chair"
  }
 ],
 "select": [
  {
   "on": "window",
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

- `466092/44796568/16111.993`  (1920x1440)
- relaxation level **L0**, chosen from 179 frames (stride 10)
- top-8 alternative frames: `[['44796568', '16111.993'], ['44796562', '15935.300'], ['44796562', '15943.296'], ['44796568', '16103.497'], ['44796562', '16007.403'], ['44796568', '16105.996'], ['44796562', '15944.296'], ['44796568', '16114.992']]`

## Candidate counts (after NMS)

- `window handle` (target): **5**
- `window` (host): **4**
- `chair` (landmark): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
