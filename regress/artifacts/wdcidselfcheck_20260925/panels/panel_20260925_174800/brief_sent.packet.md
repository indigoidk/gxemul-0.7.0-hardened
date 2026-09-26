# #551d -- THE REPAIR'S OWN PASS, AND THE PANEL'S FINDINGS SHARED: the test harness's comparator self-check

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`** (here `regress/`).  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under `_archive/audit-results-*/builds/`).
They are NOT this fork.  **The working tree's `regress/diff_wdc_identify.c` is #551's FIRST version**
(four `row_cmp()` probes, no `cmp_fails`, no `sc_g`); #551b, #551c and #551d exist only as the
generated files and diffs named below.  Review the INLINED code, not the checkout.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — a count, a probe table's answers — ENUMERATE it
rather than reasoning about it.**  Walk the values.

**VERDICT LINE FIRST:** `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`, then numbered findings.

## 1. WHAT THIS IS, AND WHY THIS PASS EXISTS

`regress/diff_wdc_identify.c` is an offline differential test (128 rows) of the emulator's IDE IDENTIFY
data, built against the REAL `src/devices/dev_wdc.c`.  `#551` gives it a SELF-CHECK: a block that feeds
its two comparators, `chk()` and `row_cmp()`, known answers -- including known MISmatches -- and requires
each to change the failure tallies by exactly the right amount, first and last in the run.  Gate 2
(`regress/gate_offline.sh`) then requires the log to print `SELFCHECK the comparator can still fail`
(the G row) and the source to carry the `@@SELFCHECK@@` token (the H row).

**#551c's own pass** (panel `panel_20260925_171441` + a dedicated grok job + the Opus 5.5 measuring seat)
found the repair still let a covered row stop failing with gate 2 green, and four sentences false.
**#551d is the repair of that, and under the repair-chain rule it owes ITS OWN pass: this one.**  The
chain closes on the first VALID pass that finds zero floor breaches -- a zero carried WITH its
denominator (the shapes you tried).  Section 3 gives every seat's findings with my disposition, so you
can correct another seat -- or me.

## 2. SETTLED PREMISES (re-inlined; each verified against the generated #551d file, md5 e0c3399b)

* **Who writes the tallies.**  `failures` and `rows` are file-scope ints (`static int rows = 0, failures
  = 0;`).  `cmp_fails` is incremented ONLY inside `chk()` and `row_cmp()`, each time beside `failures ++`
  (grep `cmp_fails ++` = 2 lines, both in comparator failure arms).  `selfcheck()` ASSIGNS it back
  (`cmp_fails = sc_cf;`, three places) -- a restore, not an increment.  The 96 inline rows and the
  self-check's forced failure write `failures` alone, so on an untampered run `failures >= cmp_fails`.
* **main()'s order** (verbatim call sequence, condensed): `selfcheck("first");` -> eight `row(...)` calls
  (the capacity rows, each into `row_cmp()`) -> 59 zero-argument `row_*()` calls (derive: `grep -cE
  '^[[:space:]]+row_[a-z0-9_]+\(\);$'` over main's body), among them
  `row_ring_occupancy_sound();` (the 24 `chk()` calls) and, later, `row_wide_geometry();` (an INLINE row:
  it increments `failures` directly, never `cmp_fails`) -> `selfcheck("last");` -> the IDENTITY row
  (`rows != 128` -> `failures ++`) -> the trailer (inlined in 4b).
* **Gate 2's wdc checks** (read in `gate_offline.sh`, cited by grep anchor): `grep -c 'WDC_IDENTIFY_PASS'
  "$WDCLOG"` must be `1`; `grep -c 'high byte' "$WDCLOG"` must be `1`; the G text must be in the log; the
  `@@SELFCHECK@@` token must be in the source; and the self-mutant lane `selfmutant_one
  diff_wdc_identify.c src/devices/dev_wdc.c wdc_identify "geometry words carry their high byte"`.
* **The self-mutant lane** (`regress/selfmutant.py`): on the pristine device it needs exactly one
  `ok`/`FAIL` line containing the row id and NOT containing `@@SELFCHECK@@`; with the device mutant
  (`regress/selfmutants/wdc_identify.old` -> `.new`) applied it needs `WDC_IDENTIFY_FAIL` and a `FAIL`
  line naming that row id.  **Its failing row is `row_wide_geometry`, an INLINE row** -- so no gate-2
  input ever makes a COVERED row fail.  (That is why every escape below is measured on device VARIANTS
  the measuring script builds, never by gate 2 itself.)
* The owner ruled #551's scope on 2026-09-25: *"24/128 now, file the rest"* -- 24 rows compare inside a
  comparator the self-check feeds (16 of `chk()`'s 24 calls, all 8 of `row_cmp()`'s); the rest is filed
  as `wdcidcomparators`.

## 3. THE #551c PASS'S FINDINGS, SHARED -- WITH MY DISPOSITION ON EACH

Seats that answered #551c's pass: **agy** (SHIP), **grok** (panel, SHIP WITH CHANGES), **glm, deepseek,
minimax** and the **kimi-k3:cloud** substitute (all SHIP WITH CHANGES), the **dedicated grok** job (SHIP
WITH CHANGES) and the **Opus 5.5** measuring seat (SHIP WITH CHANGES, measured).  **Codex was walled**
(usage limit until 2026-09-26 07:01) and **the kimi CLI was walled** (weekly limit; covered by kimi-k3).
Those are SEAT FAILURES, not agreement.

* **F1 -- the trailer could be weakened: a covered row stops failing, gate 2 stays green.**  Raised
  independently by SIX: Opus 5.5 (MEASURED: `if (cmp_fails >= failures) failures -= cmp_fails;` -- two
  characters -- and `failures -= cmp_fails;` after the reconciliation both print `0 failures` +
  `WDC_IDENTIFY_PASS` on the drop-oldest, DRQ-dropped and word-57 device variants, with the lane green);
  the dedicated grok (the same two, citing Opus's table); grok (`if (cmp_fails == failures) failures = 0`);
  glm (`failures = 0;` AFTER the reconciliation); kimi-k3 (`failures = 0;` between the reconciliation and
  the printf); minimax and deepseek (deleting or neutering the reconciliation line, then a reset).
  **ACCEPTED, FIXED:** the verdict and the exit status read `cmp_fails` DIRECTLY --
  `if (failures == 0 && cmp_fails == 0 && sc_g)` and `return (failures || cmp_fails || !sc_g) ? 1 : 0;`
  -- so no edit of `failures` alone, anywhere, turns the run green.  The reconciliation line stays, for
  the printed count only.  **Measured:** `recon2` (the two-character edit) and `subafter` (the
  subtraction after it) are now RED on drqring and w57hi (table 4c).  *This is glm's and Opus's proposed
  closure, adopted as written; both are asked below to be HARDER on it, not softer.*
* **F2 -- "only they touch it" (the `cmp_fails` declaration and the block comment) is false:** the
  self-check writes `cmp_fails = sc_cf;`.  Opus, dedicated grok, grok, deepseek, kimi-k3.  **ACCEPTED,
  FIXED:** "only they increment it" (both places).
* **F3 -- "A reset of `failures' ALONE after the comparators is not among them" was false** for a reset
  placed after the reconciliation.  Opus, glm, kimi-k3.  **ACCEPTED, FIXED by F1's repair**, and the
  sentence now reads "A reset of `failures' alone is not among them, wherever it sits: the comparators
  also count cmp_fails, which only they increment, and the verdict and the exit status read it directly."
* **F4 -- the self-check never checked that `cmp_fails` MOVED**, so deleting a comparator's `cmp_fails ++`
  plus a `failures` reset silenced the `chk()` rows (Opus MEASURED on the two `chk()` defect variants;
  kimi-k3 predicted it as F3 from the packet).  **ACCEPTED, FIXED:** each probe now requires the exact
  change in `cmp_fails` as well as in `failures`.  **Measured:** `incdel_reset` (that pair) is RED.
* **F5 -- "an edit that keeps those answers and changes the rest KEEPS every gate-2 row green" is false
  as a universal** (a `failures = 0;` after the covered rows keeps the self-check's answers and reds
  gate 2).  Opus.  **ACCEPTED, FIXED:** "CAN keep".
* **F6 -- "Measured on #551's passes" was attached to "an edit of this block itself"**, and no green
  block edit was ever measured -- the block edits measured (deletion; forced-failure removal) are caught.
  Opus.  **ACCEPTED, FIXED:** that class is now marked "(reasoned: the block edits measured so far are
  caught)".
* **F7 -- "restoring `rows' and `failures' after every probe" became incomplete** (the loops also
  restore `cmp_fails`).  kimi-k3.  **ACCEPTED, FIXED.**
* **F8 -- the gate-2 bullet repeated F3 and F5.**  (Mine, from the above.)  **FIXED** the same way.
* **F9 -- the chk()/row_cmp() hunk at the first `cmp_fails ++` might be in `row()`, not `chk()`**
  (minimax, not checkable from its packet).  **REJECTED on reading:** it is in `static void chk(const char
  *name, long long got, long long want)`; `row()` builds a device and calls `row_cmp()` (inlined in 4b).
* **F10 -- `scnoforce_chkstub` printing "1 failures" looked irreconcilable** (minimax).  **EXPLAINED:**
  with the forced failure removed and `chk()` stubbed, the self-check fails (`sc_g` stays 0), and the
  trailer's `if (!sc_g && failures == 0) failures = 1;` supplies the 1.  grok traced the same.
* **F11 -- "The comment rewrite deletes 'each operand zero and past 32 bits'"** (glm).  **REJECTED:** the
  phrase is still the block's second line (the diff replaced the line that carried it with two lines that
  begin with it).
* **F12 -- the brief's (b) reading called `rows` "GREEN as DISCLOSED" while `MINE_rows srstbit` is RED**
  (glm).  **ACCEPTED as a brief-wording fix:** the rows-keyed escape is demonstrated on the pristine
  device; on srstbit some of its eleven failures do not go through `chk()`, which is the only comparator the
  key edits.
* **F13 -- the brief said "run551c.out, file md5 765f71d8"; 765f71d8 is the md5 of the generated C file,
  not of the .out** (agy).  **ACCEPTED** (wording; this brief says "file md5" of the C file only).
* **F14 -- `got57 + got60 != 2 * sectors` in place of `row_cmp()`'s disjunction answers all eight probes
  right and misses a compensating pair** (grok, reasoned).  **DISPOSITION: inside the general disclosure**
  ("an edit that keeps those answers and changes the rest CAN keep every gate-2 row green"), not rowed.
  See D2.
* **F15 -- a gate-2 lane whose device mutant makes a COVERED row fail would catch the both-tally reset
  and every keyed edit that silences it** (deepseek).  **DISPOSITION: FILE, not in this round.**  Today's
  lane mechanism takes one mutant per stem and its row is inline (settled premises); a second lane is a
  harness change owing its own negative controls.  See D3.
* **F16 -- agy: SHIP, "0 false sentences".**  Contradicted by F1-F3 and F5 (measured).  Recorded as a
  reading that missed the trailer, not as a vote.

### DISAGREEMENTS

* **D1 -- "each of row_cmp()'s two disjuncts alone and on either side of its want".**  minimax: misleading
  -- both NEW probes have got ABOVE want, so "either side" contradicts the brief's own "got ABOVE its
  want".  Opus, agy, grok: TRUE -- across all eight probes, `got57` is wrong alone below its want (probes
  0 and 4) and above it (probe 6), `got60` below (1 and 5) and above (7).  **My ruling: TRUE (enumerated
  below in 4a's probe table), reworded for clarity** to "each of row_cmp()'s two disjuncts alone with got
  both below and above its want".  minimax: is the rewording still wrong?
* **D2 -- F14's sum form.**  grok places it inside the general sentence; the cheap alternative is a ninth
  probe `(sectors 2, got57 3, got60 1)`, which the sum form answers wrongly.  **My ruling: disclose, do
  not probe** -- the general sentence exists because every finite probe set admits a predicate agreeing
  on it, and "a probe per clever predicate" is the unbounded growth the floor rules refuse.  Should it
  be NAMED in the disclosure?
* **D3 -- F15's covered-row lane.**  deepseek: a cheap measured close.  Grok (dedicated) and agy: no
  in-file close exists for the both-tally reset; the lane is the only external one.  **My ruling: FILE as
  a queue item carrying deepseek's text verbatim**, because it changes the gate, not the file under
  review, and #551's owner-ruled scope is the comparator self-check.

### WHAT IS STILL OWED, AND WHERE I MIGHT BE FOOLING MYSELF

* **Astra (codex GPT-6 Astra) has not seen #551b, #551c or #551d** -- walled all day.  By owner ruling
  nothing commits until it confirms after 07:01.
* I have ACCEPTED twelve of sixteen findings.  That is a lot of agreement; say which acceptance is wrong.
* F1's fix makes the reconciliation line redundant for the verdict.  I kept it so the printed count
  still shows the comparator failures after a reset -- is keeping it a liability (a line that looks
  load-bearing and is not)?

## 4. THE REPAIR, INLINED AND MEASURED

### 4a. The self-check's probe table, enumerated (from `selfcheck()` in 4b)

```
row_cmp probe  sectors  got57  got60   must fail?  which disjunct is wrong
  0            2        1      2       yes         got57 alone, BELOW its want
  1            2        2      1       yes         got60 alone, BELOW
  2            1        0      0       yes         both, below
  3            3        3      3       NO          --
  4            2^32     0      2^32    yes         got57 alone, below (and a >32-bit operand)
  5            2^32     2^32   0       yes         got60 alone, below
  6            0        1      0       yes         got57 alone, ABOVE (sectors 0)
  7            0        0      1       yes         got60 alone, ABOVE (sectors 0)
chk probe      got      want
  0            1        2              yes
  1            2^32     0              yes
  2            0        1              yes
  3            0        2^32           yes
  4            7        7              NO
```

### 4b. The code under review (the generated #551d file, md5 e0c3399b; code-identical to the measured
### 19018ccb -- the two differ only in one comment's line breaks, checked by comparing
### `gcc -fpreprocessed -dD -E -P` output: md5 280722af for both)

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
	} else {
		printf("  ok   %-38s %llu\n", why, (unsigned long long)sectors);
	}
}

static void row(const char *why, uint64_t sectors)
{
	struct wdc_data d;
	uint64_t got57, got60;

	build(&d, sectors, 1, 1, 1);
	got57 = sectors_from_block(&d, 57, 58);
	got60 = sectors_from_block(&d, 60, 61);
	row_cmp(why, sectors, got57, got60);
}

static void chk(const char *name, long long got, long long want)
{
	chk_calls ++;
	rows ++;
	if (got != want) {
		failures ++;
		cmp_fails ++;
		printf("  FAIL %-40s got %lld want %lld\n", name, got, want);
	} else
		printf("  ok   %-40s %lld\n", name, got);
}

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
	if (!sc_bad && sc_first_bad == 0) {
		sc_g = 1;
		printf("  ok    SELFCHECK the comparator can still fail (first and last)\n");
	} else if (!sc_bad)
		printf("  FAIL  SELFCHECK(last): the first run did not run, or did not pass\n");
	printf("  note  SELFCHECK comparator calls this run: chk() %d, row_cmp() %d\n",
	    chk_calls, rowcmp_calls);
}

/*  ...main() -- order in section 2 ...  */
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

	/*  #551: the comparators' own count survives a reset of `failures' (which always counts at least as
	    many, untouched), and a self-check that did not pass is a failure the count shows.  */
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

### 4c. Measured -- `regress/artifacts/wdcidselfcheck_20260925/measured/run551d_r2.out`

`# #551 measurement 2026-09-25 17:42:20 -- MINE md5 19018ccb, ORIG md5 1fd7ff1d`

(a) the #551d file against HEAD's, -O2 and -O0, on the real `dev_wdc.c` and six variants of it -- byte-identical
except the SELFCHECK lines?  same exit code?

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

(b) controls and escapes -- variant, device variant, exit code, trailer, PASS-token count.  `rc=1` / `0 PASS` is
red.  The device variants: `drqring` drops DRQ from the status (two `chk()` rows fail), `w57hi` zeroes word 57's
high byte (four `row_cmp()` rows fail), `srstbit` tests the wrong control bit (eleven failures).

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
MINE_reset2     drqring   rc=0 | 128 rows, 0 failures | 1 PASS
MINE_reset2     w57hi     rc=0 | 128 rows, 0 failures | 1 PASS
MINE_recon2     drqring   rc=1 | 128 rows, 0 failures | 0 PASS
MINE_recon2     w57hi     rc=1 | 128 rows, 0 failures | 0 PASS
MINE_subafter   drqring   rc=1 | 128 rows, 0 failures | 0 PASS
MINE_subafter   w57hi     rc=1 | 128 rows, 0 failures | 0 PASS
MINE_incdel_reset drqring   rc=1 | 128 rows, 1 failures | 0 PASS
MINE_phase      pristine  rc=0 | 128 rows, 0 failures | 1 PASS
MINE_phase      drqring   rc=0 | 128 rows, 0 failures | 1 PASS
ORIG            drqring   rc=1 | 128 rows, 2 failures | 0 PASS
ORIG            w57hi     rc=1 | 128 rows, 4 failures | 0 PASS
ORIG            srstbit   rc=1 | 128 rows, 11 failures | 0 PASS
```

Reading (b).  **RED as intended:** both comparators stubbed; each disjunct dropped; `&& got`; `uint16_t`
operands; `&& sectors<4`; `<` for `!=` (`lt`); `&& sectors` (`andsect`); the single-tally reset (`reset`, on the
failing variants); the double edits (`scnoforce_*`); **and #551c's three escapes -- `recon2`, `subafter`,
`incdel_reset` -- now red**.  **GREEN as DISCLOSED:** a rows-keyed test (`rows`, `postinc` -- on the PRISTINE
device; see F12), a name-keyed test (`name`, `phase`), a value-keyed test (`want165`), the feed edit (`wrap`), and
the both-tally reset (`reset2`).  `nosc` (the whole block and the verdict's use of its flag deleted) prints PASS
with no G line and no token: gate 2's G and H rows are what catch it.

### 4d. The diff, #551c -> #551d

```diff
--- regress/diff_wdc_identify.c.551c
+++ regress/diff_wdc_identify.c.551d
@@ -505,7 +505,7 @@
     disjunct alone, and a zero, without building a device.  row() and its eight callers are unchanged in
     what they print.  */
 static int rowcmp_calls;
-static int cmp_fails;	/*  failures the two comparators counted; only they touch it  */
+static int cmp_fails;	/*  failures the two comparators counted; only they increment it  */
 
 static void row_cmp(const char *why, uint64_t sectors, uint64_t got57, uint64_t got60)
 {
@@ -5646,10 +5646,10 @@
 
 /*
  *  @@SELFCHECK@@ -- #551.  CAN THIS FILE'S COMPARATORS STILL FAIL?  Feeds chk() and row_cmp() known answers --
- *  each operand zero and past 32 bits, each of row_cmp()'s two disjuncts alone and on either side of its
- *  want, and one pair that must NOT
- *  fail -- and requires the EXACT change in `failures' for each, restoring `rows' and `failures' after every
- *  probe.  Run FIRST (before any row) and LAST (after every row, before the identity row), so a comparator
+ *  each operand zero and past 32 bits, each of row_cmp()'s two disjuncts alone with got both below and
+ *  above its want, and one pair that must NOT fail -- and requires the EXACT change in `failures' and in
+ *  cmp_fails for each, restoring `rows', `failures' and cmp_fails after every probe.  Run FIRST (before
+ *  any row) and LAST (after every row, before the identity row), so a comparator
  *  that goes inert partway through is caught at one end or the other.  Only the success arm prints gate 2's G
  *  text; the failure arm does not, and forces one failure.
  *
@@ -5659,12 +5659,13 @@
  *  other row in this file compares inline: neither is covered by this block.  "Covered" means the
  *  COMPARATOR is live, not that a row is.  NOT CAUGHT, DISCLOSED: the self-check proves only that the
  *  comparators answer right on ITS OWN calls, so an edit that keeps those answers and changes the rest
- *  keeps every gate-2 row green -- a test keyed on a value, a name, a position or the self-check's own
- *  phase that the probes do not share; an edit of the code that FEEDS the comparators (row() handing
- *  row_cmp() its own want); an edit of this block itself.  Measured on #551's passes; reviewed in the
- *  differential, not chased.  A reset of `failures' ALONE after the comparators is not among them: they
- *  also count cmp_fails, which only they touch, and the trailer reports the larger.  A reset of BOTH
- *  tallies is, and is disclosed.  No line this block prints carries the self-mutant row's
+ *  CAN keep every gate-2 row green -- a test keyed on a value, a name, a position or the self-check's
+ *  own phase that the probes do not share, or an edit of the code that FEEDS the comparators (row()
+ *  handing row_cmp() its own want), each measured on #551's passes; or an edit of this block itself
+ *  (reasoned: the block edits measured so far are caught).  Reviewed in the differential, not chased.
+ *  A reset of `failures' alone is not among them, wherever it sits: the comparators also count
+ *  cmp_fails, which only they increment, and the verdict and the exit status read it directly.  A reset
+ *  of BOTH tallies is, and is disclosed.  No line this block prints carries the self-mutant row's
  *  text or "high byte" (gate 2 counts both).  Gate 2's G text is printed ONCE, by the last run, only
  *  when both runs passed -- and the run's own PASS needs that line (sc_g), so a self-check that failed
  *  fails the run even if its forced failure is gone.  The rest of the file is filed as
@@ -5685,13 +5686,14 @@
 
 	for (i = 0; i < 5; i++, n++) {
 		chk("@@SELFCHECK@@/chk", cg[i], cw[i]);
-		if (failures != sc_f + (cg[i] != cw[i]))
+		if (failures != sc_f + (cg[i] != cw[i]) || cmp_fails != sc_cf + (cg[i] != cw[i]))
 			sc_bad++;
 		failures = sc_f; rows = sc_r; cmp_fails = sc_cf;
 	}
 	for (i = 0; i < 8; i++, n++) {
 		row_cmp("@@SELFCHECK@@/row", rw[i], r57[i], r60[i]);
-		if (failures != sc_f + (r57[i] != rw[i] || r60[i] != rw[i]))
+		if (failures != sc_f + (r57[i] != rw[i] || r60[i] != rw[i])
+		    || cmp_fails != sc_cf + (r57[i] != rw[i] || r60[i] != rw[i]))
 			sc_bad++;
 		failures = sc_f; rows = sc_r; cmp_fails = sc_cf;
 	}
@@ -5826,9 +5828,9 @@
 	if (!sc_g && failures == 0)
 		failures = 1;
 	printf("\n%d rows, %d failures\n", rows, failures);
-	if (failures == 0 && sc_g)
+	if (failures == 0 && cmp_fails == 0 && sc_g)
 		printf("WDC_IDENTIFY_PASS\n");
 	else
 		printf("WDC_IDENTIFY_FAIL\n");
-	return (failures || !sc_g) ? 1 : 0;
+	return (failures || cmp_fails || !sc_g) ? 1 : 0;
 }
```

```diff
--- regress/gate_offline.sh.551c
+++ regress/gate_offline.sh.551d
@@ -2262,15 +2262,15 @@
 #                   regress/diff_wdc_identify.c), and the other
 #                   96 compare inline -- NOT covered.  "Covered" means the COMPARATOR is live,
 #                   not that a row is: the self-check proves only its own calls, so an edit that
-#                   keeps those right keeps gate 2 green -- a test keyed on a value, a name, a
-#                   position or the self-check's phase that the probes do not share, feeding a
-#                   comparator its own want, or an edit of the self-check itself (measured on
-#                   #551's passes; disclosed, not chased).  A reset of `failures' alone is not:
-#                   the comparators keep their own count and the trailer reports the larger; a
-#                   reset of both tallies is, and is disclosed.  The
-#                   file prints its comparator call counts on every run, and its PASS needs the
-#                   G line.  #551, by owner ruling 2026-09-25 ("24/128 now, file the rest"); the
-#                   rest is `wdcidcomparators'.
+#                   keeps those right CAN keep gate 2 green -- a test keyed on a value, a name,
+#                   a position or the self-check's phase that the probes do not share, or
+#                   feeding a comparator its own want (measured on #551's passes), or an edit of
+#                   the self-check itself (reasoned); disclosed, not chased.  A reset of
+#                   `failures' alone is not, wherever it sits: the comparators keep their own
+#                   count, which the verdict reads directly; a reset of both tallies is, and is
+#                   disclosed.  The file prints its comparator call counts on every run, and its
+#                   PASS needs the G line.  #551, by owner ruling 2026-09-25 ("24/128 now, file
+#                   the rest"); the rest is `wdcidcomparators'.
 #  rtc_range is in the UNIFORM group: every row goes through chk(), its single comparator.
 #  Named here rather than left to be re-derived, because the exception list above
 #  is only trustworthy if additions are classified as they arrive.
```

## 5. QUESTIONS

1. **The floor question, asked of the SHIPPED COMPOSITE (#551d), not only of the c->d diff:** is there an edit
   -- outside the disclosed classes (a test keyed on a value, a name, a position or the self-check's phase the
   probes do not share; feeding a comparator its own want; an edit of the self-check block; a reset of BOTH
   tallies) -- that keeps every gate-2 check green while a row going through `chk()` or `row_cmp()` can no longer
   fail?  Name the edit, the row it silences, and the gate-2 check it survives.  **A zero needs its denominator.**
2. **Adjudicate F1..F16 and D1..D3** -- UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each.  If you
   raised a finding, be HARDER on my fix for it than on anyone else's.
3. **Which of my twelve acceptances is wrong?**
4. **Does any new or changed sentence say something false?**
5. **Does anything change a healthy run's output beyond the SELFCHECK lines?**
6. **What did all of us miss?**

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
