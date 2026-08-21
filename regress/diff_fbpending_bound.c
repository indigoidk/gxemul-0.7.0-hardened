/*
 *  #442 fbpending: an OFFLINE DIRECT-CALL DETECTOR for the pending-interrupt bound.
 *
 *  *** THIS IS NOT A REPRODUCTION AND MUST NEVER BE RECORDED AS ONE. ***  Under this
 *  project's witness ladder it is rung 1: it #includes the device's own translation
 *  unit and calls timer_tickN() directly, with no machine description, no address
 *  decode and no device dispatch.  It still compiles and still fails with all of that
 *  removed, which is the mechanical discriminator the ladder gives.  The reproduction
 *  is the rung-3 cold-debugger witness; this is the row that DEFENDS the fix.
 *
 *  WHY IT IS NEEDED IN ADDITION TO THE RUNG-3 ROW, measured rather than assumed.  The
 *  rung-3 drain probe measures a backlog by letting DEVICE_TICK deliver ticks the guest
 *  can see.  Two consequences, both measured against real mutants:
 *
 *    - a bound placed in DEVICE_TICK instead of in the callback (mutant m2) is applied
 *      by the very mechanism the probe uses to observe, so the probe reads a bounded
 *      counter and passes.  A direct call never runs DEVICE_TICK at all.
 *    - a bound with no ABSOLUTE ceiling (mutant m6, cap == (int)freq alone) is correct
 *      at cats' 50 MHz and overflows at a higher emulated_hz.  A guest probe cannot
 *      reach that in bounded time: the core delivers at most TIMER_MAX_CATCHUP *
 *      TIMER_BASE_FREQUENCY == 68,157,440 increments per wall second, so 2^31 of them
 *      take 31.5 s AT BEST.  A direct call does 2^31 increments in seconds.
 *
 *  It compiles the SHIPPED source, not a copy of it -- a detector that restates the
 *  code it is testing is the vacuity taxonomy's first entry.
 */

#include "dev_footbridge.c"

#include <limits.h>
#include <stdarg.h>


/*  The four globals main.c owns.  Linking against every object EXCEPT main.o and
    dev_footbridge.o is what keeps this detector honest -- it runs the real timer.c
    and the real footbridge, not re-implementations -- and these are the only
    symbols that dropping main.o leaves undefined.  */
struct settings *global_settings;
int extra_argc;
char **extra_argv;
char *progname = (char *) "fbpending_bound";
size_t dyntrans_cache_size = DEFAULT_DYNTRANS_CACHE_SIZE;


static struct machine fake_machine;
static struct cpu fake_cpu;

static int failures;


/*  #442: the identity row's expected counts, named rather than written inline so a reader
    sees WHICH number moved when a row is added or removed.

    MEASURED, not predicted.  The first draft carried 18/17 from counting the rows by hand
    and both were off by one -- which is the whole argument for this row existing: a count
    a human derives is a count that drifts, and here it was wrong before it ever shipped.  */
#define IDENT_DEEP     19	/*  with R2, i.e. a depth argument was given  */
#define IDENT_SHALLOW  18	/*  without  */

static int rows;

static void row(const char *name, int good, const char *fmt, ...)
{
	va_list ap;
	printf("  %-4s %-44s ", good ? "ok" : "FAIL", name);
	va_start(ap, fmt);
	vprintf(fmt, ap);
	va_end(ap);
	printf("\n");
	rows ++;
	if (!good)
		failures ++;
}


/*
 *  Drive one timer through `n` producer ticks and report the high-water mark.
 *
 *  The counter is read back after EVERY call rather than only at the end, because the
 *  interesting failure is transient: a bound that resets to 1 makes the final value
 *  small even when the peak was INT_MIN.  A final-value-only check would be green on
 *  the very defect this file exists for.
 */
static void drive(struct footbridge_data *d, int nr, long long n,
	int *peak, int *trough)
{
	long long i;
	*peak = INT_MIN;
	*trough = INT_MAX;
	for (i = 0; i < n; i++) {
		switch (nr) {
		case 0: timer_tick0(NULL, d); break;
		case 1: timer_tick1(NULL, d); break;
		case 2: timer_tick2(NULL, d); break;
		case 3: timer_tick3(NULL, d); break;
		}
		if (d->pending_timer_interrupts[nr] > *peak)
			*peak = d->pending_timer_interrupts[nr];
		if (d->pending_timer_interrupts[nr] < *trough)
			*trough = d->pending_timer_interrupts[nr];
	}
}


/*  Arm timer `nr` exactly as a guest would: a control write then a load write,
    through the device's own register handler, so the model's own interpretation of
    the two registers is what is under test rather than a re-derivation of it.  */
static void arm(struct footbridge_data *d, int nr, uint32_t load, uint32_t control)
{
	d->timer_control[nr] = control;
	d->timer_load[nr] = load & TIMER_MAX_VAL;
	reload_timer_value(&fake_cpu, d, nr);
}


int main(int argc, char *argv[])
{
	struct footbridge_data *d;
	int peak, trough, nr;
	long long deep = 0;
	double f;

	if (argc > 1)
		deep = atoll(argv[1]);

	fake_cpu.machine = &fake_machine;
	timer_init();

	printf("==============================================================\n");
	printf("fbpending OFFLINE BOUND DETECTOR (rung 1 -- a DETECTOR, not a\n");
	printf("reproduction).  TIMER_MAX_CATCHUP=%d  TIMER_BASE_FREQUENCY=%.0f\n",
	    TIMER_MAX_CATCHUP, (double)TIMER_BASE_FREQUENCY);
	printf("  the most one timer can be ticked in one wall second: %.0f\n",
	    (double)TIMER_MAX_CATCHUP * TIMER_BASE_FREQUENCY);
	printf("==============================================================\n");

	/*
	 *  R0 -- the CONTROL that makes every row below mean something.  If the harness
	 *  cannot drive the counter at all, every bound row passes vacuously.  Drive an
	 *  ARMED timer 4096 times with the bound deliberately out of reach and require
	 *  the counter to actually move.
	 */
	d = (struct footbridge_data *) calloc(1, sizeof(*d));
	fake_machine.emulated_hz = 50000000;
	arm(d, 0, 1, TIMER_ENABLE);
	drive(d, 0, 4096, &peak, &trough);
	row("R0 the harness can drive the counter at all", peak >= 4096,
	    "peak after 4096 direct ticks = %d (expect >= 4096 with no bound)", peak);
	free(d);

	/*
	 *  R1 -- THE PROPERTY.  For each of the four timers, and for a spread of
	 *  guest-reachable (emulated_hz, load, control) triples, the counter must stay
	 *  inside [0, ceiling] across more increments than the ceiling itself.
	 *
	 *  emulated_hz is included in the sweep because it is USER-REACHABLE: main.c:376
	 *  sets machine->emulated_hz from -I, and emul_parse.c:621 from a config file.  A
	 *  cap of the form (int)freq with no absolute ceiling is correct at 50 MHz and
	 *  becomes INT_MAX at the top of that range -- which is mutant m6, and which no
	 *  row run only at cats' default would ever see.
	 */
	{
		static const struct { int hz; uint32_t load; uint32_t ctrl;
			const char *what; } cases[] = {
		    {    50000000, 0x000100, TIMER_ENABLE|TIMER_FCLK_256, "cats, load 256/256" },
		    {    50000000, 0x000001, TIMER_ENABLE,                "cats, load 1  (50 MHz)" },
		    {    63750000, 0x000001, TIMER_ENABLE,                "netwinder, load 1" },
		    {  1000000000, 0x000001, TIMER_ENABLE,                "-I 1e9, load 1" },
		    {  2147483647, 0x000001, TIMER_ENABLE,                "-I INT_MAX, load 1" },
		    {  2147483647, 0x000000, TIMER_ENABLE,                "-I INT_MAX, load 0 (2^24)" },
		    {    50000000, 0xFFFFFF, TIMER_ENABLE|TIMER_FCLK_256, "cats, slowest legal" },
		};
		const int ceiling = (int)(TIMER_MAX_CATCHUP * (int)TIMER_BASE_FREQUENCY);
		size_t c;
		for (c = 0; c < sizeof(cases)/sizeof(cases[0]); c++) {
			int worst_peak = INT_MIN, worst_trough = INT_MAX;
			d = (struct footbridge_data *) calloc(1, sizeof(*d));
			fake_machine.emulated_hz = cases[c].hz;
			for (nr = 0; nr < N_FOOTBRIDGE_TIMERS; nr++) {
				arm(d, nr, cases[c].load, cases[c].ctrl);
				drive(d, nr, (long long)ceiling + 4096, &peak, &trough);
				if (peak > worst_peak)
					worst_peak = peak;
				if (trough < worst_trough)
					worst_trough = trough;
			}
			f = (double)cases[c].hz /
			    (double)footbridge_effective_cycles(cases[c].load & TIMER_MAX_VAL,
			    cases[c].ctrl, 1);
			row("R1 bounded across all 4 timers",
			    worst_peak <= ceiling && worst_trough >= 0,
			    "%-28s rate %12.2f Hz  peak %11d trough %11d  (ceiling %d)",
			    cases[c].what, f, worst_peak, worst_trough, ceiling);
			/*
			 *  R3 -- ONE INTERRUPT IS STILL OWED, and it is a separate row
			 *  from R1 because a bound that resets to ZERO satisfies R1
			 *  perfectly while dropping an interrupt the guest was owed.
			 *  luna88k resets to 1 for exactly this reason
			 *  (dev_luna88k.c:255-257: "restart the nr of pending
			 *  interrupts", not "forget them").  Measured: this row is the
			 *  only one of the four that separates reset-to-1 from
			 *  reset-to-0, and the rung-3 guest probe cannot see the
			 *  difference at all.
			 */
			row("R3 the reset still owes one interrupt",
			    worst_trough >= 1,
			    "%-28s lowest value the counter ever held: %d",
			    cases[c].what, worst_trough);
			free(d);
		}
	}

	/*
	 *  R2 -- NO SIGNED OVERFLOW, stated as its own row because R1's ceiling is a
	 *  CHOICE and this one is not.  2^31 + 4096 increments at the worst-case rate;
	 *  the counter must never be negative.  Skipped unless a depth is given, because
	 *  it costs a few seconds -- but the default depth is still above any cap the
	 *  fix could reasonably choose.
	 */
	if (deep > 0) {
		d = (struct footbridge_data *) calloc(1, sizeof(*d));
		fake_machine.emulated_hz = 2147483647;
		arm(d, 0, 1, TIMER_ENABLE);
		drive(d, 0, deep, &peak, &trough);
		row("R2 no signed overflow", trough >= 0 && peak >= 0,
		    "%lld direct ticks: peak %d trough %d", deep, peak, trough);
		free(d);
	} else {
		printf("  --   R2 no signed overflow                       "
		       "SKIPPED (pass a depth, e.g. 2147487744)\n");
	}

	/*
	 *  @@SELFCHECK@@ -- the SECOND failability control, asking a different question
	 *  from the self-mutant in gate_offline.sh.  That one breaks dev_footbridge.c and
	 *  demands a NAMED row notice, so it catches a fixture that has stopped reaching
	 *  the code.  This one breaks nothing and feeds row() itself a deliberate
	 *  mismatch, so it catches a comparator edited into always-passing -- a state in
	 *  which every row prints `ok` and the row count AND the verdict token both
	 *  survive.  Neither catches the other's failure.
	 *
	 *  The token in the row name is load-bearing: selfmutant.py filters exactly it,
	 *  and without it these deliberate FAIL lines would be read as a mutant kill for
	 *  a mutant nothing caught.
	 */
	{
		int sc_f = failures, sc_r = rows, sc_bad = 0;

		row("@@SELFCHECK@@/false", 0, "a deliberate mismatch");
		if (failures <= sc_f)
			sc_bad++;
		failures = sc_f; rows = sc_r;

		row("@@SELFCHECK@@/true", 1, "a deliberate match");
		if (failures != sc_f)
			sc_bad++;
		failures = sc_f; rows = sc_r;

		/*  sc_bad is a SEPARATE local that survives the restore above -- restoring
		    `failures` is what makes the sentinel non-destructive, so the evidence
		    cannot live in `failures` itself.  */
		row("SELFCHECK the comparator can still fail", sc_bad == 0,
		    "both directions");
	}

	/*
	 *  R4 -- THE AGGREGATE, and it exists for a mechanical reason rather than a
	 *  semantic one: selfmutant.py requires the pinned row id to name EXACTLY ONE
	 *  row, and R1/R3 each print seven times (once per emulated_hz/load case).  A pin
	 *  of "R1 " would match seven lines and the helper refuses it.  R4 is the unique
	 *  name the lane pins, and any case failing above takes it red.
	 */
	row("R4 every case bounded (the selfmutant pin)", failures == 0,
	    "%d row failure(s) above", failures);

	/*
	 *  IDENTITY -- the row count asserts itself.  Without it, DELETING a row is
	 *  invisible: every remaining row prints ok, the verdict token survives, and the
	 *  gate's `rows actually run` floor only notices a drop BELOW the floor.  This is
	 *  the constblind shape, and gate section E hard-fails a new differential lacking
	 *  it.
	 *
	 *  `rows + 1` counts this row itself, which has not been printed yet -- arguments
	 *  are evaluated before the call.  The expectation is CONDITIONAL on `deep`,
	 *  because R2 only runs when a depth is given, and hardcoding one value would make
	 *  a no-depth run red for no defect.  The SELFCHECK block restores `rows`, so its
	 *  two deliberate rows do not count while its verdict row does.
	 */
	row("IDENTITY: row count", rows + 1 == (deep > 0 ? IDENT_DEEP : IDENT_SHALLOW),
	    "%d rows (expect %d with R2, %d without)",
	    rows + 1, IDENT_DEEP, IDENT_SHALLOW);

	printf("\nFBBOUND_VERDICT=%s\n", failures ? "FAIL" : "PASS");
	return failures ? 1 : 0;
}
