# q013

**Instruction**: Turn on the TV using the right remote on the nightstand

**target**: `remote control`   **host**: `None`

## Reasoning

With host=None the parsed `select` applies directly to the target, which is a legitimate form.
on_top(., nightstand) first removes #2 (cx 1314, off the nightstand); of the remaining #0
(cx 733) and #1 (cx 849), right -> #1. The residual confirms the ground truth annotates the
whole remote, so stopping the concept at device level is correct here.

**FINAL: #1**
