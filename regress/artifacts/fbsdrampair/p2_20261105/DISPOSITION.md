# fbsdrampair PASS 2 -- disposition (main loop, 2026-11-05)

Seats: GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_fbs_p2.txt; `CODEXP2FBS: 8 CELLS SWEPT 0 BREACHES 3 FALSE RECORDS
VERDICT:REPAIR`).  Gemini 4 Argon: SEAT FAILURE, because the web route is down.  glm-5.3 and grok-4.7: walled.
* THE FLOOR CHAIN CLOSES on this pass.  Its denominator is 8 cells: two registers x read/write x own latch clear/set.  No undisclosed
  escape was found.
* WIDTH IS clause-(e) DEBT, not floor.  `len` appears in DEVICE_ACCESS(footbridge) only in memory_readmax64 (:520) and
  memory_writemax64 (:803); no arm, dispatch or fold tests it, and importing the helpers' partitions would cross the
  enclosing-function bound.
* The five EQUIVALENT claims hold.  The early-return pair rests on memory_rw.c:491 zeroing the buffer before the handler.
* The fix is sound against the manual (7.3.9/7.3.10 reset 0; 00FC0000h is the blank-ROM default, dc21285.txt:3206-3229), and the
  announce text is truthful.
THREE RECORDS: R1 IMPL_NOTE's O2 description; R2 the probe's "visible only here" in X; R3 X1 credited for the offset kept-exit.  They
went to the implementer (Opus 5.5, resumed) as comment-only fixes, with an AST proof against the frozen instrument.
