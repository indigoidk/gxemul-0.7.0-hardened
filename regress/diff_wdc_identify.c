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
 *  THE MANDATORY RULES. #411 added the second and third after a measure seat
 *  demonstrated that #410's condition COULD BE SATISFIED TO THE LETTER WHILE
 *  STILL SHIPPING A FALSE PASS -- and that #410 already contained one.
 *
 *    *** 1. EVERY CLAIM OF THE FORM "X WAS UNCOVERED, THIS ROW COVERS IT" MUST
 *    CITE A MUTANT RE-RUN AGAINST THE SHIPPED ROW, NOT THE DESIGNED ONE, AND
 *    THE KILL MUST NAME THE ROW. *** (#410 wrote the row-name half as HISTORY,
 *    under "what was true when this file was declared done", so a later round
 *    could cite a kill that actually came from an UNRELATED row -- the #409
 *    shape, one level up. It is a requirement, not a past observation.)
 *
 *    *** 2. EVERY ENTRY IN THE SURVIVOR CLASSIFICATION BELOW MUST NAME EITHER A
 *    ROW, A MEASURED MUTANT RESULT, OR AN EXPLICIT BLOCKER WITH A REPRODUCTION.
 *    *** Self-assigned prose is not a classification. Without this, any future
 *    round can retire an inconvenient survivor into "accepted gap" with one
 *    sentence and satisfy the condition completely.
 *
 *    *** 3. "CHECKED, NOT ASSUMED" MAY ONLY BE WRITTEN WHERE A ROW OR A MEASURED
 *    MUTANT BACKS IT. *** #410 used that phrase for the no-stack-leak claim; the
 *    corresponding mutant -- deleting diskimage_getname's return-value check --
 *    SURVIVES GREEN AT ALL FIVE OPTIMISATION LEVELS, because this file's own
 *    stub returns 1 unconditionally and no row can observe the branch. The
 *    phrase was doing the work of a test while being prose.
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
 *    (b) UNREACHABLE     -- heads/spt above 255. #410 named chs_override as the
 *                           blocker; #411 CORRECTS THAT REASON, which was
 *                           INCOMPLETE. `-d f:` sets the type to FLOPPY at ANY
 *                           file size, BEFORE the recalc and with no override at
 *                           all. Measured against the real diskimage_recalc_size:
 *                           `-d f:` on a 20 MB file would give spt 256, and on a
 *                           100 MB file 1280 -- both above 255. It is masked
 *                           TODAY only by the very defect (#113) named as the
 *                           blocker, so fixing the override arm alone will NOT
 *                           re-close this bucket: the `-d f:` route opens at the
 *                           same moment. Timing right, mechanism wrong.
 *    (c) ACCEPTED GAP    -- six unasserted constant fields (words 47/51/64/67/
 *                           68), two identify_struct memset variants already
 *                           covered by DEVINIT(wdc)'s own memset, and two
 *                           serial/firmware placements.
 *                           #411 CORRECTS #410's stack-leak reasoning. The
 *                           CONCLUSION holds -- there is no leak -- but not for
 *                           the stated reason, and snprintf's NUL-termination is
 *                           IRRELEVANT on that path. The two facts that actually
 *                           carry it: diskimage_getname does not write buf at all
 *                           when it fails (it returns 0 without touching it), so
 *                           what prevents the leak is the CALLER's return-value
 *                           check falling through to a string literal; and the
 *                           failure path is unreachable anyway, because
 *                           wdc_command returns ABRT when !diskimage_exist and
 *                           diskimage_exist uses the IDENTICAL id/type predicate
 *                           as diskimage_getname. The original wording licensed
 *                           exactly the wrong refactor -- "it always
 *                           NUL-terminates, so the caller's check is redundant".
 *                           NO ROW BACKS THIS: measured, deleting that check
 *                           survives green at all five optimisation levels.
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

/*  #473: dev_wdc_access() reaches the disk layer, which the IDENTIFY-only rows never
 *  did -- --gc-sections had been dropping these paths entirely.  Stubbed rather than
 *  linked: the re-arm row under test never performs real I/O, it only needs the call
 *  to return without pulling in the whole disk subsystem.  A stub that SUCCEEDS would
 *  be wrong here (it would fabricate data); these report 'no disk', which is the
 *  honest answer for a fixture that has none.  */
void debug(const char *fmt, ...) { (void) fmt; }
/*  Little-endian and SELF-CONSISTENT, which is all that is required: the device
 *  only ever reads back what this driver wrote.  Same bodies as diff_footbridge.c,
 *  which drives its own access handler the same way.  */
uint64_t memory_readmax64(struct cpu *cpu, unsigned char *buf, int len)
{
	uint64_t x = 0; int i;
	(void) cpu;
	for (i = 0; i < len; i++)
		x |= (uint64_t) buf[i] << (8*i);
	return x;
}

void memory_writemax64(struct cpu *cpu, unsigned char *buf, int len, uint64_t data)
{
	int i;
	(void) cpu;
	for (i = 0; i < len; i++)
		buf[i] = (unsigned char) (data >> (8*i));
}

/*  The SCSI layer, reached only by the packet-command path.
 *
 *  DEFAULT INERT, SELECTIVELY PRODUCTIVE.  Most rows here never issue a command -- they
 *  place the state machine one read from the arithmetic under test and then read.  For
 *  those, a scsicommand returning 1 would fabricate a transfer the fixture never asked
 *  for and would overwrite the atapi_st the row set up.
 *
 *  But `row_arm_overrun` MUST issue a real packet command, because the initial arm it
 *  tests is reachable no other way.  So the stub is controlled by a file-static byte
 *  count: zero (the default) keeps it inert for every other row, non-zero makes it
 *  fabricate exactly one DATA-IN transfer of that size.  */
static int stub_datain_len = 0;
struct scsi_transfer *scsi_transfer_alloc(void)
{
	return (struct scsi_transfer *) calloc(1, sizeof(struct scsi_transfer));
}

void scsi_transfer_free(struct scsi_transfer *p)
{
	free(p);
}

int diskimage_scsicommand(struct cpu *cpu, int id, int type,
	struct scsi_transfer *xferp)
{
	size_t i;

	(void) cpu; (void) id; (void) type;

	if (stub_datain_len <= 0)
		return 0;

	/*  One DATA-IN transfer, marked so the caller can tell WHICH bytes
	    survived: byte 0 alone carries 0x5a, everything else 0xc3.  A ring
	    overrun wraps block 514 onto block 0, so the first byte popped
	    becomes 0xc3 and the marker is destroyed.  */
	xferp->data_in = (unsigned char *) malloc(stub_datain_len);
	if (xferp->data_in == NULL)
		return 0;
	for (i = 0; i < (size_t) stub_datain_len; i++)
		xferp->data_in[i] = 0xc3;
	xferp->data_in[0] = 0x5a;
	xferp->data_in_len = stub_datain_len;
	return 1;
}

int diskimage_exist(struct machine *machine, int id, int type)
{
	(void)machine; (void)id; (void)type;
	return 0;
}

int diskimage_access(struct machine *machine, int id, int type, int writeflag,
	off_t offset, unsigned char *buf, size_t len)
{
	(void)machine; (void)id; (void)type; (void)writeflag;
	(void)offset; (void)buf; (void)len;
	return 0;
}

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
/*
 *  #473 `wdcrearmzero`: the DATAIN re-arm reports ZERO remaining mid-transfer.
 *
 *  `if (atapi_len > 32768) atapi_len = 0;` at the re-arm, where the INITIAL arm clamps
 *  to 32768 in the identical condition.  With more than 32768 bytes remaining the guest
 *  is told zero remain, and there is no recovery: the next read does
 *  `atapi_len -= consumed` from 0, steps PAST zero, and `== 0` never fires again --
 *  precisely the #341 class this file's own comment describes, reintroduced by the
 *  re-arm.
 *
 *  MEASURED BAND [65537, 262655].  65536 completes (remaining is exactly 32768, so the
 *  `> 32768` test is false); 262656 also trips the ring overrun, so it is not purely
 *  this defect.
 *
 *  GUEST-VISIBLE at the first re-arm, read back through the handler: bytecount 0,
 *  STATUS 0x58 (DRDY|DSC|DRQ), ireason 0x02 -- "data-in phase, DRQ asserted, zero bytes
 *  to transfer".
 *
 *  THE IRQ SINK IS REQUIRED, and its absence is not a field omission: dev_wdc_tick() runs
 *  unconditionally after every access and calls INTERRUPT_ASSERT(d->irq).  DEVINIT wires
 *  that with INTERRUPT_CONNECT -- a macro, invisible to a scan for field assignments.
 *  Two earlier attempts died there and were removed rather than shipped as false reds.
 *
 *  THE STATE IS SYNTHESISED AND SAYS SO.  Under the SHIPPED code the machine breaks at
 *  the FIRST re-arm (received = 32768), so no real trajectory reaches these values; they
 *  are the arithmetic under test placed one read from firing.  131070 is on the FIXED
 *  code's trajectory (end of chunk 4), chosen so the row reads as a plausible state
 *  rather than an arbitrary one.
 */
static int rearm_asserts = 0;
static void rearm_sink(struct interrupt *a) { (void)a; rearm_asserts++; }

static void row_rearm_zero(void)
{
	struct wdc_data d;
	struct scsi_transfer st;
	unsigned char buf[4];
	unsigned char *payload;
	int occ;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;		/*  non-zero: :678 divides by it (SIGFPE otherwise)  */
	d.io_enabled = 1;		/*  or :680 goto ret skips the whole switch  */
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = rearm_sink;	/*  what INTERRUPT_CONNECT would wire  */
	if (d.inbuf == NULL) { printf("  SETUP inbuf alloc failed\n"); return; }

	payload = (unsigned char *) calloc(1, 200000);
	if (payload == NULL) { free(d.inbuf); printf("  SETUP payload failed\n"); return; }

	/*  MARKERS, so the refill can be caught taking bytes from the WRONG place.
	    atapi_received advances BEFORE the re-arm (`received += consumed`), so
	    with 131070 received and 2 consumed the refill must start at 131072.
	    A refill that ignores atapi_received starts at 0 and yields 0xaa.  */
	payload[0]      = 0xaa;
	payload[131072] = 0x3c;

	memset(&st, 0, sizeof(st));
	st.data_in = payload;
	st.data_in_len = 200000;

	d.atapi_st = &st;
	d.atapi_phase = PHASE_DATAIN;
	d.atapi_cmd_in_progress = 1;
	d.atapi_received = 131070;	/*  on the FIXED code's trajectory  */
	d.atapi_len = 2;		/*  this read drains the chunk  */

	wdc_addtoinbuf(&d, 0x5a);
	wdc_addtoinbuf(&d, 0x5a);

	rearm_asserts = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_READ, &d);

	/*  68930 remain, so a correct re-arm reports min(remaining, 32768) = 32768.
	    The committed code reports 0 and the command never completes.  */
	rows ++;
	if (d.atapi_len != 32768) {
		printf("  FAIL %-38s atapi_len = %i, want 32768\n",
		    "re-arm: >32768 left is not zeroed", d.atapi_len);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "re-arm: >32768 left is not zeroed", d.atapi_len);
	}

	/*  FREE SECOND ORACLE: proves the re-arm BRANCH was taken, not merely that the
	    call survived.  A fixture that silently missed the branch would otherwise
	    look identical to one that took it and measured the wrong thing.  */
	rows ++;
	if (rearm_asserts != 1) {
		printf("  FAIL %-38s asserts = %i, want 1\n",
		    "re-arm: the branch was actually taken", rearm_asserts);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "re-arm: the branch was actually taken", rearm_asserts);
	}

	/*  *** THESE TWO ROWS CLOSE A MEASURED FLOOR CLAUSE (d) BREACH. ***  The length
	    check above passes under BOTH of these mutants, each of which keeps the
	    32768 guard and nulls its repair:
	
	      Md_norefill   delete the refill loop -- the guest is told 32768 bytes are
	                    ready and the ring is EMPTY
	      Md_wrongoff   refill from data_in[j] -- every chunk returns chunk 0 again,
	                    which is silent data corruption
	
	    The arm row already carried a corruption oracle and this one did not: the
	    sibling-parity check exists precisely to catch that asymmetry.  */
	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;
	rows ++;
	if (occ != 32768) {
		printf("  FAIL %-38s occupancy = %i, want 32768\n",
		    "re-arm: the chunk is REFILLED", occ);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "re-arm: the chunk is REFILLED", occ);
	}

	rows ++;
	if (d.inbuf[d.inbuf_tail] != 0x3c) {
		printf("  FAIL %-38s first byte = 0x%02x, want 0x3c\n",
		    "re-arm: refill starts at received", d.inbuf[d.inbuf_tail]);
		failures ++;
	} else {
		printf("  ok   %-38s 0x%02x\n",
		    "re-arm: refill starts at received", d.inbuf[d.inbuf_tail]);
	}

	free(payload);
	free(d.inbuf);
}


/*
 *  *** CONTRACT (vacuity floor clause (e)) -- what the six #473 rows are DESIGNED to
 *  catch, stated so a later escape is a breach or an exclusion rather than an argument
 *  about overclaiming. ***
 *
 *  IN CONTRACT -- measured killed, 8 of 8, table in kill473_table.txt:
 *    (b) the arm defect reinstated verbatim (clamp moved back after the push loop)
 *    (b) the re-arm defect reinstated verbatim (= 0, no refill)
 *    (b) both sites reinstated together -- the full pre-fix code
 *    (c) a null medium: a comment-only dev_wdc.c (caught at COMPILE time)
 *    (d) the arm clamp widened to the ring size, still reading as a bound
 *    (d) the arm clamp inverted to 0, guard kept
 *    (d) the re-arm clamp kept and the REFILL LOOP DELETED
 *    (d) the refill re-based to data_in[j], ignoring atapi_received
 *
 *  OUT OF CONTRACT, stated rather than hidden:
 *    - wdc_addtoinbuf() itself is still UNBOUNDED.  The fix bounds its CALLER, and no
 *      row here constrains the primitive.  A future caller that pushes without a clamp
 *      reproduces the same overrun and these rows will not see it.
 *    - only TIMER-style single-chunk trajectories are exercised.  A transfer crossing
 *      several re-arms is not walked end to end; the rows pin the FIRST re-arm.
 *    - the fixture drives one packet command.  Interleaved commands, aborts and
 *      resets are outside it.
 */
/*
 *  #473 `wdcringambig`: the initial DATAIN arm pushed the WHOLE transfer into a ring
 *  that cannot hold it.
 *
 *  WDC_INBUF_SIZE is 512*(WDC_MAX_SECTORS+1) -- exactly 513 blocks.  The arm did
 *  `atapi_len = data_in_len`, pushed every byte, and clamped to 32768 AFTERWARDS, so a
 *  514-block transfer wrapped block 514 onto block 0 and destroyed unread data.  The
 *  clamp was not missing; it was on the wrong side of the loop.
 *
 *  *** THIS ROW REPLACES ONE AIMED A LEVEL TOO LOW, AND THAT IS THE LESSON WORTH
 *  KEEPING.  ***  The first version called wdc_addtoinbuf() directly, 514 blocks' worth.
 *  It went RED on the committed build, which made it look like a reproduction -- but the
 *  primitive is unbounded and THE FIX DID NOT BOUND IT.  The repair is in the caller, so
 *  the row pinned something still true afterwards and could never go green.  A detector
 *  aimed at a primitive cannot verify a fix made in its caller: right defect, wrong
 *  instrument.
 *
 *  SO THIS ONE DRIVES THE ARM.  atapi_cmd_in_progress plus exactly 12 bytes in the ring,
 *  then a wd_data WRITE pops the packet and calls diskimage_scsicommand() -- and the
 *  controllable stub fabricates a 514-block DATA-IN transfer for this row alone.
 *
 *  TWO ORACLES.  Occupancy separates the two builds arithmetically (263168 bytes into a
 *  262656-byte ring reports 512, not 263168 and not 32768).  The marker byte is the
 *  CORRUPTION oracle: it shows block 0's data actually destroyed rather than merely
 *  miscounted, which is the guest-visible harm.
 */
static int arm_asserts = 0;
static void arm_sink(struct interrupt *a) { (void)a; arm_asserts++; }

static void row_arm_overrun(void)
{
	struct wdc_data d;
	unsigned char buf[4];
	int i, occ, first;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) { printf("  SETUP inbuf alloc failed\n"); return; }

	/*  The packet fires when inbuf holds 12 bytes AFTER this access adds its
	    own -- the test is `inbuf_len == 12` and the write pushes first.  So
	    ten are queued here and the 2-byte write below completes the packet.
	    Queueing twelve gives 14 and the command silently never fires, which
	    is what the first version of this row measured.  */
	d.atapi_cmd_in_progress = 1;
	for (i = 0; i < 10; i++)
		wdc_addtoinbuf(&d, 0x00);

	/*  514 blocks: one more than the ring holds.  */
	stub_datain_len = 514 * 512;
	arm_asserts = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	stub_datain_len = 0;		/*  inert again for every later row  */

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;

	/*  FIXED: one DRQ chunk, 32768.  BROKEN: 263168 pushed into a 262656-byte
	    ring reports 512 -- the ring cannot even tell you how much it lost.  */
	rows ++;
	if (occ != 32768) {
		printf("  FAIL %-38s occupancy = %i, want 32768\n",
		    "arm: pushes one chunk, not the whole", occ);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "arm: pushes one chunk, not the whole", occ);
	}

	/*  THE CORRUPTION ORACLE.  Block 0's first byte carries 0x5a; an overrun wraps
	    block 514 onto it and leaves 0xc3.  Occupancy alone says the count is wrong;
	    this says the DATA is gone, which is the guest-visible harm.  */
	first = d.inbuf[d.inbuf_tail];
	rows ++;
	if (first != 0x5a) {
		printf("  FAIL %-38s first byte = 0x%02x, want 0x5a\n",
		    "arm: block 0 survives the push", first);
		failures ++;
	} else {
		printf("  ok   %-38s 0x%02x\n",
		    "arm: block 0 survives the push", first);
	}

	if (d.atapi_st != NULL) {
		free(d.atapi_st->data_in);
		free(d.atapi_st->cmd);
		free(d.atapi_st);
	}
	free(d.inbuf);
}


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
	/*  Unbuffered, so a crash mid-run still shows how far it got -- with stdout
	    block-buffered a segfault loses every row and looks like a build failure.
	    Same reason diff_diskimage_io.c does this; this file lacked it, and that
	    cost a diagnostic cycle chasing an invisible crash.  */
	setvbuf(stdout, NULL, _IONBF, 0);

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
	row_arm_overrun();
	row_rearm_zero();
	row_atapi_flags();
	row_wide_geometry();
	row_no_lba_claim();
	row_selfconsistent();

	/*
	 *  IDENTITY GUARD.  Two files with this name once differed only by the case of a
	 *  parent directory, and the stale one encoded a REVERSED design decision.  A row
	 *  count is the cheapest proof that the file which RAN is the file that was
	 *  reviewed.  Last, so it counts every row above it.
	 *
	 *  It is also floor clause (c): against a null medium -- a stale copy, or a
	 *  comment-only source -- this row is what refuses to report a pass.
	 */
	rows ++;
	if (rows != 23) {
		printf("  FAIL %-38s rows = %i, want 23\n",
		    "[IDENTITY] row count", rows);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n", "[IDENTITY] row count", rows);
	}

	printf("\n%d rows, %d failures\n", rows, failures);
	if (failures == 0)
		printf("WDC_IDENTIFY_PASS\n");
	else
		printf("WDC_IDENTIFY_FAIL\n");
	return failures ? 1 : 0;
}
