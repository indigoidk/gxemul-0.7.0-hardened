# #551e -- THE ENUMERATION-VERIFYING PASS: the test harness's comparator self-check, contract rewritten (measured)

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** (here `regress/`).  There are THREE pristine-2021-upstream copies of GXemul
under the project root; they are NOT this fork.  **The working tree's `regress/diff_wdc_identify.c` is #551's FIRST
version**; #551e exists only as the generated file and the diff inlined below.  Review the INLINED code.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any premise you cannot settle
from this packet rather than guessing at it.

**VERDICT LINE FIRST:** `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.

## 1. WHAT THIS IS, AND WHAT THIS PASS IS FOR

`regress/diff_wdc_identify.c` is an offline differential test (128 rows) of the emulator's IDE IDENTIFY data, built
against the REAL `src/devices/dev_wdc.c`.  #551 gives it a SELF-CHECK that feeds its two comparators, `chk()` and
`row_cmp()`, known answers and requires each to change the failure tallies by exactly the right amount, first and last
in the run.  Gate 2 then requires the log to print the G line and the source to carry the `@@SELFCHECK@@` token.

**The chain so far.**  #551b and #551c each had a pass that found a single edit keeping gate 2 green while a covered row
stopped failing; each was repaired.  #551d's own pass (nine transports, codex and the kimi CLI walled; the dedicated grok
job; the Opus measuring seat, 34 variants) found **no single edit outside the disclosed classes** -- every one of 24
measured single edits was red -- but found COMPOSITES (two or three coordinated edits, each red alone) that keep gate 2
green, and one POSITIONAL composite: the covered rows moved past the verdict with the identity row re-pinned.

**The adjudication (the Fable 5.1 seat, `pass551d/fable5_pass551d.md`) -- its sentences, CONDENSED where `...` marks a
cut; the full text is in that file:**

> The composites are not floor breaches ... but "disclose the class" must not become the way to dodge a closable class.
> The question is whether the trailer class is closable in-file.  It is not: everything gate 2 reads is produced at one
> call site in `main()`, a probe cannot pin a call site, and any single-call-site helper is inlined away by one edit ...
> So the trailer becomes CONTRACT, honestly worded (Q3), and the chain does not stay open for it.
>
> **#551e is owed anyway, and contains exactly:** (1) the call-count pin at the last self-check ... (2) the
> block-comment and gate-2 bullet
> ... Then ONE pass ... whose job is to VERIFY THE ENUMERATION: it closes on a valid zero where a composite inside the
> four named classes is a contract fact, not a finding; only a single edit outside the four classes, or a class the
> contract does not name, reopens.
>
> One caution: the "not closable in-file" claim is reasoned from the single-call-site argument, not measured; a seat
> that shows an in-file pin on `main()`'s trailer that survives one inlining edit and one inserted conditional reset
> would overturn it, and #551e's pass should be asked exactly that.

It overturned one of my dispositions (I had proposed FILING the call-count pin; it ruled ADOPT: "disclosing a closable
cell while filing a six-line fix is the addition licence inverted"), refined three, upheld seventeen.

## 2. SETTLED PREMISES (re-inlined; each verified against the generated #551e file, md5 1b467a08)

* **Who writes the tallies.**  `failures` and `rows` are file-scope ints.  `cmp_fails` is incremented ONLY inside
  `chk()` and `row_cmp()`, each time beside `failures ++`; `selfcheck()` assigns it back (a restore, three places).  The
  96 inline rows, the identity row and the self-check's forced failure write `failures` alone.
* **main()'s order**: `selfcheck("first");` -> eight `row(...)` calls (each into `row_cmp()`) -> 59 zero-argument
  `row_*()` calls, among them `row_ring_occupancy_sound();` (all 24 `chk()` calls) and, later,
  `row_wide_geometry();` (an INLINE row; the self-mutant lane's row) -> `selfcheck("last");` -> the IDENTITY row
  (`rows != 128` -> `failures ++`) -> the trailer (inlined in 4b).
* **Coverage.**  24 rows compare inside a comparator the self-check feeds: 16 of `chk()`'s 24 calls and all 8 of
  `row_cmp()`'s.  `chk()`'s other 8 are handed a 0/1 verdict computed at the call (derive: `grep -cE '\? [01] : [01],
  1\);' regress/diff_wdc_identify.c` = 8); the other 96 rows compare inline.  24 + 8 + 96 = 128.
* **Gate 2's checks on this log** (read in `gate_offline.sh`): the printed failure count must be `0` (`grep -oE '[0-9]+
  failures'`); rows run at least 42 (`check_min`); `WDC_IDENTIFY_PASS` exactly once; sixteen named rows present once
  each; `high byte` once; the G text; the `@@SELFCHECK@@` token in the source; and the self-mutant lane
  (`selfmutant.py`: on the device mutant it needs `WDC_IDENTIFY_FAIL` and a FAIL line naming the geometry row).  **Gate
  2 discards the exit status.**
* The owner ruled #551's scope on 2026-09-25: *"24/128 now, file the rest"* (`wdcidcomparators`).

## 3. THE CODE UNDER REVIEW (the generated #551e file, md5 1b467a08)

### 3a. The block comment -- the contract, with its four disclosed classes

```c
/*
 *  @@SELFCHECK@@ -- #551.  CAN THIS FILE'S COMPARATORS STILL FAIL?  Feeds chk() and row_cmp() known answers --
 *  each operand zero and past 32 bits, each of row_cmp()'s two disjuncts alone with got both below and
 *  above its want, and one probe per comparator that must NOT fail -- and requires the EXACT change in
 *  `failures' and in cmp_fails for each, restoring `rows', `failures' and cmp_fails after every probe.
 *  Run FIRST (before any row) and LAST (after every row, before the identity row), so a comparator that
 *  goes inert partway through is caught at one end or the other; the LAST run also requires every
 *  covered call to have run before it (chk() 24, row_cmp() 8).  Only the success arm prints gate 2's G
 *  text; the failure arm does not, and forces one failure.
 *
 *  WHAT IT COVERS: the rows that go through chk() and row_cmp() -- the last run prints how many calls
 *  each comparator took.  Of chk()'s calls, the ones in row_ring_occupancy_sound() that pass a
 *  `cond ? 1 : 0' (or `? 0 : 1') hand it a VERDICT computed at the call, not a comparison, and every
 *  other row in this file compares inline: neither is covered by this block.  "Covered" means the
 *  COMPARATOR is live, not that a row is.
 *
 *  NOT CAUGHT, DISCLOSED.  This block pins the two COMPARATORS and nothing else: it proves they answer
 *  right on ITS OWN calls, so an edit that keeps those answers and changes the rest CAN keep every gate-2
 *  row green.  Four classes, each measured on #551's passes: (1) inside a comparator, a test keyed on a
 *  value, a name, a position or this block's own phase that the probes do not share, or a predicate
 *  rewritten to agree with the original on every probe and differ elsewhere (the sum of the two gots
 *  against twice the want, say -- one member of a class no finite probe set closes); (2) the code that
 *  FEEDS a comparator (row() handing row_cmp() its own want); (3) THE TRAILER, one call site: the printed
 *  count, the PASS token and the exit status are produced there, and any rewrite that keeps them
 *  consistent with each other is green -- today two coordinated edits, each red alone (the verdict's
 *  cmp_fails term dropped with `failures -= cmp_fails' after the reconciliation; the verdict and the
 *  printed count both scoring `failures - cmp_fails'); a reset of BOTH tallies is in this class --
 *  unconditional, only after the covered rows and before the self-mutant's row; conditional on their
 *  equality, anywhere.  No in-file probe can pin a single call site; the close is gate-side, a lane
 *  whose device mutant fails the FIRST covered row (filed: `wdcidlane'); (4) this block itself (a probe's
 *  cmp_fails check weakened together with the increment it guards and a reset).  A reset of `failures'
 *  alone is not among them, wherever it sits: the comparators also count cmp_fails, which only they
 *  increment, and the verdict and the exit status read it directly.  Nor is moving the covered rows past
 *  the verdict: the LAST run requires chk() 24 and row_cmp() 8 calls.  On #551d's pass no single edit
 *  outside these four classes kept gate 2 green (24 measured:
 *  regress/artifacts/wdcidselfcheck_20260925/opus551_measured_d/analyze6.out).  Reviewed in the
 *  differential, not chased.
 *
 *  No line this block prints carries the self-mutant row's
 *  text or "high byte" (gate 2 counts both).  Gate 2's G text is printed ONCE, by the last run, only
 *  when both runs passed -- and the run's own PASS needs that line (sc_g), so a self-check that failed
 *  fails the run even if its forced failure is gone.  The rest of the file is filed as
 *  `wdcidcomparators' (#551; owner ruling 2026-09-25).
 */
```

### 3b. The self-check, with the call-count pin (`#551e:` comment)

```c
static int sc_first_bad = -1;	/*  -1 until the FIRST run has happened  */
static int sc_g;	/*  set ONLY where gate 2's G line prints: the run's PASS needs it  */

static void selfcheck(const char *where)
{
	static const long long cg[] = { 1, 0x100000000LL, 0, 0, 7 };
	static const long long cw[] = { 2, 0, 1, 0x100000000LL, 7 };
	static const uint64_t rw[] = { 2, 2, 1, 3, 0x100000000ULL, 0x100000000ULL, 0, 0 };
	static const uint64_t r57[] = { 1, 2, 0, 3, 0, 0x100000000ULL, 1, 0 };
	static const uint64_t r60[] = { 2, 1, 0, 3, 0x100000000ULL, 0, 0, 1 };
	int sc_f = failures, sc_r = rows, sc_c = chk_calls, sc_rc = rowcmp_calls, sc_cf = cmp_fails, sc_bad = 0;
	int i, n = 0;

	for (i = 0; i < 5; i++, n++) {
		chk("@@SELFCHECK@@/chk", cg[i], cw[i]);
		if (failures != sc_f + (cg[i] != cw[i]) || cmp_fails != sc_cf + (cg[i] != cw[i]))
			sc_bad++;
		failures = sc_f; rows = sc_r; cmp_fails = sc_cf;
	}
	for (i = 0; i < 8; i++, n++) {
		row_cmp("@@SELFCHECK@@/row", rw[i], r57[i], r60[i]);
		if (failures != sc_f + (r57[i] != rw[i] || r60[i] != rw[i])
		    || cmp_fails != sc_cf + (r57[i] != rw[i] || r60[i] != rw[i]))
			sc_bad++;
		failures = sc_f; rows = sc_r; cmp_fails = sc_cf;
	}
	chk_calls = sc_c; rowcmp_calls = sc_rc;
	if (sc_bad) {
		printf("  FAIL  SELFCHECK(%s): %d of %d probes answered wrongly\n", where, sc_bad, n);
		failures = sc_f + 1; rows = sc_r; cmp_fails = sc_cf;
	}
	if (where[0] == 'f') {
		sc_first_bad = sc_bad;
		if (!sc_bad)
			printf("  ok    SELFCHECK(first): all %d probes answered right\n", n);
		return;
	}
	/*  #551e: the LAST run also requires every covered call to have run BEFORE it -- chk() 24 and row_cmp() 8,
	    the counts the note line below prints.  Covered rows moved past the verdict, with the identity row
	    re-pinned, would otherwise print their FAILs after the PASS token.  Change these with the rows, as the
	    identity row's 128.  */
	if (chk_calls != 24 || rowcmp_calls != 8) {
		printf("  FAIL  SELFCHECK(last): chk() ran %d times and row_cmp() %d before this run; want 24 and 8\n",
		    chk_calls, rowcmp_calls);
		if (!sc_bad)
			failures = sc_f + 1;
		sc_bad++;
	}
	if (!sc_bad && sc_first_bad == 0) {
		sc_g = 1;
		printf("  ok    SELFCHECK the comparator can still fail (first and last)\n");
	} else if (!sc_bad)
		printf("  FAIL  SELFCHECK(last): the first run did not run, or did not pass\n");
	printf("  note  SELFCHECK comparator calls this run: chk() %d, row_cmp() %d\n",
	    chk_calls, rowcmp_calls);
}
```

### 3c. The identity row and the trailer

```c
	/*
	 *  IDENTITY GUARD.  Two files with this name once differed only by the case of a
	 *  parent directory, and the stale one encoded a REVERSED design decision.  A row
	 *  count is the cheapest proof that the file which RAN is the file that was
	 *  reviewed.  Last, so it counts every row above it.
	 *
	 *  It is also floor clause (c): against a null medium -- a stale copy, or a
	 *  comment-only source -- this row is what refuses to report a pass.
	 */
	rows ++;
	if (rows != 128) {
		printf("  FAIL %-38s rows = %i, want 128\n",
		    "[IDENTITY] row count", rows);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n", "[IDENTITY] row count", rows);
	}

	/*  #551: the PRINTED count shows the comparators' failures even after a reset of `failures' placed
	    before this line (untouched, `failures' always counts at least as many); the verdict and the exit
	    status read cmp_fails directly.  A self-check that did not pass is a failure the count shows.  */
	if (cmp_fails > failures)
		failures = cmp_fails;
	if (!sc_g && failures == 0)
		failures = 1;
	printf("\n%d rows, %d failures\n", rows, failures);
	if (failures == 0 && cmp_fails == 0 && sc_g)
		printf("WDC_IDENTIFY_PASS\n");
	else
		printf("WDC_IDENTIFY_FAIL\n");
	return (failures || cmp_fails || !sc_g) ? 1 : 0;
}
```

## 4. MEASURED -- `regress/artifacts/wdcidselfcheck_20260925/measured/run551e.out`

`# #551 measurement 2026-09-25 18:25:58 -- MINE md5 1b467a08, ORIG md5 1fd7ff1d`

(a) the #551e file against HEAD's, -O2 and -O0 (a one-line `quiet_mode` stub linked into both arms), on the real
`dev_wdc.c` and six variants of it -- byte-identical except the SELFCHECK lines?  same exit code?

```
pristine  O2  IDENTICAL rc ORIG=0 MINE=0  | 128 rows, 0 failures
pristine  O0  IDENTICAL rc ORIG=0 MINE=0  | 128 rows, 0 failures
selfmut   O2  IDENTICAL rc ORIG=1 MINE=1  | 128 rows, 1 failures
selfmut   O0  IDENTICAL rc ORIG=1 MINE=1  | 128 rows, 1 failures
rev255    O2  IDENTICAL rc ORIG=1 MINE=1  | 128 rows, 9 failures
rev255    O0  IDENTICAL rc ORIG=1 MINE=1  | 128 rows, 9 failures
cyl13     O2  IDENTICAL rc ORIG=1 MINE=1  | 128 rows, 1 failures
cyl13     O0  IDENTICAL rc ORIG=1 MINE=1  | 128 rows, 1 failures
srstbit   O2  IDENTICAL rc ORIG=1 MINE=1  | 128 rows, 11 failures
srstbit   O0  IDENTICAL rc ORIG=1 MINE=1  | 128 rows, 11 failures
drqring   O2  IDENTICAL rc ORIG=1 MINE=1  | 128 rows, 2 failures
drqring   O0  IDENTICAL rc ORIG=1 MINE=1  | 128 rows, 2 failures
w57hi     O2  IDENTICAL rc ORIG=1 MINE=1  | 128 rows, 4 failures
w57hi     O0  IDENTICAL rc ORIG=1 MINE=1  | 128 rows, 4 failures
```

(b) controls, escapes and the new shapes -- variant, device variant, exit code, trailer, PASS-token count (and, for the
moves, the call-count line).  `rc=1` / `0 PASS` is red.  Device variants: `drqring` (two `chk()` rows fail), `w57hi`
(four `row_cmp()` rows fail), `srstbit` (eleven inline rows fail), `selfmut` (the self-mutant lane's device mutant: the
geometry row fails).

```
MINE_chkstub    pristine  rc=1 | 128 rows, 2 failures | 0 PASS
MINE_rowstub    pristine  rc=1 | 128 rows, 2 failures | 0 PASS
MINE_nosc       pristine  rc=0 | 128 rows, 0 failures | 1 PASS
MINE_scnoforce  pristine  rc=0 | 128 rows, 0 failures | 1 PASS
MINE_scnoforce_chkstub pristine  rc=1 | 128 rows, 1 failures | 0 PASS
MINE_scnoforce_chkstub drqring   rc=1 | 128 rows, 1 failures | 0 PASS
MINE_scnoforce_rowstub pristine  rc=1 | 128 rows, 1 failures | 0 PASS
MINE_drop60     pristine  rc=1 | 128 rows, 2 failures | 0 PASS
MINE_drop60     w57hi     rc=1 | 128 rows, 6 failures | 0 PASS
MINE_andgot     pristine  rc=1 | 128 rows, 2 failures | 0 PASS
MINE_andgot     drqring   rc=1 | 128 rows, 2 failures | 0 PASS
MINE_drop57     pristine  rc=1 | 128 rows, 2 failures | 0 PASS
MINE_drop57     w57hi     rc=1 | 128 rows, 2 failures | 0 PASS
MINE_rows       pristine  rc=0 | 128 rows, 0 failures | 1 PASS
MINE_rows       srstbit   rc=1 | 128 rows, 11 failures | 0 PASS
MINE_u16        pristine  rc=1 | 128 rows, 2 failures | 0 PASS
MINE_sect4      pristine  rc=1 | 128 rows, 2 failures | 0 PASS
MINE_wrap       pristine  rc=0 | 128 rows, 0 failures | 1 PASS
MINE_wrap       w57hi     rc=0 | 128 rows, 0 failures | 1 PASS
MINE_want165    pristine  rc=0 | 128 rows, 0 failures | 1 PASS
MINE_postinc    pristine  rc=0 | 128 rows, 0 failures | 1 PASS
MINE_postinc    drqring   rc=0 | 128 rows, 0 failures | 1 PASS
MINE_name       pristine  rc=0 | 128 rows, 0 failures | 1 PASS
MINE_name       drqring   rc=0 | 128 rows, 0 failures | 1 PASS
MINE_lt         pristine  rc=1 | 128 rows, 2 failures | 0 PASS
MINE_lt         w57hi     rc=1 | 128 rows, 6 failures | 0 PASS
MINE_andsect    pristine  rc=1 | 128 rows, 2 failures | 0 PASS
MINE_reset      pristine  rc=0 | 128 rows, 0 failures | 1 PASS
MINE_reset      drqring   rc=1 | 128 rows, 2 failures | 0 PASS
MINE_reset      w57hi     rc=1 | 128 rows, 4 failures | 0 PASS
MINE_reset2     pristine  rc=0 | 128 rows, 0 failures | 1 PASS
MINE_reset2     drqring   rc=0 | 128 rows, 0 failures | 1 PASS
MINE_reset2     w57hi     rc=0 | 128 rows, 0 failures | 1 PASS
MINE_reset2     selfmut   rc=1 | 128 rows, 1 failures | 0 PASS
MINE_recon2     drqring   rc=1 | 128 rows, 0 failures | 0 PASS
MINE_recon2     w57hi     rc=1 | 128 rows, 0 failures | 0 PASS
MINE_subafter   drqring   rc=1 | 128 rows, 0 failures | 0 PASS
MINE_subafter   w57hi     rc=1 | 128 rows, 0 failures | 0 PASS
MINE_incdel_reset drqring   rc=1 | 128 rows, 1 failures | 0 PASS
MINE_move_repin pristine  rc=1 | 104 rows, 1 failures | 0 PASS | FAIL  SELFCHECK(last): chk() ran 0 times and row_cmp() 8 before this run; want 24 and 8
MINE_move_repin drqring   rc=1 | 104 rows, 1 failures | 0 PASS | FAIL  SELFCHECK(last): chk() ran 0 times and row_cmp() 8 before this run; want 24 and 8
MINE_move_repin w57hi     rc=1 | 104 rows, 5 failures | 0 PASS | FAIL  SELFCHECK(last): chk() ran 0 times and row_cmp() 8 before this run; want 24 and 8
MINE_move_repin selfmut   rc=1 | 104 rows, 2 failures | 0 PASS | FAIL  SELFCHECK(last): chk() ran 0 times and row_cmp() 8 before this run; want 24 and 8
MINE_nopin      pristine  rc=0 | 128 rows, 0 failures | 1 PASS | (no call-count FAIL line)
MINE_nopin      drqring   rc=1 | 128 rows, 2 failures | 0 PASS | (no call-count FAIL line)
MINE_nopin_move_repin pristine  rc=0 | 104 rows, 0 failures | 1 PASS | (no call-count FAIL line)
MINE_nopin_move_repin drqring   rc=1 | 104 rows, 0 failures | 1 PASS | (no call-count FAIL line)
MINE_nopin_move_repin selfmut   rc=1 | 104 rows, 1 failures | 0 PASS | (no call-count FAIL line)
MINE_condreset  pristine  rc=0 | 128 rows, 0 failures | 1 PASS
MINE_condreset  drqring   rc=0 | 128 rows, 0 failures | 1 PASS
MINE_condreset  w57hi     rc=0 | 128 rows, 0 failures | 1 PASS
MINE_condreset  selfmut   rc=1 | 128 rows, 1 failures | 0 PASS
MINE_phase      pristine  rc=0 | 128 rows, 0 failures | 1 PASS
MINE_phase      drqring   rc=0 | 128 rows, 0 failures | 1 PASS
ORIG            drqring   rc=1 | 128 rows, 2 failures | 0 PASS
ORIG            w57hi     rc=1 | 128 rows, 4 failures | 0 PASS
ORIG            srstbit   rc=1 | 128 rows, 11 failures | 0 PASS
```

The new rows: `move_repin` is the Opus seat's positional composite (`row_ring_occupancy_sound();` moved after the
PASS/FAIL printf, the identity row re-pinned 128 -> 104); `nopin` deletes the call-count pin; `nopin_move_repin` is the
composite against a file without the pin (the control); `condreset` is the disclosed class (3)'s conditional form,
`if (failures == cmp_fails) failures = cmp_fails = 0;` placed before the reconciliation.

## 5. THE DIFF, #551d -> #551e

```diff
--- regress/diff_wdc_identify.c.551d
+++ regress/diff_wdc_identify.c.551e
@@ -5647,25 +5647,42 @@
 /*
  *  @@SELFCHECK@@ -- #551.  CAN THIS FILE'S COMPARATORS STILL FAIL?  Feeds chk() and row_cmp() known answers --
  *  each operand zero and past 32 bits, each of row_cmp()'s two disjuncts alone with got both below and
- *  above its want, and one pair that must NOT fail -- and requires the EXACT change in `failures' and in
- *  cmp_fails for each, restoring `rows', `failures' and cmp_fails after every probe.  Run FIRST (before
- *  any row) and LAST (after every row, before the identity row), so a comparator
- *  that goes inert partway through is caught at one end or the other.  Only the success arm prints gate 2's G
+ *  above its want, and one probe per comparator that must NOT fail -- and requires the EXACT change in
+ *  `failures' and in cmp_fails for each, restoring `rows', `failures' and cmp_fails after every probe.
+ *  Run FIRST (before any row) and LAST (after every row, before the identity row), so a comparator that
+ *  goes inert partway through is caught at one end or the other; the LAST run also requires every
+ *  covered call to have run before it (chk() 24, row_cmp() 8).  Only the success arm prints gate 2's G
  *  text; the failure arm does not, and forces one failure.
  *
  *  WHAT IT COVERS: the rows that go through chk() and row_cmp() -- the last run prints how many calls
  *  each comparator took.  Of chk()'s calls, the ones in row_ring_occupancy_sound() that pass a
  *  `cond ? 1 : 0' (or `? 0 : 1') hand it a VERDICT computed at the call, not a comparison, and every
  *  other row in this file compares inline: neither is covered by this block.  "Covered" means the
- *  COMPARATOR is live, not that a row is.  NOT CAUGHT, DISCLOSED: the self-check proves only that the
- *  comparators answer right on ITS OWN calls, so an edit that keeps those answers and changes the rest
- *  CAN keep every gate-2 row green -- a test keyed on a value, a name, a position or the self-check's
- *  own phase that the probes do not share, or an edit of the code that FEEDS the comparators (row()
- *  handing row_cmp() its own want), each measured on #551's passes; or an edit of this block itself
- *  (reasoned: the block edits measured so far are caught).  Reviewed in the differential, not chased.
- *  A reset of `failures' alone is not among them, wherever it sits: the comparators also count
- *  cmp_fails, which only they increment, and the verdict and the exit status read it directly.  A reset
- *  of BOTH tallies is, and is disclosed.  No line this block prints carries the self-mutant row's
+ *  COMPARATOR is live, not that a row is.
+ *
+ *  NOT CAUGHT, DISCLOSED.  This block pins the two COMPARATORS and nothing else: it proves they answer
+ *  right on ITS OWN calls, so an edit that keeps those answers and changes the rest CAN keep every gate-2
+ *  row green.  Four classes, each measured on #551's passes: (1) inside a comparator, a test keyed on a
+ *  value, a name, a position or this block's own phase that the probes do not share, or a predicate
+ *  rewritten to agree with the original on every probe and differ elsewhere (the sum of the two gots
+ *  against twice the want, say -- one member of a class no finite probe set closes); (2) the code that
+ *  FEEDS a comparator (row() handing row_cmp() its own want); (3) THE TRAILER, one call site: the printed
+ *  count, the PASS token and the exit status are produced there, and any rewrite that keeps them
+ *  consistent with each other is green -- today two coordinated edits, each red alone (the verdict's
+ *  cmp_fails term dropped with `failures -= cmp_fails' after the reconciliation; the verdict and the
+ *  printed count both scoring `failures - cmp_fails'); a reset of BOTH tallies is in this class --
+ *  unconditional, only after the covered rows and before the self-mutant's row; conditional on their
+ *  equality, anywhere.  No in-file probe can pin a single call site; the close is gate-side, a lane
+ *  whose device mutant fails the FIRST covered row (filed: `wdcidlane'); (4) this block itself (a probe's
+ *  cmp_fails check weakened together with the increment it guards and a reset).  A reset of `failures'
+ *  alone is not among them, wherever it sits: the comparators also count cmp_fails, which only they
+ *  increment, and the verdict and the exit status read it directly.  Nor is moving the covered rows past
+ *  the verdict: the LAST run requires chk() 24 and row_cmp() 8 calls.  On #551d's pass no single edit
+ *  outside these four classes kept gate 2 green (24 measured:
+ *  regress/artifacts/wdcidselfcheck_20260925/opus551_measured_d/analyze6.out).  Reviewed in the
+ *  differential, not chased.
+ *
+ *  No line this block prints carries the self-mutant row's
  *  text or "high byte" (gate 2 counts both).  Gate 2's G text is printed ONCE, by the last run, only
  *  when both runs passed -- and the run's own PASS needs that line (sc_g), so a self-check that failed
  *  fails the run even if its forced failure is gone.  The rest of the file is filed as
@@ -5708,6 +5725,17 @@
 			printf("  ok    SELFCHECK(first): all %d probes answered right\n", n);
 		return;
 	}
+	/*  #551e: the LAST run also requires every covered call to have run BEFORE it -- chk() 24 and row_cmp() 8,
+	    the counts the note line below prints.  Covered rows moved past the verdict, with the identity row
+	    re-pinned, would otherwise print their FAILs after the PASS token.  Change these with the rows, as the
+	    identity row's 128.  */
+	if (chk_calls != 24 || rowcmp_calls != 8) {
+		printf("  FAIL  SELFCHECK(last): chk() ran %d times and row_cmp() %d before this run; want 24 and 8\n",
+		    chk_calls, rowcmp_calls);
+		if (!sc_bad)
+			failures = sc_f + 1;
+		sc_bad++;
+	}
 	if (!sc_bad && sc_first_bad == 0) {
 		sc_g = 1;
 		printf("  ok    SELFCHECK the comparator can still fail (first and last)\n");
@@ -5821,8 +5849,9 @@
 		printf("  ok   %-38s %i\n", "[IDENTITY] row count", rows);
 	}
 
-	/*  #551: the comparators' own count survives a reset of `failures' (which always counts at least as
-	    many, untouched), and a self-check that did not pass is a failure the count shows.  */
+	/*  #551: the PRINTED count shows the comparators' failures even after a reset of `failures' placed
+	    before this line (untouched, `failures' always counts at least as many); the verdict and the exit
+	    status read cmp_fails directly.  A self-check that did not pass is a failure the count shows.  */
 	if (cmp_fails > failures)
 		failures = cmp_fails;
 	if (!sc_g && failures == 0)
```

```diff
--- regress/gate_offline.sh.551d
+++ regress/gate_offline.sh.551e
@@ -2261,16 +2261,19 @@
 #                   verdict computed at the call (derive: grep -cE '\? [01] : [01], 1\);'
 #                   regress/diff_wdc_identify.c), and the other
 #                   96 compare inline -- NOT covered.  "Covered" means the COMPARATOR is live,
-#                   not that a row is: the self-check proves only its own calls, so an edit that
-#                   keeps those right CAN keep gate 2 green -- a test keyed on a value, a name,
-#                   a position or the self-check's phase that the probes do not share, or
-#                   feeding a comparator its own want (measured on #551's passes), or an edit of
-#                   the self-check itself (reasoned); disclosed, not chased.  A reset of
-#                   `failures' alone is not, wherever it sits: the comparators keep their own
-#                   count, which the verdict reads directly; a reset of both tallies is, and is
-#                   disclosed.  The file prints its comparator call counts on every run, and its
-#                   PASS needs the G line.  #551, by owner ruling 2026-09-25 ("24/128 now, file
-#                   the rest"); the rest is `wdcidcomparators'.
+#                   not that a row is: the self-check pins chk() and row_cmp() and nothing else.
+#                   What it does not see, disclosed and not chased (measured on #551's passes):
+#                   a keyed or probe-agreeing test inside a comparator; feeding a comparator its
+#                   own want; the TRAILER (one call site -- two coordinated edits keep the count
+#                   and the token consistent; a both-tally reset, conditional, or placed before
+#                   the self-mutant's row); and an edit of the self-check itself.  No single edit
+#                   outside those classes kept gate 2 green (24 measured, #551d).  A reset of
+#                   `failures' alone is caught wherever it sits; so is moving the covered rows
+#                   past the verdict (the last run pins chk() 24 and row_cmp() 8).  The gate-side
+#                   close for the trailer is a covered-row lane, filed as `wdcidlane'.  The file
+#                   prints its comparator call counts on every run, and its PASS needs the G
+#                   line.  #551, by owner ruling 2026-09-25 ("24/128 now, file the rest"); the
+#                   rest is `wdcidcomparators'.
 #  rtc_range is in the UNIFORM group: every row goes through chk(), its single comparator.
 #  Named here rather than left to be re-derived, because the exception list above
 #  is only trustworthy if additions are classified as they arrive.
```

## 6. QUESTIONS

1. **Verify the enumeration.**  Is there a SINGLE edit, outside the four classes the contract names, that keeps every
   gate-2 check green while a row going through `chk()` or `row_cmp()` can no longer fail?  Or a class of green edits
   the contract does not name?  Either reopens the chain; a composite INSIDE a named class does not.  **A zero needs
   its denominator** -- the shapes you tried.
2. **The adjudication's caution, asked exactly:** can an in-file pin on `main()`'s trailer survive ONE inlining edit and
   ONE inserted conditional reset (`if (failures == cmp_fails) failures = cmp_fails = 0;`)?  If yes, show it: the
   trailer class is then closable in-file and the contract's class (3) is wrong.
3. **The call-count pin:** does it catch every way of running a covered row after the verdict?  Is there a way to move
   covered rows past the verdict that keeps chk() at 24 and row_cmp() at 8 by the last self-check?  Does it change any
   healthy run's output beyond SELFCHECK lines?
4. **Is any sentence of the new contract false** -- the four classes, "each measured on #551's passes", the placement
   sentence for the both-tally reset, "No in-file probe can pin a single call site", the gate-2 bullet?
5. **What did all of us miss?**

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
