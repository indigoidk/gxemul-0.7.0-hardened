# qhslowifetch PASS 9 -- disposition (main loop, 2026-11-05)

Seats: GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_qhs_p9.txt; `CODEXP9QHS: 16 CELLS SWEPT 1 BREACHES 2 FALSE RECORDS
VERDICT:REPAIR`; source-derived).  Gemini 4 Argon x2 ANSWERED (gemini_p9_qhs.md: VALID; gemini_p9_qhs_r2.md: CLOSE, 0 broken) -- both
accepted the 8 x 9 grid as stated and engaged neither the visit count by ME nor codex's joint toggle; their agreement weighs nothing
against codex's derived cell.  glm-5.3 and grok-4.7: walled.

* B1 (L2 if measured): a toggle conditioned JOINTLY on ME and alignment (`(msr & ME) && pc != addr`, here of SRR0) cancels on the three
  unaligned ME-set read-ahead sessions; repair 9 gave one-entry sessions to the low-bit patterns but all of them ME-clear.  codex's
  16-cell table -- {low bits} x {ME} x {two-entry, one-entry} -- shows three cells with no session: one-entry ME-set at 01, 10, 11.  The
  class-closure rule asks for the whole table in one diff: repair 10 completes it.
* R1: the packet's "each passed all 153 rows" was the MAIN LOOP'S PACKET ERROR (a text substitution in mk_p9_qhs.py turned the record's
  correct 137 into 153); the shipped records say 137.  No shipped record to fix.
* R2 (L4): `T blr o2 srr0`'s note names R9_tog_srr0_1, which it cannot catch (low bits 10 vs 01); it owes its own named variant.
* Repair 10 (the same implementer): measure B1 and its isolated members first, the three one-entry ME-set sessions, R2, table 11.

*Corrected 2026-11-05 (main loop): this file's time-of-day stamps (removed: ~11:5xZ) were GUESSES that ran up to 3.5 hours AHEAD of the clock; the qhs landing-kit agent found them by checking against the files' own timestamps.  The file's own timestamps are the record: created 10:43Z, last written 10:58Z before this note (UTC).*
