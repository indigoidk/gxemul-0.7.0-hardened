# #551c -- THE REPAIR'S OWN PASS: the test harness's comparator self-check after the F2 repair (measured)

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** (here `regress/`).  Pristine-2021-upstream copies of GXemul sit under the
project root; they are NOT this fork.  **If you cannot read files that is expected**: every fact you need is inlined;
name any premise you cannot settle from this packet rather than guessing.

**VERDICT LINE FIRST:** `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.

## 1. WHAT THIS IS

`regress/diff_wdc_identify.c` is an offline differential test (128 rows) of the emulator's IDE IDENTIFY data.  `#551`
gives it a SELF-CHECK: a block that feeds its two comparators, `chk()` and `row_cmp()`, known answers -- including
known MISmatches -- and requires each to change the failure count by exactly the right amount, first and last in the
run.  Gate 2 (`regress/gate_offline.sh`) then requires the file's log to print `SELFCHECK the comparator can still fail`
(the G row) and its source to carry the `@@SELFCHECK@@` token (the H row); it pins `grep -c 'high byte'` at 1 and runs a
self-mutant lane that needs one untagged pristine line.

The F2 pass on #551's pass 2 found three ways a covered row could stop being able to fail while gate 2 stayed green,
and the Fable 5.1 adjudication (`wdcidselfcheck_20260925/fable_f2b/fable5_f2b_550_551.md`) ruled the repair owes its OWN
pass on the panel.  **This is that pass.**  The repair, #551b -> #551c:

* two more `row_cmp()` probes, (sectors 0, got57 1, got60 0) and (0, 0, 1): each disjunct wrong alone with got ABOVE its
  want, and sectors 0 -- a `<` in place of `!=`, and an added `&& sectors`, each answered every earlier probe right;
* `cmp_fails`: the two comparators count their own failures (nothing else touches it; the self-check restores it with
  `failures`), and the trailer reports the larger of the two counts -- so a `failures = 0;` placed after the covered
  rows no longer turns the run green; untampered runs are unchanged, since `failures` always counts at least what the
  comparators counted;
* a self-check that did not pass counts one failure in the trailer (the trailer used to read "0 failures" beside
  `WDC_IDENTIFY_FAIL` for one double edit);
* the disclosure in its general form: the self-check proves only that the comparators answer right on ITS OWN calls;
  a reset of `failures` alone is caught, a reset of BOTH tallies is disclosed (Fable ruling 6).

## 2. SETTLED PREMISES

* The Fable 5.1 ruling on the F2 pass: #551 SHIP WITH CHANGES, 1 of 11 dispositions changed (disclose the two-statement
  reset); #551c owes its own pass on the panel, closing on a VALID zero whose denominator names the swept shapes.
* `main(void)` calls the self-check exactly twice, `"first"` then `"last"`, with literal arguments.
* Gate 2 greps the per-stem log for the G text and the source for the token (read, `gate_offline.sh`).

## 3. MEASURED (`wdcidselfcheck_20260925/measured/run551c.out`, file md5 765f71d8)

(a) The new file against HEAD's, built at -O2 and -O0 (with a one-line `quiet_mode` stub in both arms), on the real
`dev_wdc.c` and six variants of it: **14 of 14 byte-identical except the SELFCHECK lines, same exit codes.**

(b) Controls and escapes (variant, device, exit code, trailer, PASS count):

```
## (b) vacuity controls and escapes    
MINE_chkstub pristine rc=1 | 128 rows, 2 failures | 0
MINE_rowstub pristine rc=1 | 128 rows, 2 failures | 0
MINE_nosc pristine rc=0 | 128 rows, 0 failures | 1
MINE_scnoforce pristine rc=0 | 128 rows, 0 failures | 1
MINE_scnoforce_chkstub pristine rc=1 | 128 rows, 1 failures | 0
MINE_scnoforce_chkstub drqring rc=1 | 128 rows, 1 failures | 0
MINE_scnoforce_rowstub pristine rc=1 | 128 rows, 1 failures | 0
MINE_drop60 pristine rc=1 | 128 rows, 2 failures | 0
MINE_drop60 w57hi rc=1 | 128 rows, 6 failures | 0
MINE_andgot pristine rc=1 | 128 rows, 2 failures | 0
MINE_andgot drqring rc=1 | 128 rows, 2 failures | 0
MINE_drop57 pristine rc=1 | 128 rows, 2 failures | 0
MINE_drop57 w57hi rc=1 | 128 rows, 2 failures | 0
MINE_rows pristine rc=0 | 128 rows, 0 failures | 1
MINE_rows srstbit rc=1 | 128 rows, 11 failures | 0
MINE_u16 pristine rc=1 | 128 rows, 2 failures | 0
MINE_sect4 pristine rc=1 | 128 rows, 2 failures | 0
MINE_wrap pristine rc=0 | 128 rows, 0 failures | 1
MINE_wrap w57hi rc=0 | 128 rows, 0 failures | 1
MINE_want165 pristine rc=0 | 128 rows, 0 failures | 1
MINE_postinc pristine rc=0 | 128 rows, 0 failures | 1
MINE_postinc drqring rc=0 | 128 rows, 0 failures | 1
MINE_name pristine rc=0 | 128 rows, 0 failures | 1
MINE_name drqring rc=0 | 128 rows, 0 failures | 1
MINE_lt pristine rc=1 | 128 rows, 2 failures | 0
MINE_lt w57hi rc=1 | 128 rows, 6 failures | 0
MINE_andsect pristine rc=1 | 128 rows, 2 failures | 0
MINE_reset pristine rc=0 | 128 rows, 0 failures | 1
MINE_reset drqring rc=1 | 128 rows, 2 failures | 0
MINE_reset w57hi rc=1 | 128 rows, 4 failures | 0
MINE_reset2 drqring rc=0 | 128 rows, 0 failures | 1
MINE_reset2 w57hi rc=0 | 128 rows, 0 failures | 1
MINE_phase pristine rc=0 | 128 rows, 0 failures | 1
MINE_phase drqring rc=0 | 128 rows, 0 failures | 1
ORIG drqring rc=1 | 128 rows, 2 failures | 0
ORIG w57hi rc=1 | 128 rows, 4 failures | 0
ORIG srstbit rc=1 | 128 rows, 11 failures | 0
RUN551C_DONE         
```

Reading (b): `rc=1` / `0 PASS` is red.  RED as intended: chk() and row_cmp() stubbed, each disjunct dropped, `&& got`,
u16 operands, `&& sectors<4`, `<` (`lt`), `&& sectors` (`andsect`), the single-tally reset (`reset`, on the two failing
device variants), and the double edits (`scnoforce_*`, now "1 failures").  GREEN as DISCLOSED: a rows-keyed test
(`rows`, `postinc`), a name-keyed test (`name`, `phase`), a value-keyed test (`want165`), the feed edit (`wrap`), and
the both-tally reset (`reset2`).  `nosc` (the block deleted, with the verdict's use of its flag) prints PASS with no G
line and no token: gate 2's G and H rows are what catch it.  `reset` on the pristine device has no failure to hide.

## 4. THE DIFF (#551b -> #551c), INLINED

### 4a. regress/diff_wdc_identify.c

```diff
--- regress/diff_wdc_identify.c	2026-09-25 16:29:27.233710200 -0500
+++ regress/diff_wdc_identify.c	2026-09-25 17:12:45.870004700 -0500
@@ -505,6 +505,7 @@
     disjunct alone, and a zero, without building a device.  row() and its eight callers are unchanged in
     what they print.  */
 static int rowcmp_calls;
+static int cmp_fails;	/*  failures the two comparators counted; only they touch it  */
 
 static void row_cmp(const char *why, uint64_t sectors, uint64_t got57, uint64_t got60)
 {
@@ -516,6 +517,7 @@
 		    why, (unsigned long long)sectors,
 		    (unsigned long long)got57, (unsigned long long)got60);
 		failures ++;
+		cmp_fails ++;
 	} else {
 		printf("  ok   %-38s %llu\n", why, (unsigned long long)sectors);
 	}
@@ -4865,6 +4867,7 @@
 	rows ++;
 	if (got != want) {
 		failures ++;
+		cmp_fails ++;
 		printf("  FAIL %-40s got %lld want %lld\n", name, got, want);
 	} else
 		printf("  ok   %-40s %lld\n", name, got);
@@ -5643,7 +5646,8 @@
 
 /*
  *  @@SELFCHECK@@ -- #551.  CAN THIS FILE'S COMPARATORS STILL FAIL?  Feeds chk() and row_cmp() known answers --
- *  each operand zero and past 32 bits, each of row_cmp()'s two disjuncts alone, and one pair that must NOT
+ *  each operand zero and past 32 bits, each of row_cmp()'s two disjuncts alone and on either side of its
+ *  want, and one pair that must NOT
  *  fail -- and requires the EXACT change in `failures' for each, restoring `rows' and `failures' after every
  *  probe.  Run FIRST (before any row) and LAST (after every row, before the identity row), so a comparator
  *  that goes inert partway through is caught at one end or the other.  Only the success arm prints gate 2's G
@@ -5653,10 +5657,14 @@
  *  each comparator took.  Of chk()'s calls, the ones in row_ring_occupancy_sound() that pass a
  *  `cond ? 1 : 0' (or `? 0 : 1') hand it a VERDICT computed at the call, not a comparison, and every
  *  other row in this file compares inline: neither is covered by this block.  "Covered" means the
- *  COMPARATOR is live, not that a row is.  NOT CAUGHT, DISCLOSED: a test keyed on a value, a name or a
- *  position the probes do not present, in either comparator, and an edit of the code that FEEDS them
- *  (row() handing row_cmp() its own want), keep every gate-2 row green -- measured, pass 2 of #551;
- *  reviewed in the differential, not chased.  No line this block prints carries the self-mutant row's
+ *  COMPARATOR is live, not that a row is.  NOT CAUGHT, DISCLOSED: the self-check proves only that the
+ *  comparators answer right on ITS OWN calls, so an edit that keeps those answers and changes the rest
+ *  keeps every gate-2 row green -- a test keyed on a value, a name, a position or the self-check's own
+ *  phase that the probes do not share; an edit of the code that FEEDS the comparators (row() handing
+ *  row_cmp() its own want); an edit of this block itself.  Measured on #551's passes; reviewed in the
+ *  differential, not chased.  A reset of `failures' ALONE after the comparators is not among them: they
+ *  also count cmp_fails, which only they touch, and the trailer reports the larger.  A reset of BOTH
+ *  tallies is, and is disclosed.  No line this block prints carries the self-mutant row's
  *  text or "high byte" (gate 2 counts both).  Gate 2's G text is printed ONCE, by the last run, only
  *  when both runs passed -- and the run's own PASS needs that line (sc_g), so a self-check that failed
  *  fails the run even if its forced failure is gone.  The rest of the file is filed as
@@ -5669,27 +5677,28 @@
 {
 	static const long long cg[] = { 1, 0x100000000LL, 0, 0, 7 };
 	static const long long cw[] = { 2, 0, 1, 0x100000000LL, 7 };
-	static const uint64_t rw[] = { 2, 2, 1, 3, 0x100000000ULL, 0x100000000ULL };
-	static const uint64_t r57[] = { 1, 2, 0, 3, 0, 0x100000000ULL };
-	static const uint64_t r60[] = { 2, 1, 0, 3, 0x100000000ULL, 0 };
-	int sc_f = failures, sc_r = rows, sc_c = chk_calls, sc_rc = rowcmp_calls, sc_bad = 0, i, n = 0;
+	static const uint64_t rw[] = { 2, 2, 1, 3, 0x100000000ULL, 0x100000000ULL, 0, 0 };
+	static const uint64_t r57[] = { 1, 2, 0, 3, 0, 0x100000000ULL, 1, 0 };
+	static const uint64_t r60[] = { 2, 1, 0, 3, 0x100000000ULL, 0, 0, 1 };
+	int sc_f = failures, sc_r = rows, sc_c = chk_calls, sc_rc = rowcmp_calls, sc_cf = cmp_fails, sc_bad = 0;
+	int i, n = 0;
 
 	for (i = 0; i < 5; i++, n++) {
 		chk("@@SELFCHECK@@/chk", cg[i], cw[i]);
 		if (failures != sc_f + (cg[i] != cw[i]))
 			sc_bad++;
-		failures = sc_f; rows = sc_r;
+		failures = sc_f; rows = sc_r; cmp_fails = sc_cf;
 	}
-	for (i = 0; i < 6; i++, n++) {
+	for (i = 0; i < 8; i++, n++) {
 		row_cmp("@@SELFCHECK@@/row", rw[i], r57[i], r60[i]);
 		if (failures != sc_f + (r57[i] != rw[i] || r60[i] != rw[i]))
 			sc_bad++;
-		failures = sc_f; rows = sc_r;
+		failures = sc_f; rows = sc_r; cmp_fails = sc_cf;
 	}
 	chk_calls = sc_c; rowcmp_calls = sc_rc;
 	if (sc_bad) {
 		printf("  FAIL  SELFCHECK(%s): %d of %d probes answered wrongly\n", where, sc_bad, n);
-		failures = sc_f + 1; rows = sc_r;
+		failures = sc_f + 1; rows = sc_r; cmp_fails = sc_cf;
 	}
 	if (where[0] == 'f') {
 		sc_first_bad = sc_bad;
@@ -5810,6 +5819,12 @@
 		printf("  ok   %-38s %i\n", "[IDENTITY] row count", rows);
 	}
 
+	/*  #551: the comparators' own count survives a reset of `failures' (which always counts at least as
+	    many, untouched), and a self-check that did not pass is a failure the count shows.  */
+	if (cmp_fails > failures)
+		failures = cmp_fails;
+	if (!sc_g && failures == 0)
+		failures = 1;
 	printf("\n%d rows, %d failures\n", rows, failures);
 	if (failures == 0 && sc_g)
 		printf("WDC_IDENTIFY_PASS\n");
```

### 4b. regress/gate_offline.sh (the #551 bullet)

```diff
--- regress/gate_offline.sh	2026-09-25 16:30:53.012469700 -0500
+++ regress/gate_offline.sh	2026-09-25 17:12:45.903630500 -0500
@@ -2261,12 +2261,16 @@
 #                   verdict computed at the call (derive: grep -cE '\? [01] : [01], 1\);'
 #                   regress/diff_wdc_identify.c), and the other
 #                   96 compare inline -- NOT covered.  "Covered" means the COMPARATOR is live,
-#                   not that a row is: an edit of the code that feeds it (row() handing
-#                   row_cmp() its own want), or a test keyed on a value, a name or a position
-#                   the probes do not present, keeps gate 2 green -- measured on #551's pass 2,
-#                   disclosed, not chased.  The file prints its comparator call counts on every
-#                   run, and its PASS needs the G line.  #551, by owner ruling 2026-09-25
-#                   ("24/128 now, file the rest"); the rest is `wdcidcomparators'.
+#                   not that a row is: the self-check proves only its own calls, so an edit that
+#                   keeps those right keeps gate 2 green -- a test keyed on a value, a name, a
+#                   position or the self-check's phase that the probes do not share, feeding a
+#                   comparator its own want, or an edit of the self-check itself (measured on
+#                   #551's passes; disclosed, not chased).  A reset of `failures' alone is not:
+#                   the comparators keep their own count and the trailer reports the larger; a
+#                   reset of both tallies is, and is disclosed.  The
+#                   file prints its comparator call counts on every run, and its PASS needs the
+#                   G line.  #551, by owner ruling 2026-09-25 ("24/128 now, file the rest"); the
+#                   rest is `wdcidcomparators'.
 #  rtc_range is in the UNIFORM group: every row goes through chk(), its single comparator.
 #  Named here rather than left to be re-derived, because the exception list above
 #  is only trustworthy if additions are classified as they arrive.
```

## 5. QUESTIONS

1. **The floor question for the self-check:** is there an edit to either comparator, to the code between them and the
   trailer, or to the trailer's two new lines -- outside the disclosed classes -- that keeps every gate-2 check green
   while a covered row can no longer fail?  Name the edit and the row it silences; a zero needs its denominator (the
   shapes you tried).
2. **Does any new sentence say something false** -- in the block comment, the trailer comment, or the gate-2 bullet?
3. **Is disclosing the both-tally reset right**, or is there a cheap measured way to close it too?
4. **Does any change alter a healthy run's output** beyond the SELFCHECK lines?

If, while verifying a claim, you found something ELSE -- say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
