TWO PARKED REPAIRS THE CENSUS FOUND UNCOMMITTED -- are they right, and do they discharge the rows that were closed on them?

Open with the token `ASTRAPARKED_ALIVE_1002` on its own line, then ONE verdict line:
`VERDICT: boilerplateprefix <SHIP / HOLD>; gdromcontractresidual <SHIP / HOLD>`.

This is a RECORDS-AND-HARNESS check: a checker's repair and a probe's docstring against the ledger rows that describe
them.  Write nothing, build nothing, run no emulator.  The tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` at HEAD
`1329d894`; committed files with `git -C C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC show HEAD:<path>`; the WORKING copies
of the two files below carry the parked edits (`git -C ... diff HEAD -- <path>` shows each).  Ignore any other `src/`
under the project root.  Everything else is under `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\artifacts\closeassess_20261002\`.

**Context.**  Your census confirmation (`aconf_census\codex_aconf_census.txt`) found two closed ledger rows whose fix
is NOT at HEAD: `boilerplateprefix` (HEAD still has `PREFIX = 60`) and `gdromcontractresidual` (the two contract
corrections absent).  Both fixes EXIST, uncommitted, in the working tree since 2026-09-17 -- parked by an earlier
session and never landed.  They are to be committed in a round of their own, with a pass on the diff; this is that
pass.  Please do not simply ratify: the comment in the first file makes measured claims, and the docstring in the
second makes coverage claims, and both were written by the session that then forgot to commit them.

1. **`tools/pipeline/check_boilerplate.py`** -- `draft\parked_check_boilerplate.diff` (+39/-3).  The comparison key
   becomes the full seat note instead of `note[:60]`; `EXCERPT = 60` stays for display.  The row `boilerplateprefix`
   (`tools/pipeline/ledger.json`, state closed, witness "controlled in both directions ... 7 false positives cleared
   and 54 genuine stamps retained").  Controls re-run today on scratch copies of the working ledger:
   `draft\boilerplate_controls_20261002.out` -- the untouched ledger gives `BOILERPLATE_PASS 54 archived, 0 new`; one
   identical paragraph injected across four seat entries of one row, dated after the cutoff, gives `BOILERPLATE_FAIL`
   naming the row.  Questions: (a) is the code change exactly the key change and nothing else (read the diff, not the
   comment)?  (b) does the comment's narrative match the row and the controls -- any number or claim in it the file or
   the row does not support?  (c) is there any way the pre-commit hook, which runs this checker, behaves differently
   on the committed ledger than the controls show?  One line each: `1a | ... | 1b | ... | 1c | ...`.

2. **`regress/gdrom_default_probe.py`** -- `draft\parked_gdrom_default_probe.diff` (+260/-4, docstring only: the M3
   label split into M3a / M3b, a coverage MATRIX of {arm} x {width} naming the row that holds each cell, the measured
   per-mutant scores with their log paths, and dated records).  The row `gdromcontractresidual` says the probe's
   contract used the bare label `M3` for two different mutants and carried an undated escape record; your census said
   both corrections are absent from HEAD at `:56` and `:119`.  Questions: (a) does the parked docstring make the two
   corrections the row names?  (b) is every claim in it true: the row names in the matrix exist in the probe, the
   scores named exist at the log paths under `regress/artifacts/gdromdmadefault/repairB_20260917/logs/` (read them),
   the mutant descriptions match the kill tables?  (c) is anything in it a program change (the diff must be docstring
   and comment only -- a `verify_hrec`-style check will be run, but say what you see)?  (d) the row also says a
   `gdromdmasilent` re-measurement is OWED (`tools/pipeline/ledger.json`, the row's last entries): does the docstring
   claim it was done?  One line each: `2a .. 2d`.

For each file end with `SHIP` (commit as it stands, under the row's id, with the row's commits field filled) or
`HOLD: <what must change first>`.  End with `DENOMINATOR: <h> hunks of 2 diffs read; <l> logs read`.
