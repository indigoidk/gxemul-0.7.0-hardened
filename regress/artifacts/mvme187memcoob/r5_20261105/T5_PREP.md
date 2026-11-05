# mvme187memcoob -- test-variant TABLE 5 preparation (repair 5, 206 rows), 2026-11-05 local

model: claude-mythos-5-1 (Mythos 5.1; configured id, serving model may differ)
ruling implemented: p4_20261105/CONS_MYTHOS_local.md section 3 (the closed enumeration L) and section 4's order of work
("write the L-walking script, emit PRETABLE_5 ... then run table 5").  THE TABLE WAS NOT RUN HERE.

## Files written (all under r5_20261105/)
- memc_variants_5.py -- `list | apply <name> <in> <out> | pretable | predmap | check4 | stats | cells`.  Table 4's 112 edits
  (chained from r4_20261105/memc_variants_4.py, byte for byte) plus the L-walk.  `apply` refuses with MUTANT-TEXT-NOT-FOUND
  unless each anchor occurs exactly once; new-cell names are parsed back into their edit (no walk needed to apply).
- PRETABLE_5.out -- 9,699 lines, written 02:32:32 local, BEFORE any table5/ output (the frozen probe copy predates it).
- table5/probe206_frozen.py -- cmp-identical to regress/mvme187_memc_probe.py (md5 5d0cb614dc185067ee850d975a904062).
- table5_memc.sh -- adapted from r4_20261105/table4_memc.sh: WSL scratch clone /tmp/gxmemc6 of build/, clone-local .MUTANT
  sentinel, refuses without PRETABLE_5.out / the frozen probe / the HEAD source, legs base / HEAD / three null media, every
  variant, restore = cmp against GXEMUL-SEC + fresh rebuild before clearing the sentinel.  New against table 4: writes
  table5/PRED_MAP.txt (`predmap`) and table5/check4.out first, and scores every SCORES line PRED=match|atleast-ok|MISS|none
  against the prediction; variant transcripts stay in the clone and are copied out only on a MISS; TALLY.txt at the end.
  `bash -n table5_memc.sh` parses; LF line endings.
- T5_APPLY_CHECK.txt -- the apply check below.

## Variant count: 3,575 = 112 old + 3,463 new
APPLY CHECK (T5_APPLY_CHECK.txt): every one of the 3,575 names from `list` applied by the CLI to GXEMUL-SEC/src/devices/
dev_mvme187.c (md5 97e983872a72d159fbaaf54d8694ba49, == det_20261104/dev_mvme187.c.fix2) into /tmp/t5apply/ (not the project):
applied+changed=3575, unchanged=0, failed=0.  One variant per shape and position was diffed by eye: each statement lands at
its position with the right indentation (H before the switch, CI/CR/MT after the field read, MW after the write test, MB/DB
after the latch set, ME/DA before `break`, DT before the default test, TL before the read-back; GS/TA/TO/NV/ND edit the
existing statement).

## The denominator (section 3, walked cell by cell)
Class L: one inserted `if (G) T op V;` at a position, or one gate added to an existing latch set / latch test / notice predicate.
- positions: the ruling's ten (H, CI, CR, MT, MW, MB, DT, DB, DA, TL) plus ME (memconf arm end, after the write block --
  the memconf twin of DA, added as a superset; T2_mlatch_hoist lives there).
- latch targets M, D x ops {= 1, = 0, = idata, ^= 1, ^= idata}; keep targets chipid, chiprev, memconf x ops {=, |=, ^=, &=} idata.
- gates: all 81 conjunctions of literals over {W, C, M, D} incl. always ("ANY boolean function" of the ruling, restricted to
  conjunctions: disjunctions, two-bit masks, bit-with-predicate joints and len are the ruling's disclosed OUT-cells, not walked);
  64 single idata-bit tests (b = 0..31, set/clear) at every position (the ruling places none at CI/CR; walked there as a
  superset); 16 single offset-bit tests (m = 0..7, set/clear) at H, DT, DB, DA, TL.
- gated existing statements: GS (the set at :116/:135 gated), TA/TO (the test at :112/:127 made `!x && G` / `!x || G`),
  NV/ND (the value guard at :132 and direction ternary at :129 made `W && G`).
Cells walked: 37,974 = latch statements 16,750 + keep statements 20,100 + gated sets/tests 912 + gated notice predicates 212.
- VACUOUS 6,676: semantically no-op at the position for every access the function can see there (gate unsatisfiable, e.g. `M`
  inside the memconf latch body; or statement without effect, e.g. `M = 1` after the set, `F |= idata` under a read-only gate).
  Not mutants; not built.
- Non-vacuous 31,298:
  - predicted RED 26,999 cells in 2,686 distinct observable traces -> 2,798 BUILT (one per trace + 112 promoted so every
    statement and every gate form compiles at least once); the other 24,201 are EQUIV (identical notices and read-back values
    on every probe access as their representative; listed under it in PRETABLE_5).
  - predicted GREEN 4,299 cells in 1,600 (statement, deviation-set) groups -> 665 BUILT: one per group for UNFIRED (106) and
    UNOBSERVED (411), one per statement for NOCHANGE (148 built for 1,083 groups: fired but changed nothing -- the ruling's
    disclosed probe-equivalent `^= idata` / `= idata` into a set latch and kin).
Cells NOT made into a variant: the 6,676 vacuous (not mutants), the 24,201 RED-EQUIV and 935 GREEN-NOCHANGE cells (each
measured by its built representative; the walk lists them as such, per the ruling's D4 "equivalent cells are listed as such").

## How the predictions were made, and the calibration
Every `exact` prediction is the frozen probe's own verdict: the probe is executed with subprocess.run replaced by a fake gxemul
that decodes its m88k words and runs them against DEVICE_ACCESS(mvme187_memc) as written in the fix with the cell's statement
inserted (memc_variants_5.py, class Device / Fake).  Checks:
- base: the fake's 206-row "got" column equals base206/probe_base206.out column for column; red set empty.
- `check4`: table 4's frozen 148-row instrument replayed through the model for base, HEAD, the three null media, B1/B2 and the
  53 table-4 variants the model expresses: 60 compared, 0 mismatches against table4/SCORES.txt.
- old variants the model does not express (57: exits/faults/indexed read/masks/casts/swaps/widths) carry table 4's measured
  red set as `at least`, minus the ten rows repair 5 re-wanted (R5_lines, R5_pc, R7_pc, R9_lines, R9_pc, R12_pc, R13_lines,
  R13_pc, R15_lines, R15_pc).  The 55 expressed ones get exact 206-row predictions beside their table-4 measured set.
- legs (exact): base 206/206; HEAD 29/206 SYMPTOM=PRESENT; null media 27/206, 4/206, 5/206, each CONTROL=FAIL.

## FINDING: the 206 rows do NOT close L under this denominator (predicted survivors, to be measured by the table)
UNFIRED (106 groups; the probe makes no access that satisfies the gate at that position):
- 48 groups OUTSIDE the ruling's alphabet: idata bits 8..31 set at CI/CR -- every served store the probe makes is a byte store,
  so no word store to +0x00/+0x04/+0x100/+0x104 exists.  Walked as a superset; a word store to chipid/chiprev would close them.
- 58 groups INSIDE the denominator (conjunctions over the four tests):
  - memconf store, controller 0, M set, D clear (W.nC.M.nD at MT/MW; nC.M.nD at MW; TO_M forms): 20+20+20+4 statements.
    PHASE 10 HAS NO CONTROLLER-0 MEMCONF STORE: R16's phase-10 memconf store is the controller-1 ST_B(0,3,0x108); R3's,
    R7's and R9's second controller-0 stores all come after a default access (phase 11).
  - default store, controller 1, both latches set (W.C.M.D at DT; TO_D W.C.M / W.C.M.D): 20+2 statements.  PHASE 11 HAS NO
    CONTROLLER-1 DEFAULT STORE: R16's phase-11 default accesses are LD 0x83, ST_W 0x1c (controller 0), LD 0x10c, LD 0x1c.
UNOBSERVED (411 groups; the statement fired and changed a latch or field, and no later access read it back), chiefly:
- keeps mis-targeted into chipid from the chiprev arm (CR) gated on D (and joints): chiprev accesses with D set are never
  followed by a chipid read (R5, R10, R13, R14 read chipid before chiprev; R16 phase 11 and R17 read chipid before the chiprev
  stores and never again).
- keeps into chipid/chiprev at the first memconf store (MB) gated on D, C, or joints: R5, R7, R13, R17 make their first memconf
  store with D set (and R7/R9 through controller 1) and never read chipid or chiprev afterwards.
- keeps into chipid/chiprev at the default arm (DT/DB/DA) gated on M.D or joints: phase-11 default accesses (R8's twelve
  reads, R12's and R16's tails) are never followed by a chipid/chiprev read.
- `M ^= idata` at DT/DA/H/TL under ib0c/ib2c/ib5c/ib7c: R10's 0x5a default store sets M by parity and no memconf store follows;
  under ob2s / ob3c: R17's two word stores at +0x1c/+0x11c toggle twice and cancel (the ruling disclosed even-count toggles
  only for two-predicate gates).
- `D = 0` / `D ^= 1` at DB under W.nC.M: R15's first default access (ST_W 0x1c with M set) is its last default access.
- chiprev &= at H/MT/MW under W.C.M.D and kin: R15's controller-1 store with both latches set is followed only by a memconf read.
The exact survivor list (kind, position, gate, statements) is the SURVIVOR SUMMARY at the end of PRETABLE_5.out; each built
GREEN cell is listed with "exact: none -- UNFIRED|UNOBSERVED|NOCHANGE".  The ruling's closure condition (section 3: every access
kind in every phase, with a memconf store, a default access AND served read-backs after each) is therefore not met by the row
list of section 4; the table will measure how many of the 517 UNFIRED/UNOBSERVED representatives in fact survive (predicted:
all), which the next ruling must turn into rows (a controller-0 memconf store in phase 10, a controller-1 default store in
phase 11, chipid/chiprev read-backs at the end of R5, R7, R9, R13, R15, R17 and after R16's phase-11 tail, a memconf store after
R10's 0x5a store, an odd count of word default stores in R17).

## Run-time note for the main loop
Table 4 ran 117 legs in 147 s (1.26 s each).  Table 5 runs 3,580 legs: expect roughly 75-90 minutes.  `python3 $V list` and
`predmap` each walk the class once (about 45-75 s).  PRED_MAP.txt and SCORES.txt's PRED= column make the verdict mechanical:
PRED=MISS lines are the only ones that need reading.
