# q377

**Instruction**: Unplug the stereo system on the shelf

**target**: `plug`   **host**: `stereo system`

## Reasoning

The residual already states that the plug is not on the stereo, so the host mechanism fails by
design here. stereo system#0 spans x[1176,1439], and plug#1 (cx 1101) is only 76 px from its
left edge, while the other three are more than 400 px away.

**FINAL: #1**

> Flagged as a question defect (`ambiguous_gt`).
