/*
 *  #400: offline differential of the REAL SH-4 TMU tick arithmetic.
 *
 *  WHY THIS COMPILES THE DEVICE FILE INSTEAD OF TRANSCRIBING IT. gate 2 exists
 *  because its first version copied both sides of a differential into its own C
 *  file and compared the copy against itself -- it never linked the code it
 *  claimed to guard, so deleting the correction under test changed nothing.
 *  sh4_timer_tick() is static, so this driver stubs fatal() and #includes
 *  dev_sh4.c, and the function that runs is the one that ships.
 *
 *  #401 corrects how strongly that may be stated. #400 called the old vacuity
 *  "structurally impossible" here; a seat pointed out it is not -- replace the
 *  include with a pasted body and the test is green against a copy again. What
 *  is true, and is enough, is that IT CANNOT HAPPEN SILENTLY WHILE THE INCLUDE
 *  LINE REMAINS: deleting the include does not weaken the test, it fails to
 *  compile.
 *
 *  THE DEFECT: underflow was detected and reloaded in int32_t and then clamped
 *  to zero, so once a reload could not lift the counter back above the sign
 *  boundary it pinned TCNT at 0 permanently. Measured on a booting
 *  OpenBSD/landisk guest: the wall clock tracked host UTC for 17 samples and
 *  then froze, and reproduced offline on the real function at call 56693 =
 *  515.4 s. It also landed on TCOR-1 rather than TCOR, so the old code did not
 *  implement its own comment.
 *
 *  THE ASSUMPTION, stated because there is NO SH-4 manual in this source
 *  collection: TCNT counts TCOR..0 and underflows to TCOR, so a period is
 *  TCOR+1 counts. The only in-tree evidence was the comment this round
 *  replaced; dev_sh4.c now restates it deliberately.
 *
 *  Build: see regress/gate_offline.sh. Runs in milliseconds; no emulator, no
 *  pty, no wall clock, and no dependence on host timing.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>

/*  The one symbol sh4_timer_tick() needs from the rest of the emulator.  */
void fatal(const char *fmt, ...) { (void)fmt; }

#include "../src/devices/dev_sh4.c"

static int failures = 0;
static int rows = 0;

static void reset(struct sh4_data *d)
{
	memset(d, 0, sizeof(*d));
	/*  bsc_rtcsr must stay 0: a non-zero CMIE/OVIE takes the refresh
	    branch at the top of the tick, which fatal()s and exit(1)s.  */
}

/*
 *  One timer, one tick. `hz` is chosen so that (hz / SH4_PSEUDO_TIMER_HZ)
 *  truncates to exactly `step` -- the production expression is left untouched,
 *  so the step this test drives is the step the device computes.
 */
static void row1(const char *name, uint32_t tcor, uint32_t tcnt, uint32_t step,
	uint32_t want_tcnt, int want_unf)
{
	struct sh4_data d;
	uint32_t got;
	int unf;

	reset(&d);
	d.tcor[0] = tcor;
	d.tcnt[0] = tcnt;
	d.timer_hz[0] = (double)step * SH4_PSEUDO_TIMER_HZ;
	d.tstr = TSTR_STR0;

	sh4_timer_tick(NULL, &d);

	got = d.tcnt[0];
	unf = (d.tcr[0] & TCR_UNF) ? 1 : 0;
	rows ++;

	if (got != want_tcnt || unf != want_unf) {
		printf("  FAIL %-34s tcor=%08x tcnt=%08x step=%u -> "
		    "%08x/UNF%d want %08x/UNF%d\n", name, tcor, tcnt, step,
		    got, unf, want_tcnt, want_unf);
		failures ++;
	} else {
		printf("  ok   %-34s %08x/UNF%d\n", name, got, unf);
	}
}

/*
 *  THE ROW THAT EXISTS BECAUSE A SEAT FOUND TWO SURVIVING MUTANTS.
 *
 *  `P12_idx0` (tcor[0] written where tcor[i] is meant) and `P14_cnt0`
 *  (cnt = d->tcnt[0]) are BIT-IDENTICAL to the correct code across all 824288
 *  single-timer cases -- because every other row starts timer 0 only. Measured
 *  with three timers running they diverge on 19990 and 20000 of 20000 cases.
 *
 *  This is a property the rewrite NEWLY RISKS: it introduced two locals and
 *  four [i] subscripts where the previous code indexed inline. A live landisk
 *  boot does not catch either; this row costs microseconds.
 *
 *  Claim under test: THE BODY OPERATES ON THE TIMER IT IS ITERATING.
 */
static void row_three_timers(void)
{
	struct sh4_data d;
	static const uint32_t tcor[3] = { 20833, 0xffffffff, 7 };
	static const uint32_t tcnt[3] = { 100, 100, 3 };
	static const uint32_t step[3] = { 18939, 200, 5 };
	/*  Independently derived: t0 no underflow (step>cnt -> 20833-(18838%20834));
	    t1 wraps once; t2 3 -> underflow, remaining 1, 7-(1%8) = 6.  */
	static const uint32_t want[3] = { 1995, 0xffffff9c, 6 };
	static const int want_unf[3]  = { 1, 1, 1 };
	int i, bad = 0;

	reset(&d);
	for (i = 0; i < 3; i++) {
		d.tcor[i] = tcor[i];
		d.tcnt[i] = tcnt[i];
		d.timer_hz[i] = (double)step[i] * SH4_PSEUDO_TIMER_HZ;
	}
	d.tstr = TSTR_STR0 | (TSTR_STR0 << 1) | (TSTR_STR0 << 2);

	sh4_timer_tick(NULL, &d);
	rows ++;

	for (i = 0; i < 3; i++) {
		int unf = (d.tcr[i] & TCR_UNF) ? 1 : 0;
		if (d.tcnt[i] != want[i] || unf != want_unf[i]) {
			printf("  FAIL three-timers t%d -> %08x/UNF%d want "
			    "%08x/UNF%d\n", i, d.tcnt[i], unf, want[i],
			    want_unf[i]);
			bad = 1;
		}
	}
	if (bad)
		failures ++;
	else
		printf("  ok   %-34s all three advanced independently\n",
		    "three timers at once");
}

/*
 *  The freeze itself, as a regression row rather than a 9.5-minute boot. From
 *  the reset defaults (TCNT = TCOR = 0xffffffff) at the landisk P4 step, the
 *  pre-#400 code pinned TCNT at 0 from call 56693 onward. Here the counter must
 *  still be moving well past that point.
 */
static void row_no_freeze(void)
{
	struct sh4_data d;
	uint32_t step = 75757, prev;
	int i, frozen = 0;

	reset(&d);
	d.tcor[0] = 0xffffffff;
	d.tcnt[0] = 0xffffffff;
	d.timer_hz[0] = (double)step * SH4_PSEUDO_TIMER_HZ;
	d.tstr = TSTR_STR0;

	for (i = 0; i < 70000; i++) {
		prev = d.tcnt[0];
		sh4_timer_tick(NULL, &d);
		/*  A step that exactly divides the period would legitimately
		    revisit a value; 75757 does not divide 2^32, so any repeat
		    here is the clamp, not arithmetic.  */
		if (i > 56693 && d.tcnt[0] == prev) {
			frozen = 1;
			break;
		}
	}
	rows ++;
	if (frozen) {
		printf("  FAIL %-34s TCNT stopped advancing at call %d\n",
		    "no freeze past 515.4 s", i);
		failures ++;
	} else {
		printf("  ok   %-34s still advancing after 70000 calls\n",
		    "no freeze past 515.4 s");
	}
}

int main(void)
{
	printf("SH-4 TMU tick arithmetic (#400), against the REAL dev_sh4.c\n");

	/*  Boundaries around the <= that decides the two arms. The step == cnt
	    case is the one the comparison itself turns on, so it is asserted
	    rather than approached from one side.  */
	row1("step < cnt",            20833,   100,     99,  1,          0);
	row1("step == cnt (boundary)", 20833,  100,    100,  0,          0);
	row1("step == cnt+1 -> TCOR",  20833,  100,    101,  20833,      1);

	row1("full-scale wrap",   0xffffffff,  100,    200,  0xffffff9cU, 1);
	row1("hardclock-shaped",       20833,  100,  18939,  1995,       1);

	/*  TCOR = 0 is period 1 -- but only in STEADY STATE. A seat caught the
	    brief calling it "every step underflows": in the transient the
	    counter must still walk down first.  */
	row1("TCOR=0 steady state",        0,    0,      1,  0,          1);
	row1("TCOR=0 transient, no UNF",   0,    5,      1,  4,          0);

	row1("step == 0 leaves it alone", 20833, 777,     0,  777,       0);

	/*
	 *  #401: THE ROWS THAT MAKE THE MODULO MEAN ANYTHING.
	 *
	 *  Four panel seats independently found that dropping `% period` passed
	 *  every row of #400's table, because no row ever reached
	 *  `remaining >= period`: three had remaining == 0, and the rest used a
	 *  period (2^32, or 20834) far larger than any remaining they produced. The
	 *  modulo IS the correction, and nothing exercised it. The original kill map
	 *  asked which mutants each row catches and never asked which mutant NO row
	 *  catches.
	 *
	 *  These two step past several whole periods, so `remaining % period` is not
	 *  the identity. They also separate period == TCOR+1 from period == TCOR --
	 *  a distinction the earlier rows could not make, which let a mutant that
	 *  guards TCOR==0 to dodge the SIGFPE survive as well.
	 *
	 *    TCOR=5  (period 6):  3 -> 0 is 3 ticks, one more underflows to 5,
	 *                         16 remain; 16 % 6 == 4; 5 - 4 == 1.
	 *                         Period 5 would give 16 % 5 == 1 -> 4.  Distinct.
	 *    TCOR=20833 (period 20834): remaining 99899, 99899 % 20834 == 16563,
	 *                         20833 - 16563 == 4270.
	 */
	row1("multi-period wrap (small)",     5,   3,     20,  1,        1);
	row1("multi-period wrap (hardclock)", 20833, 100, 100000, 4270,  1);
	/*  The counter can legitimately sit far above TCOR -- that is the reset
	    state, and it is what makes the freeze reachable with a small TCOR.
	    Stepping past zero from there must bridge into the periodic regime.  */
	row1("cnt > TCOR bridges in",     20833, 0xfffffffeU, 0xffffffffU, 20833, 1);

	row_three_timers();
	row_no_freeze();

	printf("\n%d rows, %d failures\n", rows, failures);
	if (failures == 0)
		printf("SH4_TMU_PASS\n");
	else
		printf("SH4_TMU_FAIL\n");
	return failures ? 1 : 0;
}
