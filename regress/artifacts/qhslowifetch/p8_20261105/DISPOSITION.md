# qhslowifetch PASS 8 -- disposition (main loop, 2026-11-05)

Seats: GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_qhs_p8.txt; `CODEXP8QHS: 8 CELLS SWEPT 1 BREACHES 1 FALSE RECORDS
VERDICT:REPAIR`; source-derived, nothing built or run).  Gemini 4 Argon x2: being sent at the time of writing.  glm-5.3 and grok-4.7:
walled (seat failures).

* B1 (L2 if measured): an MSR[ME] toggle conditioned on pc's low bits, inserted at the top of the failed-read block, CANCELS on every
  read-ahead session because each enters the block twice (read-ahead failure, then the real fetch); the eight cells' final-state rows
  cannot see an even number of visits.  The rows that can are ONE-ENTRY failures at each unaligned pattern; only `T blr` (11) exists.
  Inside the class (alignment x the state the block writes), so a floor cell -- a TIMING face of B3's shape the 8 x 9 grid did not hold.
* R1 (L4): "any transfer to bad: prints UNIMPLEMENTED" is false for a read-ahead transfer (cpu_dyntrans.c:1990-1991 returns silently
  while translation_readahead is set).
* Everything else held: the nine-channel re-check (exception text, read-failed text, prompt, LR; SRR1 disclosed), the disclosures G1-G3,
  the row and score counts.
* Repair 9 (the same implementer, resumed): measure B1 and its `== 2` form first; one-entry failure sessions for low bits 01 and 10 (and
  00 if none exists); R1; table 10; then pass 9.

LATE ADDENDUM: `p8_qhs` answered on a later send (gemini_p8_qhs.md: 0 broken) after repair 9 had started; `p8_qhs_r2` timed out.

*Corrected 2026-11-05 (main loop): this file's time-of-day stamps (removed: ~10:5xZ) were GUESSES that ran up to 3.5 hours AHEAD of the clock; the qhs landing-kit agent found them by checking against the files' own timestamps.  The file's own timestamps are the record: created 10:17Z, last written 10:47Z before this note (UTC).*
