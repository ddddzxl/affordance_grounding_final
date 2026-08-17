# q282_466437_57b6a5d3 - visit 466437 / desc 57b6a5d3

## Instruction

> Open the small red jewelry box next to the mirror on the cabinet

## Stage 0 parse

```json
{
 "target": {
  "concept": "lid",
  "host": "jewelry box"
 },
 "entities": [
  {
   "name": "lid",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "jewelry box",
   "role": "host",
   "instanceable": true
  },
  {
   "name": "mirror",
   "role": "landmark",
   "instanceable": true
  },
  {
   "name": "cabinet",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "next_to",
   "a": "jewelry box",
   "b": "mirror"
  },
  {
   "rel": "on_top",
   "a": "jewelry box",
   "b": "cabinet"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `466437/45260951/6170.109`  (1440x1920)
- relaxation level **POOL**, chosen from 257 frames (stride 10)
- top-8 alternative frames: `[['45260951', '6170.109'], ['45260951', '6173.108'], ['45260951', '6172.108'], ['45260951', '6171.109'], ['45260951', '6184.320'], ['45260951', '6195.316'], ['45260951', '6204.312'], ['45260951', '6113.215']]`

## Candidate counts (after NMS)

- `lid` (target): **3**
- `jewelry box` (host): **0**
- `mirror` (landmark): **0**
- `cabinet` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
