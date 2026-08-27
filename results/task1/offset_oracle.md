# offset oracle — does skipping DBSCAN buy anything? (sprint §4 step0)

> val scenes 30 | eps=0.05 min_samples=10 min_cluster=20
> ALL modes use GT per-point cls -> AP deltas are pure instancing-paradigm signal.

## Headline (AP / AP50 / AP25)
| mode | AP | AP50 | AP25 | isolates |
|---|---|---|---|---|
| perfect_inst | 93.248 | 96.742 | 96.993 | observed-only ceiling (100→ gap = unobserved-pt FN) |
| offset | 89.231 | 94.906 | 95.157 | UPPER BOUND of a perfect offset head |
| dbscan | 71.128 | 84.413 | 85.964 | current oracle (raw-xyz DBSCAN), baseline to beat |

## Gap decomposition (AP)
- 100 → perfect_inst : **+6.75**  (unobserved points; unfixable by us)
- perfect_inst → offset : **-4.02**  (residual: adjacent centroids < eps)
- offset → dbscan : **-18.10**  ← **DECISION**: what offset-grouping buys = -(this)

## Per-class AP (focus: plug_in / unplug = DBSCAN's merge victims @ oracle 39/38)
| class | perfect_inst | offset | dbscan | offset−dbscan |
|---|---|---|---|---|
| rotate | 84.385 | 76.554 | 66.192 | +10.362 |
| key_press | 99.367 | 99.367 | 75.548 | +23.819 |
| tip_push | 97.065 | 92.521 | 88.015 | +4.506 |
| hook_pull | 96.453 | 96.453 | 76.384 | +20.069 |
| pinch_pull | 91.945 | 91.945 | 84.406 | +7.539 |
| hook_turn | 75.995 | 75.995 | 72.460 | +3.535 |
| foot_push | 100.000 | 100.000 | 100.000 | +0.000 |
| plug_in | 97.248 | 73.471 | 38.951 | +34.520 |
| unplug | 96.774 | 96.774 | 38.198 | +58.576 |

## Verdict (mechanical heuristic — confirm by eye)
- offset−dbscan overall = **+18.10**  → **BUILD offset head**
- plug_in: offset 73.471 vs dbscan 38.951 (+34.520)
- unplug: offset 96.774 vs dbscan 38.198 (+58.576)
> heuristic: ≥5 build · <2 skip · else marginal. The real call also weighs plug_in/unplug specifically (that's where DBSCAN merges).
