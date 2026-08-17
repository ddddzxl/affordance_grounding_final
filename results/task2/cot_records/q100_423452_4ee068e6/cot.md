# q100

**Instruction**: Plug the device in the socket next to the dining table

**target**: `socket`   **host**: `None`

## Reasoning

dining table#0's left edge is at 1143 and socket#0's right edge at 1079 -- only 64 px apart,
while the other three sockets are 438-870 px away. #0 also has the highest score in the frame
at 0.857.

**FINAL: #0**

> Flagged as a question defect (`ambiguous_gt`): the wording admits more than one reading and
> the ground truth annotates only one of them.
