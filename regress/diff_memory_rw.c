/*
 *  Offline differential for the SHIPPED memory slow path -- src/cpus/memory_rw.c.
 *
 *  WHY THIS EXISTS.  #430 changed where memory_rw() translates, and the defect it fixes is
 *  invisible to anything that only watches a guest boot: it needs two pages that are
 *  adjacent VIRTUALLY and NOT adjacent physically, which no rig in this tree can be made to
 *  produce on demand.  So the map is supplied by a stub and the whole thing runs offline.
 *
 *  IT IS THE REPOSITORY FILE.  memory_rw.c is never compiled on its own -- it is #included
 *  by the per-CPU files with MEMORY_RW #defined to the flavour's name (see
 *  tmp_ppc_tail.c:38).  This driver does exactly that, with NO family macro.
 *
 *  SAID CORRECTLY, because the first version of this comment gave a wrong reason: every
 *  family DOES get a MEM_<FAMILY> macro (generate_tail.c:107 emits one, and
 *  tmp_ppc_tail.c carries MEM_PPC).  What makes the no-macro build representative is
 *  narrower, and it is the fact that actually matters -- memory_rw.c only ever TESTS
 *  MEM_ALPHA, MEM_MIPS and MEM_M88K, so PPC/ARM/SH/RISC-V/i960 all compile the same
 *  text this driver compiles.  Nothing is transcribed; there is nothing to keep in sync.
 *
 *  SIX STUBS, and they are the whole scaffolding: debug(), fatal(), debugmsg_cpu(),
 *  machine_watchpoint_match(), memory_warn_about_unimplemented_addr(), and
 *  memory_paddr_to_hostaddr().  The last is the interesting one -- it is what lets the test
 *  paint known bytes into known physical pages.  The four real headers are included as-is.
 *
 *  THE FIXTURE, and why the expected values are ABSOLUTE.  The stub map is deliberately
 *  NON-MONOTONIC:
 *
 *      virtual page 0x010  ->  physical page 0x040, painted 0xaa
 *      virtual page 0x011  ->  physical page 0x020, painted 0xbb
 *      physical page 0x041 (the one that FOLLOWS 0x040 physically), painted 0xcc
 *
 *  A 4-byte read at 0x10ffe straddles the two virtual pages, so the correct answer is
 *  `aa aa bb bb`.  Before #430 it was `aa aa cc cc` -- the physically-following page.  The
 *  0xbb-versus-0xcc byte is the whole reproduction, and it is an absolute consequence of
 *  the fixture rather than anything read out of the source.  That matters: R4's review
 *  established that a row which reads its expected value from the code is green for any
 *  value of it (filed as `constblind`), so this file asserts painted bytes, never a
 *  constant re-derived from the thing under test.
 *
 *  WHAT IT PROVES, and what it does not.  It proves the SPLIT: that both pages are
 *  translated, that reads take bytes from the virtually-next page, that writes land there
 *  and leave the physically-next page alone, that a device at the head of a straddling
 *  access is handed only its own bytes, that a faulting tail now reports failure instead of
 *  returning OK, and -- the two rows that defend the design rather than the fix -- that a
 *  PHYSICAL access is NOT split, and that the split does not consume stack per page.  It
 *  does NOT prove INTEGRATION: that every machine still boots is a rig question and only the
 *  weekly battery answers it.
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

static int fatal_calls, debug_calls, debugmsg_calls, warn_calls;

void debug(const char *fmt, ...) { (void) fmt; debug_calls++; }
void fatal(const char *fmt, ...) { (void) fmt; fatal_calls++; }
void debugmsg_cpu(struct cpu *cpu, int subsystem, const char *name,
	int verbosity_required, const char *fmt, ...)
{
	(void) cpu; (void) subsystem; (void) name; (void) verbosity_required;
	(void) fmt;
	debugmsg_calls++;
}

int machine_watchpoint_match(struct machine *machine, uint64_t addr, uint64_t len)
{
	(void) machine; (void) addr; (void) len;
	return 0;
}

bool memory_warn_about_unimplemented_addr(struct cpu *cpu, struct memory *mem,
	int writeflag, uint64_t paddr, size_t len)
{
	(void) cpu; (void) mem; (void) writeflag; (void) paddr; (void) len;
	warn_calls++;
	return false;
}

/*
 *  Stack-depth probe.  memory_paddr_to_hostaddr() is reached once per page (or per
 *  memblock), so the spread of the addresses of ITS locals bounds how much stack the split
 *  consumed.  This is what makes "a loop, not recursion" a CHECKED property rather than a
 *  stylistic note: a recursive split measured ~160 bytes per page, so a 16 MB access cost
 *  640 KB of stack and a 256 MB one died against a default 8 MB limit.
 */
static uintptr_t sp_lo, sp_hi;
static int sp_armed;
static void sp_note(void)
{
	char probe;
	uintptr_t a = (uintptr_t) &probe;
	if (!sp_armed)
		return;
	if (sp_lo == 0 || a < sp_lo) sp_lo = a;
	if (a > sp_hi) sp_hi = a;
}

#define	NBLOCKS	64
static unsigned char *blocks[NBLOCKS];
static int n_p2h;

unsigned char *memory_paddr_to_hostaddr(struct memory *mem, uint64_t paddr, int writeflag)
{
	uint64_t idx = paddr >> BITS_PER_MEMBLOCK;

	(void) mem;
	n_p2h++;
	sp_note();
	if (idx >= NBLOCKS)
		return NULL;
	if (blocks[idx] == NULL) {
		if (writeflag == MEM_READ)
			return NULL;
		blocks[idx] = calloc(1, 1 << BITS_PER_MEMBLOCK);
	}
	return blocks[idx] + (paddr & ((1 << BITS_PER_MEMBLOCK) - 1));
}

#define	MEMORY_RW	test_memory_rw
#include "../src/cpus/memory_rw.c"
#undef MEMORY_RW

/* --------------------------------------------------------------- harness --- */

static int n_translations, xlat_fail_vpage = -1;

static int stub_translate_v2p(struct cpu *cpu, uint64_t vaddr,
	uint64_t *return_paddr, int flags)
{
	uint64_t vpage = vaddr >> 12;
	uint64_t ppage = vpage;

	(void) cpu; (void) flags;
	n_translations++;

	if ((int) vpage == xlat_fail_vpage)
		return 0;

	/*
	 *  A 1 KB-GRANULAR REGION, because 4 KB is not the smallest granule this tree can
	 *  produce and a split that assumes it is leaves the defect alive.  ARM descriptor
	 *  type 3 on a non-XScale core is a 1 KB page (memory_arm.c:198-207) and SH has
	 *  SH4_PTEL_SZ_1K; both return MEMORY_NOT_FULL_PAGE, i.e. exactly the case where a
	 *  translation is least uniform.  Virtual page 0x001 is modelled that way here:
	 *
	 *      0x1000..0x13ff -> physical 0x50000.. (painted 0xa1)
	 *      0x1400..0x17ff -> physical 0x30000.. (painted 0xb1)
	 *      physical 0x50400 is the decoy         (painted 0xc1)
	 *
	 *  A read at 0x13fe crosses a translation boundary WITHOUT crossing a 4 KB one, so a
	 *  4 KB split does not fire and the answer is the decoy.  This fixture is the review
	 *  seat's counterexample, kept.
	 */
	if (vpage == 0x001) {
		uint64_t base = (vaddr & 0x400) ? 0x30000 : 0x50000;
		*return_paddr = base + (vaddr & 0x3ff);
		return 2 | MEMORY_NOT_FULL_PAGE;
	}

	/*  THE NON-MONOTONIC PAIR: adjacent virtually, far apart physically.  */
	if (vpage == 0x010) ppage = 0x040;
	if (vpage == 0x011) ppage = 0x020;

	*return_paddr = (ppage << 12) | (vaddr & 0xfff);
	return 2;
}

static int n_utt;
static void stub_utt(struct cpu *cpu, uint64_t vaddr_page,
	unsigned char *host_page, int writeflag, uint64_t paddr_page)
{
	(void) cpu; (void) vaddr_page; (void) host_page; (void) writeflag;
	(void) paddr_page;
	n_utt++;
}

/*  A fake device that records the length it was handed.  */
static int dev_calls, dev_last_len;
static int fake_dev(struct cpu *cpu, struct memory *mem, uint64_t paddr,
	unsigned char *data, size_t len, int writeflag, void *extra)
{
	size_t i;
	(void) cpu; (void) mem; (void) paddr; (void) extra;
	dev_calls++;
	dev_last_len = (int) len;
	if (writeflag == MEM_READ)
		for (i = 0; i < len; i++)
			data[i] = 0xd0;
	return 1;
}

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
static void check_i(const char *name, long got, long want)
{
	char g[32], w[32];
	snprintf(g, sizeof(g), "%ld", got);
	snprintf(w, sizeof(w), "%ld", want);
	check(name, g, w);
}
static void hex(char *out, size_t outlen, const unsigned char *b, size_t n)
{
	size_t i;
	out[0] = '\0';
	if (b == NULL) { snprintf(out, outlen, "(null)"); return; }
	for (i = 0; i < n; i++)
		snprintf(out + strlen(out), outlen - strlen(out), "%s%02x",
		    i ? " " : "", b[i]);
}

static struct cpu *cpu;
static struct machine *machine;
static struct memory *mem;
static struct memory_device dev;

static void paint(void)
{
	memset(memory_paddr_to_hostaddr(mem, 0x040000, MEM_WRITE), 0xaa, 4096);
	memset(memory_paddr_to_hostaddr(mem, 0x041000, MEM_WRITE), 0xcc, 4096);
	memset(memory_paddr_to_hostaddr(mem, 0x020000, MEM_WRITE), 0xbb, 4096);
	/*  the 1 KB-granular fixture: two 1 KB regions and a decoy 1 KB below the second  */
	memset(memory_paddr_to_hostaddr(mem, 0x050000, MEM_WRITE), 0xa1, 1024);
	memset(memory_paddr_to_hostaddr(mem, 0x050400, MEM_WRITE), 0xc1, 1024);
	memset(memory_paddr_to_hostaddr(mem, 0x030000, MEM_WRITE), 0xb1, 1024);
}

int main(void)
{
	unsigned char buf[16];
	char got[128];
	int r;

	cpu = calloc(1, sizeof(struct cpu));
	machine = calloc(1, sizeof(struct machine));
	mem = calloc(1, sizeof(struct memory));

	cpu->machine = machine;
	cpu->mem = mem;
	cpu->translate_v2p = stub_translate_v2p;
	cpu->update_translation_table = stub_utt;
	cpu->running = true;

	mem->physical_max = (uint64_t) NBLOCKS << BITS_PER_MEMBLOCK;
	mem->mmap_dev_minaddr = 1;	/*  min > max == "no devices"  */
	mem->mmap_dev_maxaddr = 0;
	paint();

	{
		/*
		 *  SELFCHECK -- CAN THIS FILE'S COMPARATOR STILL FAIL?
		 *
		 *  Feed check() a mismatch and require the failure counter to move, then un-record
		 *  it so the row is free.  If check() has been stubbed, neutered, or had its
		 *  comparison edited away, EVERY other row in this file is silently inert and the
		 *  gate cannot tell -- measured: 118 rows across five detectors stayed green under
		 *  exactly that stub, row counts, identity rows and verdict tokens intact.
		 *
		 *  This does NOT prove any particular row is correct.  It proves the file can still
		 *  say FAIL.  Read it as a liveness sentinel and nothing more; the per-harness
		 *  self-mutant in gate 2 covers a different failure (a fixture that stops reaching
		 *  the code), and neither substitutes for the other.
		 */
		int selfcheck_f = fails, selfcheck_r = rows;
		check("SELFCHECK the comparator can still fail", "a", "b");
		if (fails != selfcheck_f + 1) {
			printf("  FAIL  SELFCHECK: check() no longer compares -- every row in "
			    "this file is inert\n");
			fails = selfcheck_f + 1;
			rows = selfcheck_r;
		} else {
			fails = selfcheck_f;
			rows = selfcheck_r;
		}
	}

	printf("--- A. control: an access wholly inside one page is untouched ---\n");
	memset(buf, 0, sizeof(buf));
	test_memory_rw(cpu, mem, 0x10000, buf, 4, MEM_READ, CACHE_DATA);
	hex(got, sizeof(got), buf, 4);
	check("A1 in-page read", got, "aa aa aa aa");

	printf("--- B. THE REPRODUCTION: a straddling READ ---\n");
	/*  0xbb is the virtually-next page; 0xcc is the physically-next one.  Before #430
	    this row returned `aa aa cc cc`.  */
	memset(buf, 0, sizeof(buf));
	n_translations = 0; n_utt = 0;
	test_memory_rw(cpu, mem, 0x10ffe, buf, 4, MEM_READ, CACHE_DATA);
	hex(got, sizeof(got), buf, 4);
	check("B1 straddling read takes the VIRT-next page", got, "aa aa bb bb");
	check_i("B2   it translates once per page", n_translations, 2);
	check_i("B3   and maps each page it touched", n_utt, 2);

	printf("--- C. a straddling WRITE, which is the worse half ---\n");
	/*  The old code did not merely read the wrong page: it CORRUPTED one.  C2 and C3 are
	    the two halves of that -- the intended page was left unmodified while an unrelated
	    physical page was overwritten.  */
	memset(buf, 0x77, sizeof(buf));
	test_memory_rw(cpu, mem, 0x10ffe, buf, 4, MEM_WRITE, CACHE_DATA);
	hex(got, sizeof(got), memory_paddr_to_hostaddr(mem, 0x040ffe, MEM_READ), 2);
	check("C1 the head page took its bytes", got, "77 77");
	hex(got, sizeof(got), memory_paddr_to_hostaddr(mem, 0x020000, MEM_READ), 2);
	check("C2 the VIRT-next page took the tail", got, "77 77");
	hex(got, sizeof(got), memory_paddr_to_hostaddr(mem, 0x041000, MEM_READ), 2);
	check("C3 the PHYS-next page was NOT corrupted", got, "cc cc");
	paint();

	printf("--- D. a straddling access that STARTS INSIDE A DEVICE ---\n");
	/*  THE ROW THAT SETTLED THE DESIGN.  A late split (after device dispatch) leaves this
	    case broken: the device length clamp truncates len and the zero-fill supplies the
	    rest, so the guest gets `d0 d0 00 00`.  Measured -- it is why the split is placed
	    before dispatch rather than at the memblock check.  */
	dev.baseaddr = 0x040000; dev.endaddr = 0x041000; dev.length = 0x1000;
	dev.flags = DM_DEFAULT; dev.name = "fake"; dev.f = fake_dev;
	mem->devices = &dev; mem->n_mmapped_devices = 1;
	mem->last_accessed_device = 0;
	mem->mmap_dev_minaddr = 0x040000; mem->mmap_dev_maxaddr = 0x041000;
	dev_calls = 0; dev_last_len = -1;
	memset(buf, 0, sizeof(buf));
	test_memory_rw(cpu, mem, 0x10ffe, buf, 4, MEM_READ, CACHE_DATA);
	hex(got, sizeof(got), buf, 4);
	check("D1 device head, RAM tail, both correct", got, "d0 d0 bb bb");
	check_i("D2   the device was handed only its own bytes", dev_last_len, 2);
	mem->devices = NULL; mem->n_mmapped_devices = 0;
	mem->mmap_dev_minaddr = 1; mem->mmap_dev_maxaddr = 0;

	printf("--- E. a faulting TAIL is now a reported failure, not a silent wrong page ---\n");
	/*  Measured on the old code: it returned MEMORY_ACCESS_OK and wrote the wrong page
	    anyway.  So this was a MISSING FAULT as well as a wrong-page bug.  */
	paint();
	xlat_fail_vpage = 0x011;
	memset(buf, 0x55, sizeof(buf));
	r = test_memory_rw(cpu, mem, 0x10ffe, buf, 4, MEM_WRITE, CACHE_DATA);
	xlat_fail_vpage = -1;
	check_i("E1 a straddling write with a bad tail returns FAILED", r, 0);
	hex(got, sizeof(got), memory_paddr_to_hostaddr(mem, 0x041000, MEM_READ), 2);
	check("E2   and still did not touch the PHYS-next page", got, "cc cc");

	paint();
	xlat_fail_vpage = 0x011;
	memset(buf, 0x11, sizeof(buf));
	r = test_memory_rw(cpu, mem, 0x10ffe, buf, 4, MEM_READ, CACHE_DATA);
	xlat_fail_vpage = -1;
	check_i("E3 a straddling read with a bad tail returns FAILED", r, 0);
	hex(got, sizeof(got), buf, 4);
	/*  PARTIAL COMPLETION IS RECORDED, NOT FIXED: the head is kept and the tail is
	    deterministically zeroed by #244.  The old code had this property too (the
	    memblock split at the end of the worker still does), so the split does not
	    introduce it.  Atomicity is a separate question and is filed, not chased.  */
	check("E4   head kept, tail zeroed (partial, by design)", got, "aa aa 00 00");

	printf("--- G. a 1 KB mapping: the granule a 4 KB split silently misses ---\n");
	/*  THE ROW A REVIEW SEAT FORCED, and it caught a real hole: the first version of this
	    split used the 4 KB mask, so this access -- which crosses a translation boundary but
	    NOT a 4 KB one -- never entered the loop and returned the decoy.  */
	paint();
	memset(buf, 0, sizeof(buf));
	n_translations = 0;
	test_memory_rw(cpu, mem, 0x13fe, buf, 4, MEM_READ, CACHE_DATA);
	hex(got, sizeof(got), buf, 4);
	check("G1 a read across a 1 KB mapping boundary", got, "a1 a1 b1 b1");
	check_i("G2   and it translated both 1 KB regions", n_translations, 2);

	printf("--- H. a fault on the FIRST chunk still zeroes the WHOLE read buffer ---\n");
	/*  #244 promises a failed read leaves the caller's buffer deterministically zeroed, and
	    splitting broke that: the worker zeroes only the chunk IT was handed, so a failure
	    before the last chunk left the rest as the caller's uninitialised stack.  Unsplit,
	    one call covered the whole length.  The E rows fail the TAIL and cannot see this;
	    this row fails the HEAD.  */
	paint();
	xlat_fail_vpage = 0x010;
	memset(buf, 0x55, sizeof(buf));
	r = test_memory_rw(cpu, mem, 0x10ffe, buf, 4, MEM_READ, CACHE_DATA);
	xlat_fail_vpage = -1;
	check_i("H1 a first-chunk fault returns FAILED", r, 0);
	hex(got, sizeof(got), buf, 4);
	check("H2   and no byte of the buffer is left uninitialised", got, "00 00 00 00");

	printf("--- Z. a ONE-BYTE tail, which an off-by-one in the loop test hides behind ---\n");
	/*  MEASURED BY A REVIEW SEAT'S FUZZER, not by these rows: changing the loop test from
	    `len > granule - offset` to `... + 1` passed all twenty-one rows above while
	    diverging from a per-byte reference 1089 times.  Every row above happens to leave a
	    tail of two bytes or more.  These two give the loop a tail of exactly ONE, at both
	    granule edges.  */
	paint();
	memset(buf, 0, sizeof(buf));
	test_memory_rw(cpu, mem, 0x13ff, buf, 2, MEM_READ, CACHE_DATA);
	hex(got, sizeof(got), buf, 2);
	check("Z1 a 1-byte tail across the 1 KB edge", got, "a1 b1");
	memset(buf, 0, sizeof(buf));
	test_memory_rw(cpu, mem, 0x10fff, buf, 2, MEM_READ, CACHE_DATA);
	hex(got, sizeof(got), buf, 2);
	check("Z2 a 1-byte tail across the 4 KB edge", got, "aa bb");

	printf("--- F. the design rows: what must NOT be split, and what must not cost stack ---\n");
	/*  F1 defends the PHYSICAL exemption.  Under PHYSICAL there is no per-page map to
	    redo, so a 16 MB DMA must still cost one call per MEMBLOCK (16), not one per page
	    (4096).  Without the exemption this row reads 4096.  */
	{
		unsigned char *big = calloc(1, 16 << 20);
		int bi;
		for (bi = 4; bi < 21; bi++)
			(void) memory_paddr_to_hostaddr(mem, (uint64_t) bi << 20, MEM_WRITE);
		n_p2h = 0;
		test_memory_rw(cpu, mem, 0x400000, big, 16 << 20, MEM_READ,
		    CACHE_NONE | PHYSICAL);
		check_i("F1 a 16 MB PHYSICAL access splits per MEMBLOCK, not per page",
		    n_p2h, 16);
		free(big);
	}
	/*  F2 defends the loop.  A recursive split measured ~160 bytes of stack per page, so
	    this same access spanned ~640 KB.  The bound below is ABSOLUTE -- it is not derived
	    from anything in the source, so it notices a return to recursion.  */
	{
		unsigned char *big = calloc(1, 16 << 20);
		long span;
		n_p2h = 0; n_translations = 0;
		sp_lo = sp_hi = 0; sp_armed = 1;
		test_memory_rw(cpu, mem, 0x400000, big, 16 << 20, MEM_READ, CACHE_NONE);
		sp_armed = 0;
		span = (long) (sp_hi - sp_lo);
		/*  16 MB at a 1 KB granule.  The number is large on purpose: it is what
		    "the split really is 1 KB" looks like from outside, and it moves if the
		    granule is ever widened back.  */
		check_i("F3 a 16 MB translated access translates once per 1 KB",
		    n_translations, 16384);
		snprintf(got, sizeof(got), "%s", span < 4096 ? "flat" : "GROWS PER PAGE");
		printf("        (measured stack span %ld bytes)\n", span);
		check("F2 the split is a loop: stack does not grow per page", got, "flat");
		free(big);
	}

	/*  IDENTITY, as every differential here carries: a row count asserted against itself,
	    so a truncated or half-copied file cannot report a clean run of fewer rows.  The
	    gate floors the count at exactly this number too.  */
	snprintf(got, sizeof(got), "%d", rows + 1);
	check("IDENTITY row count -- guards against a stale copy", got, "23");

	printf("\n%d rows, %d failures   (fatal=%d debug=%d debugmsg=%d warn=%d)\n",
	    rows, fails, fatal_calls, debug_calls, debugmsg_calls, warn_calls);
	printf("DIFF_MEMORY_RW_%s\n", fails == 0 ? "PASS" : "FAIL");
	return fails ? 1 : 0;
}
