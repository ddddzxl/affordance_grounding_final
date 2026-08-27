# q260

**Instruction**: Open the bottom drawer of the blue closet near the window

**target**: `drawer handle`   **host**: `drawer`

## select applies to the host; with one host it is a no-op

```
drawer#0  x[867,1072] y[839,1056]  contains #0, #1
```

`select: vertical bottom` is meant to take the lowest of **several drawers**. Only one drawer
was detected, so the set degenerates to a single element and **select becomes a no-op** -- that
is not a signal that it may instead be applied to the handles.

So rule 3 applies: emit everything `drawer#0` contains -> **#0, #1**.

## Why `bottom` may not be pushed down to the handles

Comparing `bottom` against the two handles' cy (902 vs 981) and taking the lower one is **the
same trap as pushing select down to the target layer**.

The tempting justification is that "drawer#0 is 217 px tall and holds two handles 79 px apart,
so it is two merged layers". But "the host is a merged detection" only licenses applying
select at the target layer when the instruction **explicitly acknowledges the subdivision**
(as in questions that say "window **part**"); here the instruction says "the bottom drawer",
which selects among several drawers, and only one was detected.

**FINAL: #0, #1**
