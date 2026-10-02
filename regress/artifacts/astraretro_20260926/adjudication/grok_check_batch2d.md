GROK SEAT -- an independent check of the Fable seat's batch 2d adjudication (NOT the Astra confirmation, which follows
when the codex seat is available again)

Open your answer with the token `GROK_CHECK_2D_ALIVE_0930`.  FIRST LINE after it:
`VERDICT: <n> of 28 dispositions wrong (<m> more need a change of wording or severity)`.

The tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC` (a hardened fork of the GXemul machine emulator, C99).  Read
committed files with `git -C C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC show <commit>:<path>`; the answers under review
cite commit `8ea26abb` for source (identical to HEAD `db8b1a33` under `src/`) and the queue file
`OUTSTANDING_BUGS.md` at HEAD.  Never read `C:\DocumentNoSnc\CC\GXEMUL\src\` (a pristine 2021 upstream copy).  Read
nothing under `regress/artifacts/` except the files this brief names.  Write nothing; return text.

The adjudication: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\astraretro_20260926\adjudication\fable_batch2d.md`
(28 dispositions over five answers, each `job:F<n> | <disposition>` followed by a `Checked:` line).  The answers it
rules on are named in its brief, `fable_brief_batch2d.md` beside it, and the earlier batches' final rulings are in
`..\DISPOSITIONS.md` (so a "DUPLICATE-OF-ROW" claim can be checked against the row it names).

For EVERY disposition, check it against the source and the queue file yourself and write one line:
`<job>:F<n> | Fable said <disposition, short> | RIGHT / WRONG: <should be> / WORDING: <the change> | <the line you checked>`
Be hardest on: a CONFIRMED-FILED whose id does not exist at HEAD, or exists for a different defect; a FILED-BY-PROSE
whose quoted line range does not describe this defect; a NEW whose defect the queue already records in prose without an
id (grep by the function name, the diagnostic text and the file's basename); a RECORD-L4 whose replacement text is
itself false of the code; a severity the source does not support under the rule (HIGH: input under the guest's
control ends the process, makes a memory access leave a buffer's bounds, or stops progress; MED: differs from the
hardware documentation; LOW: records, diagnostics, coverage).  Then the DENOMINATOR: how many you checked in the
source versus ruled on from the adjudication's text.
