# q009

**Instruction**: Open the fourth drawer of the cabinet located to the left of the TV

**target**: `drawer handle`   **host**: `drawer`

## Reasoning (revised)

cabinet 1 (x 81-663, cx 392.4) is left of the TV (cx 1018.2) -> that is the target container.

**First resolve the drawer layer structure** (the previous version skipped this step):

    layer 1  drawer 5 (x  80-295, cy 186)  holds handle #13      <- left
             drawer 9 (x 278-564, cy 231)  holds handle #5       <- right   two narrow drawers
    layer 2  drawer 6 (x 129-584, cy 380)  holds #14 + #9        <- wide drawer, two handles
    layer 3  drawer 2 (x 159-595, cy 527)  holds #12 + #8
    layer 4  drawer 7 (x 194-614, cy 662)  holds #15 + #19
    layer 5  drawer 8 (x 226-628, cy 782)  holds #16 + #10
    layer 6  drawer 3 (x 253-640, cy 889)  holds #18 + #11

Seven drawers = two in the top row plus five wide ones below. The wide drawers span about
455 px, close to the sum of the top row's two (about 215 and 286) -- **the widths alone
establish the structure.**

fourth -> the fourth **layer** from the top -> drawer 7 -> it covers #15 and #19 -> **give
both**.

The previous version answered #15 only. The error was treating the two columns of handles as
two columns of independent drawers, which turns "the fourth" into "fourth in the left column"
and then requires deciding which column to use. In fact **the lower layers have no left/right
division at all**: one layer is one drawer.

## The uniform rule for cabinet reasoning (fixed from this question onward)

    1. `select` always applies to the **host (drawer)**, never directly to the handles
    2. having chosen the target drawer, take its **hole-filled mask**
    3. every handle inside that mask is emitted -- however many there are

This rule distinguishes the two cabinet structures automatically, with no need to decide in
advance which layer splits left/right:

    narrow drawer (common in the top row)  -> covers 1 handle  -> emit 1
    wide drawer (the lower layers)         -> covers 2 handles -> emit 2

Whether left/right matters is decided by the drawer's actual width, not by my judgement. The
first version failed precisely by **skipping the host and ordering handles directly**, which
mistook one wide drawer's two handles for two columns of independent drawers.

## FINAL

`FINAL: #15, #19`   confidence **high**

> Revision: the first version answered [15] and missed the paired second handle.
