# #551 wdcidselfcheck -- THE §F2 PASS: every seat's pass-1 findings, and my disposition on each

The tree is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\` (ignore any other `src/`).  **FIRST LINE:**
`VERDICT: <PROCEED | PROCEED WITH CHANGES | DO NOT PROCEED>`, then numbered findings.  **The load-bearing question:
WHICH OF MY DISPOSITIONS BELOW IS WRONG?  Name the count.**  If you raised a finding, be HARDER on it than on anyone
else's, including whether the fix I propose for it is right.  If you cannot read files, everything you need is inlined.

## SETTLED PREMISES (re-inlined; do not re-derive)

* Owner ruling 2026-09-25, the option the owner chose, verbatim: "Fix wdc_identify now -- a harness round right after
  #549 that moves diff_wdc_identify.c's nine row functions onto one comparator with a @@SELFCHECK@@ block, done before
  09-28.  Only ieee_store gets re-dated."  *(That option text was written by me from the exemption's own 2026-08-19
  census; the census was stale -- see F1.)*
* Gate 2 checks, per COVERED stem: `@@SELFCHECK@@` in the SOURCE (H); the text `SELFCHECK the comparator can still fail`
  in the LOG (G, a bare `grep -q`, no `ok` anchor); and separately a self-mutant of `dev_wdc.c` that must red the named
  row "geometry words carry their high byte".  `SC_EXEMPT`'s `wdc_identify:2026-09-27` reds one gate-2 row from 09-28.
* gate_offline.sh ALREADY ACCEPTS PARTIAL coverage when it is stated: its COVERED comment lists `sh4_tmu` (12 of 18
  rows through its one comparator), `geom` and `sync` as the stems whose sentinel does not cover every row.

## PASS 1 -- WHO SAID WHAT (panel_20260925_141428 + dedicated jobs; Opus measured)

PROCEED WITH CHANGES: agy, grok (panel), glm, minimax, kimi-k3:cloud, Opus 5.5 (measured: prototypes, counts, a
forced-site differential).  DO NOT PROCEED: deepseek, grok (dedicated job).  codex: WALLED (usage limit, resets
2026-09-26 07:01) on both the panel seat and the dedicated job -- a SEAT FAILURE, not agreement.  kimi CLI: weekly
wall, covered by kimi-k3:cloud.

## FINDINGS AND MY DISPOSITIONS

* **F1 (grok ded., Opus, agy, grok; MEASURED): the exemption's premise is stale.**  The file already has a got/want
  comparator, `static void chk(const char *name, long got, long want)`, added by #484 on 2026-08-27, carrying 24 of
  the 128 rows; and `row(why, sectors)` carries 8 more (its want is derived from its input -- the exemption's point,
  true of those 8 only).  95 `failures ++` sites in 61 functions; 95 executable `rows ++` (the 96th hit is a comment).
  **DISPOSITION: ACCEPT.  The fix is a sentinel on the comparators the file HAS, with the fraction stated -- not a
  95-site refactor.**
* **F2 (glm; Opus's "C′"): give `row()` an explicit `want`** so its 8 rows can be fed a mismatch too: `row(why,
  sectors, want)` with `want == sectors` at all 8 call sites, and the sentinel calls `row("@@SELFCHECK@@/row", 1, 2)`.
  **DISPOSITION: ADOPT** -> 32 of 128 rows go through a comparator a sentinel can feed.
* **F3 (contested): option A, a shared verdict helper `row_failed(int c)` over the other sites.**  For (agy, grok, glm,
  minimax, kimi, Opus -- each WITH conditions: rename away from `bad`, strict 0/1 contract, a hardened sentinel checking
  return values with inputs {1, 0, 2, 0x10000, -1}, first AND last, a forced-site differential as the equivalence
  proof, a one-`failures ++` gate pin).  Against (deepseek, grok ded.): it feeds a COUNTER, not a comparison, so the G
  text "the comparator can still fail" would be printed about something that is not a comparator; Opus agrees that
  "it guards a single point of failure that A itself creates" and that "the net gain is manifest conformance ... not
  coverage of any comparison"; and a fuse honouring calls 1, 2 and 127 keeps every gate-2 check green (grok ded.).
  **DISPOSITION: DO NOT SHIP A IN #551.  FILE it** (`wdcidverdict`, with every measured requirement above) as the
  route to the other 96 rows, where the honest end state is a COMPARATOR per site (option B), not a verdict sink.
  #551 ships F1+F2 only.
* **F4 (grok, Opus, kimi, minimax, glm): sentinel design.**  Probe `chk()` NARROW (1 vs 2) and WIDE (0x100000000 vs 0)
  -- the file's defect class is a high byte -- and `row()` (1 sector vs want 2); widen `chk()`'s `long` parameters to
  `long long` (`%ld` -> `%lld`; the output is unchanged for every value the rows pass, which the byte-identity run
  below must show).  Run the sentinel FIRST (before any row) AND LAST (after every row, before the identity row), each
  restoring `rows` and `failures`.  Print the G text ONLY from the success arm, as a raw `printf`; the failure arm prints
  a line WITHOUT the G text and forces `failures = sc_f + 1`, as `diff_rtc_range.c` does.  **ADOPT.**
* **F5 (Opus, grok; MEASURED): the stateful-helper class survives every placement** (`if (rows && rows < 125) return
  0;` inside a comparator).  **DISCLOSE under clause (e)** in the COVERED comment, as `rtc_range`'s `chk()` already
  bears; not chased.
* **F6 (all): gate 2's text.**  `SC_COVERED` gains `wdc_identify`, `SC_EXEMPT` loses it, and the COVERED comment's
  exception list gains a bullet: *"wdc_identify -- 32 of 128 rows through a comparator the sentinel feeds (`chk()` 24,
  `row()` 8); the other 96 compare inline and are NOT covered; stateful comparator edits disclosed; the route to the
  rest is filed as `wdcidverdict`."*  The stale "NOTHING TO FEED A MISMATCH TO" paragraph is REPLACED by its correction,
  quoting what it said.  **ADOPT.**
* **F7 (Opus; MEASURED): the equivalence proof.**  With no 95-site edit, it reduces to: build before and after at -O2
  (gate 2's line) and at -O0 with a one-line `quiet_mode` stub linked into BOTH arms (without it -O0 does not link, and a
  diff of two failed builds reads "identical"); on the real `dev_wdc.c` and the four `dev_wdc.c` variants Opus used
  (the self-mutant, the `% 255` revert, a 13-bit cylinder truncation, the pre-#481 reset bit), require byte-identical
  stdout except the SELFCHECK lines.  Then the vacuity controls, MEASURED: `chk()` stubbed to always pass -> the
  SELFCHECK reds; `row()`'s compare stubbed -> reds; the SELFCHECK deleted -> gate 2's H and G red.  **ADOPT.**
* **F8 (Opus; read): `diff_fbpending_bound.c` prints its SELFCHECK verdict through the helper under test, and its FAIL
  line still contains the G text, so G cannot fail there.**  **FILE** (`fbpendingselfcheckG`), with glm's companion:
  `diff_rtc_range.c`'s sentinel runs only first (the same stateful window) -- one filing, "sentinel placement and the G
  text across the COVERED stems".
* **F9 (deepseek): "A is not ONE comparator"; (glm): the owner's "nine functions" cannot be executed literally.**
  **DISPOSITION:** answered by F1-F3 -- #551 ships a sentinel on the comparators that exist, states 32 of 128, and does
  not claim the rest; the ruling's intent (fix, not re-date) is met honestly and its stale premise is recorded.

## QUESTIONS
1. Which of my dispositions is wrong -- name the count.  Especially F3 (file A rather than ship it) and F2 (row()'s
   explicit want): is either wrong?
2. Is "32 of 128, stated" an honest discharge of the owner's "fix it", or does it owe the owner a question?
3. The smallest edit to the F1+F2+F4 design that keeps gate 2 green while a covered row can no longer fail?
If, while verifying a claim, you found something ELSE -- say so.
