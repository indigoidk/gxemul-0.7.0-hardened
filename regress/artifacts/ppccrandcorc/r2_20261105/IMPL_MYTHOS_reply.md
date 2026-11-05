MYTHOSIMPLR575B

VERDICT: DONE. N = 66 (62 + 4 rows), base 66/66 CONTROL=OK on the fix, closure 239 cells with 0 undetected; table 2 inputs written, nothing built or run beyond the one base run.

**Base run** (`r2_20261105/base66/probe_base66.out`, build/gxemul; CLEARANCE.txt: cmp identical rc=0, binary newer rc=0):
`PPC_CRLOGIC_RESULT=66/66`, `PPC_CRLOGIC_CONTROL=OK`, `PPC_CRLOGIC_PROBE_DONE`, elapsed 0.2s. No row red on the fix, so no row was redesigned and no want fitted.

**Rows added (4)**, single-instruction sessions after the hi rows (`ppc_crlogic_probe.py` `pin_row`):
- `64 crandc bbmask` crandc 16,5,31 over 0xfffffffe, want 1, CR[16] pre-set EQUAL (every BB mask 0..30, BB read of CR[BT], BB read mask &3/&7).
- `64 crandc order` crandc 9,5,9 over bits 5,9, want 0, inverse pre-set (clear before reads).
- `64 crorc bamask` crorc 16,31,5 over 0xffff7ffe, want 0, CR[16] pre-set EQUAL (every BA mask but 16, which `64 crorc 11` covers; BB read of CR[BT]; also the crorc toggle).
- `64 crorc bbmask` crorc 31,5,31 over 0x00000001, want 0, inverse (every BB mask; clear before reads).

**Closure** (`r2_20261105/CLOSURE.md`, simulator `v575b.py`; `check62` reproduces table 1's 17 legs exactly). Denominator 239 = 186 field masks + 8 read-index substitutions + 8 read-mask widenings + 6 clear + 4 set + 15 condition + 12 dispatch. The 62 rows miss 25 (codex's nine and glm's crandc BB `& 3` among them; crandc BB masks miss 11, codex's sweep saw 3). With the 4 rows: 0 undetected. Cells left: 4 EQUIVALENT (crandc BA read mask &3/&7: `ba & !bb` is bitwise with !bb in {0,1}, so glm's BA-site cell is not a breach; set `|=`→`^=` after the clear, both handlers), 1 EXCLUDED (crandc toggle, clause (e)(5)); the crorc toggle is now red.

**Variants written** (27, `r2_20261105/variants/`, each one exact edit): table 1's 15 re-created + s1/s2 (BB reads CR[BT]), o1/o2 (early clear), m5-m9 (codex B5-B9), m10 (crandc BB &17), g1 (crandc BB read &3), g2 (crandc BA read &3, predicted 0 red = equivalent). `PRETABLE_2.out` holds the 66-row manifest and exact red sets, plus the four R5 bt-substitutions as PREDICTED ONLY (4,4,5,2 red).

**Records**: probe docstring fixed for F1, F2, F3, (e)(5); F7 touched nothing in the probe (fixed in v575b/PRETABLE_2 wording). `table1_20261105/PRETABLE.errata.md` (F4, F5, F7, R5 62-row sets 3,3,3,2) and `table1/VERDICT.errata.md` (F6) written; PRETABLE.out, SCORES.txt, VERDICT.md untouched.

**Gate**: #575 block names list = base order (66), RESULT=66/66, rows run/green 66, header 66-row. Diff vs backup: old lines 328, 333-334, 347, 349, 353-354 only (7 out, 9 in), `bash -n` clean.

**Files touched**: `regress/ppc_crlogic_probe.py`, `regress/gate_ppc.sh`; r2_20261105/{two .pre_r2 backups, v575b.py, CLOSURE.md, CLEARANCE.txt, PRETABLE_2.out, IMPL_NOTE.md, base66/, variants/}; the two errata files. No src edit, no build, no git, no table run.

**Not done / caveats**: table 2 not run (main loop). Equivalence of the 4 cells is by algebra plus 40000 random differential trials, not exhaustive. The crandc toggle remains undetected by design.
