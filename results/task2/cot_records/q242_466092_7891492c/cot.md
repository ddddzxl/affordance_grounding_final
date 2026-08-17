# q242

**Instruction**: Open the window behind the table

**target**: `window handle`   **host**: `window`

## Reasoning

Of the four window candidates, only two contain a handle:

    window #0 x[1302,1764] w=462 score 0.730 -> #2
    window #3 x[1873,1919] w= 46 score 0.230 -> #0

behind(window, table) is **undecidable** under a 2D projection (the rules mark it as such), and
has_on_top(table, flower vase) only identifies which table is meant, which does not help choose
a window.

That leaves detection quality: #3 is only 46 px wide and flush with the right border, so it is
a truncated window, while #0 is a complete one. -> window #0 -> **#2**.

## FINAL

`FINAL: #2`   confidence **low**

> `behind` is undecidable, so this falls back on detection quality.
