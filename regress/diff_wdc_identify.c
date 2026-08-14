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
 *
 *  ============================================================================
 *  #410: THIS FILE IS DONE. THE STOPPING CONDITION, AND WHY IT IS WRITTEN DOWN.
 *  ============================================================================
 *
 *  FOUR rounds went into this one file -- #405 built it, #407, #408 and #409
 *  each repaired the last -- and every one of the first three shipped believing
 *  it was complete. They were wrong every time for the SAME reason: each round's
 *  confidence rested on "the mutants I thought of are dead", which is not a
 *  falsifiable claim. The scope was put to a review panel, which said stop.
 *
 *  SCOPE, stated so a later round does not have to re-derive it:
 *
 *    *** THIS FILE IS THE ORACLE FOR WHAT wdc_initialize_identify_struct()
 *    BUILDS. IT IS NOT AN ORACLE FOR WHAT THE GUEST RECEIVES. ***
 *
 *  Everything here reads d->identify_struct directly. The transmit loop between
 *  that array and the guest is therefore invisible to every row -- swapping its
 *  two pushes byte-swaps every word a guest reads at ZERO failures. That
 *  boundary is assigned to a SEPARATE I/O harness (queue item #112) and is not a
 *  gap to be closed by adding rows here. Measured: the content detector kills 64
 *  of 93 dev_wdc.c mutants, a transport harness kills 20, and together they kill
 *  80 -- neither subsumes the other.
 *
 *  WHAT WAS TRUE WHEN THIS FILE WAS DECLARED DONE:
 *    - 16 rows, 0 failures, at -O0 -O1 -O2 -O3 -Os (the NULL-cpu UB that hid
 *      behind -O2 for two rounds is why the sweep is part of the criterion);
 *    - each row's mutant kill asserts the ROW NAME, not merely that something
 *      failed, so a kill from an unrelated row cannot be mistaken for coverage;
 *    - a known-detectable mutant is carried as a positive control, and build
 *      failures and signals are scored as FAULTS, never as detections.
 *
 *  THE RULE THAT WOULD HAVE STOPPED #409, and the one to keep:
 *
 *    *** EVERY CLAIM OF THE FORM "X WAS UNCOVERED, THIS ROW COVERS IT" MUST
 *    CITE A MUTANT RE-RUN AGAINST THE SHIPPED ROW, NOT THE DESIGNED ONE. ***
 *
 *  #409 added a row named "geometry words carry their high byte" and gave it
 *  s = 17, so word 6's high byte stayed permanently zero while the row's name,
 *  this comment, the gate and the commit message all claimed words 3 AND 6. The
 *  designed row covered both; the shipped row covered one. #410 corrected it and
 *  measured the word-6 mutant dying.
 *
 *  KNOWN SURVIVORS, classified rather than left implicit -- this is the part
 *  that makes "done" checkable instead of hopeful. Roughly a dozen mutants
 *  survive the 16 rows, and NONE is guest-visible on a default configuration:
 *    (a) EQUIVALENT      -- /512 rewritten as >>9; no observable difference.
 *    (b) UNREACHABLE     -- heads/spt above 255 require chs_override, i.e. the
 *                           `-d gH;S` path, WHICH IS ITSELF BROKEN (queue #113
 *                           yields a zero-capacity disk). Blocker named and
 *                           filed; these become reachable when #113 lands.
 *    (c) ACCEPTED GAP    -- six unasserted constant fields (words 47/51/64/67/
 *                           68), two identify_struct memset variants already
 *                           covered by DEVINIT(wdc)'s own memset, and two
 *                           serial/firmware placements. Checked, not assumed:
 *                           diskimage_getname is snprintf, which always
 *                           NUL-terminates, so the padding loop always finds a
 *                           NUL and there is NO stack leak.
 *
 *  A future round may reopen this file, but it should first say which of those
 *  three buckets it is emptying, and why that outranks the guest-visible queue.
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

/*
 *  #409: THIS STUB HAD TO LEARN `id` TOO, AND SO DID getname BELOW.
 *
 *  #408 poisoned diskimage_getsize() and wrote the reason into this file -- "a
 *  stub that answers correctly for an id nobody asked about is not a stub, it is
 *  a second implementation" -- and then left the OTHER TWO stubs ignoring `id`.
 *  Measured: with only getsize poisoned, `is_a_cdrom` and `getname` each SURVIVE
 *  both an id-off-by-one and a dropped base_drive, four mutants in total.
 *  #408's commit message claims it closed base_drive "at all three call sites".
 *  It closed ONE.
 *
 *  The is_a_cdrom case is genuinely reachable: a machine with a disk at id 0 and
 *  a CD-ROM at id 1 would make drive 0's IDENTIFY announce ATAPI/CDROM/removable.
 *
 *  POISON BY INVERSION, and the first attempt got this wrong. Putting the CD-ROM
 *  at ONE specific id does not work: the correct id is drive+base_drive = 3, so
 *  the "drop base_drive" mutant asks about id 1 and the "+1" mutant asks about
 *  id 4 -- and with the CD-ROM at id 2 both simply MISS it and still read "not a
 *  CD-ROM". Both survived. The stub must instead answer WRONGLY for every id
 *  except the expected one: exactly one drive is not a CD-ROM, and any id error
 *  therefore flips word 0 to ATAPI/removable.
 */
static int stub_cdrom_poison = 0;	/*  0 = nothing is a CD-ROM  */
static int stub_noncdrom_id  = -1;	/*  the ONLY id that is not  */

int diskimage_is_a_cdrom(struct machine *machine, int id, int type)
{
	(void)machine; (void)type;
	if (!stub_cdrom_poison)
		return 0;
	return (id == stub_noncdrom_id) ? 0 : 1;
}

int diskimage_is_a_tape(struct machine *machine, int id, int type)
{
	(void)machine; (void)id; (void)type;
	return 0;
}

int diskimage_getname(struct machine *machine, int id, int type,
	char *buf, size_t bufsize)
{
	(void)machine; (void)type;
	/*  #409: the name carries the id, so asking for the wrong drive is
	    visible in the model-number field rather than silently identical.  */
	snprintf(buf, bufsize, "%s id%d", stub_name, id);
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
 *
 *  #409: ZERO IT ONCE, NOT PER CALL. sizeof(struct cpu) is 60,821,568 bytes, and
 *  #408 memset it on every call -- 65,535 times in the oracle below, roughly 4 TB
 *  of memory traffic. MEASURED: 148,188 ms shipped versus 34 ms hoisted, a 4,358x
 *  slowdown, with byte-identical output (verified by cmp). Both are static, so
 *  they are already zero at program start; the explicit zeroing is kept only so
 *  the intent survives someone making them automatic.
 */
static struct machine stub_machine;
static struct cpu     stub_cpu;

static struct cpu *fake_cpu(void)
{
	static int done = 0;
	if (!done) {
		memset(&stub_machine, 0, sizeof(stub_machine));
		memset(&stub_cpu, 0, sizeof(stub_cpu));
		stub_cpu.machine = &stub_machine;
		done = 1;
	}
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

	int bad = 0;

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
		bad = 1;
	}

	/*
	 *  #409: THE GEOMETRY HALF, and it kills an OUT-OF-BOUNDS READ.
	 *
	 *  base_drive is the DISKIMAGE id, not an index into the per-drive arrays,
	 *  which are `int cyls[2]`. A mutant indexing them as [d->drive +
	 *  d->base_drive] reads element 2 of a 2-element array -- and it SURVIVED
	 *  all five optimisation levels, because nothing asserted this drive's
	 *  geometry. Only ASan caught it. Asserting the geometry here kills it
	 *  without needing a sanitizer in the gate.
	 */
	if (word(&d, 1) != 500 || word(&d, 3) != 16 || word(&d, 6) != 63) {
		printf("  FAIL %-38s c=%u h=%u s=%u, want 500/16/63"
		    " (indexed by base_drive?)\n",
		    "base_drive is a disk id, not an array index",
		    word(&d, 1), word(&d, 3), word(&d, 6));
		bad = 1;
	}

	if (bad)
		failures ++;
	else
		printf("  ok   %-38s id 2 -> %llu sectors, c=500 h=16 s=63\n",
		    "base_drive reaches the diskimage id",
		    (unsigned long long)got);
}

/*
 *  #409: THE ROW THAT MAKES THE OTHER TWO STUBS' id-DEPENDENCE OBSERVABLE.
 *
 *  Teaching is_a_cdrom() and getname() about `id` accomplishes nothing on its
 *  own -- no row read either answer, so all four id mutants still survived. This
 *  row reads BOTH:
 *
 *    * word 0. The device sets 0x8580 (ATAPI/CDROM/removable) when the disk is a
 *      CD-ROM and 0x0040 (fixed) otherwise. The CD-ROM here is a DIFFERENT id on
 *      the same controller, so any id arithmetic error makes this drive announce
 *      itself removable -- which is exactly the reachable configuration: a disk
 *      at one id and a CD-ROM at the next.
 *    * the model number (word 27, 40 bytes). getname() now embeds the id, so
 *      fetching the wrong drive's name is visible as a wrong string rather than
 *      as an identical one.
 */
static void row_identity(void)
{
	struct wdc_data d;
	uint64_t want = 700ULL * 16 * 63;
	char model[41];
	int bad = 0;

	memset(&d, 0, sizeof(d));
	d.drive = 1;
	d.base_drive = 2;			/*  so the wanted id is 3  */
	d.cyls[1] = 700; d.heads[1] = 16; d.sectors_per_track[1] = 63;
	memset(stub_size_for, 0, sizeof(stub_size_for));
	stub_size_for[3] = want * 512;
	stub_size = 0;
	stub_size_for_active = 1;
	stub_noncdrom_id = 3;		/*  ONLY id 3 is a plain disk  */
	stub_cdrom_poison = 1;		/*  every other id is a CD-ROM  */
	wdc_initialize_identify_struct(fake_cpu(), &d);
	stub_cdrom_poison = 0; stub_noncdrom_id = -1;
	stub_size_for_active = 0;

	rows ++;
	if (word(&d, 0) != 0x0040) {
		printf("  FAIL %-38s word 0 = %04x, want 0040"
		    " (0x8580 = it asked is_a_cdrom about the wrong id)\n",
		    "this drive is not the CD-ROM next to it", word(&d, 0));
		bad = 1;
	}

	memcpy(model, &d.identify_struct[2 * 27], 40);
	model[40] = '\0';
	if (strstr(model, "id3") == NULL) {
		printf("  FAIL %-38s model \"%s\" lacks id3\n",
		    "the model number names THIS drive", model);
		bad = 1;
	}

	if (bad)
		failures ++;
	else
		printf("  ok   %-38s word 0 = 0040, model names id3\n",
		    "is_a_cdrom and getname get the right id");
}

/*
 *  #410: THE POSITIVE HALF OF THE CD-ROM DECISION.
 *
 *  #409's inverted poison made the drive under test the ONLY non-CD-ROM, so
 *  row_identity can observe nothing but the NEGATIVE answer -- and MEASURED,
 *  four mutants therefore survived all fifteen rows: deleting the
 *  `if (cdrom) flags = 0x8580` branch outright, forcing cdrom to 0, changing
 *  0x8580 to 0x8500, and dropping word 0's high byte. *** The entire ATAPI
 *  announcement was deletable with the whole table green. ***
 *
 *  A fix that only ever exercises one branch of a two-branch decision is half a
 *  test. This row takes the other branch: the drive under test IS the CD-ROM,
 *  and word 0 must read 0x8580 (ATAPI, CDROM, removable) rather than the plain
 *  0x0040 fixed-disk flag.
 *
 *  Reachability, so this is not a synthetic configuration: wdc_command() rejects
 *  WDCC_IDENTIFY for a CD-ROM before the switch, but ATAPI_IDENTIFY_DEVICE falls
 *  into the SAME case and calls this same initializer with cdrom set -- so a
 *  guest issuing ATAPI IDENTIFY reaches exactly this state.
 */
static void row_atapi_flags(void)
{
	struct wdc_data d;

	memset(&d, 0, sizeof(d));
	d.drive = 0;
	d.cyls[0] = 50; d.heads[0] = 16; d.sectors_per_track[0] = 63;
	memset(stub_size_for, 0, sizeof(stub_size_for));
	stub_size_for[0] = 50ULL * 16 * 63 * 512;
	stub_size = 0;
	stub_size_for_active = 1;
	stub_noncdrom_id = -1;		/*  nothing is exempt: THIS drive is a CD-ROM  */
	stub_cdrom_poison = 1;
	wdc_initialize_identify_struct(fake_cpu(), &d);
	stub_cdrom_poison = 0;
	stub_size_for_active = 0;

	rows ++;
	if (word(&d, 0) != 0x8580) {
		printf("  FAIL %-38s word 0 = %04x, want 8580"
		    " (ATAPI/CDROM/removable)\n",
		    "a CD-ROM announces itself as one", word(&d, 0));
		failures ++;
	} else {
		printf("  ok   %-38s word 0 = 8580\n",
		    "a CD-ROM announces itself as one");
	}
}

/*
 *  #409: EXERCISE THE HIGH BYTE OF THE GEOMETRY WORDS.
 *
 *  Every other fixture keeps heads and sectors-per-track below 256, so the
 *  `>> 8` half of words 3 and 6 is never non-zero -- MEASURED: forcing either
 *  high byte to a literal 0 SURVIVES the whole table. Cylinders were already
 *  covered (300 > 255).
 *
 *  #410 CORRECTION, and it was a FALSE PASS in this very row. #409 shipped it
 *  with s = 17, so word 6's high byte was STILL permanently zero while this
 *  comment, the row's name, the gate and the commit all claimed words 3 AND 6.
 *  Measured: forcing word 6's high byte to 0 survived at all five optimisation
 *  levels, exactly as before the row existed. Word 3 was genuinely closed; word
 *  6 was not. The three values now carry DISTINCT high bytes -- 4096 = 0x1000,
 *  300 = 0x012c, 770 = 0x0302 -- so a mutant that SWAPS two high bytes is caught
 *  as well. A fixture whose fields share a byte value proves less than it looks:
 *  a first attempt at the multi-drive fixture used heads 400 and 271, both high
 *  byte 0x01, and killed nothing. These values are not reachable from the command line
 *  today only because the geometry override is broken (a separate round), and
 *  wdc copies whatever geometry the diskimage layer hands it.
 */
static void row_wide_geometry(void)
{
	struct wdc_data d;

	build(&d, 4096ULL * 300 * 770, 4096, 300, 770);
	rows ++;
	if (word(&d, 1) != 4096 || word(&d, 3) != 300 || word(&d, 6) != 770) {
		printf("  FAIL %-38s c=%u h=%u s=%u, want 4096/300/770\n",
		    "geometry words carry their high byte",
		    word(&d, 1), word(&d, 3), word(&d, 6));
		failures ++;
	} else {
		printf("  ok   %-38s c/h/s high bytes 10/01/03\n",
		    "geometry words carry their high byte");
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
	row_identity();
	row_atapi_flags();
	row_wide_geometry();
	row_no_lba_claim();
	row_selfconsistent();

	printf("\n%d rows, %d failures\n", rows, failures);
	if (failures == 0)
		printf("WDC_IDENTIFY_PASS\n");
	else
		printf("WDC_IDENTIFY_FAIL\n");
	return failures ? 1 : 0;
}
