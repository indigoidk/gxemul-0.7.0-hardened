OPUS_SEAT_ALIVE_20260925_551d
# CHECKPOINT -- 2026-09-25 ~16:45 (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT: SHIP WITH CHANGES

The code holds: no single edit outside the disclosed classes escapes, and both #551c escapes are now red. The changes needed are to the disclosure's wording. Four edits of two changes each, plus one three-edit combination, keep gate 2 green, and "a reset of BOTH tallies" does not describe them.

How I measured: a WSL `/tmp` copy of `MINE_d.c` (e0c3399b) and serial `-O2` builds. I swept 33 shapes, each on the real device and on three device variants that only covered rows see: dropold (`chk()` comparison rows), drqring (`chk()`'s 0/1 rows) and w57hi (`row_cmp()` rows). "Gate 2" is the 73 extracted wdc checks, H, G, the PASS token, and the self-mutant lane following `selfmutant.py`'s logic. Everything is saved in `regress/artifacts/wdcidselfcheck_20260925/opus551_measured_d/`. The four "move" logs legitimately end after the PASS/FAIL line; `NOTE_move_logs.txt` explains why.

**1. Q1, the floor question (MEASURED).**
- **Single edits: all 24 are accounted for.** Every one outside the disclosed classes is red on all three device variants. That covers:
  - `failures` reset before or after the reconciliation line, a `cmp_fails` reset, and a subtraction before or after it;
  - the reconciliation deleted, made unconditional, flipped to `<`, rewritten `-=`, or rewritten `>=`/`-=`;
  - the `!sc_g` line deleted;
  - the verdict's `cmp_fails` term dropped, made `>= 0`, or replaced by `failures == cmp_fails`;
  - the return line's `cmp_fails` term dropped, and the trailer printing `failures - cmp_fails`;
  - `chk()`'s `cmp_fails ++` deleted (now red at the self-check);
  - the new self-check check weakened alone, the covered calls moved alone, `uint16_t` operands, and the sum form.
- **Disclosed single edits are still green, as disclosed:** `want-165` (dropold), the post-increment rows test (dropold, drqring), and the `row()` feed edit (w57hi).
- **Your three #551c escapes are now red.** The reconciliation `>=`/`-=` edit and the subtraction after it both print `0 failures` but `WDC_IDENTIFY_FAIL`. The increment-deletion pair reds at the self-check.
- **Two-edit shapes green on the covered-only device variants.** None of them resets `cmp_fails`:
  - a. delete the verdict's `cmp_fails == 0 &&`, and add `failures -= cmp_fails;` after the reconciliation line;
  - b. the same verdict edit, plus the reconciliation rewritten `>=`/`-=`;
  - c. the verdict becomes `failures == cmp_fails && sc_g`, and the trailer prints `failures - cmp_fails`;
  - d. **positional:** move `row_ring_occupancy_sound();` after the PASS/FAIL printf, and change the identity pin from 128 to 104. This is green on dropold and drqring: the 24 `chk()` rows print their FAIL lines after the token.
- **A three-edit shape is also green (the block-edit class):** weaken the new `cmp_fails` check from `!=` to `>`, delete `chk()`'s increment, and reset `failures`. Green on dropold and drqring.
- **Rows silenced** include "R6 liveness: DRQ asserted", "R2 anchor: inbuf[tail] survives" and "threshold: >>8 byte reaches 255".
- **Optional fix for (d) (MEASURED):** have the last self-check require `chk()` 24 and `row_cmp()` 8 calls. The move-and-re-pin then prints `WDC_IDENTIFY_FAIL`, and the whole log is identical to `MINE_d.c` on 5 device variants. My prototype prints no FAIL line explaining this, and a real implementation should. It pins two counts the way the identity row pins 128, so this is your call.

**2. Q2, your dispositions: 0 overturned, 4 refined (F1, F6, F9, F12), the rest upheld.**
- **F1 REFINE.** The fix is right: every single edit of `failures` is red wherever it sits. But editing `failures` together with the verdict's `cmp_fails` term escapes (shapes a–c). Disclose "two coordinated edits, one per tally path", not only "a reset of both".
- **F2 UPHOLD.** `cmp_fails ++` occurs twice: :520 in `row_cmp()` and :4870 in `chk()`.
- **F3 UPHOLD** (measured, as above).
- **F4 UPHOLD.** Deleting the increment now reds the self-check (2 failures on the real device). The new check is itself a line in the self-check block, and weakening it gives the three-edit escape — see F6.
- **F5 UPHOLD.**
- **F6 REFINE.** The block-edit class is now measured green, so "(reasoned: the block edits measured so far are caught)" is overtaken.
- **F7 UPHOLD. F8 UPHOLD.**
- **F9 REFINE.** The first `cmp_fails ++` (:520) is in `row_cmp()`, not `chk()`; neither is in `row()`. The rejection stands, but the location it states is wrong.
- **F10 UPHOLD. F11 UPHOLD** (the phrase is at :5649).
- **F12 REFINE.** None of srstbit's eleven failing rows goes through `chk()` (all are inline rows, measured on pass 2), so "some" should read "none".
- **F13 UPHOLD.**
- **F14 UPHOLD (MEASURED).** The sum form answers all 13 probes right and still reds w57hi; it misses only compensating pairs.
- **F15 UPHOLD. F16 UPHOLD.**
- **D1 UPHOLD.** Walked the table: got57 is wrong alone below its want at probes 0 and 4 and above it at 6; got60 below at 1 and 5, above at 7.
- **D2 UPHOLD. D3 UPHOLD.**

**3. Q3, the reconciliation line (MEASURED): not a liability.**
- Deleting it alone leaves every covered defect red.
- It does real work in one case. With the verdict's `cmp_fails` term deleted, a `failures = 0;` placed before it is undone (red); that combination only goes green if the line is deleted too (three edits).
- Its protection depends on placement: shape (a) puts the subtraction after it.
- Its comment should say it protects the printed count, not the verdict.

**4. Q4, false sentences: none false as written.**
- **Overtaken (see F6):** "(reasoned: the block edits measured so far are caught)" and the gate-2 bullet's "(reasoned)".
- **Incomplete:** "A reset of BOTH tallies is, and is disclosed" is true but does not cover shapes a–d. The general sentence ("CAN keep every gate-2 row green") covers them in principle; the list should name them.
- **Checked and true:** "only they increment it", "exact change in `failures` and in cmp_fails … restoring rows, failures and cmp_fails", "got both below and above its want", "each operand zero and past 32 bits", and "wherever it sits".

**5. Healthy runs (MEASURED).** Output matches HEAD's harness line for line, apart from the SELFCHECK lines, on 7 device variants. It matches #551c the same way on 9, with the same exit codes.

**6. Missed by everyone, including me:** shape (d). The identity row pins the row count at a point before the verdict, and nothing stops covered rows from running after it. No seat raised it before this pass.

---
*Recorded by the main loop: agent a088149d37f1fac24 (resumed for #551d's own pass), final text by claude-opus-5-5
(`agent_models.py`: status clean, every run opus-5-5).  Badge s.  The notification rendered `<`, `>` and `&` as HTML
entities; they are restored here to the characters the seat wrote.*
