# pvrrenderexit PASS 5 -- disposition (main loop, 2026-11-05)

Seats: GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_pvr_p5.txt; `CODEXP5PVR: 181 CELLS SWEPT 27 BREACHES 2 FALSE RECORDS
VERDICT:REPAIR`; source-derived, nothing executed).  Gemini 4 Argon: SEAT FAILURE -- the web route is down (control errors since
~11:07Z).  glm-5.3 and grok-4.7: walled.

* The 27 are SWAP-BODY edits that pass all 140 rows by derivation.  One is a DELETION: simpleline's `tmpf = z1;`, the only survivor
  of six temporary-assignment deletions.  The other 26 are COMPOUND-ASSIGNMENT substitutions: 11 depth, 9 RGB, 6 UV.  They are
  hidden by zero operands and saturation.  Codex gives a detecting set per attribute.
* R1: B2t is not EQUIVALENT -- (int)(x1 + 0.5) != x1 for negative x1 (truncation toward zero), and attributes advance on clipped
  iterations.  Codex gives a witness triangle.  This refutes D2-F's "texturedline's fractional moves are EQUIVALENT" as stated.
* R2: "a red COVER8 would hide the u2 case" is false.

PROPOSED (not ruled):
- The deletion is FLOOR, the same class as B4-B10, found again, so repair 5 owes the CLASS CLOSURE of exchange-statement deletions.
- The compound substitutions are clause-(e) DEBT: not a null, not a predicate weakening, not a body-read operand swap.
- B2t is FLOOR under D2-F; D2-F's equivalence wording is corrected.
- R1 and R2 are upheld.
Sent to the ruler (local Mythos 5.1, prompt mythos_local/prompt_pvr_adj5.md) -> ../adj_p5_20261105/.

## The ruling (2026-11-05): ../adj_p5_20261105/ADJ_MYTHOS_local.md -- `3 FLOOR 26 DEBT 2 RECORDS UPHELD VERDICT:REPAIR-5`

* (a) STANDS, with two refinements.  The `tmpf = z1` deletion is FLOOR, and the class closure is owed: 27 swap statements, 3 of them
  undeletable declarations, so 24 deletion cells.  1 is OPEN, 7 are measured (B4-B10), 16 are derived caught.  Row `ramp8hi r end` and
  its Z-off twin.
* (b) STANDS: the compound substitutions are clause-(e) DEBT.  An arithmetic perturbation of an exchanged value is not a DEPENDS-ON
  edit shape, and its observability needs values the body never tests as a case.  The disclosure sentence is in the ruling, section 2.
  The 11 depth members are predicted red by `ramp8hi`.
* (c) WRONG in three places.  B2t is a WHOLE-pixel move at a NEGATIVE start, not a half-pixel move.  The other texturedline
  fractional COMPARE moves stay EQUIVALENT for every integer end, negative included.  And the truncation reaches simpleline too: N1s
  (`int x = x1 + 0.25`) is a new FLOOR cell, and the ruler's own D2-F sentence putting the start family in SAMPLED is R3.
  Rows: `texnegx n start` and `negx n start`, each with a Z-off twin.
* (d) STANDS: R2 is corrected, with the ruler's own pass-4 line named as its source.
Repair 5 is ONE diff: measure first; 6 rows (140 -> 146; two optional left-end rows only on a measured delta); the 24-cell closure
in the contract; the corrected D2-F; errata; table 5.  It went to the round's implementer (Opus 5.5, resumed).

*Corrected 2026-11-05 (main loop): this file's time-of-day stamps (removed: ~14:4xZ, ~15:0xZ) were GUESSES that ran up to 3.5 hours AHEAD of the clock; the qhs landing-kit agent found them by checking against the files' own timestamps.  The file's own timestamps are the record: created 11:58Z, last written 12:07Z before this note (UTC).*
