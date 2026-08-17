# q262

**Instruction**: Close the bedroom door

**target**: `door handle`   **host**: `door`

## Reasoning

`door#0` x[691,845] and `door#1` x[846,997] meet exactly at their boundary -> **a double door**.
Handles `#1` (cx 823) and `#0` (cx 858) are 35 px apart at almost the same height (817 / 814)
-> **a pair of handles either side of the central seam**, assigned one to each leaf at the
845/846 boundary, consistent with the containment table.

There is no select, so "the door" takes the more complete leaf: `door#0` at area 2.894% and
629 px tall, against `door#1` at 1.561% and only 317 px tall (a door is not that short, so it is
probably occluded).

**FINAL: #1**
