OPUS548D_ALIVE
VERDICT: SHIP WITH CHANGES

Revision 2 closes everything pass 2 found, and every row reddens under its named edit. One sealed prediction missed, in the safe direction. The one ask found a one-token edit to R6 itself that gives the `==` mutant a full gate-2 pass, pins included.

**1. Table 3 part 1: the final `diff_fbpending_bound.c` against base and 22 mutants. MEASURED.**
- **Setup:** HEAD plus the final text, with every overlaid file `cmp`-equal to the working tree. Compiled with gate_offline.sh's exact line against the clone's 222 objects, run at depth 2147487744, and grepped as the gate greps.
- **In every run:** IDENTITY 28, `R2 actually ran` = 1, and rows run = 30.

| mutant | FBBOUND | R6 | R6b | pin R6 | pin R6b |
|---|---|---|---|---|---|
| base | PASS | ok | ok | 1 | 1 |
| M_eq, M_idle | FAIL | FAIL (timer 2 peak 8192) | ok | 0 | 1 |
| M_pendguard | FAIL | FAIL (timer 0 peak 4096) | ok | 0 | 1 |
| M_frozen | FAIL | FAIL | ok | 0 | 1 |
| M_idx0 | FAIL | FAIL (owing 1) | FAIL (peaks 6103 1 1 1) | 0 | 0 |
| M_nobound, M_nr0, M_devtick, M_x2, M_x8, M_lowonly | FAIL | FAIL | FAIL | 0 | 0 |
| M_fclk, M_noceil | FAIL (R1/R5) | ok | ok | 1 | 1 |
| M_cmp0 | FAIL | ok | **FAIL** (peaks 762 762 762 762) | 1 | 0 |
| M_pct3 | FAIL | ok | **FAIL** (peaks 6103 1525 3051 1) | 1 | 0 |
| M_rst2 | **FAIL**: R5 "cats, slowest legal" (peak 2, want 1) | ok | ok | 1 | 1 |
| M_neqB, M_zge | PASS | ok | ok | 1 | 1 |
| M_en, M_en0, M_nper, M_f16 | PASS | ok | ok | 1 | 1 |

- **Scored against the sealed predictions:**
  - Hit:
    - M_cmp0 is red in R6b only.
    - M_pct3 is red in R6b.
    - M_neqB and M_zge pass, as the disclosed `fbbounddebt` cells.
    - Every earlier red mutant stays red, and base is green.
  - **Missed:** M_rst2 was predicted PASS and is RED, through one row, R5's slowest-legal case, where the bound is 1. The block's claim that reset-to-2 is "gate 2's" is therefore true, but it rests on that single row.
  - Not sealed: M_lowonly is red.

**2. Harness edits, on base and on M_eq. MEASURED.**

| edit | R6 row | FBBOUND | R6 pin |
|---|---|---|---|
| `&&` → `\|\|` on base | ok | PASS | 1 |
| `&&` → `\|\|` on M_eq | **ok** | **PASS** | **0 (red)** |
| precharge 4096 → 0, both binaries | FAIL (owing 0) | FAIL | 0 |
| precharge 4096 → 762, both binaries | FAIL (owing 762) | FAIL | 0 |

The `||` edit is caught only by the gate_offline pin, which is its job. At a precharge of 762, `==` fires too, and it is the row's own `owed2 == 4096` clause that catches it.

**3. The gate-14 block, verbatim (lines 1163–1252), run with lib.sh. MEASURED.** Row codes: A = the "asked for 4 s at 762.94 Hz" row, M = "the run measured timer t", R = "backlogs in [1, 762]", B/P/X = bounded, verdict, exit.

| run | red rows per timer | D/X | fbd_ran | result |
|---|---|---|---|---|
| base | none | 3/3 | 0123 | PASS 41/41 |
| M_nobound | B R P X on t0–t3 | 3051/3051 | 0123 | FAIL 16 |
| M_en0 | t0 none; B R P X on t1–t3 | t1–t3 3/3051 | 0123 | FAIL 12 |
| M_cmp0 | none | t1–t3 1/1 | 0123 | PASS (gate 2's R6b catches it) |
| `--time` on base | M on t1–t3 (TIMER=0 base=0x300) | 3/3 | **0 (red)** | FAIL 4 |
| loop list `0 1 2` on base | t3 absent | 3/3 | **012 (red)** | FAIL 1 of 31 |
| `--accrue .4`, base and M_nobound | A only (uncapped 305) | **375/375 on both** | 0123 | FAIL 4 |
| LOAD_RUN 0x800, base / M_nobound | A only (uncapped 381) | 1/1 and 381/381 | 0123 | FAIL 4 |
| `add1("sp")`, base and M_nobound | R only (0/0) | 0/0 | 0123 | FAIL 4 |

- **The accrual and rate edits:** the bound-removed binary reads the same range as base, so row A is the only thing standing between those edits and a silent pass. It works.
- **Not in the block, only in the addendum:** its claim that the UNCAPPED line sees CTRL_ON is false. RATE is EMU_HZ / (LOAD_RUN × 256), which does not read CTRL_ON. A CTRL_ON edit is still caught, by rows B and R.

**4. The one ask: the smallest edit that breaks a claim and passes every row. MEASURED.**
- **The edit:** one token in R6, retargeting the post-re-arm drive from timer 2 to timer 0: `drive(r6, 2, 4096, &peak2, &trough2);` → `drive(r6, 0, …)` (line 309 of the final file).
- **Result:** base, M_eq and M_idle each give `FBBOUND_PASS`, the R6 pin 1, the R6b pin 1, and IDENTITY ok.
- **Why:** the printed line still reads "timer 2 owing 4096 peak 762", because `owed2` is sampled before the re-arm and `peak2` is now timer 0's peak.
- **What it breaks:** the harness comment's claim that "an edit to this row … cannot hand `==` its pass back". It is not disclosed; the comment names only `||` and a smaller precharge.
- **Cheapest repair (not built):** sample the count again after the second drive and pin that value, or print the timer index each peak came from.
- **Severity:** it is an edit to the row itself, not to product code, so it can be disclosed rather than rowed if the owner prefers.

**Commands.**
- **git-bash:** the freeze, done before table 1 (md5s in `out/p3/FROZEN.md5`), the block extraction (`sed -n '1163,1252p'`), the HEAD-plus-block check, `git clone -q -c core.autocrlf=false …`, the overlay copies, the two-part clearance, and removal of the clone.
- **WSL**, run as `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash …/scripts/<name>`:
  - `p3_gen.sh` (runs `p3_gen.py`): 22 mutants.
  - `p3_build.sh` (runs `p3_hedits.py`): base, the harness table, the edits, three binaries, restore and rebuild.
  - `p3_hdrv0.sh`: the part 4 edit.
  - `p3_block_runs.sh` (runs `p3_mkdrivers.py`): the block runs.
  - `pscheck.sh`.

**State.**
- The sentinel was cleared only after the two-part clearance: the sources equal the working tree, and the binary is newer than the source with md5 equal to base.
- Every instrument is unchanged against the working tree after the runs.
- The clone is removed, no processes are left, and GXEMUL-SEC is untouched.
- `out/p3` holds no `.py` files. Skip `bin` (217 MB); the logs are 2.0 MB.

Files are in `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\opus548\out\p3\`:
- `table3_part1_part2.txt`
- `table3_part3_blocks.txt`
- `part4_H_drv0.txt`
- `gate14\`, `runs\`, `frozen\`, `mutants\`
