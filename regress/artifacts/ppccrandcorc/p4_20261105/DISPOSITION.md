# #575 ppccrandcorc PASS 4 -- disposition (main loop, 2026-11-05)

Seats: codex GPT-6 Astra at `ultra` ANSWERED (codex_codex_r575_p4.txt; `CODEXP4R575: 453 CELLS SWEPT 0 BREACHES 5 FALSE RECORDS
VERDICT:REPAIR`; it read the packet, the handlers, the decoder, the probe, v575c.py, CLOSURE3, the gate block and the records, and
built and ran nothing).  Gemini 4 Argon x2 ANSWERED (gemini_p4_r575.md, gemini_p4_r575_r2.md): both CLOSE, each re-deriving the four
new rows' seeds and whole-CR wants; neither ended in the requested line (scored exit 1 by the sender; read in full).  glm-5.3 SEAT DOWN
(Ollama monthly limit); grok-4.7 SEAT FAILURE (402 billing wall).

## The chain: this is the closing pass

ZERO floor breaches survive, on a VALID pass: the diff was delivered (both probe hunks inlined), the roster's misses are named above,
and the zero carries its denominator -- codex's independent partition of the 453 cells (416 detected, 36 equivalent, 1 disclosed), with
the six constant sites (the four reads, the two set literals) proved over their whole 2^32 value space.  Under the stop condition the
repair chain CLOSES here.

## The five false records (L4 -- corrected in-round; records only, no row and no product change)

* F1 -- CLOSURE3's claim that its proof covers every FIELD-mask constant: the C code masks RAW shifted instruction words (`iword >> 21`
  carries the opcode above BT, and so on), so a mask with bits above bit 4 imports a neighbouring field (BT mask 63 gives BT + 32; BA
  mask 63 imports BT's low bit).  v575c.py masks already-extracted indices and cannot support that extrapolation.  Correct the scope:
  the enumerated field masks m = 0..30 are covered; raw-word masks reaching into neighbouring fields are outside the denominator and
  disclosed (their compiled behaviour, including out-of-range shift counts, is not modelled).
* F2 -- the `64 crorc baread` row's printed note says "a=0 for every mask": the baseline a is 0, and the mutations are caught exactly
  because they make it nonzero (read mask 3 gives a = 2; BA field mask 16 gives a = CR[16] = 1).
* F3 -- the docstring lists "the crandc toggle of (5)" under "EQUIVALENT, proved": it is not equivalent (crandc 31,0,1 over CR 0 must
  leave 0; the toggle gives 1); it is the DISCLOSED cell, as CLOSURE3 itself classifies it.
* F4 -- CLOSURE3:732, "C without bit 0 is red on every result-1 row": later instructions in a session can set the missed bit
  (crorc C = 2: `64 crorc 10` and `32 crorc 10` pass); other rows catch the mutant, and the setbits proof is the correct statement.
* F5 -- "WHY FOUR AND NO FEWER"'s claim that a multi-instruction session would cost more apparatus rows: under the whole-CR comparison,
  one session (seed 0x2; crandc 31,30,31; crorc 30,30,0; mfcr) catches both set-literal families, so three rows suffice; four is the
  minimum only under the single-instruction restriction the round chose.  The four measured rows stay.

The corrections go to the round's ruler and implementer (local Mythos 5.1, which wrote CLOSURE3 -- asked to be harder on its own claims):
dated errata beside CLOSURE3.md, the docstring and the row note corrected in place.  The baread note is a printed string, so the
in-tree probe will then differ from table 3's frozen instrument in TEXT ONLY; that difference is recorded rather than re-tabled, and
the gate's row patterns do not read note text.  A records correction earns a second reading (a correction is not safer than what it
corrects): one Gemini reading of the corrected sentences before landing.

ADDENDUM: two later re-sends of the same Gemini jobs (gemini_p4_r575_b.md: VALID AND CLOSES, 0 breaches on 453;
gemini_p4_r575_r2_b.md: UNSETTLED -- the per-cell sections were omitted from its packet for size).  Nothing beyond the record above.

*Corrected 2026-11-05 (main loop): this file's time-of-day stamps (removed: ~09:4xZ, ~10:1xZ) were GUESSES that ran up to 3.5 hours AHEAD of the clock; the qhs landing-kit agent found them by checking against the files' own timestamps.  The file's own timestamps are the record: created 09:14Z, last written 10:08Z before this note (UTC).*
