# WHY THIS DIRECTORY EXISTS -- written 2026-09-06 by the retrospective re-check (batch 10)

`#404`'s differential fixture is **GONE**.  Its session directory survives and holds ZERO files, so the
round's own measurement had no durable record anywhere in the repository: it lived only in
`_scratchpad/r106_measure.md`, which is untracked and is exactly the volatile path the project's own
rule says a cited measurement may not live at.

`r106_measure.md` is copied here VERBATIM, with its modification time preserved, so the round's numbers
are attributable again.  **It is a rescued receipt, not a re-run**: nothing here was measured today, and
the file says what it said when it was written.

**Still owed, and deliberately not done here:** the fixture itself.  Rebuilding it as
`regress/diff_rs5c313.c` belongs to the offset-model round for this device, because a differential
written now would pin today's behaviour rather than the behaviour `#404` was reasoning about.  Filed as
`rs5c313receipt` (LOW, records).

*The general lesson this instance is an example of: a measurement cited in a durable record must live at
a durable path.  `#404` cited a scratchpad file, the scratchpad outlived it by luck, and the fixture that
would have let anyone re-derive the numbers did not.*
