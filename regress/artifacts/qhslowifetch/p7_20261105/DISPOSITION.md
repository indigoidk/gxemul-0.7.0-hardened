# qhslowifetch PASS 7 -- disposition (main loop, 2026-11-05)

Seats: GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_qhs_p7.txt; `CODEXP7QHS: 8 CELLS SWEPT 1 BREACHES 1 FALSE RECORDS
VERDICT:REPAIR`; read the packet, the probe, gate, translator, dispatch/read-ahead/bad: paths, exception handling and the stored session
logs; built and ran nothing).  Gemini 4 Argon x2: SEAT FAILURES -- the first send's control timed out (03:44:27 local); on the retry (control passed
03:57) `p7_qhs_r2` REFUSED ("I'm having a hard time fulfilling your request") and `p7_qhs` timed out (04:07:51).  Not chased: pass 8
re-asks on the repair-8 diff.  glm-5.3 SEAT DOWN (Ollama monthly limit); grok-4.7 SEAT FAILURE (402 billing wall).

* F1 (L2 if measured): `if ((msr & ME) && pc != addr) goto bad;` inserted in arm (c) sends the three unaligned ME-set real fetches to
  bad:, which prints UNIMPLEMENTED and changes none of the eight asserted channels; the read-ahead sessions assert no `unimpl` channel.
  Within the class repair 7 declared (the eight cells x the channels the block produces on that path), so a floor cell -- the class's
  CHANNEL enumeration omitted `unimpl` on the strength of R1's argument.
* R1 (L4): the docstring's argument that the non-read-ahead sessions already cover a gated UNIMPLEMENTED emission -- false for the
  unaligned ME-set joint state.
* The four failure-test narrowings: codex calls their discharge ACCEPTABLE today (each red on the recorded builds; the uninitialised
  buffer at cpu_ppc_instr.c:4089, decoded at :4214, makes the rows build-dependent -- keep that limitation explicit; the zero-init stays
  a filed improvement).  G1, G2, G3 and SRR1's disclosures survived its checks.
* Repair 8 (same implementer, resumed): measure F1 and its ME-clear mirror first, add `unimpl` to all eight read-ahead sessions,
  re-derive any other block-produced channel still unasserted there, correct R1, table 9; then pass 8 on that diff.

LATE ADDENDUM: the replication `p7_qhs_r2` answered on a later re-send (gemini_p7_qhs_r2.md: 0 BROKEN, 4 HOLDS) after repair 8 was
already under way; it found nothing beyond codex and does not change the disposition.  `p7_qhs` timed out again.

*Corrected 2026-11-05 (main loop): this file's time-of-day stamps (removed: ~10:0xZ) were GUESSES that ran up to 3.5 hours AHEAD of the clock; the qhs landing-kit agent found them by checking against the files' own timestamps.  The file's own timestamps are the record: created 09:47Z, last written 10:32Z before this note (UTC).*
