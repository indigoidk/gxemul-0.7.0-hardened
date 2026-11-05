# mvme187memcoob -- REPAIR PASS 3 measurement of the pass-3 seats' floor findings, 2026-11-04 local

Instrument: table_p3/probe118_p3.py (the in-tree 118-row probe; AST-equal to r3_20261105/table3/probe118_frozen.py).
Baseline: det_20261104/dev_mvme187.c.fix2 (== GXEMUL-SEC).  Driver: ../table_p3.run.sh (frozen copy of table_p3.sh; table 3's driver
without the HEAD and null legs), scratch clone /tmp/gxmemc4 under a clone-local sentinel; restored, cmp-clean against GXEMUL-SEC,
rebuilt fresh, sentinel cleared (../table_p3_run.log).  ORDER: ../PRETABLE_P3.out mtime 23:00:07.44 local; the driver's first output,
build_base.log, 23:00:38.82.

base 118/118.  ALL 34 VARIANTS 118/118 -- exactly as every seat derived: GPT-6 Astra's B1-B12 (27 cases) and glm-5.3's distinct
breaches (the direction ternary of breach 1, breach 2's byte-width gate on the default announce, breach 3's idata-gated served keeps,
breach 5's printed-value masks, and the conditional breach 6, the default announce gated on offset bit 3).  No variant reddened a row,
so a stale binary would read the same: every one of the 36 build logs shows dev_mvme187.c recompiled, and the driver's freshness test
(dev_mvme187.o newer than the source, gxemul newer than the object) passed for each.
So all 34 are MEASURED escapes of the 118-row detector.  Which of them lie inside the floor's bound is the adjudication's question.
