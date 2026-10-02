ASTRA RETRO-REVIEW (HARNESS) -- FABLE ADJUDICATION, batch h08

Open your answer with the token `FABLE_HARNESS_H08_ALIVE_1001`, then quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md` -- this proves the brief and file access reached you.

**Context.**  GPT-6 Astra (the codex seat, `ultra` effort) read this GXemul fork's REGRESSION HARNESS -- the Python
probes that drive the emulator's debugger through a pty, the gate scripts that score them, the offline C differentials
and the pipeline checkers run before every commit -- at commit `db8b1a33`, source reading only.  Its answers are the four
files below: 47 findings.  Each finding is one block `F<n> | path:line | round | CLASS | <claim> | <smallest check> |
confidence`, in these classes: **CANNOT-FAIL** (a row or check that passes with the defect it guards reinstated or its
oracle removed -- the project's vacuity-floor class), **SELECTS-NOTHING** (a pattern or range that can match nothing and
then reports success or zero), **STATUS-LAUNDERED** (a failure that surfaces as success: an exit status lost in a pipe, a
killed run scored complete, a skip scored as a pass), **ENCODING** (a hand-assembled instruction word that is not what
its comment says), **RECORD** (a comment or docstring false of the code), **OTHER**.

**You are the adjudicator.**  The project owner has ruled that the Fable seat adjudicates findings LAST and GPT-6 Astra
then confirms (or overturns) your dispositions.  The harness is committed, so the LATE-DISSENT rule applies: *closure
changes the licence, never the truth-value.*
1. A WRONG RECORD -- a comment, docstring, CHANGELOG sentence or OUTSTANDING_BUGS closure false of the code -- is
   corrected in place (L4).  Give the exact replacement text.
2. A defect already in the queue keeps its id; check the id exists.  **An entry recorded in OUTSTANDING_BUGS.md prose
   WITHOUT a short id is still FILED** -- rule CONFIRMED-FILED, quote its line range, and propose the id it should get.
   This queue records many harness defects in prose: search `git show db8b1a33:OUTSTANDING_BUGS.md` by the file's
   basename, the row name and the check's text before you propose an id.
3. Everything else is FILED as a new queue row with a severity, or REFUTED with the reason.  Nothing is fixed here.

**Severity for a harness defect is graded by WHAT THE GATE WOULD MISS**, not by the harness code itself: **HIGH** if the
defect the check was shipped to catch ends the emulator process or makes a memory access leave a buffer's bounds;
**MED** if it is guest-visible; **LOW** otherwise (diagnostics, records, coverage).  A check that cannot fail on the
defect it was shipped to catch reports coverage that does not exist -- say what both versions of the product code would
produce at that row.  A proposed id is short, lowercase, no spaces, must not contain "kill", and must not already exist
in `OUTSTANDING_BUGS.md` or in `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\DISPOSITIONS.md` (the retro campaign's rulings -- a defect a row there already
names is `DUPLICATE-OF-ROW <id>`).

**The tree, and WHICH COMMIT.**  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git).  The answers' line numbers are commit `db8b1a33`'s: read every file there,
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show db8b1a33:<path>` (pipe through `grep -n`, or number lines with `awk '{print NR": "$0}'`).  HEAD is still `db8b1a33`.  The
WORKING TREE carries other people's uncommitted work -- do not read from disk.  Ignore every other `src/` under the
project root (`src/`, `est/`, `build/`, `build-asan/`, `_archive/` are other copies).  Run nothing; write only the one
file named below.

**For EACH finding: CHECK it against the committed file before you rule** -- for CANNOT-FAIL trace what the check
compares and what a defective target would produce; for SELECTS-NOTHING apply the pattern to the data it is meant to
match; for STATUS-LAUNDERED follow the exit status from the failing command to the verdict; for RECORD quote the code
the comment misdescribes.  Then one disposition line:

`<job>:F<n> | CONFIRMED-NEW <HIGH/MED/LOW> <proposed-id> "<one-line title>" | CONFIRMED-FILED <id or OUTSTANDING_BUGS.md
line range + proposed id> | RECORD-L4 "<the exact corrected text>" | REFUTED "<why>" | UNSETTLED "<what would settle it>"
| DUPLICATE <job>:F<n> | DUPLICATE-OF-ROW <id>`

followed by ONE line naming what you checked (`path:line` at `db8b1a33`).

**A VERIFICATION EXISTS, and it is not a ruling.**  Every finding in these four answers was re-checked by
the grok seat (grok-4.7, xhigh) -- an independent model family: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\grokjobs_20260930\hverify_08\grok_hverify_08.txt`.
It gives one line per finding -- RIGHT / WRONG / UNSETTLED with the lines it read, and a DRAFT disposition (NEW /
FILED / FILED-BY-PROSE / RECORD / DROP) -- and lists in its section (a) the findings it thinks wrong or overstated.  Use
it to spend your budget where it matters: rule FIRST-HAND on every finding, be HARDEST on the findings it marks RIGHT
with a NEW disposition (those become queue rows) and on anything it marks UNSETTLED, verify every lookup it cites, and
say in your file which of its draft dispositions you changed and why.  A ruling that merely ratifies the draft is
worth nothing to this project.

Then: **(a)** which findings you could NOT confirm, and why; **(b)** any defect in the same files that both the review
and the verification missed (clearly marked as yours); **(c)** the DENOMINATOR -- how many findings you checked against
the source versus ruled on from the texts alone.

**The answers to adjudicate:**
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\hbundle_regress29\codex_hbundle_regress29.txt`  (its brief: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\briefs\hbundle_regress29.md`)
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\hbundle_regress3\codex_hbundle_regress3.txt`  (its brief: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\briefs\hbundle_regress3.md`)
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\hbundle_regress30\codex_hbundle_regress30.txt`  (its brief: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\briefs\hbundle_regress30.md`)
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\hbundle_regress31\codex_hbundle_regress31.txt`  (its brief: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\briefs\hbundle_regress31.md`)

**Write your full answer to** `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\adjudication\fable_hbatch_08.md` -- that file ONLY; change nothing else anywhere
-- **and return the same text as your final message.**  First line of the file: `VERDICT: <c> confirmed-new,
<f> confirmed-filed, <r> record-L4, <x> refuted, <u> unsettled, <d> duplicate, of <n> findings`.
