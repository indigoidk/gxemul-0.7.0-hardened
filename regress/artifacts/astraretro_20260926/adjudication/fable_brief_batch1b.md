ASTRA RETRO-REVIEW -- FABLE ADJUDICATION, batch 1b

Open your answer with the token `FABLE_RETRO_1b_ALIVE_0926`, then quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md` -- this proves the brief and file access reached you.

**Context.** GPT-6 Astra (the codex seat, `ultra` effort) has just done its first-ever reading of this GXemul fork's
accumulated changes to several source files, at HEAD `8ea26abb`: the fork's NET change to each file since the upstream
import `39748e3c`, source reading only, no builds or runs.  Its answers are the files listed below.  Each finding is one
block: `F<n> | path:line at HEAD | round | CODE / RECORD / TEST-GAP | live at HEAD | consequence | smallest check |
confidence`.

**You are the adjudicator.**  The project owner has ruled that the Fable seat adjudicates findings LAST and GPT-6 Astra
then confirms (or overturns) your dispositions.  The rule you apply is the project's LATE-DISSENT rule, because these
rounds are all committed: *closure changes the licence, never the truth-value.*
1. A WRONG RECORD -- a `/* #NNN: */` comment, a CHANGELOG sentence or an OUTSTANDING_BUGS closure that is false of the
   code at HEAD -- is corrected in place (L4).  Give the exact replacement text.
2. A defect of CODE that is already filed keeps its id; say so, and check the id really exists at HEAD.
3. Everything else is FILED as a new queue row with a severity, or DROPPED with the reason.  Nothing is fixed here.

**The tree.**  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git).  Read files AT HEAD with
`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show HEAD:<path>` (pipe through `grep -n` or `sed -n 'A,Bp'` with line
numbers via `awk '{print NR": "$0}'`); the WORKING TREE carries other people's uncommitted work that is not under review.
Ignore every other `src/` under the project root (`src/`, `est/`, `build/`, `build-asan/`, `_archive/` are other
copies, and a copy reports line numbers off by hundreds).  Hardware manuals: `ls C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\*.txt`.

**For EACH finding: CHECK it against HEAD before you rule on it** -- this project's standing rule is that anything
checkable in under about two minutes gets CHECKED, not judged, and a confident reviewer's error is exactly the one
nobody re-checks, so be hardest on the findings Astra marks `high`.  Then one disposition line:

`<job>:F<n> | CONFIRMED-FILED <id> | CONFIRMED-NEW <HIGH/MED/LOW> <proposed-id> "<one-line title>" | RECORD-L4 "<the exact
corrected text>" | TEST-GAP-FILE <proposed-id> | REFUTED | UNSETTLED "<the measurement that would settle it>" |
DUPLICATE <job>:F<n>`

followed by ONE line naming what you checked (`path:line` at HEAD, or the `OUTSTANDING_BUGS.md` line of a filed id).
Severity: **HIGH** -- a guest can end the emulator process, make it read or write outside a buffer, or hang it;
**MED** -- guest-visible behaviour contrary to the hardware documentation; **LOW** -- diagnostics, latent code, test gaps.
A proposed id is short, lowercase, no spaces, and must not already exist in `OUTSTANDING_BUGS.md` at HEAD.

Then: **(a)** which of Astra's CODE findings you could NOT confirm, and why; **(b)** any finding Astra missed that you
noticed while checking (clearly marked as yours); **(c)** the DENOMINATOR -- how many findings you checked against the
source versus ruled on from Astra's text alone.

**The answers to adjudicate:**
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\bundle_include1\codex_bundle_include1.txt`  (its brief: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\briefs\bundle_include1.md`)
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\bundle_include2\codex_bundle_include2.txt`  (its brief: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\briefs\bundle_include2.md`)

**Write your full answer to** `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\adjudication\fable_batch1b.md` -- that file ONLY; change nothing else anywhere -- **and return the same text as
your final message.**  First line of the file: `VERDICT: <c> confirmed-new, <f> confirmed-filed, <r> record-L4,
<t> test-gap, <x> refuted, <u> unsettled, <d> duplicate, of <n> findings`.
