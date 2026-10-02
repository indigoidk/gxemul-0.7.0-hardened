ASTRA RETRO-REVIEW -- FABLE ADJUDICATION, batch 3d

Open your answer with the token `FABLE_RETRO_3d_ALIVE_0928`, then quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md` -- this proves the brief and file access reached you.

**Context.** GPT-6 Astra (the codex seat, `ultra` effort) has done its first-ever reading of this GXemul fork's
accumulated changes to several source files, at commit `8ea26abb`: the fork's NET change to each file since the upstream
import `39748e3c`, source reading only, no builds or runs.  Its answers are the files listed below -- 31 findings in
6 answers.  Each finding is one block: `F<n> | path:line | round | CODE / RECORD / TEST-GAP | live | consequence |
smallest check | confidence`.

**You are the adjudicator.**  The project owner has ruled that the Fable seat adjudicates findings LAST and GPT-6 Astra
then confirms (or overturns) your dispositions.  The rule you apply is the project's LATE-DISSENT rule, because these
rounds are all committed: *closure changes the licence, never the truth-value.*
1. A WRONG RECORD -- a `/* #NNN: */` comment, a CHANGELOG sentence or an OUTSTANDING_BUGS closure that is false of the
   code -- is corrected in place (L4).  Give the exact replacement text.
2. A defect of CODE that is already filed keeps its id; say so, and check the id really exists.  **An entry recorded in
   OUTSTANDING_BUGS.md prose WITHOUT a short id is still FILED** -- rule CONFIRMED-FILED, quote its line range, and
   propose the id it should be given.  (Astra overturned six dispositions of batch 2a for ruling such entries NEW.)
3. Everything else is FILED as a new queue row with a severity, or DROPPED with the reason.  Nothing is fixed here.

**The tree, and WHICH COMMIT.**  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git).  The answers' line numbers are commit `8ea26abb`'s, so read every file
there: `git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show 8ea26abb:<path>` (pipe through `grep -n`, or number the lines with
`awk '{print NR": "$0}'`).  HEAD has since moved to `db8b1a33` by one records-only commit (#553: CHANGELOG.md,
OUTSTANDING_BUGS.md, the ledger, regress/diff_wdc_identify.c, tools/pipeline/check_probe_wiring.py) -- NO file under
`src/` changed, so a CODE finding confirmed at `8ea26abb` is live at HEAD; but CHANGELOG.md and OUTSTANDING_BUGS.md line
numbers differ between the two, so cite them at `8ea26abb` and say so once in your first paragraph.  Check an id's
EXISTENCE at HEAD too (`git show HEAD:OUTSTANDING_BUGS.md`): #553 filed three rows.  The WORKING TREE carries other
people's uncommitted work that is not under review -- do not read from disk.  Ignore every other `src/` under the
project root (`src/`, `est/`, `build/`, `build-asan/`, `_archive/` are other copies, and a copy reports line numbers off
by hundreds).  Hardware manuals: `ls C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\*.txt`.

**What earlier batches of this campaign already ruled** is in
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\DISPOSITIONS.md` (on disk; batches 1a, 1b, 2a, 2b, each adjudicated by the
Fable seat and confirmed by GPT-6 Astra).  Read it before you propose an id: if a finding is the same defect as a row
it lists, rule `DUPLICATE-OF-ROW <id>` and add what this finding contributes -- do not propose a second id for one
defect.  Its open RULE QUESTION (`shoddprfield`: is an out-of-ARRAY access that stays inside the containing struct
HIGH under the severity rule below?) is not yours to settle here; if one of your findings has that shape, grade it by
the consequence you can show and mark it `RULE-QUESTION shoddprfield`.

**For EACH finding: CHECK it against the source before you rule on it** -- this project's standing rule is that
anything checkable in under about two minutes gets CHECKED, not judged, and a confident reviewer's error is exactly
the one nobody re-checks, so be hardest on the findings Astra marks `high`.  Then one disposition line:

`<job>:F<n> | CONFIRMED-FILED <id> | CONFIRMED-NEW <HIGH/MED/LOW> <proposed-id> "<one-line title>" | RECORD-L4 "<the exact
corrected text>" | TEST-GAP-FILE <proposed-id> | REFUTED | UNSETTLED "<the measurement that would settle it>" |
DUPLICATE <job>:F<n> | DUPLICATE-OF-ROW <id>`

followed by ONE line naming what you checked (`path:line` at `8ea26abb`, or the `OUTSTANDING_BUGS.md` line of a filed
id).  Severity, in plain engineering terms: **HIGH** -- guest-controlled input makes the emulator process terminate,
makes one of its memory accesses leave a buffer's bounds, or stops it making progress; **MED** -- guest-visible
behaviour differs from the hardware documentation; **LOW** -- diagnostics, latent code, test coverage.  Grade by what
the source shows, not by the queue's existing grade: Astra raised two filed rows in batch 2a whose recorded severity
the adjudication had accepted unread.  A proposed id is short, lowercase, no spaces, and must not already exist in
`OUTSTANDING_BUGS.md` or in `DISPOSITIONS.md`.

Then: **(a)** which of Astra's CODE findings you could NOT confirm, and why; **(b)** any finding Astra missed that you
noticed while checking (clearly marked as yours); **(c)** the DENOMINATOR -- how many findings you checked against the
source versus ruled on from Astra's text alone.


**A DRAFT EXISTS, and it is not a ruling.**  The codex seat (GPT-6 Astra, ultra; a sibling of the model that wrote
the findings, so its agreement is not independent evidence) prepared DRAFT dispositions for this batch on 2026-09-28:
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexpack_20260928\draft_3d\codex_draft_3d.txt`.
It did the mechanical work -- the source re-checks, the OUTSTANDING_BUGS.md lookups by id AND by prose, the
duplicate checks against DISPOSITIONS.md and across answers, the replacement texts -- and lists in its section (a)
the findings it thinks wrong or overstated.  Use it to spend your budget where it matters: RULE FIRST-HAND on every
finding, be HARDEST on the draft's dispositions (a draft that agrees with a finding was written by its author's
sibling), verify every lookup it cites, and say in your file which of its dispositions you changed and why.  A
ruling that merely ratifies the draft is worth nothing to this project.


**A CHECK OF THAT DRAFT EXISTS TOO** (2026-10-01): `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\grokjobs_20260930\draftcheck_3d\codex_draftcheck_3d.txt` -- every draft disposition checked against the source,
with RIGHT / WRONG / WORDING per finding.  It was written by the codex seat (the draft's own model family, because the grok
seat's balance ran out), so treat agreement between draft and check as weak evidence and their DISAGREEMENTS as the
findings to rule first-hand first.

**The answers to adjudicate:**
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\cpush\codex_cpush.txt`  (its brief: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\briefs\cpush.md`)
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\devpvr\codex_devpvr.txt`  (its brief: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\briefs\devpvr.md`)
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\cpuppc\codex_cpuppc.txt`  (its brief: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\briefs\cpuppc.md`)
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\cpualpha\codex_cpualpha.txt`  (its brief: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\briefs\cpualpha.md`)
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\cpualphapalcode\codex_cpualphapalcode.txt`  (its brief: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\briefs\cpualphapalcode.md`)
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\devlca\codex_devlca.txt`  (its brief: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\briefs\devlca.md`)

**One ownership note.**  `src/devices/dev_lca.c` and `src/cpus/cpu_alpha_palcode.c` rows belong to ANOTHER
working session, which holds uncommitted work on both files.  Rule on those findings exactly as on the others
(at `8ea26abb`), and mark each new row you propose on them `FOR-PEER` so it is handed over rather than filed twice.

**Write your full answer to** `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\adjudication\fable_batch3d.md` -- that file ONLY; change nothing else
anywhere -- **and return the same text as your final message.**  First line of the file: `VERDICT: <c> confirmed-new,
<f> confirmed-filed, <r> record-L4, <t> test-gap, <x> refuted, <u> unsettled, <d> duplicate, of <n> findings`.
