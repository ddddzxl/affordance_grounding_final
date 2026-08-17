# q353

**Instruction**: Open the left door of the wooden cabinet located directly under the shelf with
the picture frames

**target**: `door handle`   **host**: `cabinet door`

## Reasoning

door handle#0 (434x922, area 9.6%) and #1 (230x703) are giant false detections, not handles;
the real handles are #2/#3/#4, at about 26x25 px. #2 (cx 1286) and #4 (cx 1279) are stacked
vertically and belong to the left leaf, #3 (cx 1459) to the right leaf, with the central seam
at about x=1370. left -> the left leaf; take the higher-scoring #2.

**FINAL: #2**   confidence **low**
