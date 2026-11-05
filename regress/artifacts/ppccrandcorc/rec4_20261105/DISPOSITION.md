# #575 ppccrandcorc -- second reading of the five records corrections (main loop, 2026-11-05)

Seats: GPT-6 Astra (codex, `ultra`) ANSWERED: `CODEXREC4R575: 2 ACCEPTED 3 TO FIX VERDICT:FIX` (codex_codex_r575_rec4.txt; it raised the
five findings and was asked to be harder on their corrections).  Gemini 4 Argon: the first send's control check came back EMPTY
(gweb/rounds.log 03:23:21 local); the retry ANSWERED (gemini_rec4_r575.md, 03:25:16 local).  glm-5.3 / grok-4.7: walled.

Outcome: F3 and F5 ACCEPTED as corrected.  F1, F2 and F4 had each acquired a NEW universal claim in the correction itself -- the
correction-is-not-safer rule landing exactly as written: F1 "a mask above bit 4 imports the neighbouring field" (it MAY; 0x8000001f
decodes exactly) and "the identity in the simulator" (only when (m & 31) == 31); F2's note "only under the fix's decode" (read mask 0
also gives a = 0; the corrected PROBE note itself is true); F4 "with no appeal to the table rows" (crandc C = 3 needs `64 crandc 01`).
All qualified in place in ../r3_20261105/CLOSURE3.errata.md and RECORDS4_NOTE.md (pre-correction copies *.pre_2nd); the probe is
unchanged by this step.  None of it is a detector gap: the chain stays closed.  One phrase of the main loop's own qualification
("0x8000001f keeps only bit 31") was itself wrong and was corrected before this record (it adds bit 31 to the field's five bits).

ADDENDUM: Gemini's reading (gemini_rec4_r575.md) says ACCEPT on all five -- including F1's "masks beyond 5 bits import adjacent fields"
as stated, which codex refuted with a concrete counterexample (0x8000001f decodes exactly).  Gemini read the corrections BEFORE the
qualifications above and ratified the overbroad sentence as the packet gave it; codex's counterexamples are checkable from the code
and stand.  Count the arguments, not the seats: the qualified text is the record.

*Corrected 2026-11-05 (main loop): this file's time-of-day stamps (removed: ~09:5xZ) were GUESSES that ran up to 3.5 hours AHEAD of the clock; the qhs landing-kit agent found them by checking against the files' own timestamps.  The file's own timestamps are the record: created 09:27Z, last written 09:34Z before this note (UTC).*
