# q387

**Instruction**: Open the cabinet door above the microwave

**target**: `door handle`   **host**: `cabinet door`

## Reasoning

`microwave#0` spans x[376,1343] y[1615,1919].

Of the four cabinet doors, only `#0` x[471,1358] overlaps it in x and has cy 1076 < 1791, i.e.
sits above it; `#2` and `#3` are entirely to the left at x <= 205, and `#1` overlaps by only
13 px.

`cabinet door#0` scores **0.977** and the containment table gives `contains #0`.

**FINAL: #0**

> **Manual review overturned the automatic score here**: the projected ground-truth centre is
> only 48 px from the pick's centre while their own diagonals are 421 and 444 px (a ratio of
> 0.11) -- a displacement caused by pose accuracy, not a wrong selection.
