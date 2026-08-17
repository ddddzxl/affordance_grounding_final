# q401_467115_d198ade8 - visit 467115 / desc d198ade8

## Instruction

> Select a microwave function

## Stage 0 parse

```json
{
 "target": {
  "concept": "microwave button",
  "host": "microwave"
 },
 "entities": [
  {
   "name": "microwave button",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "microwave",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": "no disambiguating cue — any of the microwave controls is acceptable"
}
```

## Selected frame

- `467115/47333310/28315.757`  (1440x1920)
- relaxation level **L0**, chosen from 608 frames (stride 10)
- top-8 alternative frames: `[['47333310', '28315.757'], ['47333308', '28018.162'], ['47333308', '28017.162'], ['47333308', '28021.160'], ['47333308', '28099.362'], ['47333308', '28015.163'], ['47333310', '28221.562'], ['47333308', '28016.162']]`

## Candidate counts (after NMS)

- `microwave button` (target): **21**
- `microwave` (host): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
