OPUS551F2_ALIVE

VERDICT: PROCEED WITH CHANGES

**I would change 5 of your 9 dispositions: F2, F4, F6, F7, F9.**

How I measured: in WSL `/tmp/opus551f2`, from HEAD f4f601c4.
- **P** is F1+F2+F4 exactly as you dispositioned them. **Q** is my alternative (finding 4).
- "Gate 2" means the 73 wdc checks copied verbatim from `gate_offline.sh:1455-1877`, plus H, G, and the self-mutant lane following `selfmutant.py`'s logic.
- Scripts are `run2.sh`, `xform2.py` and `analyze2.py` in my scratchpad `opus551p1/`. The repo is untouched.

1. **(a) Byte-identity (measured).** P matches the original byte for byte except the SELFCHECK lines, with equal exit codes. That holds on the real `dev_wdc.c`, your four variants and two more of mine, at -O2 and at -O0 (with the `quiet_mode` stub in both arms). Q matches too.

2. **(b) Vacuity controls (measured).**
   - `chk()` stubbed to always pass: both sentinels print "2 of 3 deliberate mismatches went unnoticed" and the run ends with 2 failures.
   - `row()` stubbed: "1 of 3" at both sentinels.
   - Sentinel deleted: H and G both red. H only reds because my prototype keeps the token inside the block; a stray `@@SELFCHECK@@` in any comment keeps H green.

3. **(c) Two stateless edits keep gate 2 fully green on a defective device (measured).**
   - **` && got` added to `chk()`'s test (7 characters).** Both of F4's `chk()` probes have a nonzero `got`, so the sentinels pass. I deleted DRQ for a non-empty ring (every PIO data phase loses DRQ). The original reports 2 failures; P reports 128 rows, 0 failures, PASS.
   - **Delete `got57 != want ||` from `row()`.** F4's `row()` probe (1 vs 2) mismatches both word pairs at once, so it cannot see either disjunct disappear. `row()` is the only reader of words 57-58. I zeroed word 57's high byte, which makes "current capacity" wrong for every disk of 256 sectors or more. The original reports 4 failures; P reports 0 failures, PASS.
   - Q's sentinel reds both (2 of 9 and 1 of 9 probes wrong).
   - The stateful edit `&& (rows & 127) < 2` stays green under P and Q. That is F5's class, already disclosed.

4. **F2: change the form (measured, finding 3).** Do not add `want` to the 8 call sites. Split the comparison into a pure `row_cmp(why, sectors, got57, got60)` that `row()` calls. Output is identical and no call site changes. The sentinel can then feed each disjunct alone, and a zero `got`, without running the device.

5. **F4: change the probe set (measured).**
   - `chk()` probes: (1, 2), (2^32, 0), (0, 1), (0, 2^32), plus (7, 7), which must not fail.
   - `row_cmp` probes: 57 wrong alone, 60 wrong alone, zero, and a match.
   - Assert the exact increment (`== sc_f + 1`), not just that `failures` rose.
   - First and last placement is fine as you have it.
   - Widening `long` to `long long` changes nothing on LP64, where `long` is already 64-bit. It is harmless.

6. **F6: the 32 is wrong (measured).**
   - Of `chk()`'s 24 calls, 8 pass an inline `cond ? 1 : 0` verdict: R6 DRQ, R3 DRQ, R5b, R7 ×2, R8, R11 ×2.
   - That is exactly the verdict-sink shape F3 rejects for option A, and exactly the rows ` && got` silences permanently.
   - Honest text: "24 of 128 rows compare inside a sentinel-fed comparator (`chk` 16, `row` 8); 8 more hand `chk()` a 0/1 verdict."
   - Have the last sentinel print that count at runtime rather than writing a literal into the comment.
   - `wdcidverdict` names the very option F3 rejects; name the filing for B.

7. **F7: the variant set cannot prove the `chk()` edit (measured).** Your four named variants reach `chk()`'s FAIL arm at 0 of 24 rows, so the `%ld` → `%lld` change to the FAIL line is never exercised. My DRQ variant reaches 2 of 24. Add at least one variant that reddens a `chk()` row. The -O0 stub is confirmed necessary.

8. **F9 / Q2: this owes the owner a question (read).**
   - The ruling names nine functions, and F1+F2 covers one of them (`row()`).
   - The other eight carry the rows gate 2 greps by label: "packing anchor", "IDENTIFY agrees with itself", and "geometry words carry their high byte". The last is also the row the self-mutant pins.
   - Folding those eight onto `chk()` as real got/want rows is option B at 8 sites, not 95, and is plausible before 09-28 (not measured). It changes their printed text, and one gate grep keys on ok-line detail rather than the label (`of 65535 contradict their geometry`).
   - Suggested one-line question: ship 24 of 128 now and file the rest, or also fold the eight?

9. **F3, F5 and F8 stand.** F1 stands with the fraction corrected as in finding 6.

---
*Recorded by the main loop: agent a088149d37f1fac24 (resumed), `agent_models.py` = clean, opus-5-5 throughout.  Its
F2 scripts copied to `opus551_measured_f2/` (`.py` renamed `.py.txt`).*
