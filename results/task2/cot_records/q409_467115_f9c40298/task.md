# q409_467115_f9c40298 - visit 467115 / desc f9c40298

## Instruction

> Plug the device in the bottom socket above the kitchen counter

## Stage 0 parse

```json
{
 "target": {
  "concept": "socket",
  "host": null
 },
 "entities": [
  {
   "name": "socket",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "counter",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "above",
   "a": "socket",
   "b": "counter"
  }
 ],
 "select": [
  {
   "on": "socket",
   "axis": "vertical",
   "value": "bottom",
   "index": null,
   "from": null
  }
 ],
 "residual": null
}
```

## Selected frame

- `467115/47333310/28288.768`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-8 alternative frames: `[['47333310', '28288.768'], ['47333308', '28042.269'], ['47333319', '28408.652'], ['47333308', '28095.364'], ['47333310', '28274.757'], ['47333319', '28477.857'], ['47333319', '28493.851'], ['47333308', '28043.268']]`

## Candidate counts (after NMS)

- `socket` (target): **1**
- `counter` (landmark): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
