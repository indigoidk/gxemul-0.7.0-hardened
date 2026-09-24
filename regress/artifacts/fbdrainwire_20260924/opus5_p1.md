OPUS548_ALIVE
# CHECKPOINT -- 2026-09-24 ~03:20 (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT: PROCEED WITH CHANGES

The wiring is worth doing. The drain probe's arm X is the only thing in the battery that kills a bound that applies only while the timer is enabled; gate 2 is blind to it (measured). But as written the proposal checks one timer, uses three aggregate rows, and carries a contract with two false sentences.

**1. Test-first half: MEASURED, and the prediction held.**
- **Setup:** HEAD bead6ad9, built in a scratch clone. I ran exactly `python3 -u fbpending_drain_probe.py <bin> <stub> --expect-cap 762 [--timer N]`, using the stub written the way gate_arm.sh's STUB block writes it (bytes `00 00 a0 e1`).
- **HEAD, default and `--timer 0,1,2,3` (5 runs):** `FBDRAIN_CONTROL=OK`, `BACKLOG_D=3`, `BACKLOG_X=3`, `CLOCK_DEAD=` (empty), `BOUNDED=YES (cap asserted: 762)`, `VERDICT=PASS`, exit 0.
- **Mutant with the bound removed, all four timers:** `D=3051`, `X=3051`, `VERDICT=FAIL`, exit 1.
- **Why the count is 3051:** it is exactly floor(4.000 s × 762.94). The delivered tick count follows the SIGALRM clock (260 signals), not the harness's 4.02 s. Every idle run gave 3051.
- **PROBE_WALL is never printed when `--expect-cap` is set.** The probe calls `sys.exit` at the verdict, before the print: 0 of 4 capped logs have the line. The report-only run printed `PROBE_WALL=16.7s`.
- **Cost:** 16.7 s per run measured externally, so four timers take 66.8 s.

**2. Q1, premise audit.**
- **The arithmetic is right.** (int)762.939453125 = 762. The ceiling (68,157,440) does not engage. After the fix the counter ranges over [1, 762], so 762 is the tightest cap that cannot false-fail. `-E cats` gets 50 MHz only because no `-I` is given.
- **The probe does arm other rates.** All three of these happen in the single-stepped prologue, while timer callbacks are stopped:
  - LOAD←0x12345678 under DEVINIT's control 0x40: 14.58 Hz, bound 14 (this is also where the struct timer is created).
  - CONTROL←0x88: 0.057 Hz, bound 1.
  - LOAD←256: 762.94 Hz, bound 762.
  - No tick lands during those transients: N is exactly 3051.
- **There is a fourth rate:** the FREEZE sets the bound to 1 for the entire drain. That is what causes finding 5.
- **Loaded host (probe and emulator pinned to one core with competing busy loops):**

  | busy loops on the core | bound-removed mutant (D/X) | HEAD (D/X) |
  |---|---|---|
  | 3 | 3049/3052, FAIL | 5/30, PASS |
  | 12 (about 1/13 of a core) | 1183/1183, FAIL (1.55× margin) | 385/379, PASS |

- **So "always exceeds 762" is not guaranteed.** When the emulator is starved it accrues fewer ticks. The failure mode is losing teeth silently, never a false red. Say so in the contract.

**3. Q2: one timer is not enough. MEASURED.**
- **The brief's premise is wrong.** A per-timer defect does not need a callback-level edit. `footbridge_pending` takes `nr`, so one conjunct inside it is enough.
- **`if (nr == 0 && …)`:** passes timer 0 (3/3) and fails timers 1–3 (3051). Gate 2 catches it anyway.
- **The case that matters:** `if ((nr == 0 || (d->timer_control[nr] & TIMER_ENABLE)) && …)`.
  - Passes on timer 0 (3/3) and fails on timer 1 (X=3051).
  - Both gate 2 differentials pass: diff_fbpending_bound gives `FBBOUND_PASS`, diff_footbridge gives 864/864.
  - It breaks the clock again, as #442 did, at rung 3: 45 s disabled at 50 MHz on timer 1 gives `CLOCK_DEAD=X`. HEAD under the same command reads 3485 and is alive.
- **Consequence:** with a timer-0-only row, nothing in the battery sees this. Run all four timers, for about 50 s more.

**4. Q3: yes, single edits get past the proposed rows and bring #442 back. MEASURED.**

| edit | drain probe (proposed rows) | gate 2 | brings the dead clock back? |
|---|---|---|---|
| `!(d->timer_control[nr] & TIMER_MODE_PERIODIC) &&` (bound skipped in periodic mode) | **PASS on all 4 timers** (3/3) | **PASS in both differentials** | yes, rung 3 |
| Bound moved from the callback into DEVICE_TICK's enabled branch (two hunks) | **PASS on all 4 timers** (1/1) | FAIL (R1/R2/R5/R6) | yes, rung 3 |
| `(d->timer_control[nr] & TIMER_ENABLE) &&` | FAIL, and only through arm X (3/3051) | **PASS (blind)** | yes, rung 3 |
| `bound = freq * 2.0` | PASS (1/1) | FAIL (R5/R6) | no |
| Ceiling deleted | PASS | FAIL (R1/R5) | no (see finding 8) |

- **The periodic-mode edit gets past every row in the battery.** Neither instrument ever sets PERIODIC, FCLK_16 or EXTERNAL: the probe uses 0x88 and 0x00, gate 2 uses 0x80 and 0x88. Yet DEVINIT resets every timer to periodic mode.
  - A scratch copy of the probe with one constant changed to add 0x40: HEAD passes (3/3), the mutant fails (D=3051).
  - With that variant, `--fast --accrue 45 --only D` gives `CLOCK_DEAD=D`; HEAD reads 3455 and is alive.
  - This is coverage debt, outside the carrier's DEPENDS-ON enumeration. Disclose it and file it. The cheapest fix is one periodic case in `diff_fbpending_bound.c`'s R1 table.
- **I predicted the FCLK_256-only conjunct would also get through. It does not:** arm X's CTRL=0 write clears that bit too (X=3051 on all four timers), and gate 2 catches it as well.

**5. The contract and the probe header make false claims. MEASURED.**
- **"Catches any RAISE above 762" is false.** What the rows see is ((N−1) mod B)+1, so a raised bound below the tick count wraps around: doubling the bound (B=1525) reads 1/1 and passes.
- **The contract leaves out** the DEVICE_TICK placement and the control-register axis (finding 4).
- **Arm X's "PLACEMENT DISCRIMINATOR" text is false.** The DEVICE_TICK mutant reads X=1 and passes. The freeze's LOAD write sets the bound to 1, so any clamp outside the callback collapses the backlog before it is counted. What X actually catches is a bound that depends on control bits X's CTRL=0 write clears (the enable-only and FCLK_256-only bounds).

**6. Q4: row design.**
- **Every mutant this probe caught shows up in the VERDICT row alone.** In every run, `VERDICT=PASS` held exactly when the exit code was 0, CONTROL was OK, CLOCK_DEAD was empty and both backlogs were ≤ 762. Rows 1 and 3 add attribution only.
- **Row 3 is dangerous if written as an empty-string compare.** `v=$(sed -n 's/^FBDRAIN_CLOCK_DEAD=//p' log); [ "$v" = "" ]` is green on a log that has no such line at all (I demonstrated this). Use `grep -cx 'FBDRAIN_CLOCK_DEAD=' = 1`.
- **The brief quotes only the first 3 lines of a roughly 90-line block.** Idioms it did not name:
  - a completion guard. The probe has no `*_DONE` line; with the cap set, `grep -c '^FBDRAIN_VERDICT=' = 1` can serve.
  - checks per named control row plus a pinned denominator. There are 12 rows: R0 C1 C2 A1 A2 E H1 H2 T L1 L2 P. `CONTROL=OK` is an aggregate and stays OK if a row is deleted from the probe.
  - xscale's `|| xrc=$?` exit-status row.
  - `grep -cx 'FBDRAIN_BOUNDED=YES  (cap asserted: 762)'`, to pin the cap the probe actually parsed.
- **Other details:**
  - Pass `--accrue 4` explicitly.
  - Do not echo the MEASURED block: after the fix it prints "measured accrual rate 0.7 Hz".
  - `--only` cannot carry a row. `--only X --timer 1 --expect-cap 762` gives `CONTROL=FAILED`, `VERDICT=REPORT-ONLY`, exit 1.
- **Gate 14 is the right home.** It already runs `-E cats` with the same stub. But `gatedevicesplit` has been OWED since #498, and the #497/#498 text in gate_arm.sh says not to compound it silently, so the new block must say so.
- **Other units' edits are uncommitted in the same files.** The working copies carry another unit's uncommitted `crime_width` section in gate_arm.sh and 156 uncommitted lines in check_probe_wiring.py. Stage hunks selectively.

**7. Q5: records. MEASURED with `check_probe_wiring.py` on the clone.**
- Wired, entry kept: `STALE EXEMPTION … RUN by gate_arm.sh:1776`. This confirms the brief's premise.
- Wired, entry deleted: `PASS 71/81, 10 dated-exempt`.
- **A one-line `for t in 0 1 2 3; do python3 …; done` reads as `UNWIRED DETECTOR`.** The command-position regex rejects the `for …;` prefix, so `python3` must start its own line.
- A timer-0-only call passes: section R cannot tell one timer from four.
- **On 2026-09-28 it still goes red, with 10 expired entries** (11 at HEAD). #548 clears 1 of the 11 exemptions that lapse that day.
- `--selftest` on the edited checker: 22/22.
- `GATE_MANIFEST` stays 16, and nothing else pins gate 14's check count.
- Text still owed: the probe header's arm X paragraph, `fable_queue.md:516`, and a pointer from `gate_offline.sh:1311`.

**8. Something else: two false statements about the ceiling. MEASURED with gate 2's own harness.**
- **The claims:** `dev_footbridge.c` (in reload_timer_value) says deleting the ceiling means "the overflow returns". The #442 block in `gate_offline.sh` says the no-ceiling mutant fails R2.
- **What I measured:** with the ceiling deleted, run at depth 2147487744, R2 prints `ok R2 no signed overflow … peak 2147483647 trough 1`.
- **Why:** the comparison runs before the increment and resets the counter to 1, so it fires at INT_MAX and no int-sized bound can overflow. The ceiling limits how large the backlog can get (R1/R5 go red at high emulated_hz); it does not prevent a wrap. Both are wrong records (L4); file them, and do not cite the ceiling deletion as a #442 regression.

**9. Traps in the build recipe the seats were given (all bit me).**
- On this machine `git clone` checks files out with CRLF; `-c core.autocrlf=false` is needed.
- `--shared` from a `C:/` path records a Windows path for git's shared object store, so every git command inside WSL fails. My scripted restore refused and kept the sentinel. I restored from git-bash and cleared the sentinel only after the two-part check: source `cmp` against the HEAD blob, and the rebuilt binary's md5 equal to the base.
- Redirecting `wsl.exe` output on the git-bash side lost stdout lines. I re-derived the mutant build status from artifacts: 8 distinct md5s, all different from the base.
- `regress/fbpending_drain_probe.py` is committed with CRLF line endings. That is harmless unless someone executes it directly.

**Commands run.** Reads used `git show HEAD:` or `git grep` against GXEMUL-SEC; I wrote nothing there. All work ran as `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/.../_scratchpad/opus548/scripts/<script>`:
- **Build:** `envcheck.sh`, `build_base.sh` (`sh ./configure`, `make -j8`), `mkstub.sh`, `mkmutants.py`.
- **Mutants:** `build_mutants.sh` and `build_one.sh` (`rm src/cpus/*.o`, `make`, `[ gxemul -nt … ]`, `cc … diff_fbpending_bound.c`, run at depth 2147487744), `restore_rebuild.sh`.
- **Probe runs:** `batch_base.sh`, `batch_mutants.sh`, `batch_extra2.sh`, `devtick_fast.sh`, `en0_fast.sh`, `batch_starve.sh` (uses `taskset -c 7`).
- **Checks:** `diff_footbridge_mutants.sh`, `wiring_check.sh`, `wiring_exp.py`, `pscheck.sh` (no leftover processes).
- **git-bash:** the two clones, `git -C clone checkout`, the `cmp` checks, and `rm -rf clone`. The clone is removed; the repo status is unchanged from start.

Everything is in `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\opus548\` (about 119 MB, mostly the binaries):
- `out\results_table.txt` — every run
- `out\runs\` — full logs
- `out\mutants\` — mutant sources
- `out\bin\` — binaries
- `out\wiring_exp.out`
- `scripts\`
