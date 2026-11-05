# qhslowifetch -- REGRESS stage (main loop, 2026-11-05; written after 13:2xZ by `date -u`)

Seat: Mythos 5.1, run locally, holds the flagship hat for this stage because the round was released to Mythos on AUP grounds.  It
ANSWERED (REG_MYTHOS_local.md; `MYTHOSREGQHS: 262 CHECKS 0 FLOOR-BREACHES 2 RECORD-FINDINGS VERDICT:REGRESS-WITH-FINDINGS`).
The vacuity floor's clauses (a) through (e) are discharged, each with its SCORES.txt line.  All 262 gate checks fail on at least one
leg.  The pairing invariant's first-visit core and both DERIVED kills were re-derived from the code.  No row is vacuous by
construction: the three never-red rows (isi text, isi nonex, isi1 nonex) are premise controls.  Two record findings, both applied by
the main loop:
* R-A -- the gate comment still carried the second-visit pairing sentence that rec12 defeated and rec13 cut from the docstring; it was
  accepted at rec11 and never re-read.  REPLACED by the rec13 first-visit core (comment-only; r7_20261105/gate_ppc.sh.regrec.diff,
  copy .pre_regrec; `bash -n` clean; only those two lines changed, so the #575 block is untouched).
* R-B -- clause (e)'s per-variant catch lists are SUBSETS of table 12's red sets for variants whose rows grew at repairs 9-11.  One
  scoping sentence was added at the clause head: the rows named are those that first caught each variant, and the full red set is
  that variant's RED list in SCORES.txt (docstring-only; r7_20261105/ppc_ifetch_probe.py.regrec.diff; regrec_proof.out all six
  EQUAL, negative control DIFFERENT).
OWED AT LANDING, as the review lists them: the filings the contract names ("(filed)" ib zero-init; "filed separately" -- the branch
ignoring pc's low bits; "FILED pending X11", ROW 5's arm (d) producer) and the C file's #MMM/#QQQ/#PPP placeholders, plus the in-situ
gate 13 run on the 249-row block.  Recommended, not owed: one table run of the two self-referential variants, to upgrade the two
DERIVED kills to measured.
