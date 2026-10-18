**Your token: `GROK_CLOSE527_20261018`** -- open your answer with it.

# Closing ledger rows `ppcrlwimiwidth` and `ppcrldimimask` (#527) -- is anything still owed?  A records check

**Please do not simply ratify.**  The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` at HEAD.  READ-ONLY: write nothing to
any project tree.  The working tree carries ANOTHER session's uncommitted edits in some files (not in `regress/gate_ppc.sh`
or these rows' probes); where a file is dirty, judge it by `git show HEAD:<path>` or by its committed artifacts.

## What this is

Round `#527` committed both fixes as `7e39a49e` on 2026-09-12; Fable 5.1's adjudication ruling
(`regress/artifacts/xscaleinten/fable_adjudication_20260912.md`) says the repair chain CLOSED on that pass.  Both ledger
rows (`tools/pipeline/ledger.json`, ids `ppcrlwimiwidth` and `ppcrldimimask`) are nevertheless still `in work`, with no
closure.  This commit would CLOSE both, hold their REGRESS review for the flagship, and change nothing else.  The records:
the rows' notes and entries, CHANGELOG.md's `#527` block, OUTSTANDING_BUGS.md's entries for both ids (the last is
"`ppcrldimimask` -- SHIPPED with `ppcrlwimiwidth` as `#527` (2026-09-12); residuals FILED, none owed"),
`regress/pass2_ledger.tsv`'s `7e39a49` receipt, and `regress/artifacts/ppcrlwimiwidth/` and `ppcrldimimask/`.  Gate 13
(`regress/gate_ppc.sh`) was extended this morning by `#565` (`8d038908`, an rldicl block); the rlwimi/rldimi blocks
are #527's.

## The closure fields, as drafted

- **ppcrlwimiwidth closure.note:** CLOSED by its closure-records commit (2026-10-18): #527 (7e39a49e, 2026-09-12) made X(rlwimi) rotate the 32-bit word at 32-bit width and write a wrapping mask's high word, as Book I's RTL does.  Detector: regress/ppc_rlwimi_probe.py, 28 rows, wired into gate 13 (gate_ppc.sh, pin 28; PASS 110 checks at the time, regress/artifacts/ppcrlwimiwidth/gate_ppc_20260912.log).  Kill table 3 (regress/artifacts/ppcrlwimiwidth/killtable3_20260912/SCORES.txt): the fix 28/28, the pre-fix HEAD leg 14/28, the identity body 12/28, every R_ mutant killed (17 legs, zero escapes).  The repair chain CLOSED on the §F2 adjudication pass by Fable 5.1's ruling (regress/artifacts/xscaleinten/fable_adjudication_20260912.md: zero floor breaches, denominator named); the residuals are filed in OUTSTANDING_BUGS.md (`ppcrldimimask` -- SHIPPED with `ppcrlwimiwidth` as `#527`), none owed.  The row stayed `in work` after that ruling only because nothing moved it; this commit does.
- **ppcrldimimask closure.note:** CLOSED by its closure-records commit (2026-10-18): #527 (7e39a49e, 2026-09-12) stopped X(rldimi)'s rotate loop from consuming its own shift count -- the post-decrement had left sh == -1, so every insert mask was built to bit 63.  Detector: regress/ppc_rldimi_probe.py, 29 rows, wired into gate 13 (gate_ppc.sh, pin 29; PASS 110 checks at the time, regress/artifacts/ppcrlwimiwidth/gate_ppc_20260912.log).  Kill table 3 (regress/artifacts/ppcrlwimiwidth/killtable3_20260912/SCORES.txt): the fix 29/29, the pre-fix HEAD leg 17/29, the identity body 13/29, every D_ mutant killed (17 legs, zero escapes).  The repair chain CLOSED on the §F2 adjudication pass by Fable 5.1's ruling (regress/artifacts/xscaleinten/fable_adjudication_20260912.md: zero floor breaches, denominator named); the residuals are filed in OUTSTANDING_BUGS.md (`ppcrldimimask` -- SHIPPED with `ppcrlwimiwidth` as `#527`), none owed.  The row stayed `in work` after that ruling only because nothing moved it; this commit does.
- **hold_question (both rows):** REGRESS (held 2026-10-18 at the #527 closure): do regress/ppc_rlwimi_probe.py and regress/ppc_rldimi_probe.py still score 28/28 and 29/29 with CONTROL=OK on a build of HEAD, and 14/28 and 17/29 on a build of 7e39a49e's parent eb26590b -- kill table 3's BASE and HEAD legs (killtable3_20260912/SCORES.txt)?  eb26590b (#526) changed no PowerPC source, so its cpu_ppc_instr.c is the pre-#527 file table 3's HEAD leg measured.
- **state_note** gains at its head (both rows): [2026-10-18, CLOSED] The closure-records commit closed the row on Fable 5.1's 2026-09-12 ruling; REGRESS is held for the flagship (hold_question).

## Questions

**Q1.**  Do #527's records show ANYTHING still owed before the rows close -- a held or unanswered stage, a residual the
bug file calls FILED that has no home (is each of the five residuals under the SHIPPED entry a ledger row, a named
measurement, or only prose?), an open wrong record, a gate wiring gap, a disclosed survivor with no row?  Quote each
with file and line.
**Q2.**  Is every fact in the drafted fields true -- the commit and its date, each fix's description, the detectors and
their pins, the gate result, the kill-table scores (BASE, HEAD, the null legs, the escape count), the parent SHA and the
claim that it changed no PowerPC source?
**Q3.**  Is there any reason either row should NOT close now?

**Format:** your token first, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q3.  Every defect is a line
starting `FLAG:`.  Facts and flags only.
