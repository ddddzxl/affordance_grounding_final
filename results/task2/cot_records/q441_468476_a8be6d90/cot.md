# q441

**Instruction**: Unplug the floor lamp next to the couch

**target**: `plug`   **host**: `floor lamp`

## Reasoning

The containment table offers #2, which sits on the lamp body -- but the residual states
explicitly that the plug is at the socket end, which makes that assignment suspect rather than
supportive. #0 (cy 1367) and #1 (cy 1318) are near the floor, at wall-socket height, and their
cx of 639 and 644 places them directly below the floor lamp. Their y intervals almost touch, so
they are one object split in two; take the larger by score and area, #0.

**FINAL: #0**

> Flagged as a question defect (`unanswerable`).
