# #551f -- THE PARTITION-VERIFYING PASS: the test harness's comparator self-check, with covered failures reporting themselves (measured)

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.  *(My last brief said gate 2 pins
"sixteen named rows"; it pins 69, and two seats caught it.)*

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** (here `regress/`).  Three pristine-2021-upstream copies of GXemul sit
under the project root; they are NOT this fork.  **The working tree's `regress/diff_wdc_identify.c` is #551's FIRST
version**; #551f exists only as the generated file and the diff inlined below.  Review the INLINED code.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any premise you cannot settle
from this packet rather than guessing at it.

**VERDICT LINE FIRST:** `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.

## 1. WHAT THIS IS, AND WHY THIS PASS IS DIFFERENT

`regress/diff_wdc_identify.c` is an offline differential test (128 rows) of the emulator's IDE IDENTIFY data.  #551
gives it a SELF-CHECK on its two comparators, `chk()` and `row_cmp()`.  Each pass since #551b has found a way for an
adversary with full control of the file to keep gate 2 green while a covered row stopped failing; #551e's pass found
that the call-count pin checks two WRITABLE counters (a one-statement `atexit` deferral that bumps them was measured
green), and that the trailer is not the only thing gate 2 reads.

**The adjudication of #551e's pass (the Fable 5.1 seat, `pass551e/fable5_pass551e.md`) -- its sentences, CONDENSED
where `...` marks a cut:**

> [#551f's] contract is a partition of where an in-file edit can act (comparator / its inputs / rows not run and their
> observables forged / the block) ... My premise -- everything gate 2 reads is produced at one call site -- is measured
> false: the count check reads the whole log, so a comparator can report to gate 2 at the moment it fails ...
>
> **Stop condition for #551f's pass -- verify the partition, do not hunt.**  It closes when: (1) the diff is delivered
> and the roster is complete or its misses named; (2) everything the contract says is caught is MEASURED red -- trailer
> rewrites single and paired; resets of either or both tallies, conditional and unconditional, at the start, mid,
> trailer and after the printf; `countforge`, `movefake`, the dummy-call move, the `atexit` deferral; and healthy runs
> whole-log identical on pristine, selfmut, cyl13, srstbit; (3) every green shape found lies inside A-D as worded.  A
> green shape inside A-D that the wording does not obviously cover is L4, fixed in-round, no new pass.  What reopens: a
> green shape the contract says is caught (a defect in the mechanism, L2, one pass), or a green single edit outside A-D
> -- which the partition says cannot exist, since any edit is inside a comparator, at its inputs, around it, or in the
> block ...

**What #551f changes (inlined in section 3; the diff in section 5):**
* **(B) a covered failure reports itself**: on a covered (non-probe) mismatch each comparator prints `  FAIL  covered
  comparator failure -- N failures so far`.  Gate 2's failure-count check is `grep -oE '[0-9]+ failures' "$WDCLOG" |
  grep -oE '^[0-9]+'` compared, as ONE STRING, to `0` -- so every such line anywhere in the log, before or after the
  trailer, turns it red.  (The Opus 5.5 measuring seat found and measured this mechanism on #551e's pass.)
* the call-count pin kept, its comment rewritten as a second identity constant (forgeable -- contract (C));
* the contract rewritten as the four-part partition (A)-(D), in the adjudication's words;
* two imprecise opening sentences fixed.

## 2. SETTLED PREMISES (re-inlined; each verified against the generated #551f file, md5 7fd15d1d)

* **Who writes the tallies.**  `failures` and `rows` are file-scope ints; `cmp_fails` is incremented ONLY in the two
  comparators' failure arms, each beside `failures ++`; `selfcheck()` assigns it back (restores).  The 96 inline rows,
  the identity row and the self-check's forced failure write `failures` alone.
* **main()'s order**: `selfcheck("first");` -> eight `row(...)` calls (each into `row_cmp()`) -> 59 zero-argument
  `row_*()` calls, among them `row_ring_occupancy_sound();` (all 24 `chk()` calls) and, later, `row_wide_geometry();`
  (an INLINE row; the self-mutant lane's row) -> `selfcheck("last");` -> the identity row (`rows != 128`) -> the trailer.
* **Coverage**: 16 of `chk()`'s 24 calls and all 8 of `row_cmp()`'s compare inside the comparator (24 covered); 8 hand
  `chk()` a 0/1 verdict computed at the call (`grep -cE '\? [01] : [01], 1\);' regress/diff_wdc_identify.c` = 8); 96
  rows compare inline.  With (B), all 32 comparator calls REPORT a failure.
* **Gate 2's checks on this log** (`gate_offline.sh`; derive with the awk block the measurement script uses): the
  failure-count string must equal `0`; rows at least 42 (`check_min`); `WDC_IDENTIFY_PASS` exactly once; **69 named
  rows** present exactly once each (`grep -c` / `grep -cF`, whole log, order-blind); `high byte` once; the G text; the
  `@@SELFCHECK@@` token in the source; and the self-mutant lane (on its device mutant: a FAIL token and a FAIL line
  naming the geometry row).  **Gate 2 discards the exit status.**
* **The measurement's device variants** (the Opus seat's, reused): `dropold` (a drop-oldest ring: three COVERED
  `chk()` comparisons fail), `drqring` (the DRQ status bit dropped: two VERDICT-HANDED `chk()` rows fail), `w57hi`
  (word 57's high byte zeroed: four `row_cmp()` rows fail), each also with the self-mutant applied (`_sm`) for the lane;
  and `selfmut`, `cyl13`, `srstbit`, `rev255`, `w58lo`.

## 3. THE CODE UNDER REVIEW (the generated #551f file, md5 7fd15d1d)

### 3a. The two comparators, each with its (B) report

```c
static void row_cmp(const char *why, uint64_t sectors, uint64_t got57, uint64_t got60)
{
	rowcmp_calls ++;
	rows ++;

	if (got57 != sectors || got60 != sectors) {
		printf("  FAIL %-38s sectors=%llu -> 57/58=%llu 60/61=%llu\n",
		    why, (unsigned long long)sectors,
		    (unsigned long long)got57, (unsigned long long)got60);
		failures ++;
		cmp_fails ++;
		if (why[0] != '@')	/*  #551f: contract (B) -- a covered failure reports itself  */
			printf("  FAIL  covered comparator failure -- %d failures so far\n", cmp_fails);
	} else {
		printf("  ok   %-38s %llu\n", why, (unsigned long long)sectors);
	}
}

static void chk(const char *name, long long got, long long want)
{
	chk_calls ++;
	rows ++;
	if (got != want) {
		failures ++;
		cmp_fails ++;
		printf("  FAIL %-40s got %lld want %lld\n", name, got, want);
		if (name[0] != '@')	/*  #551f: contract (B) -- a covered failure reports itself  */
			printf("  FAIL  covered comparator failure -- %d failures so far\n", cmp_fails);
	} else
		printf("  ok   %-40s %lld\n", name, got);
}
```

### 3b. The block comment -- the contract, as the partition (A)-(D)

```c
/*
 *  @@SELFCHECK@@ -- #551.  CAN THIS FILE'S COMPARATORS STILL FAIL?  Feeds chk() and row_cmp() known answers --
 *  each operand zero and past 32 bits, each of row_cmp()'s two disjuncts alone with got both below and
 *  above its want, and one probe per comparator that must NOT fail -- and requires the EXACT change in
 *  `failures' and in cmp_fails for each, restoring `rows', `failures' and cmp_fails after every probe.
 *  Run FIRST (before any row) and LAST (after every row, before the identity row), so a comparator that
 *  goes inert partway through is caught at one end or the other; the LAST run also requires the
 *  comparator call counts (chk() 24, row_cmp() 8).  Only the success arm prints gate 2's G text; see (D)
 *  for what the failure arms do.
 *
 *  WHAT IT COVERS: the rows that go through chk() and row_cmp() -- the last run prints how many calls
 *  each comparator took.  Of chk()'s calls, the ones in row_ring_occupancy_sound() that pass a
 *  `cond ? 1 : 0' (or `? 0 : 1') hand it a VERDICT computed at the call, not a comparison, and every
 *  other row in this file compares inline: neither is covered by this block.  "Covered" means the
 *  COMPARATOR is live, not that a row is.  The 8 verdict-handed calls still REPORT through (B): the file
 *  covers 24 comparisons and reports all 32 comparator failures.
 *
 *  WHAT THIS FILE'S CHECKS CAN AND CANNOT SEE.  Every check here reads state this file writes (the
 *  tallies, the call counts, `rows', sc_g) or output this file prints, so an edit that reproduces a healthy
 *  run's observables is invisible to all of them.  That boundary is a fact about in-file checks, not a gap
 *  in this block, and only a gate-side run on a device that fails a COVERED row sees across it (filed:
 *  `wdcidlane', on the FIRST covered row).  Inside the boundary:
 *
 *  (A) THE COMPARATORS ARE PINNED -- the probes require the exact change in `failures' and cmp_fails on
 *  their own calls, so an inert or narrowed comparator is caught at one end of the run or the other.  Not
 *  caught, measured: a test inside a comparator keyed on a value, a name, a position or this block's phase
 *  that the probes do not share; a predicate rewritten to agree with the original on every probe and differ
 *  elsewhere (the sum of the two gots against twice the want, say); and the code that FEEDS a comparator
 *  (row() handing row_cmp() its own want).
 *
 *  (B) A COVERED FAILURE REPORTS ITSELF -- on a non-probe mismatch each comparator prints a line gate 2's
 *  failure-count check reads (`N failures so far'), at the moment it fails; that check compares every such
 *  line in the log against "0", so a printed line cannot be taken back and no line can be added.  Hence no
 *  edit that leaves the covered rows running and the comparators intact hides a covered failure: not the
 *  trailer's count, token or exit rewritten singly or together, not a reset of either tally or both at any
 *  placement, not rows moved or deferred past the verdict with their counts forged (measured: #551f's
 *  pass, regress/artifacts/wdcidselfcheck_20260925/measured/run551f.out).  Not caught: that report switched off for
 *  non-probe calls -- its guard is itself a probe/real key -- together with an edit that hides the tallies.
 *
 *  (C) A ROW THAT DOES NOT RUN CANNOT REPORT -- the identity row's 128 and the LAST run's call counts
 *  (chk() 24, row_cmp() 8) raise the cost of skipping covered rows, and both are values this file can
 *  forge: skipping the ring rows while printing their gate-pinned labels and adding 24 to `rows' and
 *  chk_calls is one insertion and green here.  That is the boundary's own class; its close is `wdcidlane'.
 *
 *  (D) This block itself.  Nothing this block prints carries the self-mutant row's text, "high byte" or a
 *  pinned label.  Gate 2's G text is printed ONCE, by the last run, only when both runs passed; the run's
 *  PASS needs that line (sc_g) and both tallies at zero; a probe failure forces one failure, and a missing
 *  first run is counted by the trailer's `!sc_g' line.  Reviewed in the differential, not chased.  The rest
 *  of the file is filed as `wdcidcomparators' (#551; owner ruling 2026-09-25).
 */
```

### 3c. The self-check, with the call-count pin

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
	/*  #551e: a second identity constant -- the LAST run requires the comparator call counts the note line
	    below prints, chk() 24 and row_cmp() 8.  It catches covered rows skipped or moved without their counts
	    forged; like the identity row's 128 it is forgeable by an edit that writes the counter (contract (C)).
	    Change these with the rows.  */
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

### 3d. The identity row and the trailer

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

## 4. MEASURED -- `regress/artifacts/wdcidselfcheck_20260925/measured/run551f.out` (verbatim)

Every shape is one text transformation of the #551f file per edit (`pass551f/meas551f.py.txt`), built against Opus's
device variants and scored by `pass551f/analyze8.py.txt`: gate 2's wdc block extracted verbatim from
`gate_offline.sh`, H, G, the one PASS token, and the self-mutant lane on the matching `_sm` device.  A cell is
`GREEN`/`red`, then (rows / printed failures, token, `rN` = N covered-failure report lines).  **The exit status is
recorded but is not a gate-2 input.**  A shape ESCAPES on a device when the unedited #551f file reds it, the shape keeps
gate 2 green there, and the pristine device is green too.

```
=== (1) #551f and 40 shapes x the real device + 3 covered-only defects, with the lane ===
    cell = gate-2 GREEN/red (rows/printed-failures token, rN = N covered-failure report lines)
    shape                    pristine                   dropold (chk cmp)          drqring (chk 0/1)          w57hi (row_cmp)            class   escapes on
    F                        GREEN(128/0 PASS)          red(128/3 FAIL r3)         red(128/2 FAIL r2)         red(128/4 FAIL r4)         -       -
    F_atexit_defer           GREEN(128/0 PASS)          red(128/0 PASS r3)         red(128/0 PASS r2)         red(128/4 FAIL r4)         caught  -
    F_both_afterprintf       red(128/0 PASS)            red(128/3 PASS r3)         red(128/2 PASS r2)         red(128/4 PASS r4)         caught  -
    F_both_trailer           red(128/0 PASS)            red(128/0 PASS r3)         red(128/0 PASS r2)         red(128/0 PASS r4)         caught  -
    F_cond_afterprintf       GREEN(128/0 PASS)          red(128/3 PASS r3)         red(128/2 PASS r2)         red(128/4 PASS r4)         caught  -
    F_cond_mid               GREEN(128/0 PASS)          red(128/0 PASS r3)         red(128/0 PASS r2)         red(128/0 PASS r4)         caught  -
    F_cond_start             GREEN(128/0 PASS)          red(128/3 FAIL r3)         red(128/2 FAIL r2)         red(128/4 FAIL r4)         caught  -
    F_cond_trailer           GREEN(128/0 PASS)          red(128/0 PASS r3)         red(128/0 PASS r2)         red(128/0 PASS r4)         caught  -
    F_countforge             GREEN(104/0 PASS)          red(104/0 PASS r3)         red(104/0 PASS r2)         red(104/4 FAIL r4)         caught  -
    F_delring_repin          red(104/1 FAIL)            red(104/1 FAIL)            red(104/1 FAIL)            red(104/5 FAIL r4)         caught  -
    F_delrow_repin           red(127/1 FAIL)            red(127/4 FAIL r3)         red(127/2 FAIL r1)         red(127/5 FAIL r4)         caught  -
    F_emitoff                GREEN(128/0 PASS)          red(128/3 FAIL)            red(128/2 FAIL)            red(128/4 FAIL)            caught  -
    F_emitoff_cond_trailer   GREEN(128/0 PASS)          GREEN(128/0 PASS)          GREEN(128/0 PASS)          GREEN(128/0 PASS)          (B)     dropold,drqring,w57hi
    F_forge_move             GREEN(128/0 PASS)          red(128/0 PASS r3)         red(128/0 PASS r2)         red(128/4 FAIL r4)         caught  -
    F_hardcode               GREEN(128/0 PASS)          red(128/0 PASS r3)         red(128/0 PASS r2)         red(128/0 PASS r4)         caught  -
    F_move_repin             red(104/1 FAIL)            red(104/1 FAIL r3)         red(104/1 FAIL r2)         red(104/5 FAIL r4)         caught  -
    F_movefake               GREEN(128/0 PASS)          red(128/0 PASS r3)         red(128/0 PASS r2)         red(128/4 FAIL r4)         caught  -
    F_movefake_row           GREEN(128/0 PASS)          red(128/3 FAIL r3)         red(128/2 FAIL r2)         red(128/0 PASS r4)         caught  -
    F_name                   GREEN(128/0 PASS)          GREEN(128/0 PASS)          GREEN(128/0 PASS)          red(128/4 FAIL r4)         (A)     dropold,drqring
    F_nopin                  GREEN(128/0 PASS)          red(128/3 FAIL r3)         red(128/2 FAIL r2)         red(128/4 FAIL r4)         caught  -
    F_nopin_delring_repin    red(104/0 PASS)            red(104/0 PASS)            red(104/0 PASS)            red(104/4 FAIL r4)         (C)     -
    F_nopin_delrow_repin     GREEN(127/0 PASS)          red(127/3 FAIL r3)         red(127/1 FAIL r1)         red(127/4 FAIL r4)         (C)     -
    F_nopin_move_repin       GREEN(104/0 PASS)          red(104/0 PASS r3)         red(104/0 PASS r2)         red(104/4 FAIL r4)         caught  -
    F_phase                  GREEN(128/0 PASS)          GREEN(128/0 PASS)          GREEN(128/0 PASS)          red(128/4 FAIL r4)         (A)     dropold,drqring
    F_postinc                GREEN(128/0 PASS)          GREEN(128/0 PASS)          GREEN(128/0 PASS)          red(128/4 FAIL r4)         (A)     dropold,drqring
    F_printf_sub             GREEN(128/0 PASS)          red(128/0 FAIL r3)         red(128/0 FAIL r2)         red(128/0 FAIL r4)         caught  -
    F_recon_ge_sub           GREEN(128/0 PASS)          red(128/0 FAIL r3)         red(128/0 FAIL r2)         red(128/0 FAIL r4)         caught  -
    F_reset2_mid             GREEN(128/0 PASS)          red(128/0 PASS r3)         red(128/0 PASS r2)         red(128/0 PASS r4)         caught  -
    F_reset_mid              GREEN(128/0 PASS)          red(128/3 FAIL r3)         red(128/2 FAIL r2)         red(128/4 FAIL r4)         caught  -
    F_resetcmp_mid           GREEN(128/0 PASS)          red(128/3 FAIL r3)         red(128/2 FAIL r2)         red(128/4 FAIL r4)         caught  -
    F_ret_nocmp              GREEN(128/0 PASS)          red(128/3 FAIL r3)         red(128/2 FAIL r2)         red(128/4 FAIL r4)         caught  -
    F_scweak_nocmpinc_reset  GREEN(128/0 PASS)          red(128/0 PASS r3)         red(128/0 PASS r2)         red(128/4 FAIL r4)         (D)     -
    F_skipforge              GREEN(128/0 PASS)          GREEN(128/0 PASS)          GREEN(128/0 PASS)          red(128/4 FAIL r4)         (C)     dropold,drqring
    F_sub_after              GREEN(128/0 PASS)          red(128/0 FAIL r3)         red(128/0 FAIL r2)         red(128/0 FAIL r4)         caught  -
    F_sum                    GREEN(128/0 PASS)          red(128/3 FAIL r3)         red(128/2 FAIL r2)         red(128/4 FAIL r4)         (A)     -
    F_v_eq                   GREEN(128/0 PASS)          red(128/3 PASS r3)         red(128/2 PASS r2)         red(128/4 PASS r4)         caught  -
    F_v_eq_printf_sub        GREEN(128/0 PASS)          red(128/0 PASS r3)         red(128/0 PASS r2)         red(128/0 PASS r4)         caught  -
    F_v_nocmp                GREEN(128/0 PASS)          red(128/3 FAIL r3)         red(128/2 FAIL r2)         red(128/4 FAIL r4)         caught  -
    F_v_nocmp_sub_after      GREEN(128/0 PASS)          red(128/0 PASS r3)         red(128/0 PASS r2)         red(128/0 PASS r4)         caught  -
    F_want165                GREEN(128/0 PASS)          GREEN(128/0 PASS)          red(128/2 FAIL r2)         red(128/4 FAIL r4)         (A)     dropold
    F_wrap                   GREEN(128/0 PASS)          red(128/3 FAIL r3)         red(128/2 FAIL r2)         GREEN(128/0 PASS)          (A)     w57hi
  CONTRACT CHECK: every CAUGHT shape is red on every covered-only defect
  shapes GREEN on at least one covered-only defect: F_emitoff_cond_trailer F_name F_phase F_postinc F_skipforge F_want165 F_wrap
  ...of which the manifest does NOT class inside A-D: NONE
  the pin's delta (one unpinned covered row deleted, identity re-pinned 127): with the pin red(127/1 FAIL); without it GREEN(127/0 PASS)

=== (2) #551f against #551e and against HEAD, WHOLE log ===
    cyl13       F vs E: WHOLE-LOG IDENTICAL                          | F vs HEAD without SELFCHECK and report lines: IDENTICAL | rc F=1 E=1 HEAD=1
    dropold     F vs E: +3 lines, all report lines: True             | F vs HEAD without SELFCHECK and report lines: IDENTICAL | rc F=1 E=1 HEAD=1
    dropold_sm  F vs E: +3 lines, all report lines: True             | F vs HEAD without SELFCHECK and report lines: IDENTICAL | rc F=1 E=1 HEAD=1
    drqring     F vs E: +2 lines, all report lines: True             | F vs HEAD without SELFCHECK and report lines: IDENTICAL | rc F=1 E=1 HEAD=1
    drqring_sm  F vs E: +2 lines, all report lines: True             | F vs HEAD without SELFCHECK and report lines: IDENTICAL | rc F=1 E=1 HEAD=1
    pristine    F vs E: WHOLE-LOG IDENTICAL                          | F vs HEAD without SELFCHECK and report lines: IDENTICAL | rc F=0 E=0 HEAD=0
    rev255      F vs E: +6 lines, all report lines: True             | F vs HEAD without SELFCHECK and report lines: IDENTICAL | rc F=1 E=1 HEAD=1
    selfmut     F vs E: WHOLE-LOG IDENTICAL                          | F vs HEAD without SELFCHECK and report lines: IDENTICAL | rc F=1 E=1 HEAD=1
    srstbit     F vs E: WHOLE-LOG IDENTICAL                          | F vs HEAD without SELFCHECK and report lines: IDENTICAL | rc F=1 E=1 HEAD=1
    w57hi       F vs E: +4 lines, all report lines: True             | F vs HEAD without SELFCHECK and report lines: IDENTICAL | rc F=1 E=1 HEAD=1
    w57hi_sm    F vs E: +4 lines, all report lines: True             | F vs HEAD without SELFCHECK and report lines: IDENTICAL | rc F=1 E=1 HEAD=1
    w58lo       F vs E: +5 lines, all report lines: True             | F vs HEAD without SELFCHECK and report lines: IDENTICAL | rc F=1 E=1 HEAD=1
    w58lo_sm    F vs E: +5 lines, all report lines: True             | F vs HEAD without SELFCHECK and report lines: IDENTICAL | rc F=1 E=1 HEAD=1
ANALYZE8_DONE
```

**Reading it.**  `CONTRACT CHECK` compares each shape the contract says is CAUGHT (the manifest's `caught` column)
against the table: every one is red on every covered-only defect.  The green shapes are the (A) keys and feed
(`want165`, `postinc`, `name`, `phase`, `wrap`), the (B) residual (`emitoff_cond_trailer`: both reports switched off
plus a reset), and the (C) insertion (`skipforge`: the ring rows skipped, their 24 labels printed, 24 added to `rows`
and `chk_calls`).  `sum` is (A) and red here because no device variant is a compensating pair.  `scweak_nocmpinc_reset`
(D) is red: with `chk()`'s increment deleted its report prints "0 failures so far", and gate 2 compares the WHOLE
multi-line capture to "0".  The pin's delta: one unpinned covered row deleted and the identity re-pinned is red with the
pin and green without it.

## 5. THE DIFF, #551e -> #551f

```diff
--- regress/diff_wdc_identify.c.551e
+++ regress/diff_wdc_identify.c.551f
@@ -518,6 +518,8 @@
 		    (unsigned long long)got57, (unsigned long long)got60);
 		failures ++;
 		cmp_fails ++;
+		if (why[0] != '@')	/*  #551f: contract (B) -- a covered failure reports itself  */
+			printf("  FAIL  covered comparator failure -- %d failures so far\n", cmp_fails);
 	} else {
 		printf("  ok   %-38s %llu\n", why, (unsigned long long)sectors);
 	}
@@ -4869,6 +4871,8 @@
 		failures ++;
 		cmp_fails ++;
 		printf("  FAIL %-40s got %lld want %lld\n", name, got, want);
+		if (name[0] != '@')	/*  #551f: contract (B) -- a covered failure reports itself  */
+			printf("  FAIL  covered comparator failure -- %d failures so far\n", cmp_fails);
 	} else
 		printf("  ok   %-40s %lld\n", name, got);
 }
@@ -5650,43 +5654,49 @@
  *  above its want, and one probe per comparator that must NOT fail -- and requires the EXACT change in
  *  `failures' and in cmp_fails for each, restoring `rows', `failures' and cmp_fails after every probe.
  *  Run FIRST (before any row) and LAST (after every row, before the identity row), so a comparator that
- *  goes inert partway through is caught at one end or the other; the LAST run also requires every
- *  covered call to have run before it (chk() 24, row_cmp() 8).  Only the success arm prints gate 2's G
- *  text; the failure arm does not, and forces one failure.
+ *  goes inert partway through is caught at one end or the other; the LAST run also requires the
+ *  comparator call counts (chk() 24, row_cmp() 8).  Only the success arm prints gate 2's G text; see (D)
+ *  for what the failure arms do.
  *
  *  WHAT IT COVERS: the rows that go through chk() and row_cmp() -- the last run prints how many calls
  *  each comparator took.  Of chk()'s calls, the ones in row_ring_occupancy_sound() that pass a
  *  `cond ? 1 : 0' (or `? 0 : 1') hand it a VERDICT computed at the call, not a comparison, and every
  *  other row in this file compares inline: neither is covered by this block.  "Covered" means the
- *  COMPARATOR is live, not that a row is.
+ *  COMPARATOR is live, not that a row is.  The 8 verdict-handed calls still REPORT through (B): the file
+ *  covers 24 comparisons and reports all 32 comparator failures.
  *
- *  NOT CAUGHT, DISCLOSED.  This block pins the two COMPARATORS and nothing else: it proves they answer
- *  right on ITS OWN calls, so an edit that keeps those answers and changes the rest CAN keep every gate-2
- *  row green.  Four classes, each measured on #551's passes: (1) inside a comparator, a test keyed on a
- *  value, a name, a position or this block's own phase that the probes do not share, or a predicate
- *  rewritten to agree with the original on every probe and differ elsewhere (the sum of the two gots
- *  against twice the want, say -- one member of a class no finite probe set closes); (2) the code that
- *  FEEDS a comparator (row() handing row_cmp() its own want); (3) THE TRAILER, one call site: the printed
- *  count, the PASS token and the exit status are produced there, and any rewrite that keeps them
- *  consistent with each other is green -- today two coordinated edits, each red alone (the verdict's
- *  cmp_fails term dropped with `failures -= cmp_fails' after the reconciliation; the verdict and the
- *  printed count both scoring `failures - cmp_fails'); a reset of BOTH tallies is in this class --
- *  unconditional, only after the covered rows and before the self-mutant's row; conditional on their
- *  equality, anywhere.  No in-file probe can pin a single call site; the close is gate-side, a lane
- *  whose device mutant fails the FIRST covered row (filed: `wdcidlane'); (4) this block itself (a probe's
- *  cmp_fails check weakened together with the increment it guards and a reset).  A reset of `failures'
- *  alone is not among them, wherever it sits: the comparators also count cmp_fails, which only they
- *  increment, and the verdict and the exit status read it directly.  Nor is moving the covered rows past
- *  the verdict: the LAST run requires chk() 24 and row_cmp() 8 calls.  On #551d's pass no single edit
- *  outside these four classes kept gate 2 green (24 measured:
- *  regress/artifacts/wdcidselfcheck_20260925/opus551_measured_d/analyze6.out).  Reviewed in the
- *  differential, not chased.
- *
- *  No line this block prints carries the self-mutant row's
- *  text or "high byte" (gate 2 counts both).  Gate 2's G text is printed ONCE, by the last run, only
- *  when both runs passed -- and the run's own PASS needs that line (sc_g), so a self-check that failed
- *  fails the run even if its forced failure is gone.  The rest of the file is filed as
- *  `wdcidcomparators' (#551; owner ruling 2026-09-25).
+ *  WHAT THIS FILE'S CHECKS CAN AND CANNOT SEE.  Every check here reads state this file writes (the
+ *  tallies, the call counts, `rows', sc_g) or output this file prints, so an edit that reproduces a healthy
+ *  run's observables is invisible to all of them.  That boundary is a fact about in-file checks, not a gap
+ *  in this block, and only a gate-side run on a device that fails a COVERED row sees across it (filed:
+ *  `wdcidlane', on the FIRST covered row).  Inside the boundary:
+ *
+ *  (A) THE COMPARATORS ARE PINNED -- the probes require the exact change in `failures' and cmp_fails on
+ *  their own calls, so an inert or narrowed comparator is caught at one end of the run or the other.  Not
+ *  caught, measured: a test inside a comparator keyed on a value, a name, a position or this block's phase
+ *  that the probes do not share; a predicate rewritten to agree with the original on every probe and differ
+ *  elsewhere (the sum of the two gots against twice the want, say); and the code that FEEDS a comparator
+ *  (row() handing row_cmp() its own want).
+ *
+ *  (B) A COVERED FAILURE REPORTS ITSELF -- on a non-probe mismatch each comparator prints a line gate 2's
+ *  failure-count check reads (`N failures so far'), at the moment it fails; that check compares every such
+ *  line in the log against "0", so a printed line cannot be taken back and no line can be added.  Hence no
+ *  edit that leaves the covered rows running and the comparators intact hides a covered failure: not the
+ *  trailer's count, token or exit rewritten singly or together, not a reset of either tally or both at any
+ *  placement, not rows moved or deferred past the verdict with their counts forged (measured: #551f's
+ *  pass, regress/artifacts/wdcidselfcheck_20260925/measured/run551f.out).  Not caught: that report switched off for
+ *  non-probe calls -- its guard is itself a probe/real key -- together with an edit that hides the tallies.
+ *
+ *  (C) A ROW THAT DOES NOT RUN CANNOT REPORT -- the identity row's 128 and the LAST run's call counts
+ *  (chk() 24, row_cmp() 8) raise the cost of skipping covered rows, and both are values this file can
+ *  forge: skipping the ring rows while printing their gate-pinned labels and adding 24 to `rows' and
+ *  chk_calls is one insertion and green here.  That is the boundary's own class; its close is `wdcidlane'.
+ *
+ *  (D) This block itself.  Nothing this block prints carries the self-mutant row's text, "high byte" or a
+ *  pinned label.  Gate 2's G text is printed ONCE, by the last run, only when both runs passed; the run's
+ *  PASS needs that line (sc_g) and both tallies at zero; a probe failure forces one failure, and a missing
+ *  first run is counted by the trailer's `!sc_g' line.  Reviewed in the differential, not chased.  The rest
+ *  of the file is filed as `wdcidcomparators' (#551; owner ruling 2026-09-25).
  */
 static int sc_first_bad = -1;	/*  -1 until the FIRST run has happened  */
 static int sc_g;	/*  set ONLY where gate 2's G line prints: the run's PASS needs it  */
@@ -5725,10 +5735,10 @@
 			printf("  ok    SELFCHECK(first): all %d probes answered right\n", n);
 		return;
 	}
-	/*  #551e: the LAST run also requires every covered call to have run BEFORE it -- chk() 24 and row_cmp() 8,
-	    the counts the note line below prints.  Covered rows moved past the verdict, with the identity row
-	    re-pinned, would otherwise print their FAILs after the PASS token.  Change these with the rows, as the
-	    identity row's 128.  */
+	/*  #551e: a second identity constant -- the LAST run requires the comparator call counts the note line
+	    below prints, chk() 24 and row_cmp() 8.  It catches covered rows skipped or moved without their counts
+	    forged; like the identity row's 128 it is forgeable by an edit that writes the counter (contract (C)).
+	    Change these with the rows.  */
 	if (chk_calls != 24 || rowcmp_calls != 8) {
 		printf("  FAIL  SELFCHECK(last): chk() ran %d times and row_cmp() %d before this run; want 24 and 8\n",
 		    chk_calls, rowcmp_calls);
```

```diff
--- regress/gate_offline.sh.551e
+++ regress/gate_offline.sh.551f
@@ -2261,19 +2261,20 @@
 #                   verdict computed at the call (derive: grep -cE '\? [01] : [01], 1\);'
 #                   regress/diff_wdc_identify.c), and the other
 #                   96 compare inline -- NOT covered.  "Covered" means the COMPARATOR is live,
-#                   not that a row is: the self-check pins chk() and row_cmp() and nothing else.
-#                   What it does not see, disclosed and not chased (measured on #551's passes):
-#                   a keyed or probe-agreeing test inside a comparator; feeding a comparator its
-#                   own want; the TRAILER (one call site -- two coordinated edits keep the count
-#                   and the token consistent; a both-tally reset, conditional, or placed before
-#                   the self-mutant's row); and an edit of the self-check itself.  No single edit
-#                   outside those classes kept gate 2 green (24 measured, #551d).  A reset of
-#                   `failures' alone is caught wherever it sits; so is moving the covered rows
-#                   past the verdict (the last run pins chk() 24 and row_cmp() 8).  The gate-side
-#                   close for the trailer is a covered-row lane, filed as `wdcidlane'.  The file
-#                   prints its comparator call counts on every run, and its PASS needs the G
-#                   line.  #551, by owner ruling 2026-09-25 ("24/128 now, file the rest"); the
-#                   rest is `wdcidcomparators'.
+#                   not that a row is.  What this file's checks can see stops at what the file
+#                   itself writes: a keyed or probe-agreeing test inside a comparator, feeding a
+#                   comparator its own want, that comparator's own failure report switched off, an
+#                   edit of the self-check, or covered rows skipped with their labels and counts
+#                   forged CAN keep this gate green -- measured on #551's passes, disclosed, not
+#                   chased; the close is a lane whose device mutant fails the first covered row,
+#                   filed as `wdcidlane'.  Any edit that leaves the covered rows running and the
+#                   comparators intact is caught: a covered failure prints a line this gate's
+#                   `[0-9]+ failures' check reads at the moment it fails, so no trailer rewrite,
+#                   reset or deferral hides it; the last self-check pins the comparator call
+#                   counts; the run's PASS needs the G line and both tallies at zero.  The file
+#                   covers 24 comparisons and reports all 32 comparator failures.  #551, by owner
+#                   ruling 2026-09-25 ("24/128 now, file the rest"); the rest is
+#                   `wdcidcomparators'.
 #  rtc_range is in the UNIFORM group: every row goes through chk(), its single comparator.
 #  Named here rather than left to be re-derived, because the exception list above
 #  is only trustworthy if additions are classified as they arrive.
```

## 6. QUESTIONS -- the adjudication's stop condition, asked as questions

1. **Is everything the contract says is CAUGHT measured red?**  Section 4's `caught` shapes are my reading of (B) and
   (C)'s sentences.  Is a shape the contract says is caught MISSING from the table, or classed `caught` when the
   contract does not say so?  A green shape the contract says is caught reopens the chain (L2).
2. **Is every green shape inside A-D as worded?**  Name any green shape -- measured here or constructed by you -- that
   the four parts do not cover.  **A green SINGLE edit outside A-D reopens**; the partition claims none can exist
   (every edit is inside a comparator, at its inputs, around it, or in the block).  Test that claim; do not assume it.
3. **Is the report itself sound?**  The '@' guard keeps probe mismatches from reporting (else a healthy log would carry
   a nonzero "N failures").  Is there a probe or a healthy row whose name starts with '@' or reaches a report line?  Is
   there a covered failure that does NOT report?  Does anything in the report text collide with a gate-2 grep (a named
   row, "high byte", the geometry row's text, `@@SELFCHECK@@`)?
4. **Is any sentence of the new contract or the gate-2 bullet false?**  In particular (B)'s "a printed line cannot be
   taken back and no line can be added", and "the file covers 24 comparisons and reports all 32 comparator failures".
5. **What did all of us miss?**

If, while verifying a claim, you found something ELSE -- say so.
