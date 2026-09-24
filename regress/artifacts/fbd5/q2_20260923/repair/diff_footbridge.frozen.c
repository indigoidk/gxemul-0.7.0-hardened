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

	/*  fbclearread: `case TIMER_1_CLEAR:` carries NO writeflag test, while the case
	    immediately above it (TIMER_1_CONTROL) does.  So a guest READ runs the whole
	    body: it reloads the counter when periodic, decrements the pending count, and
	    DEASSERTS the interrupt.  A guest that merely reads the register silently
	    acknowledges a pending timer interrupt -- the likely guest-visible consequence
	    is a LOST interrupt, not a corrupted value.

	    FOUR addresses, not one: the timer fold normalises 0x30C/0x32C/0x34C/0x36C onto
	    this single case.

	    These rows drive the ACCESS HANDLER rather than poking struct fields, for the
	    reason this file already records above: a struct-poking row cannot see a
	    handler-level defect at all.  */
	{
		struct footbridge_data *h = calloc(1, sizeof(*h));
		unsigned char buf[4];
		uint64_t back;

		arm_irqs(h);

		/*  CONTROL first: a WRITE must decrement.  Without it a green defect row
		    could equally mean the handler never ran.  */
		h->pending_timer_interrupts[0] = 2;
		memset(buf, 0, sizeof(buf));
		dev_footbridge_access(cpu, NULL, TIMER_1_CLEAR, buf, 4, MEM_WRITE, h);
		check_u("[LIVE] a WRITE of TIMER_1_CLEAR decrements pending",
		    h->pending_timer_interrupts[0], 1);

		/*  THE DEFECT: a READ must leave the pending count alone.  */
		h->pending_timer_interrupts[0] = 2;
		memset(buf, 0xff, sizeof(buf));
		dev_footbridge_access(cpu, NULL, TIMER_1_CLEAR, buf, 4, MEM_READ, h);
		/*  THE GUARD WRAPS THREE EFFECTS AND THE ROWS ABOVE OBSERVE TWO.
		    reload_timer_value and the pending decrement are both pinned;
		    INTERRUPT_DEASSERT was not.  A panel seat named the mutant that
		    exploits the gap -- hoist the deassert OUT of the guard so a READ
		    still deasserts:

		        if (writeflag == MEM_WRITE) { reload; pending--; }
		        INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);

		    Every other row passes -- the deassert touches neither the pending
		    count nor timer_value -- while the guest READ once again
		    acknowledges a pending interrupt.  **That is #474's headline
		    symptom, reintroduced**: the round's own record calls the
		    consequence a LOST interrupt, and a lost interrupt IS a spurious
		    deassert.

		    The counter was already armed by noop_deassert and NEVER READ.
		    A counter nothing asserts on is a row that does not exist.  */
		/*  THE ACCEPT COMPANION, and the row below is HALF A ROW without it.
		    A row that wants ZERO can only fail UPWARD: delete
		    INTERRUPT_DEASSERT from the guarded body outright and the READ
		    row stays green, because zero deasserts is exactly what it
		    asserts.  Measured by a panel seat against the version that
		    shipped this row without its pair.

		    This is the de-escalation clause's accept side in miniature:
		    the fix made a channel CONDITIONAL, so the detector owes a row
		    proving the channel still fires on the legal path.  */
		irq_deasserts = 0;
		h->pending_timer_interrupts[0] = 2;
		memset(buf, 0, sizeof(buf));
		dev_footbridge_access(cpu, NULL, TIMER_1_CLEAR, buf, 4, MEM_WRITE, h);
		check_u("[LIVE] a WRITE DOES deassert the irq", irq_deasserts, 1);

		irq_deasserts = 0;
		h->pending_timer_interrupts[0] = 2;
		memset(buf, 0xff, sizeof(buf));
		dev_footbridge_access(cpu, NULL, TIMER_1_CLEAR, buf, 4, MEM_READ, h);
		check_u("a READ must NOT deassert the irq", irq_deasserts, 0);

		check_u("a READ of TIMER_1_CLEAR must NOT clear pending",
		    h->pending_timer_interrupts[0], 2);

		/*  ENABLE.  A measuring seat named this the worst of five one-token
		    escapes: widen the guard with `|| (timer_control & TIMER_ENABLE)`
		    and it sweeps the whole table, because every other row here uses
		    control = 0 or PERIODIC and never TIMER_ENABLE.

		    It is the worst because of WHICH state it re-opens: a DISABLED
		    timer can never hold a pending interrupt, so the mutant re-opens
		    the defect on precisely the state this round exists for.  */
		h->timer_control[0] = TIMER_ENABLE;
		h->pending_timer_interrupts[0] = 2;
		memset(buf, 0xff, sizeof(buf));
		dev_footbridge_access(cpu, NULL, TIMER_1_CLEAR, buf, 4, MEM_READ, h);
		check_u("an ENABLED timer READ does not clear",
		    h->pending_timer_interrupts[0], 2);
		h->timer_control[0] = 0;

		/*  WIDTH.  `&& len == 4` sweeps every row above -- they all use a
		    four-byte access.  The same shape as the wdc detector's own width
		    hole, found the same day in a different file.  */
		h->pending_timer_interrupts[0] = 2;
		memset(buf, 0xff, sizeof(buf));
		dev_footbridge_access(cpu, NULL, TIMER_1_CLEAR, buf, 2, MEM_READ, h);
		check_u("a 2-byte READ does not clear either",
		    h->pending_timer_interrupts[0], 2);

		/*  *** THE ANCHOR ROWS, and the premise they correct is mine. ***
		    This round's record said 'every row exercises timer 1'.  It does
		    not: TIMER_1_CLEAR is 0x30C and (0x30C >> 5) & 3 == 0, so every
		    row above is an INDEX-0 row.  That is exactly why `timer_nr = 0`
		    and a widened fold mask each score a clean sweep -- the file
		    claims FOUR addresses and carried no row distinguishing any of
		    them.

		    0x32C selects index 1 and 0x36C index 3.  Asserting the NEIGHBOUR
		    is untouched is what makes these ANCHORED rather than merely
		    distinct: a re-map that collides on one probed cell still reds.
		    */
		h->pending_timer_interrupts[0] = 5;
		h->pending_timer_interrupts[1] = 2;
		memset(buf, 0, sizeof(buf));
		dev_footbridge_access(cpu, NULL, TIMER_2_CLEAR, buf, 4, MEM_WRITE, h);
		check_u("0x32C decrements timer index 1",
		    h->pending_timer_interrupts[1], 1);
		check_u("...and leaves index 0 untouched",
		    h->pending_timer_interrupts[0], 5);

		h->pending_timer_interrupts[3] = 2;
		memset(buf, 0, sizeof(buf));
		dev_footbridge_access(cpu, NULL, TIMER_4_CLEAR, buf, 4, MEM_WRITE, h);
		check_u("0x36C decrements timer index 3",
		    h->pending_timer_interrupts[3], 1);
		check_u("...and index 0 is still untouched",
		    h->pending_timer_interrupts[0], 5);

		/*  A READ AT A NON-ZERO INDEX, and it is the row the anchor pair
		    above could not be: those drive WRITES, so a guard widened by
		    `|| timer_nr != 0` passes them for the ordinary reason and
		    nothing reds.  MEASURED: that mutant escaped the 32-row table
		    until this row existed.

		    The general shape is worth naming: an ANCHOR row proves WHICH
		    cell an access lands on, and a GUARD row proves the access is
		    refused.  A mutant that widens the guard per-index needs both
		    properties in ONE row, and neither existing row had them.  */
		h->pending_timer_interrupts[1] = 2;
		memset(buf, 0xff, sizeof(buf));
		dev_footbridge_access(cpu, NULL, TIMER_2_CLEAR, buf, 4, MEM_READ, h);
		check_u("a READ at index 1 does not clear",
		    h->pending_timer_interrupts[1], 2);

		/*  THE COMMON TAIL, and it is the row the fix's own comment needed.
		    That comment says the `break` is deliberate because an early
		    `return` would skip
		        if (writeflag == MEM_READ)
		                memory_writemax64(cpu, data, len, odata);
		    and hand a guest an untouched buffer.  Nothing tested that: buf was
		    memset to 0xff and never read, so `break` -> `return 1` passed both
		    rows.  A stated rationale with no row behind it is a claim, not a
		    property.  Same access as the row above -- the question is what that
		    call LEFT IN THE BUFFER, not what it did to the device.

		    Zero is the tail writing an untouched odata, which is also what the
		    pre-fix code returned; the datasheet specifies no read value for a
		    write-only register, so this pins DETERMINISM, not architecture.  */
		back = memory_readmax64(cpu, buf, 4);
		check_u("a READ still runs the common tail", back, 0);

		/*  PERIODIC READ.  The rows above use control = 0, so the periodic arm
		    of the guarded body never runs and a guard widened to admit a
		    periodic read still passes them.  reload_timer_value() assigns
		    timer_value = timer_load, so a value deliberately UNEQUAL to load
		    makes the reload observable with no clock and no tick.

		    This is the clause-(d) row for this fix: it keeps the guard and
		    nulls its repair on the one path the other rows cannot reach.  */
		h->timer_control[0] = TIMER_MODE_PERIODIC;
		h->timer_load[0]    = 0x1234;
		h->timer_value[0]   = 0x9999;	/*  deliberately != load  */
		h->pending_timer_interrupts[0] = 2;
		memset(buf, 0xff, sizeof(buf));
		dev_footbridge_access(cpu, NULL, TIMER_1_CLEAR, buf, 4, MEM_READ, h);
		check_u("a PERIODIC read must not reload the counter",
		    h->timer_value[0], 0x9999);
		check_u("a PERIODIC read must not clear pending either",
		    h->pending_timer_interrupts[0], 2);

		free(h);
	}

	/*
	 *  #545 P-ROWS -- the five undefined-direction accesses that used to end the process are
	 *  DECLINED with a latched announce.  These rows pin what no stepped guest can (the guest
	 *  rows live in footbridge_sites_probe.py, arm S): PRESERVATION under a NONZERO status, the
	 *  read EXPRESSIONS, the widths, and the latch -- fatal() is a counter here, so the announce
	 *  is counted, never read (the misname check is the guest rows' job).
	 *
	 *  SEEDED BY DIRECT FIELD WRITE, NEVER THROUGH +0x188/+0x18c.  A bare calloc'd instance has
	 *  NULL d->irq callbacks and the enable arms call INTERRUPT_ASSERT(d->irq), so this block
	 *  installs counting no-ops FIRST; the seeds are still written directly, so that no enable-
	 *  arm assert is mixed into the interrupt-output counts the rows below compare.
	 *  Seeds (enumerated, pass 2): 0x18/0x30/0x60/0xc0 -- every field-for-field swap in either
	 *  status expression yields a DIFFERENT value (0x50 collided: 0x50 & 0x30 == 0x18 & 0x30).
	 *  fiq_status has no writer in the product; seeding it pins the +0x280/+0x284 expressions
	 *  against a value the product never produces -- a NARROWING of that gap, not its closure.
	 */
	{
		struct footbridge_data *h = calloc(1, sizeof(struct footbridge_data));
		unsigned char buf[8];
		char nm[96], nm2[128];
		int f0, i;
		static const struct { uint64_t addr; int wf; int len; const char *what; } dec[] = {
			{ IRQ_STATUS,       MEM_WRITE, 4, "P1 write IRQ_STATUS"       },
			{ IRQ_RAW_STATUS,   MEM_WRITE, 4, "P2 write IRQ_RAW_STATUS"   },
			{ IRQ_ENABLE_CLEAR, MEM_READ,  4, "P3 read IRQ_ENABLE_CLEAR"  },
			{ FIQ_STATUS,       MEM_WRITE, 4, "P4 write FIQ_STATUS"       },
			{ FIQ_RAW_STATUS,   MEM_WRITE, 4, "P5 write FIQ_RAW_STATUS"   },
		};
		arm_irqs(h);
		h->irq.interrupt_assert = noop_assert;
		h->irq.interrupt_deassert = noop_deassert;
		/*  seeds chosen so MASKED != RAW: a dropped `&` (raw returned as status) reds P0  */
		h->irq_status = 0x18;  h->irq_enable = 0x30;	/*  masked 0x10, raw 0x18  */
		h->fiq_status = 0x60;  h->fiq_enable = 0xc0;	/*  masked 0x40, raw 0x60  */
		fatal_calls = 0;	/*  this block counts announces from a clean baseline  */
#define P_STATE_OK(tag) do { \
		snprintf(nm2, sizeof(nm2), "%s -- irq_status preserved", tag); check_u(nm2, h->irq_status, 0x18); \
		snprintf(nm2, sizeof(nm2), "%s -- irq_enable preserved", tag); check_u(nm2, h->irq_enable, 0x30); \
		snprintf(nm2, sizeof(nm2), "%s -- fiq_status preserved", tag); check_u(nm2, h->fiq_status, 0x60); \
		snprintf(nm2, sizeof(nm2), "%s -- fiq_enable preserved", tag); check_u(nm2, h->fiq_enable, 0xc0); } while (0)
#define PN(suffix) (snprintf(nm, sizeof(nm), "%s: %s", dec[i].what, suffix), nm)
		/*  the legal reads FIRST, on the seeded state: the expressions, not a constant 0  */
		memset(buf, 0, sizeof(buf));
		dev_footbridge_access(cpu, NULL, IRQ_STATUS, buf, 4, MEM_READ, h);
		check_u("P0 IRQ_STATUS read = irq_status & irq_enable (0x10)", memory_readmax64(cpu, buf, 4), 0x10);
		dev_footbridge_access(cpu, NULL, IRQ_RAW_STATUS, buf, 4, MEM_READ, h);
		check_u("P0 IRQ_RAW_STATUS read = irq_status (0x18)", memory_readmax64(cpu, buf, 4), 0x18);
		dev_footbridge_access(cpu, NULL, FIQ_STATUS, buf, 4, MEM_READ, h);
		check_u("P0 FIQ_STATUS read = fiq_status & fiq_enable (0x40)", memory_readmax64(cpu, buf, 4), 0x40);
		dev_footbridge_access(cpu, NULL, FIQ_RAW_STATUS, buf, 4, MEM_READ, h);
		check_u("P0 FIQ_RAW_STATUS read = fiq_status (0x60)", memory_readmax64(cpu, buf, 4), 0x60);
		check_u("P0 the legal reads announce nothing", fatal_calls, 0);
		for (i = 0; i < 5; i++) {
			int a0 = irq_asserts, d0 = irq_deasserts, rv;
			f0 = fatal_calls;
			memory_writemax64(cpu, buf, 4, 0x70);	/*  bits in BOTH enables: 0x70&0x30=0x30, 0x70&0xc0=0x40  */
			rv = dev_footbridge_access(cpu, NULL, dec[i].addr, buf, dec[i].len, dec[i].wf, h);
			check_u(PN("handler returned 1 (declined, not failed)"), rv, 1);
			check_u(PN("announced exactly once"), fatal_calls - f0, 1);
			if (dec[i].wf == MEM_READ)
				check_u(PN("the declined read returns 0"), memory_readmax64(cpu, buf, 4), 0);
			P_STATE_OK(PN("after #1"));
			check_u(PN("interrupt output untouched"), (irq_asserts - a0) + (irq_deasserts - d0), 0);
			f0 = fatal_calls;
			memory_writemax64(cpu, buf, 4, 0x70);
			dev_footbridge_access(cpu, NULL, dec[i].addr, buf, dec[i].len, dec[i].wf, h);
			check_u(PN("#2 announced nothing more (latched)"), fatal_calls - f0, 0);
			memory_writemax64(cpu, buf, 4, 0x70);
			dev_footbridge_access(cpu, NULL, dec[i].addr, buf, 1, dec[i].wf, h);
			memory_writemax64(cpu, buf, 4, 0x70);
			dev_footbridge_access(cpu, NULL, dec[i].addr, buf, 2, dec[i].wf, h);
			check_u(PN("byte and halfword accesses: still latched"), fatal_calls - f0, 0);
			P_STATE_OK(PN("after #2, byte, halfword"));
		}
		/*  the latches are per SITE: five accesses, five announces, none shared  */
		check_u("P6 five sites announced five times in one instance", fatal_calls, 5);
		/*  a legal read after the declines still reads the seeded expressions  */
		dev_footbridge_access(cpu, NULL, IRQ_STATUS, buf, 4, MEM_READ, h);
		check_u("P7 IRQ_STATUS read after the declines (0x10)", memory_readmax64(cpu, buf, 4), 0x10);
		dev_footbridge_access(cpu, NULL, FIQ_RAW_STATUS, buf, 4, MEM_READ, h);
		check_u("P7 FIQ_RAW_STATUS read after the declines (0x60)", memory_readmax64(cpu, buf, 4), 0x60);
		/*  a LEGAL EnableClear write still works, next to the declined read of the same address  */
		memory_writemax64(cpu, buf, 4, 0x10);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, buf, 4, MEM_WRITE, h);
		check_u("P8 legal EnableClear write: 0x30 & ~0x10", h->irq_enable, 0x20);
		check_u("P8 ... announced nothing", fatal_calls, 5);
#undef PN
#undef P_STATE_OK
		free(h);
		/*  P9: a FRESH instance whose FIRST access to a site is a BYTE write.  A decline that fires only
		    for len == 4 would let the byte fall through silently -- indistinguishable above, where the
		    word access had already latched the site.  Here it must announce.  */
		h = calloc(1, sizeof(struct footbridge_data));
		arm_irqs(h);
		h->irq.interrupt_assert = noop_assert;
		h->irq.interrupt_deassert = noop_deassert;
		h->irq_status = 0x18;  h->irq_enable = 0x30;
		fatal_calls = 0;
		memory_writemax64(cpu, buf, 1, 0x70);
		dev_footbridge_access(cpu, NULL, IRQ_STATUS, buf, 1, MEM_WRITE, h);
		check_u("P9 a BYTE write as the first access is declined AND announced", fatal_calls, 1);
		check_u("P9 ... and stores nothing", h->irq_status, 0x18);
		free(h);
		fatal_calls = 0;
	}

	/*  #545 pass 2 (L2 floor repair, measured by the Opus seat): the P-rows above pinned width and latch at ONE site
	    each, so a `len == 4` conjunct on any of the other four decline guards, a legal read that re-arms a latch, and
	    a decline guard widened to swallow a LEGAL narrow read all passed every row.  X1: every site at len 1 and 2 as
	    the FIRST access announces once (and the narrow declined read returns 0).  X2: legal narrow reads of the
	    five readable registers return the low lanes and announce nothing.  X3: legal reads of every sibling at every
	    width, legal enable writes, and reads of other registers re-arm NO latch.  X4/X5 (pass 2, codex): ZERO data
	    or a zero enable as the first access still declines AND announces; a legal zero Clear write does not.  */
	{
		static const struct { uint64_t addr; int wf; const char *what; } s5[] = {
			{ IRQ_STATUS, MEM_WRITE, "X1 write IRQ_STATUS" }, { IRQ_RAW_STATUS, MEM_WRITE, "X1 write IRQ_RAW_STATUS" },
			{ IRQ_ENABLE_CLEAR, MEM_READ, "X1 read IRQ_ENABLE_CLEAR" }, { FIQ_STATUS, MEM_WRITE, "X1 write FIQ_STATUS" },
			{ FIQ_RAW_STATUS, MEM_WRITE, "X1 write FIQ_RAW_STATUS" } };
		static const struct { uint64_t addr; uint64_t want; const char *what; } rd5[] = {
			{ IRQ_STATUS, 0x10, "IRQ_STATUS" }, { IRQ_RAW_STATUS, 0x18, "IRQ_RAW_STATUS" },
			{ FIQ_STATUS, 0x40, "FIQ_STATUS" }, { FIQ_RAW_STATUS, 0x60, "FIQ_RAW_STATUS" },
			{ IRQ_ENABLE_SET, 0x30, "IRQ_ENABLE_SET" } };
		unsigned char b[8];
		char xn[160];
		int i, w, f0;
		struct footbridge_data *x;
#define XSEED(x) do { arm_irqs(x); (x)->irq.interrupt_assert = noop_assert; (x)->irq.interrupt_deassert = noop_deassert; \
		(x)->irq_status = 0x18; (x)->irq_enable = 0x30; (x)->fiq_status = 0x60; (x)->fiq_enable = 0xc0; } while (0)
		for (w = 1; w <= 2; w++)
			for (i = 0; i < 5; i++) {
				x = calloc(1, sizeof(*x)); XSEED(x);
				fatal_calls = 0;
				memory_writemax64(cpu, b, w, 0x70);
				dev_footbridge_access(cpu, NULL, s5[i].addr, b, w, s5[i].wf, x);
				snprintf(xn, sizeof(xn), "%s: len %d as the FIRST access announces once", s5[i].what, w);
				check_u(xn, fatal_calls, 1);
				if (s5[i].wf == MEM_READ) {	/*  the narrow declined read's VALUE (pass 2)  */
					snprintf(xn, sizeof(xn), "X1 read IRQ_ENABLE_CLEAR: len %d declined read returns 0", w);
					check_u(xn, memory_readmax64(cpu, b, w), 0);
				}
				free(x);
			}
		x = calloc(1, sizeof(*x)); XSEED(x);
		fatal_calls = 0;
		for (w = 1; w <= 2; w++)
			for (i = 0; i < 5; i++) {
				memset(b, 0, sizeof(b));
				dev_footbridge_access(cpu, NULL, rd5[i].addr, b, w, MEM_READ, x);
				snprintf(xn, sizeof(xn), "X2 legal len %d read of %s = low lanes", w, rd5[i].what);
				check_u(xn, memory_readmax64(cpu, b, w), rd5[i].want & (w == 1 ? 0xff : 0xffff));
			}
		check_u("X2 the legal narrow reads announce nothing", fatal_calls, 0);
		for (i = 0; i < 5; i++) {
			memory_writemax64(cpu, b, 4, 0x70);
			dev_footbridge_access(cpu, NULL, s5[i].addr, b, 4, s5[i].wf, x);
		}
		check_u("X3 the five declines latch (5 announces)", fatal_calls, 5);
		f0 = fatal_calls;
		for (w = 1; w <= 4; w *= 2)
			for (i = 0; i < 5; i++)
				dev_footbridge_access(cpu, NULL, rd5[i].addr, b, w, MEM_READ, x);
		for (i = 0; i < 5; i++) {
			memory_writemax64(cpu, b, 4, 0x70);
			dev_footbridge_access(cpu, NULL, s5[i].addr, b, 4, s5[i].wf, x);
		}
		check_u("X3 legal reads of every sibling re-arm NO latch", fatal_calls - f0, 0);
		/*  X3, widened (pass 2): legal WRITES to the four enable registers, and reads of registers outside the
		    five above (VENDOR_ID, TIMER_1_VALUE, the silent FIQEnableClear read), re-arm no latch either.  */
		f0 = fatal_calls;
		memory_writemax64(cpu, b, 4, 0);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_SET, b, 4, MEM_WRITE, x);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		dev_footbridge_access(cpu, NULL, FIQ_ENABLE_SET, b, 4, MEM_WRITE, x);
		dev_footbridge_access(cpu, NULL, FIQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		dev_footbridge_access(cpu, NULL, VENDOR_ID, b, 4, MEM_READ, x);
		dev_footbridge_access(cpu, NULL, TIMER_1_VALUE, b, 4, MEM_READ, x);
		dev_footbridge_access(cpu, NULL, FIQ_ENABLE_CLEAR, b, 4, MEM_READ, x);
		for (i = 0; i < 5; i++) {
			memory_writemax64(cpu, b, 4, 0x70);
			dev_footbridge_access(cpu, NULL, s5[i].addr, b, 4, s5[i].wf, x);
		}
		check_u("X3 legal ZERO-data enable writes and other-register reads re-arm NO latch", fatal_calls - f0, 0);
		free(x);
		/*  X4 (codex, pass 2): the FIRST access carries ZERO -- a zero-data write, or the +0x18c read with
		    IRQEnable 0.  A latch guard conditioned on the data (`&& idata`), a +0x18c guard conditioned on
		    irq_enable, or a direction test rewritten as `!idata`, lets such an access through without an
		    announce; each must announce once and change no field.  (A WRITE-site guard conditioned on an
		    enable -- X4 keeps the seeded enables there -- is X6's all-zero-state cells, not X4's.)  */
		for (i = 0; i < 5; i++) {
			x = calloc(1, sizeof(*x)); XSEED(x);
			if (s5[i].wf == MEM_READ)
				x->irq_enable = 0;
			fatal_calls = 0;
			memory_writemax64(cpu, b, 4, 0);
			dev_footbridge_access(cpu, NULL, s5[i].addr, b, 4, s5[i].wf, x);
			snprintf(xn, sizeof(xn), "X4 %s: ZERO data/enable as the FIRST access announces once", s5[i].what + 3);
			check_u(xn, fatal_calls, 1);
			snprintf(xn, sizeof(xn), "X4 %s: ZERO data/enable changes no field", s5[i].what + 3);
			check_u(xn, (x->irq_status == 0x18) + (x->irq_enable == (s5[i].wf == MEM_READ ? 0u : 0x30u))
			    + (x->fiq_status == 0x60) + (x->fiq_enable == 0xc0), 4);
			free(x);
		}
		/*  X5 (codex, pass 2): a LEGAL ZERO EnableClear write is a write, not a declined read -- a direction test
		    rewritten as `idata` sends it to the decline and announces.  */
		x = calloc(1, sizeof(*x)); XSEED(x);
		fatal_calls = 0;
		memory_writemax64(cpu, b, 4, 0);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		check_u("X5 a legal ZERO EnableClear write announces nothing", fatal_calls, 0);
		check_u("X5 ... and leaves IRQEnable at 0x30", x->irq_enable, 0x30);
#undef XSEED
		free(x);
		fatal_calls = 0;
	}

	/*
	 *  #545 CLASS CLOSURE (repair pass 2 -- two consecutive passes found breaches of ONE class, so the
	 *  whole space is enumerated from the handler's own inputs and closed in one block; carrier rule).
	 *
	 *  X6: EVERY DECLINED ACCESS -- site (5) x width (1, 2, 4) x data (zero, nonzero; writes only) x state
	 *      (seeded, all-zero, wide) x occurrence (first, repeated).  Each cell, as ONE row, requires: the handler
	 *      returns 1; the announce count moves by exactly 1 on the first access and 0 on the repeat; all four
	 *      register fields are unchanged; the interrupt output is untouched (no assert, no deassert); and a
	 *      declined read returns 0 over its whole width.
	 *  X7: EVERY LEGAL ACCESS RE-ARMS NO LATCH -- with all five sites latched: each enable write (Set/Clear,
	 *      IRQ/FIQ) with zero and nonzero data, and each legal read of the readable registers plus VENDOR_ID
	 *      and TIMER_1_VALUE at widths 1, 2 and 4; from the seeded, all-zero and wide states (so a read that
	 *      returns 0 is covered, and so is a field bit above byte 0).  After each, re-declining all five sites
	 *      must announce nothing.
	 *  X9 (below X8) is the other half of the legal side: every legal access with the latches still CLEAR.
	 *
	 *  CONTRACT (clause e): the class is ACCESS (declined, legal) x STATE (seeded, all-zero, wide) x LATCH
	 *  (clear, set) at these five sites -- declined x both latches in X6, legal x set in X7, legal x clear in
	 *  X9.  *** THIS SAID "the cells above are the whole class" UNTIL THE ADJUDICATION PASS OF 2026-09-23, AND
	 *  IT WAS MEASURED FALSE: X7 latched every site BEFORE its legal access, so LEGAL x ALL-ZERO x LATCH-CLEAR
	 *  -- the reset state -- had no row, and five one-conjunct edits to the DIRECTION test (`writeflag ==
	 *  MEM_READ && d->irq_enable` and its mirrors) passed all 333 rows here and all 37 guest rows
	 *  (regress/artifacts/fbd5/q2_20260923/Q2.log). ***  The DEPENDS-ON bound these rows use: the predicates
	 *  dominating each edited decline (case label, direction test, latch), and the lvalues read by BOTH
	 *  branches under the direction test -- the four interrupt fields and the five latches.  Not in the
	 *  class: the interrupt output after a LEGAL access except where X9 pins it, any other register's
	 *  semantics, WIDE DATA on a declined write (data stays 0 / 0x70), joint conjuncts over two fields
	 *  beyond the three states, and a latch guard conditioned on a field neither branch reads (measured F1:
	 *  `&& !timer_control[0]` passes every row here; the guest sites probe catches it only because its
	 *  prologue arms timer 1; table4_20260919).
	 */
	{
		static const struct { uint64_t addr; int wf; const char *nm; } S5[] = {
			{ IRQ_STATUS, MEM_WRITE, "write IRQ_STATUS" }, { IRQ_RAW_STATUS, MEM_WRITE, "write IRQ_RAW_STATUS" },
			{ IRQ_ENABLE_CLEAR, MEM_READ, "read IRQ_ENABLE_CLEAR" }, { FIQ_STATUS, MEM_WRITE, "write FIQ_STATUS" },
			{ FIQ_RAW_STATUS, MEM_WRITE, "write FIQ_RAW_STATUS" } };
		/*  #545 adjudication (Fable 5.1, Q2 (e) cell): the byte seeds left bits 8-31 of every field unexercised,
		    so a decline store or a latch clearer keyed on them passed every row.  "wide" is X8's seeds.  */
		static const struct { uint32_t is, ie, fs, fe; const char *nm; } ST[3] = {
			{ 0x18, 0x30, 0x60, 0xc0, "seeded" }, { 0, 0, 0, 0, "all-zero" },
			{ 0x80010018, 0x00010030, 0x40020060, 0x000200c0, "wide" } };
		static const int W[3] = { 1, 2, 4 };
		static const struct { uint64_t addr; int wf; uint64_t data; const char *nm; } LW[8] = {
			{ IRQ_ENABLE_SET, MEM_WRITE, 0, "IRQ Set write 0" }, { IRQ_ENABLE_SET, MEM_WRITE, 0x70, "IRQ Set write 0x70" },
			{ IRQ_ENABLE_CLEAR, MEM_WRITE, 0, "IRQ Clear write 0" }, { IRQ_ENABLE_CLEAR, MEM_WRITE, 0x70, "IRQ Clear write 0x70" },
			{ FIQ_ENABLE_SET, MEM_WRITE, 0, "FIQ Set write 0" }, { FIQ_ENABLE_SET, MEM_WRITE, 0x70, "FIQ Set write 0x70" },
			{ FIQ_ENABLE_CLEAR, MEM_WRITE, 0, "FIQ Clear write 0" }, { FIQ_ENABLE_CLEAR, MEM_WRITE, 0x70, "FIQ Clear write 0x70" } };
		static const struct { uint64_t addr; const char *nm; } LR[9] = {
			{ IRQ_STATUS, "IRQ_STATUS" }, { IRQ_RAW_STATUS, "IRQ_RAW_STATUS" }, { FIQ_STATUS, "FIQ_STATUS" },
			{ FIQ_RAW_STATUS, "FIQ_RAW_STATUS" }, { IRQ_ENABLE_SET, "IRQ_ENABLE_SET" }, { FIQ_ENABLE_SET, "FIQ_ENABLE_SET" },
			{ FIQ_ENABLE_CLEAR, "FIQ_ENABLE_CLEAR" }, { VENDOR_ID, "VENDOR_ID" }, { TIMER_1_VALUE, "TIMER_1_VALUE" } };
		unsigned char b[8];
		char xn[200];
		int si, st, wi, dv, ord, k, f0, a0, d0, rv, ok;
		struct footbridge_data *x;
#define XSET(x, s) do { arm_irqs(x); (x)->irq.interrupt_assert = noop_assert; (x)->irq.interrupt_deassert = noop_deassert; \
		(x)->irq_status = ST[s].is; (x)->irq_enable = ST[s].ie; (x)->fiq_status = ST[s].fs; (x)->fiq_enable = ST[s].fe; } while (0)
#define XSAME(x, s) ((x)->irq_status == ST[s].is && (x)->irq_enable == ST[s].ie && (x)->fiq_status == ST[s].fs \
		&& (x)->fiq_enable == ST[s].fe)
		for (si = 0; si < 5; si++)
			for (st = 0; st < 3; st++)
				for (wi = 0; wi < 3; wi++)
					for (dv = 0; dv < (S5[si].wf == MEM_WRITE ? 2 : 1); dv++) {
						x = calloc(1, sizeof(*x)); XSET(x, st);
						fatal_calls = 0;
						for (ord = 0; ord < 2; ord++) {
							a0 = irq_asserts; d0 = irq_deasserts; f0 = fatal_calls;
							memset(b, 0xa5, sizeof(b));
							if (S5[si].wf == MEM_WRITE)
								memory_writemax64(cpu, b, W[wi], dv ? 0x70 : 0);
							rv = dev_footbridge_access(cpu, NULL, S5[si].addr, b, W[wi], S5[si].wf, x);
							ok = rv == 1 && fatal_calls - f0 == (ord == 0 ? 1 : 0) && XSAME(x, st)
							    && irq_asserts == a0 && irq_deasserts == d0
							    && (S5[si].wf != MEM_READ || memory_readmax64(cpu, b, W[wi]) == 0);
							snprintf(xn, sizeof(xn), "X6 %s len %d %s %s %s: declined, fields/irq kept, once",
							    S5[si].nm, W[wi], S5[si].wf == MEM_WRITE ? (dv ? "data 0x70" : "data 0") : "",
							    ST[st].nm, ord ? "repeat" : "first");
							check_u(xn, ok, 1);
						}
						free(x);
					}
		for (st = 0; st < 3; st++)
			for (k = 0; k < 8 + 9 * 3; k++) {
				x = calloc(1, sizeof(*x)); XSET(x, st);
				for (si = 0; si < 5; si++) {
					memory_writemax64(cpu, b, 4, 0x70);
					dev_footbridge_access(cpu, NULL, S5[si].addr, b, 4, S5[si].wf, x);
				}
				f0 = fatal_calls;
				if (k < 8) {
					memory_writemax64(cpu, b, 4, LW[k].data);
					dev_footbridge_access(cpu, NULL, LW[k].addr, b, 4, MEM_WRITE, x);
					snprintf(xn, sizeof(xn), "X7 %s (%s) re-arms NO latch", LW[k].nm, ST[st].nm);
				} else {
					int r = (k - 8) / 3, w = W[(k - 8) % 3];
					memset(b, 0, sizeof(b));
					dev_footbridge_access(cpu, NULL, LR[r].addr, b, w, MEM_READ, x);
					snprintf(xn, sizeof(xn), "X7 legal len %d read of %s (%s) re-arms NO latch", w, LR[r].nm, ST[st].nm);
				}
				for (si = 0; si < 5; si++) {
					memory_writemax64(cpu, b, 4, 0x70);
					dev_footbridge_access(cpu, NULL, S5[si].addr, b, 4, S5[si].wf, x);
				}
				check_u(xn, fatal_calls - f0, 0);
				free(x);
			}
#undef XSAME
#undef XSET
		fatal_calls = 0;
	}
	/*  X8 (adjudication pass, G11): every seed above fits in ONE byte, so a legal read truncated to 8 bits
	    passed every row.  Wide seeds, bits in every byte lane that matters: each legal word read returns its
	    full 32-bit value (the masked reads: 0x80010018 & 0x00010030 = 0x00010010, 0x40020060 & 0x000200c0 =
	    0x00020040).  */
	{
		struct footbridge_data *x = calloc(1, sizeof(*x));
		unsigned char b[8];
		arm_irqs(x);
		x->irq.interrupt_assert = noop_assert;
		x->irq.interrupt_deassert = noop_deassert;
		x->irq_status = 0x80010018;  x->irq_enable = 0x00010030;
		x->fiq_status = 0x40020060;  x->fiq_enable = 0x000200c0;
		fatal_calls = 0;
		memset(b, 0, sizeof(b));
		dev_footbridge_access(cpu, NULL, IRQ_STATUS, b, 4, MEM_READ, x);
		check_u("X8 wide IRQ_STATUS read = 0x00010010 (all 32 bits)", memory_readmax64(cpu, b, 4), 0x00010010);
		dev_footbridge_access(cpu, NULL, IRQ_RAW_STATUS, b, 4, MEM_READ, x);
		check_u("X8 wide IRQ_RAW_STATUS read = 0x80010018", memory_readmax64(cpu, b, 4), 0x80010018);
		dev_footbridge_access(cpu, NULL, FIQ_STATUS, b, 4, MEM_READ, x);
		check_u("X8 wide FIQ_STATUS read = 0x00020040", memory_readmax64(cpu, b, 4), 0x00020040);
		dev_footbridge_access(cpu, NULL, FIQ_RAW_STATUS, b, 4, MEM_READ, x);
		check_u("X8 wide FIQ_RAW_STATUS read = 0x40020060", memory_readmax64(cpu, b, 4), 0x40020060);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_SET, b, 4, MEM_READ, x);
		check_u("X8 wide IRQEnable read = 0x00010030", memory_readmax64(cpu, b, 4), 0x00010030);
		check_u("X8 the wide legal reads announce nothing", fatal_calls, 0);
		free(x);
		fatal_calls = 0;
	}
	/*  X9 (adjudication pass, 2026-09-23 -- Fable 5.1's Q2, MEASURED before this block existed): EVERY LEGAL
	    ACCESS WITH THE LATCHES STILL CLEAR, from each state.  X7 latched all five sites before its legal access,
	    so a direction test conjoined with a field that is 0 in the RESET state (`writeflag == MEM_READ &&
	    d->irq_enable` at IRQ_STATUS, its three read mirrors, `writeflag == MEM_WRITE && d->irq_enable` at
	    IRQEnableClear) sent the legal access into the decline, which announced a phantom complaint, consumed the
	    latch and returned 0 -- the right value in that state -- and every row stayed green
	    (regress/artifacts/fbd5/q2_20260923/Q2.log: 333/333 and 37/37 for all five).  Each cell is ONE row on a
	    fresh instance: the access returns 1 and announces nothing; a read returns its value over the width and
	    changes no field; a write sets the enable it targets as written and leaves the other three alone, and IRQ
	    Set/Clear drive the interrupt output exactly once by (irq_status & the new enable) while FIQ Set/Clear do
	    not touch it; then the five declines announce EXACTLY 5, because no latch was consumed.  */
	{
		static const struct { uint32_t is, ie, fs, fe; const char *nm; } S9[3] = {
			{ 0x18, 0x30, 0x60, 0xc0, "seeded" }, { 0, 0, 0, 0, "all-zero" },
			{ 0x80010018, 0x00010030, 0x40020060, 0x000200c0, "wide" } };
		static const struct { uint64_t addr; int wf; } D5[5] = {
			{ IRQ_STATUS, MEM_WRITE }, { IRQ_RAW_STATUS, MEM_WRITE }, { IRQ_ENABLE_CLEAR, MEM_READ },
			{ FIQ_STATUS, MEM_WRITE }, { FIQ_RAW_STATUS, MEM_WRITE } };
		static const struct { uint64_t addr; const char *nm; } R5[5] = {
			{ IRQ_STATUS, "IRQ_STATUS" }, { IRQ_RAW_STATUS, "IRQ_RAW_STATUS" }, { FIQ_STATUS, "FIQ_STATUS" },
			{ FIQ_RAW_STATUS, "FIQ_RAW_STATUS" }, { IRQ_ENABLE_SET, "IRQEnable" } };
		static const struct { uint64_t addr; int fiq, set; uint32_t data; const char *nm; } W8[8] = {
			{ IRQ_ENABLE_SET, 0, 1, 0, "IRQ Set write 0" }, { IRQ_ENABLE_SET, 0, 1, 0x70, "IRQ Set write 0x70" },
			{ IRQ_ENABLE_CLEAR, 0, 0, 0, "IRQ Clear write 0" }, { IRQ_ENABLE_CLEAR, 0, 0, 0x70, "IRQ Clear write 0x70" },
			{ FIQ_ENABLE_SET, 1, 1, 0, "FIQ Set write 0" }, { FIQ_ENABLE_SET, 1, 1, 0x70, "FIQ Set write 0x70" },
			{ FIQ_ENABLE_CLEAR, 1, 0, 0, "FIQ Clear write 0" }, { FIQ_ENABLE_CLEAR, 1, 0, 0x70, "FIQ Clear write 0x70" } };
		static const int W9[3] = { 1, 2, 4 };
		unsigned char b[8];
		char xn[200];
		int st, k, si, a0, d0, rv, ok;
		struct footbridge_data *x;
		for (st = 0; st < 3; st++)
			for (k = 0; k < 5 * 3 + 8; k++) {
				uint32_t is = S9[st].is, ie = S9[st].ie, fs = S9[st].fs, fe = S9[st].fe;
				x = calloc(1, sizeof(*x));
				arm_irqs(x);
				x->irq.interrupt_assert = noop_assert;
				x->irq.interrupt_deassert = noop_deassert;
				x->irq_status = is;  x->irq_enable = ie;  x->fiq_status = fs;  x->fiq_enable = fe;
				fatal_calls = 0;
				a0 = irq_asserts;  d0 = irq_deasserts;
				if (k < 15) {
					int r = k / 3, w = W9[k % 3];
					uint64_t want = r == 0 ? (uint64_t) (is & ie) : r == 1 ? (uint64_t) is
					    : r == 2 ? (uint64_t) (fs & fe) : r == 3 ? (uint64_t) fs : (uint64_t) ie;
					want &= w == 4 ? 0xffffffffULL : w == 2 ? 0xffffULL : 0xffULL;
					memset(b, 0xa5, sizeof(b));
					rv = dev_footbridge_access(cpu, NULL, R5[r].addr, b, w, MEM_READ, x);
					ok = rv == 1 && fatal_calls == 0 && memory_readmax64(cpu, b, w) == want
					    && x->irq_status == is && x->irq_enable == ie && x->fiq_status == fs
					    && x->fiq_enable == fe && irq_asserts == a0 && irq_deasserts == d0;
					snprintf(xn, sizeof(xn), "X9 legal len %d read of %s (%s, latches clear)",
					    w, R5[r].nm, S9[st].nm);
				} else {
					int j = k - 15;
					uint32_t old = W8[j].fiq ? fe : ie;
					uint32_t ne = W8[j].set ? (old | W8[j].data) : (old & ~W8[j].data);
					memory_writemax64(cpu, b, 4, W8[j].data);
					rv = dev_footbridge_access(cpu, NULL, W8[j].addr, b, 4, MEM_WRITE, x);
					ok = rv == 1 && fatal_calls == 0 && x->irq_status == is && x->fiq_status == fs
					    && (W8[j].fiq ? (x->fiq_enable == ne && x->irq_enable == ie)
					                  : (x->irq_enable == ne && x->fiq_enable == fe))
					    && (W8[j].fiq ? (irq_asserts == a0 && irq_deasserts == d0)
					        : (is & ne) ? (irq_asserts == a0 + 1 && irq_deasserts == d0)
					                    : (irq_asserts == a0 && irq_deasserts == d0 + 1));
					snprintf(xn, sizeof(xn), "X9 %s (%s, latches clear)", W8[j].nm, S9[st].nm);
				}
				for (si = 0; si < 5; si++) {
					memory_writemax64(cpu, b, 4, 0x70);
					dev_footbridge_access(cpu, NULL, D5[si].addr, b, 4, D5[si].wf, x);
				}
				ok = ok && fatal_calls == 5;
				check_u(xn, ok, 1);
				free(x);
			}
		fatal_calls = 0;
	}
	/*  IDENTITY, as every differential here carries.  #545: 33 -> 333 (78 P-rows + 222 X-rows); the adjudication
	    pass, 2026-09-23: 333 -> 491 (X6 +54 and X7 +35 for the wide state, X9 69).  */
	{
		char buf[32];
		snprintf(buf, sizeof(buf), "%d", rows + 1);
		check("IDENTITY row count -- guards against a stale copy", buf, "491");
	}

	printf("\n%d rows, %d failures\n", rows, fails);
	printf("DIFF_FOOTBRIDGE_%s\n", fails == 0 ? "PASS" : "FAIL");
	return fails ? 1 : 0;
}
