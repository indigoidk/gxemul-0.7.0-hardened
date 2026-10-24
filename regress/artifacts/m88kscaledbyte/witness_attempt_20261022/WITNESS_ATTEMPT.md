# m88kscaledbyte -- the rung-3 witness ATTEMPT, 2026-10-22: BLOCKED (recorded so `none` never means "did not think to")

Round T1 of the external-fixes batch (`regress/artifacts/research_20261022/`).  The carrier's lifecycle step 2 asks for
a rung-3 witness attempt before the fix; the 2026-08-27 owner ruling asks one seat to try it; the 2026-08-27 `detector:`
term requires the attempt to be RECORDED.

**What was attempted.**  A measuring seat was briefed (Agent tool, Opus) to make a cold-debugger probe through real
instruction decode and real `memory_rw` on the unmodified in-tree `testm88k` machine, with the liveness and
device-signature controls the witness ladder requires, built from HEAD 13233723 in a scratch clone -- the probe SHAPE both
design seats specified in `research_20261022/crit_20261022/codex_rescrit.txt` and `grok_crit.txt` (their Q1 sections).
The brief named no instruction words or decode paths; it pointed at the row id and those two answers.

**What happened.**  The coordinator's response was stopped by the harness safety classifier while the brief was being
written (the seventh such stop that day; the class is recorded in the project memory `gxemul-panel-benign-framing`).
The agent launched with a truncated brief and was killed at once; it had written nothing.  Per the standing rule for
that class, the brief was not re-issued in any form.

**Owner ruling (2026-10-22, by question):** "Detector-only, attempt recorded" -- ship the agreed fix with an offline
regression detector under the ledger's `detector:` witness term, record this attempt as BLOCKED, and leave a guest-path
witness to the owner (or a session they drive) by another route if one is wanted.  The probe shape for that later run
is the one the two seat answers specify; nothing here restates it.

**Status:** rung-3 attempt BLOCKED (classifier), not "not tried".  Witness term for the round: `detector:<path>`.
