OPUS548C_ALIVE
VERDICT: SHIP WITH CHANGES

Both tables match what the diff claims, and M_x8 now backs "any B >= N, which reads N". But a one-token edit to `dev_footbridge.c` passes every row in the battery and falsifies the contract's claim that lowerings are gate 2's job.

**1. Table 2 part 1: the final R6both against 15 mutants. MEASURED; no difference from my pass-1 R6both column.**
- **Setup:** the clone is HEAD plus the final text of the four files; I checked each against the working tree with `cmp`. The harness was compiled with gate_offline.sh's exact line against the clone's 222 objects and run at depth 2147487744.
- **Result:** IDENTITY is ok with 28 rows in every run.

| mutant | verdict | R6 | R6b | R6 peaks (t0 / t2) |
|---|---|---|---|---|
| base | PASS | ok | ok | 762 / 762 |
| M_eq | FAIL | FAIL | ok | 762 / **8192** |
| M_pendguard | FAIL | FAIL | ok | **4096** / 762 |
| M_idle | FAIL | FAIL | ok | 762 / 8192 |
| M_frozen | FAIL | FAIL | ok | 4096 / 8192 |
| M_idx0 | FAIL | FAIL | FAIL | 762 / 1 |
| M_nobound, M_nr0, M_devtick, M_x2 | FAIL | FAIL | FAIL | as before |
| M_fclk, M_noceil | FAIL (R1/R5) | ok | ok | 762 / 762 |
| M_en, M_en0, M_nper | PASS | ok | ok | as before |
| M_x8 (new) | FAIL | FAIL | FAIL | 4096 / 6103 |

**2. Table 2 part 2: the gate-14 block, extracted verbatim. MEASURED.**
- **Setup:** lines 1163–1228 of the working tree. They equal the brief's `+` lines byte for byte, and HEAD plus the block differs from the working tree only in the other unit's crime_width hunk.
- **How it ran:** lib.sh was sourced as gate_arm.sh does, the stub was written with gate_arm.sh's own lines, and LOGDIR was private.
- **Row codes:** B = bounded at cap, P = verdict PASS, X = exit status.

| binary | red rows per timer | D / X backlog | block result |
|---|---|---|---|
| base | none | 3 / 3 on all four | PASS 28/28 |
| M_nobound | B P X on t0–t3 | 3051 / 3051 | FAIL 12/28 |
| M_en | B P X on t0–t3 | 3 / 3051 | FAIL 12/28 |
| M_en0 | t0 none; B P X on t1–t3 | t0 3/3; t1–t3 3 / 3051 | FAIL 9/28 |
| M_fclk | B P X on t0–t3 | 3 / 3051 | FAIL 12/28 |
| M_x8 | B P X on t0–t3 | 3051 / 3051 (reads N) | FAIL 12/28 |
| M_eq | none | 3 / 3 | PASS (disclosed) |
| M_devtick | none | 1 / 1 | PASS (disclosed) |
| M_nper | none | 3 / 3 | PASS (disclosed) |

- **Rows that never went red:** "reached a verdict", "controls", "twelve ids" and "clocks alive" stayed green throughout, as the PRETABLE CHANNEL section predicts. Each run took 66–67 s.

**3. The adversarial ask. MEASURED.**
- **The smallest escape:** one token in `footbridge_pending()` of `dev_footbridge.c`, `d->pending_bound[nr]` → `d->pending_bound[0]` (M_cmp0).
  - Gate-14 block: PASS 28/28. Timer 0 reads 3/3; timers 1–3 read 1/1, pinned at timer 0's unarmed seed bound of 1.
  - Gate 2: `FBBOUND_PASS`, and `diff_footbridge` passes 864/864.
- **What it breaks:**
  - The contract's line "A LOWERING … All of those are gate 2's": this lowering is invisible to gate 2.
  - R6b's own stated property, "each timer carries its OWN bound". R6b cannot see a cross-timer read because timers 0 and 1 both end at 762 Hz.
  - It does not wrap. It is the lost-ticks class R5/R6b exist for.
- **Disclosure:** not disclosed anywhere.
- **Repair, measured:** arm R6b's timer 1 at load 128 (1525 Hz) and want 1525. M_cmp0 goes red (peak 762, want 1525); no mutant goes from red to green; IDENTITY stays 28. File: `out/p2/r6b_distinct_repair.txt`.
- **Instrument, one hex digit:** in `fbpending_drain_probe.py`, `LOAD_RUN … else 0x100` → `0x800` (95.37 Hz).
  - With the bound removed, the block reads D/X = 381 on all four timers and passes 28/28. The claim "CATCHES the bound REMOVED" falls.
  - Nothing pins the rate or N. The LOAD clause discloses starvation only.
  - The same mechanism applies to `--accrue 4` → `.4` in the block itself (reasoned, not run).
  - A cheap row would catch the rate edit and the `--accrue` edit, not an accrual shortened inside the probe or starvation: a whole-line match on `  UNCAPPED prediction: backlog = 3052`. It reads 1 on the real probe and 0 under the edit.

**4. Wording that is false or undisclosed.**
- **M_f16:** a bound skipped while FCLK_16 is set passes the block (28/28, 3/3) and both gate-2 differentials. The NOT CLAIMED list names only PERIODIC, so `fbboundmodes` should state the whole class: any control value that no instrument driving `footbridge_pending()` sets. That includes FCLK_16 (measured) and EXTERNAL (reasoned).
- **"neither this probe nor gate 2 ever sets that bit":** the reason is false. `diff_footbridge.c:129` and `:642` set PERIODIC. The conclusion still holds only because that file makes 0 callback calls.
- **"the smallest edit still passing the rung-3 probe":** this superlative in the rewritten device comment is false. M_eq and M_cmp0 are one token each and both pass the block.
- **Reset-to-0 "cannot show at all" (reasoned):** it reads CLOCK_DEAD, a red, when N ≡ 0 mod 763.
- **Confirmed:** the gate_offline citation file exists.

**Commands.**
- **git-bash:** freeze with `sed -n '1163,1228p'` and `cp` (md5s in `out/p2/FROZEN.md5`), the brief cross-check, `git clone -q -c core.autocrlf=false …`, the overlay copies, two-part clearance, removal of the clone.
- **WSL**, run as `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash …/scripts/<name>`:
  - `p2_gen.sh` (runs `p2_gen.py`): 17 mutants from the final file.
  - `p2_build.sh`: configure/make, the harness per mutant, 10 binaries, restore and rebuild.
  - `p2_block_runs.sh`: runs `drive_548.sh`.
  - `p2_instmut.py`, `p2_dfb.sh`, `p2_r6b_run.sh` (runs `p2_r6b_variant.py`), `pscheck.sh`.

**State.**
- The sentinel was cleared only after the two-part clearance: the source equals the final text, the binary is newer than the source, and its md5 equals base.
- The clone is removed, no gxemul or probe processes are left, and GXEMUL-SEC is untouched.
- The frozen instruments still equal the working tree after all runs.
- When copying into artifacts:
  - Skip `out/p2/bin` (177 MB of binaries); everything else is 2.2 MB.
  - `out/p2` holds no `.py` files. The frozen `.py` instruments are in `p2/instruments` and `p2/regress_*`, so check_probe_wiring.py will not see unclassified probes.

Files are in `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\opus548\out\p2\`:
- `table2_part1_and_builds.txt`
- `table2_part2_blocks.txt`
- `r6b_distinct_repair.txt`
- `diff_footbridge_p2.txt`
- `gate14\` (per-binary logs)
- `runs\`, `mutants\`, `frozen\`
