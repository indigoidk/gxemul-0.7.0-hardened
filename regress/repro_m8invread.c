/*
 *  TEST-FIRST REPRODUCTION for `m8invread`.
 *
 *  THE CLAIM.  dev_m8820x.c:304-314 groups six CMMU registers -- PFSR, PFAR, SAR, SCTR,
 *  SAPR, UAPR -- and calls
 *
 *        c->invalidate_translation_caches(c, 0, INVALIDATE_ALL);
 *
 *  UNCONDITIONALLY, one line ABOVE the `if (writeflag == MEM_WRITE)` that actually stores.
 *  So a plain guest READ of any of the six purges the emulator's entire translation cache.
 *
 *  WHY IT MATTERS RATHER THAN BEING MERELY UNTIDY.  PFSR (fault status) is read by the
 *  fault handler on every fault, so the cost is paid by the ordinary page-fault path.
 *
 *  *** THE COST IS TWICE PER FAULT -- AND GETTING TO THAT SENTENCE TOOK TWO WRONG ONES,
 *  BOTH RECORDED HERE BECAUSE THE PAIR IS MORE INSTRUCTIVE THAN EITHER. ***
 *
 *  Draft 1 said "twice per fault" and reasoned that a handler reads PFSR *and* PFAR.  A
 *  per-register instrumented boot refuted the REASON: PFAR is read ZERO times.
 *
 *  Draft 2 therefore said "once per fault".  That was an OVER-CORRECTION, and a second
 *  seat caught it: PFAR's absence rules out the reason, not the count.  Measured, PFSR is
 *  read 286,519 times and 49.98% of those reads return NONZERO -- almost exactly half.
 *  The mechanism is at memory_m88k.c:382-384, which on every fault sets the faulting
 *  CMMU's PFSR and EXPLICITLY ZEROES THE OTHER ONE'S (CMMU_PFSR_SUCCESS is 0), precisely
 *  so the handler can tell which CMMU faulted.  It must read BOTH.  Hence twice, hence the
 *  half.  Draft 1 had the right number for the wrong reason; draft 2 had the right reason
 *  and the wrong number.  A correction is a claim too, and it needs the same evidence. ***
 *
 *  THIS IS THE SAME CALLBACK whose NULLness corrupted this round's first m8820x
 *  reproduction by exactly six in each direction: the arm fires on READS, the driver left
 *  the pointer NULL, and the resulting segfaults were counted as detections.  That
 *  accident is this defect, seen from the other side -- so the measurement below counts
 *  the callback rather than trusting survival, and installs a real no-op for it.
 *
 *  WHAT IS DELIBERATELY *NOT* CLAIMED.  Nothing here says the purge is WRONG for a write.
 *  SAPR/UAPR are the area pointers and a write to those genuinely does change what
 *  m88k_translate_v2p reads (memory_m88k.c:135,137).  SCTR was named alongside them in an
 *  earlier draft; a pass-2 seat checked and THE CURRENT TRANSLATION PATH NEVER READS SCTR
 *  -- its defined bits are parity, snoop and arbitration controls -- so that is CONFIRMED
 *  for this model and UNKNOWN for silicon.  The existing TODO about narrowing the write
 *  side is a separate, filed question (`m8sarpurge`).  The claim here is only about the
 *  READ side, where nothing has changed.
 */
#include <inttypes.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "include/misc.h"
#include "include/memory.h"
#include "include/machine.h"
#include "include/cpu.h"

bool single_step = false;
bool about_to_enter_single_step = false;
static int verb[16];
int *debugmsg_current_verbosity = verb;

static int fatal_calls, debug_calls;
void fatal(const char *fmt, ...) { (void) fmt; fatal_calls++; }
void debug(const char *fmt, ...) { (void) fmt; debug_calls++; }

uint64_t memory_readmax64(struct cpu *cpu, unsigned char *buf, int len)
{
	uint64_t x = 0; int i;
	(void) cpu;
	for (i = 0; i < len; i++) x |= (uint64_t) buf[i] << (8*i);
	return x;
}
void memory_writemax64(struct cpu *cpu, unsigned char *buf, int len, uint64_t data)
{
	int i; (void) cpu;
	for (i = 0; i < len; i++) buf[i] = (data >> (8*i)) & 255;
}

static int invalidate_calls;
static void noop_invalidate(struct cpu *c, uint64_t a, int flags)
{ (void)c; (void)a; (void)flags; invalidate_calls++; }

#include "../src/devices/dev_m8820x.c"

static struct cpu *cpu;
static struct machine *machine;
static struct m8820x_data dev;
static struct m8820x_cmmu *cmmu;

static int rows, fails;
static void check_u(const char *name, uint64_t got, uint64_t want)
{
	rows++;
	if (got == want)
		printf("  ok    %-58s %" PRIu64 "\n", name, got);
	else {
		fails++;
		printf("  FAIL  %-58s got %" PRIu64 " want %" PRIu64 "\n",
		    name, got, want);
	}
}

static void fresh(void)
{
	memset(cmmu, 0, sizeof(*cmmu));
	memset(&dev, 0, sizeof(dev));
	cmmu->reg[CMMU_IDR] = (M88200_ID << 21) | (9 << 16);
	fatal_calls = debug_calls = invalidate_calls = 0;
}

static uint32_t access_word(uint64_t off, int writeflag, uint32_t val)
{
	unsigned char buf[4];
	memset(buf, 0, sizeof(buf));
	if (writeflag == MEM_WRITE)
		memory_writemax64(cpu, buf, 4, val);
	dev_m8820x_access(cpu, NULL, off, buf, 4, writeflag, &dev);
	return (uint32_t) memory_readmax64(cpu, buf, 4);
}

int main(void)
{
	static const struct { uint32_t reg; const char *nm; } group[] = {
		{ CMMU_PFSR, "PFSR" }, { CMMU_PFAR, "PFAR" }, { CMMU_SAR,  "SAR"  },
		{ CMMU_SCTR, "SCTR" }, { CMMU_SAPR, "SAPR" }, { CMMU_UAPR, "UAPR" },
	};
	size_t i;
	int purges_on_read = 0, purges_on_write = 0;
	uint32_t v;

	setvbuf(stdout, NULL, _IOLBF, 0);
	cpu = calloc(1, sizeof(struct cpu));
	machine = calloc(1, sizeof(struct machine));
	cmmu = calloc(1, sizeof(struct m8820x_cmmu));
	machine->cpus = calloc(1, sizeof(struct cpu *));
	machine->cpus[0] = cpu;
	cpu->machine = machine;
	cpu->cd.m88k.cmmu[0] = cmmu;
	cpu->invalidate_translation_caches = noop_invalidate;

	printf("--- how many full translation-cache purges does a READ cost? ---\n");
	for (i = 0; i < sizeof(group)/sizeof(group[0]); i++) {
		fresh();
		access_word(group[i].reg * 4, MEM_READ, 0);
		printf("      read  %-5s -> %d purge(s)\n", group[i].nm, invalidate_calls);
		purges_on_read += invalidate_calls;
	}
	for (i = 0; i < sizeof(group)/sizeof(group[0]); i++) {
		fresh();
		access_word(group[i].reg * 4, MEM_WRITE, 0x1234);
		purges_on_write += invalidate_calls;
	}

	/*  THE DEFECT ROW.  A read changes no translation, so it owes no purge.  */
	check_u("a READ of the six registers purges the whole cache", purges_on_read, 6);

	/*  THE CONTROL, and it is what stops this being a one-sided reading: the WRITE
	    side is not under test and must be untouched by any fix.  If a fix made this
	    zero too it would have removed a purge that is arguably owed.  */
	check_u("CONTROL: a WRITE still purges (not under test)", purges_on_write, 6);

	/*  A SECOND CONTROL, against the reproduction rather than the code: an offset
	    OUTSIDE the group must not purge at all, or `purges_on_read` would be
	    measuring something ambient rather than this arm.  */
	fresh();
	access_word(CMMU_IDR * 4, MEM_READ, 0);
	check_u("CONTROL: reading IDR (outside the group) purges nothing",
	    invalidate_calls, 0);

	/*  And the read must still RETURN the register, so a later fix cannot pass by
	    turning the read into a no-op.  Seed through the write path first.  */
	fresh();
	access_word(CMMU_SCTR * 4, MEM_WRITE, 0xabcd);
	v = access_word(CMMU_SCTR * 4, MEM_READ, 0);
	check_u("CONTROL: the read still returns the register", v, 0xabcd);

	printf("\n%s\n", fails == 0 ? "REPRO_M8INVREAD_CONFIRMED"
	                            : "REPRO_M8INVREAD_NOT_REPRODUCED");
	printf("%d rows, %d failures\n", rows, fails);
	return 0;
}
