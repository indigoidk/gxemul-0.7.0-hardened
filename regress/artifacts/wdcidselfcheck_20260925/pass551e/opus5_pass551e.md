OPUS_SEAT_ALIVE_20260925_551e
# CHECKPOINT -- 2026-09-25 ~18:30 (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT: SHIP WITH CHANGES

The call-count pin works against the move it was built for, and no single edit outside the four classes is green. But this pass does not close the chain:
- **An unnamed class keeps gate 2 green:** covered rows moved past the verdict, with the pin's counts supplied another way.
- **Three sentences of the new contract are false.**
- **The trailer class can be closed inside the file after all.** A pin on the trailer cannot do it; a line printed by the comparator itself can (finding 3).

How I measured: a WSL `/tmp` copy of `MINE_e.c` (1b467a08), 424 serial `-O2` builds. There are 51 shapes: my 33 from #551d, regenerated from this file by the unchanged #551d script, plus 18 new ones. Each ran on the real device and on dropold, drqring and w57hi, plus the self-mutant device for the lane. "Gate 2" means the 73 extracted wdc checks, H, G, one PASS token, and the self-mutant lane using `selfmutant.py`'s logic. Everything is in `regress/artifacts/wdcidselfcheck_20260925/opus551_measured_e/`: `analyze7.out` holds the table, and `NOTE_moved_logs.txt` explains the logs that end after the token.

**1. Q1: the re-run, and the floor question.**
- **Re-run (MEASURED):** `move_repin` is now red everywhere (`chk() ran 0 times and row_cmp() 8 before this run`). The other 32 give the same results as on #551d.
- **Single edits (MEASURED):** all 24 outside the classes are still red. The two new single edits outside class (3), a conditional reset at `main()`'s start and one after the printed count, are both red.
- **Healthy runs (MEASURED):** #551e's whole log is identical to #551d's on 9 device variants, with the same exit codes.
- **Unnamed class, green (MEASURED):** move the covered calls past the verdict, and supply the pin's count another way:
  - 24 calls of `chk("x", 0, 0)` placed before `selfcheck("last")`, plus the move. Two edits; green on dropold and drqring. The identity row still reads 128.
  - The same with 8 calls of `row_cmp("y", 1, 1, 1)` and the `row()` block moved. Two edits; green on w57hi.
  - `chk_calls = 24;`, the move, and the identity row re-pinned to 104. Three edits; green on dropold and drqring.
- The contract says moving is caught, so this class is not merely unnamed — it is denied. Under the stop rule it reopens the chain.

**2. Q2: attacking the pin (MEASURED).**
- The pin counts calls, not which calls ran. It is beaten by the composites above; none is a single edit.
- The fed-call form borrows class (2)'s mechanism (a comparator fed its own want). But what it silences is the moved real rows, whose own comparisons are untouched. So it sits in no named class.

**3. Q3: the adjudication's caution.**
- **A pin ON the trailer does not survive (MEASURED).** I wrote a verdict function that the last self-check probes at (0,0,1), (1,0,1), (0,1,1) and (0,0,0), and used it for the token and the exit status.
  - One inserted conditional reset: green on all three device variants.
  - One inlining edit plus its partner subtraction: green on all three.
  - That half of the claim stands.
- **But the trailer class can be closed in the file (MEASURED).** The premise "everything gate 2 reads is produced at one call site in `main()`" is false. Gate 2's failure-count check greps `[0-9]+ failures` over the whole log.
  - The change: on a covered failure (probe names excluded), each comparator prints `  FAIL  covered comparator failure, N failures so far` at the moment it fails.
  - All six attacks I stacked on it are red: the conditional reset after the covered rows and at the trailer, the both-tally reset, both two-edit trailer rewrites, and the move with fed calls.
  - A line already printed cannot be taken back by a later edit.
  - Cost: healthy runs are whole-log identical to #551e (real device, self-mutant, cyl13, srstbit). Failing runs gain exactly one line per covered failure (+2, +3, +4, +5, +6 lines).
  - Residual: switching the emission off inside a comparator is a class (1) edit. With both switched off plus a reset, it is green again (three edits).

**4. Q4: false sentences.**
- **"conditional on their equality, anywhere" (MEASURED false).** It is red at `main()`'s start (before the covered rows) and after the printed count. The truthful form is "anywhere after the covered rows and before the count is printed".
- **"Nor is moving the covered rows past the verdict" (block comment) and "so is moving the covered rows past the verdict" (gate bullet) (MEASURED false).** See finding 1.
- **"requires every covered call to have run before it (chk() 24, …)" (READ).** It requires 24 `chk()` calls of any kind. Eight of the real 24 are the verdict-handed calls, which are not covered, and fed calls count too.
- **"the close is gate-side" (MEASURED false).** Finding 3 is an in-file close. The half before it, "no in-file probe can pin a single call site", is true.
- **True:** "four classes, each measured"; "24 measured, #551d"; "a reset of `failures` alone … wherever it sits" (every such shape is red); and the placement of the unconditional both-tally reset.

**5. Missed by all of us, including me until this pass.** Gate 2 reads the whole log, not just the trailer. A covered failure can therefore report itself at the moment it happens, and no rewrite of the trailer can reach that line.

**Suggested repair (#551f), your call:**
- **Recommended:**
  - Adopt the emission line.
  - Keep the pin; it is now redundant against the move but harmless.
  - Class (3) collapses into class (1); fix the four sentences above.
- **Alternative:** keep the design and name the move-with-supplied-counts class, fix "anywhere", and drop "the close is gate-side".

---
*Recorded by the main loop: agent a088149d37f1fac24 (resumed for #551e's pass), final text by claude-opus-5-5 at 2026-09-25T23:52:59.406Z, extracted verbatim from the agent transcript.  Badge s.*
