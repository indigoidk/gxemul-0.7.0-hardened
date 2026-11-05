# #575 ppccrandcorc PASS 3 -- disposition (main loop, 2026-11-05)

Seats: codex GPT-6 Astra at `ultra` ANSWERED (codex_codex_r575_p3.txt; `CODEXP3R575: 447 CELLS SWEPT 54 BREACHES 7 FALSE RECORDS
VERDICT:REPAIR`; read the packet, CLOSURE.md and source; built and ran nothing).  Gemini 4 Argon x2 ANSWERED (gweb/jobs_20261105_rounds/
p3_r575 and p3_r575_r2: both `VERDICT: CLOSE`, 0 BROKEN) -- they confirmed the four EQUIVALENT cells by derivation and accepted the
239-cell enumeration AS THE PACKET STATED IT; neither re-derived the vocabulary, so their agreement on the brief's own premise is no
evidence (carrier: unanimity on a brief-supplied fact is worth nothing).  glm-5.3 SEAT DOWN (Ollama monthly limit); grok-4.7 SEAT
FAILURE (402 billing wall).

## codex's findings (DERIVED, not measured -- checkable by the round's own simulator)

The 239-cell vocabulary did not exhaust the single-constant edits at two sites it had already put in scope:
* B1 -- crorc's BB read `& 1` -> `& (1 | 1<<k)`, k = 2..30: 29 survivors (the only a=0, b=0 crorc row reads BB=2, whose shifted word
  has no set bit above bit 1).  B2 -- crorc's BA read `& 1` -> `& 0x8001`: 1 survivor.
* B3 -- crandc's set literal `1` -> `1 + 2^k` for 22 values of k; B4 -- crorc's for k = 26, 27: extra SET bits outside the destination,
  invisible because the sessions that would show them check only the destination bit or shift the extra bit out.
* R1-R7: the uniform-seed claim for `crorc bamask` (CR[16] is 0 in its seed); "four rows and no fewer" (one crandc row, `crandc
  16,16,31` seed 0xfffffffe, would cover both crandc additions); the `&7` value in the crandc bbmask comment (6, not 2); table 2 calling
  m5-m10 single-bit masks (m10 removes three bits); table 2's "MD5.txt is the earliest file" (PRETABLE_2.out predates it, but probe66_
  frozen.py and the .fix575 are earlier than MD5.txt); PRETABLE_2's control seed 0 (the probe's CTL_CR is 0x12345678); gate_ppc.sh's
  "every destination pre-set to the INVERSE" (the new rows use equal presets).

## Disposition (standing rules; no new ruling is needed)

* The READ-MASK class was graded a floor breach at pass 2 (glm's `& 1` -> `& 3`) and repair 2's closure put it, and the set
  statement, in its own enumeration -- with a vocabulary ({&3, &7}; |= -> ^=) narrower than the class.  Pass 3 found the same classes
  open.  So, if the simulator confirms B1-B4, they are floor breaches (L2) and repair 3 completes the closure over the FULL
  single-constant space at those sites (codex's 447-cell denominator is the starting point), adding the fewest rows that detect every
  non-equivalent cell, and writes into the contract which cells are covered and which are deliberately not.
* R1-R7 are wrong records (L4): corrected in place in the probe/gate, and as dated errata beside the table-2 files and CLOSURE.md
  (never rewriting a measurement record).  R2 corrects the minimality CLAIM; the four measured rows stay.
* Repair 3 is #575's, an AUP-released item: implemented by a LOCAL Mythos 5.1 run (as repair 2 was).  It writes the gate_ppc.sh change
  as a block file for the main loop to apply, because the qhs repair-7 implementer is editing gate_ppc.sh's qhs block in the same window.

*Corrected 2026-11-05 (main loop): this file's time-of-day stamps (removed: ~10:0xZ) were GUESSES that ran up to 3.5 hours AHEAD of the clock; the qhs landing-kit agent found them by checking against the files' own timestamps.  The file's own timestamps are the record: created 08:32Z, last written 08:32Z before this note (UTC).*
