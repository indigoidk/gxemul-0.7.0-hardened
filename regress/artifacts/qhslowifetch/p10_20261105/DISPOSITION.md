# qhslowifetch PASS 10 -- disposition (main loop, 2026-11-05)

Seats: GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_qhs_p10.txt; `CODEXP10QHS: 16 CELLS SWEPT 1 BREACHES 2 FALSE RECORDS
VERDICT:REPAIR`; source-derived).  Gemini 4 Argon x2: SEAT FAILURES so far -- the sender's control check timed out (05:07:37 local),
one retry after a 30-minute pause is scheduled.  glm-5.3 and grok-4.7: walled.

* B1 (L2 if measured): a toggle conditioned on the FULL pc/address (`(pc & ~0xb) != addr`, of SRR0) cancels on every two-visit read-ahead
  session (pcs 0xfec00008..b, masked to 0xfec00000) and never fires on the one-entry sessions (pcs 0x02040000..7, masked to addr).
  The repair-10 grid paired the cells by low bits and ME; the pairs still differed in the full pc, which the block reads.  The same
  family for the third time (passes 8, 9, 10 -- low bits, ME, full address): the closure owed is STRUCTURAL -- a one-entry partner at the
  SAME full pc and ME for each read-ahead cell, so a pair differs only in the visit count, and a condition on translation_readahead
  (the one state that differs) fires on one visit and cannot cancel.  Repair 11 builds that, with the pairing invariant in the contract.
* R1 (L4): the docstring's universal "any condition both visits share" claim.
* R2: the packet's "passed all 177 rows" was the MAIN LOOP'S PACKET ERROR again (the same text substitution in the packet builder as
  pass 9's; the record says 153).  Builder lesson: never blanket-replace a row count in packet text -- the question and the history
  share the number.

*Corrected 2026-11-05 (main loop): this file's time-of-day stamps (removed: ~12:2xZ) were GUESSES that ran up to 3.5 hours AHEAD of the clock; the qhs landing-kit agent found them by checking against the files' own timestamps.  The file's own timestamps are the record: created 11:09Z, last written 11:09Z before this note (UTC).*
