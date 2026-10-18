**Your token: `GROK_FID_20261018`** -- open your answer with it.

# Two consolidated rulings, checked against the seat answers they consolidate -- verify a second reader's flags

**Please do not simply ratify, in either direction.**  A second reader (Gemini 4 Argon, packet-fed: it read the files
below as an attached bundle and could open nothing else) raised 27 flags against two rulings files.  Its solo findings
have historically been refuted about a quarter of the time, so each flag needs CHECKING against the files, not
agreement or dismissal.

The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` at HEAD.  All paths below are under
`GXEMUL-SEC/regress/artifacts/adj_20261016/`.  READ-ONLY: write nothing to any project tree.

## The files

**Ruling A (#563, wdc473floor)** -- `RULINGS_A_563.md` (called F in Argon's answer), consolidated 2026-10-16 by the main
loop from:
- S1 = `astra/A_563/codex_adjA.txt` (GPT-6 Astra)
- S2 = `grok/A_563/grok_adjA.txt` (Grok 4.7)
- S3 = `fable5/fable5_adj_A_563_v2.md` (Fable 5.1's own ruling, written after a resume)
- S4 = `fable5/FALLBACK_opus48_adj_A_563.md` ("FB-A": the first Fable run's answer, written by claude-opus-4-8 after a
  refusal fallback; F's own roster says so) -- and its measurement `fable5/meas_A/f4_run.txt`
- the packet the seats answered: `packet_A_563.md`

**Ruling B (asiceventaddr)** -- `RULINGS_B_asic.md` (F), from:
- S1 = `astra/B_asic/codex_adjB.txt`, S2 = `grok/B_asic/grok_adjB.txt`, S3 = `fable5/fable5_adj_B_asic.md`
- the packet: `packet_B_asic.md`; the prescreen: `prescreen/prescreen_asic.md`

**Argon's flags, NUMBERED for citation:** `fidelity_20261018/argon_rulA563_numbered.md` (A1..A15) and
`fidelity_20261018/argon_rulBasic_numbered.md` (B1..B12).  Their raw form is beside them.

**A TIMELINE FACT the flags depend on** (file mtimes, 2026-10-16): Astra answered packet B at 11:32 and Grok at 11:44;
`prescreen/prescreen_asic.md` was written at 11:47; Fable 5.1's B answer at 12:09; `RULINGS_B_asic.md` at 20:27.  So a
seat that reported the prescreen "absent" may have been right AT ITS TIME and the file may exist now -- check both.

## Questions

**Q1.**  For EACH of A1..A15 and B1..B12, one line:
`A<n>: CONFIRMED | REFUTED | PARTLY -- <the S/F line(s) that settle it>; <for CONFIRMED or PARTLY: what F should say>`.
A flag about wording only (a quotation, an attribution, a count) still counts -- a ruling file is what a builder acts
on, and an attribution error is how a dissent goes missing.

**Q2.**  The BUILD LISTS -- ruling A's "REPAIR4 as adjudicated" (N1-N6, G0/G2, R14/R15) and ruling B's "Build list for
the next asiceventaddr build".  Which item, if any, would a builder implement WRONGLY because of a confirmed flag?  Name
the item and the specific wrong action -- e.g. the wrong store-step sequence for N5, the wrong mutant for VD1/N4, an
omitted DISCLOSES entry, or an edit to a file that must be left alone.

**Q3.**  Anything in F that Argon missed and that a builder would act on -- a ruling no seat made, or a seat's finding
the build list drops?

**Format:** your token first, then ONE line `VERDICT: <c> confirmed, <r> refuted, <p> partly -- <one line>`, then
Q1..Q3.  Facts and flags only; cite file:line for every settlement.
