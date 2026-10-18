**Your token: `GROK_CLOSE528_20261018`** -- open your answer with it.

# Closing ledger row `mapledmaaddr` (#528) -- is anything still owed?  A records check

**Please do not simply ratify.**  The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` at HEAD.  READ-ONLY: write nothing to
any project tree.  **The working tree carries ANOTHER session's uncommitted edits** in, among others,
`regress/gate_sh_rounding.sh` (gate 10, where this row's detector is wired) -- judge gate 10 from its committed
artifacts (`regress/artifacts/mapledmaaddr/gate_sh_rounding_20260912.log`) or `git show HEAD:regress/gate_sh_rounding.sh`,
never from the working-tree file.

## What this is

Round `#528` committed its fix as `ca3be4e` on 2026-09-12; Fable 5.1's closing ruling
(`regress/artifacts/mapledmaaddr/fable_close_20260912.md`) says the repair chain CLOSES on kill table 7.  The ledger row
(`tools/pipeline/ledger.json`, id `mapledmaaddr`) is nevertheless still `in work`, with no closure.  This commit would
CLOSE it, hold its REGRESS review for the flagship, and change nothing else.  The records: the row's note and entries,
CHANGELOG.md's `#528` block, OUTSTANDING_BUGS.md's `mapledmaaddr` entry, `regress/pass2_ledger.tsv`'s `ca3be4e` receipt,
and `regress/artifacts/mapledmaaddr/`.

## The closure fields, as drafted

- **closure.note:** CLOSED by its closure-records commit (2026-10-18): #528 (ca3be4e, 2026-09-12) stopped an ordinary guest read of the Dreamcast Maple DMA-address register (MAPLE_DMAADDR, case 0x04) from ending the emulator after the model had computed the right value -- the read arm now breaks into the common tail, which returns the modelled d->dmaaddr.  Detector: regress/maple_dmaaddr_probe.py, 37 rows, wired into gate 10 (gate_sh_rounding.sh, pin 37; gate PASS 391 checks, regress/artifacts/mapledmaaddr/gate_sh_rounding_20260912.log).  Kill table 7: the fix 37/37, the pre-fix HEAD leg 11/37 (killtable7_20260912/SCORES.txt).  The repair chain CLOSED on table 7 by Fable 5.1's closing ruling (regress/artifacts/mapledmaaddr/fable_close_20260912.md, 21/21 on prediction); M_TICKPERIODIC4 and M_FILE are disclosed outside the contract.  The row stayed `in work` after that ruling only because nothing moved it; this commit does.  Split out earlier: mapledmaadvance (MED, filed).
- **hold_question:** REGRESS (held 2026-10-18 at the mapledmaaddr closure): does regress/maple_dmaaddr_probe.py still score 37/37 with MAPLE_DMAADDR_CONTROL=OK on a build of HEAD, and 11/37 on a build of ca3be4e's parent 7457c04b -- kill table 7's BASE and HEAD legs (killtable7_20260912/SCORES.txt; table 7 ran at 2026-09-13T02:21Z, when 7457c04b was HEAD)?
- **state_note** gains at its head: [2026-10-18, CLOSED] The closure-records commit closed the row on Fable 5.1's 2026-09-12 closing ruling; REGRESS is held for the flagship (hold_question).

## Questions

**Q1.**  Do #528's records show ANYTHING still owed before the row closes -- a held or unanswered stage, a filed
follow-up that should exist and does not, an open wrong record, a gate wiring gap, a disclosed survivor with no row?
Quote each with file and line.
**Q2.**  Is every fact in the drafted fields true -- the commit, the disposition, the detector and its pin, the gate
result, the two kill-table scores, the parent SHA and the table's timestamp, the two disclosed mutants, the split-off
row?
**Q3.**  Is there any reason the row should NOT close now?

**Format:** your token first, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q3.  Every defect is a line
starting `FLAG:`.  Facts and flags only.
