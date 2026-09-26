OPUS551P1_ALIVE

VERDICT: PROCEED WITH CHANGES

How I measured: on a `git archive HEAD` copy in WSL `/tmp/opus551p1`, using gate 2's compile line and gcc 15.2.1. The repo is untouched (the target files' md5s are unchanged and there are no new files). Scripts and logs were written to the session scratchpad (`opus551p1\`: `xform.py`, `runall.sh`, `force.sh`, `analyze.py`, `results\`); that location is volatile.

1. **Counts (measured, with a parser that ignores comments).**
   - Confirmed: 95 `failures ++` sites, 128 rows at runtime, and 14 multi-line or braceless conditions (11 multi-line; 3 braceless at :597, :659, :5457).
   - Three corrections:
     - There are 95 `rows ++` statements, not 96. The 96th grep hit is the comment at :4785.
     - The sites sit in 61 functions, not 59 (counting `main`, `chk`, `midxfer_case`, `pkt_cdb_case`).
     - The `% 255` revert reddens 9 rows at HEAD, not 7.

2. **The exemption's premise is stale (read, plus git).**
   - The file already has a got/want comparator: `chk(name, got, want)` at :4849. It was added by #484 on 2026-08-27 and carries 24 of the 128 rows.
   - The "NOTHING TO FEED A MISMATCH TO" text dates from 7e3b1204 (2026-08-19), and the 09-18 re-date carried it forward without re-reading it.
   - So option C aimed at `row()` is the wrong partial. The right one (call it C′) is the template's own sentinel on `chk()`: 24 of 128 rows, no refactor.

3. **Option-set completeness (read).**
   - `diff_fbpending_bound.c`'s `row(name, good, fmt, ...)` is an in-tree boolean verdict helper that owns `rows++`, the verdict and the print. It is already COVERED, inside the group `gate_offline.sh` says "covers the file". So A is not a new kind of discharge, but that sentence already overclaims for fbpending.
   - Side finding: fbpending prints its SELFCHECK verdict through the helper under test, and its FAIL line still contains the G text. So G cannot fail there; only the verdict token or the self-mutant lane would catch it (read, not measured).

4. **Prototype of A (measured).**
   - The wrap matches parentheses on the comment-masked text; the helper is renamed `row_failed`.
   - Combined stdout+stderr is byte-identical to the original except the SELFCHECK line(s), and exit codes match, in all 15 cases: 5 `dev_wdc.c` variants (pristine, the self-mutant, the `% 255` revert, a 13-bit cylinder truncation, the pre-#481 reset bit) × -O0/-O1/-O2.
   - This holds for both the brief's sentinel and a hardened one.
   - No site has inverted polarity, reads `failures`, or jumps out of its branch before the increment.

5. **Site shapes the wrap gets wrong (measured).**
   - a. The name `bad` collides with a local `int bad` in 5 functions (`row_slave`, `row_base_drive`, `row_every_opcode_resets`, `row_identity`, `row_selfconsistent`), giving 5 compile errors.
   - b. At the 3 braceless sites, deleting `failures ++;` leaves `if (…) else`. It must become `;`.
   - c. The 11 multi-line conditions break any line-based wrap.
   - d. `row_slave`, `row_base_drive` and `row_identity` print FAIL in earlier, unwrapped blocks. Under a helper that returns 0, the same row prints FAIL and then ok.
   - e. :5619 `if (bad)` passes a count (for example 57344). It is the only argument that is not 0 or 1.

6. **The proof as specified is not enough (measured).**
   - -O0 does not link with gate 2's flags at HEAD (3 undefined references to `quiet_mode`). A script diffing two failed builds compares two empty outputs and reads "identical". I linked a one-line stub into both arms.
   - My five variants exercise FAIL arms at only 16 of the 95 sites; the brief's two named mutants reach 5.
   - I planted two transform defects at :1576: one deletes the count without wrapping, the other wraps but keeps the count. Both were byte-identical to the original on all five variants.
   - A forced-site differential did catch them. `FORCE_SITE=k` makes site k's condition true in both arms through identical instrumentation. It reached 95 of 95 FAIL arms, showed A identical to the original in 96 of 96 runs, and flagged both planted defects at exactly k=22.
   - Cost: 2 compiles and about a minute. Require it; the denominator is sites, not "groups".

7. **Q2, the smallest edits that break A and still pass (measured, -O2).** Against the brief's sentinel (first; tally only; inputs 1 and 0):
   - A helper that keeps counting but returns 0 stays green; its sites print ok, and only the self-mutant lane catches it.
   - Changing the helper's parameter from `int c` to `unsigned char c` (one token), or narrowing it to `c == 1`, stays green, and the self-mutant lane still passes.
     - On the 13-bit-cylinder tree the harness then reports 128 rows, 0 failures, `WDC_IDENTIFY_PASS`, and "ok IDENTIFY agrees with itself 0 of 65535". The original reports 1 failure.
     - Every gate-2 wdc check is green on a defective device.
     - That ok line prints a literal 0.
   - A helper that goes inert after 3 calls passes a first-placed sentinel; a last-placed one catches it.
   - A hardened sentinel reds all of these. It checks the return value as well as the tally, uses inputs {1, 0, 2, 0x10000, −1}, and runs first and last.
   - One edit survives every placement: `if (rows && rows < 125) return 0;`.
     - It stays green first and last, and the self-mutant lane passes (the self-mutant's row is row 125).
     - The reset-bit defect's 11 rows then read 0 failures and PASS.
     - Any helper that reads `rows` or a call counter can do this; `rtc_range`'s `chk()` has the same limit. It is sabotage-shaped, so disclose it under clause (e) rather than chase it.

8. **Q1 (read; reasoning from 4–7).**
   - A can fail (helpers that return 0 or never count both red it), so it is not a check that cannot fail.
   - But it guards a single point of failure that A itself creates. Today no ordinary edit silences all 95 sites at once; after A, one does.
   - The net gain is manifest conformance and one site shape, not coverage of any comparison.
   - The COVERED comment should list wdc_identify as an exception: "verdict path of all 128 rows via row_failed(); comparison probed for chk()'s 24; 104 inline comparisons unprobed; stateful helper edits disclosed."
   - Also add two things:
     - A gate pin requiring exactly one `failures ++` in the file, or a later hand-written site silently falls outside the claim.
     - A SELFCHECK FAIL line that does not contain the G text, as `rtc_range` already does.

9. **Q5 (measured).** A plus the forced-site proof took about an hour here, so 09-28 is realistic. If it slips, ship C′ with the stated fraction (24/128) rather than re-dating.

**Required changes before implementing A:**
1. Rename the helper away from `bad`.
2. Turn the braceless deletions into `;`.
3. Use the hardened sentinel, plus the template's narrow and wide probes on `chk()`.
4. Use the forced-site differential as the equivalence proof, with a `quiet_mode` stub at -O0 or -O1 in its place.
5. Add the one-`failures ++` gate pin.
6. Scope the COVERED text as in finding 8.

---
*Recorded by the main loop: agent a088149d37f1fac24, `agent_models.py` = clean, opus-5-5 throughout.  Its scratch was
copied to `opus551_measured/` (the 11 MB HEAD tarball dropped; `.py` renamed `.py.txt` so the wiring checker does not
read measuring scripts as probes).*
