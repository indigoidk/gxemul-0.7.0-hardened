# mvme187memcoob -- REGRESS stage (main loop, 2026-11-05)

Seat: Mythos 5.1, run locally, holds the flagship hat for this stage because the round was released to Mythos on AUP grounds, as
#575's was.  It ANSWERED (REG_MYTHOS_local.md; `MYTHOSREGMEMC: 20 CHECKS 2 FLOOR-BREACHES 9 RECORD-FINDINGS VERDICT:REGRESS-BREACH`).
It had no Bash, so every count it gives is read from an artifact.

THE BREACH.  Eight variants classed NOCHANGE in PRETABLE_5 write a repair path's OWN latch under that path's own predicates, or
under no gate: L_MB_M_xori_any, L_ME_M_xori_any, L_DB_D_xori_any, L_DA_D_xori_any, L_MT_M_xori_M, L_MW_M_xori_M, L_DT_D_xori_D
and L_DT_D_idat_W.D.  All eight are MEASURED green.  Checked by the main loop: SCORES.txt:2916-2919, :2931, :2936-2937 and :2990
each read 206/206, and PRETABLE_5.out classes them NOCHANGE (:7789, :7996, ...).  The pass-5 ruling scanned the 517
UNFIRED/UNOBSERVED by family and treated the 148 NOCHANGE as no-ops.  Its own test -- "whether the gate's predicates and the target
are the path's own", which it applied to NB4 -- makes these eight floor cells.  None is a semantic no-op: a store of 0x01 XORs a
set latch to zero, and the probe never stores one.  The reviewer proposes ONE session, R18 (0x01, 0x01, 0x00 to +0x18 and +0x08,
with loads), predicted by REASONING to red all eight.

DISPOSITION: the classification follows the ruling of record's own test, as the reviewer applied it, so it is not re-argued here;
the measurement settles it.  REPAIR 6 is in-round, because the detector has not shipped (L1/L2):
  - R18, after measuring that the eight are green on the 206 rows in a fresh clone;
  - PRETABLE_6 written first;
  - table 6 over the eight, the 665 green representatives and the legs;
  - the nine record findings, with deletion preferred over new explanation;
  - the gate block as a patch.
It owes its own pass 2.  An Opus 5.5 implementer runs it.
OWNER-FLAGGED: the reviewer names the one ruling that would change this.  If codex's narrower bound were adopted -- an insertion is
in bound only if it restores a removed operation or nulls the repair directly -- the eight would be debt and the verdict
REGRESS-WITH-FINDINGS.  The ruling of record rejected that bound.  Record item 6 (bank the kit's dry-run, identity and staged-diff
files in regress/artifacts/ before the commit) goes to the landing-kit agent.

*Corrected 2026-11-05 (main loop): this file's time-of-day stamps (removed: ~16:0xZ) were GUESSES that ran up to 3.5 hours AHEAD of the clock; the qhs landing-kit agent found them by checking against the files' own timestamps.  The file's own timestamps are the record: created 12:28Z, last written 12:28Z before this note (UTC).*

## FOLLOW-UP (REG2_MYTHOS_local.md; `MYTHOSREG2MEMC: 20 CHECKS 0 FLOOR-BREACHES 4 RECORD-FINDINGS VERDICT:REGRESS-WITH-FINDINGS`)

THE BREACH IS CLOSED, MEASURED.  The eight each score 212/213, red on R18_lines (table6/SCORES.txt:9-16), and were 206/206 in a fresh
clone before R18.  The shipped probe is AST-equal to the measured instrument.  The 641 survivors hold no own-arm, own-target cell,
which agrees with codex's 693-cell enumeration.  All nine first-round findings were dispositioned correctly; the retarget of finding
4 and finding 8's measured form are both upheld.  Four record items remain:
* A: finding 6, banking landing_20261105/, is still open and belongs to the landing-kit agent, which is doing it in phase 2.
* B: family (2)'s "or which lands on a set latch".
* C: family (6) should exclude the red representatives' GROUPS.
* D: IMPL_NOTE's "MEASURED" for a synthetic replay.
B, C and D went to the repair-6 implementer (Opus 5.5, resumed).  For B it must check with the walker whether any UNOBSERVED
representative still relies on the clause, because the review's example, L_CI_D_xori_D, is classed NOCHANGE (PRETABLE_5.out:7816)
and so belongs to family (6), not (2).  The in-situ 223-check gate run stays owed at landing.
