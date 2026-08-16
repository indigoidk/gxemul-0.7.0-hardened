/*
 *  Offline differential for the SHIPPED footbridge timer -- src/devices/dev_footbridge.c.
 *
 *  WHY THIS EXISTS.  #432 fixed a guest-reachable HOST CRASH: `random() % timer_load[i]` with
 *  a guest-writable zero load is an integer division by zero, reproduced independently by two
 *  seats as SIGFPE (exit 136).  A crash fix with no detector is this project's fifth vacuity
 *  class, and here the detector had to be offline for a reason stronger than convenience:
 *  THERE IS NO NETWINDER OR CATS RIG ANYWHERE IN regress/ -- nothing in this tree boots a
 *  machine that has a footbridge.  So this is not the cheapest detector, it is the ONLY
 *  possible one.
 *
 *  IT IS THE REPOSITORY FILE.  This driver #includes the shipped dev_footbridge.c, exactly as
 *  diff_sh4_tmu.c #includes dev_sh4.c -- an identical header set, and the precedent that made
 *  the feasibility question answerable at all.  Nothing is transcribed.
 *
 *  SEVEN STUBS, and `-Wl,--gc-sections` is LOAD-BEARING rather than cosmetic: without it the
 *  link needs eleven more symbols (bus_pci_*, interrupt_*, console_start_slave,
 *  machine_add_tickfunction, memory_device_register).  The trade-off, stated so it is not
 *  mistaken for coverage: gc-sections drops DEVINIT, so this file cannot test devinit.
 *
 *  THE TWO STUBS THAT ARE INSTRUMENTS, not scaffolding: timer_add() and
 *  timer_update_frequency() RECORD the frequency the device asked for.  That is what lets a
 *  row assert the rate semantics directly, instead of inferring them from a boot that cannot
 *  happen here.
 *
 *  EXPECTED VALUES ARE ABSOLUTES DERIVED FROM THE 24-BIT WIDTH, never re-read from the header
 *  symbol the code itself uses.  R4's review established that a row which takes its expected
 *  value from the code under test is green for ANY value of it (filed as `constblind`), so
 *  16777216 is written out here on purpose.
 */
#include <inttypes.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#include "include/misc.h"
#include "include/memory.h"
#include "include/machine.h"
#include "include/cpu.h"

bool single_step = false;
bool about_to_enter_single_step = false;
static int verb[16];
int *debugmsg_current_verbosity = verb;

static int fatal_calls;
void fatal(const char *fmt, ...) { (void) fmt; fatal_calls++; }
void debug(const char *fmt, ...) { (void) fmt; }

/*  The recorder stubs: what rate did the device ASK the timer core for?  */
static double last_freq = -1.0;
static int timer_add_calls, timer_update_calls;
struct timer;
struct timer *timer_add(double freq, void (*f)(struct timer *, void *), void *extra)
{
	(void) f; (void) extra;
	last_freq = freq;
	timer_add_calls++;
	return (struct timer *) (void *) &last_freq;	/*  non-NULL cookie  */
}
void timer_update_frequency(struct timer *t, double freq)
{
	(void) t;
	last_freq = freq;
	timer_update_calls++;
}

uint64_t memory_readmax64(struct cpu *cpu, unsigned char *buf, int len)
{
	uint64_t x = 0; int i;
	(void) cpu;
	/*  Little-endian, which is what the rigs are; the device only ever reads back what
	    this driver wrote, so the convention only has to be self-consistent.  */
	for (i = 0; i < len; i++)
		x |= (uint64_t) buf[i] << (8*i);
	return x;
}
void memory_writemax64(struct cpu *cpu, unsigned char *buf, int len, uint64_t data)
{
	int i;
	(void) cpu;
	for (i = 0; i < len; i++)
		buf[i] = (data >> (8*i)) & 255;
}
void console_putchar(int handle, int ch) { (void) handle; (void) ch; }

/*  The device asserts an interrupt on every delivered tick, and INTERRUPT_ASSERT calls
    through a function pointer in the struct.  A calloc'd struct leaves that NULL, so the
    first tick SIGSEGVs -- which looks exactly like the crash under test and would have made
    this whole file a liar.  Install counting no-ops instead.  */
static int irq_asserts, irq_deasserts;
static void noop_assert(struct interrupt *i) { (void) i; irq_asserts++; }
static void noop_deassert(struct interrupt *i) { (void) i; irq_deasserts++; }

#include "../src/devices/dev_footbridge.c"

/*  Needs the struct, so it lives AFTER the device include.  */
static void arm_irqs(struct footbridge_data *d)
{
	int i;
	for (i = 0; i < N_FOOTBRIDGE_TIMERS; i++) {
		d->timer_irq[i].interrupt_assert = noop_assert;
		d->timer_irq[i].interrupt_deassert = noop_deassert;
	}
}

/* --------------------------------------------------------------- harness --- */

static int rows, fails;
static void check(const char *name, const char *got, const char *want)
{
	rows++;
	if (strcmp(got, want) == 0)
		printf("  ok    %-54s %s\n", name, got);
	else {
		fails++;
		printf("  FAIL  %-54s\n          got  %s\n          want %s\n",
		    name, got, want);
	}
}
static void check_u(const char *name, uint64_t got, uint64_t want)
{
	char g[32], w[32];
	snprintf(g, sizeof(g), "%" PRIu64, got);
	snprintf(w, sizeof(w), "%" PRIu64, want);
	check(name, g, w);
}

/*  The helper is static inside the shipped file, which is exactly why this driver includes
    the file rather than linking it.  */
int main(void)
{
	struct footbridge_data *d;
	struct cpu *cpu;
	struct machine *machine;

	/*  LINE-BUFFERED ON PURPOSE.  gate_offline.sh redirects this binary's stdout to a file,
	    which makes it FULLY buffered -- so when a mutant re-introduces the crash, the log is
	    0 BYTES and the operator gets a red row with nothing in it.  Measured: line-buffered,
	    the same run leaves 943 bytes naming A1/B2/D1 as FAIL before it dies.  The gate's
	    greps fail either way, so this is legibility rather than detection -- but it is this
	    project's own recorded stdout-buffering trap, in a new place.  */
	setvbuf(stdout, NULL, _IOLBF, 0);

	cpu = calloc(1, sizeof(struct cpu));
	machine = calloc(1, sizeof(struct machine));
	d = calloc(1, sizeof(struct footbridge_data));
	cpu->machine = machine;
	machine->emulated_hz = 100000000;	/*  100 MHz, an ordinary rate  */

	printf("--- A. the load interpretation: zero is a FULL PERIOD, never a divisor of 0 ---\n");
	/*  16777216 == 2^24, written as an absolute rather than read from TIMER_MAX_VAL: a row
	    that takes its expected value from the code under test cannot notice the code
	    changing (the `constblind` finding).  */
	check_u("A1 load 0 becomes the full 24-bit span",
	    footbridge_effective_cycles(0, 0, 0), 16777216);
	check_u("A2 an ordinary load is untouched",
	    footbridge_effective_cycles(1000, 0, 0), 1000);
	check_u("A3 the maximum load is untouched",
	    footbridge_effective_cycles(0xffffff, 0, 0), 16777215);

	printf("--- B. the prescaler is 64-bit MULTIPLICATION, not a signed shift ---\n");
	/*  THE ROW THAT CATCHES THE DEFECT THE OBVIOUS FIX RE-CREATES.  The old code used
	    `int cycles` with `cycles <<= 8`; three seats found independently that this
	    overflows for exactly half the legal range, and that mapping zero to 2^24 while
	    leaving `int` gives 2^24 << 8 == 2^32 == 0 -> +INF again.  B1 and B2 are the two
	    halves of that: the reset load prescaled, and the zero load prescaled.  */
	check_u("B1 reset load x256 does not overflow",
	    footbridge_effective_cycles(0xffffff, TIMER_FCLK_256, 1),
	    (uint64_t) 16777215 * 256);
	check_u("B2 zero load x256 does not wrap to zero",
	    footbridge_effective_cycles(0, TIMER_FCLK_256, 1),
	    (uint64_t) 16777216 * 256);
	check_u("B3 the x16 prescaler", footbridge_effective_cycles(1000, TIMER_FCLK_16, 1),
	    16000);

	printf("--- C. TIMER_EXTERNAL is a LEGAL encoding and must not kill the host ---\n");
	/*  Both prescaler bits set is TIMER_EXTERNAL (0x0C).  The order of the tests matters:
	    with a bare `else if` chain, 0x0C reads as FCLK_16 by accident.  */
	check_u("C1 TIMER_EXTERNAL is not silently read as x16",
	    footbridge_effective_cycles(1000, TIMER_FCLK_16 | TIMER_FCLK_256, 1), 1000);

	printf("--- D. THE TWO CONSUMERS LIVE IN DIFFERENT DOMAINS ---\n");
	/*  THE ROW A TENTH READING FORCED.  timer_value is a 24-bit GUEST-READABLE register.
	    Feeding it the PRESCALED span would store values far above 24 bits -- the measuring
	    seat's own first proposal did exactly that and put 19833 of 20000 ticks out of
	    range.  The prescaler slows the RATE; it does not widen the COUNTER.  */
	check_u("D1 the counter domain ignores the prescaler",
	    footbridge_effective_cycles(0, TIMER_FCLK_256, 0), 16777216);
	{
		int i, over = 0;
		arm_irqs(d);
		d->timer_load[0] = 0;
		d->timer_control[0] = TIMER_ENABLE | TIMER_FCLK_256;
		d->pending_timer_interrupts[0] = 1;
		for (i = 0; i < 20000; i++) {
			dev_footbridge_tick(cpu, d);
			if (d->timer_value[0] > 0xffffff)
				over++;
		}
		check_u("D2 20000 ticks leave the 24-bit counter in range", over, 0);
	}
	/*  D3 EXISTS BECAUSE D2 WAS NOT ENOUGH, and the review measured why: every tick-path
	    row above uses load == 0, and for load == 0 the constant 16777216 is exactly the
	    right answer -- so replacing the whole helper call with that literal passed the
	    entire file.  The counter must TRACK THE GUEST'S LOAD, not merely stay in range.  */
	{
		int i, over = 0;
		struct footbridge_data *e = calloc(1, sizeof(*e));
		arm_irqs(e);
		e->timer_load[0] = 1000;
		e->timer_control[0] = TIMER_ENABLE;
		e->pending_timer_interrupts[0] = 1;
		for (i = 0; i < 20000; i++) {
			dev_footbridge_tick(cpu, e);
			if (e->timer_value[0] >= 1000)
				over++;
		}
		check_u("D3 the counter stays below the guest's OWN load", over, 0);
		free(e);
	}

	printf("--- E. the rate the device asks the timer core for ---\n");
	memset(d, 0, sizeof(*d));
	d->timer_load[0] = 1000;
	d->timer_control[0] = TIMER_ENABLE;
	last_freq = -1.0;
	reload_timer_value(cpu, d, 0);
	check_u("E1 a 1000-cycle load at 100 MHz asks for 100 kHz",
	    (uint64_t) (last_freq + 0.5), 100000);
	/*  E2 is the route that needs NO load write at all: the reset load is TIMER_MAX_VAL,
	    so one write of ENABLE|FCLK_256 reaches the old overflow.  Before #432 this asked
	    for a NEGATIVE rate, which the core's floor clamp turned into one tick per ~3.2
	    years, silently.  */
	d->timer_load[0] = 0xffffff;
	d->timer_control[0] = TIMER_ENABLE | TIMER_FCLK_256;
	last_freq = -1.0;
	reload_timer_value(cpu, d, 0);
	check(  "E2 the reset load x256 asks for a POSITIVE rate",
	    last_freq > 0.0 ? "positive" : "NEGATIVE OR ZERO", "positive");
	/*  E3: a zero load must ask for a slow, SERVICEABLE rate -- not the domain ceiling.
	    100e6 / 2^24 is about 5.96 Hz.  */
	d->timer_load[0] = 0;
	d->timer_control[0] = TIMER_ENABLE;
	last_freq = -1.0;
	reload_timer_value(cpu, d, 0);
	check(  "E3 a zero load asks for a few Hz, not the ceiling",
	    (last_freq > 1.0 && last_freq < 100.0) ? "serviceable" : "OUT OF RANGE",
	    "serviceable");
	/*  E4 EXISTS BECAUSE E2 WAS A SIGN-ONLY ORACLE, and the review measured the cost of
	    that: changing the `1` in reload_timer_value()'s helper call to a `0` -- ONE
	    CHARACTER -- silently deletes the prescaler from the RATE domain for every guest,
	    and all fifteen rows stayed green.  Sections B and C prove the HELPER prescales;
	    D1/D2 prove the COUNTER consumer does not; nothing pinned the RATE consumer to
	    prescaling, which is the round's headline design decision.  100 MHz / (1000 * 256)
	    is 390.625 Hz; the mutant asks for 100000, a rate 256x too fast.  */
	d->timer_load[0] = 1000;
	d->timer_control[0] = TIMER_ENABLE | TIMER_FCLK_256;
	last_freq = -1.0;
	reload_timer_value(cpu, d, 0);
	check_u("E4 the RATE consumer really applies the x256 prescaler",
	    (uint64_t) (last_freq * 1000.0 + 0.5), 390625);

	printf("--- F. END TO END: the shipped tick survives route 2, in a forked child ---\n");
	/*  ROUTE 2, the one that PREDATES #427/#428 and is the reason this round does not get
	    to blame its own hardening: TIMER_x_LOAD does not clear pending_timer_interrupts
	    (TIMER_x_CONTROL does), so an ordinary legal timer accrues a backlog and a later
	    write of zero divides.  Forked, because a mutant that re-crashes would otherwise
	    take the whole gate binary down and score as a census FAULT rather than a named-row
	    KILL.  */
	{
		pid_t pid = fork();
		if (pid == 0) {
			struct footbridge_data *c = calloc(1, sizeof(*c));
			int i;
			arm_irqs(c);
			c->timer_load[0] = 50000;	/*  an ordinary legal timer  */
			c->timer_control[0] = TIMER_ENABLE;
			for (i = 0; i < 400; i++)
				c->pending_timer_interrupts[0]++;
			c->timer_load[0] = 0;		/*  the guest writes zero  */
			dev_footbridge_tick(cpu, c);
			_exit(0);
		} else {
			int st = 0;
			waitpid(pid, &st, 0);
			check("F1 a zero load after a backlog does not kill the host",
			    WIFEXITED(st) && WEXITSTATUS(st) == 0 ? "survived"
			    : "KILLED BY SIGNAL", "survived");
		}
	}

	printf("--- G. the CONTROL write path: a legal encoding must not exit() ---\n");
	/*  THE ROW THAT DEFENDS THE FOLD.  Section C proves the helper INTERPRETS 0x0C; this
	    proves the guest can actually WRITE it.  Before #432 this exact write reached
	    fatal()+exit(1) in the CONTROL arm -- a guest selecting the external clock source
	    killed the host, and no amount of helper correctness would have saved it.  Forked,
	    because a mutant that restores the exit(1) would otherwise take the gate binary
	    down and score as a census FAULT instead of a named-row KILL.  */
	{
		pid_t pid = fork();
		if (pid == 0) {
			struct footbridge_data *c = calloc(1, sizeof(*c));
			unsigned char buf[4];
			arm_irqs(c);
			c->timer_load[0] = 1000;
			memset(buf, 0, sizeof(buf));
			buf[0] = TIMER_ENABLE | TIMER_FCLK_16 | TIMER_FCLK_256;
			dev_footbridge_access(cpu, NULL, TIMER_1_CONTROL, buf,
			    4, MEM_WRITE, c);
			_exit(0);
		} else {
			int st = 0;
			waitpid(pid, &st, 0);
			check("G1 a guest write of ENABLE|EXTERNAL does not exit()",
			    WIFEXITED(st) && WEXITSTATUS(st) == 0 ? "survived"
			    : "HOST KILLED", "survived");
		}
	}

	printf("--- H. the LOAD register reads back EXACTLY what the guest wrote ---\n");
	/*  THE FIFTH-VACUITY-CLASS ROW, and the adjudicating seat found it by attacking its own
	    design: "timer_load[] is never rewritten -- the guest reads back exactly what it
	    wrote" is a shipped, load-bearing claim, and it had NO DETECTOR.  Reinstating
	    normalize-at-write -- `timer_load = idata ? idata : 1`, precisely the alternative
	    this round REJECTED -- passed all fifteen rows, because nothing in this file ever
	    drove TIMER_1_LOAD through the access handler; every other row pokes struct fields
	    directly.  These two rows go through dev_footbridge_access in both directions.  */
	{
		struct footbridge_data *h = calloc(1, sizeof(*h));
		unsigned char buf[4];
		uint64_t back;
		arm_irqs(h);

		memset(buf, 0, sizeof(buf));
		dev_footbridge_access(cpu, NULL, TIMER_1_LOAD, buf, 4, MEM_WRITE, h);
		memset(buf, 0xff, sizeof(buf));
		dev_footbridge_access(cpu, NULL, TIMER_1_LOAD, buf, 4, MEM_READ, h);
		back = memory_readmax64(cpu, buf, 4);
		check_u("H1 a guest write of 0 reads back as 0, not normalised", back, 0);

		/*  H2 pins the 24-bit MASK as well: 0x1000000 is "one full wrap", and the mask
		    aliases it to zero -- which is the arithmetic that makes the full-period
		    mapping the continuous choice in the first place.  */
		memset(buf, 0, sizeof(buf));
		memory_writemax64(cpu, buf, 4, 0x1000000);
		dev_footbridge_access(cpu, NULL, TIMER_1_LOAD, buf, 4, MEM_WRITE, h);
		memset(buf, 0xff, sizeof(buf));
		dev_footbridge_access(cpu, NULL, TIMER_1_LOAD, buf, 4, MEM_READ, h);
		back = memory_readmax64(cpu, buf, 4);
		check_u("H2 0x1000000 is masked to 0, and stays 0 on read-back", back, 0);
		free(h);
	}

	/*  IDENTITY, as every differential here carries.  */
	{
		char buf[32];
		snprintf(buf, sizeof(buf), "%d", rows + 1);
		check("IDENTITY row count -- guards against a stale copy", buf, "19");
	}

	printf("\n%d rows, %d failures\n", rows, fails);
	printf("DIFF_FOOTBRIDGE_%s\n", fails == 0 ? "PASS" : "FAIL");
	return fails ? 1 : 0;
}
