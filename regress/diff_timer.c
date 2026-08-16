/*
 *  Offline differential for the SHIPPED timer core -- src/core/timer.c.
 *
 *  WHY THIS EXISTS.  #427-#429 changed the frequency domain, the catch-up bound and the
 *  RTC's narrowing, and none of that can be seen by a gate that only reads a driver's
 *  output.  The emulator's C had never been driven offline here, so the round's own
 *  research asked whether it COULD be -- and it can: timer_tick() is static, so this file
 *  #includes the shipped source, exactly as the SH-4 TMU differential does.  IT IS THE
 *  REPOSITORY FILE, compiled as committed; there is nothing to keep in sync.
 *
 *  THE ONE STUB IS gettimeofday().  timer_start()/timer_stop() install a real SIGALRM
 *  handler, so this driver does NOT call them: it replicates the two lines of state
 *  timer_start() sets and then calls timer_tick(0) directly, once per simulated host
 *  period.  No signal is ever raised and no host clock enters the measurement -- the
 *  arithmetic is the subject, so letting real time in would make the rows load-sensitive,
 *  which is the oracle class this project has already lost a battery run to.
 *
 *  WHAT IT PROVES, and what it does not.  It proves the DOMAIN and the POLICY: the clamps,
 *  the NaN and infinity handling, that the recorded rate is the running rate, that a
 *  repeated request is idempotent, that the catch-up is bounded, and -- the row that keeps
 *  the round honest -- that an UNDISTURBED timer delivers exactly what it delivered before
 *  the change.  It does NOT prove INTEGRATION: that the twelve other callers still boot and
 *  keep time is a rig question, and only the weekly battery answers it.
 *
 *  EVERY CONSTANT IS READ FROM THE HEADER, never transcribed.  A test that carries its own
 *  copy of the number under test cannot notice when the two disagree -- that is precisely
 *  the defect #425 closed one layer up.
 */
#include <inttypes.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/*  BEFORE the macro below, so the real declaration is seen unmangled: defining
    gettimeofday() first would rewrite the prototype in this header and not compile.  */
#include <sys/time.h>

/*  The stub: the shipped file calls gettimeofday() in its resync path.  Simulated time is
    handed in by the harness so no host clock enters.  */
static double stub_now = 0.0;
static int stub_gettimeofday(struct timeval *tv, void *tz)
{
	(void) tz;
	tv->tv_sec = (long) stub_now;
	tv->tv_usec = (long) ((stub_now - (double) tv->tv_sec) * 1000000.0);
	return 0;
}
#define	gettimeofday(tv, tz)	stub_gettimeofday((tv), (tz))

/*  The other stub: fatal() lives in misc.c, and linking that would drag in the world.
    Counting the calls instead turns the clamp's complaint into something a row can assert
    -- the report must fire ONCE for a repeated request, not once per write.  */
static int fatal_calls;
static void fatal(const char *fmt, ...) { (void) fmt; fatal_calls++; }

#include "../src/core/timer.c"

#undef gettimeofday

static int rows = 0, fails = 0;

static void check(const char *name, const char *got, const char *want)
{
	rows++;
	if (strcmp(got, want) == 0) {
		printf("  ok    %-56s\n", name);
	} else {
		fails++;
		printf("  FAIL  %-56s\n          got  %s\n          want %s\n",
		    name, got, want);
	}
}

static void check_d(const char *name, double got, double want)
{
	char g[64], w[64];
	snprintf(g, sizeof(g), "%.10g", got);
	snprintf(w, sizeof(w), "%.10g", want);
	check(name, g, w);
}

static long long ticks;
static void count_tick(struct timer *t, void *extra) { (void)t; (void)extra; ticks++; }

/*  Drive the shipped tick handler for `periods` host periods, advancing simulated time by
    one period each, and return how many callbacks the timer received.  `stall` inserts a
    gap of that many seconds before the last period, which is how a real backlog arises.  */
static long long run_periods(struct timer *t, int periods, double stall)
{
	int i;
	double step = 1.0 / TIMER_BASE_FREQUENCY;

	(void) t;
	ticks = 0;
	for (i = 0; i < periods; i++) {
		if (stall > 0.0 && i == periods - 1)
			stub_now += stall;
		else
			stub_now += step;
		timer_tick(0);
	}
	return ticks;
}

static struct timer *fresh(double freq)
{
	struct timer *t;
	/*  Start from a clean list so one case cannot inherit another's backlog.  */
	while (first_timer != NULL)
		timer_remove(first_timer);
	timer_current_time = 0.0;
	timer_current_time_step = 1.0 / TIMER_BASE_FREQUENCY;
	timer_countdown_to_next_gettimeofday = 1 << 30;   /*  never resync: see the header  */
	stub_now = 0.0;
	t = timer_add(freq, count_tick, NULL);
	t->next_tick_at = timer_current_time + t->interval;
	return t;
}

int main(void)
{
	struct timer *t;
	char buf[64];
	long long n;

	printf("--- A. the domain: every request lands inside it, and the record agrees ---\n");
	t = fresh(1000.0);
	check_d("an ordinary rate is untouched", t->freq, 1000.0);
	t = fresh(0.0);
	check_d("zero lands on the floor", t->freq, TIMER_MIN_FREQUENCY);
	t = fresh(-5.0);
	check_d("a negative rate lands on the floor", t->freq, TIMER_MIN_FREQUENCY);
	t = fresh(1e300);
	check_d("an absurd rate lands on the ceiling", t->freq, TIMER_MAX_FREQUENCY);
	t = fresh(INFINITY);
	check_d("infinity lands on the ceiling", t->freq, TIMER_MAX_FREQUENCY);

	/*  THE ROW THAT NEEDS THE NEGATED TEST.  A plain `f > MAX` is false for a NaN, so a
	    NaN would pass both clamps, make interval NaN, and the timer would never fire --
	    silently.  The floor is tested first so a NaN lands SLOW rather than fast.  */
	t = fresh(NAN);
	check_d("NaN lands on the FLOOR, not through the clamps", t->freq, TIMER_MIN_FREQUENCY);

	printf("--- B. the interval is finite and positive for every one of them ---\n");
	{
		static const double in[] = { 1000.0, 0.0, -5.0, 1e300, INFINITY, NAN };
		size_t i;
		int bad = 0;
		for (i = 0; i < sizeof(in) / sizeof(in[0]); i++) {
			t = fresh(in[i]);
			if (!(t->interval > 0.0) || !(t->interval < INFINITY))
				bad++;
		}
		snprintf(buf, sizeof(buf), "%d", bad);
		check("no input yields a zero, negative or infinite interval", buf, "0");
	}

	printf("--- C. a repeated request is idempotent, including an absurd one ---\n");
	/*  The row that kills a clamp placed BELOW the early-out: with the clamp at the store
	    only, the comparison sees a CLAMPED record against a RAW request, never matches,
	    and every repeat resets next_tick_at -- measured on five of six input classes.  */
	{
		static const double rep[] = { 1000.0, 1e300, INFINITY, NAN, 0.0, -5.0 };
		size_t i;
		int resets = 0;
		for (i = 0; i < sizeof(rep) / sizeof(rep[0]); i++) {
			double first_at;
			int k;
			t = fresh(rep[i]);
			first_at = t->next_tick_at;
			for (k = 0; k < 5; k++) {
				timer_current_time += 1.0;   /*  time MUST advance: a probe that
				                                 held it fixed cleared the defect  */
				timer_update_frequency(t, rep[i]);
			}
			if (t->next_tick_at != first_at)
				resets++;
		}
		snprintf(buf, sizeof(buf), "%d", resets);
		check("five identical requests reset the schedule for no input", buf, "0");
	}

	printf("--- C2. the complaint is made once, not once per write ---\n");
	{
		int k, before;
		t = fresh(1e300);          /*  one report for the add itself  */
		before = fatal_calls;
		for (k = 0; k < 5; k++) {
			timer_current_time += 1.0;
			timer_update_frequency(t, 1e300);
		}
		snprintf(buf, sizeof(buf), "%d", fatal_calls - before);
		check("five repeats of an absurd rate complain 0 more times", buf, "0");
	}

	printf("--- D. the catch-up is bounded, and the backlog is KEPT ---\n");
	/*  THE BOUND IS PER TIMER PER SIGNAL, so a run of N periods may legitimately deliver
	    N times it -- an earlier version of this row asserted the single-period figure
	    against a two-period run and went red on correct code.  Unbounded, this same case
	    measured over twenty million ticks in ONE signal.  */
	t = fresh(TIMER_MAX_FREQUENCY);
	n = run_periods(t, 2, 1.0);
	snprintf(buf, sizeof(buf), "%s",
	    n <= 2LL * TIMER_MAX_CATCHUP ? "bounded" : "unbounded");
	check("a stalled maximum-rate timer stops at the bound", buf, "bounded");
	snprintf(buf, sizeof(buf), "%s", n > 0 ? "delivered" : "none");
	check("...and it still delivers what it could", buf, "delivered");

	printf("--- E. ANTI-REGRESSION: an undisturbed timer is unchanged ---\n");
	/*  This is the row that forbids "drop the missed ticks": catch-up IS the delivery
	    mechanism for anything faster than the host period, so dropping caps every timer
	    at TIMER_BASE_FREQUENCY.  A 100 Hz timer must still deliver 100 ticks a second.  */
	/*  A FLOOR, NOT AN EXACT COUNT, and the reason is arithmetic rather than laziness:
	    the harness advances simulated time by 1/65 sixty-five times, and in binary that
	    sum lands a hair under 1.0, so the last tick of a second falls outside the window.
	    An exact-count row went red on correct code for that alone.  What must be true is
	    that the CAP CHANGED NOTHING for a timer the host can deliver -- dropping missed
	    ticks would show here as 65, not 99.  */
	t = fresh(100.0);
	n = run_periods(t, (int) TIMER_BASE_FREQUENCY, 0.0);
	snprintf(buf, sizeof(buf), "%s", n >= 99 ? "delivers ~100" : "throttled");
	check("a 100 Hz timer still delivers ~100 ticks per second", buf, "delivers ~100");
	t = fresh(1000.0);
	n = run_periods(t, (int) TIMER_BASE_FREQUENCY, 0.0);
	snprintf(buf, sizeof(buf), "%s", n >= 999 ? "delivers ~1000" : "throttled");
	check("a 1 kHz timer still delivers ~1000", buf, "delivers ~1000");

	/*  IDENTITY, as every differential here carries: a row count asserted against itself,
	    so a truncated or half-copied file cannot report a clean run of fewer rows.  The
	    gate floors the count too; this catches the case where the file still says PASS.  */
	snprintf(buf, sizeof(buf), "%d", rows + 1);
	check("IDENTITY row count -- guards against a stale copy", buf, "14");

	printf("\n%d rows, %d failures\n", rows, fails);
	printf("DIFF_TIMER_%s\n", fails == 0 ? "PASS" : "FAIL");
	return fails ? 1 : 0;
}
