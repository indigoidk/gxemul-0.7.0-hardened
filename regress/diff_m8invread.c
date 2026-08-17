/*
 *  Offline differential for #434 -- a guest READ of six CMMU registers used to purge the
 *  emulator's entire translation cache.  src/devices/dev_m8820x.c, the REPOSITORY FILE,
 *  #included exactly as diff_m8820x.c includes it.
 *
 *  *** A 1:1:1 RIG BOOT IS NOT EVIDENCE THAT THE REMOVAL IS SAFE, and this round proved
 *  that twice over.  Mutant A boots to `login:`.  So does the read-purge-under-a-value-guard
 *  mutant, which RESTORES HALF the removed purges.  The rig shows the machine still works;
 *  it does not show this property holds.  The support is the semantic argument alone --
 *  none of the six registers is consulted by m88k_translate_v2p on a read (SAPR/UAPR at
 *  memory_m88k.c:135,137 are read but not modified, SAR only at dev_m8820x.c:110, SCTR
 *  nowhere) -- plus the rows below. ***
 *
 *  THE DEFECT.  `c->invalidate_translation_caches(c, 0, INVALIDATE_ALL)` sat one line ABOVE
 *  the `if (writeflag == MEM_WRITE)` that stores, so PFSR, PFAR, SAR, SCTR, SAPR and UAPR
 *  each dropped the whole dyntrans mapping on a plain read.  Measured on the luna88k rig:
 *  291,807 such reads per boot-to-login, 16.5% of every INVALIDATE_ALL in the machine.
 *
 *  *** THE SPY RECORDS ARGUMENTS, NOT JUST A COUNT, AND THAT IS THE WHOLE POINT OF THIS
 *  FILE.  A count-only detector was proposed, reviewed, and BROKEN BY TWO SEATS: ***
 *
 *    mutant A   INVALIDATE_ALL -> INVALIDATE_VADDR.  addr is 0, so cpu_dyntrans.c:1228-1255
 *               invalidates virtual page 0 alone and the write-side purge becomes a
 *               near-no-op -- UNDER-invalidation, the direction dev_m8820x.c names as the
 *               dangerous one.  The call COUNT is bit-identical, so every count row stays
 *               green.  A measuring seat then built it as a real emulator and BOOTED IT:
 *               luna88k reached `login:` 1:1:1 with no diagnostics -- so THAT THREE-RUN
 *               BOOT-TO-LOGIN TRIAL did not catch it.  (An earlier draft said "the rig
 *               cannot catch it"; a pass-2 seat was right that a different workload or a
 *               different assertion on the same rig might.)  The likely masking mechanism
 *               is that OpenBSD issues ~603,000 SCR flush commands per boot and that arm
 *               does its own INVALIDATE_ALL -- BELIEVED, because co-occurrence plus a
 *               successful boot is not established attribution.
 *               ARGUMENT-INSPECTING ROWS are what catch it: F1 AND F2 both fail, which is
 *               what the census records (`mutA_vaddr -> F1/F2`).  An earlier draft of this
 *               comment said F1 was "the only thing in existence" that catches it; the
 *               census printed directly underneath it said otherwise, and nobody noticed
 *               until a pass-2 seat read them together.
 *
 *    mutant B   c -> cpu as the callback receiver.  dev_m8820x.c computes `c` from
 *               d->cpu_nr precisely because they differ; luna88k packs cpu_nr into the
 *               address and supports up to 4 CPUs, so this purges the wrong CPU's cache.
 *               A SINGLE-CPU FIXTURE CANNOT SEE IT -- and both repro_m8invread.c and
 *               diff_m8820x.c are single-cpu.  Row G1 drives the device from a SECOND cpu.
 *
 *    mutant C   drop the braces the fix introduced:
 *                     if (writeflag == MEM_WRITE)
 *                             c->invalidate_translation_caches(...);
 *                             regs[...] = idata;
 *               MEM_READ is 0 and idata is filled only on a write, so A READ NOW ZEROES THE
 *               REGISTER.  Purge counts are untouched and a FIRST read still returns the
 *               right value, because odata is snapshotted before the switch.  Only a SECOND
 *               read sees it.  That is row E7, the idempotency row.
 *
 *    mutant G   `if (writeflag == MEM_WRITE && idata)` -- ONE APPENDED TOKEN, found by a
 *               pass-2 seat, and it SURVIVED all sixteen rows when they were written.  A
 *               zero write then neither purges nor stores, so writing 0 to a previously
 *               nonzero SAPR or UAPR silently fails to disable that translation context.
 *               Every other write row used NONZERO data; E8's single zero is written to
 *               a register that fresh() already zeroed, so it is not a TRANSITION and
 *               proves nothing.  Row E9 is the repair: seed nonzero, write zero, assert
 *               BOTH that the store landed AND that the purge still happened.
 *
 *  THE EQUALITY-GUARD MUTANT, AND AN HONEST DOWNGRADE OF WHY ROW F4 EXISTS.  Gating the
 *  purge on `idata != regs[...]` (mirroring the BWP arm) used to pass every row here, and
 *  this note said so while also declining to call it a defect.  #435 added F4, which
 *  CATCHES it -- so the two statements could not both stand, and a pass-2 seat said so.
 *
 *  The honest position is the seat's: an unchanged APR word changes no translation INPUT,
 *  so skipping the purge is NOT under-invalidation in this model, and F4 pins HISTORICAL
 *  CALL BEHAVIOUR rather than a demonstrated correctness requirement.  F4 stays, because
 *  the purge-on-change shape is easy to write by accident beside a BWP arm that does
 *  exactly that, and a row noticing the arm change shape is worth having -- but it is a
 *  SHAPE PIN, not a proof of harm, and an earlier draft calling it dangerous was too
 *  strong.  Contrast mutant G, which IS a defect: it drops a write of zero to a register
 *  holding something else, and that loses state.
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

/*
 *  THE SPY.  It captures the RECEIVER, the ADDRESS and the FLAGS of every call, because a
 *  detector that counts calls and ignores their arguments is green for any argument -- the
 *  `constblind` shape, and mutant A walks straight through it.
 */
static int inv_calls;
static struct cpu *inv_last_cpu;
static uint64_t inv_last_addr;
static int inv_last_flags;
static int inv_all_were_ALL, inv_all_addr_zero;
static struct cpu *inv_all_same_cpu;
static int inv_cpu_mismatch;

static void spy_invalidate(struct cpu *c, uint64_t a, int flags)
{
	inv_calls++;
	inv_last_cpu = c; inv_last_addr = a; inv_last_flags = flags;
	if (flags != INVALIDATE_ALL) inv_all_were_ALL = 0;
	if (a != 0) inv_all_addr_zero = 0;
	if (inv_all_same_cpu == NULL) inv_all_same_cpu = c;
	else if (inv_all_same_cpu != c) inv_cpu_mismatch = 1;
}

#include "../src/devices/dev_m8820x.c"

/* --------------------------------------------------------------- harness --- */

static int rows, fails;
static void check(const char *name, const char *got, const char *want)
{
	rows++;
	if (strcmp(got, want) == 0)
		printf("  ok    %-58s %s\n", name, got);
	else {
		fails++;
		printf("  FAIL  %-58s\n          got  %s\n          want %s\n",
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

static struct cpu *cpu0, *cpu1;
static struct machine *machine;
static struct m8820x_data dev;
/*  THREE cmmu objects, not one.  A pass-2 seat showed that a single shared object makes
    two whole classes of one-identifier mutant structurally invisible: with cpu0 and cpu1
    pointing at the SAME cmmu, `regs = c->...` -> `regs = cpu->...` lands in the same array
    either way; and with cmmu_nr always 0, `cmmu[d->cmmu_nr]` -> `cmmu[0]` is a no-op.  */
static struct m8820x_cmmu *cmmu;	/*  cpu0, cmmu_nr 0 -- the instruction CMMU  */
static struct m8820x_cmmu *cmmu_d;	/*  cpu0, cmmu_nr 1 -- the DATA CMMU        */
static struct m8820x_cmmu *cmmu_b;	/*  cpu1's own -- a DIFFERENT object        */

/*
 *  `owes` -- does a WRITE to this register owe a translation-cache purge?  #435 split the
 *  arm: only SAPR and UAPR are read by m88k_translate_v2p (memory_m88k.c:135,137), so only
 *  those two can change a translation.  The other four STORE but do not purge.
 *
 *  THE ROWS BELOW WERE RE-PINNED IN THE SAME COMMIT AS THAT SPLIT, ON PURPOSE.  A detector
 *  that goes red on an intended change cannot tell intent from defect, and this file's own
 *  forward note predicted which rows would move -- it named THREE and the answer was FOUR.
 *  Writing the prediction down is what made the miss visible; getting it slightly wrong is
 *  why the rule is "re-pin in the same commit", not "trust the note".
 */
static const struct { uint32_t reg; const char *nm; int owes; } GROUP[] = {
	{ CMMU_PFSR, "PFSR", 0 }, { CMMU_PFAR, "PFAR", 0 }, { CMMU_SAR,  "SAR",  0 },
	{ CMMU_SCTR, "SCTR", 0 }, { CMMU_SAPR, "SAPR", 1 }, { CMMU_UAPR, "UAPR", 1 },
};
#define NOWES 2		/*  SAPR and UAPR  */
#define NGROUP ((int) (sizeof(GROUP)/sizeof(GROUP[0])))

static void fresh(void)
{
	memset(cmmu, 0, sizeof(*cmmu));
	memset(&dev, 0, sizeof(dev));
	cmmu->reg[CMMU_IDR] = (M88200_ID << 21) | (9 << 16);
	fatal_calls = debug_calls = inv_calls = 0;
	inv_last_cpu = NULL; inv_last_addr = 0; inv_last_flags = -1;
	inv_all_were_ALL = 1; inv_all_addr_zero = 1;
	inv_all_same_cpu = NULL; inv_cpu_mismatch = 0;
}

static uint32_t acc(struct cpu *c, uint64_t off, int writeflag, uint32_t val)
{
	unsigned char buf[4];
	memset(buf, 0, sizeof(buf));
	if (writeflag == MEM_WRITE)
		memory_writemax64(c, buf, 4, val);
	dev_m8820x_access(c, NULL, off, buf, 4, writeflag, &dev);
	return (uint32_t) memory_readmax64(c, buf, 4);
}

int main(void)
{
	int i, read_purges = 0, write_purges = 0, perreg_bad = 0;
	int e9_store_bad = 0, e9_purge_bad = 0;
	uint32_t v;
	char buf[64];

	setvbuf(stdout, NULL, _IOLBF, 0);
	cpu0 = calloc(1, sizeof(struct cpu));
	cpu1 = calloc(1, sizeof(struct cpu));
	machine = calloc(1, sizeof(struct machine));
	cmmu = calloc(1, sizeof(struct m8820x_cmmu));
	cmmu_d = calloc(1, sizeof(struct m8820x_cmmu));
	cmmu_b = calloc(1, sizeof(struct m8820x_cmmu));
	machine->cpus = calloc(2, sizeof(struct cpu *));
	machine->cpus[0] = cpu0;
	machine->cpus[1] = cpu1;
	machine->ncpus = 2;
	cpu0->machine = machine; cpu1->machine = machine;
	cpu0->cd.m88k.cmmu[0] = cmmu;
	cpu0->cd.m88k.cmmu[1] = cmmu_d;		/*  the DATA cmmu -- cmmu_nr 1     */
	cpu1->cd.m88k.cmmu[0] = cmmu_b;		/*  NOT the same object as cpu0's  */
	cpu0->invalidate_translation_caches = spy_invalidate;
	cpu1->invalidate_translation_caches = spy_invalidate;
	fresh();

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

	printf("--- E. a READ owes no purge, PER REGISTER ---\n");
	/*  PER REGISTER, not an aggregate.  A seat named the mutant an aggregate misses:
	    move a purge from one register to another and the totals do not budge.  */
	for (i = 0; i < NGROUP; i++) {
		fresh();
		acc(cpu0, GROUP[i].reg * 4, MEM_READ, 0);
		if (inv_calls != 0) perreg_bad++;
		read_purges += inv_calls;
	}
	check_u("E1 reads that purge, summed over the six", read_purges, 0);
	check_u("E2 registers whose READ purges (per-register, not a sum)", perreg_bad, 0);

	/*  THE CONTROL that stops this being one-sided: the WRITE side is NOT under test.
	    THIS FORWARD NOTE WAS RIGHT IN KIND AND WRONG IN COUNT, WHICH IS WHY IT IS KEPT.
	    It predicted that the filed `m8sarpurge` would redden E3/E4/F1 and that they must
	    be RE-PINNED rather than deleted.  #435 landed and **FOUR** rows went red, not
	    three: E9 as well, because E9 welded a purge assertion to a store assertion and
	    only the purge half moved.  The note is what made the miss visible -- a prediction
	    you can check beats a rule you have to remember -- but "re-pin in the SAME COMMIT
	    and re-run" is the part that has to hold, because the note itself was off by one.
	    "CONTROL" here means "not the thing under test in THIS round", never "invariant".  */
	perreg_bad = 0;
	for (i = 0; i < NGROUP; i++) {
		fresh();
		acc(cpu0, GROUP[i].reg * 4, MEM_WRITE, 0x1000 + i);
		if (inv_calls != GROUP[i].owes) perreg_bad++;
		write_purges += inv_calls;
	}
	check_u("E3 writes that purge, summed (only SAPR/UAPR owe one)",
	    write_purges, NOWES);
	check_u("E4 every register purges exactly as much as it owes", perreg_bad, 0);

	/*  A control on the reproduction rather than the code: outside the group, nothing.  */
	fresh();
	acc(cpu0, CMMU_IDR * 4, MEM_READ, 0);
	check_u("E5 CONTROL: reading IDR (outside the group) purges nothing", inv_calls, 0);
	fresh();
	acc(cpu0, CMMU_IDR * 4, MEM_WRITE, 1);
	check_u("E6 CONTROL: writing IDR does not purge either", inv_calls, 0);

	/*
	 *  E7 -- THE IDEMPOTENCY ROW, and it exists because of mutant C.  Dropping the braces
	 *  makes the store unconditional, so a READ writes idata (0) into the register.  The
	 *  FIRST read still returns the right value because odata is snapshotted before the
	 *  switch; only a SECOND read can see it.  Read every register twice.
	 */
	perreg_bad = 0;
	for (i = 0; i < NGROUP; i++) {
		uint32_t seed = 0xa5a50000u + (uint32_t) i, r1, r2;
		fresh();
		acc(cpu0, GROUP[i].reg * 4, MEM_WRITE, seed);
		r1 = acc(cpu0, GROUP[i].reg * 4, MEM_READ, 0);
		r2 = acc(cpu0, GROUP[i].reg * 4, MEM_READ, 0);
		if (r1 != seed || r2 != seed) perreg_bad++;
	}
	check_u("E7 a read is IDEMPOTENT -- twice returns the same (mutant C)",
	    perreg_bad, 0);

	/*  E8 -- read-back for ALL SIX, not SCTR alone: a mutant dropping the store for the
	    five non-SCTR registers passes a single-register row outright.  Distinct values
	    including zero and a high-bit value.
	    THE FIRST VERSION OF THIS COMMENT ADDED "so a data-dependent guard cannot hide",
	    AND A PASS-2 SEAT FALSIFIED IT BY CONSTRUCTION -- see E9.  The claim is removed
	    rather than softened, because it was simply wrong: the one zero in this table is
	    written to PFSR immediately after fresh(), when PFSR is ALREADY zero, so dropping
	    the store is invisible here and E8 never inspects a purge at all.  A value table
	    that merely CONTAINS zero proves nothing; the zero has to be a TRANSITION.  */
	perreg_bad = 0;
	for (i = 0; i < NGROUP; i++) {
		static const uint32_t vals[] = { 0x00000000u, 0x80000000u, 0xffffffffu,
		                                 0x00000001u, 0x5a5a5a5au, 0xdeadbeefu };
		fresh();
		acc(cpu0, GROUP[i].reg * 4, MEM_WRITE, vals[i]);
		if (acc(cpu0, GROUP[i].reg * 4, MEM_READ, 0) != vals[i]) perreg_bad++;
	}
	check_u("E8 every one of the six stores and reads back its own value",
	    perreg_bad, 0);

	/*
	 *  E9 -- THE NONZERO -> ZERO TRANSITION, and it exists because a pass-2 seat built
	 *  a mutant that survived all sixteen rows without it:
	 *
	 *        if (writeflag == MEM_WRITE && idata) {
	 *
	 *  One appended token.  A zero write then neither purges nor stores -- so writing 0
	 *  to a previously nonzero SAPR or UAPR silently fails to disable that translation
	 *  context, which is a real behaviour change on the write side this round promised
	 *  to leave alone.  It survived because every other write row uses NONZERO data:
	 *  E3/E4, F1-F3, G1/G2 and E7 all do, reads carry idata == 0 so E1/E2 stay green,
	 *  E8's single zero is not a transition, and H exercises the separate SCR arm.
	 *
	 *  So the row has to do BOTH things the mutant breaks: seed nonzero, write zero,
	 *  then assert the register really became zero AND that the zero write still purged
	 *  exactly once.  Checking only the read-back would leave the purge half undetected.
	 */
	perreg_bad = 0;
	for (i = 0; i < NGROUP; i++) {
		fresh();
		acc(cpu0, GROUP[i].reg * 4, MEM_WRITE, 0xffffffffu);	/*  seed nonzero  */
		inv_calls = 0;
		acc(cpu0, GROUP[i].reg * 4, MEM_WRITE, 0x00000000u);	/*  the transition  */
		if (inv_calls != GROUP[i].owes) e9_purge_bad++;
		if (acc(cpu0, GROUP[i].reg * 4, MEM_READ, 0) != 0) e9_store_bad++;
	}
	/*
	 *  SPLIT INTO TWO ROWS BY #435, AND THAT IS THE INTERESTING PART.  This was ONE row
	 *  asserting "still purges once AND still stores" -- two properties welded together,
	 *  which was fine while they moved together and wrong the moment they did not.  The
	 *  PURGE half follows the split; the STORE half must stay ALL SIX, and it is the half
	 *  that kills the natural over-reading of #435's own argument (drop the store as well
	 *  as the purge), which a measure seat built and which passed every other row.  A row
	 *  that conflates two properties can only be re-pinned as a unit, so it has to be
	 *  taken apart before either half can move.
	 */
	check_u("E9a a nonzero->ZERO write still STORES, all six", e9_store_bad, 0);
	check_u("E9b   ...and purges exactly as much as it owes", e9_purge_bad, 0);

	/*
	 *  E10 -- EVERY READ ROW ABOVE RUNS AGAINST A ZERO REGISTER FILE, and that is a
	 *  structural blind spot rather than an oversight in any one row.  fresh() memsets
	 *  the cmmu, so a read-side purge gated on the register's VALUE never fires during
	 *  E1/E2, and E7/E8 do not look at inv_calls at all.  A pass-2 seat built exactly
	 *  that mutant --
	 *
	 *        if (writeflag == MEM_READ && odata != 0)
	 *                c->invalidate_translation_caches(c, 0, INVALIDATE_ALL);
	 *
	 *  -- and it passed all seventeen rows, passed diff_m8820x.c as well, AND BOOTED THE
	 *  luna88k RIG 1:1:1 with no diagnostics.  It is not a subtle survivor: measured, it
	 *  restores 144,536 of the ~286,500 purges this round removes, i.e. HALF THE DEFECT.
	 *  Half, because memory_m88k.c:383-384 zeroes the NON-faulting CMMU's PFSR on every
	 *  fault so the handler can tell the two apart, which makes exactly 49.98% of PFSR
	 *  reads return nonzero.  So: seed a nonzero value first, then read.
	 */
	perreg_bad = 0;
	for (i = 0; i < NGROUP; i++) {
		int before;
		fresh();
		acc(cpu0, GROUP[i].reg * 4, MEM_WRITE, 0xdeadbe00u + (uint32_t) i);
		before = inv_calls;
		acc(cpu0, GROUP[i].reg * 4, MEM_READ, 0);
		if (inv_calls != before) perreg_bad++;
	}
	check_u("E10 a read of a NONZERO register still owes no purge", perreg_bad, 0);

	printf("--- F. the purge's ARGUMENTS, not merely its count ---\n");
	/*
	 *  F1 AND F2 BOTH CATCH MUTANT A, and a measuring seat proved a full rig boot does
	 *  not: INVALIDATE_ALL -> INVALIDATE_VADDR leaves the count identical, invalidates
	 *  virtual page 0 alone, and still reaches `login:` 1:1:1.
	 *
	 *  This said "F1 IS THE ONLY ROW" until a pass-2 seat found it -- the SECOND copy of
	 *  a claim already retracted in this file's own header, in the same file, one round
	 *  after the retraction.  That is the grep-for-siblings rule failing twice on one
	 *  sentence.  A correction is not finished until the FILE has been searched for the
	 *  claim, not just the place someone happened to notice it.
	 */
	fresh();
	for (i = 0; i < NGROUP; i++)
		acc(cpu0, GROUP[i].reg * 4, MEM_WRITE, 0x2000 + i);
	check_u("F1 every write purge passes INVALIDATE_ALL (mutant A)",
	    (uint64_t) (inv_all_were_ALL && inv_calls == NOWES), 1);
	snprintf(buf, sizeof(buf), "%d", inv_last_flags);
	{
		char want[32];
		snprintf(want, sizeof(want), "%d", (int) INVALIDATE_ALL);
		check("F2 the last purge's flags, named rather than counted", buf, want);
	}
	/*  F3 pins the CALL SHAPE.  Today the ALL branch ignores addr, so this is inert as
	    behaviour -- recorded as such rather than dressed up as a behavioural row.  */
	check_u("F3 every purge passes addr 0 (pins the shape; inert under ALL)",
	    (uint64_t) inv_all_addr_zero, 1);

	/*
	 *  F4 -- THE ONE GENUINELY NEW ROW #435 ADDS, and the only thing that catches a mutant
	 *  a measure seat named as the likeliest to be written by accident: purge only when the
	 *  value actually CHANGES.  The BATC arm further down already does exactly that
	 *  (`if (old != idata)`), so the asymmetry invites it -- and it is the under-
	 *  invalidation direction.  A redundant same-value write must still purge.
	 *
	 *  *** BOTH AREA POINTERS, NOT JUST SAPR, AND THAT COST A SURVIVING MUTANT. ***  The
	 *  first version of this row repeated a same-value write to SAPR alone.  A pass-2 seat
	 *  reasoned -- without being able to compile anything, in a read-only sandbox -- that
	 *  an equality guard applied to UAPR ONLY would therefore slip through all 23 rows,
	 *  because every other UAPR write in this file changes the value.  Built and run: it
	 *  SURVIVED, exactly as predicted.  A row that pins a property on one member of a set
	 *  pins it for that member only, and the set here has two.
	 */
	perreg_bad = 0;
	for (i = 0; i < NGROUP; i++) {
		if (!GROUP[i].owes)
			continue;
		fresh();
		acc(cpu0, GROUP[i].reg * 4, MEM_WRITE, 0x600d600du);
		inv_calls = 0;
		acc(cpu0, GROUP[i].reg * 4, MEM_WRITE, 0x600d600du);	/*  SAME value  */
		if (inv_calls != 1) perreg_bad++;
	}
	check_u("F4 a redundant same-value write still purges, BOTH area pointers",
	    perreg_bad, 0);

	printf("--- G. WHICH cpu is purged (single-cpu fixtures are blind here) ---\n");
	/*
	 *  G1 -- MUTANT B.  dev_m8820x.c derives `c` from d->cpu_nr because it is not the
	 *  accessing cpu; luna88k packs cpu_nr into the address and allows up to 4 CPUs.  A
	 *  one-cpu fixture aliases the two and cannot see the difference, which is a gap that
	 *  repro_m8invread.c and diff_m8820x.c both still have.
	 */
	fresh();
	dev.cpu_nr = 0;			/*  the CMMU belongs to cpu0 ...  */
	acc(cpu1, CMMU_SAPR * 4, MEM_WRITE, 0x77);	/*  ... but cpu1 is accessing it  */
	check_u("G1 the purge targets the CMMU's OWNER, not the accessor (mutant B)",
	    (uint64_t) (inv_calls == 1 && inv_last_cpu == cpu0), 1);
	check_u("G2   ...and it is NOT the accessing cpu",
	    (uint64_t) (inv_last_cpu != cpu1), 1);

	/*
	 *  G3/G4 -- THE REGISTER FILE, not the callback receiver.  G1/G2 inspect only the
	 *  purge's argument, so the SAME one-identifier substitution applied to the regs
	 *  pointer at dev_m8820x.c:251 (`c->cd.m88k...` -> `cpu->cd.m88k...`) survived them
	 *  outright -- while the two cpus shared one cmmu object it landed in the same array
	 *  either way.  With distinct objects it cannot.  Two rows that look alike can still
	 *  leave a gap between them.
	 */
	fresh();
	dev.cpu_nr = 0;
	acc(cpu1, CMMU_SAPR * 4, MEM_WRITE, 0x5150);
	check_u("G3 the STORE lands in the OWNER's register file",
	    (uint64_t) cmmu->reg[CMMU_SAPR], 0x5150);
	check_u("G4   ...and not in the accessor's",
	    (uint64_t) cmmu_b->reg[CMMU_SAPR], 0);

	/*
	 *  G5 -- THE SECOND CMMU.  There are two per cpu, instruction and data, and
	 *  d->cmmu_nr selects between them.  Every row above leaves cmmu_nr at 0 because
	 *  fresh() memsets dev, so `cmmu[d->cmmu_nr]` -> `cmmu[0]` was invisible to all of
	 *  them -- and memory_m88k.c:383-384 depends on the two being distinct.
	 */
	fresh();
	dev.cpu_nr = 0; dev.cmmu_nr = 1;
	acc(cpu0, CMMU_SAPR * 4, MEM_WRITE, 0xd47a);
	check_u("G5 cmmu_nr 1 addresses the DATA cmmu, not the instruction one",
	    (uint64_t) (cmmu_d->reg[CMMU_SAPR] == 0xd47a &&
	                cmmu->reg[CMMU_SAPR] == 0), 1);

	/*
	 *  *** G6-G9 EXIST BECAUSE #435 CREATED A SECOND STORE SITE AND EVERY SELECTOR ROW
	 *  ABOVE DRIVES CMMU_SAPR, WHICH THE SPLIT LEFT IN THE OTHER ARM. ***
	 *
	 *  G1-G5 pin who owns the register file and which CMMU is addressed -- but all of them
	 *  write SAPR.  After the split SAPR is in the PURGING arm, so the new store-only arm
	 *  had ZERO owner/cmmu coverage, and symmetrically every purge-asserting row leaves
	 *  cpu_nr and cmmu_nr at 0 because fresh() memsets dev.  A measure seat built SEVEN
	 *  mutants through that gap and FIVE were real defects, the smallest being one appended
	 *  clause:
	 *
	 *        if (writeflag == MEM_WRITE && d->cmmu_nr == 0)
	 *
	 *  which is structurally the SAME attack as the historical `&& idata` mutant this file
	 *  already records as having survived sixteen rows.  Adding a second
	 *  `if (writeflag == MEM_WRITE)` re-opened it on a selector instead of on data.
	 *
	 *  NOT THEORETICAL, measured on the rig: dev_luna88k.c:1001-1004 registers cmmu_nr 0 and
	 *  1 on EVERY boot including the single-CPU one, and the data CMMU (cmmu_nr 1, the one
	 *  memory_m88k.c:112 uses for every data access) takes 318,457 of the 613,342 SAR writes
	 *  -- 51.9%.  So `d->cmmu_nr == 0` silently discards half the SAR traffic, and a witness
	 *  driving SAR THROUGH THE HANDLER shows the consequence: the wrong page is flushed and a
	 *  stale supervisor translation is kept.
	 *
	 *  THE GENERAL LESSON, worth more than the rows: WHEN A ROUND SPLITS AN ARM, EVERY ROW
	 *  THAT PINNED A PROPERTY OF THE OLD ARM NOW PINS IT FOR ONLY ONE HALF.  Re-pinning the
	 *  rows that go RED is the obvious half of that; the rows that stay GREEN while quietly
	 *  covering less are the half that gets missed.
	 */
	fresh();
	dev.cpu_nr = 0;
	acc(cpu1, CMMU_SAR * 4, MEM_WRITE, 0x5a71);		/*  the STORE-ONLY arm  */
	check_u("G6 the store-only arm lands in the OWNER's register file",
	    (uint64_t) (cmmu->reg[CMMU_SAR] == 0x5a71 && cmmu_b->reg[CMMU_SAR] == 0), 1);

	fresh();
	dev.cpu_nr = 0; dev.cmmu_nr = 1;
	acc(cpu0, CMMU_SAR * 4, MEM_WRITE, 0x5a72);
	check_u("G7   ...and addresses the DATA cmmu when cmmu_nr says so",
	    (uint64_t) (cmmu_d->reg[CMMU_SAR] == 0x5a72 && cmmu->reg[CMMU_SAR] == 0), 1);

	/*  G8/G9 -- the purge must not be gated on either selector being zero.  Every other
	    purge row runs with cpu_nr = cmmu_nr = 0, so a `&& d->cmmu_nr == 0` on the PURGING
	    arm would be invisible to all of them.  */
	fresh();
	dev.cpu_nr = 0; dev.cmmu_nr = 1;
	acc(cpu0, CMMU_SAPR * 4, MEM_WRITE, 0x5a73);
	check_u("G8 a purge still happens with cmmu_nr = 1", inv_calls, 1);

	fresh();
	dev.cpu_nr = 1; dev.cmmu_nr = 0;
	acc(cpu1, CMMU_SAPR * 4, MEM_WRITE, 0x5a74);
	check_u("G9 a purge still happens with cpu_nr = 1", inv_calls, 1);

	printf("--- H. the neighbouring arm still purges (nothing here may weaken it) ---\n");
	/*
	 *  H1 -- the SCR flush command's own purge at dev_m8820x.c:187.  Measured at ~603,000
	 *  per boot, it is the mechanism that actually keeps translation correct on this
	 *  guest; nothing in rows E-G would stop a careless edit deleting it.
	 */
	fresh();
	acc(cpu0, CMMU_SCR * 4, MEM_WRITE, CMMU_FLUSH_SUPER_PAGE);
	check_u("H1 CONTROL: an SCR flush command still purges", inv_calls, 1);
	check_u("H2 CONTROL: and it too passes INVALIDATE_ALL",
	    (uint64_t) inv_all_were_ALL, 1);

	snprintf(buf, sizeof(buf), "%d", rows + 1);
	check("IDENTITY row count -- guards against a stale copy", buf, "27");

	printf("\n%d rows, %d failures\n", rows, fails);
	printf("%s\n", fails == 0 ? "DIFF_M8INVREAD_PASS" : "DIFF_M8INVREAD_FAIL");
	return fails != 0;
}
