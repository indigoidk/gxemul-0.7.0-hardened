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
 *  THE TWO STUBS ARE gettimeofday() AND fatal().  timer_start() installs a real SIGALRM
 *  handler, so this driver does NOT call it: it replicates the state timer_start() sets
 *  and then calls timer_tick(0) directly, once per simulated host period.  No signal is
 *  ever raised and no host clock enters the measurement -- the arithmetic is the subject,
 *  so letting real time in would make the rows load-sensitive, which is the oracle class
 *  this project has already lost a battery run to.  timer_stop() IS called (section F),
 *  because the cap-hit report is made there and a report with no row is a property with
 *  no detector; it only disarms a timer that was never armed.
 *
 *  WHAT IT PROVES, and what it does not.  It proves the DOMAIN and the POLICY: the clamps,
 *  the NaN and infinity handling, that the recorded rate is the running rate, that a
 *  repeated request is idempotent, that the catch-up stops at EXACTLY the bound, that the
 *  backlog is RETAINED rather than dropped, that the cap hit is reported once and the flag
 *  cleared, and -- the row that keeps the round honest -- that an UNDISTURBED timer
 *  delivers exactly what it delivered before the change.  It does NOT prove INTEGRATION:
 *  that the other callers still boot and keep time is a rig question, and only the weekly
 *  battery answers it.
 *
 *  TWO PROPERTIES THIS INSTRUMENT CANNOT REACH, STATED SO THEY ARE NOT MISTAKEN FOR
 *  COVERED (named by the #429 review panel, 2026-08-16):
 *    1.  Downgrading `volatile sig_atomic_t timer_catchup_hit` to a plain `int` is a
 *        one-word edit that breaks a real property and passes every row here, because no
 *        signal handler is ever installed.  NO ROW CAN CATCH IT -- only a signal-driven
 *        test could, and that test would be load-sensitive.  Recorded, not covered.
 *    2.  #429 lives in src/devices/dev_rtc.c, which this driver does not compile; reverting
 *        it leaves every row green.  MEASURED by the agy seat.  Closing that needs the
 *        guest-rate narrowing to move into the timer core where it is reachable, which is
 *        a shipped-code change in its own round -- filed, not silently tolerated.
 *
 *  EVERY CONSTANT IS READ FROM THE HEADER, never transcribed.  A test that carries its own
 *  copy of the number under test cannot notice when the two disagree -- that is precisely
 *  the defect #425 closed one layer up.
 */
#include <inttypes.h>
#include <limits.h>
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
    -- the report must fire ONCE for a repeated request, not once per write, and the
    cap-hit report in timer_stop() must fire once and not again.  */
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

/*  Drive the shipped tick handler for `periods` host periods and return how many callbacks
    the timer received.  */
static long long run_periods(struct timer *t, int periods)
{
	int i;

	(void) t;
	ticks = 0;
	for (i = 0; i < periods; i++)
		timer_tick(0);
	return ticks;
}

/*
 *  Arm the SHIPPED resync path so the next tick discovers the host clock has run away.
 *
 *  THIS IS THE CORRECTION THE REVIEW FORCED.  The first version of this file advanced a
 *  local `stall` variable that timer_tick() never reads -- timer_current_time is advanced
 *  by the handler itself, and the gettimeofday stub was never called because fresh() had
 *  disabled the resync.  Three review seats traced it independently and one MEASURED that
 *  passing stall=0.0 and stall=100000.0 produced byte-identical output.  A row named "a
 *  stalled timer ..." that does not stall is the "a green row means nothing" class.
 *
 *  Zeroing the countdown makes the next tick take the resync branch, which moves
 *  timer_current_time HALFWAY to the host clock (the shipped code approaches it
 *  exponentially rather than jumping), so ask for twice the lag wanted.  Section D asserts
 *  the clock really moved, so this helper cannot silently go inert again.
 */
static void arm_stall(double host_seconds)
{
	stub_now = host_seconds;
	timer_countdown_to_next_gettimeofday = 0;
}

/*
 *  Disarm it again, and this is NOT optional -- it is the difference between a row that
 *  discriminates and one that does not.
 *
 *  timer_start() is what sets timer_freq, and this driver deliberately never calls it, so
 *  timer_freq is 0.0 and the shipped line that re-arms the countdown after a resync
 *  computes 0 * SECONDS_BETWEEN_GETTIMEOFDAY_SYNCH = 0.  The resync therefore fires again
 *  on EVERY following tick, injecting fresh lag each time.  With that left running, the
 *  deduct-versus-drop row below could not tell the two policies apart: both delivered
 *  enormous counts in the period after the stall, and the drop mutant SURVIVED the census.
 *  One stall, then ordinary periods, is what makes the two policies diverge.
 */
static void disarm_stall(void)
{
	timer_countdown_to_next_gettimeofday = 1 << 30;
}

static struct timer *fresh(double freq)
{
	struct timer *t;
	/*  Start from a clean list so one case cannot inherit another's backlog.  */
	while (first_timer != NULL)
		timer_remove(first_timer);
	timer_current_time = 0.0;
	timer_current_time_step = 1.0 / TIMER_BASE_FREQUENCY;
	timer_countdown_to_next_gettimeofday = 1 << 30;   /*  never resync unless armed  */
	stub_now = 0.0;
	t = timer_add(freq, count_tick, NULL);
	t->next_tick_at = timer_current_time + t->interval;
	return t;
}

int main(void)
{
	struct timer *t;
	char buf[64];
	long long n, n2;

	{
		/*
		 *  SELFCHECK -- CAN THIS FILE'S COMPARATOR STILL FAIL?
		 *
		 *  Feed check() deliberate mismatches and require the failure counter to move,
		 *  then un-record them so the rows are free.  If check() has been stubbed,
		 *  neutered, or had its comparison edited away, EVERY other row in this file is
		 *  silently inert and the gate cannot tell -- measured: 118 rows across five
		 *  detectors stayed green under exactly that stub, row counts, identity rows and
		 *  verdict tokens all intact.
		 *
		 *  TWO MISMATCHES, ONE ALPHABETIC AND ONE DIGIT-LEADING, and the second is not
		 *  padding.  The first version fed only "a" vs "b", and a pass-2 seat defeated it
		 *  with one line -- `isdigit(got[0]) || strcmp(...) == 0` -- because EVERY REAL ROW
		 *  IN THIS FILE COMPARES NUMBERS.  118 rows went inert, this sentinel stayed blind,
		 *  and four of the five gate-2 self-mutants stayed green too.  A sentinel whose
		 *  input does not resemble the rows it vouches for is a sentinel with a whitelist.
		 *
		 *  THE HEALTHY PATH PRINTS AN ok-SHAPED LINE, DELIBERATELY.  The first version
		 *  printed nothing on success and a FAIL line only on failure, which broke two
		 *  things at once: there was no stable string for gate 2 to grep, so DELETING THIS
		 *  WHOLE BLOCK FROM ALL FIVE FILES left the gate at PASS with the same 220 checks
		 *  and zero red rows -- and the FAIL text it printed on the HEALTHY path polluted
		 *  the gate's kill attribution, so a self-mutant pinned to a row id like "fail"
		 *  matched this line and reported OK for a mutant nothing had caught.
		 *
		 *  `>` not `== +1`: a comparator that double-counts compares perfectly well, and
		 *  the exact form printed "no longer compares" at it.  Direction was safe, the
		 *  diagnosis was wrong.
		 *
		 *  This does NOT prove any row is correct.  It proves the comparator still fails on
		 *  inputs shaped like the ones the rows use.  A comparator that compares
		 *  SELECTIVELY -- or that special-cases this row by name -- is still invisible to
		 *  it, and only a census would see that.  Liveness sentinel, nothing more.
		 *
		 *  THE PROBE ROWS ARE NAMED @@SELFCHECK@@ SO THEY CANNOT BE MISTAKEN FOR A ROW.
		 *  They are deliberate mismatches, so check() prints FAIL for them on the HEALTHY
		 *  path -- and a pass-2 seat measured that a self-mutant pinned to a row id like
		 *  "fail" matched one of those lines and reported OK for a mutant nothing caught.
		 *  The obvious cure is worse than the disease: suppressing the print INSIDE check()
		 *  would need a name test in the comparator, which is precisely the whitelist the
		 *  same seat showed defeats this sentinel (`strncmp(name,"SELFCHECK",9)`).  So the
		 *  comparator is left alone and the probe rows carry a token no real row would use;
		 *  selfmutant.py filters it, and gate 2 greps the SUMMARY line below for presence.
		 */
		int selfcheck_f = fails, selfcheck_r = rows, selfcheck_bad = 0;

		check("@@SELFCHECK@@/str", "a", "b");
		if (fails <= selfcheck_f)
			selfcheck_bad++;
		fails = selfcheck_f; rows = selfcheck_r;

		check("@@SELFCHECK@@/num", "1", "2");
		if (fails <= selfcheck_f)
			selfcheck_bad++;
		fails = selfcheck_f; rows = selfcheck_r;

		if (selfcheck_bad) {
			printf("  FAIL  SELFCHECK the comparator no longer compares (%d of 2 "
			    "mismatches went unnoticed) -- every row in this file is inert\n",
			    selfcheck_bad);
			fails = selfcheck_f + 1;
			rows = selfcheck_r;
		} else {
			printf("  ok    SELFCHECK the comparator can still fail       "
			    "str+num\n");
		}
	}

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

	printf("--- A2. the CONSTANTS themselves, which reading them cannot check ---\n");
	/*
	 *  THE BLIND SPOT EVERY READING ROW SHARES, and four seats found it independently.
	 *
	 *  Every row above takes its expected value FROM THE HEADER, which is the rule that
	 *  stops a test carrying a stale copy of the number under test (#425).  But a row that
	 *  reads the constant is BY CONSTRUCTION green for any value of it: three seats
	 *  MEASURED that TIMER_MAX_CATCHUP -> 65536, TIMER_MAX_FREQUENCY -> 32768.0 and
	 *  TIMER_MIN_FREQUENCY -> 1e-300 each break a property the round claims and pass every
	 *  row.  Reading the constant defeats transcription drift; it cannot notice the
	 *  constant being WRONG.
	 *
	 *  So the answer is BOTH: read it above, and assert an ABSOLUTE consequence here --
	 *  one derived from something outside the header.
	 */
	/*  The ceiling's whole claim is that it is INT_MAX, so say that structurally rather
	    than trusting the literal in the header to still be that number.  */
	snprintf(buf, sizeof(buf), "%s",
	    TIMER_MAX_FREQUENCY == (double) INT_MAX ? "INT_MAX" : "NOT INT_MAX");
	check("the ceiling IS INT_MAX, not merely some large literal", buf, "INT_MAX");

	/*  The floor's claim is that it is slow, not that it is any particular slowness; an
	    interval beyond a host lifetime is indistinguishable from a stopped timer.  */
	snprintf(buf, sizeof(buf), "%s",
	    1.0 / TIMER_MIN_FREQUENCY <= 1.0e8 ? "reachable" : "beyond a lifetime");
	check("the floor's interval is still a reachable duration", buf, "reachable");

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

	printf("--- B2. the interval is EXACTLY the reciprocal, not merely positive ---\n");
	/*  Section B asserts only that the interval is finite and positive, so a seat MEASURED
	    that `interval = 0.5 / freq` -- every timer running at twice its rate -- passed the
	    whole file: the anti-regression rows are FLOORS and a doubled rate sails over them.
	    A floor cannot catch a value that is too big.  */
	t = fresh(1000.0);
	snprintf(buf, sizeof(buf), "%s",
	    t->interval == 1.0 / t->freq ? "reciprocal" : "NOT the reciprocal");
	check("the interval is exactly 1/freq", buf, "reciprocal");

	printf("--- C2. the complaint is made once, and it IS made ---\n");
	/*  THE ROW THAT CERTIFIED ITSELF, named by the measuring seat.  The delta-only test
	    below is green when the complaint is made ZERO times, so deleting `*was_clamped = 1`
	    -- the line that makes the clamp complain at all -- passed the entire file.  An
	    absolute row has to come first: the add itself must complain exactly once.  */
	{
		int k, before, at_add;
		before = fatal_calls;
		t = fresh(1e300);          /*  one report for the add itself  */
		at_add = fatal_calls - before;
		snprintf(buf, sizeof(buf), "%d", at_add);
		check("adding a timer above the ceiling complains exactly once", buf, "1");

		before = fatal_calls;
		for (k = 0; k < 5; k++) {
			timer_current_time += 1.0;
			timer_update_frequency(t, 1e300);
		}
		snprintf(buf, sizeof(buf), "%d", fatal_calls - before);
		check("five repeats of an absurd rate complain 0 more times", buf, "0");
	}

	printf("--- D. the catch-up stops at EXACTLY the bound ---\n");
	/*  AN EXACT COUNT, NOT A CEILING, and the review is why.  The first version asserted
	    n <= 2 * TIMER_MAX_CATCHUP over a two-period run, and a seat MEASURED that
	    `budget = 1000` -- three orders of magnitude off -- passed it, as did the
	    off-by-one `--budget < 0`.  A bound row that tolerates a thousand-fold error is
	    not measuring the bound.  One period at the maximum rate owes ~33 million ticks,
	    so exactly TIMER_MAX_CATCHUP must come out.  */
	t = fresh(TIMER_MAX_FREQUENCY);
	n = run_periods(t, 1);
	snprintf(buf, sizeof(buf), "%lld", n);
	snprintf(buf + 32, 32, "%lld", (long long) TIMER_MAX_CATCHUP);
	check("one period at the maximum rate delivers exactly the bound", buf, buf + 32);

	printf("--- D2. the stall used below is REAL (the instrument checks itself) ---\n");
	/*  Without this row the section below can go inert again exactly as it did once: the
	    stall parameter was read by nothing and the row named for it still passed.  */
	t = fresh(100000.0);
	arm_stall(40.0);
	(void) run_periods(t, 1);
	snprintf(buf, sizeof(buf), "%s", timer_current_time > 1.0 ? "clock moved" : "INERT");
	check("arming the resync really moves the emulated clock", buf, "clock moved");

	printf("--- D3. the backlog is DEDUCTED, not DROPPED ---\n");
	/*  THE ROW THE REVIEW SHOWED WAS MISSING, and the round's census was wrong without
	    it: `next_tick_at = timer_current_time` at cap-hit passed every earlier row.  The
	    discriminator needs a case where one signal owes MORE than the cap and the next
	    owes LESS.  A 100 kHz timer owes ~1538 ticks per period normally; a 20 s lag owes
	    ~2 million, over the cap.  Retaining leaves ~950k for the NEXT period; dropping
	    leaves ~1538.  The floor below sits between them with two orders of margin.  */
	t = fresh(100000.0);
	arm_stall(40.0);                  /*  resync halves it: ~20 s of lag  */
	n = run_periods(t, 1);            /*  this period hits the cap  */
	disarm_stall();                   /*  ONE stall, then ordinary periods -- see above  */
	n2 = run_periods(t, 1);           /*  the one after must still be paying it off  */
	snprintf(buf, sizeof(buf), "%s", n == TIMER_MAX_CATCHUP ? "capped" : "not capped");
	check("the stalled period is the one that hits the cap", buf, "capped");
	snprintf(buf, sizeof(buf), "%s", n2 > 100000 ? "kept" : "DROPPED");
	check("the next period still delivers the retained backlog", buf, "kept");

	printf("--- F. the cap hit is REPORTED, once, and the flag is cleared ---\n");
	/*  A property whose only evidence is a comment is a property with no detector: a seat
	    MEASURED that deleting `timer_catchup_hit = 1;` from the handler left every row
	    green.  timer_stop() is the reporting site, so the rows call it.  */
	{
		int before = fatal_calls;
		timer_is_running = 1;          /*  timer_stop() returns early otherwise; this is
		                                   the same state-replication the file already
		                                   does for timer_start()  */
		timer_stop();
		snprintf(buf, sizeof(buf), "%d", fatal_calls - before);
		check("a run that hit the cap reports it exactly once", buf, "1");

		before = fatal_calls;
		timer_is_running = 1;
		timer_stop();
		snprintf(buf, sizeof(buf), "%d", fatal_calls - before);
		check("...and the flag was cleared, so it is not reported twice", buf, "0");

		/*  NEGATIVE CONTROL: without it the two rows above would pass under a mutant
		    that simply reports every time.  */
		t = fresh(100.0);
		(void) run_periods(t, 2);
		before = fatal_calls;
		timer_is_running = 1;
		timer_stop();
		snprintf(buf, sizeof(buf), "%d", fatal_calls - before);
		check("a run that never hit the cap reports nothing", buf, "0");
	}

	printf("--- E. ANTI-REGRESSION: an undisturbed timer is unchanged ---\n");
	/*  This is the row that forbids "drop the missed ticks": catch-up IS the delivery
	    mechanism for anything faster than the host period, so dropping caps every timer
	    at TIMER_BASE_FREQUENCY (65 Hz).  A 100 Hz timer must still deliver ~100 a second.  */
	/*  A FLOOR, NOT AN EXACT COUNT, and the reason is arithmetic rather than laziness:
	    the harness advances simulated time by 1/65 sixty-five times, and in binary that
	    sum lands a hair under 1.0, so the last tick of a second falls outside the window.
	    An exact-count row went red on correct code for that alone.  */
	t = fresh(100.0);
	n = run_periods(t, (int) TIMER_BASE_FREQUENCY);
	snprintf(buf, sizeof(buf), "%s", n >= 99 ? "delivers ~100" : "throttled");
	check("a 100 Hz timer still delivers ~100 ticks per second", buf, "delivers ~100");
	t = fresh(1000.0);
	n = run_periods(t, (int) TIMER_BASE_FREQUENCY);
	snprintf(buf, sizeof(buf), "%s", n >= 999 ? "delivers ~1000" : "throttled");
	check("a 1 kHz timer still delivers ~1000", buf, "delivers ~1000");

	/*
	 *  THE ROW THAT DEFENDS THE CAP'S VALUE, and it is the only kind that can.
	 *
	 *  The header derives TIMER_MAX_CATCHUP from a measurement: 65536 breaks a legitimate
	 *  40 MHz timer, dropping its delivered rate to 0.1065.  Nothing asserted that.  Three
	 *  seats independently MEASURED that the constant can be cut to 65536 -- or a digit
	 *  deleted, or cut to 16 -- with every other row green, because they all read the
	 *  constant and the fastest of them is 1 kHz.
	 *
	 *  40 MHz is not arbitrary: it is the pmax rig's emulated_hz, so this row is the
	 *  offline half of a case the weekly battery boots.  The floor is ABSOLUTE -- derived
	 *  from the machine, not from the header -- which is exactly what makes it able to
	 *  notice the header changing.  65536 would deliver 4,259,840 here.
	 */
	t = fresh(40.0e6);
	n = run_periods(t, (int) TIMER_BASE_FREQUENCY);
	snprintf(buf, sizeof(buf), "%s", n >= 39000000 ? "keeps time" : "THROTTLED");
	check("a 40 MHz timer (the pmax rate) still keeps time", buf, "keeps time");

	/*  IDENTITY, as every differential here carries: a row count asserted against itself,
	    so a truncated or half-copied file cannot report a clean run of fewer rows.  The
	    gate floors the count too; this catches the case where the file still says PASS.  */
	snprintf(buf, sizeof(buf), "%d", rows + 1);
	check("IDENTITY row count -- guards against a stale copy", buf, "24");

	printf("\n%d rows, %d failures\n", rows, fails);
	printf("DIFF_TIMER_%s\n", fails == 0 ? "PASS" : "FAIL");
	return fails ? 1 : 0;
}
