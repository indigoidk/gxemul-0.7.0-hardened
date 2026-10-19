**Kill table 1b** (`killtable1b_20261018/`, 23:13:18-23:17:48; its addendum `PRETABLE_ADDENDUM_t1b.out` was written at
21:50:25, before the run; same frozen instrument, same baseline; the clone restored to the fix, both clearance parts,
sentinel cleared).  Five mutants, each an exact-anchor edit of the fix, each answering a gap table 1 left:

```
mutant      edit                                                        predicted   measured
E1_gt3      `> GET_RESOLUTION' -> `> GET_RESOLUTION + 1' (FILL accepted) 19 red      76/95 -- the same 19 rows
E2_nopref   the gate also refuses NOP                                    3 red       92/95 -- acc nop cmd 0x2,
                                                                                     acc nop quiet 1, latch nop cmd 0x2
E3_setref   the gate also refuses SET_RESOLUTION                         5 red       90/95 -- the same 5 rows
E4_hoist    the dispatch moved out of the store branch, so a refusal     22 red      73/95 -- ref * x1 and ref * y1,
            re-runs the PREVIOUS command (the seed's GET)                            all 11 classes (0x0)
E5_signed   `(int64_t) idata > GET_RESOLUTION' (negative values pass)    5 red       90/95 -- ref m1d, its 5 rows
```

**Every prediction held, row for row.**  E1 is rule D2's past-the-bound edge in the direction that re-opens the host
kill: `ref 3` and `ref sb3` die, and so do the sessions whose first refusal is 3 (L, T2, F).  E2 and E3 settle table
1's one failed prediction: with only ONE cell refused, the NOP and SET rows that D4 masked are live (the seed's GET now
lands, so a refused NOP leaves COMMAND at 2).  E4 shows the "nothing executes" claim is carried by every R class's
X1/Y1 rows.  E5 shows the sign axis is carried by `m1d` alone -- `m1w` (sw 0xffffffff) arrives zero-extended and is
positive.
