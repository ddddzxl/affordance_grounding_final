# q412_467139_7fd69cfa - visit 467139 / desc 7fd69cfa

## Instruction

> Flush the toilet

## Stage 0 parse

```json
{
 "target": {
  "concept": "flush button",
  "host": "toilet"
 },
 "entities": [
  {
   "name": "flush button",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "toilet",
   "role": "host",
   "instanceable": true
  }
 ],
 "relations": [],
 "select": [],
 "residual": null
}
```

## Selected frame

- `467139/47333298/26661.650`  (1920x1440)
- relaxation level **L0**, chosen from 366 frames (stride 10)
- top-8 alternative frames: `[['47333298', '26661.650'], ['47333298', '26660.650'], ['47333298', '26662.649'], ['47333298', '26659.651'], ['47333293', '26506.047'], ['47333293', '26535.052'], ['47333298', '26683.957'], ['47333298', '26664.649']]`

## Candidate counts (after NMS)

- `flush button` (target): **6**
- `toilet` (host): **1**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
