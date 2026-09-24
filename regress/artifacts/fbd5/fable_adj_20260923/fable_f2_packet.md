# `#545` (fbdeclinefive) -- Fable 5.1 as the LAST seat of the adjudication stage and the regress stage, before commit

Open with the token `FABLE_SEAT_ALIVE_20260923_FBD5F2` and the FIRST LINE of
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\CHECKPOINT.md` quoted verbatim.  Then ONE line: `VERDICT: CLOSE` or
`VERDICT: DO NOT CLOSE -- <reason>`.  Then Q1-Q5 by number, then a seat record (model, files read, commands run).
**READ-ONLY**: read files and run read-only git (`git -C C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC diff/show/log/grep`);
edit, stage, commit, build and run nothing.  The tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC` (HEAD `f685d75`);
ignore every other `src/` under the project root.  Plain engineering language.

## The round

`src/devices/dev_footbridge.c` ended the emulator process on five guest accesses in the direction the DC21285 does not
define (writes to +0x180/+0x184/+0x280/+0x284, a read of +0x18c).  The fix declines each (no state change, a declined
read returns 0) and announces once per site through five `int` latches carrying `(once)`; the +0x18c arm no longer
returns `irq_enable`.  The three footbridge probes' old failability control (a +0x18c read ending the process) is
replaced by two harness legs, H1 and H2.  You answered the design pass on 2026-09-19 (`_scratchpad/fbd5/FABLE_P1_ANSWER.md`).
The owner then HELD this seat for the rest of the round; the owner has now asked for it before the commit.

## Read

* The uncommitted diff: `git diff HEAD -- src/devices/dev_footbridge.c regress/diff_footbridge.c
  regress/footbridge_sites_probe.py regress/fbpending_drain_probe.py regress/fbpending_witness.py regress/gate_offline.sh
  regress/gate_arm.sh` -- in `gate_arm.sh` only the footbridge block and the E0-E6 hunk are this round's; the section
  from about line 1772 on is `#529`'s and does NOT ship here.
* Pass 2: `_scratchpad/fbd5/p2/P2_FINDINGS.md` (F1-F50, consolidated from panel `_scratchpad/panel_20260919_115657`) and
  `p2/CODEX_DED_TRIAGE.md`.  The repair and its own pass: `p2r/brief_fbd5_f2.md`, `p2r/repair.patch`,
  `p2r/F2_FINDINGS.md` (G1-G33, from panel `_scratchpad/panel_20260919_131006`, where the kimi CLI walled mid-answer).
* Measurements: `impl/PRETABLE.out`, `impl/TABLE_SUMMARY.md`, and the durable logs under
  `GXEMUL-SEC/regress/artifacts/fbd5/` -- `killtable_20260919/`, `xtable_20260919/`, `table3_20260919/`,
  `table4_20260919/` (incl. `opus_f2/`), `gate_20260919/` (`gate_arm_545b.log` PASS 1061, `gate_offline_545d.log` PASS
  351), and `r3_m9_20260923/` (M9 re-measured TODAY on the final 37-row probe: 33/37, red N1 N2 N0 NO).
* Records drafts: `_scratchpad/fbd5/records/cl545_draft.md` (corrected today by a records audit),
  `bugs_draft545.md`, `ledger_write545.py`.  Today's audit: `GXEMUL-SEC/regress/artifacts/stateaudit_20260923/FINAL.md`
  (items D3 and D5 concern this round).

## Questions

**Q1 -- the adjudication stage.**  Which of the main loop's ACCEPTED dispositions in `P2_FINDINGS.md` and
`F2_FINDINGS.md` is wrong?  Name at least one to reverse or narrow, or say plainly none is and why you are confident.

**Q2 -- the floor, asked of the SHIPPED COMPOSITE.**  Two consecutive passes found cells of one space, so the repair
closed the class (X6: every declined access, 108 cells; X7: every legal access re-arms no latch, 70 cells; X8: wide
seeds).  Is there a single-edit variant inside the DEPENDS-ON enumeration of the five declined arms (the predicates
dominating the edited lines, up to the function boundary; operand swaps drawn only from fields the guarded bodies read)
that passes BOTH the 37-row guest probe and the 333-row differential?  Give the denominator: which cells and which edit
shapes you swept.  Disclosed and not rowed, per the contract: a latch guard conditioned on a field the decline never
reads (`timer_control`, caught only by the guest prologue), the interrupt output after a legal access, and the legs'
own predicates.

**Q3 -- the regress stage (Fable-only by standing directive).**  Are the gate results (both measured on the COMBINED
working tree, which also carried other rounds' edits), the four tables plus today's M9 re-measure, and the build-tree
clearance enough to discharge regression?  If not, name the missing measurement.

**Q4 -- records.**  Name any wrong record in `cl545_draft.md`, `bugs_draft545.md` or `ledger_write545.py` (its CLOSURE
note, WITNESS, and the filings `armdesc3kill`, `armdacr2kill`, `fbirqsoftunimpl`, `hygienecensus`,
`upstreamdeleteprose`, the `fiqenableread` dissent).

**Q5 -- the commit.**  Plan: stage BY NAME; `gate_arm.sh` goes in as a HEAD-based partial blob (HEAD + the footbridge
block + #539's never-committed E0-E6 fix, which this commit ships; NOT #529's section); tool files carrying other
rounds' uncommitted hunks are swapped to their HEAD copies for the hook and restored after; `CHANGELOG.md` also carries
two in-place wrong-record notes from today's audit (#539's, which is this campaign's, and #517's), `OUTSTANDING_BUGS.md`
today's audit section, `ledger.json` the peer session's 2026-09-21 state notes (authorship recorded as theirs).  Would
this ship a wrong record, or a check fitted to the tree?  What must change first?
