#558 -- the two repairs of your aconf_558e: right?

Open with the token `ASTRA558F_ALIVE_1006` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CONFIRMED -- both repairs are right and nothing else is wrong`
`VERDICT: <n> things wrong`

A RECORDS AND TOOLING check.  Write nothing, build nothing.  Tree `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`, HEAD
`e1871fa5`; files under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\idlessaudit_20261002\`.

Your answer: `aconf_558e\codex_aconf_558e.txt` (2 things wrong: item 4, a missing whole-token control; "anything
else", the module docstring's grading contract named only `reopened`).

**The repairs:**
1. `draft\CLOSEWORD_controls.out` -- six controls now, each run on the shipped checker AND on a mutant with `lists()`
   replaced by `names()` on the new branch (the copy runs from the scratchpad, so its `SEC` is pinned to the repo; no
   other change).  Your `(e1871fa5) -- reason` is the sixth.
2. `draft\CLOSEWORD_checker_v2.diff` -- the whole working diff of `tools/pipeline/check_commit_attribution.py` against
   HEAD: the branch as before, plus the docstring's HARD paragraph and its "HARD (or REOPENED, or NOT A CLOSURE)".

Questions, each `<n> | RIGHT / WRONG: <why, path:line>`:
1. Does the sixth control do what you asked -- HARD on the shipped checker, NOT A CLOSURE on the mutant -- and is
   the mutant exactly the broadening you named?
2. Does the docstring now state the exception truly and in both places, and is any other copy of the grading
   contract in the file left stale?
Then: anything else in the diff.  End with `DENOMINATOR: <n> of 2 files read`.
