# #575 ppccrandcorc -- test-variant TABLE 3 (repair 3: the full single-constant closure, 70 rows), 2026-11-05 ~08:43-08:59Z

Driver `../table3_575.run.sh` (frozen copy of table3_575.sh), WSL scratch clone /tmp/gx575t3 under a clone-local .MUTANT; restored,
cmp-clean against GXEMUL-SEC, rebuilt fresh, sentinel cleared (TABLE.log).  Instrument `probe70_frozen.py`, cmp-identical to the
in-tree probe and to `../base70/probe70_run.py` (70/70 on build/, CLEARANCE.txt part 1 and part 2 OK).  `../PRETABLE_3.out` (every
prediction EXACT, computed by `../v575c.py`, which first reproduces all 29 table-2 legs) is older than every file in this directory.
Scores: SCORES.txt (57 lines).

* base 70/70 CONTROL=OK; HEAD 60/70 on exactly the 10 predicted rows (the eight table rows where NAND/NOR differ from ANDC/ORC -- crandc 00
  and 01, crorc 10 and 11, each in the 64- and 32-bit sessions -- plus the two edge rows).  Null media: /bin/true 5/70 and /bin/false 1/70, each CONTROL=FAIL; an absent binary: the probe raises before any row (no
  RESULT line, CONTROL=none, DONE=0), as predicted.
* ALL 51 VARIANTS EXACTLY AS PREDICTED -- 53 of 53 predicted lines (base, HEAD, 51 variants) match their red sets row for row, 0
  misses: table 2's 27 re-created (26 red, g2 green as the proved equivalent); and the 24 repair-3 representatives -- crorc's BB read
  widened by one bit at k = 2, 15, 30, 31 and its BA read `& 0x8001` (red on `64 crorc bbread` / `baread`), crandc's set literal
  `1 + 2^k` at k = 7, 19, 30, 31 and crorc's at k = 26, 27 (red on `64 crandc setbits` / `64 crorc setbits`), one read mask of 0/2/4/6
  per site, the eight non-equivalent structural cells, and the crorc read swap green as the proved equivalent.
* The four R5 bt-substitutions are predictions only (PRETABLE_2.errata.md); they were not built, as the pass-1 ruling allowed.
