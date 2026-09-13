# opus_final_20260912 -- Opus 5 measuring seat, final verification pass on `mapledmaaddr` (#528)

Brief: `_scratchpad/brief_maple_final_20260912.md`.  Instrument: `regress/maple_dmaaddr_probe.py` (37 rows, whole-transcript
`read silent`), FROZEN at each run's launch and `cmp`-IDENTICAL to `regress/` (each SCORES file line 2).  Scratch clone
`/tmp/gxopus528f` (a `cp -a` of `build/`), baseline = SEC `src/devices/dev_dreamcast_maple.c` (the fix), `cmp` CLEAN before
the first leg of every run; clone-local `.MUTANT` sentinel; every build `rc=0` and `[ gxemul -nt source ]` FRESH before its
leg was scored.  Restored at the end of every run: `cmp`-CLEAN + FRESH, sentinel cleared.  Nothing written to GXEMUL-SEC
outside this directory, nor to est/, build/, build-asan/.

## Runs

| run | scores | legs |
|---|---|---|
| 1 | `SCORES_run1.txt` | BASE 37/37; M_STDOUTNONL 36/37.  **M_STDERR, M_FILE, M_ATEXITPRINTF: BUILD FAILED -- NOT kills.**  Apparatus error: the Bash-heredoc path ate one backslash level, so `\\n` became a real newline inside a C string (`run1_build_*.log`, `run1_mut_final_BROKEN_BACKSLASH.py`).  Re-measured in run 2 with a `chr(92)` mutator. |
| 2 | `SCORES2.txt` | BASE 37/37; M_STDERR 36/37; **M_FILE 37/37** (18 lines written to /tmp -- the disclosed off-channel); M_ATEXITPRINTF 36/37; M_TICKDEFER 36/37; M_TICKDEFER2 36/37 (**my prediction was 37/37 -- WRONG**; see below) |
| 3 | `SCORES3.txt` | BASE 37/37 (shipped and repair); **M_EXITATQUIT 37/37**; **M_ABORTATQUIT 37/37**; M_EXITATQUIT0 (control) 36/37 `exit status`; M_TICKDEFER3 36/37 (read silent **2/12**, as predicted); **M_TICKPERIODIC4 37/37** |

Artifacts per leg: `<leg>.diff` (vs SEC), `run2_probe_<leg>.raw` / `probe3_SHIPPED_<leg>.raw` / `probe3_REPAIR_<leg>.raw`,
`*build*_<leg>.log`, `*mutate*_<leg>.txt`.  Non-equivalence (free-run the guest's `bra .` 4 s after one read):
`run2_noneq_*.txt`, `noneq3_*.txt` (driver `noneq_tick.py`).  Mutators: `mut_final2.py`, `mut_final3.py`.  Runners:
`run1_run_final.sh`, `run_final2.sh`, `run_final3.sh`.

## The wrong prediction, and what it found

M_TICKDEFER2 (announce on the 2nd maple tick after the read) was predicted to escape and was KILLED in 12/12 sessions,
one surplus line AFTER the `quit' echo.  Cause, by reading: `src/cpus/cpu.c` `cpu_run_deinit()` -- "Two last ticks of
every hardware device" -- runs at shutdown, after the main loop breaks on `emul_shutdown` (`src/core/emul.c`).  So a
probe session spans at most THREE maple ticks: the initial tick (`ticks_till_next` starts at 0, so it fires on the first
stepped instruction, AFTER that instruction) plus the two deinit ticks.  M_TICKDEFER3 (3rd tick) then reds exactly the
2 sessions whose FIRST stepped instruction is the DMAADDR read (`initial zero', `marker survive') -- predicted and
measured 2/12 -- and M_TICKPERIODIC4 (report every 4th tick) never prints in any session: 37/37.

## Repair candidate for the exit-status gap (MEASURED)

`maple_dmaaddr_probe.REPAIR_HOW.py` = the shipped probe plus ONE statement (`REPAIR_HOW.diff`): fold each read session's
own end (`how`, already stored in READS and never read) into `read silent`.  BASE 37/37; M_EXITATQUIT 36/37 and
M_ABORTATQUIT 36/37 (`read silent` 10/12: `session ended exit1` / `sig6`); the two sessions it cannot see read only a
0 field, which the mutants' key excludes.  Row count unchanged.
