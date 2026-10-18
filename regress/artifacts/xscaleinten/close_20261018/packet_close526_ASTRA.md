**Your token: `ASTRA_CLOSE526_20261018`** -- open your answer with it.

# Closing ledger row `xscaleinten` (#526) -- is anything still owed?  A records check

**Please do not simply ratify.**  The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` at HEAD.  READ-ONLY: write nothing to
any project tree.  The working tree carries ANOTHER session's uncommitted edits in some files (not in `regress/gate_arm.sh`
or this row's probe); where a file is dirty, judge it by `git show HEAD:<path>` or by its committed artifacts.

## What this is

Round `#526` committed its fix as `eb26590` on 2026-09-12; Fable 5.1's adjudication ruling
(`regress/artifacts/xscaleinten/fable_adjudication_20260912.md`) says the repair chain CLOSED on that pass.  The ledger row
(`tools/pipeline/ledger.json`, id `xscaleinten`) is nevertheless still `in work`, with no closure.  This commit would
CLOSE it, hold its REGRESS review for the flagship, and change nothing else.  The records: the row's note and entries,
CHANGELOG.md's `#526` block, OUTSTANDING_BUGS.md's three `xscaleinten` entries (the last is "SHIPPED as `#526`
(2026-09-12); residuals FILED, none owed"), `regress/pass2_ledger.tsv`'s `eb26590` receipt, and
`regress/artifacts/xscaleinten/`.

## The closure fields, as drafted

- **closure.note:** CLOSED by its closure-records commit (2026-10-18): #526 (eb26590, 2026-09-12) stopped a guest read of the modelled i80321 XScale CP6 interrupt-enable register (arm_coproc_i80321_6) from ending the emulator after it had loaded the right value into rd -- the fatal() and exit(1) after the load are deleted (member 4, ACCEPT).  Detector: regress/xscale_inten_probe.py, 30 rows, wired into gate 14 (gate_arm.sh, pin 30; PASS 922 checks with the xscale rows 30/30, regress/artifacts/xscaleinten/gate_arm_20260912.log).  Kill table 3: the fix 30/30, the pre-fix HEAD leg 12/30 (killtable3_20260912/SCORES.txt).  The repair chain CLOSED on the §F2 adjudication pass by Fable 5.1's ruling (regress/artifacts/xscaleinten/fable_adjudication_20260912.md: zero floor breaches, denominator named); the coverage debt the contract discloses is filed (OUTSTANDING_BUGS.md, `xscaleinten` -- SHIPPED as `#526`).  The row stayed `in work` after that ruling only because nothing moved it; this commit does.
- **hold_question:** REGRESS (held 2026-10-18 at the xscaleinten closure): does regress/xscale_inten_probe.py still score 30/30 with XSCALE_CONTROL=OK on a build of HEAD, and 12/30 on a build of eb26590's parent 85f8b465 -- kill table 3's BASE and HEAD legs (killtable3_20260912/SCORES.txt; table 3 ran at 2026-09-12T15:32:59Z, when 85f8b465 was HEAD)?
- **state_note** gains at its head: [2026-10-18, CLOSED] The closure-records commit closed the row on Fable 5.1's 2026-09-12 ruling; REGRESS is held for the flagship (hold_question).

## Questions

**Q1.**  Do #526's records show ANYTHING still owed before the row closes -- a held or unanswered stage, a filed
follow-up that should exist and does not (the bug file names a `panel.sh` ECHO-ONLY false positive as a harness change
owing two negative controls -- is it filed as a row?), an open wrong record, a gate wiring gap, a disclosed survivor with
no row?  Quote each with file and line.
**Q2.**  Is every fact in the drafted fields true -- the commit and its date, the disposition, the detector and its pin,
the gate result, the two kill-table scores, the parent SHA and the table's timestamp?
**Q3.**  Is there any reason the row should NOT close now?

**Format:** your token first, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q3.  Every defect is a line
starting `FLAG:`.  Facts and flags only.
