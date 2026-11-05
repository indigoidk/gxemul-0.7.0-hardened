# #575 ppccrandcorc -- test-variant TABLE 1 (62 rows), 2026-11-05 07:4xZ (01:4x local)

Driver `../table1_575.run.sh` (frozen copy), WSL scratch clone /tmp/gx575t under a clone-local .MUTANT sentinel; restored, cmp-clean
against GXEMUL-SEC, rebuilt fresh, sentinel cleared (TABLE.log, last lines).  Instrument `probe62_frozen.py` == the in-tree probe after
apply_r575.py (cmp-identical to base62/probe62_run.py, which scored 62/62 on build/).  `../PRETABLE.out` was written before the driver
(the only older file here is the frozen probe, copied first); its predictions are EXACT and were COMPUTED by `../v575.py`, a simulator of
the probe's sessions.  Scores: SCORES.txt (red sets read off each run's FAIL rows; the probe prints no RED line).

* base 62/62, CONTROL=OK.  HEAD (impl_20261105/cpu_ppc_instr.c.pre575) 52/62, CONTROL=OK: exactly the ten predicted rows (64/32 crandc
  00, 01; 64/32 crorc 10, 11; edge crandc bt0; edge crorc bt31) -- the same ten as the 10-29 witness (witness_20261029/WITNESS_head.out).
* All 15 variants scored EXACTLY their predicted red sets (17 of 17 including base and HEAD):
  b1 crandc NAND restored, b2 crorc NOR restored -- 5 each; c identity bodies (the ruled null medium of the two handlers) -- 20;
  d1-d6 (operand complement moved, dropped, operator crossed) -- 5 each, the four the ruling listed per variant plus a hi row on d1-d4;
  m1-m4 (BA/BB mask & 7 and & 15) -- 1 each, the hi row of that handler ONLY (the owed rows' whole reason: 58/58 before them);
  t1, t2 (BT mask & 7) -- 13 each.
* Null media: /bin/true 5/62 CONTROL=FAIL; /bin/false 1/62 CONTROL=FAIL; an absent binary raises FileNotFoundError in the probe before
  any row and prints no sentinel (probe_null_absent.out) -- the gate's first check (the completion sentinel) reds it.
