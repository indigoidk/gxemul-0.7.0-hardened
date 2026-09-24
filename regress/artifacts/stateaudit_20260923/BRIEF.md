# Records-versus-tree audit of the GXemul hardened fork, 2026-09-23 -- please check my inventory, do not ratify it

**Open your answer with ONE verdict line:** `VERDICT: INVENTORY CORRECT` or `VERDICT: INVENTORY HAS <n> ERRORS`.
Then answer Q1-Q6 by number.  End with a seat record: which model you are, what you read, what you ran.

**READ-ONLY.**  Do not edit, stage, commit, delete or move anything, and do not run gates, probes, builds or the
emulator.  Reading files and read-only git commands (`git diff`, `git show`, `git log`, `git ls-files`, `git grep`) are
fine.  The owner decides every commit; propose, do not act.

## Context

After an unattended Windows Update reboot (2026-09-22 21:32) the owner asked whether any progress on this project was
lost, and asked for every uncommitted patch to be reviewed against the records.  I measured the state and wrote
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\verify_20260923\INVENTORY.md`.  **Read it first.**  Everything it claims was
measured by a command, and the files it cites are beside it in that directory:

* `diffs/<path with / as _>.diff` -- `git diff HEAD -- <file>` for each of the 32 modified tracked files; `diffs/_STAT.txt`
* `untracked_outside_artifacts.txt` (10 files), `untracked_artifact_dirs.txt` (47 untracked artifact directories)
* `vs_ff7ab93.txt` -- name-status of the current full tree against the 2026-09-21 full-tree snapshot
* `checkers/*.out` -- the project's own record checkers, run today on the working tree
* `ledger_uncommitted_claims.out` -- every ledger row whose entries say work is uncommitted / in the working tree

**The tree under review is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC` (git repo, HEAD `f685d75`).  Ignore every other
`src/` under the project root** -- `./src/` and `_archive/**/builds/*` are pristine 2021 upstream copies and differ by
hundreds of lines.  The records are `GXEMUL-SEC/CHANGELOG.md`, `GXEMUL-SEC/OUTSTANDING_BUGS.md` and
`GXEMUL-SEC/tools/pipeline/ledger.json` (rows have `id`, `state`, `commits`, and `entries` whose text is in `note`).
If you cannot run commands, the `diffs/` directory holds every hunk.

**Premises are stated as questions on purpose.**  A previous review had seven of nine reviewers confirm a premise
that was wrong by a factor of four.  Where I say "measured", check whether the command I name actually measures what
I claim.

## Questions

**Q1 -- completeness of the unit table (INVENTORY.md section B).**  Denominator: 32 modified tracked files + 10
untracked files outside `regress/artifacts/` + 47 untracked artifact directories.  Is every one mapped to a unit, and
is each mapping right?  Several files carry hunks from more than one round (`regress/gate_arm.sh`,
`regress/gate_sh_rounding.sh`, `regress/gdrom_default_probe.py`, `tools/pipeline/check_probe_wiring.py`,
`tools/precommit_check.sh`) -- read the hunks and say whether I split them correctly.  Name any hunk that belongs to a
different round than the table says, and any file I missed.

**Q2 -- each patch against its own record.**  For units U3, U4, U5, U6 and U7, does the working-tree hunk contain what
its record says it contains, and nothing else?  Check the numbers (row counts, `EXPECT_ROWS`, gate pins), the row
names, and every claimed comment correction.  Report mismatches with `file:line`.  I claim `src/devices/dev_sh4.c`'s
126 added lines contain NO code, only comments -- verify it.

**Q3 -- the owner-held round U1 (#545), in detail.**  Check the claims in
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\records\cl545_draft.md` against the U1 hunks and the logs under
`GXEMUL-SEC/regress/artifacts/fbd5/` (the gate logs are in `gate_20260919/`, the four measurement tables in
`killtable_20260919/`, `xtable_20260919/`, `table3_20260919/`, `table4_20260919/`): 37 guest rows in the sites probe;
333 offline rows in `regress/diff_footbridge.c`; families P0-P9 = 78, X1-X8 = 222, of which X6 = 108, X7 = 70, X8 = 6;
gate_arm 1061 checks and gate_offline 351; 49 test variants across the four tables, every one detected by the
combined guest+offline detector; five `int` latch fields; the `+0x18c` read no longer returns `irq_enable`.  Mark each
MATCHES or DIFFERS, with the evidence line.

**Q4 -- commit coupling.**  Which units can be committed on their own, and which only together?  Name any file whose
commit ALONE would make a gate or a record checker fail.  Candidates to test, not conclusions: the uncommitted
`check_probe_wiring.py` manifest names 78 untracked files; `SCORE_CLAIMS_MANIFEST=31` in `tools/precommit_check.sh`
assumes #529's probe is gated; `regress/gate_arm.sh` holds U1 + U7 + a #539 hunk; `regress/gate_sh_rounding.sh` holds
U4 + U5.

**Q5 -- the inventory's own errors.**  Which statement in INVENTORY.md is false, overstated, or not supported by the
evidence it names?  Be harder on sections A and D than on B: they carry the claim the owner actually asked about,
"nothing was lost".  What check would falsify that claim that I did NOT run?  (For example: I compared the tree only
against a snapshot taken 2026-09-21 15:36 -- is there work older than that snapshot which the records say exists and
which is in no tree, no snapshot and no commit?)

**Q6 -- the 2026-09-27 / 09-28 deadlines.**  From the files, what exactly fails at the weekly battery on Sunday
2026-09-27 18:00 (`GXEMUL-SEC/tools/nightly_battery.sh`, `GXEMUL-SEC/regress/run.sh`), and what fails from 2026-09-28
(`SC_EXEMPT` in `regress/gate_offline.sh`; the `EXEMPT` table in `tools/pipeline/check_probe_wiring.py`)?  Read, do not
run.  Then name the SMALLEST set of owner decisions that would let the 09-27 battery pass.
