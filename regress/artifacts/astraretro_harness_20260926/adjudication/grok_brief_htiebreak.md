HARNESS REVIEW -- TIE-BREAK BY THE GROK SEAT: the rows where two verifications disagree

FIRST LINE of your answer: `VERDICT: <a> rows where the agy verification is supported, <c> where the codex one is, <n> neither, of 21 rows`.
SECOND line: the token `GROK_HTIEBREAK_ALIVE_1002`.  THIRD line: quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.

**Context.**  GPT-6 Astra reviewed this GXemul fork's regression harness at commit `db8b1a33` (finding blocks
`F<n> | path:line | round | CLASS | claim | smallest check | confidence`).  Ten groups of those answers were re-verified
twice: by the agy seat (gemini) and by the codex seat (GPT-6 Astra's own family, a fallback).  They agree on 378 of 387
findings.  You are the third model family: RULE the rows below, first-hand, from the committed source.  The project
owner ruled on 2026-10-02 that the working seats are GPT-6 Astra, agy and grok.

**The tree.**  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git).  Read COMMITTED files at `db8b1a33` only (`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show db8b1a33:<path>`, numbered with
`awk '{print NR": "$0}'` or `grep -n`); the working tree carries other people's uncommitted work.  Never read any other
`src/` under the project root.  You MAY read files under `regress/artifacts/` where a claim rests on one (several of
these rows are disputed only because one seat was not allowed to).  Write nothing; run nothing that changes a file.

**Where the two verifications are** -- for group NN in 11, 13, 14, 15, 16, 17 (and 07, 09 for two severity rows):
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\grokjobs_20260930\hverify_NN\agy_hverify_NN.txt` and `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\grokjobs_20260930\hverify_NN\codex_hverify_NN.txt`; the findings themselves are in
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\<job>\codex_<job>.txt`.  Both lines of every disputed row are quoted in `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\agypack_20261001\ingest_hverify.md`.

**STATUS -- one seat says RIGHT, the other UNSETTLED or WRONG (9 rows):**
hverify_11 `hcheckprobewiring:F12`; hverify_13 `hgatehygiene:F3`, `hgatehygiene:F5`; hverify_14 `hgateshrounding:F4`,
`hgdromdefaultprobe:F3`; hverify_15 `hm88kroundingprobe:F6`; hverify_16 `hpcc2widthprobe:F1`, `hprecommitcheck:F11`;
hverify_17 `hsgirecolourdefaultprobe:F4`.
**DRAFT KIND -- both say RIGHT, they file it differently (5 rows):**
hverify_11 `hbundle_tools2:F2` (NEW MED vs FILED-BY-PROSE OUTSTANDING_BUGS.md:10878-10888), `hdiffdiskimageio:F2` (NEW LOW vs
RECORD); hverify_14 `hgateoffline:F5` (FILED `exemptcal` vs NEW LOW), `hgdromcondprobe:F3` (NEW HIGH vs FILED
`ptywaitstatus`); hverify_15 `hlcaisalaneprobe:F4` (FILED `wiringcliff` vs FILED-BY-PROSE).
**SEVERITY with a HIGH on one side (7 rows; agy grade first):**
hverify_07 `hbundle_regress28:F1` (HIGH / MED); hverify_09 `hbundle_regress32:F4` (HIGH / LOW); hverify_11
`hcheckprobewiring:F3` (LOW / HIGH); hverify_13 `hdiffwdcidentify:F1` (LOW / HIGH), `hdiffwdcidentify:F3` (HIGH / MED),
`hgatehygiene:F6` (HIGH / LOW), `hgatehygiene:F7` (MED / HIGH).

**For EACH of the 21 rows, one line:**
`<job>:F<n> | STATUS: RIGHT / WRONG: <why> / UNSETTLED: <what would settle it> | DISPOSITION: NEW <HIGH/MED/LOW> <id> "<title>" / FILED <id> / FILED-BY-PROSE <OUTSTANDING_BUGS.md lines> / RECORD "<text>" / DROP "<why>" | SUPPORTED: agy / codex / neither | <the lines you read at db8b1a33>`
Severity for a harness defect is graded by WHAT THE GATE WOULD MISS: HIGH if the defect the check was shipped to catch
ends the emulator process or makes a memory access leave a buffer's bounds; MED if guest-visible; LOW otherwise.  For
a FILED, check the id exists in `git show db8b1a33:OUTSTANDING_BUGS.md` and names THIS defect.  One note the main loop
already checked and you should verify rather than trust: for `hgdromdefaultprobe:F3`, `regress/gdrom_default_probe.py`
at `db8b1a33` lines 1357-1371 say the destination byte is 0xea beforehand.
Then: **(a)** any row where BOTH seats are wrong; **(b)** DENOMINATOR -- rows ruled from the source versus from the two
seats' texts.
