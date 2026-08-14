/*
 *  #405: offline differential of the REAL ATA IDENTIFY capacity packing.
 *
 *  Same construction as regress/diff_sh4_tmu.c and for the same reason:
 *  wdc_initialize_identify_struct() is static, so this driver stubs what it
 *  needs and #includes dev_wdc.c, and the function that runs is the one that
 *  ships. Deleting the include does not weaken the test, it fails to compile.
 *  (That is the honest form of the claim -- it does not make a transcription
 *  IMPOSSIBLE, only unable to happen silently.)
 *
 *  THE DEFECT. Six of the eight capacity lines used `% 255` where `& 255` is
 *  meant. The two that were already correct are the ones whose operand cannot
 *  exceed a byte; every other line shifts without pre-masking, so `% 255` is a
 *  base-256 digit sum rather than byte extraction:
 *      x % 255 == ((x >> 8) + (x & 255)) % 255      (0 counterexamples over 2^26)
 *  Above the threshold it is wrong 100% of the time. Worst case announces ZERO
 *  SECTORS for a real disk.
 *
 *  *** THE TRAP THIS TABLE EXISTS TO AVOID: `%` and `&` AGREE for every operand
 *  below 255, so EVERY disk size under 33,423,360 bytes passes on the UNFIXED
 *  code. A table of plausible-looking sizes proves nothing. Each row below is
 *  chosen to put a specific byte at or above the divergence point, and says
 *  which. ***
 *
 *  THE CONSISTENCY ORACLE NEEDS NO SPECIFICATION. There is no ATA document in
 *  this tree, so the absolute encoding of words 57-58 / 60-61 cannot be cited.
 *  But diskimage_recalc_size() (diskimage.c:254-268) rounds every image up to a
 *  whole number of cylinders, so the sector count IS the product of the geometry
 *  words in the same block -- and the block can therefore be checked against
 *  ITSELF.
 *
 *  #407 CORRECTION, and it is a correction to THIS FILE'S OWN RECORD. The
 *  original text here claimed "65,471 of 65,535 cylinder counts produce a
 *  self-contradicting block, the first at 65 cylinders". That number is true for
 *  H=16 -- the geometry diskimage.c:255-256 actually pins -- but the loop below
 *  used H=15 and stopped at c=2000, so what it really printed on reverted code
 *  was "1931 of 2000, first at 70". Both figures are true; they belong to
 *  different geometries. The loop now uses the REAL H=16 and runs to 65535, so
 *  the comment and the measurement finally describe the same thing.
 *
 *  #407: THE RECORDED "KNOWN SURVIVOR" WAS WRONG, and it was wrong in the
 *  flattering direction. It claimed a compensating pair -- swap +0/+1 in the
 *  eight capacity lines AND swap the two transmit pushes -- was invisible here.
 *  BUILT AND MEASURED: that pair produces EIGHT FAILURES. So does the packing
 *  swap alone. The transmit swap alone produces zero, which is the real gap
 *  (see below). The mutation that IS guest-invisible is the WHOLE-STRUCT swap
 *  plus the transmit swap -- which this comment never described -- and the
 *  word-53 anchor CATCHES even that, nine failures, reporting "02 00, want
 *  00 02". The anchor therefore earns its keep against a mutation nobody
 *  anticipated. Word 47 is 0x8080, a byte-swap palindrome, and would have been
 *  useless for it.
 *
 *  *** THE ACTUAL BLIND SPOT, recorded honestly and NOT closed here: the
 *  transmit loop -- the `for (i=0; i<sizeof(d->identify_struct); i+=2)` inside
 *  wdc_command()'s WDCC_IDENTIFY case -- is entirely ungated. Swapping its two
 *  pushes byte-swaps every IDENTIFY word a guest reads -- 4,096 heads, 13,330
 *  cylinders -- at ZERO failures, because this driver reads identify_struct
 *  DIRECTLY rather than through the path the guest uses. Closing it needs a
 *  different harness (drive wdc_command(WDCC_IDENTIFY) then dev_wdc_access on
 *  wd_data), which is new machinery rather than another row, so it is filed. ***
 *
 *  #408: THAT CITATION USED TO BE A LINE NUMBER AND IT WENT STALE TWICE.
 *  #405's references were +31 off (the length of its own inserted comment);
 *  #407 "corrected" them and was itself +9 off, from the identical mechanism,
 *  while carrying a comment that said to re-read line references after editing.
 *  Naming the construct is the fix that does not need repeating.
 *
 *  THE BUILD FLAGS BELOW ARE LOAD-BEARING FOR CORRECTNESS, NOT SPEED. This file
 *  needs -ffunction-sections -fdata-sections -Wl,--gc-sections to LINK at all
 *  (otherwise: undefined debug, quiet_mode, diskimage_access, diskimage_exist,
 *  machine_add_tickfunction). gate_offline.sh passes them. Do not "simplify"
 *  them away.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>

/*  Externals the identify path reaches. Sizes come from the row under test.  */
static uint64_t stub_size = 0;
static const char *stub_name = "GXemul regress disk";

void fatal(const char *fmt, ...)
{
	va_list ap;
	va_start(ap, fmt);
	vfprintf(stderr, fmt, ap);
	va_end(ap);
}

#include "../src/devices/dev_wdc.c"

/*
 *  DEFINITIONS, not macros -- diskimage.h declares real prototypes and a #define
 *  collides with them. They also have to come AFTER the include: `struct
 *  machine` is not a known type until the device file's own headers have been
 *  pulled in, and defining them first produces "conflicting types" against the
 *  very prototypes they are meant to satisfy.
 */
/*
 *  #407: THE STUB MUST DEPEND ON `id`, and that is not tidiness.
 *
 *  While it ignored id, the SMALLEST SURVIVING MUTANT in the whole file was ten
 *  characters -- delete `d->drive + ` from dev_wdc.c:179 -- which makes the
 *  SLAVE announce the MASTER's capacity, and passed all ten rows. Measured on a
 *  100-cylinder master with a 300-cylinder slave: drive 1 reported 100,800
 *  sectors while still reporting 300 cylinders, a block contradicting its own
 *  geometry, which is precisely what the oracle below claims to guard.
 *
 *  So each drive id gets a distinct size, and row_slave() below reads drive 1.
 */
static uint64_t stub_size_for[8] = { 0, 0, 0, 0, 0, 0, 0, 0 };
static int stub_size_for_active = 0;

/*
 *  #408: NO FALLBACK WHEN THE PER-ID TABLE IS ACTIVE.
 *
 *  #407's version fell back to the single `stub_size` for any id outside the two
 *  it populated, and row_slave() set that fallback to the SLAVE's size -- so an
 *  id that was off by one still returned the correct answer and the mutant
 *  `id + 1` SURVIVED. A stub that answers correctly for an id nobody asked about
 *  is not a stub, it is a second implementation.  Poison instead.
 */
int64_t diskimage_getsize(struct machine *machine, int id, int type)
{
	(void)machine; (void)type;
	if (stub_size_for_active) {
		if (id < 0 || id >= 8)
			return 0;
		return (int64_t) stub_size_for[id];	/*  0 = poison  */
	}
	return (int64_t) stub_size;
}

int diskimage_is_a_cdrom(struct machine *machine, int id, int type)
{
	(void)machine; (void)id; (void)type;
	return 0;
}

int diskimage_is_a_tape(struct machine *machine, int id, int type)
{
	(void)machine; (void)id; (void)type;
	return 0;
}

int diskimage_getname(struct machine *machine, int id, int type,
	char *buf, size_t bufsize)
{
	(void)machine; (void)id; (void)type;
	snprintf(buf, bufsize, "%s", stub_name);
	return 1;
}

static int rows = 0, failures = 0;

/*  A 16-bit IDENTIFY word, assembled the way the transmit path presents it.  */
static uint32_t word(struct wdc_data *d, int w)
{
	return (d->identify_struct[2 * w + 0] << 8) | d->identify_struct[2 * w + 1];
}

static uint64_t sectors_from_block(struct wdc_data *d, int lo, int hi)
{
	return ((uint64_t)word(d, hi) << 16) | word(d, lo);
}

/*
 *  #408: A REAL struct cpu, BECAUSE PASSING NULL WAS UNDEFINED BEHAVIOUR.
 *
 *  wdc_initialize_identify_struct() dereferences cpu->machine three times (the
 *  diskimage_getsize, diskimage_is_a_cdrom and diskimage_getname calls). #405
 *  and #407 both passed NULL, and it "worked" only because -O2 inlines the stubs
 *  and deletes the load. MEASURED: the same driver SEGFAULTS at -O0 and at -O1
 *  (exit 139). That is not a latent nicety -- it means the gate's optimisation
 *  flags were load-bearing for CORRECTNESS, and a future "build regress at -O0 to
 *  debug this" would have turned the gate red in a way that looks exactly like a
 *  capability regression.
 */
static struct machine stub_machine;
static struct cpu     stub_cpu;

static struct cpu *fake_cpu(void)
{
	memset(&stub_machine, 0, sizeof(stub_machine));
	memset(&stub_cpu, 0, sizeof(stub_cpu));
	stub_cpu.machine = &stub_machine;
	return &stub_cpu;
}

static void build(struct wdc_data *d, uint64_t sectors, int c, int h, int s)
{
	memset(d, 0, sizeof(*d));
	d->cyls[0] = c;
	d->heads[0] = h;
	d->sectors_per_track[0] = s;
	stub_size = sectors * 512;
	stub_size_for_active = 0;			/*  single-drive rows  */
	wdc_initialize_identify_struct(fake_cpu(), d);
}

/*
 *  One row: an exact sector count, asserted through BOTH capacity word pairs
 *  (57-58 "current capacity" and 60-61 "total addressable"). `why` names the
 *  byte this row puts at or past the divergence point -- a row that cannot say
 *  that is a row that would pass unfixed.
 */
static void row(const char *why, uint64_t sectors)
{
	struct wdc_data d;
	uint64_t got57, got60;

	build(&d, sectors, 1, 1, 1);
	got57 = sectors_from_block(&d, 57, 58);
	got60 = sectors_from_block(&d, 60, 61);
	rows ++;

	if (got57 != sectors || got60 != sectors) {
		printf("  FAIL %-38s sectors=%llu -> 57/58=%llu 60/61=%llu\n",
		    why, (unsigned long long)sectors,
		    (unsigned long long)got57, (unsigned long long)got60);
		failures ++;
	} else {
		printf("  ok   %-38s %llu\n", why, (unsigned long long)sectors);
	}
}

/*
 *  The anchor. Word 53's bytes are 0x00,0x02 -- asymmetric, so a +0/+1 swap in
 *  the packing is visible here. Word 47 (0x8080) is a palindrome and would not
 *  be, which is exactly why it is not used.
 */
static void row_anchor(void)
{
	struct wdc_data d;

	build(&d, 1024, 1, 1, 1);
	rows ++;
	if (d.identify_struct[2 * 53 + 0] != 0x00 ||
	    d.identify_struct[2 * 53 + 1] != 0x02) {
		printf("  FAIL word-53 anchor: %02x %02x, want 00 02"
		    " (a +0/+1 swap in the packing)\n",
		    d.identify_struct[2 * 53 + 0], d.identify_struct[2 * 53 + 1]);
		failures ++;
	} else {
		printf("  ok   %-38s word 53 = 00 02\n", "packing anchor (non-palindromic)");
	}
}

/*
 *  #407: THE SLAVE ROW. Kills the smallest surviving mutant in the file -- ten
 *  characters, deleting `d->drive + ` from dev_wdc.c:179 -- which made drive 1
 *  report drive 0's capacity while still reporting its own geometry. It passed
 *  all ten of the original rows because every one of them left d->drive at 0.
 */
static void row_slave(void)
{
	struct wdc_data d;
	uint64_t master = 100ULL * 16 * 63;	/*  100 cylinders  */
	uint64_t slave  = 300ULL * 16 * 63;	/*  300 cylinders  */
	uint64_t got;
	int bad = 0;

	memset(&d, 0, sizeof(d));
	d.drive = 1;
	d.cyls[0] = 100; d.heads[0] = 16; d.sectors_per_track[0] = 63;
	d.cyls[1] = 300; d.heads[1] = 15; d.sectors_per_track[1] = 17;
	memset(stub_size_for, 0, sizeof(stub_size_for));
	stub_size_for[0] = master * 512;
	stub_size_for[1] = slave  * 512;
	stub_size = 0;				/*  poison: no fallback answer  */
	stub_size_for_active = 1;
	wdc_initialize_identify_struct(fake_cpu(), &d);
	stub_size_for_active = 0;

	rows ++;
	got = sectors_from_block(&d, 60, 61);
	if (got != slave) {
		printf("  FAIL %-38s drive 1 says %llu, want %llu\n",
		    "the SLAVE reports its own capacity",
		    (unsigned long long)got, (unsigned long long)slave);
		bad = 1;
	}

	/*
	 *  #408: THE GEOMETRY HALF, which #407 left open. It closed the mutant that
	 *  made the slave report the master's CAPACITY and never checked that the
	 *  slave reports its own CYLINDERS, HEADS and SECTORS. Measured: four
	 *  mutants -- cyls[d->drive]->cyls[0], heads[...]->heads[0],
	 *  sectors_per_track[...]->[0], on both bytes -- all SURVIVED the 12 rows.
	 *  Master and slave are given DELIBERATELY DIFFERENT geometries (16/63 vs
	 *  15/17) so that reading the wrong drive's field cannot coincide.
	 */
	if (word(&d, 1) != 300 || word(&d, 3) != 15 || word(&d, 6) != 17) {
		printf("  FAIL %-38s drive 1 reports c=%u h=%u s=%u, want 300/15/17\n",
		    "the SLAVE reports its own geometry",
		    word(&d, 1), word(&d, 3), word(&d, 6));
		bad = 1;
	}

	if (bad)
		failures ++;
	else
		printf("  ok   %-38s %llu sectors, c=300 h=15 s=17\n",
		    "the SLAVE reports its own capacity+geometry",
		    (unsigned long long)got);
}

/*
 *  #408: base_drive IS NOT HYPOTHETICAL -- dev_wdc_init() sets it to 2 for the
 *  SECONDARY controller (the 0x170 address arm), so every access on that
 *  controller adds it. #407's slave row never varied it, and MEASURED, dropping
 *  `+ d->base_drive` from all three call sites SURVIVED every row. Here drive 0
 *  of a base_drive=2 controller must read diskimage id 2, and ids 0/1 are poison
 *  so borrowing the primary controller's disk cannot look correct.
 */
static void row_base_drive(void)
{
	struct wdc_data d;
	uint64_t want = 500ULL * 16 * 63;
	uint64_t got;

	memset(&d, 0, sizeof(d));
	d.drive = 0;
	d.base_drive = 2;
	d.cyls[0] = 500; d.heads[0] = 16; d.sectors_per_track[0] = 63;
	memset(stub_size_for, 0, sizeof(stub_size_for));
	stub_size_for[2] = want * 512;		/*  ids 0,1,3.. stay poison  */
	stub_size = 0;
	stub_size_for_active = 1;
	wdc_initialize_identify_struct(fake_cpu(), &d);
	stub_size_for_active = 0;

	rows ++;
	got = sectors_from_block(&d, 60, 61);
	if (got != want) {
		printf("  FAIL %-38s got %llu, want %llu (base_drive ignored?)\n",
		    "base_drive reaches the diskimage id",
		    (unsigned long long)got, (unsigned long long)want);
		failures ++;
	} else {
		printf("  ok   %-38s id 2 -> %llu sectors\n",
		    "base_drive reaches the diskimage id",
		    (unsigned long long)got);
	}
}

/*
 *  #407: WORD 49 MUST STAY ZERO, and this row is worth one character of mutant.
 *  Setting dev_wdc.c:236 to 2 advertises LBA and passed all ten original rows.
 *  It is not cosmetic: the LBA offset arms in wdc__read/wdc__write are `#if 0`
 *  (:315-321, :361-367), the live offsets at :311-313/:358-360 are pure CHS, and
 *  d->lba is parsed at :970 and never reaches an offset computation. A guest
 *  told LBA is supported would have its LBA addresses read as C/H/S.
 *
 *  This asserts the CURRENT, DELIBERATE state. If LBA is ever implemented, this
 *  row must be re-authored in the SAME change -- that is the point of pinning it.
 */
static void row_no_lba_claim(void)
{
	struct wdc_data d;

	build(&d, 1024, 1, 1, 1);
	rows ++;
	if (d.identify_struct[2 * 49 + 0] != 0 ||
	    d.identify_struct[2 * 49 + 1] != 0) {
		printf("  FAIL word 49 claims a capability: %02x %02x"
		    " (0x200 = LBA, 0x100 = DMA -- neither is implemented)\n",
		    d.identify_struct[2 * 49 + 0], d.identify_struct[2 * 49 + 1]);
		failures ++;
	} else {
		printf("  ok   %-38s word 49 = 00 00\n",
		    "no unimplemented capability claimed");
	}
}

/*
 *  THE SPEC-FREE ORACLE. Images are rounded to whole cylinders, so the sector
 *  count must equal cyls * heads * sectors_per_track -- both readable from the
 *  same block. No ATA document is needed to see the block contradict itself.
 *
 *  #407: H WAS 15 AND THE BOUND WAS 2000. Both were wrong for their purpose.
 *  diskimage.c:255-256 pins H=16/S=63 for every non-floppy, so H=15 measured a
 *  geometry no image has. And an 11-bit cylinder truncation, `(cyls >> 8) & 7`,
 *  SURVIVED all ten rows because its first self-contradiction is at c=2048 --
 *  the loop stopped 48 short of catching it. 65535 is the last count word 1 can
 *  represent, so it is the right bound; c=65536 cannot be represented at all and
 *  is a separate defect (the missing clamp) with its own round.
 */
static void row_selfconsistent(void)
{
	struct wdc_data d;
	int c, bad = 0, first_bad = 0;
	const int H = 16, S = 63;

	for (c = 1; c <= 65535; c++) {
		uint64_t sectors = (uint64_t)c * H * S;
		uint64_t claimed, geom;

		build(&d, sectors, c, H, S);
		claimed = sectors_from_block(&d, 60, 61);
		geom    = (uint64_t)word(&d, 1) * word(&d, 3) * word(&d, 6);

		if (claimed != geom) {
			if (!bad)
				first_bad = c;
			bad ++;
		}
	}
	rows ++;
	if (bad) {
		printf("  FAIL self-consistency: %d of 65535 cylinder counts give a\n"
		       "       block that contradicts its own geometry, first at %d\n",
		    bad, first_bad);
		failures ++;
	} else {
		printf("  ok   %-38s 0 of 65535 contradict their geometry\n",
		    "IDENTIFY agrees with itself");
	}
}

int main(void)
{
	printf("ATA IDENTIFY capacity packing (#405), against the REAL dev_wdc.c\n");

	/*  Controls: below the divergence point these pass either way, and they
	    are here to prove the rig reports correct values, not to detect.  */
	row("control: 1 sector (passes unfixed too)",        1);
	row("control: 255 sectors (the correct line)",       255);

	/*  Each of these puts a specific byte at or past the point where % and &
	    part company. Without them the whole table is vacuous.  */
	row("threshold: >>8 byte reaches 255",               65280);
	row("carry: >>8 wraps into >>16",                    65536);
	row("all four bytes distinct",                       0x12345678ULL);
	row(">>8 accidentally right, >>16 wrong",            0xFF0000ULL);
	row("threshold: >>24 byte reaches 255",              0xFF010203ULL);
	row("every byte 255",                                0xFFFFFFFFULL);

	row_anchor();
	row_slave();
	row_base_drive();
	row_no_lba_claim();
	row_selfconsistent();

	printf("\n%d rows, %d failures\n", rows, failures);
	if (failures == 0)
		printf("WDC_IDENTIFY_PASS\n");
	else
		printf("WDC_IDENTIFY_FAIL\n");
	return failures ? 1 : 0;
}
