# q10 - Plug in the air fryer using the nearest socket

## Reasoning

`air fryer` has only two low-confidence detections (score 0.546 / 0.455). Computing the pixel
distance from each to both sockets:

    taking `air fryer #0` (cx=227): to socket 1 = 391, to socket 0 = 1128 -> **socket 1**
    taking `air fryer #1` (cx=828): to socket 1 = 493, to socket 0 =  522 -> **socket 1**

Both detections give the same answer, so the conclusion does not depend on which of them is the
real air fryer. Recorded as medium rather than high because the landmark's own detection quality
is poor.

```json
{"final": [1], "confidence": "medium", "kind": "relation"}
```
