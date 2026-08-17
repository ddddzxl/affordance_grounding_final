# q436

**Instruction**: Close the door next to the white couch

**target**: `door handle`   **host**: `door`

## Reasoning

door#0 (score 0.951) overlaps couch#0 in x, so next_to holds; it contains #1. Candidate #0 is
claimed by door#1, which is only 43 px wide -- a door frame, not a door -- so #0 is not a door
handle.

**FINAL: #1**

> Flagged as a question defect (`ambiguous_gt`).
