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
 *  ITSELF. Measured on the committed code: 65,471 of 65,535 cylinder counts
 *  produce a self-contradicting IDENTIFY block, the first at 65 cylinders.
 *
 *  KNOWN SURVIVOR, recorded rather than papered over: a COMPENSATING PAIR that
 *  swaps +0/+1 in all eight capacity lines AND swaps the two pushes in the
 *  transmit loop is invisible here, because this driver reads identify_struct
 *  directly rather than through the transmit path. The word-53 anchor below
 *  catches the packing half alone. Note that word 47 is 0x8080 -- a byte-swap
 *  palindrome -- and is therefore useless as an anchor.
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
int64_t diskimage_getsize(struct machine *machine, int id, int type)
{
	(void)machine; (void)id; (void)type;
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

static void build(struct wdc_data *d, uint64_t sectors, int c, int h, int s)
{
	memset(d, 0, sizeof(*d));
	d->cyls[0] = c;
	d->heads[0] = h;
	d->sectors_per_track[0] = s;
	stub_size = sectors * 512;
	wdc_initialize_identify_struct(NULL, d);
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
 *  THE SPEC-FREE ORACLE. Images are rounded to whole cylinders, so the sector
 *  count must equal cyls * heads * sectors_per_track -- both readable from the
 *  same block. No ATA document is needed to see the block contradict itself.
 */
static void row_selfconsistent(void)
{
	struct wdc_data d;
	int c, bad = 0, first_bad = 0;
	const int H = 15, S = 63;

	for (c = 1; c <= 2000; c++) {
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
		printf("  FAIL self-consistency: %d of 2000 cylinder counts give a\n"
		       "       block that contradicts its own geometry, first at %d\n",
		    bad, first_bad);
		failures ++;
	} else {
		printf("  ok   %-38s 0 of 2000 contradict their geometry\n",
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
	row_selfconsistent();

	printf("\n%d rows, %d failures\n", rows, failures);
	if (failures == 0)
		printf("WDC_IDENTIFY_PASS\n");
	else
		printf("WDC_IDENTIFY_FAIL\n");
	return failures ? 1 : 0;
}
