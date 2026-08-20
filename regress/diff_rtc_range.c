/*
 *  #429 differential: does the RTC frequency range check still exist?
 *
 *  *** THIS ROW SAT HELD FOR DAYS ON A RECORDED OBSTACLE THAT WAS FALSE. *** The filing said
 *  a differential "cannot simply #include the device (it pulls in cpu.h, machine.h, emul.h,
 *  device.h)".  MEASURED: FIVE differentials already did exactly this before this one --
 *  diff_footbridge.c:99, diff_m8820x.c:76, diff_m8invread.c:135, diff_sh4_tmu.c:57 and
 *  diff_wdc_identify.c:192 (four distinct devices; m8invread and m8820x share one).  The
 *  round is six stubs and one table, not the four-device refactor the ledger recorded.
 *  A MIS-RECORDED OBSTACLE IS WHY THIS SAT.
 *
 *  *** THE "STRICT SUPERSET" SENTENCE THAT USED TO STAND HERE WAS FALSE, AND SO WAS THE
 *  FIRST CORRECTION OF IT. ***  It read "dev_sh4.c pulls a STRICT SUPERSET of dev_rtc.c's
 *  headers except emul.h".  The flagship seat called that wrong and said emul.h IS pulled
 *  transitively (cpu.h -> cpu_m88k.h -> emul.h) while testmachine/dev_rtc.h is the real
 *  exception.  BOTH were settled by asking the preprocessor rather than reading include
 *  lines, since nearly all of the closure is transitive:
 *
 *      gcc -E -H  ->  dev_rtc.c 23 project headers, dev_sh4.c 35
 *      in dev_rtc.c and NOT in dev_sh4.c:  emul.h  AND  testmachine/dev_rtc.h
 *
 *  So there are TWO exceptions, the original named one of them, the correction named the
 *  other and denied the first, and "strict superset" is false either way.  cpu_m88k.h and
 *  cpu_mips.h mention only float_emul.h, and only in comments.  None of this changes the
 *  conclusion -- the obstacle was refuted by the file COMPILING, not by a header argument --
 *  which is why the sentence was load-bearing for nothing and wrong for three passes.
 *
 *  WHAT IT DEFENDS.  #429 added a range check to dev_rtc.c.  Two seats MEASURED that
 *  reverting it entirely, or flipping its comparison, passes gate 2 -- because NOTHING under
 *  regress/ compiled or even mentioned dev_rtc.c.  That is the fifth vacuity class: a shipped
 *  fix with no detector.
 *
 *  It kills on VALUES, not by crashing: no host clock, no signal handler, no real timer.  The
 *  six stubs are the device's whole contact surface with the emulator, and the timer_add /
 *  timer_remove counters are what let a row say "the ADD became a REMOVE" rather than merely
 *  "something changed".
 *
 *  *** THE PANEL FOUND A REAL ESCAPE AND THE FIRST NINE ROWS DID NOT CATCH IT. ***  Two
 *  seats independently said the clamp TARGET is never asserted -- the rows only check that
 *  the result is nonzero, positive, and did not remove the timer.  MEASURED: changing
 *  `d->hz = (int) TIMER_MAX_FREQUENCY;` to `d->hz = 1;` passed all nine rows.  A guest that
 *  asks for the fastest rate available would silently get 1 Hz.  The three
 *  "clamped to exactly TIMER_MAX_FREQUENCY" rows close that.  They took the table from 9 to
 *  12; the measure seat's two further escapes (below) took it from 12 to 17.
 *
 *  TWO OTHER PANEL CLAIMS WERE MEASURED AND DID NOT SURVIVE, recorded because a refuted
 *  claim is a result:
 *    * "replace TIMER_MAX_FREQUENCY with 0x7fffffff and the limit is gone for everything in
 *      (TIMER_MAX_FREQUENCY, 0x7fffffff]" -- that interval is EMPTY.  timer.h:81 defines the
 *      constant as 2147483647.0, which IS 0x7fffffff, so the edit is a NO-OP and passing it
 *      is the correct answer.  A packet-fed seat reasoning about a constant it cannot read.
 *    * "the rows do not pin the bound" -- HALF REFUTED, AND PASS 2 GOT ITS OWN MEASUREMENT
 *      WRONG.  Pass 2 wrote "raising the threshold past 2^31 fails THREE rows (both 2^32
 *      rows and the bit-31 row)".  Re-measured at the exact value: raising the threshold to
 *      2^31 kills TWO rows and BOTH ARE THE BIT-31 PAIR; the 2^32 rows do not die until the
 *      threshold passes 2^32 (then 5).  Pass 2 had tested 2^36 and described it as "past
 *      2^31" -- the intent, not the measurement, which is the very class this file's own
 *      commit rules warn about.
 *
 *      And the seat was RIGHT in the direction pass 2 did not test.  The bound was pinned
 *      only from ABOVE.  See R6.
 *
 *  *** THE MEASURE SEAT THEN FOUND TWO MORE, AND THE FIRST IS THE CHEAPEST EDIT ON RECORD
 *  HERE. ***  Both passed the 12-row table with ZERO failures:
 *
 *    TIMER_MAX_FREQUENCY -> TIMER_MAX_CATCHUP.  ONE IDENTIFIER, and the two macros sit two
 *      lines apart in timer.h (:81 and :82).  The table sampled exactly ONE in-range value,
 *      1000, so the threshold could be moved anywhere in [1000, INT_MAX] undetected.  Every
 *      guest rate above 2^20 would be silently boosted to INT_MAX -- a rate timer.h:72-77
 *      itself calls unserviceable, where "the debt grows without bound".  Closed by R6/R7.
 *
 *    timer_update_frequency() deleted.  The stubs captured last_timer_hz from the first
 *      draft and NO ROW EVER READ IT, so the device could keep a correct d->hz and never
 *      pass it on.  Closed by R8.
 *
 *  MEASURED, all arms, against the 17-row table (17 rows, 0 failures, RTC_RANGE_PASS
 *  pristine).  Failure counts, not kill counts, so they can be reproduced by running it:
 *    the true pre-#429 revert            -> 7 failures
 *    the flipped comparison              -> 11 failures
 *    clamp target -> 1 Hz                -> 3 failures
 *    threshold -> TIMER_MAX_CATCHUP      -> 1 failure
 *    threshold -> exactly 2^31           -> 2 failures  (both the bit-31 pair)
 *    threshold -> exactly 2^32           -> 5 failures
 *    timer_update_frequency deleted      -> 2 failures
 *    threshold -> 0x7fffffff             -> 0 failures  (a genuine no-op; see above)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <inttypes.h>

void fatal(const char *fmt, ...)
{ va_list ap; va_start(ap, fmt); vfprintf(stderr, fmt, ap); va_end(ap); }

/*  The quoted relative form every differential here uses.  It resolves against THIS file's
    own directory first, which is why a mutant tree must contain the detector too -- the
    lesson diff_diskimage_sync.c's header records after a control tested the fix twice.  */
#include "../src/devices/dev_rtc.c"

/*  The device's whole contact surface with the rest of the emulator.  */
static uint64_t stub_in;              /*  what the "guest" wrote          */
static int      timer_adds, timer_removes, timer_updates;
static double   last_timer_hz;

uint64_t memory_readmax64(struct cpu *cpu, unsigned char *data, int len)
{ (void)cpu; (void)data; (void)len; return stub_in; }
void memory_writemax64(struct cpu *cpu, unsigned char *data, int len, uint64_t d)
{ (void)cpu; (void)data; (void)len; (void)d; }
struct timer *timer_add(double freq, void (*f)(struct timer *, void *), void *e)
{ (void)f; (void)e; timer_adds++; last_timer_hz = freq; return (struct timer *)(void *)&timer_adds; }
void timer_remove(struct timer *t) { (void)t; timer_removes++; }
void timer_update_frequency(struct timer *t, double freq)
{ (void)t; timer_updates++; last_timer_hz = freq; }


static int rows = 0, failures = 0;

static void wr_hz(struct rtc_data *d, uint64_t v)
{
	unsigned char buf[8];
	stub_in = v;
	dev_rtc_access(NULL, NULL, DEV_RTC_HZ, buf, 8, MEM_WRITE, (void *)d);
}

static void chk(const char *name, long long got, long long want)
{
	rows++;
	if (got == want) printf("  ok    %-46s %lld\n", name, got);
	else { failures++; printf("  FAIL  %-46s got %lld want %lld\n", name, got, want); }
}

int main(void)
{
	struct rtc_data d;

	/*
	 *  @@SELFCHECK@@ -- the SECOND failability control, and it asks a different question
	 *  from the self-mutant in gate_offline.sh.  That one breaks dev_rtc.c and demands a
	 *  NAMED row notice, so it catches a fixture that has stopped reaching the code.  This
	 *  one breaks nothing and feeds chk() itself a deliberate mismatch, so it catches a
	 *  comparator edited into always-passing -- a state in which every row prints `ok` and
	 *  the row count, the identity row and the verdict token ALL SURVIVE.
	 *
	 *  Every row in this file goes through chk(), so unlike sh4_tmu (12 of 18) this
	 *  sentinel covers the whole table.  The token in the row name is load-bearing:
	 *  selfmutant.py filters exactly it, and without it these deliberate FAIL lines would
	 *  be read as a mutant kill for a mutant nothing caught.
	 */
	{
		int sc_f = failures, sc_r = rows, sc_bad = 0;

		chk("@@SELFCHECK@@/narrow", 1, 2);
		if (failures <= sc_f)
			sc_bad++;
		failures = sc_f; rows = sc_r;

		/*  A 64-bit mismatch as well as a small one: the defect under test is a
		    NARROWING, so a comparator truncating to int would pass the row above
		    and still be blind to every value this file exists to check.  */
		chk("@@SELFCHECK@@/wide", 0x100000000LL, 0);
		if (failures <= sc_f)
			sc_bad++;
		failures = sc_f; rows = sc_r;

		if (sc_bad) {
			printf("  FAIL  SELFCHECK the comparator no longer compares (%d of 2 "
			    "mismatches went unnoticed) -- every row in this file is inert\n",
			    sc_bad);
			failures = sc_f + 1;
			rows = sc_r;
		} else {
			printf("  ok    SELFCHECK the comparator can still fail       "
			    "narrow+wide\n");
		}
	}

	/*  R1: 2^32 must NOT be read as zero (the #429 narrowing defect).  */
	memset(&d, 0, sizeof d); d.hz = 100;
	d.timer = (struct timer *)(void *)&rows;
	timer_adds = timer_removes = timer_updates = 0;
	wr_hz(&d, 0x100000000ULL);
	chk("2^32: timer NOT removed", timer_removes, 0);
	chk("2^32: hz clamped, not zeroed", d.hz != 0, 1);
	chk("2^32: clamped to exactly TIMER_MAX_FREQUENCY", d.hz,
	    (long long) TIMER_MAX_FREQUENCY);

	/*  R2: bit-31 value must not become a negative int.  */
	memset(&d, 0, sizeof d);
	timer_adds = timer_removes = timer_updates = 0;
	wr_hz(&d, 0x80000000ULL);
	chk("bit31: hz is positive", d.hz > 0, 1);
	chk("bit31: clamped to exactly TIMER_MAX_FREQUENCY", d.hz,
	    (long long) TIMER_MAX_FREQUENCY);

	/*  R3: 0x8000000000000000 must not remove the timer.  */
	memset(&d, 0, sizeof d); d.hz = 100;
	d.timer = (struct timer *)(void *)&rows;
	timer_adds = timer_removes = timer_updates = 0;
	wr_hz(&d, 0x8000000000000000ULL);
	chk("2^63: timer NOT removed", timer_removes, 0);
	chk("2^63: clamped to exactly TIMER_MAX_FREQUENCY", d.hz,
	    (long long) TIMER_MAX_FREQUENCY);

	/*  R4: zero KEEPS its documented meaning -- stop the timer.  */
	memset(&d, 0, sizeof d); d.hz = 100;
	d.timer = (struct timer *)(void *)&rows;
	timer_adds = timer_removes = timer_updates = 0;
	wr_hz(&d, 0);
	chk("zero: hz == 0", d.hz, 0);
	chk("zero: timer removed", timer_removes, 1);

	/*  R5: an ordinary in-range rate is passed through EXACTLY.  */
	memset(&d, 0, sizeof d);
	timer_adds = timer_removes = timer_updates = 0;
	wr_hz(&d, 1000);
	chk("1000 Hz: hz passed through exactly", d.hz, 1000);
	chk("1000 Hz: timer added once", timer_adds, 1);
	chk("1000 Hz: timer core got that same rate", (long long) last_timer_hz, 1000);

	/*
	 *  R6: THE THRESHOLD IS PINNED FROM BELOW.  Until this row the table sampled exactly
	 *  ONE in-range value, 1000, so the bound could be moved anywhere in [1000, INT_MAX]
	 *  undetected.  MEASURED: changing TIMER_MAX_FREQUENCY to TIMER_MAX_CATCHUP -- ONE
	 *  IDENTIFIER, and the two macros are two lines apart in timer.h -- passed all twelve
	 *  rows while boosting every guest rate above 2^20 to INT_MAX.
	 */
	memset(&d, 0, sizeof d);
	timer_adds = timer_removes = timer_updates = 0;
	wr_hz(&d, 1048577);		/*  TIMER_MAX_CATCHUP + 1  */
	chk("above CATCHUP: passed through, NOT clamped", d.hz, 1048577);

	/*
	 *  R7: THE BOUNDARY ITSELF, lower half.  The test is `>`, so the ceiling value must
	 *  pass through untouched.  Its upper half is the bit-31 pair above: 0x80000000 is
	 *  INT_MAX + 1 and must clamp.  Together they pin the comparison to the exact edge --
	 *  a `>=` here would fail this row and nothing else.
	 */
	memset(&d, 0, sizeof d);
	timer_adds = timer_removes = timer_updates = 0;
	wr_hz(&d, 2147483647ULL);
	chk("INT_MAX exactly: passed through, not clamped", d.hz, 2147483647LL);

	/*
	 *  R8: WHAT THE TIMER CORE IS ACTUALLY TOLD, on the update path.  The stubs captured
	 *  last_timer_hz from the beginning and no row read it, so deleting
	 *  timer_update_frequency() entirely passed twelve of twelve -- the device would keep
	 *  a correct d->hz and never pass it on.  A detector that names a value as part of
	 *  "the device's whole contact surface" and then never asserts it is describing its
	 *  own apparatus, not the device.
	 */
	memset(&d, 0, sizeof d); d.hz = 100;
	d.timer = (struct timer *)(void *)&rows;
	timer_adds = timer_removes = timer_updates = 0;
	last_timer_hz = -1.0;
	wr_hz(&d, 500);
	chk("update: existing timer updated, not re-added", timer_updates, 1);
	chk("update: timer core got the new rate", (long long) last_timer_hz, 500);

	/*  IDENTITY: this table asserts its own row count.  */
	chk("IDENTITY: row count", rows + 1, 17);

	printf("%d rows, %d failures\n", rows, failures);
	printf(failures ? "RTC_RANGE_FAIL\n" : "RTC_RANGE_PASS\n");
	return failures ? 1 : 0;
}
