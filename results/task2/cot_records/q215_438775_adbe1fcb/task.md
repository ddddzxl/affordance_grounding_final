# q215_438775_adbe1fcb - visit 438775 / desc adbe1fcb

## Instruction

> Open the right window door behind the leather ottoman

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
   "value": "right",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `438775/44358173/62470.957`  (1920x1440)
- relaxation level **L0**, chosen from 266 frames (stride 10)
- top-8 alternative frames: `[['44358173', '62470.957'], ['44358170', '62328.147'], ['44358173', '62472.956'], ['44358170', '62358.352'], ['44358176', '62280.449'], ['44358173', '62471.957'], ['44358176', '62261.457'], ['44358170', '62334.561']]`

## Candidate counts (after NMS)

- `window handle` (target): **4**
- `window door` (host): **2**
- `ottoman` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
