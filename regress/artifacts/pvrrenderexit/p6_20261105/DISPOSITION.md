# pvrrenderexit PASS 6 -- disposition (main loop, 2026-11-05; written 13:0xZ by `date -u`)

Seats: GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_pvr_p6.txt; `CODEXP6PVR: 108 CELLS SWEPT 20 BREACHES 1 FALSE RECORDS
VERDICT:REPAIR`; source-derived, nothing executed).  Gemini 4 Argon: SEAT FAILURE -- the web route is down (control errors since
~11:07Z).  glm-5.3 and grok-4.7: walled.

* Codex confirmed the eight new rows and the 24-cell deletion closure, each cell held by its named row and twin.  It also confirmed
  the corrections repair 5 made to the ruling, with full arithmetic.
* The 20 are OPERAND SUBSTITUTIONS inside the exchange bodies (right-hand side -> d->xsize / ysize / zwrite_disabled /
  bytes_per_pixel).  12 are depth and 8 are RGB, and they survive by VALUE COINCIDENCE with the probe's chosen values.  Detecting
  sets are given.
* R3: the corrected D2-F "every 0 < c <= 1 begins at x1 + 1" is false under binary64 rounding (-1 + 2^-54 == -1).
* Two FP-sensitive candidates (u1 -> ysize; x1 + 2^-54) are reported outside the count.
THIS IS THE THIRD CONSECUTIVE PASS TO FIND A NEW EDIT SHAPE IN THE SAME TWO EXCHANGE BODIES: deletions (p4/p5), compounds (p5),
operand substitutions (p6).  So the question sent to the ruler is not only how to grade the 20.  It must also enumerate EVERY
single-site edit shape on the exchange bodies, once, each graded FLOOR or DEBT, so that pass 7 verifies an enumeration instead of
hunting for a fourth shape.  The main loop proposes (does not rule) that the 20 are DEBT: a body-assignment operand swap is a
data-flow perturbation like the compounds, and clause (2) governs the guard's operands.  The prompt also gives the two other
readings (clause (2) read literally; null-plus-constant by analogy with the FLOOR deletions).  Sent to the ruler (local Mythos 5.1,
prompt mythos_local/prompt_pvr_adj6.md) -> ../adj_p6_20261105/.

## The ruling: ../adj_p6_20261105/ADJ_MYTHOS_local.md -- `0 FLOOR 29 DEBT 1 RECORDS UPHELD VERDICT:CLOSE-AFTER-RECORDS`

* The 20 are DEBT by reading (i), the main loop's proposal.  Clause (2)'s operand swap is defined on the GUARD's operand, and the
  exchange bodies entered the bound as P4's effect, holding deletion cells only.  Reading (ii) would admit every assignment the body
  reads -- the transitive chase the bound refuses.  Reading (iii) fails because `z2 = B` is a value-specific bug, not a null, and the
  body never tests z == 2.0 as a case.
* THE ENUMERATION THAT ENDS THE CHAIN, section 2: every single-site edit shape on the 27 exchange statements, graded.
  - (a) deletion: FLOOR, closed, 24 cells.
  - (b) compound operator: 108 forms, not 80 -- the 16 x compounds were never screened, and all are caught.
  - (c) operand to a body-read field: 108 cells, not codex's 84 -- codex omitted UV.  21 survive, 8 are FP-undetermined.
  - (d) operand to another local, and (e) to a constant: open families, disclosed.
  - (f) sign: 27 forms, 8 survive.  The UV remedy set is amended.
  - (g) reorder and (h) swapped target: held.
  - (i) type change: `int tmpf` at :664 survives.
  29 DEBT cells are named, with remedy sets.
* The probe-design note goes on record: the probe's standard depth 2.0 equals d->bytes_per_pixel.
* R3 UPHELD, the ruler's own: the start family is exhausted only down to the double's resolution.  c = 2^-54 is SAMPLED, with
  codex's (B) witness; the ruler corrected codex's want to 0x5540.
Records only: no rows, no product change, no pass 12 owed for floor material.  Pass 7 verifies section 2 and the records.  The
records went to the round's implementer (Opus 5.5, resumed) with a COMPACT instruction: one line per shape, citing the ruling for
each derivation.
