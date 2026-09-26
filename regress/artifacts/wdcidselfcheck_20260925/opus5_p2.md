VERDICT: SHIP WITH CHANGES

The final file (md5 ef662cb5) is sound on the real `dev_wdc.c`, but two of its comment claims are measured false. Its probes miss narrowing in `row_cmp()`, and the run itself still reports PASS when its self-check has failed. Three changes follow: correct the disclosure, add two wide `row_cmp()` probes, and make the PASS verdict depend on the self-check. Each is measured, and none changes the output of any healthy run.

How I measured: a WSL `/tmp` copy, serial `cc -O2` builds only (48 plus 10). "Gate 2" below means the 73 wdc checks extracted verbatim from `gate_offline.sh:1455-1877`, plus H, G, and the self-mutant lane using `selfmutant.py`'s logic (device plus device-with-self-mutant). Scripts, outputs and 17 sentinel-checked logs are in `regress/artifacts/wdcidselfcheck_20260925/opus551_measured_p2/`; `.py` files are saved as `.py.txt`. The harness, gate script and `dev_wdc.c` are untouched.

1. **Baseline (MEASURED).** On the real `dev_wdc.c`, gate 2 is green.
   - The run prints `ok SELFCHECK(first): all 9 probes answered right`, the G line once, and `note … chk() 24, row_cmp() 8`.
   - `grep -c 'high byte'` is 1 (lines).
   - There is exactly one untagged self-mutant line.
   - The token appears only at :5645, :5675 and :5681, and the 8-verdict deriver prints 8.

2. **Q3: six edits keep gate 2 fully green on a defective device (MEASURED).** Each device variant carries a defect that only the silenced rows see; the final file reds every one of them.

   | edit | defect variant | rows silenced (print ok) |
   |---|---|---|
   | `chk()`: ` && want-165` (12 chars) | #484's drop-oldest mutant | **"R2 anchor: inbuf[tail] survives"**, "R2 anchor: cell 0 untouched", "R4 fifo: first pop is first push" (3 of 3) |
   | `row()`: `row_cmp(why, sectors, sectors, sectors)` (2 identifiers) | word 57's high byte zeroed | **"threshold: >>8 byte reaches 255"** and 3 more |
   | `row_cmp()`: `(…) && sectors<4` | same | same 4 |
   | `row_cmp()`: its three `uint64_t` → `uint16_t` | word 58's low byte zeroed | "carry: >>8 wraps into >>16" and 4 more |
   | `chk()`: `&& (rows & 127) < 2` placed after `rows ++` | DRQ dropped for a non-empty ring | "R6 liveness: DRQ asserted", "R3 full ring: DRQ still set" |
   | `chk()`: `&& *name == '@'` placed after `rows ++` | same | same |

   - **Smallest inside a comparator:** ` && want-165`. It is keyed on a value no probe presents, so it is neither rows- nor name-keyed and falls outside the disclosure. Gate 2 calls "R2 anchor: inbuf[tail] survives" and "R4 fifo" ANCHORED.
   - **Smallest overall:** the 2-token `row()` edit. It sits outside every control: the self-check tests `row_cmp()`, the self-mutant pins `row_wide_geometry`, and nothing tests `row()`'s decode.

3. **The disclosure is a wrong record, inherited from ruling 7 (MEASURED).**
   - "(after the increment, the same test reds through `failures`)" and "placed before its rows ++" are false. The last two rows of finding 2 are post-increment and stay green; a name test cannot depend on increment order.
   - "Except the self-mutant's" is also false. That row compares inline, so no covered row is protected.
   - Suggested wording: "a test keyed on any value, name or position the probes do not present, in either comparator — or an edit to the code that feeds them — keeps gate 2 green; disclosed, not chased."

4. **Wide `row_cmp()` probes close the natural class (MEASURED).**
   - Add two probes, each disjunct wrong only above bit 32: (2^32, 0, 2^32) and (2^32, 2^32, 0).
   - Output is byte-identical to the final file except the SELFCHECK lines, with the same exit codes, on 8 device variants.
   - They red the `uint16_t` narrowing and `sectors<4` (2 of 11 probes).
   - They also make the block comment's "each operand zero and past 32 bits" true. Today that holds only for `chk()`; `row_cmp()`'s probe operands never exceed 3, and its `sectors` argument is never 0.
   - Ruling 1's four-probe list has this gap, and so did the four probes I proposed.

5. **Q4: G is an adequate but sole carrier; one small change reds the run itself (MEASURED).**
   - Forced failure removed plus `chk()` stubbed prints both SELFCHECK FAIL lines, then `128 rows, 0 failures`, `WDC_IDENTIFY_PASS`, exit 0.
   - Gate 2 reds exactly one row, G; the lane stays OK. The run's own verdict is false to anything reading the trailer or the exit status.
   - **Smallest change:** make PASS depend on the flag only the G arm sets: `static int sc_g;`, `sc_g = 1` in the G arm, `if (failures == 0 && sc_g)` and `return (failures || !sc_g) ? 1 : 0;`.
   - With it, the double edit prints `WDC_IDENTIFY_FAIL`, exits 1, and reds three gate-2 rows (offline verdict, G, lane).
   - **Byte-identity cost: none.** The whole log and exit code are identical to the final file on all 7 device variants. This makes ruling 6's "must still go red through `failures`" true.

6. **Hunks against the ruling (READ, with the measured items above).**
   - Rulings 1–5, 8 and 9 are implemented as ruled: the pure `row_cmp()`, the probe values, exact increments, runtime counts, the G line printed once and only if both runs passed, no "high byte" or named-row text, the token only in probe names and the comment, the heading without a count, the quoted replacement paragraph, the owner ruling cited, and `wdcidcomparators`.
   - Not as ruled:
     - Ruling 6's red-through-`failures` requirement is unmet (finding 5).
     - Ruling 7's text is implemented verbatim and is false (finding 3).

7. **Something else (MEASURED).** "24 of 128 rows compare inside a comparator the sentinel feeds" is accurate as worded. But the 2-token `row()` edit shows that "covered" means the comparator is live, not that the row is live — worth one clause in the gate-2 bullet.

---
*Recorded by the main loop: agent a088149d37f1fac24 (resumed for the pass 2 on the final diff), `agent_models.py` = clean, claude-opus-5-5; final text 2026-09-25T21:19:40.363Z UTC.  Same model family as the main loop: badge s.*
