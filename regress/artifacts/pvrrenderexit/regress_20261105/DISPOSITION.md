# pvrrenderexit -- REGRESS stage (main loop, 2026-11-05)

Seat: Mythos 5.1, run locally, holds the flagship hat for this stage, which was released to Mythos on AUP grounds.  It ANSWERED
(REG_MYTHOS_local.md; `MYTHOSREGPVR: 32 CHECKS 0 FLOOR-BREACHES 5 RECORD-FINDINGS VERDICT:REGRESS-WITH-FINDINGS`).
* Clauses (a) through (f) are discharged with their SCORES lines.  B1_exit's red set equals HEAD's, at 78 rows, counted by session.
* The gate block's pins are sound, and the per-row anchor holds against sibling names.
* The 30 greens are each placed against the code.
* D2-F's binary64 claims were re-derived.
ONE CANDIDATE FLOOR CELL, LEFT UNSETTLED by the seat itself.  Swapping the guard's constant 0 for `fb_base` -- REG(FB_RENDER_ADDR1),
a value the guarded body reads at :715/:775, and which the probe leaves at 0 -- is predicted 148/148 green.  The same holds for the
texturedline palette_cfg analogue.  This is #462's shape, the operand-swap measured case, reached through a local assigned one line
above the guard.  CLOSURE3's swap list never named fb_base.  Whether clause (2)'s "fields the guarded BODY reads" covers a local
copied from d->reg is a RULE QUESTION, and the seat put it to the owner instead of ratifying it.
MEASURE FIRST: the round's implementer (Opus 5.5, resumed) builds the swaps and runs them on the 148 rows.  It also runs the
remedy -- one session pair with FB_RENDER_ADDR1 non-zero -- as a CANDIDATE, not added to the shipped probe.  The reading then goes to
the round's ruler, with the measurement, and is flagged to the owner.
RECORDS:
* R1, clause (c) stated as a prediction although it was measured;
* R3, 2.2 s should be 2.1 s;
* R5, the STDIN cap's "before running anything" should be "before running that session".
These three went to the implementer as docstring fixes.  R2, banking landing_20261105/, and R4, filing the register-coincidence
note next to F3, belong to the landing kit.  [Narrowed 2026-11-05, REG2 R-A: R4 is FILED in the probe's F3 note; the kit's F3 ledger row must carry it, and the kit must be re-pinned to 164 rows -- r7_20261105/R7_NOTE.md, OWED.]

## The ruling on the candidate: ../adj_reg_20261105/ADJ_MYTHOS_local.md -- `16 FLOOR 1 DEBT VERDICT:REPAIR-7`

READING (i).  A register value the guarded body reads through a local that is one assignment from a single `d->reg` read in the
same function is a "field the guarded BODY reads" for clause (2).  The decisive argument is (a): the textual reading defeats
itself.  `REG()` is textually `d->reg[...]`, the early-return guard dominates the local's own initialiser, so a `d->` grep already
lists the register.  Reading (ii) would grade one species two ways, depending on whether the body spelled the register with a local
-- the mark of a wrong discriminator.  The bound stays finite: a local that is the SPELLING of one field read is in; a local
computed from several inputs is a derived input graded by the body's tests on it; parameters and buffer elements stay out.
* 16 FLOOR cells: 4 guard sites x {fb_base} in simpleline, plus 4 x {fb_base, palette_cfg, PALETTE} in texturedline.  5 are
  measured green, 11 green by derivation.
* 1 DEBT: palette_cfg's switch partition, reached only for pixel format 6, SAMPLED.
* CLOSURE3's "int fields the body reads" omitted d->reg.
Rows owed in ONE diff: 16 rows in 8 sessions (148 -> 164), the measured pair plus three more pairs.  Records: CLOSURE3 erratum, the
contract, the F3 note, and pass 6's "0 FLOOR" narrowed to the exchange bodies.  Pass 8 verifies the enumeration.
OWNER-FLAGGED: the reading changes what every later round must enumerate as clause-(2) swap sources.  Repair 7 went to the
implementer (Opus 5.5, resumed).

## CORRECTION (2026-11-05, main loop; codex pass 8 and its reading, ../p8_20261105/ and ../recp8_20261105/)

The ruling section above says "16 FLOOR cells", puts PALETTE in the source set, and gives "5 measured, 11 derived".  The PALETTE
register at dev_pvr.c:842 is an ADDRESS (`&d->reg[PVRREG_PALETTE/4]`), and the palette loads at :843-844 are buffer elements indexed by
a VRAM byte, so the ruler's own bound excludes them.  The class is 12 FLOOR cells: fb_base at 4 guard sites in simpleline, and fb_base
and palette_cfg at 4 sites each in texturedline.  PL1t-PL4t are four measured checks OUTSIDE the class, and their rows stay.  The
ruling's own erratum is ../adj_reg_20261105/ (dated erratum file).  This section supersedes the count and source set above.


## FOLLOW-UP (REG2_MYTHOS_local.md; `MYTHOSREG2PVR: 23 CHECKS 0 FLOOR-BREACHES 1 RECORD-FINDINGS VERDICT:REGRESS-WITH-FINDINGS`)

THE CANDIDATE IS CLOSED, MEASURED.  All 12 FLOOR cells are red on the 164-row detector, each on exactly its predicted rows and on both
Z-states (table7/SCORES.txt:84-91, :149-152), and PL1t-PL4t are red at :153-156.  Their survival on the old 148 rows is measured
(meas7, meas7b).  The reading-(i) source set misses no register local: the seat grepped both rasterizers.  The pass-8 correction is
consistent across the whole erratum chain.  R1, R3 and R5 are fixed; R2 is owed; R4 is filed.
ONE RECORD (R-A): the landing kit was still pinned to the 148-row probe, and nothing recorded the re-pin as owed.  Now recorded as an
OWED item in r7_20261105/R7_NOTE.md (the FROZEN/PIN constants, the gate block, the dry-run replay over table7/, the F3 ledger text),
with the R4 line above narrowed.  pvr's review and records are CLOSED; it goes to the landing kit's phase 2 (re-pin, then build).
