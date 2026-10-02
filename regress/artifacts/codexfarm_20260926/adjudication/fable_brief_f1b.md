CODEX FARM 2026-09-26 -- FABLE ADJUDICATION, batch f1b

Open your answer with the token `FABLE_FARM_f1b_ALIVE_0926`, then quote verbatim the first line of
`C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\CHECKPOINT.md` -- this proves the brief and file access reached you.

**Context.**  The codex seat (GPT-6 Astra at `ultra` effort; where Astra's content filter refused the brief, the
Daybreak model `gpt-daybreak-blue-latest` answered instead -- each answer's `.launch.log` says which) researched one
open queue row per job, read-only, from the fork's source, its `OUTSTANDING_BUGS.md` rows and its artifacts.  Each
answer ends in a RECOMMENDATION for what the row's next round should do (re-scope it, witness it, fix it one way,
close it, split it, file records corrections).  The briefs and answers are listed below.

**You are the adjudicator.**  The project owner has ruled that the Fable seat adjudicates findings LAST and GPT-6 Astra
then confirms (or overturns) your dispositions.  These are recommendations about FUTURE work, so your ruling decides
what the queue says next -- nothing is fixed here.

**The tree.**  `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git), at HEAD (`git -C ... show HEAD:<path>`; the working tree
carries other people's uncommitted work).  Ignore every other `src/` under the project root.  The queue is
`OUTSTANDING_BUGS.md`; the ledger is `tools/pipeline/ledger.json`; hardware manuals are `_scratchpad/*.txt` under the
project root.

**For EACH answer:**
1. CHECK its load-bearing premises against the tree -- this project's standing rule is that anything checkable in under
   about two minutes gets CHECKED, not judged.  Name the premises you checked (with `path:line` at HEAD) and any you
   found FALSE.  A recommendation resting on a false premise is not adopted as written.
2. Rule: **ADOPT** / **ADOPT WITH CHANGES** (say exactly what changes) / **REJECT** (why) -- and for a row the answer
   says to CLOSE, whether the closure meets the project's closure conditions (a fix shipped with a measured detector, or
   an OVERTAKEN closure's three conditions: a discriminating control measured at HEAD, the carrying rows named, the
   control preserved at a durable path).
3. Give the NEXT ACTION in one line (a round, a witness attempt, a records correction, a filing), and a priority:
   **HIGH** -- a guest can end the emulator process, corrupt memory outside a buffer, or hang it, today; **MED** --
   guest-visible behaviour contrary to the hardware documentation; **LOW** -- records, diagnostics, latent code.
4. Name anything the answer MISSED that you noticed while checking, clearly marked as yours.

Be hardest on the answers whose recommendation is to CLOSE or DROP something: a wrong closure hides a live defect,
while a wrong "fix it" only costs a round.

**The answers to adjudicate:**
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\codex_armmsrmodekill.txt` (brief `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\armmsrmodekill.md`, launch log `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\armmsrmodekill.launch.log`)
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\codex_fbctrlcmdkill.txt` (brief `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\fbctrlcmdkill.md`, launch log `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\fbctrlcmdkill.launch.log`)
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\codex_armthumbabortkill.txt` (brief `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\armthumbabortkill.md`, launch log `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\armthumbabortkill.launch.log`)
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\codex_ppcrlwhighhalf.txt` (brief `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\ppcrlwhighhalf.md`, launch log `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\ppcrlwhighhalf.launch.log`)
- `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\codex_pit8253lsbnotimer.txt` (brief `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\pit8253lsbnotimer.md`, launch log `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\pit8253lsbnotimer.launch.log`)

**Write your full answer to** `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\codexfarm_20260926\adjudication\fable_f1b.md` -- that file ONLY; change nothing else anywhere -- **and return the same text as
your final message.**  First line: `VERDICT: <a> adopt, <c> adopt-with-changes, <r> reject, of <n> answers`.
