# q023

**Instruction**: Open the top right drawer of the cabinet located to the left of the TV

**target**: `drawer handle`   **host**: `drawer`

## Reasoning

Same frame as q009/q010/q011/q016, where the layer structure has already been verified several
times. cabinet 1 (x 81-663) is left of the TV (cx 1018).

    layer 1  #5 x[ 80,295] w=215 -> #13    |  #9 x[278,564] w=286 -> #5    two narrow, side by side
    layer 2  #6 w=455 -> #9,#14 | layer 3 #2 w=436 -> #8,#12 | layer 4 #7 w=420 -> #15,#19
    layer 5  #8 w=402 -> #10,#16 | layer 6 #3 w=387 -> #11,#18

Only **layer 1** splits left/right; the layers below are single full-width drawers. So
top + right must land in layer 1 -> drawer #9 (x 278-564, the right one) -> **#5**.

q003 asked for top left on a different frame and answered the left member of layer 1, which is
symmetric with this.

## FINAL

`FINAL: #5`   confidence **high**
