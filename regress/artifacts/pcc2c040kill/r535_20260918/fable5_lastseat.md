FABLE_SEAT_ALIVE_20260918_535
model: claude-fable-5-1
CHECKPOINT.md line 1: "# CHECKPOINT -- 2026-09-18 14:2x   HEAD: 4653ecf records: the owner-ordered missing seats, all fired"

VERDICT: RATIFY-WITH-FINDINGS #535 for commit.

Basis: 8 landed seats + Opus. Measurement reproduced from artifacts (not re-run): r2_BASE 18/18, r2_A 17/18, r2_F 17/18, each red on exactly `c040 once mien`, all ending PCC2C040_DONE. Gate staged hunk pins 18 and lists 18 row names; both new rows read `td` (line 499, the 0x06 session), which is NOT rebound (t2/t3 are). Reclass is staged.

Q1 -- product CLOSED. The announce MIEN axis is a 2x2: {presence,count} x {MIEN-clear,MIEN-set} = `c040 says`/`c040 once` (clear) + `c040 says mien`/`c040 once mien` (set). Pass 1 found presence x MIEN; pass 2 measured count x MIEN (A/F print the announce 7-8x in the 0x06 session, 17/17 escape) and closed the last cell in-round. No open cell in {MIEN}x{latch} for the announce.
C/D/E dispositions right:
 - C (fatal->debug): a single-step channel gap. Every C040 write here is STEPPED and debug() has no early-out under step (only under free-run v<0 or -q), so the downgrade is invisible to a stepping probe. Disclose+file (`pcc2c040debugchan`) is correct -- it needs a new probe SHAPE, not a row; this is the single-step-cannot-observe class, legitimately clause-(e)/contract, not a floor breach.
 - D (latch bit C040->MASK_LEN): correctly FILED, not a floor breach, because the (d) DEPENDS-ON bound draws operand swaps only from fields the guarded BODY reads, and MASK_LEN is not one. The `c040 predirty` note was rightly narrowed L4 (it had claimed "a DIFFERENT warned bit" generically while pinning ONE, GENCTL_LEN).
 - E (pending-count conjunct): the C040 block tests no count -> clause (e). Right.

Q2 -- reclassification WITNESS->DETECTOR is correct AND required. By check_probe_wiring.py's own definition (:56-57) a DETECTOR is green once the defect is gone; since #512 shipped, every row asserts the post-fix state and the probe is green (18/18). Independently, a WITNESS is checked for the ABSENCE of a gate (:76) -- gating a witness is itself a wiring failure -- so wiring the probe into gate_arm.sh FORCES the reclass. Both routes agree.

Q3 -- no disposition is measurably wrong. The two soft spots, neither blocking:
 - D is the nearest to a floor cell. Its filed follow-up (`pcc2c040latchswap`) should be ranked as a REACHABLE hazard, not hypothetical: `d->warned |=` is a shared bitfield written at many sites (the #490 lesson), and MASK_LEN is set by ordinary guest MASK traffic -- a latch keyed on it would be pre-silenced by benign writes. The disposition (file) is defensible under the diff-closed bound; the RANKING should say so.
 - glm's "return-variant contradiction" is real as wording, not as fact: the probe's superseded note ("`return` variant killed 14/16") and dev_pcc2.c's HEAD comment ("`assert=0`->`return` at THIS line ... every shipped row passes") name TWO DIFFERENT return sites (the non-suppressing M_d1 return vs. the after-recalc return). Not a conflict; worth one disambiguating clause (L4 clarity).

Q4 / commit hygiene (the one thing to check before committing): the WORKING TREE carries another round's (#529) uncommitted additions in BOTH gate_arm.sh (28 crime lines) and check_probe_wiring.py MANIFEST. The #535 commit must stage ONLY its own hunks -- the pcc2 reclass line, the #533/#534/#535 artifact TOOL/WITNESS entries, and the 18-row gate section -- and must not sweep in #529. `check_probe_wiring.py` is `MM` (staged + further working-tree edits), so verify the index holds exactly #535's hunk.

Nothing here reaches DO NOT RATIFY: the L2 pass 2 found is closed with measurement, the product is closed, wiring and reclass are correct.
