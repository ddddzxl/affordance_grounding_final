# q119

**Instruction**: Open the drawer of the white vanity table

**target**: `drawer handle`   **host**: `drawer`

## One host, so emit everything it holds

```
drawer#0  x[32,1299] w=1267  contains #0, #1
```

The instruction says only "the drawer", with **no select**, and only one drawer was detected.
By uniform rule 3 (choose the host -> take its filled mask -> emit however many targets fall
inside), the answer is **#0, #1**.

## Why a merged host does not license bypassing the rule

`w=1267` does suggest a whole row of drawers merged into one detection, with the two handles
861 px apart in cx belonging to two different drawers. That observation **is not grounds for
bypassing the rule**: there is no way to establish how many drawers it should split into, and
the rule exists precisely for this situation.

The expected-value argument does not favour emitting one either. Emitting both puts precision
at exactly 0.5, which passes -- **`precision >= 0.5` includes equality** -- while emitting one
carries roughly a 50% chance of picking the wrong one and scoring zero. The two options have
almost equal expected AP50, and emitting both has strictly higher AR50.

**FINAL: #0, #1**
