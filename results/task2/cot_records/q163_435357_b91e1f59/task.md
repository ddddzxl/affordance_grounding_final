# q163_435357_b91e1f59 - visit 435357 / desc b91e1f59

## Instruction

> Turn on the cylindrical white lamp in front of the window

## Stage 0 parse

```json
{
 "target": {
  "concept": "light panel",
  "host": "lamp"
 },
 "entities": [
  {
   "name": "light panel",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "lamp",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "window",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "in_front_of",
   "a": "lamp",
   "b": "window"
  }
 ],
 "select": [],
 "residual": "unified with val8's 'light switch'; which lamp it is, is carried by `host`, not by the search term"
}
```

## Selected frame

- `435357/42899624/230054.486`  (1440x1920)
- relaxation level **POOL**, chosen from 191 frames (stride 10)
- top-8 alternative frames: `[['42899624', '230054.486'], ['42899624', '230053.487'], ['42899624', '230057.485'], ['42899624', '230052.487'], ['42899624', '230051.487'], ['42899624', '230055.486'], ['42899624', '230058.485'], ['42899624', '230059.484']]`

## Candidate counts (after NMS)

- `light panel` (target): **1**
- `lamp` (host): **1**
- `window` (landmark): **0**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
