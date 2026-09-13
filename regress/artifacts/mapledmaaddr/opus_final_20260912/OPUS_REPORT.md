OPUS_FINAL528_20260912

First line of CHECKPOINT.md, verbatim:
`# CHECKPOINT -- 2026-09-12 ~19:1x   HEAD 7457c04 (records)   #528 mapledmaaddr IN FLIGHT (closing pass)`

**VERDICT: GAP** -- two measured survivors of the whole-transcript oracle, on two different axes:

1. **GAP (Q1, emulated time):** a read-caused diagnostic deferred to the maple device's own tick, reported every 4th tick --
   `static int maple_rd_count = 0, maple_tick_n = 0;` above `DEVICE_TICK(maple)`, first statement of its body
   `if (++maple_tick_n % 4 == 0 && maple_rd_count) { fatal("[ dreamcast_maple: DMAADDR was read (%i times) ]\n", maple_rd_count); maple_rd_count = 0; }`,
   and `maple_rd_count++;` after `odata = d->dmaaddr;` -- **scored 37/37**
   (`regress/artifacts/mapledmaaddr/opus_final_20260912/probe3_SHIPPED_M_TICKPERIODIC4.raw`).
2. **GAP (Q2, crashed session passes):** an abnormal end at process exit keyed on a nonzero field --
   `static void maple_q_die(void) { abort(); }` and, after the assignment,
   `if (d->dmaaddr != 0 && !maple_q_reg) { maple_q_reg = 1; atexit(maple_q_die); }` -- **scored 37/37**
   (`.../probe3_SHIPPED_M_ABORTATQUIT.raw`; the `_Exit(1)` form likewise, `probe3_SHIPPED_M_EXITATQUIT.raw`).

The in-band output channel itself is closed: every output that reaches the pty inside the session's emulated span reds,
including stderr, a no-newline stdout write, a buffered `printf` at exit, and tick deferrals of 1-3 ticks.

---

## What I measured (clone `/tmp/gxopus528f`, restored CLEAN + FRESH, sentinel cleared; SEC never written)

Probe FROZEN at each launch, `cmp`-IDENTICAL to `regress/`.  Every scored leg built `rc=0`, binary FRESH.

| leg | edit (full diff: `<leg>.diff`) | shipped probe | note |
|---|---|---|---|
| BASE x3 | the fix | 37/37 each | three runs; repair-probe BASE 37/37 too |
| M_STDOUTNONL | `printf("JUNKDMAADDR");` in the read | 36/37 | glued onto the FRONT of the next echo (`'JUNKDMAADDRGXemul> print r2'`), never into a disasm tail |
| M_STDERR | `fprintf(stderr, "...\n");` in the read | 36/37 | stderr is on the pty; lands as its own line |
| M_ATEXITPRINTF | atexit handler with `printf` (buffered stdout) | 36/37 | 1 surplus line after the `quit` echo |
| M_TICKDEFER | announce on the next maple tick | 36/37 | 12/12, surplus line after `quit` |
| M_TICKDEFER2 | announce on the 2nd tick | 36/37 | **predicted 37/37 -- WRONG**; killed 12/12 after `quit` |
| M_TICKDEFER3 | announce on the 3rd tick | 36/37 | **read silent 2/12 exactly as predicted** |
| **M_TICKPERIODIC4** | report every 4th tick | **37/37** | non-eq: prints within 4 s of free-running |
| M_FILE | append to `/tmp/maple_leak_final` | 37/37 | the DISCLOSED off-channel: 18 lines written = the 18 DMAADDR reads in the 12 sessions |
| **M_EXITATQUIT** | atexit `_Exit(1)`, keyed `d->dmaaddr != 0` | **37/37** | 10 sessions end `exit1`, unobserved |
| **M_ABORTATQUIT** | atexit `abort()`, keyed `d->dmaaddr != 0` | **37/37** | 10 sessions end `sig6`, unobserved |
| M_EXITATQUIT0 (control) | the same, unkeyed | 36/37 | only `exit status` reds -- the one session whose `how` is read |

**Apparatus disclosure:** run 1's M_STDERR / M_FILE / M_ATEXITPRINTF failed to BUILD. That is **not** a kill.
The Bash-heredoc path ate one backslash level (the carrier's recorded trap), so `\\n` became a real newline inside a
C string literal.  They were re-measured in run 2 with a `chr(92)` mutator.  Evidence: `run1_build_*.log`,
`run1_mut_final_BROKEN_BACKSLASH.py`.

**Non-equivalence -- MEASURED** (`noneq3_M_TICKPERIODIC4.txt`): one DMAADDR read stepped exactly as the probe does,
then `continue` for 4 s. The stepped part shows `IN_STEPPED False` and the value correct, then
`freerun: 'continue\r\n[ dreamcast_maple: DMAADDR was read (1 times) ]\r\n'`.  BASE under the same driver prints nothing
after `continue` (`noneq3_BASE.txt`).  So every real guest that reads DMAADDR and keeps running gets the diagnostic,
and no probe session ever does.

**Why the tick axis stops at 3 -- READING, then MEASURED by the 2/3/4 ladder:** the main loop in `src/core/emul.c`
breaks on `emul_shutdown` BEFORE `machine_run`.  Then `cpu_run_deinit()` in `src/cpus/cpu.c` runs "Two last ticks of
every hardware device".  `ticks_till_next` starts at 0 (`machine.c`, `machine_add_tickfunction`), so the maple tick
fires once, AFTER the first stepped instruction.  After that it needs 2^17 more steps, and no session steps more than
a handful.  **A session therefore sees at most 3 maple ticks after its first instruction.**  Deferral by 2 is caught in
every session; by 3, only where the read IS the first instruction; by 4 or more, never.

## Q1 -- is any output caused by the read still not compared?

**Yes, one class -- MEASURED.**  Output the read schedules on EMULATED time more than the session's span away:
three maple ticks, about 2^18 instructions.  The whole-transcript fix closed the HOST-process time axis (atexit,
exit-time flush).  Process exit is a terminal event, so that axis could be closed.  **Emulated time has no terminal
event inside a session**, apart from the two deinit ticks.

That makes it an UNBOUNDED axis.  Free-running each read session for F ticks moves the boundary to F and never closes
it.  So this cannot be repaired into a floor.  It must be DISCLOSED with its window stated:

> *output the read defers beyond the session's emulated span -- the first-step tick plus `cpu_run_deinit`'s two final
> ticks -- is not observed.*

The contract's "effects keyed on the environment (time, ...)" might be read to cover it.  But the contract's positive
claim, "a diagnostic alone, in ANY wording or shape ... or a line printed late", then says the opposite, so the record
must pick one.

Candidates checked and closed:
- **Disasm-line tail (the one partially-compared line):** unreachable.  MEASURED: M_STDOUTNONL's bytes glued onto the
  next ECHO, so the disasm line's newline precedes execution.
- **stderr:** carried and caught. MEASURED.
- **Buffered stdout at exit:** caught. MEASURED.
- **Before the first prompt** (the `find("GXemul> ")` anchor discards it): unreachable, because no guest instruction
  runs before the first prompt under `-V`. READING.
- **File:** outside reach, as disclosed.  MEASURED; I agree with the disclosure.

## Q2 -- false red on a correct build; can a crashed session pass?

**Crashed session passes: YES -- MEASURED** (M_ABORTATQUIT 37/37 with 10 of 12 sessions killed by SIGABRT).
- `rsession()` stores each session's `how` in READS, and nothing reads it.  The only `how` check is the `exit status`
  row, in `marker survive`, and that session reads DMAADDR while the field is still 0.
- So any abnormal end after the transcript completes, keyed off the value 0, is invisible.  That is the `exit(1)` half
  of the removed defect, moved to the time axis the round just closed for the diagnostic half.
- A crash BEFORE the transcript completes does red (HEAD / M_EXITONLY 11/37, table 6).
- **Repair, MEASURED:** one statement in the `read silent` row folds each READS session's `how` in (`REPAIR_HOW.diff`).
  - M_EXITATQUIT and M_ABORTATQUIT each go to 36/37 (`session ended exit1` / `sig6`, 10/12).
  - BASE stays 37/37.
  - No new session, row count unchanged.

**False red:**
- MEASURED BASE 37/37 in 3 runs here, plus 3 in table 6.
- READING, correcting my own previous report: I called this oracle load-sensitive through its fixed read windows.  **For
  this version that no longer holds for line presence.**  `noise()` reads the final buffer, and the child cannot exit
  before it has processed `quit`.  So every pre-quit byte drains before EOF; the 0.20 s / 1.2 s windows only pace input.
- The echo lines are GXemul's own (`console_init` clears ECHO/ICANON at `main.c:675`), so typed-ahead input cannot
  reorder the compared region.  Any kernel echo before that lands ahead of the anchor.
- Residual load risks:
  - `settle=2.5` before the first command.
  - The 10 s post-quit ceiling.  With the repair, an exit slower than 10 s would red via `how`.
- **A NEW COUPLING, deterministic and not load-dependent:** because the transcript now runs through `cpu_run_deinit`,
  `read silent` also asserts that **every dreamcast device is silent on its two final ticks**.  Any other device that
  ever prints at shutdown will red all 12 sessions, and the red will look like the maple read speaking.  Disclose it.

## Q3 -- does the chain close?

**No.**  Denominator swept this pass: 11 mutant legs plus BASE x3 across 3 runs, on these axes:

| axis | cells |
|---|---|
| channel | stdout-with-newline, stdout-no-newline, stderr, file |
| time | during step, at exit via atexit/flush, deinit tick 1, deinit tick 2, deinit tick 3, beyond the span |
| end state | exit0, exitN, signal |

This is on top of tables 1-6.  Measured escapes are in two cells: *beyond the span* and *end state != exit0 after a
complete transcript*.

**This is the second consecutive pass to find the SAME class: the session's time boundary.**  Last pass it was the
pre-quit snapshot and atexit; now it is emulated-time deferral and the end state after the transcript.  By the
carrier's repair-chain amendment, the next repair owes the CLASS CLOSURE, not another cell.  The enumeration above is
the space.

Dispositions:
- **End state:** a breach of the contract as stated.  It claims `exit(1) alone` is caught and rows `exit status` as
  FLOOR; this is the same axis the round graded in-round for M_ATEXIT.  Repairable in one statement, measured.
- **Beyond the span:** cannot be rowed.  It should become a stated window in NOT COVERED.  The claim as written ("ANY
  ... printed late") is a wrong record (L4) until then.

After those two, a future miss beyond the stated window would be *outside the contract*.  One inside the window (1-3
ticks, or any end state) would be *a breach*.

## Q4 -- which statement is wrong?

- **"What is left: a diagnostic that emits no byte (`fatal("")`) and output on a channel the pty never carries (a
  file)."** (probe comment; brief.)
  - **MEASURED FALSE.**  M_TICKPERIODIC4 and M_ABORTATQUIT both survive and neither is either of those.
  - This is the same sentence shape I refuted last pass, one survivor later.  **"The only thing left is X" should not
    be written without the enumeration that makes it checkable.**
- **Contract: "a diagnostic alone, in ANY wording or shape ... or a line printed late ... because the silence row
  compares each ... WHOLE transcript".**  **MEASURED FALSE** for a line printed more than 3 device ticks late.
  "Whole transcript" means the whole session's output, and the session's emulated span is about 3 ticks.
- **owed(): "`quit` owes its echo; then the process ends, and nothing may follow".**
  - READING + MEASURED: the process does not simply end.  It runs two ticks of every device first, and that is what
    killed M_TICKDEFER/2.
  - The rule ("nothing may follow") is right; the model of what happens is incomplete.  That incompleteness is why the
    coupling in Q2 is invisible from the text.
- **Brief Q1: "output written to a file ... already listed as outside the test's reach".**  Correct -- MEASURED
  (M_FILE 37/37).
- **Kill table 6 "17 runs, 17 exactly on prediction".**  Verified against `killtable6_20260912/SCORES.txt`: correct.
- **My own previous report, Q2, "load-sensitive ... fixed windows"**: overstated for this version (see Q2).
- **My own prediction, M_TICKDEFER2 37/37**: wrong.  I had not read `cpu_run_deinit`.  The miss is what located the
  3-tick boundary.

Premises I could not check from this packet: the kill counts of tables 1-5 (trusted from their SCORES files).  I did
not re-measure the disclosed value cells.

*Seat note: agy was not fired (measuring reservation).  This is the Opus compile-and-measure seat's own build+measure,
3 runs.  Every artifact cited here is in `regress/artifacts/mapledmaaddr/opus_final_20260912/` (README there).*
