VERDICT #551: SHIP WITH CHANGES

I think 2 of your dispositions are wrong (Q4 and Q10). Separately, a one-statement edit outside the disclosed classes keeps gate 2 green, and a cheap fix for it measured byte-identical.

How I measured: a WSL `/tmp` copy of `MINE_b.c` (md5 d0339493), serial `-O2` builds only, device variants built from HEAD's `dev_wdc.c`. "Gate 2" means the 73 wdc checks extracted verbatim from `gate_offline.sh`, plus H (token in the source), G (text in the log) and the self-mutant lane using `selfmutant.py`'s logic. Scripts, outputs and 20 sentinel-checked logs are in `regress/artifacts/wdcidselfcheck_20260925/opus551_measured_f2b/`. The tree is untouched.

1. **(1) The six pass-2 escapes on the final file (MEASURED).**
   - **Two now red.** Narrowing `row_cmp()`'s parameters to `uint16_t`, and `&& sectors<4`: 2 of 11 probes answer wrongly at both runs, the run prints `WDC_IDENTIFY_FAIL` (exit 1), and gate 2 reds row failures, verdict, G and lane.
   - **Four still keep gate 2 green**, all inside the rewritten disclosure: `&& want-165`, `row()` passing its own want, the after-`rows ++` `(rows & 127) < 2` test, and `*name == '@'`.
   - **The pass-2 double edit is now red.** With the forced failure removed and `chk()` stubbed, the run prints `WDC_IDENTIFY_FAIL`, exit 1, and gate 2 reds verdict, G and lane.
   - **`sc_g` changes no healthy run (the Q5 question).** `MINE_b.c` matches HEAD's harness line for line, apart from the SELFCHECK lines, on 7 device variants.

2. **(2) Smallest edit outside the disclosed classes: reset the failure tally (MEASURED).**
   - The edit is one statement, `failures = 0;`, placed in `main()` right after `row_ring_occupancy_sound();`. That is after every covered call (rows 1–105) and before the self-mutant's row 125.
   - Gate 2 stays fully green on the drop-oldest, DRQ-dropped and word-57 device variants. The covered rows print FAIL ("R2 anchor: inbuf[tail] survives got 17 want 165", "R6 liveness: DRQ asserted", "threshold: >>8 byte reaches 255"), yet the trailer reads `128 rows, 0 failures`, `WDC_IDENTIFY_PASS`.
   - It is neither a comparator test nor a feed edit. The self-check measures its own deltas and restores the tally, so it still passes; the lane's row runs after the reset; and `sc_g` is set because the self-check really did pass.
   - Every covered row, and every inline row before row 106, can print FAIL but can no longer fail the run.
   - **Fix (MEASURED):** give the comparators their own count. Add `cmp_fails ++` beside `failures ++` in `chk()` and `row_cmp()`, restore it with `failures` in the self-check, and make PASS require it to be 0.
     - The whole log and exit code match `MINE_b.c` on 9 device variants.
     - The reset edit then prints `WDC_IDENTIFY_FAIL`, exit 1, and defeating the fix takes two statements.
   - If you'd rather disclose than fix, the disclosure's list needs "the tally between the comparators and the verdict"; today it omits that class.

3. **(3) Is "block deleted" the right control? Yes for H and G, but incomplete (MEASURED, three deletion forms).**

   | deletion | build | run | gate 2 reds |
   |---|---|---|---|
   | block, calls, declarations, and the verdict reverted (yours) | ok | PASS, exit 0 | H and G only |
   | block and calls deleted; `sc_g` declaration and verdict left | ok | FAIL, exit 1 | verdict, H, G, lane |
   | declarations deleted with the block; verdict left | fails: `'sc_g' undeclared` | — | the compile row |

   - Yours is the only form under which the run passes, so it is the right control for H and G as the sole carriers.
   - The second form is the likelier maintenance edit and is exactly what `sc_g` buys; it belongs in the record too.
   - Q10's wording ("prints … no token — exactly what … H row greps for") names the wrong observable. H greps the source, where the token goes out with the deleted block; it does not grep the run's output.

4. **(4) Two dispositions I think wrong.**
   - **Q4 (MEASURED).** It says the wide probes make the comment's "each operand zero and past 32 bits" true of `row_cmp()`. That is false: `row_cmp()`'s `sectors` operand is never 0 in the probes {2, 2, 1, 3, 2^32, 2^32}, and adding `&& sectors` to `row_cmp()` passes all 11 probes. It is harmless today (no row passes 0 sectors), but it is a new false sentence written by a correction. Either add the probe (want 0, got57 1, got60 0) or change the comment to "each got operand".
   - **Q10:** as in finding 3.
   - The rest stand. For Q8 I checked "true when written": at 7e3b1204 the two files are 1311 and 766 lines.

---
*Recorded by the main loop: agent a088149d37f1fac24 (resumed for the F2 on pass 2), `agent_models.py` = clean, claude-opus-5-5; final text 2026-09-25T21:41:53.711Z UTC.  Badge s.*
