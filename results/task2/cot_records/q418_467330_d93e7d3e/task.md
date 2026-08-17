# q418_467330_d93e7d3e - visit 467330 / desc d93e7d3e

## Instruction

> Control the temperature using the radiator dial under the gnomes

## Stage 0 parse

```json
{
 "target": {
  "concept": "radiator knob",
  "host": null
 },
 "entities": [
  {
   "name": "radiator knob",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "gnomes",
   "role": "landmark",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "under",
   "a": "radiator knob",
   "b": "gnomes"
  }
 ],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467330/45261598/52935.516`  (1920x1440)
- relaxation level **L0**, chosen from 207 frames (stride 10)
- top-8 alternative frames: `[['45261598', '52935.516'], ['45261601', '52855.315'], ['45261600', '53019.117'], ['45261598', '52898.514'], ['45261601', '52848.317'], ['45261598', '52918.123'], ['45261600', '53020.116'], ['45261600', '53017.117']]`

## Candidate counts (after NMS)

- `radiator knob` (target): **2**
- `gnomes` (landmark): **3**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
