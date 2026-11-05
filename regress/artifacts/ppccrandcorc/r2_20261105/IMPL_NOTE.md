# #575 ppccrandcorc -- ROUND 2 implementation note (2026-11-05, Mythos 5.1)

The fix (src/cpus/cpu_ppc_instr.c:2735 `if (ba & !bb)`, :2762 `if (ba | !bb)`) is untouched.  This round closes the detector
over an enumerated class of single edits to the two handlers, corrects the false records pass 2 found, and prepares table 2.
No table was run here (the main loop runs it); no source, build or git action was taken.

## Rows added (4): N = 62 -> 66

Single-instruction sessions shaped like the `hi' rows (ppc_crlogic_probe.py, `pin_row`, after the two hi rows):

    64 crandc bbmask   crandc BT=16 BA=5  BB=31  seed 0xfffffffe  want 1  CR[16] pre-set EQUAL (1)
    64 crandc order    crandc BT=9  BA=5  BB=9   seed 0x04400000  want 0  CR[9]  pre-set inverse (1)
    64 crorc bamask    crorc  BT=16 BA=31 BB=5   seed 0xffff7ffe  want 0  CR[16] pre-set EQUAL (0)
    64 crorc bbmask    crorc  BT=31 BA=5  BB=31  seed 0x00000001  want 0  CR[31] pre-set inverse (1)

A source at index 31 over a uniform CR[0..30] opposite to CR[31] makes every field mask m in 0..30 at that site read a flipped
input (31 & m = m).  Two rows pre-set CR[BT] EQUAL to the result because an inverse pre-set hides a BB read of CR[BT] on every
row (codex B1-B2); the crorc one incidentally sees the crorc toggle.  BT == BB with b = 1 pins read-before-clear (BT == BA is a
fixed point for both handlers).  CLOSURE.md, "WHY THESE FOUR AND NO FEWER", gives the seed-incompatibility argument.

## Closure (CLOSURE.md; simulator v575b.py, which reproduces table 1's 17 legs on the 62 rows exactly: `check62')

Denominator 239 cells = 186 field masks (m 0..30 at BT, BA, BB, both handlers) + 8 source-read index substitutions + 8 read-mask
widenings (& 3, & 7 at BA, BB) + 6 clear edits (early, deleted, toggle) + 4 set edits (deleted, ^=) + 15 condition edits (b, d-moved,
d-dropped, d-crossed, the four R5 bt-substitutions, identity per handler, c both identity) + 12 dispatch re-bindings.

    missed by the 62 rows:        25  (codex's nine and glm's crandc BB `& 3' among them; codex's {30,29,27,23,15} sweep saw 3 of the
                                       11 crandc BB mask misses: 5,9,11,13,17,19,21,23,25,27,29)
    closed by the 4 new rows:     20
    EQUIVALENT (proved):           4  crandc BA read mask & 3 / & 7 (`ba & !bb' is bitwise with !bb in {0,1}: only bit 0 of ba
                                       survives -- glm's BA-site cell is not a breach); crandc/crorc set `|=' -> `^=' (the clear
                                       has just zeroed the bit).  Each also survives 40000 random (cr,BT,BA,BB) differential trials.
    EXCLUDED:                      1  crandc clear -> toggle (disclosed in clause (e)(5)); the crorc toggle is now red on `64 crorc bamask'.
    undetected by the 66 rows:     0

## Base run (base66/probe_base66.out, build/gxemul; CLEARANCE.txt: cmp identical, binary newer than source)

    PPC_CRLOGIC_RESULT=66/66
    PPC_CRLOGIC_CONTROL=OK
    PPC_CRLOGIC_PROBE_DONE          (elapsed 0.2s; 66 rows ok, 0 FAIL)

No row was red on the fix, so no row's seed or want was re-derived; no want was fitted to the binary.

## Records corrected

- probe docstring/comments: F1 (clause (e)(3): index-31 inputs ARE rowed -- the hi row's BA31 and the three new index-31 sources;
  index-0 inputs are the tables' BA=0/BB=0), F2 (field-mask comment: `& 1' was already red on the old edge row; `& 15/7/3' were the
  58/58 escapes), F3 (`edge disasm' compares mnemonics only), (e)(5) (toggle: crandc only; hi/pin sessions have no `others' row).
  F7 touches nothing in the probe (its only "debugger" sentence, line 19, is true); fixed in v575b.py's and PRETABLE_2's wording.
- table1_20261105/PRETABLE.errata.md: F4 (absent binary: no CONTROL record, DONE=0), F5 (probe62_frozen.py is 86 ms older than
  PRETABLE.out), F7, and the four R5 bt-substitution predictions on the 62 rows (3, 3, 3, 2 red -- codex's sets).
- table1_20261105/table1/VERDICT.errata.md: F6 (the ruling listed four rows for d1-d4 and five for d5-d6).
- PRETABLE.out, SCORES.txt, VERDICT.md: not rewritten.

## Gate (gate_ppc.sh, #575 block only)

Names list = the base run's 66 names in order; RESULT=66/66; rows run/green 66; header "66-row"; the comment names the closure and
r2_20261105/.  `diff gate_ppc.sh.pre_r2 gate_ppc.sh`: old lines 328, 333-334, 347, 349, 353-354 (7 out, 9 in), all inside lines
328-356; `bash -n` clean.

## Table-2 inputs (written BEFORE any table; the main loop runs the table)

- variants/*.c: 27 = table 1's 15 re-created (identical edits, identical names) + 12 round-2 closures: s1/s2 (BB read of CR[BT];
  codex B1-B2), o1/o2 (clear before the reads; B3-B4, glm breach 1), m5-m9 (crandc BB & 29/27/23, crorc BA & 29, crorc BB & 29;
  B5-B9), m10 (crandc BB & 17, a miss codex's sweep lacked), g1 (crandc BB read `& 3', glm breach 2's real cell), g2 (crandc BA read
  `& 3': glm's other cell, predicted 0 red = EQUIVALENT).  Each is one exact edit of GXEMUL-SEC/src/cpus/cpu_ppc_instr.c (diff: one
  changed statement; o1/o2 move one statement, c_identity is table 1's two-handler edit).
- PRETABLE_2.out: the 66-row manifest and, per variant, the EXACT red set v575b.py computes; the four R5 bt-substitutions listed
  as PREDICTED ONLY (4, 4, 5, 2 red on 66 rows).  Expectation for table 2: base 66/66; HEAD 56/66 (the same ten); 26 variants red
  exactly as listed; g2 0 red (equivalence confirmed, not a detector failure).

## Files touched

    edited:  regress/ppc_crlogic_probe.py, regress/gate_ppc.sh (#575 block)
    written: r2_20261105/{ppc_crlogic_probe.py.pre_r2, gate_ppc.sh.pre_r2, v575b.py, CLOSURE.md, CLEARANCE.txt, PRETABLE_2.out,
             IMPL_NOTE.md, base66/probe66_run.py, base66/probe_base66.out, variants/*.c (27)}
             table1_20261105/PRETABLE.errata.md, table1_20261105/table1/VERDICT.errata.md
