OPUS_SEAT_ALIVE_20260925_551f
# CHECKPOINT -- 2026-09-25 ~19:35 (087a90 sections rewritten; the peer's sections below are untouched)

VERDICT: SHIP WITH CHANGES (the stop condition is not met; this pass reopens)

**Reopens.** One line at file scope keeps gate 2 green on every covered-only device while the covered rows keep running and the comparators' code is untouched:

```c
#define printf(...) (strstr(#__VA_ARGS__, "so far") ? (failures--, cmp_fails--) : (printf)(__VA_ARGS__))
```

(B) says exactly that shape is caught, so by the stop condition's letter this is L2. If "comparators intact" is read as their compiled behaviour rather than their source text, it is instead the (B) residual in one edit, and only the wording changes.

How I measured: my own `/tmp` tree, 415 serial `-O2` builds.
- Your 40 shapes were regenerated with your `meas551f.py`; I added 7 of my own.
- Every cell was scored twice: by my stand-in for gate 2's `check()`, and by gate 2's real `lib.sh`, sourced, running the extracted block. H and G used the exact greps from `gate_offline.sh`; the lane followed `selfmutant.py`'s logic.
- For five key cells I also ran the real `selfmutant.py`, unmodified, on mirror trees.
- Everything is in `regress/artifacts/wdcidselfcheck_20260925/opus551_measured_f/` (`analyze9.out`, `reallane.out`, 14 sentinel-checked logs).

**1. Q1: your caught set is confirmed (MEASURED).**
- All 41 rows of `run551f.out` (your 40 shapes plus the unedited file) reproduce cell for cell: GREEN/red, rows, printed failures, token and report-line count on all four columns.
- No mis-scored cell. My stand-in and the real `lib.sh` agree on every cell.
- Every shape you class as caught is red on every covered-only device. Healthy runs are whole-log identical to #551e on pristine, selfmut, cyl13 and srstbit. Failing runs gain only report lines (+2 to +6).
- One limit of the cross-check: your analyzer is adapted from mine, so running it again would only confirm itself. That is why the real `lib.sh` and the real `selfmutant.py` were used for the second scoring.

**2. Q2: attacking the report (MEASURED).**
- **The printf macro above.** It is inserted after `cmp_fails`'s declaration.
  - It swallows exactly the two report `printf`s: "so far" occurs in no other call's arguments.
  - It undoes the two increments beside each report.
  - Result on the real device and on dropold, drqring and w57hi: `128/0 PASS`, no report lines. The real `selfmutant.py` returns SELFMUTANT_OK on drqring and w57hi.
- **One edit inside a comparator also suffices.** `if (name[0] != '@')` → `if (name[0] != '@' && (failures--, cmp_fails--, 0))` is green on dropold and drqring (real lane OK). The `row_cmp()` twin is green on w57hi. That is inside (A)/(B), but it contradicts (B)'s "together with an edit that hides the tallies", which implies two edits.
- **Red, as the contract says:**
  - report suppressed only;
  - report text moved off the regex (`failure(s)`).
- **Green, as the (B) residual:** each of those two plus a conditional reset.
- **The other attack surfaces hold:**
  - Changing the argument or adding a line cannot help; the whole-string comparison reds any extra match.
  - The report text matches none of the 71 text patterns in gate 2's wdc block.
  - Only the two probe call sites pass names starting with '@'.

**3. Q3: false sentences.**
- **(B) "Hence no edit that leaves the covered rows running and the comparators intact hides a covered failure", and the bullet's "Any edit that leaves the covered rows running and the comparators intact is caught" (MEASURED false).** The macro is the counterexample. The premise just before it, "a printed line cannot be taken back", is true: the macro stops the line before it is printed, it never takes one back. It is the conclusion drawn from it that fails, because it assumes the line is printed.
- **"no line can be added" (MEASURED).** True in the sense the contract means: an added line can only red the count check.
- **"its guard is itself a probe/real key -- together with an edit that hides the tallies" (MEASURED, incomplete).** One edit does both.
- **"the file covers 24 comparisons and reports all 32 comparator failures" (MEASURED true).** drqring's two verdict-handed rows print r2.
- **Checked and true:** (C)'s "one insertion and green here" (`skipforge`, real lane OK), (D), and the pin comment.

**4. What would close it, or record it honestly.**
- The partition's premise, "any edit is inside a comparator, at its inputs, around it, or in the block", holds only for source location. The preprocessor lets one edit anywhere after the tallies act inside both comparators.
- Honest options:
  - Name that in (A)/(B) and change "intact" to "intact as compiled".
  - Or make the report use a channel the macro does not rename, e.g. `fputs` or `fwrite`. That is only weaker: `#define fputs` works the same way.
- So the class cannot be closed in-file. It belongs in the contract as the residual, stated as "the report's output path redefined or switched off (one edit)", with `wdcidlane` as its close.

---
*Recorded by the main loop: agent a088149d37f1fac24 (resumed for #551f's pass), final text by claude-opus-5-5 at 2026-09-26T00:39:58.606Z (`agent_models.py`: clean, opus-5-5 throughout), extracted verbatim from the agent transcript.  Badge s.*
