#558 -- the repair of your aconf_558f item 2: right, and is the file's grading contract now consistent everywhere?

Open with the token `ASTRA558G_ALIVE_1006` on its own line, then ONE verdict line, exactly one of:
`VERDICT: CONFIRMED -- the repair is right and no copy of the contract is stale`
`VERDICT: <n> things wrong`

A RECORDS check.  Write nothing, build nothing.  Tree `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC`, HEAD `e1871fa5`.
Your answer: `regress\artifacts\idlessaudit_20261002\aconf_558f\codex_aconf_558f.txt` (item 2: the records-only
paragraph and the `reopened` comment still promised HARD unconditionally).

The repair: `regress\artifacts\idlessaudit_20261002\draft\CLOSEWORD_checker_v3.diff` -- the whole working diff of
`tools/pipeline/check_commit_attribution.py` against HEAD.  Both passages now name the exception.

1. `1 | RIGHT / WRONG: <why, path:line>` -- is the repair exactly what your item asked?
2. Read the WHOLE working file once: list EVERY sentence that states what a closure word on a non-closed row grades
   to, and say for each whether it is now true.  This is meant to close the chain, so an enumeration, not a sample.
End with `DENOMINATOR: <n> sentences found about the closure-word grade; <m> lines of the file read`.
