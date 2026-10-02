ASTRA CONFIRMATION of the harness review's DRAFT dispositions -- `hverify_02` (52 findings)

Open with the token `ASTRACONFIRM_H02_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <w> of 52 draft dispositions wrong (<m> more need a change of wording or severity)`

**Context.**  GPT-6 Astra reviewed this GXemul fork's REGRESSION HARNESS read-only (the "answers" below: gate scripts,
probes, offline differentials, pipeline checkers, at commit `db8b1a33`), reporting findings in the classes CANNOT-FAIL,
SELECTS-NOTHING, STATUS-LAUNDERED, ENCODING, RECORD and OTHER.  An INDEPENDENT seat -- the grok seat (grok-4.7, xhigh) -- then re-verified every
finding against the committed tree and attached a DRAFT disposition to each: `NEW <HIGH/MED/LOW> <id> "<title>"`,
`FILED <id>`, `FILED-BY-PROSE <OUTSTANDING_BUGS.md lines>`, `RECORD "<replacement text>"` or `DROP "<why>"`.  The project
owner ruled on 2026-10-02 that the working seats are GPT-6 Astra, agy and grok: the independent seat's draft is the
proposed ruling, and YOU confirm or overturn it before anything is filed.  Nothing is fixed here; this decides what
the queue will say.

**Please do not simply ratify -- and mind which half is yours.**  You are the same model family as the review, so your
agreement with a FINDING is not evidence of anything.  Your job is the DISPOSITION.  Check each draft against the
committed tree (`git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show db8b1a33:<path>`; the working tree carries uncommitted work that is not under review;
ignore every other `src/` under the project root).  The errors that matter:
- a `NEW` whose defect `OUTSTANDING_BUGS.md` at `db8b1a33` already records, by id OR IN PROSE WITHOUT AN ID (search by the
  file's basename, the row name and the check's own text) -- that is `FILED` / `FILED-BY-PROSE` with the line range;
- a `FILED` whose id does not exist at `db8b1a33`, or names a different defect;
- a severity that does not follow the rule for a harness defect, which is graded by WHAT THE GATE WOULD MISS: HIGH if
  the defect the check was shipped to catch ends the emulator process or makes a memory access leave a buffer's bounds;
  MED if it is guest-visible; LOW otherwise (diagnostics, records, coverage);
- a `RECORD` whose replacement text is itself false of the code;
- a `DROP`, or a WRONG verdict, on a finding that is in fact right -- a wrong refutation hides a check that cannot fail;
- two rows that are ONE defect, and a proposed id that already exists in `OUTSTANDING_BUGS.md` or in
  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\DISPOSITIONS.md` (the retro campaign's rulings).

**The draft to confirm:** `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\grokjobs_20260930\hverify_02\grok_hverify_02.txt`
**The answers it verified:** `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\hbundle_pipeline2\codex_hbundle_pipeline2.txt`, `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\hbundle_pipeline3\codex_hbundle_pipeline3.txt`, `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\hbundle_pipeline4\codex_hbundle_pipeline4.txt`, `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_harness_20260926\hbundle_regress1\codex_hbundle_regress1.txt`

**For each draft disposition you overturn or amend, one block:**
`<job>:F<n> | draft said <X> | should be <Y> | the evidence (path:line at db8b1a33, or the queue line) | confidence`

Then list the dispositions you checked and found right (ids only is fine), and end with
`DENOMINATOR: checked <c> of 52 draft dispositions against the source`.

Read-only: write nothing, build nothing, run nothing that changes a file.
