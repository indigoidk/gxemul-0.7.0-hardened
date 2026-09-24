OPUS548B_ALIVE
VERDICT: The `==` mutant passes every gated row at HEAD and was not detected until the R6 repair. The repair detects it (R6 peak 8192) and turns none of the 14 other mutants from red to green, but it is not at least as strong as R6-old: one mutant goes from red to green. Checking both re-arm cells in one row detects everything either version detects.

**1. M_eq at HEAD. MEASURED.** Your reading is confirmed.
- **Gate 2, bound harness:** `diff_fbpending_bound 2147487744` gives `FBBOUND_PASS`, with R6 peak 762 and 0 failing rows.
- **Gate 2, footbridge harness:** `diff_footbridge.c` gives 864 rows, 0 failures, `DIFF_FOOTBRIDGE_PASS`. It calls `timer_tickN` and `footbridge_pending` zero times, so it cannot see this at all.
- **Drain probe** (`--expect-cap 762 --accrue 4 --timer 0`): `CONTROL=OK`, D=3, X=3, `VERDICT=PASS`, exit 0. That is identical to the HEAD binary under the same instrument.
- **Why your reading holds:** every arm in the harness is a fresh `calloc` with count 0 (R0, R1, R2, and R6's re-arm). The probe's prologue re-arms three times at count 0 while stepping. The FREEZE lowers the bound to 1 over a residue of 3, but at 0.0116 Hz no callback lands in a 0.5 s drain slice, because each `continue` resets `next_tick_at` to one 86 s interval.

**2. The R6 repair, against 15 mutants. MEASURED.** Four harness versions:
- **R6old:** HEAD's harness.
- **R6new_a:** the drive placed right after the 50 MHz arm.
- **R6new_b:** the drive placed right before the re-arm. The two placements gave identical results for every mutant.
- **R6both:** timer 0 keeps its re-arm at count 0, and timer 2 is re-armed with 4096 ticks owed. It is one row with the same peak == 762 oracle.

| mutant | R6old | R6new (a and b) | R6both |
|---|---|---|---|
| base | PASS | PASS | PASS |
| M_eq | **PASS** | FAIL, R6 peak 8192 | FAIL |
| M_frozen | FAIL (R6, 4096) | FAIL (R6, 8192) | FAIL |
| M_idx0 | FAIL (R6b) | FAIL (R6b) | FAIL (R6 and R6b) |
| M_pendguard | FAIL (R6, 4096) | **PASS** | FAIL |
| M_idle | **PASS** | FAIL (R6, 8192) | FAIL |
| M_nobound, M_nr0, M_fclk, M_devtick, M_x2, M_noceil | FAIL | FAIL | FAIL |
| M_en, M_en0, M_nper | PASS | PASS | PASS (not R6's job) |

- **IDENTITY** is ok in all 60 runs; the row count is unchanged at 28.
- **None of the first-pass mutants moves from red to green** under any version.
- **M_frozen and M_idx0** remain red under R6 and R6b respectively, as you required.

**3. Your "at least as strong" argument does not hold. MEASURED.**
- **The mutant:** M_pendguard recomputes the bound on re-arm only when a backlog exists: `if (d->timer[timer_nr] == NULL || d->pending_timer_interrupts[timer_nr] != 0) d->pending_bound[timer_nr] = (int) bound;`
- **What happens:** R6old detects it (peak 4096). Under R6new the whole harness passes, and `diff_footbridge` passes too.
- **The mirror case:** M_idle (store only when the count is 0) passes R6old and is caught by R6new.
- **The reason:** the body's `>=` splits a re-arm into two cells, count below the new bound and count above it. R6old covers only the first and R6new only the second. R6both covers both and catches the union of what the other two catch.
- **Recommendation:** adopt R6both, not the one-liner. It adds no row and no oracle. Two cautions:
  - `diff_fbpending_bound.c` is committed with CRLF line endings, so the edit must keep them.
  - Nothing pins R6's text; I grepped.

**4. Rung-3 consequence of M_eq. MEASURED, and cheap.** I wrote a scratch driver that reuses the frozen probe's own machinery and adds a five-word re-arm stub; its encodings were checked as they executed, with 0 mismatches.
- **The sequence:** arm at 12207 Hz, accrue 0.25 s without acking, then a guest CONTROL write to ENABLE|FCLK_256 (762.94 Hz, bound 762). That write does not clear the count. Accrue 2 s more, then freeze and drain.
- **HEAD:** backlog 1. The count reset at the first slow callback.
- **M_eq:** backlog 4529, which is exactly 3004 + 1525 ticks and above the new bound of 762. All controls were OK in both runs.
- **Full wrap attempt, inconclusive:** 50 MHz for 1 s, then a LOAD write to 2 (25 MHz), then 100 s. Neither binary showed a dead clock: M_eq hit the drain limit of 200000, and HEAD drained 3390. I did not pursue it further.

**Commands.**
- **Clone** (git-bash): `git clone -q -c core.autocrlf=false C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC eq/clone`
- **WSL scripts**, run as `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash /mnt/c/.../_scratchpad/opus548/scripts/<name>`:
  - `eq_build_base.sh` — configure and `make -j8`
  - `eq_gen.sh` (runs `eq_gen.py`) — mutants and harness variants, exact-once edits, CRLF preserved
  - `eq_harness_matrix.sh` — each variant compiled in a private temp dir against the base objects and run at depth 2147487744; the clone is never modified
  - `eq_build_meq.sh` — sentinel, `rm src/cpus/*.o`, make, freshness check, `git checkout`, rebuild, md5 equal to base
  - `eq_probe_runs.sh`, `eq_wrap_runs.sh` (both run `eq_rearm_probe.py`), `eq_dfb.sh`, `pscheck.sh`
- **Clearance** was two-part and run from git-bash: source `cmp` against the SEC HEAD blob, plus the binary newer than the source with md5 equal to base. Only then was the sentinel cleared.
- **Cleanup:** the clone is removed, and no gxemul or probe processes are left running. GXEMUL-SEC is untouched (HEAD bead6ad9).

Everything is in `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\opus548\out\eq\`:
- `harness_matrix.txt`
- `runs\` — every log
- `mutants\`, `harness\`
- `wrap_runs.txt`
