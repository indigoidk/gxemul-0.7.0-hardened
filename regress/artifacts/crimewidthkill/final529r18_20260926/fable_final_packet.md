#529 (crimewidthkill) -- THE FINAL TEXT AND RECORDS, for the Fable seat (LAST) and then GPT-6 Astra's confirmation

Open with the token `FABLE_529_FINAL_ALIVE_0926`, then quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.  First line of your answer after that:
`VERDICT: <SHIP / SHIP WITH CHANGES / HOLD> -- <one clause>`.

**Where this stands.**  Your F2 adjudication (`repair16_f2_20260926/fable5_f2_adjudication.md`) closed the #529
enumeration on repair 16's F2 pass, CONDITIONAL on its Q3 text corrections, a base leg on the final bytes, the
`S_rst4clr` attribution kept durable, GPT-6 Astra's confirmation, and #549-first ordering (#549 is committed, and so
is #553, the records-only commit of the late codex answers: HEAD is `db8b1a33`).  *This packet was first fired on
2026-09-26 and the seat hit its session limit before answering; nothing in A-G changed since except item D's new
last paragraph.*  Since then the codex seat (GPT-6 Astra at
`ultra`) audited three things, and the Opus seat measured one.  Nothing below changes product code: `dev_sgi_ip32.c`
is still 8c1d1545, unchanged since 2026-09-13.  All paths are under
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\crimewidthkill\` unless absolute; read committed files with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show HEAD:<path>` (the working tree carries other sessions' work).

**Please do not simply ratify.**  For each item, check the claim against the file it cites.  The question that matters
most is the last one: WHICH OF THESE DISPOSITIONS IS WRONG?

## A0. SINCE THIS PACKET WAS WRITTEN: the final text is r19, one docstring sentence past r18

GPT-6 Astra's second records audit (2026-09-28, `codexpack_20260928/rec529audit2/codex_rec529audit2.txt`, under
`GXEMUL-SEC/regress/artifacts/`) found that r18's line 60 still said "NetBSD's +0x0c write does nothing" -- false: the
`+0x0c` write stores the low word and reaches the default arm's diagnostic (measured by the pass-1 Opus seat,
`opus_pass1_20260913/out/rows_base.out`).  r19 = r18 with that one sentence corrected
(`final529r19_20260930/crime_width_probe.r19.py`, md5 735bba9f; `mk_r19.py.txt` beside it proves the AST minus the
docstring is r18's).  Its base leg against table 16's base binary is running as you read this and lands in
`final529r19_20260930/` (`probe_base_r19.raw`, `MD5.txt`, `DIFF_vs_table16_base.txt`); item F's r18 result stands as
the r18 measurement.  The same audit's eight record corrections are applied in the drafts (`records_drafts.md`, its
dated header lines).  Everything below that says r18 is about r18; the question is whether r19 changes any answer.
**r19 RESULT (landed 2026-09-30 11:56, WALL 1235 s, PROBE_RC=0):** `CRIMEP_RESULT=226/226`, `CRIMEP_CONTROL=OK`,
`CRIMEP_DONE`, `FAILING:` empty; 24 differing row pairs against table 16's base log (233 lines each side), and a re-diff
with the `(raw ...)` values and the three note strings normalised leaves three row pairs differing only in column
padding (`time lb`, `time sb`, `time sh`); no want, got or verdict column differs.

## A. The probe's final text, r18 (docstring only)

`final529r18_20260926/crime_width_probe.r18.py` (md5 81f8894e) = r17 (`final529r17_20260926/crime_width_probe.r17.py`,
2fe7123b, your Q3 items 1-12 applied) plus:
1. GPT-6 Astra's audit of r17 (`final529r17_20260926/codex_jobs/codex_r17audit.txt`, eight false or unsupported
   sentences).  Six are corrected by the pairs in `final529r18_20260926/mk_r18.py.txt` (stepping; TIME's low bytes
   twice; TIME's upper word conditional on being zero -- verified in `dev_sgi_ip32.c`: the 32-bit truncation is inside
   `if (to_add >= 1)`; "any selection shows" only when it reaches the returned bytes; CONTROL bit 0 IS written by
   accepted rows).  The other two sit inside the ACCEPTS block and are corrected by its replacement (B).
2. `mk_r18.py` refuses unless r18's AST minus its docstring equals r17's.  r17's equals r16's but for three row notes.
Question A: is each of the six corrected sentences TRUE of the code and the tables now?

## B. The ACCEPTS-46 block -- replaced with a MEASURED enumeration

`final529r17_20260926/opus_accepts46.md` (the Opus seat, claude-opus-5-5, clean): all 92 entry x latch-state cells
measured with a silent-decline variant against predictions written before any run, 92 of 92 exact; logs in
`final529r17_20260926/opus_acc46/`.  An independent codex reading (`final529r17_20260926/codex_jobs/
codex_accepts46twin.txt`) reached the same partition.  The replacement block is `final529r18_20260926/accepts_block.txt`
(the Opus text plus one provenance line crediting the codex reading).  It names every bucket member (the two unnamed
host-diagnostic members are entries 11 and 15; the six unnamed equivalent members 12, 13, 16, 17, 43, 44) and retires
repair 13's counts: 31 guest-visible, 4 rowed on the CONTROL text in both latch states, 1 host-diagnostic only (40), 10
equivalent.
Question B: is the block true, and does it overclaim anywhere?

## C. ENTRY 34 -- the one new cell, and a grading question for you

Entry 34 is `sd +0x40 = 0`.  With the latch SET it is rowed (`lo keeps`).  With the latch CLEAR, both of its drivers
store 0 into a slot that already holds 0, so a silent decline of that access moves NO row (measured: the value session
226/226; `latch x5` by reasoning).  The Opus seat grades it clause (e): the same label and width -- an 8-byte store to a
default-arm slot, latch CLEAR -- is rowed at `+0x278` (entry 45: `top8 clear`, `top8 st+ld`, `top4 rhi/rlo`, `hi keeps`),
so only the OFFSET is unrowed, which the contract already discloses as the unrowed-slot class.  The codex reading
called it "a source-derived coverage limitation, not a measured escape result".  If you grade it a FLOOR cell instead,
the cheapest row needs no new session -- seed a nonzero value in the existing `sd +0x40` of the two value sessions and
re-want `acc 40 sw` / `p acc 40 sw` -- but it changes those sessions, so every recorded kill touching them would need
re-running before the commit.
Question C: clause (e) or floor?  Under your own rules (the (d) DEPENDS-ON closure, the label x latch floor of your
09-25 Q3 clause, "a filter may reject or discharge a cell but may demand a new row only for a floor cell").

## D. The records, corrected from GPT-6 Astra's audit of the drafts

`final529r17_20260926/codex_jobs/codex_rec529audit.txt` found eleven false or unsupported sentences in the drafts and
six omitted matters.  The corrected drafts are in the session scratchpad; their text is inlined in
`final529r18_20260926/records_drafts.md` (CHANGELOG block, OUTSTANDING_BUGS section, commit message, and the ledger
changes).  In brief: "one step at a time" -> stepped and free-running; r17 described as your items 1-12 plus the four
dossier corrections, the 13/17 wording and Astra's two, and r18 separately; the chain's conditions stated; the lane row
no longer says the `+0x0c` write "does nothing"; `M_ctldebug` separated from the joints; the per-seat "verbatim"
labels on trimmed quotes became "excerpt"; the roster gaps named (repair 14's pass 2 was grok alone; minimax down on
closing pass 3); minimax's F2 "overturn first" recorded beside deepseek's; your item 13 appended to POSTTABLE16.out
(`table16_20260926/POSTTABLE16.out`, the dated CORRECTIONS section at its end); the 2026-09-18 flagship answer
preserved (`flagship_20260918/`) and ledger [154]'s evidence repaired.
**One change since the audit, and it overturns YOUR grading:** `crimectllane` is filed HIGH, not MED.  Your farm f1c
adjudication (`GXEMUL-SEC/regress/artifacts/codexfarm_20260926/adjudication/fable_f1c.md`, item 2.4) graded it MED
("the lane defect grants a guest no capability it lacks through the modelled 64-bit HARD_RESET"); GPT-6 Astra's
confirmation (`codex_astraconfirm_farm_f1c.txt` beside it) ruled that wrong under the severity rule both used -- a
32-bit store to `+0x08` stops every CPU, and in ordinary execution `emul.c` ends the emulation and `main.c` returns.
All three drafts now say HIGH, with your argument recorded as bearing on ranking rather than severity
(`records_drafts.md`, its dated second header line).  A ruling that overturns you is the one to be hardest on.
Question D: is anything in the corrected records still false, or missing -- and is HIGH right?

## E. The carrier's Q3 clause (the project-root CLAUDE.md; working tree only, never committed)

The codex seat (`codexfarm_20260926/codex_carrierq3.txt` under `GXEMUL-SEC/regress/artifacts/`) ruled the clause I wrote
"FAITHFUL WITH CHANGES": it turned the demonstrated remaining holes into the whole floor, sourced the latch axis from
"the guard's own partition" rather than from the repair path's reads, and left the clause-(e) fallback of the
2026-09-09 label clause contradicting it.  Its replacement text is in that file.  ONE PART OF IT IS STALE and I have
checked it: it says "INTMASK and CONTROL-write label-swaps remain individually owed measurements under the ruling" --
they were measured in table 16 (`M7_intmasklatch` 223/226, `M8_ctllatch` 223/226, `table16_20260926/POSTTABLE16.out`),
which your F2 denominator already lists.
Question E: adopt the codex replacement with that sentence corrected, adopt a different text, or keep mine?

## F. The base leg on the final bytes

`final529r18_20260926/probe_base_r18.raw` against table 16's base binary; `MD5.txt` beside it names both, and
`DIFF_vs_table16_base.txt` compares it with table 16's base log (`table16_20260926/logs/probe_base.raw`).
RESULT, 2026-09-26 10:18, WALL 1258 s, PROBE_RC=0: `CRIMEP_RESULT=226/226`, `CRIMEP_CONTROL=OK`, `CRIMEP_DONE`, the
`FAILING:` line empty.  The diff has 24 differing line pairs (233 lines each side): 6 are the rows whose notes r17
rewrote -- THREE note strings, each printed by TWO rows (`ctldog sw/sd msg`, `ctlrst sw/sd msg`, `rst 4w/8w msg`), so
my "three row notes" above counts strings, not rows -- and 18 are rows that print a free-running TIME value
(`(raw N)`: 18 of the 22 TIME rows differ; the 23rd raw-bearing row, `gate hardint`, reports HARDINT and is
unchanged -- GPT-6 Astra's second audit), which differs run to run by construction.  A re-diff with `(raw ...)` and
the three note strings normalised leaves two row pairs (four diff lines, `time lb` and `time lh`), each differing
only in the column padding after a shorter or longer raw value; no want, got or verdict column differs.  (Measured
by that normalised re-diff, not read by eye; re-derived independently by GPT-6 Astra on 2026-09-28,
`codexpack_20260928/rec529audit2/`.)

## G. WHICH OF THESE DISPOSITIONS IS WRONG?

Name the count, and for each: the item, what should change, and the line you checked.

Write your answer to `final529r18_20260926/fable5_final.md` (that file only) and return the same text.
