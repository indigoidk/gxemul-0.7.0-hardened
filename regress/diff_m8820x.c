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
static struct m8820x_cmmu *cmmu;

static void fresh(void)
{
	memset(cmmu, 0, sizeof(*cmmu));
	memset(&dev, 0, sizeof(dev));
	cmmu->reg[CMMU_IDR] = (M88200_ID << 21) | (9 << 16);
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
	machine->cpus = calloc(1, sizeof(struct cpu *));
	machine->cpus[0] = cpu;
	cpu->machine = machine;
	cpu->cd.m88k.cmmu[0] = cmmu;
	cpu->invalidate_translation_caches = noop_invalidate;
	fresh();

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

	snprintf(buf, sizeof(buf), "%d", rows + 1);
	check("IDENTITY row count -- guards against a stale copy", buf, "25");

	printf("\n%d rows, %d failures\n", rows, fails);
	printf("DIFF_M8820X_%s\n", fails == 0 ? "PASS" : "FAIL");
	return fails ? 1 : 0;
}
