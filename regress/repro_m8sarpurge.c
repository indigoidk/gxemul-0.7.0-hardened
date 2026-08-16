/*
 *  TEST-FIRST REPRODUCTION for `m8sarpurge`.
 *
 *  #434 removed the purge from the READ side of the six-register arm, on the argument that a
 *  read changes no translation so it owes no purge.  This is the same argument applied to the
 *  WRITE side, where it holds for FOUR of the six registers -- and where 98% of the volume is.
 *
 *  WHO ACTUALLY CONSULTS THESE REGISTERS.  Enumerated over all of src/, not sampled:
 *
 *      SAPR   memory_m88k.c:135   read by m88k_translate_v2p (supervisor area pointer)
 *      UAPR   memory_m88k.c:137   read by m88k_translate_v2p (user area pointer)
 *      SAR    dev_m8820x.c:110    read ONCE, as the address operand of a flush COMMAND --
 *                                 and that command's own arm already purges (dev_m8820x.c:187)
 *      PFSR   memory_m88k.c:382,383, dev_luna88k.c:614   WRITTEN by the fault path; never read
 *      PFAR   memory_m88k.c:399,405                      WRITTEN by the fault path; never read
 *      SCTR   -- appears nowhere in src/ outside its own case label.  Never read at all.
 *
 *  So a guest write to SAPR or UAPR genuinely changes what the translator will do, and owes a
 *  purge.  A guest write to SAR, PFSR, PFAR or SCTR cannot change any translation IN THIS MODEL,
 *  and owes nothing -- by exactly #434's argument, pointed at the other half of the same arm.
 *
 *  WHAT THIS FILE MEASURES, AND WHAT IT DELIBERATELY DOES NOT.  It measures the current
 *  behaviour: all six purge on write.  It does NOT attempt to prove the consumer table above
 *  from inside a differential -- that is a whole-source claim, and a grep is the right
 *  instrument for it, run and recorded in the round rather than smuggled into a row.  What the
 *  rows below CAN do is pin the split once it exists, and fail loudly if a later edit moves a
 *  register from one side of it to the other.
 *
 *  CONFIRMED for this model; UNKNOWN for silicon.  There is no 88200/88204 manual in this
 *  project, so nothing here claims what real hardware does on an SCTR write.
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

static int inv_calls;
static void spy_invalidate(struct cpu *c, uint64_t a, int flags)
{ (void)c; (void)a; (void)flags; inv_calls++; }

#include "../src/devices/dev_m8820x.c"

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

static struct cpu *cpu0;
static struct machine *machine;
static struct m8820x_data dev;
static struct m8820x_cmmu *cmmu;

/*  TRUE if the translation path can be affected by a write to this register.  */
static const struct { uint32_t reg; const char *nm; int owes_purge; } GROUP[] = {
	{ CMMU_PFSR, "PFSR", 0 }, { CMMU_PFAR, "PFAR", 0 },
	{ CMMU_SAR,  "SAR",  0 }, { CMMU_SCTR, "SCTR", 0 },
	{ CMMU_SAPR, "SAPR", 1 }, { CMMU_UAPR, "UAPR", 1 },
};
#define NGROUP ((int) (sizeof(GROUP)/sizeof(GROUP[0])))

static void fresh(void)
{
	memset(cmmu, 0, sizeof(*cmmu));
	memset(&dev, 0, sizeof(dev));
	cmmu->reg[CMMU_IDR] = (M88200_ID << 21) | (9 << 16);
	fatal_calls = debug_calls = inv_calls = 0;
}

static void acc(uint64_t off, int writeflag, uint32_t val)
{
	unsigned char buf[4];
	memset(buf, 0, sizeof(buf));
	if (writeflag == MEM_WRITE)
		memory_writemax64(cpu0, buf, 4, val);
	dev_m8820x_access(cpu0, NULL, off, buf, 4, writeflag, &dev);
}

int main(void)
{
	int i, purge_owed = 0, purge_not_owed = 0;

	setvbuf(stdout, NULL, _IOLBF, 0);
	cpu0 = calloc(1, sizeof(struct cpu));
	machine = calloc(1, sizeof(struct machine));
	cmmu = calloc(1, sizeof(struct m8820x_cmmu));
	machine->cpus = calloc(1, sizeof(struct cpu *));
	machine->cpus[0] = cpu0;
	cpu0->machine = machine;
	cpu0->cd.m88k.cmmu[0] = cmmu;
	cpu0->invalidate_translation_caches = spy_invalidate;
	fresh();

	printf("--- which WRITES purge today, split by whether a purge is OWED ---\n");
	for (i = 0; i < NGROUP; i++) {
		fresh();
		acc(GROUP[i].reg * 4, MEM_WRITE, 0x1234 + i);
		printf("      write %-5s -> %d purge(s)   (owed: %s)\n",
		    GROUP[i].nm, inv_calls, GROUP[i].owes_purge ? "yes" : "NO");
		if (GROUP[i].owes_purge) purge_owed += inv_calls;
		else purge_not_owed += inv_calls;
	}

	/*  THE DEFECT ROW.  Four registers no consumer reads, each purging the whole cache.  */
	check_u("writes that purge although NO consumer reads them", purge_not_owed, 4);

	/*  THE CONTROL.  SAPR/UAPR genuinely do change translation and must keep purging;
	    a fix that silenced these too would be over-applying the argument.  */
	check_u("CONTROL: SAPR and UAPR purge, and must go on doing so", purge_owed, 2);

	/*  A control on the reproduction: something outside the arm, so the counts above are
	    this arm and not something ambient.  */
	fresh();
	acc(CMMU_IDR * 4, MEM_WRITE, 1);
	check_u("CONTROL: a write outside the arm purges nothing", inv_calls, 0);

	/*  And the neighbouring flush command must be untouched -- it is the mechanism that
	    actually keeps translation correct, at ~603,000 purges per boot.  */
	fresh();
	acc(CMMU_SCR * 4, MEM_WRITE, CMMU_FLUSH_SUPER_PAGE);
	check_u("CONTROL: an SCR flush command still purges", inv_calls, 1);

	printf("\n%s\n", fails == 0 ? "REPRO_M8SARPURGE_CONFIRMED"
	                            : "REPRO_M8SARPURGE_NOT_REPRODUCED");
	printf("%d rows, %d failures\n", rows, fails);
	return 0;
}
