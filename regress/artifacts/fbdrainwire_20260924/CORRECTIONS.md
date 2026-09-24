# #548 -- corrections to this directory's own dated artifacts

`PRETABLE.out`, `PRETABLE_ADDENDUM_r2.out`, `p1_brief.md`, `p2_brief.md` and `f2_brief.md` are left exactly as they were
written: each file's mtime is the proof of what was known and predicted BEFORE the measurement that followed it.  So the
false sentences found in them afterwards are corrected HERE, each with who found it and how.

1. `PRETABLE_ADDENDUM_r2.out`, NEW ROWS: *"asked for 4 s at 762.94 Hz (3052)  LOAD_RUN or CTRL_ON changed in the probe"*.
   **CTRL_ON is not read by the pinned line.**  The probe prints RATE * ACCRUE_S, and RATE = EMU_HZ / (LOAD_RUN x 256):
   no CTRL_ON term (the Opus seat, table 3).  Revision 4 pins CTRL_ON separately: the probe's `FBDRAIN_TIMER` line now
   carries `load=0x100 ctrl=0x88`, and gate 14 pins the whole line.
2. `f2_brief.md`, section 4: *"A CTRL_ON edit is caught by the bounded and range rows instead."*  grok (SF2) called
   it false by arithmetic -- 0x88 -> 0x80 runs the device at 195312 Hz and, over exactly the 260 signals the idle runs
   delivered, leaves a residue of 2 -- and this file first recorded that verdict.  **The Opus seat then MEASURED it
   (closing pass): 0x80 read 3134-3626 on all eight arms and every bounded/range/verdict/exit row went RED**, because
   at 195 kHz each extra signal adds about 3005 ticks.  So the sentence was right in practice and wrong structurally.
   The edit ONLY the new pin catches is 0xC8 (periodic mode plus the prescaler): measured, D = X = 3 and the
   `FBDRAIN_TIMER ... ctrl=0x88` pin is the sole red row.  Revision 4's `load=0x100 ctrl=0x88` pin stands.
3. `PRETABLE_ADDENDUM_r2.out`, SECTION 4 CORRECTED: *"Its own budgets bound it (free_run's 20 s prompt waits, the 30 s
   drain, close()'s 20 s drain + 10 s reap)."*  **False** (codex, dedicated and panel jobs, SF2; each with a fake-clock
   fixture): `Session.wait()` restarts its timeout whenever output arrives, so continuous output without a prompt keeps
   it waiting indefinitely -- a 20 s wait was still running at 120 simulated seconds.  No external watchdog wraps the
   probe in gate 14 either.  Recorded, not fixed: a probe-logic change, filed under `fbharnessedits`.
4. `f2_brief.md`, F28: *"REJECTED, and table 3 settled it by measurement: M_lowonly ... is RED."*  **Settled the wrong
   question** (the Opus seat and codex, SF2): M_lowonly also blocks FIRST arms (calloc's 0), so its failure says nothing
   about an UPWARD re-arm.  The mutant that tests it -- M_upskip, the store skipped only on a raise after a successful
   first arm -- passes every row in the battery (the Opus seat, measured).  Filed under `fbbounddebt`.
5. `f2_brief.md`, F5 and F6: *"the repair closes the class"* and *"R5 itself is unchanged"*.  **Both overturned**
   (the Opus seat: M_eq_n2 and M_pend_n0 measured passing everything; codex: a per-timer store mask hidden by R5's
   maximum).  Revision 4: R6 builds every timer in both re-arm cells at distinct rates, and R5 checks every timer.
6. `c_brief.md`, section 2: *"re-armed owing 8192 (at/above)"*.  **Only PAST the bound is rowed** (8192 exceeds every
   new bound); AT the bound is M_neqB's disclosed cell (the Opus seat, closing pass).  The harness comment says so now.
7. **A predicate narrowed to a WINDOW on its own operands passes every row** -- `count >= bound && count <= bound + W`
   with W wide enough to hold the owed 8192 (the Opus seat, closing pass, MEASURED: W = 10000 left 49603 owed against
   a bound of 762 at rung 3; HEAD 1).  Graded clause (e): it splits the ROWED past-the-bound cell at a value the body
   never tests, where `==` (L2) had escaped because that cell was not rowed at all.  Disclosed in R6's comment, filed
   under `fbbounddebt` with its closure: owe the largest debt a correct build can hold instead of 8192.
