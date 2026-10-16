# ADJUDICATION -- the expired probe-wiring exemption that blocks every commit (`wiringcliff`)

Four independent adjudicators answer this (owner roster 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3).  It is an
ordinary test-harness housekeeping decision.  READ-ONLY: write nothing to any project tree.  Every fact you need is inlined
below; seats that can read files may verify them at `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` (HEAD e483d931, read committed
text with `git show e483d931:<path>`).

Open with your seat token (`FABLE_WIRINGCLIFF_20261016` / `ASTRA_WIRINGCLIFF_20261016` / `GROK_WIRINGCLIFF_20261016` /
`GLM_WIRINGCLIFF_20261016`), then ONE line: `VERDICT: A / B / C (<one line>)`.

## Facts

1. Precommit section R runs `tools/pipeline/check_probe_wiring.py` with no `--today` argument
   (`tools/precommit_check.sh:546-550`).  The checker fails a commit when a shipped DETECTOR (a regression probe that ships
   with a fix) is run by no gate AND its dated exemption has passed: the test is `elif d < today:` (`:3940-3951`).
2. The exemption for `regress/artifacts/ip30abortkill/ip30_abort_probe.py` reads, at HEAD `:3097-3100`:
   `("2026-10-15", "no gate runs an SGI IP30 guest session (gate_asan_sweep.sh constructs only); filed to wiringcliff with
   #518/#520/#530")`.  Today is 2026-10-16, so section R now refuses EVERY commit, in both sessions that share this tree.
   The working-tree copy carries the same date (`:3112-3114`).
3. The probe is round #531's shipped detector (commit 686d179c, 2026-09-18): a 721-line cold-debugger probe on the
   unmodified `-E sgi -e ip30` machine, 27 rows, test-first (8/21 rows before the fix, 21/21 after, 27 after a later closure).
4. It was already re-dated once, individually, on 2026-09-25 (round #550, by owner ruling of 2026-09-24 "re-date all ten
   individually").  That round found a home for it: `regress/gate_arm.sh` already runs seven SGI cold-debugger probes of the
   same shape.  Measured then: 33/33 rows on build/gxemul in 568 seconds, because each surviving guest session waits out a
   12-second poll (to be sure a late process end is still seen).  The runtime is why it stayed exempt rather than wired.
5. More exemptions in the same list expire soon: 2026-10-22 (`ppc_rldicl_probe.py`, `alpha_tbi_probe.py`), 2026-10-23
   (`lca_badval_probe.py`), 2026-10-26 (`lca_widewrite_probe.py`), 2026-10-27 (`lca_isalane_probe.py`; the three LCA ones
   belong to the other session's rounds).
6. `wiringcliff` is the open ledger row that owes the wiring of these exempted detectors.

## Options

- **A. Re-date the IP30 entry only**, to a near date, with its reason updated to name the measured cost (568 s) and the row
  that owes the wiring.  One line.  The detector stays run by no gate until the wiring round lands.
- **B. Wire the probe into `gate_arm.sh` now** (the home #550 found).  Adds about 568 s to every run of that gate.
- **C. Shorten the per-session poll first, then wire** (the probe change `wiringcliff` would carry).  A probe change that owes
  its own measurement: a late process end must still be caught.
- (Not an option: deleting the exemption without wiring -- section R would then refuse every commit until wiring lands.)

## The coordinator's disposition (attack it)

**A now**: re-date the IP30 entry to 2026-10-30 (two weeks), reason updated to `"no gate runs an SGI IP30 guest session;
gate_arm.sh hosts this shape but measured 568 s/run (#550, regress/artifacts/exemptredate_20260925/); owed by wiringcliff,
re-dated 2026-10-16 by a four-seat ruling (regress/artifacts/adj_20261016/wiringcliff/)"`.  Then run the `wiringcliff` round
(B or C) as the next single task after the records landing, so the re-date is not open-ended.  Re-date nothing else today:
the 10-22..10-27 entries are decided on their own dates or folded into that round.  The commit carrying the re-date stages
HEAD's file plus this one line only (the working copy also carries two sessions' unrelated uncommitted edits).

## Questions (VERDICT LINE FIRST)

1. A, B or C -- one line with the reason.
2. If A: is 2026-10-30 the right date, and is the reason text right?
3. Is any fact above wrong?  (Seats that can read files: check facts 1, 2 and 4 against the files.)  In particular, does
   `gate_arm.sh` run per commit or only in the weekly battery?  That decides what B's 568 s costs.
4. Which of the coordinator's dispositions is wrong?
