# q220_438775_f5c1f30c - visit 438775 / desc f5c1f30c

## Instruction

> Open the left window door behind the leather ottoman

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
  },
  {
   "name": "ottoman",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "behind",
   "a": "window door",
   "b": "ottoman"
  }
 ],
 "select": [
  {
   "on": "window door",
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

- `438775/44358170/62328.147`  (1920x1440)
- relaxation level **L0**, chosen from 266 frames (stride 10)
- top-8 alternative frames: `[['44358170', '62328.147'], ['44358170', '62358.352'], ['44358173', '62470.957'], ['44358173', '62472.956'], ['44358176', '62280.449'], ['44358173', '62471.957'], ['44358170', '62356.353'], ['44358173', '62426.558']]`

## Candidate counts (after NMS)

- `window handle` (target): **19**
- `window door` (host): **3**
- `ottoman` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
