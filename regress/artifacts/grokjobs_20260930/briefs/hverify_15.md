HARNESS REVIEW VERIFICATION -- group 15 (4 answers)

Open your answer with the token `GROKJOBS_HVERIFY_15_ALIVE`.  Second line: the VERDICT line specified at the end.

**The tree.**  `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC` (git): a hardened fork of the GXemul machine emulator, C99.  Read
COMMITTED files at `db8b1a33` (`git -C C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC show db8b1a33:<path>`, numbered with
`awk '{print NR": "$0}'` or `grep -n`); the WORKING TREE carries other people's uncommitted work -- do not read source
from disk.  Never read `C:\DocumentNoSnc\CC\GXEMUL\src\` (a pristine 2021 upstream copy).  Read nothing under
`regress/artifacts/` except the files this brief names.  Hardware manuals: `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\*.txt`.
Write nothing; run nothing; return text.  Cite `path:line` at `db8b1a33` for every claim; say "not checked" rather
than guess.  Where a claim is arithmetic, enumerate the values.

**Context.**  A reviewing model read this fork's regression harness (`regress/` and `tools/` -- gate scripts, probes,
differential tests, pipeline checkers) at `db8b1a33` and reported findings in these classes: CANNOT-FAIL (a check that
passes with its defect reinstated or its oracle removed), SELECTS-NOTHING (a pattern or range that matches nothing it
is meant to), STATUS-LAUNDERED (a failure whose exit status is discarded so the run reports success), ENCODING (a
hand-assembled instruction word that is not what its comment says), RECORD (a comment or docstring false of the code),
OTHER.  Each finding is one block `F<n> | path:line | round | CLASS | <claim> | <smallest check> | confidence`.
Nothing has been ruled on these yet; the Fable seat will adjudicate with your verification in hand.

**The answers to verify:**
- `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\hhpcmipsctorprobe\codex_hhpcmipsctorprobe.txt`  (its brief: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\briefs\hhpcmipsctorprobe.md`)
- `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\hlcaisalaneprobe\codex_hlcaisalaneprobe.txt`  (its brief: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\briefs\hlcaisalaneprobe.md`)
- `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\hlunaabsentcpuprobe\codex_hlunaabsentcpuprobe.txt`  (its brief: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\briefs\hlunaabsentcpuprobe.md`)
- `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\hm88kroundingprobe\codex_hm88kroundingprobe.txt`  (its brief: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\briefs\hm88kroundingprobe.md`)

For EVERY finding in those answers write one line:
`<job>:F<n> | <CLASS> | RIGHT / WRONG: <why> / UNSETTLED: <what would settle it> | DRAFT: NEW <HIGH/MED/LOW> <proposed-id> "<title>" | FILED <id> | FILED-BY-PROSE <OUTSTANDING_BUGS.md line range> | RECORD "<exact replacement text>" | DROP "<why>" | <the lines you read>`
RIGHT means you re-derived the claim from the committed file: for CANNOT-FAIL, trace what the check compares and what a
defective target would produce; for SELECTS-NOTHING, apply the pattern to the data it is meant to match; for
STATUS-LAUNDERED, follow the exit status from the failing command to the verdict; for RECORD, quote the code the comment
misdescribes.  Search `git show db8b1a33:OUTSTANDING_BUGS.md` by the file's basename, the row name and the check's text
before proposing an id; this queue records many harness defects in prose without an id.  Severity: a check that
cannot fail on the defect it was shipped to catch is the project's vacuity-floor class -- grade it by what the gate
would miss (HIGH if the missed defect ends the process or escapes a buffer; MED if guest-visible; LOW otherwise).
A proposed id is short, lowercase, no spaces, must not exist in OUTSTANDING_BUGS.md, and must not contain "kill".
Then: **(a)** findings you think are wrong or overstated, with the line that shows it; **(b)** anything you found that
the answers missed in the same files; **(c)** DENOMINATOR: findings checked in the source versus ruled on from text.
VERDICT line (second line): `VERDICT: <r> right, <w> wrong, <u> unsettled of <n> findings -- <c> cannot-fail confirmed`.
