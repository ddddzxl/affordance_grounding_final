# q010

**Instruction**: Open the third drawer of the cabinet located to the left of the TV

**target**: `drawer handle`   **host**: `drawer`

## Reasoning

Same frame as q009. cabinet 1 (x 81-663) is left of the TV (cx 1018) -> target container.

The containment table's **w field gives the layer structure directly**, with no need to infer
it back from handle positions:

    layer 1  drawer #5 x[ 80,295] w=215 contains #13        <- narrow
             drawer #9 x[278,564] w=286 contains #5         <- narrow, meeting #5 at 295/278
    layer 2  drawer #6 x[129,584] w=455 contains #9,  #14   <- wide, about the sum of the two
    layer 3  drawer #2 x[159,595] w=436 contains #8,  #12
    layer 4  drawer #7 x[194,614] w=420 contains #15, #19
    layer 5  drawer #8 x[226,628] w=402 contains #10, #16
    layer 6  drawer #3 x[253,640] w=387 contains #11, #18

third -> layer 3 -> drawer #2 -> **#8, #12**.

## FINAL

`FINAL: #8, #12`   confidence **high**
