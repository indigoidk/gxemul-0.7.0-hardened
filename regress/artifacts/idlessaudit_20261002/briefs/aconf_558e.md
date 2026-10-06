#558 -- a new checker field and a no-panel stage record: right?

Open with the token `ASTRA558E_ALIVE_1006` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CONFIRMED -- the change is right and nothing else is wrong`
`VERDICT: <n> things wrong`

A RECORDS AND TOOLING check.  Write nothing, build nothing.  Tree `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`, HEAD
`e1871fa5`; files under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idlessaudit_20261002\draft\`.

**Why.**  #558's precheck failed section L: `e1871fa5` (#557) has the subject "#557 closeassess: the rows closed with no
commit are audited -- ... 4 members added to closeassessrows ..."; `check_commit_attribution.py` reads the closure word
`closed`, sees the row `closeassessrows` named, and grades HARD because that row is `open`.  The row is open by design:
#557 extended the class row, it closed nothing.  `reopened` would be false (nothing was closed and superseded).  And
sections I/H failed on `idlesslow`'s review stage, which ran three seats (Astra, agy, grok) under the owner's
2026-10-02 roster and was never a nine-seat panel.

**The change.**
1. `CLOSEWORD_checker.diff` (19 lines): after the `reopened` branch, a row may list in `closure_word_elsewhere` the
   commits whose subject's closure word is about something else -- whole 7-40 hex tokens before the first ` -- ` (via
   the existing `lists()`), the reason after it.  Reported as `NOT A CLOSURE`, not graded; anything else stays HARD.
2. `CLOSEWORD_ledger.txt`: the field as set on `closeassessrows`, and the new last entry on `idlesslow`
   (`[NOT A PANEL STAGE: NO PANEL CONVENED]`, no panel dir cited).
3. `CLOSEWORD_controls.out`: five controls (field absent / naming e1871fa5 / naming another sha / sha only in the reason /
   a longer non-prefix token) -- only the second passes.

Questions, each `<n> | RIGHT / WRONG: <why, path:line>`:
1. Is the exemption as narrow as stated -- can any field value other than a listed whole prefix of the commit's hash
   before the first ` -- ` exempt a commit?  Does it touch any other grading path?
2. Is `closeassessrows`'s field TRUE of `e1871fa5` (read `git show --format=%B e1871fa5` and the row at HEAD)?
3. Is the no-panel record true of `idlesslow`'s review stage, and does it hide any seat that was fired and answered?
4. Do the five controls exercise the cases that matter, and is a control missing?
Then: anything else wrong.  End with `DENOMINATOR: <n> of 3 files read`.
