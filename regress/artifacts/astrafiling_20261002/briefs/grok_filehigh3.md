TWO HIGH GRADES in the regression-harness filing that you have not ruled under your own re-read test

FIRST line of your answer: `VERDICT: <h> of 2 grades HIGH by your re-read test, <n> not HIGH`.
SECOND line: the token `GROK_FILEHIGH3_ALIVE_1002`.  THIRD line: quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md`.

**Context.**  In `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astrafiling_20261002\grok\grok_filehigh.txt`
you re-read 57 rows graded HIGH and called 21 harness rows NOT HIGH.  GPT-6 Astra conceded 11 of them (now MED) and
holds 10, which are filed HIGH and marked disputed
(`...\astrafiling_20261002\afile_07\codex_afile_07.txt`; the rule question is stated in each disputed row's note in
`...\astrafiling_20261002\FILING_OVERLAY.tsv`, lines 99-108).  The harness severity rule the campaign applied: a harness
defect is graded by WHAT THE CHECK WOULD MISS -- HIGH if a defect that ends the emulator process, or makes one of its
memory accesses leave a buffer's bounds, would pass the check.

Two HIGH grades were outside those 57 rows and so have had no reading by you under the test you applied there.  Please
do not ratify either from this text: read the files.

**1. `ptywaitstatus` -- an EXISTING class row, re-graded MED -> HIGH.**  The queue row is at `OUTSTANDING_BUGS.md`
(search the text `ptywaitstatus`; about line 21935): probes collect the child's wait status and their liveness verdict
does not consult it, so a session whose child ended after the last observation passes.  The re-grade is GPT-6 Astra's
own (`...\regress\artifacts\astraretro_harness_20260926\HARNESS_DISPOSITIONS.md`, search `regrading the existing MED
entry`: findings `hpcc2widthprobe:F2` and `hppcroundingprobe:F2`).  Astra's family wrote the findings, so its raise is
not adopted on its say-so; yours is the independent reading.
   I believe -- check it -- that the question under your own test is: at the sites the class names, would a run in
   which the emulator process ENDS (a nonzero exit or a signal after the last value was read) be reported as a pass
   TODAY?  Read at least `regress/pcc2_width_probe.py` (the place where the liveness verdict is formed and where the
   wait status is stored) and `regress/ppc_rounding_probe.py:169-185`, and one probe that DOES fold the status in, for
   contrast.

**2. `gdromcondhow` -- a NEW row you ruled and then held.**  Your tie-break made finding `hgdromcondprobe:F3` NEW HIGH;
Astra said FILED `ptywaitstatus`; on its return you HELD
(`...\astraretro_harness_20260926\adjudication\grok_20261002\grok_hopen3.txt`): rows R1b and R2b of
`regress/gdrom_cond_probe.py` pass on the announced byte alone (`:419`, `:499`) and never assert that the session
survived.  Your re-read test in `grok_filehigh.txt` called rows of this family NOT HIGH where nothing that is live
today ends the process on the path the row exercises.  Is `gdromcondhow` HIGH by that same test, or does it belong
with the ten disputed rows (HIGH only on Astra's rule that a check which would ACCEPT the re-introduction of a fixed
process-ending defect is HIGH)?  Say which of the two it is and why the answer differs from, or matches, the rows you
called NOT HIGH.

**The tree.**  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git) at commit `7440e129`.  Read committed files with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 7440e129:<path>`; if that is refused to you, read from disk and say
so (no file named here carries an uncommitted edit).  Never read any other `src/` under the project root; never
`git status` or `git diff`.  Write nothing.

**For each of the two, ONE line, then at most four sentences of reasons with `path:line`:**
`<id> | HIGH / NOT HIGH: <why> / HIGH ONLY ON THE RE-INTRODUCTION RULE (belongs with the disputed rows) | <the lines you read>`

End with `DENOMINATOR: <s> of 2 read in the source; probes opened: <list>`.
