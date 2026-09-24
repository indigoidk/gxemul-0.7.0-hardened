OPUS548E_ALIVE
VERDICT: SHIP WITH CHANGES

The change is small but it is in-round. Revision 3's R6 checks each re-arm case on one timer only. The `==` defect, applied to the other three timers, passes every row in the battery and leaves a timer owing 4529 against a bound of 762 at rung 3 (measured). That is a floor breach.

**What I rebuilt independently**, from HEAD plus revision 3 (every file `cmp`-equal to the working tree). Logs are in `_scratchpad\opus548\out\f2\`; the clone is removed and the sentinel was cleared after the two-part check.
- **Base:** `FBBOUND_PASS`, both pins 1, end counts 286/286.
- **Every earlier mutant** stays as your table in 4b says, including M_rst2 ending at 291/292. M_neqB and M_zge pass, as disclosed.
- **Harness edits on the R6 row itself:**
  - `||`: only the pin reds on M_eq.
  - Precharge 0 or 762: R6 reds.
  - Retargeting the drive, alone or with a new count: red (end 4096).
  - A **three-token** edit (drive timer 0 for 3810 ticks, and read `end2` from `[0]`) passes both pins with M_eq.

**1. Adjudication**

- **F1** UPHOLD. Measured: `--time` reds "measured timer t" on t1–t3 and `fbd_ran` reads `0`; a loop list of `0 1 2` gives `012`.
- **F2** UPHOLD, with a refinement. The pin catches LOAD_RUN and `--accrue` (381 and 305, measured). It cannot see CTRL_ON, because RATE never reads it, and cannot see an accrual shortened inside `free_run`; both belong to F4.
- **F3** UPHOLD. `add1("sp")` reads 0/0 and reddens only the range row.
- **F4** UPHOLD. It now holds a measured member: the three-token R6 edit. File it.
- **F5** The L2 grade and R6b are UPHELD. "Closes the class" is OVERTURNED; see question 3.
- **F6** UPHOLD. M_pct3 reads peaks `6103 1525 3051 1`.
- **F7** REFINE. The disposition is right and the warrant is wrong; see D3.
- **F8** UPHOLD. Re-measured.
- **F9–F20** UPHOLD. F10's case is N = 3052 = 4 × 763.
- **F21** UPHOLD. M_eq and M_cmp0 are one token each, measured.
- **F22** UPHOLD. (2^31 − 1) / 68,157,440 = 31.51 s.
- **F23** UPHOLD. R1 ×2 and R5 ×2, measured.
- **F24** UPHOLD. The addendum's own CTRL_ON channel line is also wrong and is corrected only in `f2_brief.md`, so that brief should be committed as an artifact.
- **F25, F26** UPHOLD.
- **F27** UPHOLD the withdrawal. Measured: R5 slowest-legal (2 ≠ 1) and R6's end counts 291/292.
- **F28** OVERTURN. M_lowonly does not test the finding, because it also blocks first arms. My table 3 reported it without saying so, and that let it settle the wrong question.
  - **The finding's actual mutant (M_upskip):** skip the store only on an upward re-arm, `if (d->timer[timer_nr] == NULL || (int) bound < d->pending_bound[timer_nr])`.
  - **Result:** `FBBOUND_PASS` with both pins; diff_footbridge 864/864; gate 14 41/41 with D = X = 1 on all four timers. The prologue's CONTROL write lowers the bound to 1, and the later LOAD write's raise is skipped.
  - **What it costs:** a guest that speeds a timer up keeps the old small bound and loses ticks.
  - **Disposition:** it is an added guard, outside DEPENDS-ON, so it is debt: disclose and file it, do not reject it.
- **F29–F31** UPHOLD.
- **F32** UPHOLD, independently re-measured. The comment's "each measured" list is accurate for the three edits it names. The three-token edit goes to F4 and gets filed.
- **D1** UPHOLD. The pin is measured to fail when it should.
- **D2** UPHOLD.
- **D3** REFINE.
  - **Not a stretch in outcome:** DEPENDS-ON never generates a guard added at an unguarded store.
  - **Wrong cited warrant:** "sits under no predicate" is not the warrant.
  - **The right warrant:** M_neqB and M_zge differ from base only at counts inside classes the body's `>=` already rows: 762 lies in {≥}, rowed at 4096, and 1..761 lies in {<}, rowed at 0. That is clause (e).
  - **Filed debt worth a cell:** M_zge's blind set, 1..761 owed at re-arm, is the commonest real re-arm state, so a third cell is worth filing.
- **D4** REFINE. R6b is right for M_cmp0. But R5 still compares only the maximum peak across timers, so a lowering on one timer at any of the six other configurations stays invisible. Per-timer R5 costs nothing.

**2. Which accepted dispositions are wrong: three.**
- F5's claim to close the class.
- F28's rejection. It was not an acceptance, but it was settled on the wrong mutant.
- F7/D3's warrant (the disposition itself stands).

The addendum's CTRL_ON line is a fourth wrong record, already corrected in your brief.

**3. What all nine of us missed: timer × re-arm case.**
- **The gap:** R6b closes the timer axis for the first arm only. Each R6 re-arm case runs on a single timer: count 0 on timer 0, 4096 owed on timer 2. The JOIN rule makes the timer index a floor axis here, because `nr` indexes both lvalues the guard reads. So each re-arm case is owed on all four timers, and two of eight are rowed.
- **M_eq_n2**, `==` on every timer except timer 2:
  - `FBBOUND_PASS` with both pins, IDENTITY 28.
  - diff_footbridge 864/864.
  - Gate 14 41/41 (3/3 on every timer).
  - At rung 3 on timer 1 (a 12207 Hz → 762 Hz CONTROL write): **4529 owed against a bound of 762**; HEAD reads 1.
  - **Grade: L2.** It is the M_eq breach this round already graded L2, on three of four timers, and the same measurement shows the case is reachable.
- **M_pend_n0**, M_pendguard exempted on timer 0:
  - Passes every row.
  - Gate 14 reads 13/13 on t1–t3, because the bound stays frozen at the first arm's 14.
  - That makes F5's closure text a wrong record (L4); the consequence is lost ticks, not an overflow.
- **M_upskip:** FILED (F28).
- **Repair, same row and same oracle:** run R6's two re-arm cases on all four timers (swap which timers play which case across two structs) and add one upward re-arm. Extend the pin to the new printed values. Gate 14's `[1, 762]` range reads over-bounding (1, 13) as green by design, and that is disclosed.

**Where I stand on my own findings.**
- M_eq_n2 is a breach: the round's own L2 case, now shown reachable on a timer R6 never re-arms.
- M_upskip, M_pend_n0 and the three-token harness edit are filings.

**Commands.**
- git-bash: the freeze (`out/f2/FROZEN.md5`), `git clone -q -c core.autocrlf=false` without `--shared`, the overlay, the two-part check, removal of the clone.
- WSL scripts:
  - `f2_build.sh` (runs `f2_gen.py`): gate-2-style compile for each mutant, plus the six harness edits.
  - `f2_rung3.sh`: runs `eq_rearm_probe.py small --timer 1` and the table-3 block driver.
  - `f2_upskip.sh`.
  - `pscheck.sh`.

`out/f2` holds no `.py` files. Skip `bin` when copying; everything else is 1.1 MB.
