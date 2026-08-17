# q055_422356_bd016cae - visit 422356 / desc bd016cae

## Instruction

> Turn on the TV using the remote control on the table

## Stage 0 parse

```json
{
 "target": {
  "concept": "remote control",
  "host": null
 },
 "entities": [
  {
   "name": "remote control",
   "role": "target",
   "instanceable": true
  },
  {
   "name": "table",
   "role": "container",
   "instanceable": true
  }
 ],
 "relations": [
  {
   "rel": "on_top",
   "a": "remote control",
   "b": "table"
  }
 ],
 "select": [],
 "residual": "independent check on the train split (val untouched): handheld-device GT median 478 points vs 87-108 for fixed-furniture handles, a factor of 4.4-5.5 -> the annotation covers the whole device"
}
```

## Selected frame

- `422356/42446579/205816.462`  (1920x1440)
- relaxation level **L0**, chosen from 115 frames (stride 10)
- top-8 alternative frames: `[['42446579', '205816.462'], ['42446576', '205865.359'], ['42446579', '205814.463'], ['42446579', '205815.463'], ['42446576', '205866.359'], ['42446579', '205834.655'], ['42446576', '205896.963'], ['42446579', '205835.671']]`

## Candidate counts (after NMS)

- `remote control` (target): **2**
- `table` (container): **2**

> This directory contains **no ground truth**. The reasoning stage read only
> `candidates.txt`.
