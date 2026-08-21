/*
 *  Offline differential for the SHIPPED M8820x CMMU -- src/devices/dev_m8820x.c.
 *
 *  WHY THIS EXISTS.  #433 removed five `exit(1)` calls by which an ordinary guest register
 *  access TERMINATED THE HOST PROCESS.  Measured before the fix, driving every word offset in
 *  the mapped window: 1007 of 1024 reads and 1009 of 1024 writes killed the host.
 *
 *  IT IS THE REPOSITORY FILE, #included exactly as diff_footbridge.c includes its device.
 *
 *  *** THE KILL CRITERION IS THE EXIT STATUS, NOT "THE CHILD DIED", AND THAT IS NOT A DETAIL.
 *  The first reproduction of this defect got its headline number WRONG by exactly six in each
 *  direction, because six offsets crashed in the HARNESS -- the register-file arm calls
 *  invalidate_translation_caches() BEFORE the writeflag check, so it fires on READS, and the
 *  driver had left that callback NULL.  A review seat derived the true numbers from the source
 *  and named the mechanism; re-measuring with a no-op callback and with status 1 (the real
 *  exit path) distinguished from a signal gave 1007/1009/17, matching to the offset.  So this
 *  file installs the callback AND discriminates the status, and a signal death is reported as
 *  a FAULT rather than counted as a detection.  Mechanical rule 4, in the one place it was
 *  actually violated: "did it fail for the reason under test?"
 *
 *  WHAT IT PROVES.  That no offset in the window kills the host in either direction; that the
 *  complaint is LATCHED (one report, not one per access -- a real boot writes CMMU_SCR 640,016
 *  times, so an unlatched complaint is a guest-drivable stderr flood); that the seven commands
 *  #433 folded in are handled rather than dropped; and -- the row that defends the fold itself
 *  -- that the four PATC flush variants REALLY INVALIDATE, checked white-box against the PATC
 *  array rather than inferred from survival.
 *
 *  WHAT IT DOES NOT PROVE.  That the device is reachable by a guest instruction through the
 *  real memory path.  That needs the cold-debugger probe on the luna88k rig (measured at 3.1 s
 *  for 8 rows, ~60x cheaper than a boot), which is filed as this round's follow-up.
 *
 *  *** THIS FILE IS A DETECTOR, NOT A REPRODUCTION, AND THE DISTINCTION IS MECHANICAL. ***
 *  It #includes the device and calls dev_m8820x_access() directly, so the machine description
 *  and the CPU/device dispatch have been removed -- which is the project's own discriminator
 *  for "never a reproduction" (WITNESS LADDER rung 1).  Nothing below is described as
 *  reproducing anything; every row is a defence of a property, graded by whether it fails on
 *  a mutant, never by the witness clauses.
 *
 *  ----------------------------------------------------------------------------------------
 *  SECTION F -- THE BWP/BATC ARM, ADDED BECAUSE IT HAD ZERO EXECUTABLE COVERAGE.
 *
 *  Three arms of dev_m8820x.c touch translation inputs.  Two were covered (the SAPR/UAPR
 *  purge split by diff_m8invread.c, the SCR flush commands by section D here).  The third --
 *  CMMU_BWP0..7, which programs the BLOCK ATC -- had none: `grep -cE 'BWP|bwp|batc'` returned
 *  TWO MATCHING LINES in diff_m8invread.c (grep -c counts LINES, not occurrences), both of
 *  them comment prose ABOUT THE OTHER ARM at its :65 and :72, and ZERO here.
 *
 *  MEASURED IN THIS ROUND rather than inherited from the brief that opened it: against the
 *  PRE-CHANGE files, deleting `batc[i] = idata;` at dev_m8820x.c:479 while leaving
 *  `regs[...] = idata` in place left BOTH differentials fully green -- 25 rows 0 failures and
 *  27 rows 0 failures, not one red row between them.  "This detector misses that" is itself
 *  checkable in about a minute, so it was checked rather than repeated.
 *
 *  *** WHY A REGISTER READ-BACK ROW WOULD HAVE BEEN VACUOUS HERE. ***  That mutant keeps the
 *  register file store, so write-then-read-back still returns the written word.  The shadow
 *  `batc[]` is a SECOND array, and it is the one m88k_translate_v2p consults at
 *  memory_m88k.c:152-179 -- BEFORE the PATC and BEFORE the page-table walk -- so a stale entry
 *  silently returns a wrong physical address for a 512 KB block while every register-level row
 *  stays green.  A row that observes the register cannot see the array that matters.
 *
 *  SO THE ORACLE IS THE REAL TRANSLATOR.  This file now also #includes
 *  src/cpus/memory_m88k.c -- the repository file, unmodified -- and asks
 *  m88k_translate_v2p() what a virtual address resolves to.  That is deliberately NOT a
 *  re-implementation of the BATC formula: computing the right answer in the detector and then
 *  comparing it against the device's array would assert something strictly weaker than "the
 *  device's array is what translation reads", and this project has shipped detectors broken by
 *  exactly that shape.  The two consumers are wired together here because the coupling IS the
 *  property.
 *
 *  THE ORACLE CARRIES THREE CONTROLS, NOT ONE, and the reason is on record: a sibling probe
 *  once returned 0x0 from every site WITH ITS ONE CONTROL GREEN.  Rows F0a/F0b/F0c pin that
 *  the fixture can produce THREE DISTINGUISHABLE ANSWERS -- a walked page-table address, an
 *  identity mapping when the area pointer is invalid, and a hard translation failure when the
 *  tables are unmapped.  Without them "the expected physical address came back" could be a
 *  constant.
 *
 *  UNCOVERED, STATED RATHER THAN IMPLIED: this fixture is SINGLE-CPU, so the receiver half of
 *  the arm -- `c->cd.m88k.cmmu[d->cmmu_nr]->batc` with `c` derived from d->cpu_nr -- cannot be
 *  exercised here for the cpu index.  Those rows live in diff_m8invread.c section J, which
 *  already carries the two-cpu / two-CMMU fixture.  The CMMU index IS exercised here (F3/F4),
 *  because translation itself selects cmmu[instr? 0 : 1] and that selection is observable.
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

/*  fatal() is COUNTED, because "complain exactly once" is a testable property and the
    `cflood` class is what makes it worth testing.  */
static int fatal_calls, debug_calls;
void fatal(const char *fmt, ...) { (void) fmt; fatal_calls++; }
void debug(const char *fmt, ...) { (void) fmt; debug_calls++; }

/*  Needed only by memory_m88k.c, and only on paths section F never takes: every translate
    below passes FLAG_NOEXCEPTIONS, which returns at memory_m88k.c:392 before either of these
    can be reached.  They are COUNTED anyway, and F0c asserts the count stayed zero -- an
    unexpected exception would otherwise be a silent no-op that made a row's answer mean
    something other than what its name says.  */
static int exception_calls, debugmsg_calls;
void m88k_exception(struct cpu *c, int vector, int is_trap)
{ (void) c; (void) vector; (void) is_trap; exception_calls++; }
void debugmsg_cpu(struct cpu *c, int subsystem, const char *name, int verbosity, const char *fmt, ...)
{ (void) c; (void) subsystem; (void) name; (void) verbosity; (void) fmt; debugmsg_calls++; }

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

/*  The callback the register-file arm invokes BEFORE the writeflag check -- i.e. on reads
    too.  Left NULL it segfaults, which is what corrupted the first reproduction.  */
static int invalidate_calls;
static void noop_invalidate(struct cpu *c, uint64_t a, int flags)
{ (void)c; (void)a; (void)flags; invalidate_calls++; }

#include "../src/devices/dev_m8820x.c"

/*
 *  THE ORACLE FOR SECTION F: the REAL translator, the repository file, unmodified.  It is the
 *  only consumer of the shadow batc[] array, and asking it is the only way to assert that the
 *  BWP arm's second store is a TRANSLATION INPUT rather than merely a second array.
 */
#include "../src/cpus/memory_m88k.c"

/* --------------------------------------------------- section F fixture --- */
/*
 *  A page-table image in host memory, reached through the one hook memory_m88k.c uses to touch
 *  emulated RAM.  Three physical pages are recognised and everything else is POISON, so the
 *  fixture can produce three distinguishable outcomes (see F0a/F0b/F0c).
 */
#define FAKE_SEGTAB_PA	0x00010000u
#define FAKE_PAGETAB_PA	0x00020000u
#define FAKE_UNMAPPED_PA 0x00030000u	/*  deliberately NOT recognised below  */
#define WALK_PA		0x77777000u	/*  what a page-table walk resolves to  */

static uint32_t fake_segtab[1 << SDT_BITS];
static uint32_t fake_pagetab[1 << PDT_BITS];
static uint32_t fake_poison[1 << PDT_BITS];

unsigned char *memory_paddr_to_hostaddr(struct memory *mem, uint64_t paddr, int writeflag)
{
	(void) mem; (void) writeflag;
	if ((paddr & 0xfffff000) == FAKE_SEGTAB_PA)
		return (unsigned char *) fake_segtab;
	if ((paddr & 0xfffff000) == FAKE_PAGETAB_PA)
		return (unsigned char *) fake_pagetab;
	return (unsigned char *) fake_poison;
}

/*  A BATC word: 13-bit logical block, 13-bit physical block, six flag bits.  Laid out to
    match memory_m88k.c:165 (`vaddr & 0xfff80000` vs `batc & 0xfff80000`) and :176
    (`((batc & 0x0007ffc0) << 13) | (vaddr & 0x0007ffff)`), which is where the 19-bit block
    size comes from -- thirdparty/m8820x_pte.h:191 names it BATC_BLKSHIFT.  */
#define MKBATC(lba, pba, fl)	((((uint32_t) (lba) & 0x1fff) << 19) |	\
				 (((uint32_t) (pba) & 0x1fff) <<  6) | (uint32_t) (fl))
#define BLK(b)			(((uint32_t) (b) & 0x1fff) << 19)

/*
 *  EVERY CASE IS DISTINCT, ON PURPOSE.  A table whose eight rows carry the same block would
 *  make a per-index defect invisible, which is one of the shapes that broke five consecutive
 *  detectors in this project.  Port n, sentinel slot k and their in-block offsets are all
 *  different numbers, and none of the three ranges overlaps.
 *
 *  *** AND THE UNION OF THE EIGHT WORDS COVERS ALL 32 BITS, WHICH THE FIRST VERSION DID NOT.
 *  It used LBA 0x100+n and PBA 0x200+n -- eight consecutive small numbers whose bitwise OR is
 *  0x00003fc0, so bit 31 was never set in any word this file ever stored.  A mutant masking the
 *  top of the logical block (`batc[i] = idata & 0x7fffffff`) was invisible to every row
 *  INCLUDING the exact-word row, while corrupting precisely the addresses a real kernel maps
 *  (thirdparty/m8820x.h:179-180 hardwires BATC8/BATC9 at 0xfff00000 and 0xfff80000).  The
 *  tables below OR to 0x1fff in both fields, so every logical- and physical-block bit is set by
 *  at least one port, and F13 adds all six flag bits on top.  ***
 *
 *  *** AND THE SECOND VERSION BROKE SOMETHING THE FIRST HAD BY ACCIDENT, WHICH IS THE PART
 *  WORTH KEEPING. ***  The consecutive table 0x100..0x107 gave eight ADJACENT 512 KB blocks, so
 *  widening the translator's virtual match from 512 KB to 1 MB (`0xfff80000` -> `0xfff00000` at
 *  memory_m88k.c:165) made port n's address hit port n-1's entry first, and F1 caught it for
 *  free.  Scattering the LBAs for bit coverage removed that adjacency -- and the same mutant
 *  then SURVIVED ALL 45 ROWS AND BOTH DIFFERENTIALS, measured.  A fixture change made to close
 *  one hole opened another, and nothing said so; only re-running the whole census after the
 *  change did.  The repair is not to go back: the table below is spaced at least 9 blocks apart
 *  AND covers every bit, and row F17 asserts the block BOUNDARY explicitly instead of relying on
 *  a neighbour that happens to be occupied.  A property that holds by accident is not pinned.
 */
static const uint16_t port_lba[8] =	/*  OR = 0x1fff; no two within 8 of each other  */
	{ 0x0003, 0x000c, 0x0030, 0x00c0, 0x0300, 0x0c00, 0x1000, 0x1555 };
static const uint16_t port_pba[8] =	/*  OR = 0x1fff  */
	{ 0x1002, 0x0801, 0x0404, 0x0208, 0x0110, 0x0080, 0x0060, 0x1aaa };
#define PORT_LBA(n)	((uint32_t) port_lba[n])
#define PORT_PBA(n)	((uint32_t) port_pba[n])
#define PORT_OFF(n)	((uint32_t) (0x00013000 + (n) * 0x1111))	/*  < 512 KB  */
#define PORT_VA(n)	(BLK(PORT_LBA(n)) | PORT_OFF(n))
#define PORT_PA(n)	(BLK(PORT_PBA(n)) | PORT_OFF(n))
#define SENT_LBA(k)	(0x0100 + (k) * 0x11)	/*  none of these is a port LBA  */
#define SENT_PBA(k)	(0x0300 + (k) * 0x11)
#define SENT_OFF	0x33u
#define SENT_VA(k)	(BLK(SENT_LBA(k)) | SENT_OFF)
#define SENT_PA(k)	(BLK(SENT_PBA(k)) | SENT_OFF)
#define WALKED(va)	(WALK_PA | ((va) & 0xfff))

#define SUPERVISOR_ENTRY	(BATC_SO | BATC_V)

/* --------------------------------------------------------------- harness --- */

static int rows, fails;
static void check(const char *name, const char *got, const char *want)
{
	rows++;
	if (strcmp(got, want) == 0)
		printf("  ok    %-56s %s\n", name, got);
	else {
		fails++;
		printf("  FAIL  %-56s\n          got  %s\n          want %s\n",
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

static struct cpu *cpu;
static struct machine *machine;
static struct m8820x_data dev;
static struct m8820x_cmmu *cmmu;	/*  cmmu_nr 0 -- the INSTRUCTION CMMU  */
/*  cmmu_nr 1, the DATA CMMU.  Added with section F, and it is not decoration: m88k_translate_v2p
    selects `cmmu[instr? 0 : 1]` at memory_m88k.c:112, so with one object the selector
    `cmmu[d->cmmu_nr]` -> `cmmu[0]` in the BWP arm would land in the same array either way and
    be structurally invisible.  Sections A-E leave dev.cmmu_nr at 0 (fresh() memsets dev) and
    are unaffected by its presence.  */
static struct m8820x_cmmu *cmmu_d;

static void fresh(void)
{
	memset(cmmu, 0, sizeof(*cmmu));
	memset(cmmu_d, 0, sizeof(*cmmu_d));
	memset(&dev, 0, sizeof(dev));
	cmmu->reg[CMMU_IDR] = (M88200_ID << 21) | (9 << 16);
	cmmu_d->reg[CMMU_IDR] = (M88200_ID << 21) | (9 << 16);
	fatal_calls = debug_calls = 0;
}

/*  0 survived, 1 the real exit(1) path, 2 died BY SIGNAL (a harness fault, NOT a detection).  */
static int probe(uint64_t off, int writeflag)
{
	pid_t pid = fork();
	if (pid == 0) {
		unsigned char buf[4];
		memset(buf, 0, sizeof(buf));
		dev_m8820x_access(cpu, NULL, off, buf, 4, writeflag, &dev);
		_exit(0);
	} else {
		int st = 0;
		waitpid(pid, &st, 0);
		if (WIFSIGNALED(st)) return 2;
		if (WIFEXITED(st) && WEXITSTATUS(st) == 0) return 0;
		return 1;
	}
}

static void access_word(uint64_t off, int writeflag, uint32_t val, uint32_t *out)
{
	unsigned char buf[4];
	memset(buf, 0, sizeof(buf));
	if (writeflag == MEM_WRITE)
		memory_writemax64(cpu, buf, 4, val);
	dev_m8820x_access(cpu, NULL, off, buf, 4, writeflag, &dev);
	if (out != NULL)
		*out = (uint32_t) memory_readmax64(cpu, buf, 4);
}

/* ------------------------------------------------- section F helpers --- */

/*  Write one BWP port through the device, exactly as a guest store would.  */
static void bwp(int n, uint32_t val)
{
	access_word((uint64_t) (CMMU_BWP0 + n) * 4, MEM_WRITE, val, NULL);
}

/*
 *  Rebuild the translation fixture.  Both area pointers are valid and point at the same
 *  two-level table, so a BATC MISS resolves to WALK_PA rather than failing -- three
 *  distinguishable outcomes beat two, and "the mapping went away" then has a positive
 *  signature instead of being indistinguishable from "the oracle stopped working".
 *
 *  Byte order is pinned BIG (m88k) and the seeds are written through the SAME macro
 *  memory_m88k.c:88-92 uses, which is an involution -- so the fixture is host-independent
 *  rather than relying on the host happening to be little-endian.
 */
static void batc_fixture(void)
{
	int i;
	fresh();
	for (i = 0; i < (1 << SDT_BITS); i++)
		fake_segtab[i] = BE32_TO_HOST(FAKE_PAGETAB_PA | SG_V);
	for (i = 0; i < (1 << PDT_BITS); i++)
		fake_pagetab[i] = BE32_TO_HOST(WALK_PA | PG_V);
	memset(fake_poison, 0, sizeof(fake_poison));	/*  SG_V clear -> segment fault  */
	cpu->byte_order = EMUL_BIG_ENDIAN;
	cpu->cd.m88k.cr[M88K_CR_PSR] = M88K_PSR_MODE;	/*  supervisor  */
	cmmu->reg[CMMU_SAPR] = cmmu->reg[CMMU_UAPR] = FAKE_SEGTAB_PA | APR_V;
	cmmu_d->reg[CMMU_SAPR] = cmmu_d->reg[CMMU_UAPR] = FAKE_SEGTAB_PA | APR_V;
	invalidate_calls = 0;
}

/*
 *  Ask the REAL translator.  FLAG_NOEXCEPTIONS keeps it side-effect free: the PATC refill and
 *  the U/M write-back at memory_m88k.c:317-355 are both guarded by `!no_exceptions`, so a
 *  translate cannot change what the next one sees.  A failure returns 0.
 */
static int xlate(int instr, int writeflag, int user, uint32_t vaddr, uint64_t *pa)
{
	int flags = FLAG_NOEXCEPTIONS;
	if (instr)     flags |= FLAG_INSTR;
	if (writeflag) flags |= FLAG_WRITEFLAG;
	if (user)      flags |= MEMORY_USER_ACCESS;
	*pa = 0xbadbadbadbadull;
	return m88k_translate_v2p(cpu, vaddr, pa, flags);
}

/*  "Does this virtual address resolve, through the BATC, to exactly this physical address?"  */
static int maps_to(int instr, uint32_t vaddr, uint32_t want_pa)
{
	uint64_t pa;
	return xlate(instr, 0, 0, vaddr, &pa) == 2 && pa == (uint64_t) want_pa;
}

/*  "...or did it fall through to the page-table walk?"  -- the positive signature of an
    absent BATC entry, which "not equal to the mapped address" would not give.  */
static int walks(int instr, uint32_t vaddr)
{
	uint64_t pa;
	return xlate(instr, 0, 0, vaddr, &pa) == 2 && pa == (uint64_t) WALKED(vaddr);
}

/*  Seed all TEN shadow slots with distinct sentinels, then program the eight ports.  The
    reserved slots 8 and 9 exist in the model (N_M88200_BATC_REGS is 10, cpu_m88k.h:230) and
    are never written by this arm; thirdparty/m8820x.h:176-180 records that real 88200 silicon
    hardwires two BATC entries.  Whether the emulator seeds them is beside the point here --
    the property is that a write to a BWP PORT touches exactly one of the ten slots and it is
    the slot the port names.  */
static void seed_sentinels(struct m8820x_cmmu *c)
{
	int k;
	for (k = 0; k < N_M88200_BATC_REGS; k++)
		c->batc[k] = MKBATC(SENT_LBA(k), SENT_PBA(k), SUPERVISOR_ENTRY);
}

static void program_all_ports(void)
{
	int n;
	for (n = 0; n < 8; n++)
		bwp(n, MKBATC(PORT_LBA(n), PORT_PBA(n), SUPERVISOR_ENTRY));
}

int main(void)
{
	uint64_t off;
	uint32_t v;
	int killed_r = 0, killed_w = 0, fault_r = 0, fault_w = 0;
	char buf[64];

	setvbuf(stdout, NULL, _IOLBF, 0);

	cpu = calloc(1, sizeof(struct cpu));
	machine = calloc(1, sizeof(struct machine));
	cmmu = calloc(1, sizeof(struct m8820x_cmmu));
	cmmu_d = calloc(1, sizeof(struct m8820x_cmmu));
	machine->cpus = calloc(1, sizeof(struct cpu *));
	machine->cpus[0] = cpu;
	cpu->machine = machine;
	cpu->cd.m88k.cmmu[0] = cmmu;
	cpu->cd.m88k.cmmu[1] = cmmu_d;
	cpu->invalidate_translation_caches = noop_invalidate;
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

	printf("--- A. NO offset in the window may terminate the host, either direction ---\n");
	for (off = 0; off < M8820X_LENGTH; off += 4) {
		switch (probe(off, MEM_READ))  { case 1: killed_r++; break;
		                                 case 2: fault_r++;  break; default: break; }
		switch (probe(off, MEM_WRITE)) { case 1: killed_w++; break;
		                                 case 2: fault_w++;  break; default: break; }
	}
	check_u("A1 offsets whose READ kills the host  (was 1007)", killed_r, 0);
	check_u("A2 offsets whose WRITE kills the host (was 1009)", killed_w, 0);
	/*  A FAULT is a harness bug, not a detection -- see the header.  */
	check_u("A3 harness faults, reads  (a signal death is NOT a kill)", fault_r, 0);
	check_u("A4 harness faults, writes", fault_w, 0);

	printf("--- B. the complaint is LATCHED: one report, not one per access ---\n");
	/*  A real boot writes CMMU_SCR 640,016 times in 132 s.  An unlatched complaint on a
	    guest-drivable path is the `cflood` class at ~a quarter megabyte per second.  */
	fresh();
	for (off = 0x800; off < 0x8c0; off += 4)
		access_word(off, MEM_READ, 0, NULL);
	check_u("B1 sixteen unhandled reads complain exactly once", fatal_calls, 1);
	check("B2   ...and the rest are still visible under -v",
	    debug_calls > 0 ? "yes" : "no", "yes");

	printf("--- C. the seven commands #433 folded are HANDLED, not dropped ---\n");
	{
		static const struct { uint32_t cmd; const char *nm; } folded[] = {
			{ CMMU_FLUSH_CACHE_INV_SEGMENT, "cache INV_SEGMENT" },
			{ CMMU_FLUSH_CACHE_CB_SEGMENT,  "cache CB_SEGMENT"  },
			{ CMMU_FLUSH_CACHE_CB_ALL,      "cache CB_ALL"      },
			{ CMMU_FLUSH_USER_LINE,         "PATC USER_LINE"    },
			{ CMMU_FLUSH_USER_SEGMENT,      "PATC USER_SEGMENT" },
			{ CMMU_FLUSH_SUPER_LINE,        "PATC SUPER_LINE"   },
			{ CMMU_FLUSH_SUPER_SEGMENT,     "PATC SUPER_SEGMENT"},
		};
		size_t i; int complained = 0;
		for (i = 0; i < sizeof(folded)/sizeof(folded[0]); i++) {
			fresh();
			access_word(CMMU_SCR * 4, MEM_WRITE, folded[i].cmd, NULL);
			if (fatal_calls != 0)
				complained++;
		}
		check_u("C1 none of the seven folded commands complains", complained, 0);
		/*  The control: a genuinely unimplemented command MUST still complain, or C1
		    would pass under a mutant that simply stopped complaining at all.  */
		fresh();
		access_word(CMMU_SCR * 4, MEM_WRITE, 0x2a, NULL);
		check_u("C2 CONTROL: an undefined command still complains once",
		    fatal_calls, 1);
		/*
		 *  C3 is the SECOND blind spot the R7 pass-2 agy seat named, and it is a
		 *  different latch from B1's.  B1 exercises reported_OFFSET; the command
		 *  path has its own reported_COMMAND flag, and C2 cannot see it, because
		 *  C2 issues ONE command -- and one command complains exactly once whether
		 *  the latch is set or not.  Deleting `d->reported_command = 1;` therefore
		 *  passes every other row while making a guest-drivable stderr flood: a
		 *  guest that writes an undefined command in a loop gets one line each.
		 *  Two commands is the smallest input that separates the two behaviours.
		 */
		fresh();
		access_word(CMMU_SCR * 4, MEM_WRITE, 0x2a, NULL);
		access_word(CMMU_SCR * 4, MEM_WRITE, 0x2b, NULL);
		check_u("C3 two undefined commands still complain exactly once",
		    fatal_calls, 1);
	}

	printf("--- D. THE ROW THAT DEFENDS THE FOLD: the PATC really is invalidated ---\n");
	/*
	 *  This is the row the whole round turns on, and survival cannot show it.  Before
	 *  #433 an unimplemented FLUSH_SUPER_LINE died loudly; converting the default arm to
	 *  complain-and-drop would have made it a SILENTLY IGNORED TLB FLUSH -- and
	 *  memory_m88k.c's translation fast path short-circuits on a valid PATC entry, so the
	 *  guest would keep translating through a torn-down mapping.  White-box: seed the
	 *  entry, issue the command, read the array back.
	 */
	{
		static const struct { uint32_t cmd; uint32_t sup; const char *nm; } fl[] = {
			{ CMMU_FLUSH_SUPER_LINE,    M8820X_PATC_SUPERVISOR_BIT, "SUPER_LINE" },
			{ CMMU_FLUSH_SUPER_SEGMENT, M8820X_PATC_SUPERVISOR_BIT, "SUPER_SEGMENT" },
			{ CMMU_FLUSH_USER_LINE,     0,                          "USER_LINE" },
			{ CMMU_FLUSH_USER_SEGMENT,  0,                          "USER_SEGMENT" },
		};
		size_t i; int still_valid = 0;
		for (i = 0; i < sizeof(fl)/sizeof(fl[0]); i++) {
			fresh();
			cmmu->reg[CMMU_SAR] = 0x12345000;
			cmmu->patc_v_and_control[0] = 0x12345000 | PG_V;
			cmmu->patc_p_and_supervisorbit[0] = 0x99999000 | fl[i].sup;
			access_word(CMMU_SCR * 4, MEM_WRITE, fl[i].cmd, NULL);
			if (cmmu->patc_v_and_control[0] & PG_V)
				still_valid++;
		}
		check_u("D1 all four folded PATC flushes invalidate the entry",
		    still_valid, 0);
		/*  The control: a CACHE command must NOT invalidate the PATC, or D1 would pass
		    under a mutant that invalidates on every command.  */
		fresh();
		cmmu->reg[CMMU_SAR] = 0x12345000;
		cmmu->patc_v_and_control[0] = 0x12345000 | PG_V;
		cmmu->patc_p_and_supervisorbit[0] = 0x99999000;
		access_word(CMMU_SCR * 4, MEM_WRITE, CMMU_FLUSH_CACHE_INV_SEGMENT, NULL);
		check("D2 CONTROL: a CACHE command leaves the PATC alone",
		    (cmmu->patc_v_and_control[0] & PG_V) ? "kept" : "WRONGLY FLUSHED", "kept");
	}

	printf("--- D3-D8. the fold's SEMANTICS, which D1/D2 do not reach ---\n");
	/*
	 *  D1 SEEDS ONE ENTRY AT THE FLUSHED ADDRESS, so it can only ever show that a matching
	 *  entry goes away.  Pass 2 measured what that misses: ELEVEN of twenty-one mutants
	 *  survived the first fifteen rows, and the cheapest was ONE DELETED CHARACTER --
	 *  removing the `!` from `if (!all && ...)` turns every FLUSH_*_ALL into a single-page
	 *  flush, which is precisely the silently-under-invalidating TLB the fold exists to
	 *  prevent.  These rows seed a SPREAD of entries and assert which ones SURVIVE, which
	 *  is the half D1 cannot see.
	 *
	 *  The fixture, with SAR deliberately NOT page-aligned so a LINE address is exercised:
	 *      e0  the SAR page, supervisor      e1  the SAR page, user
	 *      e2  same 4 MB segment, other page, supervisor
	 *      e3  same segment, other page, user
	 *      e4  a different segment, supervisor
	 *      e5  a different segment, user
	 */
	{
		int i;
		uint32_t surv;
		static const uint32_t SEG = 0xffc00000;	/*  memory_m88k.c:121, vaddr >> 22  */

		/*  seed(): rebuild the fixture before each command.  */
#define M8_SEED()							\
		do {							\
			fresh();					\
			cmmu->reg[CMMU_SAR] = 0x12345010;	/*  a LINE address  */ \
			cmmu->patc_v_and_control[0] = 0x12345000 | PG_V;	\
			cmmu->patc_p_and_supervisorbit[0] = 0x90000000 |	\
			    M8820X_PATC_SUPERVISOR_BIT;				\
			cmmu->patc_v_and_control[1] = 0x12345000 | PG_V;	\
			cmmu->patc_p_and_supervisorbit[1] = 0x91000000;		\
			cmmu->patc_v_and_control[2] = 0x12346000 | PG_V;	\
			cmmu->patc_p_and_supervisorbit[2] = 0x92000000 |	\
			    M8820X_PATC_SUPERVISOR_BIT;				\
			cmmu->patc_v_and_control[3] = 0x12346000 | PG_V;	\
			cmmu->patc_p_and_supervisorbit[3] = 0x93000000;		\
			cmmu->patc_v_and_control[4] = 0x56789000 | PG_V;	\
			cmmu->patc_p_and_supervisorbit[4] = 0x94000000 |	\
			    M8820X_PATC_SUPERVISOR_BIT;				\
			cmmu->patc_v_and_control[5] = 0x56789000 | PG_V;	\
			cmmu->patc_p_and_supervisorbit[5] = 0x95000000;		\
		} while (0)

		/*  surviving(): a bitmap of which of the six entries still have PG_V.  */
#define M8_SURV()	({ uint32_t _m = 0; int _i;				\
			for (_i = 0; _i < 6; _i++)				\
				if (cmmu->patc_v_and_control[_i] & PG_V)	\
					_m |= 1u << _i;				\
			_m; })

		/*  D3: a SUPER LINE flush must drop ONLY the supervisor entry on the SAR
		    page.  Under the deleted-`!` mutant and under LINE-treated-as-ALL this
		    changes, so it kills both.  Expected survivors: e1..e5 = 0x3e.  */
		M8_SEED();
		access_word(CMMU_SCR * 4, MEM_WRITE, CMMU_FLUSH_SUPER_LINE, NULL);
		surv = M8_SURV();
		check_u("D3 a SUPER LINE flush drops exactly one entry", surv, 0x3e);

		/*  D4: a SUPER ALL flush must drop EVERY supervisor entry and no user one.
		    This is the row that kills the one-character mutant: with `!` deleted,
		    e2 and e4 survive.  Expected survivors: e1,e3,e5 = 0x2a.  */
		M8_SEED();
		access_word(CMMU_SCR * 4, MEM_WRITE, CMMU_FLUSH_SUPER_ALL, NULL);
		surv = M8_SURV();
		check_u("D4 a SUPER ALL flush drops every supervisor entry", surv, 0x2a);

		/*  D5: and a USER ALL flush is its mirror -- privilege is respected in both
		    directions, so a single wrong comparison cannot pass both rows.  */
		M8_SEED();
		access_word(CMMU_SCR * 4, MEM_WRITE, CMMU_FLUSH_USER_ALL, NULL);
		surv = M8_SURV();
		check_u("D5 a USER ALL flush leaves every supervisor entry", surv, 0x15);

		/*
		 *  D6: SEGMENT is mapped to ALL, so it over-invalidates ACROSS segments.
		 *
		 *  THIS ROW WENT RED ON CORRECT CODE WHEN IT FIRST ASSERTED THE NAIVE THING --
		 *  that a SEGMENT flush spares another segment's entry.  It does not, and it is
		 *  not meant to: the fold deliberately maps SEGMENT onto ALL because
		 *  over-invalidation is safe in a model that re-walks the tables on a miss,
		 *  while under-invalidation is the defect the whole round exists to prevent.
		 *  "Did it fail for the reason under test?" -- it did not; the row was wrong.
		 *
		 *  So the property actually worth pinning is the SAFE DIRECTION: a SEGMENT
		 *  flush must be a strict SUPERSET of a PAGE flush and must still respect
		 *  privilege.  A mutant that narrowed SEGMENT to a genuine segment scope would
		 *  be an improvement in fidelity, not a defect -- but one that narrowed it
		 *  below PAGE would be exactly the under-invalidation this guards.
		 */
		M8_SEED();
		access_word(CMMU_SCR * 4, MEM_WRITE, CMMU_FLUSH_SUPER_PAGE, NULL);
		{
			uint32_t page_surv = M8_SURV();
			M8_SEED();
			access_word(CMMU_SCR * 4, MEM_WRITE, CMMU_FLUSH_SUPER_SEGMENT, NULL);
			surv = M8_SURV();
			/*  superset: every entry the SEGMENT flush left must also have been left
			    by the PAGE flush, i.e. SEGMENT's survivors are a subset of PAGE's.  */
			check("D6 a SEGMENT flush drops at least what a PAGE flush drops",
			    (surv & ~page_surv) == 0 ? "superset" : "UNDER-INVALIDATES",
			    "superset");
		}
		(void) SEG;

		/*
		 *  D6b: THE USER SIDE OF THE SAME PROPERTY, and it exists because a seat
		 *  named a mutant my own census had not run.
		 *
		 *  Every other flush-scope row here drives a SUPER command except D5, which is
		 *  USER *ALL* -- so deleting just `cmd == CMMU_FLUSH_USER_SEGMENT` from the
		 *  `all = 1` set made USER_SEGMENT page-granular instead of full-table and
		 *  SURVIVED all twenty-three rows.  The supervisor half was covered; the user
		 *  half was not.  A property worth pinning in one privilege direction is worth
		 *  pinning in both, and the asymmetry is exactly the kind a single-sided row
		 *  hides.
		 *
		 *  Expected: a USER SEGMENT flush drops every USER entry (e1, e3, e5) and no
		 *  supervisor one, i.e. survivors are e0, e2, e4 = 0x15 -- the same answer as
		 *  USER ALL in D5, which is what "SEGMENT takes ALL's settings" means.
		 */
		M8_SEED();
		access_word(CMMU_SCR * 4, MEM_WRITE, CMMU_FLUSH_USER_SEGMENT, NULL);
		surv = M8_SURV();
		check_u("D6b a USER SEGMENT flush drops every user entry", surv, 0x15);

		/*  D7: THE EMULATOR'S OWN TRANSLATION CACHE MUST BE PURGED TOO, and the
		    counter for it was already in this file and never asserted on.  Deleting
		    the invalidate_translation_caches() call leaves the PATC correct while the
		    dyntrans fast path keeps the torn-down mapping -- the round's stated
		    failure mode reached by another route.  */
		M8_SEED(); invalidate_calls = 0;
		access_word(CMMU_SCR * 4, MEM_WRITE, CMMU_FLUSH_SUPER_ALL, NULL);
		check_u("D7 a PATC flush also purges the emulator's own cache",
		    invalidate_calls, 1);
		/*  ...and a CACHE command must NOT: the control that stops D7 passing under
		    a mutant that invalidates unconditionally.  */
		M8_SEED(); invalidate_calls = 0;
		access_word(CMMU_SCR * 4, MEM_WRITE, CMMU_FLUSH_CACHE_INV_ALL, NULL);
		check_u("D8 CONTROL: a cache command purges nothing", invalidate_calls, 0);

		/*  D9: the default arm DROPS a write rather than storing it.  Storing would
		    make regs[] RAM-like and could satisfy a guest's write-then-verify probe
		    for a register the model does not implement.  */
		fresh();
		access_word(0x800, MEM_WRITE, 0xdeadbeef, NULL);
		access_word(0x800, MEM_READ, 0, &v);
		check_u("D9 an unhandled write is dropped, not stored", v, 0);

		/*  D10: and the SSR write is dropped for the same reason, which is what makes
		    the command arm's own argument true -- if a guest could set SSR's V bit,
		    a dropped PROBE would read back a plausible-looking VALID translation
		    instead of a deterministic miss.  The two decisions are coupled.  */
		fresh();
		access_word(CMMU_SSR * 4, MEM_WRITE, 0xffffffff, NULL);
		access_word(CMMU_SSR * 4, MEM_READ, 0, &v);
		check_u("D10 a guest SSR write cannot fake a valid translation", v, 0);
		i = 0; (void) i;
#undef M8_SEED
#undef M8_SURV
	}

	printf("--- E. values, not survival ---\n");
	/*  Rounds 79/80: a survival-only row cannot tell a repaired access from one that
	    merely stopped faulting.  The IDR value is the seed luna88k writes -- it can only
	    come back through the device.  */
	fresh();
	access_word(CMMU_IDR * 4, MEM_READ, 0, &v);
	check_u("E1 IDR still reads the seeded 88200 rev-9 id", v, 0x00a90000);
	fresh();
	access_word(0x800, MEM_READ, 0, &v);
	check_u("E2 an unhandled offset reads back as 0", v, 0);
	fresh();
	access_word(CMMU_IDR * 4, MEM_WRITE, 0xdeadbeef, NULL);
	access_word(CMMU_IDR * 4, MEM_READ, 0, &v);
	check_u("E3 a write to the read-only IDR does not corrupt it", v, 0x00a90000);
	fresh();
	access_word(CMMU_SCR * 4, MEM_WRITE, CMMU_FLUSH_SUPER_ALL, NULL);
	access_word(CMMU_SCR * 4, MEM_READ, 0, &v);
	check_u("E4 SCR reads back the last command written", v, CMMU_FLUSH_SUPER_ALL);

	printf("--- F. THE BWP/BATC ARM: the shadow array is a TRANSLATION INPUT ---\n");
	/*
	 *  The whole section is built so that a register read-back cannot satisfy it.  The
	 *  motivating mutant -- deleting `batc[i] = idata;` at dev_m8820x.c:479 while leaving
	 *  `regs[...] = idata` -- keeps write-then-read-back perfect and left both differentials
	 *  green at 25/25 and 27/27.  Every row below asks m88k_translate_v2p() instead.
	 */
	{
		int n, k, bad, bad2, bad3;
		uint64_t pa;

		/*  ------------------------------------------------ the controls --- */
		/*
		 *  F0a/F0b/F0c: THE ORACLE HAS RANGE.  Three different fixture states must give
		 *  three different answers, or "the expected physical address came back" is
		 *  compatible with a constant.  One control was not enough for a sibling probe
		 *  in this project -- its RAM control was green while every site returned 0x0.
		 */
		batc_fixture();
		bad = 0;
		for (n = 0; n < 8; n++)
			if (!walks(1, PORT_VA(n)))
				bad++;
		check_u("F0a CONTROL: with no BWP write, all eight blocks WALK", bad, 0);

		batc_fixture();
		cmmu->reg[CMMU_SAPR] = FAKE_SEGTAB_PA;		/*  APR_V clear  */
		check_u("F0b CONTROL: an invalid area pointer maps physical = virtual",
		    (uint64_t) (xlate(1, 0, 0, PORT_VA(0), &pa) == 2 &&
		                pa == (uint64_t) PORT_VA(0)), 1);

		batc_fixture();
		cmmu->reg[CMMU_SAPR] = FAKE_UNMAPPED_PA | APR_V;
		exception_calls = debugmsg_calls = 0;
		check_u("F0c CONTROL: unmapped tables FAIL, and take no exception path",
		    (uint64_t) (xlate(1, 0, 0, PORT_VA(0), &pa) == 0 &&
		                exception_calls == 0 && debugmsg_calls == 0), 1);

		/*  --------------------------------------- the motivating row --- */
		/*
		 *  F1: eight ports, eight DIFFERENT logical blocks, eight DIFFERENT physical
		 *  blocks, eight DIFFERENT in-block offsets.  Under the deleted-shadow mutant
		 *  all eight fall through to WALK_PA; under a wrong-index mutant the ones whose
		 *  slot was overwritten by a later port fall through too.
		 */
		batc_fixture();
		program_all_ports();
		bad = 0;
		for (n = 0; n < 8; n++)
			if (!maps_to(1, PORT_VA(n), PORT_PA(n)))
				bad++;
		check_u("F1 each BWP port programs ITS OWN block, read back by TRANSLATION",
		    bad, 0);

		/*
		 *  F2a/F2b: WHICH of the ten shadow slots a port write lands in, observed through
		 *  translation rather than by inspecting the array.  Ten distinct sentinels are
		 *  seeded first; the eight port writes must consume slots 0-7 and nothing else.
		 *
		 *  A pure "does each port resolve" row is BLIND TO A UNIFORM INDEX SHIFT -- the
		 *  translator scans all ten slots, so entries written one slot too high still
		 *  resolve.  F2b is what sees it: with `- CMMU_BWP0` shifted by one, slot 8's
		 *  sentinel is destroyed, and F2a sees slot 0's sentinel wrongly surviving.
		 */
		batc_fixture();
		seed_sentinels(cmmu);
		program_all_ports();
		bad = bad2 = 0;
		for (k = 0; k < 8; k++)
			if (!walks(1, SENT_VA(k)))
				bad++;		/*  a sentinel that outlived its port write  */
		for (k = 8; k < N_M88200_BATC_REGS; k++)
			if (!maps_to(1, SENT_VA(k), SENT_PA(k)))
				bad2++;		/*  a reserved slot that was clobbered  */
		check_u("F2a the eight ports consume exactly slots 0-7", bad, 0);
		check_u("F2b   ...and leave the two reserved slots untouched", bad2, 0);

		/*
		 *  F3/F4: WHICH CMMU.  memory_m88k.c:112 selects cmmu[instr? 0 : 1], so the CMMU
		 *  index is translation-observable even in a single-cpu fixture.  F3 drives the
		 *  DATA cmmu and reads it back with a DATA translate; F4 is the other half --
		 *  the instruction CMMU must be untouched, which a mutant writing both would
		 *  fail.  Neither row exists in the single-object form: with one cmmu object
		 *  `cmmu[d->cmmu_nr]` -> `cmmu[0]` lands in the same array either way.
		 */
		batc_fixture();
		dev.cmmu_nr = 1;
		program_all_ports();
		bad = bad2 = 0;
		for (n = 0; n < 8; n++) {
			if (!maps_to(0, PORT_VA(n), PORT_PA(n)))	/*  data side  */
				bad++;
			if (!walks(1, PORT_VA(n)))			/*  instr side  */
				bad2++;
		}
		check_u("F3 cmmu_nr 1 programs the DATA CMMU's shadow, seen by a data translate",
		    bad, 0);
		check_u("F4   ...and the instruction CMMU keeps no copy of it", bad2, 0);

		/*
		 *  F5: THE VALID BIT.  memory_m88k.c:156 skips an entry without BATC_V.  A port
		 *  write carrying V=0 must therefore create no mapping -- and the same word with
		 *  V set must create one, or the row would pass on a device that stored nothing.
		 *  Kills `batc[i] = idata | BATC_V` in the device AND the deleted `!` in the
		 *  translator's own valid test.
		 */
		batc_fixture();
		bwp(2, MKBATC(PORT_LBA(2), PORT_PBA(2), BATC_SO));		/*  V clear  */
		bad = walks(1, PORT_VA(2)) ? 0 : 1;
		bwp(2, MKBATC(PORT_LBA(2), PORT_PBA(2), SUPERVISOR_ENTRY));	/*  V set  */
		if (!maps_to(1, PORT_VA(2), PORT_PA(2)))
			bad++;
		check_u("F5 BATC_V decides: V=0 maps nothing, V=1 maps the block", bad, 0);

		/*
		 *  F6/F7: THE INVALIDATION DIRECTION, which is the dangerous one -- a guest that
		 *  tears an entry down and keeps translating through it is the whole reason the
		 *  shadow has to track the register.  Two shapes, because they die to different
		 *  mutants: writing a bare 0 is what an `&& idata` guard drops (that exact
		 *  one-token mutant survived sixteen rows in the sibling file), while writing a
		 *  nonzero word with V cleared is what a value-shaped guard drops.
		 */
		batc_fixture();
		bwp(3, MKBATC(PORT_LBA(3), PORT_PBA(3), SUPERVISOR_ENTRY));
		bad = maps_to(1, PORT_VA(3), PORT_PA(3)) ? 0 : 1;	/*  it must map first  */
		bwp(3, 0);
		if (!walks(1, PORT_VA(3)))
			bad++;
		check_u("F6 writing ZERO over a live entry removes the mapping", bad, 0);

		batc_fixture();
		bwp(4, MKBATC(PORT_LBA(4), PORT_PBA(4), SUPERVISOR_ENTRY));
		bad = maps_to(1, PORT_VA(4), PORT_PA(4)) ? 0 : 1;
		bwp(4, MKBATC(PORT_LBA(4), PORT_PBA(4), BATC_SO));	/*  nonzero, V clear  */
		if (!walks(1, PORT_VA(4)))
			bad++;
		check_u("F7 clearing V with a NONZERO word removes it too", bad, 0);

		/*
		 *  F8: THE SUPERVISOR BIT, both directions.  memory_m88k.c:160-161 requires
		 *  BATC_SO to agree with the access mode, so a single-direction row would pass
		 *  under a mutant that forced the bit one way.  Four observations.
		 */
		batc_fixture();
		bwp(5, MKBATC(PORT_LBA(5), PORT_PBA(5), BATC_SO | BATC_V));
		bad = 0;
		if (!maps_to(1, PORT_VA(5), PORT_PA(5)))	bad++;	/*  supervisor: hit   */
		if (xlate(1, 0, 1, PORT_VA(5), &pa) != 2 ||
		    pa != (uint64_t) WALKED(PORT_VA(5)))	bad++;	/*  user: must miss   */
		bwp(6, MKBATC(PORT_LBA(6), PORT_PBA(6), BATC_V));	/*  SO clear  */
		if (!walks(1, PORT_VA(6)))			bad++;	/*  supervisor: miss  */
		if (xlate(1, 0, 1, PORT_VA(6), &pa) != 2 ||
		    pa != (uint64_t) PORT_PA(6))		bad++;	/*  user: hit         */
		check_u("F8 BATC_SO reaches translation in BOTH privilege directions", bad, 0);

		/*
		 *  F9: THE WRITE-PROTECT BIT.  memory_m88k.c:171-179 turns BATC_PROT into a
		 *  denied write (return 0) and a read-only success (return 1).  This is the row
		 *  that pins the FLAG BITS of the stored word rather than its address fields --
		 *  `batc[i] = idata & 0xffffffc0` would pass F1-F4 outright.
		 */
		batc_fixture();
		bwp(7, MKBATC(PORT_LBA(7), PORT_PBA(7), BATC_PROT | SUPERVISOR_ENTRY));
		bad = 0;
		if (xlate(1, 0, 0, PORT_VA(7), &pa) != 1 ||
		    pa != (uint64_t) PORT_PA(7))	bad++;	/*  read: allowed, RO   */
		if (xlate(1, 1, 0, PORT_VA(7), &pa) != 0)	bad++;	/*  write: denied       */
		bwp(7, MKBATC(PORT_LBA(7), PORT_PBA(7), SUPERVISOR_ENTRY));
		if (xlate(1, 1, 0, PORT_VA(7), &pa) != 2 ||
		    pa != (uint64_t) PORT_PA(7))	bad++;	/*  no PROT: write ok   */
		check_u("F9 BATC_PROT reaches translation: RO read, denied write", bad, 0);

		/*
		 *  F10: THE OTHER HALF.  Every row above would stay green if the arm stopped
		 *  storing into regs[] -- the BWP ports are guest-readable and the register file
		 *  is a separate array.  This row is deliberately the VACUOUS-FOR-THE-SHADOW one,
		 *  named as such so nobody mistakes it for coverage of the shadow: it defends the
		 *  opposite mutant, and only that.
		 */
		batc_fixture();
		bad = 0;
		for (n = 0; n < 8; n++) {
			uint32_t seed = 0xb0000000u + (uint32_t) n * 0x01010101u, got;
			bwp(n, seed);
			access_word((uint64_t) (CMMU_BWP0 + n) * 4, MEM_READ, 0, &got);
			if (got != seed)
				bad++;
		}
		check_u("F10 the register half still stores and reads back, per port", bad, 0);

		/*
		 *  F11/F12: THE PURGE, both directions.  `if (old != idata)` at dev_m8820x.c:480
		 *  is a purge-on-CHANGE, and it is sound here for a reason the SAPR/UAPR arm's F4
		 *  cannot claim: an unchanged shadow word is an unchanged translation input, so
		 *  there is nothing to purge.  Pinning only "a write purges" would pass under a
		 *  mutant that purges unconditionally; pinning only "a redundant write does not"
		 *  would pass under one that never purges.  PER PORT, because a mutant gating the
		 *  purge on the index (`&& i < 4`) is invisible to a single-port row.
		 *
		 *  This is a SHAPE PIN as much as a correctness one, and it is recorded that way:
		 *  purging unconditionally would be wasteful, not wrong.  The direction that is
		 *  actually dangerous -- not purging when the entry DID change -- is F11.
		 */
		bad = bad2 = 0;
		for (n = 0; n < 8; n++) {
			batc_fixture();
			bwp(n, MKBATC(PORT_LBA(n), PORT_PBA(n), SUPERVISOR_ENTRY));
			if (invalidate_calls != 1)
				bad++;
			invalidate_calls = 0;
			bwp(n, MKBATC(PORT_LBA(n), PORT_PBA(n), SUPERVISOR_ENTRY));
			if (invalidate_calls != 0)
				bad2++;
		}
		check_u("F11 a CHANGING BWP write purges exactly once, per port", bad, 0);
		check_u("F12 a redundant same-value write purges nothing, per port", bad2, 0);

		/*
		 *  F13: THE EXACT WORD.  Translation reads four fields out of the shadow (V, SO,
		 *  PROT and the two block numbers) and ignores BATC_INH / BATC_GLOBAL / BATC_WT
		 *  entirely -- so a mutant masking those three is invisible to F1-F12 while still
		 *  corrupting what cpu_m88k.c:362-375 prints for the guest's BATC dump.  White-box
		 *  on the array is the only thing that sees it, and this row is honest about being
		 *  that: it is NOT evidence that the array feeds translation -- F1 is.
		 */
		batc_fixture();
		bad = 0;
		for (n = 0; n < 8; n++) {
			uint32_t w = MKBATC(PORT_LBA(n), PORT_PBA(n),
			    BATC_SO | BATC_V | BATC_INH | BATC_GLOBAL | BATC_WT |
			    ((n & 1) ? BATC_PROT : 0));
			bwp(n, w);
			if (cmmu->batc[n] != w)
				bad++;
		}
		check_u("F13 the shadow holds the EXACT 32-bit word, unmodelled bits included",
		    bad, 0);

		/*
		 *  F14: A READ MUST DISTURB NOTHING.  The sibling file records mutant C -- dropping
		 *  the braces so the store runs unconditionally -- and this arm is wide open to the
		 *  same shape: a guest READ of a BWP port would then write idata (0) into both the
		 *  register and the shadow, wiping a 512 KB mapping.  It is invisible to every row
		 *  above, because odata is snapshotted before the switch, so the FIRST read still
		 *  returns the right word and no row above reads a port before translating.  Read
		 *  every port twice, then re-check the mapping.
		 */
		batc_fixture();
		program_all_ports();
		bad = bad2 = bad3 = 0;
		for (n = 0; n < 8; n++) {
			uint32_t w = MKBATC(PORT_LBA(n), PORT_PBA(n), SUPERVISOR_ENTRY), r1, r2;
			access_word((uint64_t) (CMMU_BWP0 + n) * 4, MEM_READ, 0, &r1);
			access_word((uint64_t) (CMMU_BWP0 + n) * 4, MEM_READ, 0, &r2);
			if (r1 != w || r2 != w)
				bad++;
			if (!maps_to(1, PORT_VA(n), PORT_PA(n)))
				bad2++;
			if (invalidate_calls != 8)	/*  the eight programming writes, no more  */
				bad3++;
		}
		check_u("F14 reading a BWP port twice changes neither word nor mapping",
		    (uint64_t) (bad + bad2), 0);
		check_u("F15   ...and a read issues no purge either", bad3, 0);

		/*
		 *  F16: THE SHADOW IS CONSULTED BEFORE THE PATC, which is the specific claim that
		 *  makes a stale BATC entry dangerous rather than merely redundant -- the BATC
		 *  loop at memory_m88k.c:152-180 runs ahead of the PATC loop at :190-234 and
		 *  RETURNS on a match, so a wrong block mapping wins over a correct page mapping
		 *  for the same address.  No row above seeds the PATC, so swapping the two loops
		 *  was invisible to all of them.
		 *
		 *  The second half is the control that makes the first half mean something: with
		 *  the BATC entry torn down, the SAME PATC entry must be what answers.  Without
		 *  it, F16 would also pass on a build where the PATC entry was simply never
		 *  matched -- "the BATC won" and "there was nothing to beat" are different facts.
		 */
		batc_fixture();
		bwp(1, MKBATC(PORT_LBA(1), PORT_PBA(1), SUPERVISOR_ENTRY));
		cmmu->patc_v_and_control[0] = (PORT_VA(1) & 0xfffff000) | PG_V;
		cmmu->patc_p_and_supervisorbit[0] = 0x55555000 | M8820X_PATC_SUPERVISOR_BIT;
		bad = maps_to(1, PORT_VA(1), PORT_PA(1)) ? 0 : 1;
		bwp(1, 0);				/*  tear the block mapping down  */
		if (xlate(1, 0, 0, PORT_VA(1), &pa) != 2 ||
		    pa != (uint64_t) (0x55555000u | (PORT_VA(1) & 0xfff)))
			bad++;				/*  ...now the PATC entry answers  */
		check_u("F16 the shadow BATC is consulted BEFORE the PATC", bad, 0);

		/*
		 *  F17: THE BLOCK IS EXACTLY 512 KB, ASSERTED AT ITS TWO EDGES.
		 *
		 *  This row exists because a mutant found it: widening the virtual match to 1 MB
		 *  survived all forty-five rows and both differentials once the port table stopped
		 *  being adjacent (see the table note above).  Every other row probes ONE address
		 *  per block, and one address inside a region cannot measure how big the region
		 *  is.  Four observations per port -- the first byte in, the last byte in, the
		 *  byte immediately below and the byte immediately above -- pin both edges, so a
		 *  match that is too WIDE fails in the outside pair and one that is too NARROW
		 *  fails in the inside pair.  BATC_BLKSHIFT is 19 (thirdparty/m8820x_pte.h:191).
		 */
		batc_fixture();
		program_all_ports();
		bad = 0;
		for (n = 0; n < 8; n++) {
			uint32_t base = BLK(PORT_LBA(n));
			if (!maps_to(1, base, BLK(PORT_PBA(n))))
				bad++;				/*  first byte in    */
			if (!maps_to(1, base | 0x7ffff, BLK(PORT_PBA(n)) | 0x7ffff))
				bad++;				/*  last byte in     */
			if (!walks(1, base - 1))
				bad++;				/*  byte below       */
			if (!walks(1, base + 0x80000))
				bad++;				/*  byte above       */
		}
		check_u("F17 a block is EXACTLY 512 KB, pinned at both edges", bad, 0);
	}

	snprintf(buf, sizeof(buf), "%d", rows + 1);
	check("IDENTITY row count -- guards against a stale copy", buf, "46");

	printf("\n%d rows, %d failures\n", rows, fails);
	printf("DIFF_M8820X_%s\n", fails == 0 ? "PASS" : "FAIL");
	return fails ? 1 : 0;
}
