OPUS548F_ALIVE
VERDICT: SHIP WITH CHANGES

The changes are wording only. I found no floor breach inside revision 4's enumeration. One mutant of the fix's own predicate passes every row and brings back the unbounded count at rung 3 (a guest can drive it into an unmodified emulator). It splits a cell that is already rowed rather than skipping one, so under the written floor rule it gets filed; question 3 gives the counter-argument.

**The tree changed while I ran.** At 08:17 the working tree took comment-only edits: the harness's R6 comment and the gate block's NOT CLAIMED text. `gate_offline.sh` did not change. I measured the brief's revision 4. Every code line and both pins are identical to the current tree, so the results stand for it.

**1. Gate 2's harness on revision 4. MEASURED.**
- **Setup:** compiled exactly as `gate_offline.sh` compiles it. Both pins were matched with the gate's own `grep -cxF` strings, read out of the frozen `gate_offline.sh`.
- **Against your `t4.out`:** all 23 rows we share match.
  - Base: `FBBOUND_PASS`, pins 1/1.
  - Red in R6: M_eq, M_idle, M_pendguard, M_frozen, M_eq_n2, M_pend_n0.
  - Red in R6 and R6b: M_idx0, M_pct3, M_cmp0.
  - M_rst2: red in one R5 case plus the R6 pin.
  - M_mask16: red in one R5 case only (lowest peak 49,868,928 at 50 MHz).
  - Pass, as disclosed: M_neqB, M_zge, M_upskip.
- **Mutants beyond your table:**
  - Red: M_x8, M_nr0, M_fclk, M_devtick, M_noceil, M_x2, M_lowonly, M_nobound.
  - M_en, M_en0, M_nper and M_f16 pass gate 2, as expected: those belong to the drain or to `fbboundmodes`.
- **In every run:** IDENTITY ok and R2 ran.

**2. The gate-14 block, verbatim. MEASURED.** Lines 1163–1252 equal the brief's added lines.
- **Base:** 41/41, D = X = 3 on every timer, and the new line reads `load=0x100 ctrl=0x88`.
- **M_nobound:** 16 red (bounded, range, verdict and exit rows on all four timers).
- **M_en0:** 12 red, on t1–t3.
- **CTRL_ON 0x88 → 0x80:** the timer pin reds on all four (`ctrl=0x80`) and `fbd_ran` reads `none`. The bounded, range, verdict and exit rows also red: backlogs were 3134–3626.
- **Label `FBDRAIN_BACKLOG_X` → `_D`:** only the split row reds (D appears twice, X is missing), as revision 4 claims.
- **Extra, CTRL_ON → 0xC8** (periodic mode plus the 256 prescaler): ONLY the timer pin reds; D = X = 3. This is the edit the new pin exists for. 0x80 is not that edit, because other rows catch it too.

**3. The enumeration. MEASURED.**
- **R6:** the printed owed counts show 0, 0, 8192, 8192 and then the swap. Every timer sits in both re-arm cells, each at its own rate.
- **R5:** requiring both the lowest and the highest peak pins all four timers at all seven cases. No cell is unrowed.
- **Mutants of the fix's own predicate, reset and store:** I built 18, 17 new plus M_mask16.
  - **All `FBBOUND_FAIL`:**
    - Predicate: `>`, `<=`, `!=`, swapped operands, `bound - 1`, the count index as `nr^1`, the bound index as `nr^1`, `3-nr` and `(nr+1)&3`, and `bound & 0xFFFF`.
    - Reset: a reset that subtracts the bound.
    - Store: index `^1` and a rotation, `+1`, `-1`, and the unclamped `(int) freq`.
    - M_mask16.
  - **R_bnd** (reset to the bound, so it owes B instead of 1): the verdict passes and only the R6 pin reds (end counts 762/1525/3051/6103 instead of 572…). The pin is the only thing that catches it. The mid-run comment's "exactness lives in gate 2's whole-line pin" is now accurate.
  - **P_win**, `count >= bound && count <= bound + 10000` (the fix's predicate qualified on its own operands):
    - Gate 2: `FBBOUND_PASS` with both pins 1; `diff_footbridge` 864/864; gate 14 41/41.
    - **Rung 3:** the guest arms at 195,312 Hz, leaves it unacked for 0.25 s, then writes CONTROL to drop to 762.94 Hz. It ends **49,603 owed against a bound of 762**; HEAD ends at 1.
    - My first rung-3 attempt capped the debt at phase A's own bound (12,207), so the window never engaged. The corrected run is the one reported.
    - **Why it escapes:** R6's owed cell uses a single debt, and 8192 sits inside the window for every rate.
    - **Grade:** it splits the "at or above the bound" cell at a value the body never tests. By the joint-cells rule that is clause (e), so FILE it. But this round graded `==`, also a split inside that cell, as L2 because of its consequence, and P_win has the same consequence. If that precedent governs, P_win is the breach.
    - **Closure:** the closure is finite and cheap. Owe the largest debt a correct build can hold (the pre-re-arm bound, at most 68,157,440) instead of 8192; every smaller window then reds.
    - **Disclosure owed:** the not-rowed list names guards that mutants add and indices read from other fields, not a qualified predicate. It should.

**4. Sentences still false.**
- **`CORRECTIONS.md` item 2:** "0x88 → 0x80 … the residue is 2 — bounded, in range, PASS" is false as measured: 8 of 8 arms read 3134–3626 and went red.
  - At 195 kHz every extra SIGALRM tick adds about 3005 to the count, so "2" holds only if exactly 260 signals land.
  - So the f2_brief sentence it "corrected" was right in practice, though not structurally.
- **R5 comment:** "hid behind timer 0's correct peak at every case here" is overstated. M_mask16 differs from base at one case of seven (50 MHz).
- **`c_brief` §2:** "re-armed owing 8192 (at/above)" is too broad. Only *past* the bound is rowed; *at* the bound is M_neqB's disclosed cell. The mid-run edit fixed the harness comment, but the brief still says it.
- **The block's "(measured)" for a control change** was arithmetic when it was written. My 0xC8 run now measures it.

**5. May the chain close?** Yes, under the written floor rule. I found zero breaches inside the enumeration after checking:
- the 8 R6 cells;
- the 28 per-timer R5 cells;
- the 18 new mutants and 26 earlier ones;
- the block with its instrument edits.

P_win is filed unless the adjudicator applies the `==` precedent. In that case it is the one breach, and the fix is one constant.

**My own apparatus error.** My build script printed `RESTORED_BINARY_IS_BASE=NO` because it compared a 32-character hash against `md5sum <` output. A direct md5 shows the restored binary equals base (6011d2f5…). I cleared the sentinel only after that direct check.

**Commands.**
- **WSL:**
  - `c_gen.py` and `c_build.sh`: the harness table, plus binaries for M_nobound, M_en0 and P_win.
  - `c_mkdrivers.py` and `c_blocks.sh`: the block runs and instrument edits.
  - `c_rearm_probe.py` (modes `big` and `big2`) via `c_big2.sh`: rung 3.
  - `c_dfb.sh` and `pscheck.sh`.
- **git-bash:** the freeze (`out/c/FROZEN.md5`, `PINS.txt`), the clone with `-c core.autocrlf=false`, the `cmp` checks, and cleanup.

The clone is removed and GXEMUL-SEC is untouched. Logs are in `_scratchpad\opus548\out\c\` (2.1 MB without `bin`, and no `.py` files).
