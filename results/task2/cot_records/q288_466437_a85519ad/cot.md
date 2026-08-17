# q288

**Instruction**: Open the second closet door from the right

**target**: `door handle`   **host**: `closet door`

## Reasoning

Four closet door candidates, splitting into **two tiers by width and score**:

    real doors: #1 x[478,1040] w=562 score 0.929 -> #1   |  #0 x[851,1361] w=510 score 0.933 -> #0,#6
    doubtful:   #3 x[1235,1439] w=204 score 0.174 -> #3  |  #2 x[1365,1439] w= 74 score 0.410 -> (none)

#2 and #3 hug the right border and are both narrow and low-scoring -- more likely a door gap or
a truncated frame.

Counting only the two real doors from the right: #0 (cx 1118) is first and #1 (cx 764) is
second -> **#1**. If #3 counts as a door too, the answer becomes #0 -- that is the sole risk
here.

## FINAL

`FINAL: #1`   confidence **medium**

> Whether the two right-hand candidates count as doors determines where the ordinal starts.

> **Excluded from the reported statistics**: ground truth disputed. On manual review the door
> ordering from the right and from the left disagrees with the annotation, and the right side
> of the frame is cut off by a mirror.
