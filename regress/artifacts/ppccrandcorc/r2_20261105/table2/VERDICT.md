# #575 ppccrandcorc -- test-variant TABLE 2 (repair 2: 66 rows, the class closure), 2026-11-05 ~08:1xZ (02:1x local)

Driver `../table2_575.run.sh` (frozen copy), WSL scratch clone /tmp/gx575t2 under a clone-local .MUTANT sentinel; restored, cmp-clean
against GXEMUL-SEC, rebuilt fresh, sentinel cleared (TABLE.log).  Instrument `probe66_frozen.py` == the in-tree probe after repair 2
(cmp-identical to base66/probe66_run.py, 66/66 on build/).  `../PRETABLE_2.out` (02:08:00 local) predates every file in this directory
(the earliest, MD5.txt, 02:10:46); its predictions were computed by `../v575b.py`, the extended simulator whose 62-row re-derivation
reproduces table 1's 17 legs, over the closure of `../CLOSURE.md` (239 cells).  Scores: SCORES.txt (red sets read off the FAIL rows).

* base 66/66, CONTROL=OK.  HEAD 56/66: the ten DISC rows, as predicted.
* All 27 variants scored EXACTLY their predicted red sets (29 of 29 runs with base and HEAD): 26 red; g2 (crandc's BA read mask
  widened to `& 3`) green, as PRETABLE_2 predicted -- proved EQUIVALENT there (with `!bb` in {0,1}, `ba & !bb` reads only ba's low bit).
  The new variants are the pass-2 classes: s1/s2 (BB reads CR[BT]), o1/o2 (the clear moved before the source reads), m5-m10 (single-
  bit field masks, codex's B5-B9 and one more), g1 (crandc's BB read mask `& 3`) and the rest of CLOSURE.md's cell classes.
* Null media: /bin/true 5/66 CONTROL=FAIL; /bin/false 1/66 CONTROL=FAIL; an absent binary stops the probe before any row with no
  sentinel (the gate's first check reds it).
