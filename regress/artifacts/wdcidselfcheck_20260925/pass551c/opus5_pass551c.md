VERDICT: SHIP WITH CHANGES

**Your question 1 does not come back zero.** A 2-character edit, and separately a one-statement edit, keep every gate-2 check green while covered rows can no longer fail. A small change to the verdict closes both, and I measured it byte-identical to `MINE_c.c` on 9 device variants. Separately, four of the new sentences are false.

How I measured: a WSL `/tmp` copy of `MINE_c.c` (765f71d8), 160 serial `-O2` builds. "Gate 2" means the 73 wdc checks extracted verbatim from `gate_offline.sh`, plus H, G, and the self-mutant lane using `selfmutant.py`'s logic. Outputs, scripts and 17 sentinel-checked logs are in `regress/artifacts/wdcidselfcheck_20260925/opus551_measured_c/`. The tree and `MINE_c.c` are untouched.

1. **(Q1) Two edits outside the disclosed classes (MEASURED).**
   - **The 2-character edit** changes the new reconciliation line to `if (cmp_fails >= failures) failures -= cmp_fails;` (it was `>` and `=`).
     - When only covered rows fail, the two counts are equal and the subtraction takes `failures` to 0.
     - A healthy run subtracts 0 from 0, so nothing changes.
     - An inline failure (such as the self-mutant's row 125) still makes the run red, so the lane stays OK.
   - **The one-statement edit** inserts `failures -= cmp_fails;` right after the reconciliation line. This is a reset of `failures` alone — the very thing the new sentence says is caught.
   - **Effect of either edit:** on the drop-oldest, DRQ-dropped and word-57 device variants the run prints `128 rows, 0 failures` and `WDC_IDENTIFY_PASS`, and gate 2 is green. Silenced rows include "R2 anchor: inbuf[tail] survives", "R6 liveness: DRQ asserted" and "threshold: >>8 byte reaches 255".
   - **Denominator:** 15 edit shapes, each run on the real device and on three defects only covered rows see, each with its lane:
     - resets placed before the reconciliation: `failures`, `cmp_fails`, and both;
     - `chk()`'s `cmp_fails ++` deleted, alone and together with a `failures` reset;
     - the reconciliation line deleted, made unconditional, flipped to `<`, given `-=` alone, and given `>=` with `-=`;
     - a subtraction placed before it, and after it;
     - `failures = 0` placed after it;
     - the `!sc_g` line deleted.
   - **Green on all three defects:**
     - the both-tally reset (disclosed);
     - the two edits above.
   - **Green on the two `chk()` defects only:** deleting `chk()`'s `cmp_fails ++` plus a `failures` reset. That is two edits and not "a reset of both tallies" as the disclosure words it. The self-check never observes `cmp_fails` changing.
   - **Closure (MEASURED):** make the verdict and exit status read `cmp_fails` directly: `if (failures == 0 && cmp_fails == 0 && sc_g)` and `return (failures || cmp_fails || !sc_g) ? 1 : 0;`.
     - Both edits then red. The trailer can still say 0 failures, but the FAIL token reds gate 2's verdict row.
     - The whole log and exit code match `MINE_c.c` on 9 device variants.
   - **Also cheap (MEASURED):** require the exact `cmp_fails` change in the self-check as well. That reds the increment-deletion pair (4 of 13 probes wrong), and the log stays whole-log identical.
   - After both changes, the both-tally reset stays green, so it remains correctly disclosed.

2. **(Q2) Four new sentences are false.**
   - **"only they touch it" / "which only they touch" (MEASURED, by grep).** The self-check writes `cmp_fails = sc_cf;` at three lines. It should say "only they increment it".
   - **"A reset of `failures` ALONE after the comparators is not among them" (MEASURED).** It is false when the reset is placed after the reconciliation (finding 1). It holds only for resets placed before it.
   - **"an edit that keeps those answers and changes the rest keeps every gate-2 row green" (block comment and bullet) (MEASURED).** As a universal claim it is false: `failures = 0;` after the covered rows keeps the self-check's answers and reds gate 2. Your own MINE_reset on drqring shows rc=1, and my run agrees. It should say "can keep".
   - **"Measured on #551's passes" (READ).** For "an edit of this block itself", no measured green shape exists. The only block edits measured (deletion, and forced-failure removal) are caught.
   - **True:** "each operand zero and past 32 bits", "each disjunct alone and on either side of its want", and the trailer comment's "at least as many".

3. **(Q4) No healthy run changes beyond the SELFCHECK lines (MEASURED).**
   - `MINE_c.c` matches HEAD's harness line for line, apart from the SELFCHECK lines, on 7 device variants. It matches `MINE_b.c` the same way on 9, including the failing trailers.
   - The reconciliation never fires on an untampered run. The `!sc_g` line changes only the trailer of a run whose self-check is broken.

---
*Recorded by the main loop: agent a088149d37f1fac24 (resumed for #551c's own pass), final text by claude-opus-5-5 at 2026-09-25T22:23:18.088Z UTC (`agent_models.py`).  Badge s.*
