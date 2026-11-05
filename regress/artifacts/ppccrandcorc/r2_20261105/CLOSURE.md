# #575 ppccrandcorc -- CLASS CLOSURE BY SIMULATION (round 2, 2026-11-05)

Simulator: r2_20261105/v575b.py (table1_20261105/v575.py extended; `v575b.py check62' re-derives table 1's 17 predictions
on the old 62 rows and matches PRETABLE.out exactly).  Handlers simulated statement by statement:
src/cpus/cpu_ppc_instr.c X(crandc) :2729-2737 and X(crorc) :2756-2764; dispatch :4638 and :4641.

ENUMERATION (one edit per cell, per handler): field mask m in 0..30 at BT, BA, BB (3 x 31); each source read taking another
field's index (BA<-BB, BA<-BT, BB<-BA, BB<-BT); the read mask `& 1' widened to `& 3' and `& 7' at BA and at BB; the clear moved
before the reads, deleted, or replaced by a toggle; the set deleted or `|=' -> `^='; the condition edits table 1 had (b, d-moved,
d-dropped, d-crossed) plus the pass-1 ruling's four R5 bt-substitutions and the identity body; the dispatch case bound to each
of the six other CR-logical handlers; and table 1's c (both bodies identity).

DENOMINATOR: 239 cells = 6 clear + 15 cond + 12 decode + 186 mask + 8 read + 8 rmask + 4 set.

CELL -> ROW MAP (62 = red rows of the old probe; 66 = red rows of the new one; `rand-equiv' = 40000 random (cr,BT,BA,BB)
found no difference from the fix):

| class | cell | status | red on 62 | red on 66 |
|---|---|---|---|---|
| mask | crandc BT mask &0 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &1 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others |
| mask | crandc BT mask &2 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &3 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others |
| mask | crandc BT mask &4 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &5 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others |
| mask | crandc BT mask &6 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &7 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others |
| mask | crandc BT mask &8 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &9 | DETECTED(62) | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &10 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &11 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi |
| mask | crandc BT mask &12 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &13 | DETECTED(62) | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &14 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &15 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi |
| mask | crandc BT mask &16 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &17 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others |
| mask | crandc BT mask &18 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &19 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others |
| mask | crandc BT mask &20 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &21 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_crorc_11,32_others |
| mask | crandc BT mask &22 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &23 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others |
| mask | crandc BT mask &24 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &25 | DETECTED(62) | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_00,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &26 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &27 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi |
| mask | crandc BT mask &28 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &29 | DETECTED(62) | 64_crandc_00,64_crandc_10,64_crandc_11,32_crandc_00,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_10,64_crandc_11,32_crandc_00,32_crandc_10,32_crandc_11 |
| mask | crandc BT mask &30 | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_11,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_01,64_crandc_10,64_crandc_11,64_crandc_order,32_crandc_01,32_crandc_10,32_crandc_11 |
| mask | crandc BA mask &0 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,32_crandc_10 |
| mask | crandc BA mask &1 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi |
| mask | crandc BA mask &2 | DETECTED(62) | 64_crandc_10,32_crandc_10 | 64_crandc_10,32_crandc_10 |
| mask | crandc BA mask &3 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi |
| mask | crandc BA mask &4 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 |
| mask | crandc BA mask &5 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi |
| mask | crandc BA mask &6 | DETECTED(62) | 64_crandc_10,32_crandc_10 | 64_crandc_10,32_crandc_10 |
| mask | crandc BA mask &7 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi |
| mask | crandc BA mask &8 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 |
| mask | crandc BA mask &9 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi |
| mask | crandc BA mask &10 | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,32_crandc_10 |
| mask | crandc BA mask &11 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi |
| mask | crandc BA mask &12 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 |
| mask | crandc BA mask &13 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi |
| mask | crandc BA mask &14 | DETECTED(62) | 64_crandc_10,32_crandc_10 | 64_crandc_10,32_crandc_10 |
| mask | crandc BA mask &15 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi |
| mask | crandc BA mask &16 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 |
| mask | crandc BA mask &17 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi |
| mask | crandc BA mask &18 | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,32_crandc_10 |
| mask | crandc BA mask &19 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi |
| mask | crandc BA mask &20 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 |
| mask | crandc BA mask &21 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi |
| mask | crandc BA mask &22 | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,32_crandc_10 |
| mask | crandc BA mask &23 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi |
| mask | crandc BA mask &24 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 |
| mask | crandc BA mask &25 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi |
| mask | crandc BA mask &26 | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,32_crandc_10 |
| mask | crandc BA mask &27 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi |
| mask | crandc BA mask &28 | DETECTED(62) | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 | 64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_10 |
| mask | crandc BA mask &29 | DETECTED(62) | edge_crandc_bt0,64_crandc_hi | edge_crandc_bt0,64_crandc_hi |
| mask | crandc BA mask &30 | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,32_crandc_10 |
| mask | crandc BB mask &0 | DETECTED(62) | 64_crandc_11,64_crandc_hi,32_crandc_11 | 64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &1 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi,64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &2 | DETECTED(62) | 64_crandc_11,64_crandc_hi,32_crandc_11 | 64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &3 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi,64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &4 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &5 | MISSED by 62, CLOSED by 64_crandc_bbmask,64_crandc_order | none | 64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &6 | DETECTED(62) | 64_crandc_11,64_crandc_hi,32_crandc_11 | 64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &7 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi,64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &8 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &9 | MISSED by 62, CLOSED by 64_crandc_bbmask | none | 64_crandc_bbmask |
| mask | crandc BB mask &10 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &11 | MISSED by 62, CLOSED by 64_crandc_bbmask | none | 64_crandc_bbmask |
| mask | crandc BB mask &12 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &13 | MISSED by 62, CLOSED by 64_crandc_bbmask | none | 64_crandc_bbmask |
| mask | crandc BB mask &14 | DETECTED(62) | 64_crandc_11,64_crandc_hi,32_crandc_11 | 64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &15 | DETECTED(62) | 64_crandc_hi | 64_crandc_hi,64_crandc_bbmask |
| mask | crandc BB mask &16 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &17 | MISSED by 62, CLOSED by 64_crandc_bbmask,64_crandc_order | none | 64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &18 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &19 | MISSED by 62, CLOSED by 64_crandc_bbmask,64_crandc_order | none | 64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &20 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &21 | MISSED by 62, CLOSED by 64_crandc_bbmask,64_crandc_order | none | 64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &22 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &23 | MISSED by 62, CLOSED by 64_crandc_bbmask,64_crandc_order | none | 64_crandc_bbmask,64_crandc_order |
| mask | crandc BB mask &24 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &25 | MISSED by 62, CLOSED by 64_crandc_bbmask | none | 64_crandc_bbmask |
| mask | crandc BB mask &26 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &27 | MISSED by 62, CLOSED by 64_crandc_bbmask | none | 64_crandc_bbmask |
| mask | crandc BB mask &28 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| mask | crandc BB mask &29 | MISSED by 62, CLOSED by 64_crandc_bbmask | none | 64_crandc_bbmask |
| mask | crandc BB mask &30 | DETECTED(62) | 64_crandc_11,32_crandc_11 | 64_crandc_11,64_crandc_bbmask,64_crandc_order,32_crandc_11 |
| read | crandc BA read <- BB index | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_10 |
| read | crandc BA read <- BT index | DETECTED(62) | 64_crandc_00,64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_00,32_crandc_10 | 64_crandc_00,64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_00,32_crandc_10 |
| read | crandc BB read <- BA index | DETECTED(62) | 64_crandc_10,32_crandc_10 | 64_crandc_10,64_crandc_bbmask,64_crandc_order,32_crandc_10 |
| read | crandc BB read <- BT index | MISSED by 62, CLOSED by 64_crandc_bbmask | none | 64_crandc_bbmask |
| rmask | crandc BA read mask &3 | EQUIVALENT rand-equiv | none | none |
| rmask | crandc BA read mask &7 | EQUIVALENT rand-equiv | none | none |
| rmask | crandc BB read mask &3 | MISSED by 62, CLOSED by 64_crandc_bbmask | none | 64_crandc_bbmask |
| rmask | crandc BB read mask &7 | MISSED by 62, CLOSED by 64_crandc_bbmask | none | 64_crandc_bbmask |
| clear | crandc clear moved before the reads | MISSED by 62, CLOSED by 64_crandc_order | none | 64_crandc_order |
| clear | crandc clear deleted | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_11,edge_crandc_bt0,32_crandc_00,32_crandc_01,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_11,edge_crandc_bt0,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_11 |
| clear | crandc clear -> toggle (^=) | EXCLUDED | none | none |
| set | crandc set deleted | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_10 |
| set | crandc set |= -> ^= | EQUIVALENT rand-equiv | none | none |
| cond | crandc cond b1  !(ba & bb)  (NAND restored) | DETECTED(62) | 64_crandc_00,64_crandc_01,edge_crandc_bt0,32_crandc_00,32_crandc_01 | 64_crandc_00,64_crandc_01,edge_crandc_bt0,32_crandc_00,32_crandc_01 |
| cond | crandc cond d1  !ba & bb | DETECTED(62) | 64_crandc_01,64_crandc_10,64_crandc_hi,32_crandc_01,32_crandc_10 | 64_crandc_01,64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_01,32_crandc_10 |
| cond | crandc cond d3  ba & bb   (complement dropped) | DETECTED(62) | 64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_10,32_crandc_11 | 64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_10,32_crandc_11 |
| cond | crandc cond d5  ba | !bb  (operator crossed) | DETECTED(62) | 64_crandc_00,64_crandc_11,edge_crandc_bt0,32_crandc_00,32_crandc_11 | 64_crandc_00,64_crandc_11,edge_crandc_bt0,64_crandc_order,32_crandc_00,32_crandc_11 |
| cond | crandc cond r5a bt & !bb | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_10 |
| cond | crandc cond r5b ba & !bt | DETECTED(62) | 64_crandc_10,64_crandc_hi,32_crandc_10 | 64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_10 |
| cond | crandc identity body | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,edge_crandc_bt0,64_crandc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,edge_crandc_bt0,64_crandc_hi,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11 |
| decode | crandc dispatch -> instr(crand) | DETECTED(62) | 64_crandc_10,64_crandc_11,64_crandc_hi,32_crandc_10,32_crandc_11 | 64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_10,32_crandc_11 |
| decode | crandc dispatch -> instr(creqv) | DETECTED(62) | 64_crandc_00,64_crandc_10,64_crandc_11,edge_crandc_bt0,64_crandc_hi,32_crandc_00,32_crandc_10,32_crandc_11 | 64_crandc_00,64_crandc_10,64_crandc_11,edge_crandc_bt0,64_crandc_hi,64_crandc_bbmask,64_crandc_order,32_crandc_00,32_crandc_10,32_crandc_11 |
| decode | crandc dispatch -> instr(cror) | DETECTED(62) | 64_crandc_01,64_crandc_11,32_crandc_01,32_crandc_11 | 64_crandc_01,64_crandc_11,64_crandc_order,32_crandc_01,32_crandc_11 |
| decode | crandc dispatch -> instr(crorc) | DETECTED(62) | 64_crandc_00,64_crandc_11,edge_crandc_bt0,32_crandc_00,32_crandc_11 | 64_crandc_00,64_crandc_11,edge_crandc_bt0,64_crandc_order,32_crandc_00,32_crandc_11 |
| decode | crandc dispatch -> instr(crnor) | DETECTED(62) | 64_crandc_00,64_crandc_10,edge_crandc_bt0,64_crandc_hi,32_crandc_00,32_crandc_10 | 64_crandc_00,64_crandc_10,edge_crandc_bt0,64_crandc_hi,64_crandc_bbmask,32_crandc_00,32_crandc_10 |
| decode | crandc dispatch -> instr(crxor) | DETECTED(62) | 64_crandc_01,32_crandc_01 | 64_crandc_01,32_crandc_01 |
| mask | crorc BT mask &0 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crandc_bt0,edge_crorc_bt31,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crandc_bt0,edge_crorc_bt31,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &1 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &2 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &3 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &4 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &5 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &6 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &7 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &8 | DETECTED(62) | 64_crandc_00,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crandc_00,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crandc_00,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &9 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crandc_00,32_crandc_01,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crandc_01,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crandc_00,32_crandc_01,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &10 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &11 | DETECTED(62) | 64_crandc_00,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crandc_00,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crandc_00,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &12 | DETECTED(62) | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &13 | DETECTED(62) | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &14 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_11 |
| mask | crorc BT mask &15 | DETECTED(62) | edge_crorc_bt31,edge_others,64_crorc_hi | edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask |
| mask | crorc BT mask &16 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &17 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &18 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &19 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &20 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &21 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &22 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &23 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others |
| mask | crorc BT mask &24 | DETECTED(62) | 64_crandc_00,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crandc_00,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crandc_00,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &25 | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crandc_00,32_crandc_01,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crandc_01,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crandc_00,32_crandc_01,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &26 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &27 | DETECTED(62) | 64_crandc_00,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crandc_00,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crandc_00,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &28 | DETECTED(62) | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &29 | DETECTED(62) | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_bbmask,32_crorc_01,32_crorc_10,32_crorc_11 |
| mask | crorc BT mask &30 | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_11,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_11 |
| mask | crorc BA mask &0 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,32_crorc_11 |
| mask | crorc BA mask &1 | DETECTED(62) | edge_crorc_bt31,64_crorc_hi | edge_crorc_bt31,64_crorc_hi,64_crorc_bamask |
| mask | crorc BA mask &2 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,32_crorc_11 |
| mask | crorc BA mask &3 | DETECTED(62) | edge_crorc_bt31,64_crorc_hi | edge_crorc_bt31,64_crorc_hi,64_crorc_bamask |
| mask | crorc BA mask &4 | DETECTED(62) | 64_crorc_11,32_crorc_11 | 64_crorc_11,64_crorc_bamask,32_crorc_11 |
| mask | crorc BA mask &5 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask |
| mask | crorc BA mask &6 | DETECTED(62) | 64_crorc_11,32_crorc_11 | 64_crorc_11,64_crorc_bamask,32_crorc_11 |
| mask | crorc BA mask &7 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask |
| mask | crorc BA mask &8 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,32_crorc_11 |
| mask | crorc BA mask &9 | DETECTED(62) | edge_crorc_bt31 | edge_crorc_bt31,64_crorc_bamask |
| mask | crorc BA mask &10 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,32_crorc_11 |
| mask | crorc BA mask &11 | DETECTED(62) | edge_crorc_bt31 | edge_crorc_bt31,64_crorc_bamask |
| mask | crorc BA mask &12 | DETECTED(62) | 64_crorc_11,32_crorc_11 | 64_crorc_11,64_crorc_bamask,32_crorc_11 |
| mask | crorc BA mask &13 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask |
| mask | crorc BA mask &14 | DETECTED(62) | 64_crorc_11,32_crorc_11 | 64_crorc_11,64_crorc_bamask,32_crorc_11 |
| mask | crorc BA mask &15 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask |
| mask | crorc BA mask &16 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,32_crorc_11 |
| mask | crorc BA mask &17 | DETECTED(62) | edge_crorc_bt31 | edge_crorc_bt31,64_crorc_bamask |
| mask | crorc BA mask &18 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,32_crorc_11 |
| mask | crorc BA mask &19 | DETECTED(62) | edge_crorc_bt31 | edge_crorc_bt31,64_crorc_bamask |
| mask | crorc BA mask &20 | DETECTED(62) | 64_crorc_11,32_crorc_11 | 64_crorc_11,64_crorc_bamask,32_crorc_11 |
| mask | crorc BA mask &21 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask |
| mask | crorc BA mask &22 | DETECTED(62) | 64_crorc_11,32_crorc_11 | 64_crorc_11,64_crorc_bamask,32_crorc_11 |
| mask | crorc BA mask &23 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask |
| mask | crorc BA mask &24 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,32_crorc_11 |
| mask | crorc BA mask &25 | DETECTED(62) | edge_crorc_bt31 | edge_crorc_bt31,64_crorc_bamask |
| mask | crorc BA mask &26 | DETECTED(62) | 64_crorc_11,edge_crorc_bt31,32_crorc_11 | 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,32_crorc_11 |
| mask | crorc BA mask &27 | DETECTED(62) | edge_crorc_bt31 | edge_crorc_bt31,64_crorc_bamask |
| mask | crorc BA mask &28 | DETECTED(62) | 64_crorc_11,64_crorc_hi,32_crorc_11 | 64_crorc_11,64_crorc_hi,64_crorc_bamask,32_crorc_11 |
| mask | crorc BA mask &29 | MISSED by 62, CLOSED by 64_crorc_bamask | none | 64_crorc_bamask |
| mask | crorc BA mask &30 | DETECTED(62) | 64_crorc_11,64_crorc_hi,32_crorc_11 | 64_crorc_11,64_crorc_hi,64_crorc_bamask,32_crorc_11 |
| mask | crorc BB mask &0 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| mask | crorc BB mask &1 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask |
| mask | crorc BB mask &2 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| mask | crorc BB mask &3 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask |
| mask | crorc BB mask &4 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| mask | crorc BB mask &5 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask |
| mask | crorc BB mask &6 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| mask | crorc BB mask &7 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask |
| mask | crorc BB mask &8 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| mask | crorc BB mask &9 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask |
| mask | crorc BB mask &10 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| mask | crorc BB mask &11 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask |
| mask | crorc BB mask &12 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| mask | crorc BB mask &13 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask |
| mask | crorc BB mask &14 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| mask | crorc BB mask &15 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask |
| mask | crorc BB mask &16 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| mask | crorc BB mask &17 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask |
| mask | crorc BB mask &18 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| mask | crorc BB mask &19 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask |
| mask | crorc BB mask &20 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| mask | crorc BB mask &21 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask |
| mask | crorc BB mask &22 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| mask | crorc BB mask &23 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask |
| mask | crorc BB mask &24 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| mask | crorc BB mask &25 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask |
| mask | crorc BB mask &26 | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| mask | crorc BB mask &27 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bbmask |
| mask | crorc BB mask &28 | DETECTED(62) | 64_crorc_01,32_crorc_01 | 64_crorc_01,64_crorc_bbmask,32_crorc_01 |
| mask | crorc BB mask &29 | MISSED by 62, CLOSED by 64_crorc_bbmask | none | 64_crorc_bbmask |
| mask | crorc BB mask &30 | DETECTED(62) | 64_crorc_01,32_crorc_01 | 64_crorc_01,64_crorc_bbmask,32_crorc_01 |
| read | crorc BA read <- BB index | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,32_crorc_01 |
| read | crorc BA read <- BT index | DETECTED(62) | 64_crorc_01,64_crorc_11,edge_crorc_bt31,64_crorc_hi,32_crorc_01,32_crorc_11 | 64_crorc_01,64_crorc_11,edge_crorc_bt31,64_crorc_hi,64_crorc_bbmask,32_crorc_01,32_crorc_11 |
| read | crorc BB read <- BA index | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| read | crorc BB read <- BT index | MISSED by 62, CLOSED by 64_crorc_bamask | none | 64_crorc_bamask |
| rmask | crorc BA read mask &3 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask |
| rmask | crorc BA read mask &7 | DETECTED(62) | 64_crorc_hi | 64_crorc_hi,64_crorc_bamask |
| rmask | crorc BB read mask &3 | DETECTED(62) | 64_crorc_00,32_crorc_00 | 64_crorc_00,32_crorc_00 |
| rmask | crorc BB read mask &7 | DETECTED(62) | 64_crorc_00,32_crorc_00 | 64_crorc_00,32_crorc_00 |
| clear | crorc clear moved before the reads | MISSED by 62, CLOSED by 64_crorc_bbmask | none | 64_crorc_bbmask |
| clear | crorc clear deleted | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bbmask,32_crorc_01 |
| clear | crorc clear -> toggle (^=) | MISSED by 62, CLOSED by 64_crorc_bamask | none | 64_crorc_bamask |
| set | crorc set deleted | DETECTED(62) | 64_crorc_00,64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_00,32_crorc_10,32_crorc_11 | 64_crorc_00,64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_00,32_crorc_10,32_crorc_11 |
| set | crorc set |= -> ^= | EQUIVALENT rand-equiv | none | none |
| cond | crorc cond b2  !(ba | bb)  (NOR restored) | DETECTED(62) | 64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_10,32_crorc_11 | 64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_10,32_crorc_11 |
| cond | crorc cond d2  !ba | bb | DETECTED(62) | 64_crorc_01,64_crorc_10,64_crorc_hi,32_crorc_01,32_crorc_10 | 64_crorc_01,64_crorc_10,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,32_crorc_01,32_crorc_10 |
| cond | crorc cond d4  ba | bb   (complement dropped) | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_hi,32_crorc_00,32_crorc_01 | 64_crorc_00,64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,32_crorc_00,32_crorc_01 |
| cond | crorc cond d6  ba & !bb  (operator crossed) | DETECTED(62) | 64_crorc_00,64_crorc_11,edge_crorc_bt31,32_crorc_00,32_crorc_11 | 64_crorc_00,64_crorc_11,edge_crorc_bt31,32_crorc_00,32_crorc_11 |
| cond | crorc cond r5c bt | !bb | DETECTED(62) | 64_crorc_01,64_crorc_hi,32_crorc_01 | 64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,32_crorc_01 |
| cond | crorc cond r5d ba | !bt | DETECTED(62) | 64_crorc_00,32_crorc_00 | 64_crorc_00,32_crorc_00 |
| cond | crorc identity body | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crorc_bt31,64_crorc_hi,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |
| decode | crorc dispatch -> instr(crand) | DETECTED(62) | 64_crorc_00,64_crorc_10,32_crorc_00,32_crorc_10 | 64_crorc_00,64_crorc_10,32_crorc_00,32_crorc_10 |
| decode | crorc dispatch -> instr(crandc) | DETECTED(62) | 64_crorc_00,64_crorc_11,edge_crorc_bt31,32_crorc_00,32_crorc_11 | 64_crorc_00,64_crorc_11,edge_crorc_bt31,32_crorc_00,32_crorc_11 |
| decode | crorc dispatch -> instr(creqv) | DETECTED(62) | 64_crorc_10,32_crorc_10 | 64_crorc_10,32_crorc_10 |
| decode | crorc dispatch -> instr(cror) | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_hi,32_crorc_00,32_crorc_01 | 64_crorc_00,64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,32_crorc_00,32_crorc_01 |
| decode | crorc dispatch -> instr(crnor) | DETECTED(62) | 64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_10,32_crorc_11 | 64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_10,32_crorc_11 |
| decode | crorc dispatch -> instr(crxor) | DETECTED(62) | 64_crorc_00,64_crorc_01,64_crorc_11,edge_crorc_bt31,64_crorc_hi,32_crorc_00,32_crorc_01,32_crorc_11 | 64_crorc_00,64_crorc_01,64_crorc_11,edge_crorc_bt31,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,32_crorc_00,32_crorc_01,32_crorc_11 |
| cond | c   both bodies identity | DETECTED(62) | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crandc_bt0,edge_crorc_bt31,64_crandc_hi,64_crorc_hi,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 | 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crandc_bt0,edge_crorc_bt31,64_crandc_hi,64_crorc_hi,64_crandc_order,64_crorc_bbmask,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11 |

MISSED BY THE 62 ROWS (25 cells):
  - crandc BB mask &5
  - crandc BB mask &9
  - crandc BB mask &11
  - crandc BB mask &13
  - crandc BB mask &17
  - crandc BB mask &19
  - crandc BB mask &21
  - crandc BB mask &23
  - crandc BB mask &25
  - crandc BB mask &27
  - crandc BB mask &29
  - crandc BB read <- BT index
  - crandc BA read mask &3
  - crandc BA read mask &7
  - crandc BB read mask &3
  - crandc BB read mask &7
  - crandc clear moved before the reads
  - crandc clear -> toggle (^=)
  - crandc set |= -> ^=
  - crorc BA mask &29
  - crorc BB mask &29
  - crorc BB read <- BT index
  - crorc clear moved before the reads
  - crorc clear -> toggle (^=)
  - crorc set |= -> ^=

EQUIVALENT (4 cells; proved, not merely unobserved):
  - crandc BA read mask &3: `ba & !bb' is a bitwise AND with !bb in {0,1}: only bit 0 of ba (= CR[BA]) can survive
  - crandc BA read mask &7: same: (ba & !bb) != 0  <=>  (ba & 1) && !bb
  - crandc set |= -> ^=: the clear at :2734 has just zeroed the bit, so ^= and |= set it alike
  - crorc set |= -> ^=: the clear at :2761 has just zeroed the bit, so ^= and |= set it alike

EXCLUDED (1 cells):
  - crandc clear -> toggle (^=): disclosed in the probe's clause (e)(5): every crandc row with result 0 pre-sets the inverse

STILL UNDETECTED BY THE 66 ROWS (0 cells):

NEW ROWS (4; single-instruction sessions shaped like the `hi' rows):
  64 crandc bbmask  crandc BT=16 BA=5 BB=31 seed=0xfffffffe want=1  CR[BT] pre-set EQUAL to the result (1)
  64 crandc order   crandc BT=9 BA=5 BB=9 seed=0x04400000 want=0  CR[BT] pre-set inverse (1)
  64 crorc bamask   crorc BT=16 BA=31 BB=5 seed=0xffff7ffe want=0  CR[BT] pre-set EQUAL to the result (0)
  64 crorc bbmask   crorc BT=31 BA=5 BB=31 seed=0x00000001 want=0  CR[BT] pre-set inverse (1)

WHY THESE FOUR AND NO FEWER.  A source-site row detects mask m iff CR[x & m] != CR[x] with the other operand decisive; with
x = 31 every m in 0..30 is an alias, so one row per site with CR[0..30] uniformly opposite to CR[31] closes the whole site.
crandc BB needs a = 1 and CR[0..30] = 1, CR[31] = 0 (want 1): pre-setting CR[BT] EQUAL to the result keeps the uniform seed
and makes the same row read CR[BT] = 1 != CR[BB] = 0 for the BB<-BT cell (an inverse pre-set hides BB<-BT on every row, as
codex B1-B2 show).  crandc clear-before-read needs BT == BB with b = 1 (want 0), a different seed: its own row (BT == BA is
invisible for crandc: a is forced to 1-want, and the early clear changes a only when b = 1, where the result is 0 either
way).  crorc BA needs b = 1, CR[0..30] = 1, CR[31] = 0 (want 0); pre-setting CR[BT] = 0 EQUAL to the result makes it read
CR[BT] = 0 != CR[BB] = 1 for BB<-BT, and incidentally sees the crorc toggle (a 0 result pre-set 0).  Its one blind alias
(m = 16 = BT) is red on `64 crorc 11' (BA 1 -> 0).  crorc BB needs a = 0, CR[0..30] = 0, CR[31] = 1 (want 0): with BT = BB = 31
the inverse pre-set IS CR[31] = 1, and the same row is the crorc clear-before-read pin.  The two crandc needs (want 1 uniform
ones; BT == BB with b = 1) and the two crorc needs (uniform ones; uniform zeros) are pairwise incompatible seeds, so four rows
is the minimum for single-instruction sessions.

OLD rows: 62.  NEW rows: 4 (N = 66).
