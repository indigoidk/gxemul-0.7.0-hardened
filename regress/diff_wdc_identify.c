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
#include <sys/wait.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>

/*  Externals the identify path reaches. Sizes come from the row under test.  */
static uint64_t stub_size = 0;
static const char *stub_name = "GXemul regress disk";

static int stub_fatals = 0;	/*  #478: EMISSIONS, not the latch  */
/*  *** AND COUNTED BY MESSAGE, NOT BY OCCURRENCE.  A bare count cannot tell WHICH
    message fired, and the per-device bad-len notice fires alongside the drain
    announce -- so a shared-latch mutant that silences the announce still shows a
    non-zero count and ESCAPES.  Measured: it did.  This is the witness ladder's
    DEVICE-SIGNATURE control applied to a log line: the observed value must only
    have been producible by the event under test.  ***  */
static int stub_drain_msgs = 0;

void fatal(const char *fmt, ...)
{
	va_list ap;
	stub_fatals ++;
	if (strstr(fmt, "no sector") != NULL)
		stub_drain_msgs ++;
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
static int stub_frees = 0;
static int stub_scsi_cmds = 0;	/*  #477: dispatches ATTEMPTED  */
static int stub_disk_writes = 0, stub_disk_bytes = 0;
static long stub_disk_offset = 0;
static int stub_disk_first = -1;


struct scsi_transfer *scsi_transfer_alloc(void)
{
	return (struct scsi_transfer *) calloc(1, sizeof(struct scsi_transfer));
}

void scsi_transfer_free(struct scsi_transfer *p)
{
	stub_frees ++;
	free(p);
}

int diskimage_scsicommand(struct cpu *cpu, int id, int type,
	struct scsi_transfer *xferp)
{
	size_t i;

	(void) cpu; (void) id; (void) type;

	/*  counted BEFORE the inert early-out, so it records the DISPATCH
	    regardless of whether this stub fabricates a transfer.  */
	stub_scsi_cmds ++;

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

static int stub_disk_exists = 0;	/*  inert by default  */

int diskimage_exist(struct machine *machine, int id, int type)
{
	(void)machine; (void)id; (void)type;
	return stub_disk_exists;
}

int diskimage_access(struct machine *machine, int id, int type, int writeflag,
	off_t offset, unsigned char *buf, size_t len)
{
	(void)machine; (void)id; (void)type;
	/*  OBSERVABLE: `wdcdataoutdrain` needs to know whether the device wrote to
	    the IMAGE, and at what offset.  A silent stub cannot answer that.  */
	if (writeflag) {
		stub_disk_writes ++;
	if (stub_disk_first < 0 && len > 0 && buf != NULL)
		stub_disk_first = ((unsigned char *) buf)[0];
		stub_disk_bytes += (int) len;
		stub_disk_offset = (long) offset;
	}
	(void)buf;
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

	/*  *** THE REFILL IS NOT CONDITIONAL ON THE RING BEING EMPTY, AND A CLEAN
	    12-MUTANT TABLE DID NOT SHOW THAT. ***  Two panel seats independently
	    broke the shipped comment's claim that the ring IS empty here: the
	    data-port WRITE arm pushes guest bytes with no phase guard, and its
	    unexpected-write latch is suppressed precisely because
	    atapi_cmd_in_progress is set.  So a guest that writes mid-DATAIN grows
	    head without touching atapi_len.

	    One seat then turned that sentence into a mutant -- `if (inbuf_head ==
	    inbuf_tail)` around the refill -- and it SWEPT the detector clean, 23
	    rows 0 failures, because every other row leaves the ring empty here.
	    A guard built from a round's own safety argument is invisible to rows
	    written under that same argument.

	    This row is the only one that establishes a NON-EMPTY ring at the
	    re-arm.  It pins behaviour, not desirability: whether refilling onto a
	    dirty ring is RIGHT is a separate question, filed as
	    `wdcaddtoinbufbound`.  What must not happen silently is the refill
	    being skipped while the guest is still told 32768 bytes are ready.  */
	{
		struct wdc_data e;
		struct scsi_transfer es;
		unsigned char ebuf[4], *epay;
		int eocc, i;

		memset(&e, 0, sizeof(e));
		e.addr_mult = 1;  e.io_enabled = 1;
		e.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
		e.irq.interrupt_assert = rearm_sink;
		epay = (unsigned char *) calloc(1, 200000);
		if (e.inbuf == NULL || epay == NULL) {
			printf("  SETUP dirty-ring alloc failed\n");
			free(e.inbuf); free(epay);
		} else {
			memset(&es, 0, sizeof(es));
			es.data_in = epay;  es.data_in_len = 200000;
			e.atapi_st = &es;  e.atapi_phase = PHASE_DATAIN;
			e.atapi_cmd_in_progress = 1;
			e.atapi_received = 131070;
			e.atapi_len = 2;

			/*  the two chunk bytes the guest is about to drain...  */
			wdc_addtoinbuf(&e, 0x5a);
			wdc_addtoinbuf(&e, 0x5a);
			/*  ...and FIVE bytes behind them that atapi_len knows nothing
			    about, which is exactly what an interleaved data-port write
			    leaves in the ring.  */
			for (i = 0; i < 5; i++)
				wdc_addtoinbuf(&e, 0x77);

			memset(ebuf, 0, sizeof(ebuf));
			dev_wdc_access(fake_cpu(), NULL, wd_data, ebuf, 2, MEM_READ, &e);

			eocc = e.inbuf_head - e.inbuf_tail;
			while (eocc < 0)
				eocc += WDC_INBUF_SIZE;

			/*  5 leftover + 32768 refilled.  A refill skipped on a non-empty
			    ring leaves 5, and the guest is told 32768 are waiting.  */
			rows ++;
			if (eocc != 5 + 32768) {
				printf("  FAIL %-38s occupancy = %i, want %i\n",
				    "re-arm: refills a NON-EMPTY ring too", eocc, 5 + 32768);
				failures ++;
			} else {
				printf("  ok   %-38s %i\n",
				    "re-arm: refills a NON-EMPTY ring too", eocc);
			}
			free(epay);  free(e.inbuf);
		}
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
 *    (d) the refill guarded by `head == tail` -- this round's own safety sentence
 *        turned into a predicate; it swept 23 rows clean before the dirty-ring row
 *    (d) the refill's bound relaxed to the CONSTANT 32768 instead of atapi_len; it
 *        swept 24 rows clean and is a heap-buffer-overflow READ under ASan on a
 *        short last chunk
 *
 *  OUT OF CONTRACT, stated rather than hidden:
 *    - wdc_addtoinbuf() itself is still UNBOUNDED.  The fix bounds its CALLER, and no
 *      row here constrains the primitive.  A future caller that pushes without a clamp
 *      reproduces the same overrun and these rows will not see it.
 *    - THE PREMISE ITSELF: the shipped comment once said the ring IS empty at the
 *      re-arm.  It is not -- the data-port WRITE arm pushes with no phase guard, and a
 *      panel seat MEASURED one 2-byte store desynchronising an entire 32768-byte chunk
 *      that walks clean pre-fix.  Tracked as `wdcaddtoinbufbound`.  Two of the mutants
 *      above exist because every row here was written under that premise.
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

/*  *** THE FIFTH CLAUSE-(d) MUTANT, AND IT ESCAPED THE TABLE THAT HAD ALREADY
 *  CLOSED FOUR. ***  Supplied and MEASURED by the Opus seat on #473's pass 2, against
 *  the working tree with the dirty-ring row already in it:
 *
 *      for (int j=0; j<d->atapi_len; j++)   ->   for (int j=0; j<32768; j++)
 *
 *  24 rows, 0 failures -- a CLEAN SWEEP -- and under ASan on a short last chunk it is a
 *  heap-buffer-overflow READ past data_in.  The committed build is ASan-clean on the
 *  same walk, which is the negative control.
 *
 *  WHY IT HID: every other re-arm row sits where the remainder EXCEEDS 32768, so
 *  `atapi_len` and the constant 32768 are the same number and no row can tell them
 *  apart.  The rows were not weak; they were all on one side of a boundary.
 */
/*  PROPOSED ROW -- kills the fifth (d) mutant, and it is a SINGLE-RE-ARM
 *  trajectory, i.e. exactly the shape the shipped contract says IS in scope.
 *
 *  The four shipped re-arm rows all sit on a chunk where the remainder is
 *  LARGER than 32768, so `atapi_len` and the constant 32768 are the same
 *  number and nothing distinguishes them.  Put the re-arm on a SHORT last
 *  chunk and the refill's bound becomes observable.
 */
static int q2_asserts = 0;
static void q2_sink(struct interrupt *a) { (void)a; q2_asserts++; }

static void row_q2_short_last_chunk(void)
{
	struct wdc_data d;
	struct scsi_transfer st;
	unsigned char buf[4];
	unsigned char *payload;
	int occ;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = q2_sink;
	if (d.inbuf == NULL) { printf("  SETUP q2 inbuf failed\n"); return; }

	/*  EXACT allocation, no slack: an over-read past data_in_len is then a real
	    heap-buffer-overflow rather than a read into padding.  */
	payload = (unsigned char *) malloc(40000);
	if (payload == NULL) { free(d.inbuf); printf("  SETUP q2 payload failed\n"); return; }
	memset(payload, 0xc3, 40000);
	payload[35002] = 0x7e;

	memset(&st, 0, sizeof(st));
	st.data_in = payload;
	st.data_in_len = 40000;

	d.atapi_st = &st;
	d.atapi_phase = PHASE_DATAIN;
	d.atapi_cmd_in_progress = 1;
	d.atapi_received = 35000;	/*  4998 will remain: a SHORT last chunk  */
	d.atapi_len = 2;

	wdc_addtoinbuf(&d, 0x5a);
	wdc_addtoinbuf(&d, 0x5a);

	q2_asserts = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_READ, &d);

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;

	rows ++;
	if (d.atapi_len != 4998) {
		printf("  FAIL %-38s atapi_len = %i, want 4998\n",
		    "last chunk: length is the REMAINDER", d.atapi_len);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "last chunk: length is the REMAINDER", d.atapi_len);
	}

	/*  THE DISCRIMINATOR.  A refill whose bound is the CONSTANT 32768 rather than
	    atapi_len pushes 32768 here and reads 27770 bytes past data_in.  */
	rows ++;
	if (occ != 4998) {
		printf("  FAIL %-38s occupancy = %i, want 4998 (refill bound is not atapi_len)\n",
		    "last chunk: refill is BOUNDED by it", occ);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "last chunk: refill is BOUNDED by it", occ);
	}

	free(payload);
	free(d.inbuf);
}


/*
 *  `wdcoddstep`: `atapi_len -= consumed` STEPS PAST ZERO on an odd-length chunk.
 *
 *  `consumed` is `len == 4 ? 4 : (len >= 2 ? 2 : 1)` -- what the reads actually POP, which
 *  is what #341 corrected.  But nothing clamps it to what REMAINS, so a four-byte read of
 *  a three-byte remainder drives atapi_len to -1 and atapi_received to 4 of 3.
 *
 *  TWO ROWS, KEPT APART ON PURPOSE.  The completion half and the truthfulness half are
 *  repaired by DIFFERENT candidate fixes: saturating atapi_len (or testing `<= 0`) fixes
 *  completion and leaves atapi_received over-counted; clamping `consumed` fixes both.  A
 *  single combined row could not distinguish them, and the fork's own precedents (#283
 *  ASC, #338 mb89352, #341 here) all hold that the count reported has to be the count that
 *  happened.
 *
 *  SMALL ODD TRANSFER, NO RE-ARM INVOLVED -- reachable by MODE SENSE / REQUEST SENSE and
 *  NOT a consequence of #473, which only added a second road via an odd FINAL chunk.
 */
static int odd_asserts = 0;
static void odd_sink(struct interrupt *a) { (void)a; odd_asserts++; }

static void row_odd_step(void)
{
	struct wdc_data d;
	struct scsi_transfer st;
	unsigned char buf[8];
	unsigned char *payload;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = odd_sink;
	if (d.inbuf == NULL) { printf("  SETUP odd inbuf failed\n"); return; }

	payload = (unsigned char *) malloc(3);
	if (payload == NULL) { free(d.inbuf); printf("  SETUP odd payload failed\n"); return; }
	payload[0] = 0x11; payload[1] = 0x22; payload[2] = 0x33;

	memset(&st, 0, sizeof(st));
	st.data_in = payload;
	st.data_in_len = 3;

	d.atapi_st = &st;
	d.atapi_phase = PHASE_DATAIN;
	d.atapi_cmd_in_progress = 1;
	d.atapi_received = 0;
	d.atapi_len = 3;			/*  ODD  */

	/*  exactly three bytes queued: the fourth pop hits an empty ring, latches
	    warned_inbuf_overread, returns -1 and does NOT advance the tail.  */
	wdc_addtoinbuf(&d, 0x11);
	wdc_addtoinbuf(&d, 0x22);
	wdc_addtoinbuf(&d, 0x33);

	odd_asserts = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 4, MEM_READ, &d);

	/*  COMPLETION.  Today -1: `== 0` never fires again, so the command never
	    completes and the guest waits forever.  */
	rows ++;
	if (d.atapi_len != 0) {
		printf("  FAIL %-38s atapi_len = %i, want 0\n",
		    "odd chunk: the count stops at zero", d.atapi_len);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "odd chunk: the count stops at zero", d.atapi_len);
	}

	/*  TRUTHFULNESS.  Today 4 where data_in_len is 3.  Separate because the cheaper
	    fix options repair the row above and leave this one red.  */
	rows ++;
	if (d.atapi_received != st.data_in_len) {
		printf("  FAIL %-38s received = %i, want %i\n",
		    "odd chunk: received never exceeds len",
		    (int) d.atapi_received, (int) st.data_in_len);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "odd chunk: received never exceeds len", (int) d.atapi_received);
	}

	free(payload);
	free(d.inbuf);
}


/*  THE INTERMEDIATE-STATE ROW, and the two rows above do not imply it.
 *
 *  A panel seat named the escape: degrade the clamp from a MIN to a plain assignment,
 *  `consumed = d->atapi_len;`.  A plausible future simplification -- and both end-state
 *  rows still pass, because the transfer does end at 0 of 37.  What changes is WHEN: the
 *  FIRST four-byte read swallows the whole transfer and the command completes after four
 *  bytes were actually delivered.
 *
 *  So the detector needs a row that observes the walk MID-TRANSFER rather than at its end.
 *  One four-byte read of a 37-byte transfer must leave exactly 33.
 */
static void row_odd_midwalk(void)
{
	struct wdc_data d;
	struct scsi_transfer st;
	unsigned char buf[8];
	unsigned char *payload;
	int i;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = odd_sink;
	if (d.inbuf == NULL) { printf("  SETUP midwalk inbuf failed\n"); return; }

	/*  37 -- the guest-chosen INQUIRY allocation length from the worked path.  */
	payload = (unsigned char *) malloc(37);
	if (payload == NULL) { free(d.inbuf); printf("  SETUP midwalk payload failed\n"); return; }
	for (i = 0; i < 37; i++)
		payload[i] = (unsigned char) i;

	memset(&st, 0, sizeof(st));
	st.data_in = payload;
	st.data_in_len = 37;

	d.atapi_st = &st;
	d.atapi_phase = PHASE_DATAIN;
	d.atapi_cmd_in_progress = 1;
	d.atapi_received = 0;
	d.atapi_len = 37;
	for (i = 0; i < 37; i++)
		wdc_addtoinbuf(&d, payload[i]);

	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 4, MEM_READ, &d);

	/*  Correct: consumed is 4, so 33 remain.  Under `consumed = atapi_len` the whole
	    transfer is swallowed in one read and this reads 0 -- while both end-state rows
	    above stay green, because the transfer does finish at 0 of 37.  */
	rows ++;
	if (d.atapi_len != 33) {
		printf("  FAIL %-38s atapi_len = %i, want 33\n",
		    "mid-walk: one 4-byte read leaves 33", d.atapi_len);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "mid-walk: one 4-byte read leaves 33", d.atapi_len);
	}

	rows ++;
	if (d.atapi_received != 4) {
		printf("  FAIL %-38s received = %i, want 4\n",
		    "mid-walk: cursor advances by 4", (int) d.atapi_received);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "mid-walk: cursor advances by 4", (int) d.atapi_received);
	}

	free(payload);
	free(d.inbuf);
}


/*  THE WIDTH ROW.  Named by the codex seat on pass 1 and MEASURED to escape everything
 *  above: narrow the clamp to `len == 4 && consumed > atapi_len` and every other row in
 *  this file stays green, because every other row issues a FOUR-byte read.
 *
 *  This one issues a TWO-byte read with ONE byte remaining, and it sits on the same
 *  INQUIRY-37 trajectory as the mid-walk row: nine 4-byte reads leave exactly 1.
 *
 *  A detector whose rows all use one access width cannot see a fix narrowed to that
 *  width -- which is the padded-column trap's cousin: the row is present, runs, and is
 *  structurally unable to fail.
 */
static void row_odd_width(void)
{
	struct wdc_data d;
	struct scsi_transfer st;
	unsigned char buf[8];
	unsigned char *payload;
	int i;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = odd_sink;
	if (d.inbuf == NULL) { printf("  SETUP width inbuf failed\n"); return; }

	payload = (unsigned char *) malloc(37);
	if (payload == NULL) { free(d.inbuf); printf("  SETUP width payload failed\n"); return; }
	for (i = 0; i < 37; i++)
		payload[i] = (unsigned char) i;

	memset(&st, 0, sizeof(st));
	st.data_in = payload;
	st.data_in_len = 37;

	d.atapi_st = &st;
	d.atapi_phase = PHASE_DATAIN;
	d.atapi_cmd_in_progress = 1;
	d.atapi_received = 36;		/*  nine 4-byte reads have happened  */
	d.atapi_len = 1;		/*  ...leaving exactly one  */
	wdc_addtoinbuf(&d, payload[36]);

	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_READ, &d);

	/*  consumed is 2 for a 2-byte read; the clamp must cut it to 1.  A clamp that
	    only fires on len == 4 leaves atapi_len at -1 here.  */
	rows ++;
	if (d.atapi_len != 0) {
		printf("  FAIL %-38s atapi_len = %i, want 0\n",
		    "width: a 2-byte read of 1 remaining", d.atapi_len);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "width: a 2-byte read of 1 remaining", d.atapi_len);
	}

	rows ++;
	if (d.atapi_received != 37) {
		printf("  FAIL %-38s received = %i, want 37\n",
		    "width: received stops at data_in_len", (int) d.atapi_received);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "width: received stops at data_in_len", (int) d.atapi_received);
	}

	free(payload);
	free(d.inbuf);
}


/*  THE MULTI-CHUNK ROW.  This is a FLOOR fix, not strengthening.
 *
 *  The Opus seat built `Md5_xferbound` and MEASURED it past every row here: clamp to the
 *  TRANSFER remainder (`data_in_len - atapi_received`) instead of the CHUNK remainder
 *  (`atapi_len`).  It reads MORE correct, and on any single-chunk transfer it IS
 *  identical -- so it is, in that seat's words, the mutant a helpful future reviewer
 *  writes.  It diverges only at a chunk boundary, where it clamps nothing and the
 *  original defect returns.
 *
 *  *** AND IT EXPOSED A FRAMING ERROR IN THIS WHOLE ROUND. ***  "odd chunk" is the wrong
 *  name for the class.  The defect is the remainder not being a MULTIPLE OF THE ACCESS
 *  WIDTH -- so a perfectly EVEN 32768-byte chunk overshoots too, under mixed widths.
 *  Every row above tests one instance of the class; this one tests the other.
 *
 *  The state is placed at the boundary rather than walked to it: 32767 of 40000 received
 *  with 1 left in the chunk, then a 4-byte read.  Markers at data_in[32768] and [32769]
 *  make an off-by-one in the refill's source offset visible as well.
 */
static void row_odd_multichunk(void)
{
	struct wdc_data d;
	struct scsi_transfer st;
	unsigned char buf[8];
	unsigned char *payload;
	int occ;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = odd_sink;
	if (d.inbuf == NULL) { printf("  SETUP multichunk inbuf failed\n"); return; }

	payload = (unsigned char *) calloc(1, 40000);
	if (payload == NULL) { free(d.inbuf); printf("  SETUP multichunk payload failed\n"); return; }
	payload[32768] = 0xa1;		/*  where chunk 2 MUST start  */
	payload[32769] = 0xb2;		/*  one past -- catches an off-by-one  */

	memset(&st, 0, sizeof(st));
	st.data_in = payload;
	st.data_in_len = 40000;

	d.atapi_st = &st;
	d.atapi_phase = PHASE_DATAIN;
	d.atapi_cmd_in_progress = 1;
	d.atapi_received = 32767;	/*  one byte left in chunk 1...  */
	d.atapi_len = 1;		/*  ...of a 40000-byte transfer  */
	wdc_addtoinbuf(&d, 0x5a);

	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 4, MEM_READ, &d);

	/*  Correct: consumed clamps to 1, atapi_len reaches 0, the re-arm fires and
	    refills min(40000 - 32768, 32768) = 7232.  Under Md5_xferbound the clamp
	    compares against 7233 remaining in the TRANSFER, does not fire, and
	    atapi_len lands on -3 -- so `== 0` never fires and no re-arm happens.  */
	rows ++;
	if (d.atapi_len != 7232) {
		printf("  FAIL %-38s atapi_len = %i, want 7232\n",
		    "chunk edge: the re-arm still fires", d.atapi_len);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "chunk edge: the re-arm still fires", d.atapi_len);
	}

	/*  The ANCHORED half: chunk 2 must begin at data_in[32768], not [32769].  */
	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0)
		occ += WDC_INBUF_SIZE;
	rows ++;
	if (occ != 7232 || d.inbuf[d.inbuf_tail] != 0xa1) {
		printf("  FAIL %-38s occ = %i, first = 0x%02x\n",
		    "chunk edge: chunk 2 starts at 32768", occ, d.inbuf[d.inbuf_tail]);
		failures ++;
	} else {
		printf("  ok   %-38s 0x%02x\n",
		    "chunk edge: chunk 2 starts at 32768", d.inbuf[d.inbuf_tail]);
	}

	free(payload);
	free(d.inbuf);
}


/*  THE GUEST-VISIBLE ROW, and it is the only one in this file.
 *
 *  Every other row here reads DEVICE STATE.  A guest cannot see `atapi_len`; what it CAN
 *  see is the ATAPI byte-count-limit pair, served straight from it:
 *
 *        int x = d->atapi_len;
 *        if (x > 32768) x = 32768;
 *        odata = x & 255;            (CYL_LO)  /  (x >> 8) & 255  (CYL_HI)
 *
 *  So a negative count reaches the guest as 0xffff.  The Opus seat measured that this is
 *  the row separating a real fix from one that only repairs completion: an option that
 *  saturates the TEST but leaves atapi_len negative lets the command finish while the
 *  guest is still told 65535 bytes remain.
 *
 *  cur_command stays 0 so the COMMAND_RESET arm short-circuits before
 *  diskimage_is_a_cdrom(), which this harness does not stub.
 */
static void row_odd_bytecount(void)
{
	struct wdc_data d;
	struct scsi_transfer st;
	unsigned char buf[8];
	unsigned char *payload;
	uint64_t lo, hi;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = odd_sink;
	if (d.inbuf == NULL) { printf("  SETUP bytecount inbuf failed\n"); return; }
	payload = (unsigned char *) malloc(3);
	if (payload == NULL) { free(d.inbuf); printf("  SETUP bytecount payload failed\n"); return; }
	payload[0] = 0x11; payload[1] = 0x22; payload[2] = 0x33;

	memset(&st, 0, sizeof(st));
	st.data_in = payload;
	st.data_in_len = 3;
	d.atapi_st = &st;
	d.atapi_phase = PHASE_DATAIN;
	d.atapi_cmd_in_progress = 1;
	d.atapi_received = 0;
	d.atapi_len = 3;
	wdc_addtoinbuf(&d, 0x11);
	wdc_addtoinbuf(&d, 0x22);
	wdc_addtoinbuf(&d, 0x33);

	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 4, MEM_READ, &d);

	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_cyl_lo, buf, 1, MEM_READ, &d);
	lo = memory_readmax64(fake_cpu(), buf, 1);
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_cyl_hi, buf, 1, MEM_READ, &d);
	hi = memory_readmax64(fake_cpu(), buf, 1);

	rows ++;
	if (lo != 0 || hi != 0) {
		printf("  FAIL %-38s guest reads 0x%02x%02x, want 0\n",
		    "guest byte count is not 0xffff", (int) hi, (int) lo);
		failures ++;
	} else {
		printf("  ok   %-38s 0x%02x%02x\n",
		    "guest byte count is not 0xffff", (int) hi, (int) lo);
	}

	free(payload);
	free(d.inbuf);
}


/*  THE ZERO-LENGTH DATAIN ROW.
 *
 *  Also from the Opus seat: a FIFTH route the round's worked path does not cover.  READ
 *  TOC with an allocation length of 0 leaves data_in non-NULL with data_in_len == 0, so
 *  DATAIN is armed with a ZERO chunk and DRQ asserted.  The first read then drives
 *  atapi_len to -2 and the command never completes.
 *
 *  It earns its own row because it is the case a plausible ALTERNATIVE fix fails: a clamp
 *  guarded `atapi_len > 0` rather than `>=` hangs here, and that seat's own draft did.
 */
static void row_odd_zerolen(void)
{
	struct wdc_data d;
	struct scsi_transfer st;
	unsigned char buf[8];
	unsigned char *payload;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = odd_sink;
	if (d.inbuf == NULL) { printf("  SETUP zerolen inbuf failed\n"); return; }
	payload = (unsigned char *) malloc(1);
	if (payload == NULL) { free(d.inbuf); printf("  SETUP zerolen payload failed\n"); return; }
	payload[0] = 0;

	memset(&st, 0, sizeof(st));
	st.data_in = payload;
	st.data_in_len = 0;
	d.atapi_st = &st;
	d.atapi_phase = PHASE_DATAIN;
	d.atapi_cmd_in_progress = 1;
	d.atapi_received = 0;
	d.atapi_len = 0;

	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_READ, &d);

	rows ++;
	if (d.atapi_len != 0) {
		printf("  FAIL %-38s atapi_len = %i, want 0\n",
		    "zero-length DATAIN stays at zero", d.atapi_len);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "zero-length DATAIN stays at zero", d.atapi_len);
	}

	free(payload);
	free(d.inbuf);
}








/*
 *  *** `#475` SHIPPED A GUEST-REACHABLE HOST KILL, AND THIS ROW IS THE BISECT. ***
 *
 *  `#475`'s whole code change is `if (consumed > d->atapi_len) consumed = d->atapi_len;`.
 *  Before it, a data-port READ with `atapi_len == 0` drove the counter NEGATIVE and the
 *  `== 0` test never fired again.  After it, `consumed` clamps to 0, `atapi_len` STAYS 0,
 *  the test FIRES -- and the next line is
 *
 *        if (d->atapi_received < d->atapi_st->data_in_len)
 *
 *  with `atapi_st == NULL`.  The only NULL check on this pointer anywhere in the file is
 *  in the dispatch, hundreds of lines away.
 *
 *  TWO REGISTER ACCESSES FROM A FRESH DEVICE: write ATAPI_PKT_CMD to COMMAND, then read
 *  DATA.  A panel seat measured `SEGV on unknown address 0x48` -- which is
 *  `offsetof(struct scsi_transfer, data_in_len)` from NULL -- and confirmed the pre-`#475`
 *  blob survives the same input.
 *
 *  *A fix that stops a counter going negative made a previously-unreachable branch
 *  reachable.  The clamp is right; the branch it enabled was never NULL-safe.*
 *
 *  THE ROW FORKS, because the defect is a SIGNAL: an in-process oracle would take the
 *  whole differential down with it and report nothing.
 */
static void row_null_atapi_st(void)
{
	pid_t pid;
	int st = 0;

	fflush(stdout);
	pid = fork();
	if (pid == 0) {
		struct wdc_data d;
		unsigned char buf[4];
		memset(&d, 0, sizeof(d));
		d.addr_mult  = 1;
		d.io_enabled = 1;
		d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
		d.irq.interrupt_assert = arm_sink;
		/*  exactly what the two guest accesses leave behind: a packet command
		    announced, no transfer yet allocated.  */
		d.atapi_cmd_in_progress = 1;
		d.atapi_phase = PHASE_DATAIN;
		d.atapi_st = NULL;
		d.atapi_len = 0;
		d.atapi_received = 0;
		memset(buf, 0, sizeof(buf));
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_READ, &d);
		_exit(0);
	}
	if (pid < 0) { printf("  SETUP fork failed\n"); return; }
	waitpid(pid, &st, 0);

	rows ++;
	if (WIFSIGNALED(st)) {
		printf("  FAIL %-38s host killed, signal %i\n",
		    "a DATA read with no transfer survives", WTERMSIG(st));
		failures ++;
	} else {
		printf("  ok   %-38s exit %i\n",
		    "a DATA read with no transfer survives", WEXITSTATUS(st));
	}
}


/*
 *  `wdccdbmidxfer`: a mid-DATAIN data-port WRITE can FREE THE IN-FLIGHT TRANSFER.
 *
 *  The packet dispatch fires on ring occupancy == 12, gated only by
 *  `atapi_cmd_in_progress` -- which stays 1 for the whole of DATAIN.  The data-port WRITE
 *  arm pushes guest bytes with NO PHASE CHECK, so a guest that writes twelve bytes while a
 *  DATAIN transfer is live drives occupancy to exactly 12 and re-enters the dispatch:
 *
 *        if (d->atapi_st != NULL)
 *                scsi_transfer_free(d->atapi_st);     <- the LIVE transfer
 *        d->atapi_st = scsi_transfer_alloc();
 *
 *  *** AN EARLIER VERSION OF THIS COMMENT CALLED THAT A USE-AFTER-FREE.  A PANEL SEAT
 *  READ IT FALSE AND IT IS RIGHT. ***  After the free the code allocates a replacement
 *  and then RESETS `atapi_len = 0` and `atapi_received = 0` on both exits -- the reject
 *  path and the normal one.  The cursor is re-based onto the NEW transfer inside the
 *  same access, so no later read dangles through `data_in[atapi_received]`.
 *
 *  *A hazard inferred from a free site is a hypothesis about what happens NEXT, and what
 *  happens next has to be read separately.  The reset is nine lines below the free.*
 *
 *  WHAT THE DEFECT ACTUALLY IS, and it is still worth fixing:
 *    (1) the in-flight transfer is DESTROYED -- the guest's read stream is silently
 *        aborted mid-delivery, with no error reported to it;
 *    (2) a SPURIOUS SCSI COMMAND is executed against the disk image, and its opcode is
 *        `scsi_cmd[0]` -- a leftover DATAIN PAYLOAD byte.  What command runs is
 *        influenced by data the guest chose to have read back to it.
 *
 *  That is an integrity and spurious-command defect, NOT a host memory-safety
 *  primitive.  Ranked accordingly.
 *
 *  THE ORACLE IS A FREE COUNT, not a sanitiser, so the row works in an ordinary build:
 *  a mid-DATAIN write must not free the transfer the guest is still reading.
 *
 *  NOT A #475 DEFECT and not introduced by any round here -- the dispatch has always been
 *  phase-blind.  Filed from reading, then measured.
 */
static void row_cdb_midxfer(void)
{
	struct wdc_data d;
	unsigned char buf[4];
	int i, freed_during;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) { printf("  SETUP midxfer inbuf failed\n"); return; }

	/*  arm a real DATAIN transfer through the packet path, as row_arm_overrun does  */
	/*  #477 pass 2: the real device sets cur_command with the flag and the
	    phase (`cur_command = idata`, then the ATAPI_PKT_CMD arm).  Without
	    it a mutant conjoining `cur_command == ATAPI_PKT_CMD` kills this row
	    by removing LEGAL dispatch -- a false-path kill.  */
	d.cur_command = ATAPI_PKT_CMD;
	d.atapi_cmd_in_progress = 1;
	/*  SETUP RE-PIN, and it is INERT on the committed build: the real
	    device sets BOTH flags together when the packet command
	    arrives, so a fixture setting only atapi_cmd_in_progress
	    builds a state the device never produces.  A candidate fix
	    that keys on the PHASE would then fail here for the fixture's
	    reason rather than its own.  */
	d.atapi_phase = PHASE_CMDOUT;
	for (i = 0; i < 10; i++)
		wdc_addtoinbuf(&d, 0x00);
	stub_datain_len = 10;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	stub_datain_len = 0;

	/*  the guest has drained nothing; the transfer is LIVE and data_in is in use  */
	stub_frees = 0;

	/*  *** THE ARITHMETIC THAT MAKES THIS REACHABLE, and my first fixture had
	    it wrong. ***  During DATAIN the ring holds exactly `atapi_len` bytes,
	    so occupancy == 12 means TEN UNDRAINED plus a two-byte write.  The
	    first attempt armed 4096 bytes, so occupancy went 4096 -> 4108 and the
	    `== 12` equality could never fire: the row was GREEN and the defect was
	    simply not reached.

	    A ten-byte transfer is the smallest live state that reaches it, and it
	    is an ordinary one -- any DATAIN with ten bytes still queued.  */
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	freed_during = stub_frees;

	rows ++;
	if (freed_during != 0) {
		printf("  FAIL %-38s freed %i live transfer(s)\n",
		    "a mid-DATAIN write frees nothing", freed_during);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a mid-DATAIN write frees nothing", freed_during);
	}

	if (d.atapi_st != NULL) {
		free(d.atapi_st->data_in);
		free(d.atapi_st->cmd);
		free(d.atapi_st);
	}
	free(d.inbuf);
}


/*  OCCUPANCY ALREADY 12 -- the row that would have caught the fix I preferred.
 *
 *  A panel seat argued (REASONED) that guarding only the PUSH is not enough, because the
 *  dispatch runs whether or not a push happened.  Arm a DATAIN whose queued occupancy is
 *  ALREADY 12 -- a 12-byte INQUIRY response, or a larger chunk read down to twelve -- and
 *  any data-port write reaches the dispatch with occupancy still 12.
 *
 *  The row above tests TEN QUEUED PLUS A TWO-BYTE WRITE, so a push-only guard would have
 *  scored it GREEN while this case still freed the live transfer.  This row exists to make
 *  that difference visible, and it converts the seat's reasoning into a measurement.
 */
static void row_cdb_already12(void)
{
	struct wdc_data d;
	unsigned char buf[4];
	int i;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) { printf("  SETUP already12 inbuf failed\n"); return; }

	/*  arm a TWELVE-byte transfer: occupancy is then exactly 12 with nothing drained  */
	/*  #477 pass 2: the real device sets cur_command with the flag and the
	    phase (`cur_command = idata`, then the ATAPI_PKT_CMD arm).  Without
	    it a mutant conjoining `cur_command == ATAPI_PKT_CMD` kills this row
	    by removing LEGAL dispatch -- a false-path kill.  */
	d.cur_command = ATAPI_PKT_CMD;
	d.atapi_cmd_in_progress = 1;
	/*  SETUP RE-PIN, and it is INERT on the committed build: the real
	    device sets BOTH flags together when the packet command
	    arrives, so a fixture setting only atapi_cmd_in_progress
	    builds a state the device never produces.  A candidate fix
	    that keys on the PHASE would then fail here for the fixture's
	    reason rather than its own.  */
	d.atapi_phase = PHASE_CMDOUT;
	for (i = 0; i < 10; i++)
		wdc_addtoinbuf(&d, 0x00);
	stub_datain_len = 12;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	stub_datain_len = 0;

	stub_frees = 0;

	/*  a ONE-byte write: the push is what a phase guard on the push arm would stop,
	    and it is NOT what makes this reachable -- occupancy was 12 beforehand.  */
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 1, MEM_WRITE, &d);

	rows ++;
	if (stub_frees != 0) {
		printf("  FAIL %-38s freed %i at occupancy 12\n",
		    "a write at occupancy 12 frees nothing", stub_frees);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a write at occupancy 12 frees nothing", stub_frees);
	}

	if (d.atapi_st != NULL) {
		free(d.atapi_st->data_in);
		free(d.atapi_st->cmd);
		free(d.atapi_st);
	}
	free(d.inbuf);
}


/*  THE THREE ROWS THE BRIEF DID NOT HAVE, each named by a measuring seat and each the
 *  SOLE carrier of a one-token escape past a DATAIN-only detector.
 *
 *    no-push    a len-3 write pushes ZERO bytes -- the width switch's `default:` arm only
 *               latches -- and control falls straight through to the dispatch.  This is
 *               the row that proves the defect is NOT "writes push foreign bytes"; the
 *               dispatch runs on every data-port write regardless of what the write did.
 *    DATAOUT    twelve DATA-OUT payload bytes are read as a CDB.
 *    COMPLETED  the flag is never cleared at completion, so twelve bytes AFTER a finished
 *               command still free the completed transfer and issue a garbage command.
 *
 *  A guard written `atapi_phase != PHASE_DATAIN` passes every DATAIN row and leaves all
 *  three of these open.  A seat measured exactly that mutant sweeping the earlier table.
 */
static void midxfer_case(const char *name, int phase, int prefill,
	int alen, int wlen)
{
	struct wdc_data d;
	struct scsi_transfer *st;
	unsigned char buf[8], *payload;
	int i;

	/*  *** THE TRANSFER MUST BE HEAP-ALLOCATED, and the first version of this
	    fixture put it on the STACK. ***  On the unfixed build the dispatch calls
	    scsi_transfer_free() on it -- so a stack object gave
	    `double free or corruption (out)` and the run ABORTED partway, losing
	    every row after it.  A measuring seat hit the identical flaw in its own
	    first fixture.

	    An abort is not a FAIL: the rows that never ran print nothing at all, and
	    the verdict line is missing rather than red.  */

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	payload = (unsigned char *) calloc(1, 64);
	if (d.inbuf == NULL || payload == NULL) {
		printf("  SETUP %s alloc failed\n", name);
		free(d.inbuf); free(payload); return;
	}
	st = (struct scsi_transfer *) calloc(1, sizeof(*st));
	if (st == NULL) { free(d.inbuf); free(payload);
		printf("  SETUP %s xfer alloc failed@", name); return; }
	st->data_in = payload;  st->data_in_len = 64;

	/*  a live transfer, in the phase under test, with `prefill` bytes queued  */
	d.atapi_st = st;
	/*  #477 pass 2, codex: THE REAL DEVICE SETS ALL THREE TOGETHER.
	    `cur_command = idata` then the ATAPI_PKT_CMD arm sets the flag AND
	    the phase, so a fixture setting only two builds a state the device
	    never produces -- and a mutant adding `cur_command == ATAPI_PKT_CMD`
	    then dies because LEGAL DISPATCH vanishes, not because of the defect.
	    That is a FALSE-PATH KILL: the table scores it caught and it proves
	    nothing.  (Inert on the committed build: the only other reads compare
	    against COMMAND_RESET = 0x100, which 0xa0 is not.)  */
	d.cur_command = ATAPI_PKT_CMD;
	d.atapi_cmd_in_progress = 1;
	d.atapi_phase = phase;
	/*  `alen` is DECOUPLED from `prefill`: prefill is what the RING holds,
	    alen is the transfer's remaining count.  They coincide in DATAIN and
	    must NOT in COMPLETED -- see the caller.  */
	d.atapi_len = alen;
	d.atapi_received = 0;
	for (i = 0; i < prefill; i++)
		wdc_addtoinbuf(&d, 0x5a);

	stub_frees = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, wlen, MEM_WRITE, &d);

	rows ++;
	if (stub_frees != 0) {
		printf("  FAIL %-38s freed %i\n", name, stub_frees);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n", name, stub_frees);
	}
	/*  the dispatch may have freed and replaced it; free whatever is there now  */
	if (d.atapi_st != NULL && d.atapi_st != st) {
		free(d.atapi_st->data_in);
		free(d.atapi_st->cmd);
		free(d.atapi_st);
	} else if (d.atapi_st == st) {
		free(st);
	}
	free(payload);
	free(d.inbuf);
}

static void row_midxfer_phases(void)
{
	/*  occupancy 12 already, then a len-3 write that pushes NOTHING  */
	midxfer_case("no-push write does not dispatch", PHASE_DATAIN, 12, 12, 3);
	/*  ten queued plus a two-byte write, in the two phases DATAIN rows miss  */
	midxfer_case("a DATAOUT write does not dispatch", PHASE_DATAOUT, 10, 10, 2);
	/*  *** THE COMPLETED FIXTURE USED TO SET atapi_len = 10, WHICH THE DEVICE
	    CANNOT PRODUCE.  Found by the codex seat on #477 pass 2. ***

	    EVERY real transition to PHASE_COMPLETED leaves atapi_len == 0: the
	    reject path assigns zero explicitly, the ordinary path assigns zero
	    before selecting its phase, and terminal DATAIN only completes once
	    the count has reached zero.  So a guard widened by `|| atapi_len == 0`
	    passed this row for the FIXTURE's reason and swept the table, while a
	    real completed command plus twelve guest DATA writes still re-enters
	    dispatch and frees the completed transfer.

	    Ten bytes still sit in the RING (so the 2-byte write reaches occupancy
	    12 and the dispatch is genuinely attempted); only the COUNT is zero.
	    That is the state a real device is in, and it is the row codex named
	    `row_completed_zero_len`.  */
	midxfer_case("a COMPLETED write does not dispatch", PHASE_COMPLETED, 10, 0, 2);
}


/*  #477 pass 2 -- THE ACCEPT SIDE, WHICH THE SHIPPED TABLE DID NOT HAVE.
 *
 *  Two seats found this independently: NO row proved a legal CDB actually
 *  DISPATCHES.  `row_cdb_already12` asserts nothing is FREED, which is a reject
 *  assertion -- so a fix that suppressed every dispatch would have passed the
 *  whole table.  The de-escalation clause calls these rows part of the FIX'S
 *  COST, not future strengthening.
 *
 *  The stale state is the point.  ATAPI_PKT_CMD assigns only the flag and the
 *  phase, so after a PRIOR COMPLETED command a new packet begins with
 *  atapi_len == 0, atapi_received == data_in_len and atapi_st STALE NON-NULL.
 *  Every fixture in this file is memset-fresh and none crosses a command
 *  boundary, so that entire dimension was invisible.
 */
static void pkt_cdb_case(const char *name, int stray_read)
{
	struct wdc_data d;
	struct scsi_transfer *st;
	unsigned char buf[4], *payload;
	int i;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	payload = (unsigned char *) calloc(1, 64);
	st = (struct scsi_transfer *) calloc(1, sizeof(*st));
	if (d.inbuf == NULL || payload == NULL || st == NULL) {
		printf("  SETUP %s alloc failed\n", name);
		free(d.inbuf); free(payload); free(st); return;
	}
	st->data_in = payload;  st->data_in_len = 64;

	/*  a PRIOR COMPLETED command: fully received, count exhausted, transfer
	    still hanging off the device (it is freed at the NEXT dispatch and
	    never NULLed).  */
	d.atapi_st = st;
	d.atapi_received = 64;
	d.atapi_len = 0;

	/*  then A0h arrives -- it assigns EXACTLY these three and resets nothing.  */
	d.cur_command = ATAPI_PKT_CMD;
	d.atapi_cmd_in_progress = 1;
	d.atapi_phase = PHASE_CMDOUT;

	if (stray_read) {
		/*  ONE out-of-protocol data-port read in the CDB window.  Without the
		    #477 read-arm guard this rewrites the phase to PHASE_COMPLETED.  */
		memset(buf, 0, sizeof(buf));
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_READ, &d);
	}

	stub_scsi_cmds = 0;
	/*  a legal twelve-byte CDB: six 16-bit writes from an empty ring.  */
	for (i = 0; i < 6; i++) {
		memset(buf, 0, sizeof(buf));
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	rows ++;
	if (stub_scsi_cmds != 1) {
		printf("  FAIL %-38s dispatched %i, want 1\n",
			name, stub_scsi_cmds);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n", name, stub_scsi_cmds);
	}

	if (d.atapi_st != NULL && d.atapi_st != st) {
		free(d.atapi_st->data_in);
		free(d.atapi_st->cmd);
		free(d.atapi_st);
	} else if (d.atapi_st == st) {
		free(st);
	}
	free(payload);
	free(d.inbuf);
}

static void row_pkt_cdb_accept(void)
{
	/*  CONTROL first: the same fixture with no stray read MUST dispatch, so a
	    red below is attributable to the read and not to the fixture.  */
	pkt_cdb_case("completed, PKT then CDB dispatches", 0);
	/*  THE SOLE CARRIER of the #477 read-arm guard.  MEASURED by the Fable seat:
	    HEAD services this sequence; the phase guard alone wedges it FOREVER,
	    because the 12-byte residue means occupancy can never EQUAL 12 again.  */
	pkt_cdb_case("a stray read does not wedge the CDB", 1);
}

/*  #477 pass 2 -- THE ROW THAT PINS THE `malloc(12)` BOUND.
 *
 *  The kill table's `M7_ge12` mutant (`inbuf_len == 12` relaxed to `>= 12`) swept
 *  44 rows clean, and the table's first draft classified it as an IMPROVEMENT --
 *  dispatching on an overshoot beating never dispatching.  The Opus seat measured
 *  it under ASAN instead and got a heap-buffer-overflow WRITE, because nine lines
 *  below the guard:
 *
 *      CHECK_ALLOCATION(scsi_cmd = (unsigned char *) malloc(12));
 *      while (inbuf_len > 0) { scsi_cmd[x++] = wdc_get_inbuf(d); inbuf_len--; }
 *
 *  `x` is unbounded.  The equality is not only selecting the dispatch -- it is the
 *  ONLY thing bounding that copy.  Four readers reasoned about it as a dispatch
 *  predicate and none opened the tail it protects.
 *
 *  This row reds on `>= 12` WITHOUT needing a sanitiser: the oracle is the dispatch
 *  count, so an ordinary build catches it.  Reaching occupancy 13 without passing
 *  THROUGH 12 is the whole trick -- preload an odd count, then write one byte.
 */
static void row_cdb_overshoot(void)
{
	struct wdc_data d;
	unsigned char buf[4];
	int i;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) { printf("  SETUP overshoot inbuf failed\n"); return; }

	d.cur_command = ATAPI_PKT_CMD;
	d.atapi_cmd_in_progress = 1;
	d.atapi_phase = PHASE_CMDOUT;

	/*  THIRTEEN queued, so the one-byte write below lands on 14 and the ring
	    never passes through 12.  A fixture that wrote its way up two bytes at
	    a time would dispatch at 12 and never reach the overshoot at all.  */
	for (i = 0; i < 13; i++)
		wdc_addtoinbuf(&d, 0x5a);

	stub_scsi_cmds = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 1, MEM_WRITE, &d);

	rows ++;
	if (stub_scsi_cmds != 0) {
		printf("  FAIL %-38s dispatched %i at occupancy 14\n",
			"occupancy above 12 does not dispatch", stub_scsi_cmds);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
			"occupancy above 12 does not dispatch", stub_scsi_cmds);
	}

	if (d.atapi_st != NULL) {
		free(d.atapi_st->data_in);
		free(d.atapi_st->cmd);
		free(d.atapi_st);
	}
	free(d.inbuf);
}

/*  wdcdataoutdrain -- REPRODUCTION, not yet a shipped row.
 *
 *  `inbuf_len == 0` satisfies `0 % 512 == 0`, so the write-back block fires with an
 *  EMPTY ring and hands diskimage_access 512 bytes of whatever the ring happens to
 *  hold, at the guest's chosen LBA.
 *
 *  The entrance is #337's own de-fatalised arm: a 3- or 8-byte data-port write pushes
 *  NOTHING (the width switch has no case for it) and `break` leaves the SWITCH, not the
 *  handler -- so execution falls straight through to the drain with occupancy 0.
 *
 *  The ring is deliberately POISONED with 0xDD first, so the oracle can say the bytes
 *  written are ones the guest never supplied rather than merely counting a write.
 */
static void row_dataout_drain(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int i;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) { printf("  SETUP drain inbuf failed\n"); return; }

	/*  poison: any byte reaching the image is one the guest never wrote  */
	for (i = 0; i < WDC_INBUF_SIZE; i++)
		d.inbuf[i] = 0xdd;

	/*  a WRITE command is in progress and the ring is EMPTY (head == tail == 0)  */
	d.write_in_progress = WDCC_WRITE;
	d.write_count  = 1;
	d.write_offset = 0x8000;

	stub_disk_writes = 0; stub_disk_bytes = 0; stub_disk_offset = 0;
	stub_disk_first = -1;

	/*  ONE 3-byte data-port write.  Pushes nothing; falls through to the drain.  */
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 3, MEM_WRITE, &d);

	rows ++;
	if (stub_disk_writes != 0) {
		printf("  FAIL %-38s %i write(s), %i bytes to 0x%lx, first=0x%02x\n",
			"an empty ring writes nothing to disk",
			stub_disk_writes, stub_disk_bytes, stub_disk_offset,
			stub_disk_first);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
			"an empty ring writes nothing to disk", stub_disk_writes);
	}

	/*  the SIBLING, and it is the same condition: an 8-byte access.  A 64-bit guest
	    writing a sector with `sd` stores would fire this 64 times at consecutive
	    offsets.  Separate device so the first row's drain cannot mask it.  */
	{
		struct wdc_data e;
		memset(&e, 0, sizeof(e));
		e.addr_mult  = 1;
		e.io_enabled = 1;
		e.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
		e.irq.interrupt_assert = arm_sink;
		if (e.inbuf == NULL) { free(d.inbuf); return; }
		for (i = 0; i < WDC_INBUF_SIZE; i++)
			e.inbuf[i] = 0xdd;
		e.write_in_progress = WDCC_WRITE;
		e.write_count  = 1;
		e.write_offset = 0x8000;
		stub_disk_writes = 0; stub_disk_bytes = 0;
		memset(buf, 0, sizeof(buf));
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &e);
		rows ++;
		if (stub_disk_writes != 0) {
			printf("  FAIL %-38s %i write(s), %i bytes\n",
				"an 8-byte write drains nothing",
				stub_disk_writes, stub_disk_bytes);
			failures ++;
		} else {
			printf("  ok   %-38s %i\n",
				"an 8-byte write drains nothing", stub_disk_writes);
		}
		free(e.inbuf);
	}

	/*  *** THE LEFTOVER ENTRANCE, named by the grok seat and NOT closed by
	    `inbuf_len > 0`.  Leave 512 bytes UNREAD in the ring (an unread IDENTIFY or
	    DATA-IN response), start a WRITE, then do the same 8-byte store.  Occupancy
	    is 512, not 0 -- so `512 %% 512 == 0` AND `512 > 0` both pass, and the
	    guest's own returned payload is written to the disk image at its chosen
	    LBA.  Poisoned 0xBE so the byte identifies WHICH entrance fired.  ***  */
	{
		struct wdc_data f;
		memset(&f, 0, sizeof(f));
		f.addr_mult  = 1;
		f.io_enabled = 1;
		f.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
		f.irq.interrupt_assert = arm_sink;
		if (f.inbuf == NULL) { free(d.inbuf); return; }
		for (i = 0; i < 512; i++)
			wdc_addtoinbuf(&f, 0xbe);
		f.write_in_progress = WDCC_WRITE;
		f.write_count  = 1;
		f.write_offset = 0x9000;
		stub_disk_writes = 0; stub_disk_bytes = 0; stub_disk_first = -1;
		memset(buf, 0, sizeof(buf));
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &f);
		rows ++;
		if (stub_disk_writes != 0) {
			printf("  FAIL %-38s %i write(s), first=0x%02x\n",
				"leftover payload not written to disk",
				stub_disk_writes, stub_disk_first);
			failures ++;
		} else {
			printf("  ok   %-38s %i\n",
				"leftover payload not written to disk", stub_disk_writes);
		}
		free(f.inbuf);
	}

	free(d.inbuf);
}

/*  THE WRITE+PKT DOOR, measured independently by the Fable seat.
 *
 *  No bad-len access is involved at all.  A WRITE is in progress AND a packet
 *  command is being assembled; the 12-byte CDB dispatches, and the dispatch loop
 *  consumes the LOCAL `inbuf_len` down to 0 while pushing fresh DATA-IN bytes into
 *  the ring.  The drain below therefore reads a STALE ZERO and fires, putting the
 *  guest's own returned DATA-IN payload on the disk image.
 *
 *  This door is closed by `inbuf_len > 0` (the stale local is 0) and is NOT closed
 *  by declining the bad-len width, because no bad-len access occurs.  The leftover
 *  door is the exact mirror.  That is why neither edit alone is sufficient.
 */
static void row_pkt_drain(void)
{
	struct wdc_data g;
	unsigned char buf[8];
	int i;

	memset(&g, 0, sizeof(g));
	g.addr_mult  = 1;
	g.io_enabled = 1;
	g.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	g.irq.interrupt_assert = arm_sink;
	if (g.inbuf == NULL) {
		printf("  SETUP pkt_drain inbuf failed\n");
		return;
	}

	/*  the real device sets all three together  */
	g.cur_command = ATAPI_PKT_CMD;
	g.atapi_cmd_in_progress = 1;
	g.atapi_phase = PHASE_CMDOUT;

	/*  ...and a disk WRITE is live at the same time  */
	g.write_in_progress = WDCC_WRITE;
	g.write_count  = 1;
	g.write_offset = 0xa000;

	for (i = 0; i < 10; i++)
		wdc_addtoinbuf(&g, 0x5a);

	stub_datain_len = 512;
	stub_disk_writes = 0;
	stub_disk_first = -1;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &g);
	stub_datain_len = 0;

	rows ++;
	if (stub_disk_writes != 0) {
		printf("  FAIL %-38s %i write(s), first=0x%02x\n",
		    "a CDB dispatch does not drain to disk",
		    stub_disk_writes, stub_disk_first);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a CDB dispatch does not drain to disk", stub_disk_writes);
	}

	if (g.atapi_st != NULL) {
		free(g.atapi_st->data_in);
		free(g.atapi_st->cmd);
		free(g.atapi_st);
	}
	free(g.inbuf);
}


/*  THE ACCEPT ROW FOR THE BAD-LEN DECLINE.
 *
 *  A fix that declines the drain after an unimplemented width MUST NOT latch that
 *  decision for the life of the device.  If the flag is a struct field, one 8-byte
 *  store silences every subsequent legal write -- turning a corruption defect into
 *  a silent data-loss defect, which is worse.
 *
 *  Sequence: one bad-len (8-byte) store, then a full LEGAL 512-byte write via
 *  256 two-byte stores.  The legal write MUST reach the disk image.
 *
 *  Expected: RED under a persistent struct-field flag; GREEN under a per-access
 *  local.  That is the whole point of the row -- it distinguishes two fixes that
 *  the four corruption rows score identically.
 */
static void row_badlen_then_legal(void)
{
	struct wdc_data h;
	unsigned char buf[8];
	int i;

	memset(&h, 0, sizeof(h));
	h.addr_mult  = 1;
	h.io_enabled = 1;
	h.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	h.irq.interrupt_assert = arm_sink;
	if (h.inbuf == NULL) {
		printf("  SETUP badlen_then_legal inbuf failed\n");
		return;
	}

	h.write_in_progress = WDCC_WRITE;
	h.write_count  = 1;
	h.write_offset = 0xb000;

	/*  (1) the bad-len store -- pushes nothing, must drain nothing  */
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &h);

	/*  (2) a full legal sector, 256 two-byte stores carrying 0x77  */
	stub_disk_writes = 0;
	stub_disk_bytes = 0;
	stub_disk_first = -1;
	for (i = 0; i < 256; i++) {
		buf[0] = 0x77; buf[1] = 0x77;
		buf[2] = 0; buf[3] = 0;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &h);
	}

	rows ++;
	if (stub_disk_writes != 1 || stub_disk_bytes != 512) {
		printf("  FAIL %-38s %i write(s), %i bytes\n",
		    "a legal write after a bad-len lands",
		    stub_disk_writes, stub_disk_bytes);
		failures ++;
	} else {
		printf("  ok   %-38s %i write(s), %i bytes\n",
		    "a legal write after a bad-len lands",
		    stub_disk_writes, stub_disk_bytes);
	}

	free(h.inbuf);
}


/*  THE PARTIAL-SECTOR ROW.  Named by the codex seat after `M10_modinv` -- the
 *  modulus inverted from `== 0` to `!= 0` -- swept a 50-row table clean.
 *
 *  That mutant does not open the empty-ring door (the `inbuf_len > 0` half still
 *  holds), so every corruption row stays green.  What it does is authorise a
 *  512-byte disk write on ONE buffered byte, while exactly 512 bytes fail to
 *  drain.  The accept row cannot see it either: it observes one write of 512
 *  bytes, which is the right SHAPE at the wrong MOMENT.
 *
 *  So the sufficiency condition needs pinning from below as well as at the
 *  boundary: occupancy 1 and needed-1 must write NOTHING.
 */
static void row_partial_sector(void)
{
	struct wdc_data j;
	unsigned char buf[8];
	int i;

	memset(&j, 0, sizeof(j));
	j.addr_mult  = 1;
	j.io_enabled = 1;
	j.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	j.irq.interrupt_assert = arm_sink;
	if (j.inbuf == NULL) {
		printf("  SETUP partial_sector inbuf failed\n");
		return;
	}

	j.write_in_progress = WDCC_WRITE;
	j.write_count  = 1;
	j.write_offset = 0xc000;

	stub_disk_writes = 0;
	stub_disk_bytes = 0;

	/*  255 two-byte stores: occupancy climbs 2..510, one short of a sector.
	    NOT ONE of them may reach the disk.  */
	for (i = 0; i < 255; i++) {
		buf[0] = 0x33; buf[1] = 0x33;
		buf[2] = 0; buf[3] = 0;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &j);
	}

	rows ++;
	if (stub_disk_writes != 0) {
		printf("  FAIL %-38s %i write(s) at occupancy < 512\n",
		    "a partial sector does not drain", stub_disk_writes);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a partial sector does not drain", stub_disk_writes);
	}

	/*  the 256th store completes the sector: exactly one write, exactly 512
	    bytes, at exactly the offset the command named.  */
	buf[0] = 0x33; buf[1] = 0x33;
	buf[2] = 0; buf[3] = 0;
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &j);

	rows ++;
	if (stub_disk_writes != 1 || stub_disk_bytes != 512 ||
	    stub_disk_offset != 0xc000) {
		printf("  FAIL %-38s %i w, %i b, off 0x%lx\n",
		    "completing store drains one sector",
		    stub_disk_writes, stub_disk_bytes, stub_disk_offset);
		failures ++;
	} else {
		printf("  ok   %-38s %i w, %i b\n",
		    "completing store drains one sector",
		    stub_disk_writes, stub_disk_bytes);
	}

	free(j.inbuf);
}


/*  THE ROW `#477` OWED.  Prescribed by the codex seat on `#477`'s pass 2, after it
 *  reasoned that deleting the `atapi_cmd_in_progress` conjunct from the dispatch
 *  guard would sweep the table.  MEASURED: it swept all 52 rows clean.
 *
 *  THE STALE PHASE IS THE POINT.  `wdc_command(ATAPI_PKT_CMD)` sets PHASE_CMDOUT.
 *  A following `wdc_command(WDCC_WRITE)` clears the flag at the top of the function
 *  and arms the write -- but NOTHING RESETS THE PHASE.  So the device sits with
 *  `phase == PHASE_CMDOUT`, `atapi_cmd_in_progress == 0`, and a disk write armed:
 *  exactly the state a phase-only guard cannot tell from a real CDB collection.
 *
 *  Under that mutant, the guest's own sector payload reaches occupancy 12 and the
 *  first twelve bytes are issued as a SCSI command AND removed from the pending
 *  sector.  Both conjuncts are load-bearing; `#477`'s "key on the phase, not on
 *  the flag" was the wrong headline and is corrected in place.
 *
 *  (The stale phase is itself a defect and is filed as part of `wdcwipclear` /
 *  `wdcringnoflush` -- a new command does not reset what the old one left.)
 */
static void row_stale_phase_write(void)
{
	struct wdc_data d;
	unsigned char buf[4];
	int i;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) {
		printf("  SETUP stale_phase inbuf failed\n");
		return;
	}

	stub_disk_exists = 1;
	d.seccnt = 1;
	d.sector = 1;

	/*  a packet command, which is what leaves PHASE_CMDOUT behind  */
	wdc_command(fake_cpu(), &d, ATAPI_PKT_CMD);

	/*  then an ordinary ATA write.  This clears the flag and arms the write; the
	    phase is NOT reset, which is the state under test.  */
	wdc_command(fake_cpu(), &d, WDCC_WRITE);

	rows ++;
	if (d.atapi_phase != PHASE_CMDOUT || d.atapi_cmd_in_progress != 0 ||
	    d.write_in_progress == 0) {
		printf("  FAIL %-38s phase %i flag %i wip %i\n",
		    "LIVENESS: stale CMDOUT with a write",
		    d.atapi_phase, d.atapi_cmd_in_progress,
		    d.write_in_progress);
		failures ++;
	} else {
		printf("  ok   %-38s phase 0x%x\n",
		    "LIVENESS: stale CMDOUT with a write", d.atapi_phase);
	}

	/*  the guest streams one legal sector, 256 sixteen-bit stores  */
	stub_scsi_cmds = 0;
	stub_disk_writes = 0;
	stub_disk_bytes = 0;
	for (i = 0; i < 256; i++) {
		buf[0] = 0x6b; buf[1] = 0x6b;
		buf[2] = 0; buf[3] = 0;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	/*  NO byte of a disk payload may be issued as a SCSI command...  */
	rows ++;
	if (stub_scsi_cmds != 0) {
		printf("  FAIL %-38s %i SCSI dispatch(es)\n",
		    "disk payload is not issued as a CDB", stub_scsi_cmds);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "disk payload is not issued as a CDB", stub_scsi_cmds);
	}

	/*  ...and the sector must arrive INTACT, which is the half that catches a
	    mutant that merely eats the bytes without dispatching.  */
	rows ++;
	if (stub_disk_writes != 1 || stub_disk_bytes != 512) {
		printf("  FAIL %-38s %i w, %i b\n",
		    "the sector survives a stale phase",
		    stub_disk_writes, stub_disk_bytes);
		failures ++;
	} else {
		printf("  ok   %-38s %i w, %i b\n",
		    "the sector survives a stale phase",
		    stub_disk_writes, stub_disk_bytes);
	}

	stub_disk_exists = 0;
	if (d.atapi_st != NULL) {
		free(d.atapi_st->data_in);
		free(d.atapi_st->cmd);
		free(d.atapi_st);
	}
	free(d.inbuf);
}


/*  THE ACCEPT ROW FOR THE `cur_command` ESCAPE -- and it exists because the round's
 *  own disposition was INVERTED.
 *
 *  `#477` filed that escape as REAL COVERAGE DEBT: the ALT-CTRL arm sets
 *  `cur_command = COMMAND_RESET` without clearing `atapi_cmd_in_progress`, so the
 *  state that distinguishes the mutant is reachable.  That warrant is right.  The
 *  conclusion drawn from it was backwards.
 *
 *  MEASURED by a seat, through real register accesses: adding
 *  `&& cur_command == ATAPI_PKT_CMD` makes ZERO OF THREE legal packet commands
 *  dispatch, and the wedge is permanent -- the 12-byte residue blocks the dispatch
 *  even after `cur_command` returns to 0xA0.  The reachability is what makes that
 *  conjunct DANGEROUS.
 *
 *  A "coverage debt" filing invites a future round to close the debt by ADDING the
 *  conjunct.  This row makes that edit RED instead: a legal CDB delivered after an
 *  ALT-CTRL write must still dispatch.
 */
static void row_altctl_cdb_accept(void)
{
	struct wdc_data d;
	unsigned char buf[4];
	int i;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) {
		printf("  SETUP altctl inbuf failed\n");
		return;
	}

	stub_disk_exists = 1;
	stub_datain_len = 64;

	/*  a real packet command  */
	wdc_command(fake_cpu(), &d, ATAPI_PKT_CMD);

	/*  an ALT-CTRL write with WDCTL_4BIT, which this device treats as a reset
	    latch: it sets cur_command = COMMAND_RESET and clears NOTHING else.
	    Guest-reachable with one ordinary register write.  */
	memset(buf, 0, sizeof(buf));
	buf[0] = WDCTL_4BIT;
	/*  *** THE ALT-CTRL REGISTER IS A SEPARATE REGISTERED DEVICE, and the first
	    version of this row wrote to `dev_wdc_access` at relative_addr 0 -- which
	    is `wd_data`.  It pushed a byte into the RING, so occupancy reached 13
	    instead of 12 and the CDB never dispatched.  The row RED on the shipped
	    build, which is a mis-cut row and not a defect. ***  */
	dev_wdc_altstatus_access(fake_cpu(), NULL, 0, buf, 1, MEM_WRITE, &d);

	rows ++;
	if (d.atapi_cmd_in_progress != 1 || d.atapi_phase != PHASE_CMDOUT) {
		printf("  FAIL %-38s flag %i phase 0x%x\n",
		    "LIVENESS: altctl keeps packet live",
		    d.atapi_cmd_in_progress, d.atapi_phase);
		failures ++;
	} else {
		printf("  ok   %-38s flag %i\n",
		    "LIVENESS: altctl keeps packet live",
		    d.atapi_cmd_in_progress);
	}

	/*  the CDB the guest was always entitled to send  */
	stub_scsi_cmds = 0;
	for (i = 0; i < 6; i++) {
		buf[0] = 0x12; buf[1] = 0x00;
		buf[2] = 0; buf[3] = 0;
		dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_WRITE, &d);
	}

	rows ++;
	if (stub_scsi_cmds != 1) {
		printf("  FAIL %-38s dispatched %i, want 1\n",
		    "a CDB after altctl still dispatches", stub_scsi_cmds);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a CDB after altctl still dispatches", stub_scsi_cmds);
	}

	stub_datain_len = 0;
	stub_disk_exists = 0;
	if (d.atapi_st != NULL) {
		free(d.atapi_st->data_in);
		free(d.atapi_st->cmd);
		free(d.atapi_st);
	}
	free(d.inbuf);
}


/*  #478's DECLINE-AND-ANNOUNCE, measured by EMISSION COUNT rather than by the latch.
 *
 *  The latch field is a proxy and a weak one: a fix that sets the flag without
 *  printing, or prints without setting it, satisfies a latch check and fails the
 *  property.  `fatal()` is counted instead, so both halves of "N=1 PER DEVICE
 *  INSTANCE" are observable -- the ONE, and the PER INSTANCE.
 *
 *  The third row is the one that matters for the idiom.  `#269` records that a
 *  shared counter across instances is the wrong shape; a `static` latch would pass
 *  rows one and two and fail row three.
 */
static void row_drain_announce(void)
{
	struct wdc_data d, e;
	unsigned char buf[8];
	int first, second, other;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert = arm_sink;
	if (d.inbuf == NULL) {
		printf("  SETUP announce inbuf failed\n");
		return;
	}
	d.write_in_progress = WDCC_WRITE;
	d.write_count  = 1;
	d.write_offset = 0xd000;

	/*  the input where a spurious sector USED to reach the disk image  */
	stub_fatals = 0; stub_drain_msgs = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &d);
	first = stub_drain_msgs;

	/*  the SAME device again: the latch must hold  */
	stub_fatals = 0; stub_drain_msgs = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &d);
	second = stub_drain_msgs;

	/*  a DIFFERENT device: "per instance" means this one still gets told  */
	memset(&e, 0, sizeof(e));
	e.addr_mult  = 1;
	e.io_enabled = 1;
	e.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	e.irq.interrupt_assert = arm_sink;
	if (e.inbuf == NULL) { free(d.inbuf); return; }
	e.write_in_progress = WDCC_WRITE;
	e.write_count  = 1;
	e.write_offset = 0xd000;
	stub_fatals = 0; stub_drain_msgs = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 8, MEM_WRITE, &e);
	other = stub_drain_msgs;

	/*  the bad-len arm ALSO latches once, so the first access emits two
	    messages: #337's width notice and #478's dropped-write notice.  What
	    this row pins is that the count does not GROW on repetition.  */
	rows ++;
	if (first < 1) {
		printf("  FAIL %-38s emitted %i, want >= 1\n",
		    "a dropped write is announced", first);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a dropped write is announced", first);
	}

	rows ++;
	if (second != 0) {
		printf("  FAIL %-38s emitted %i on repeat, want 0\n",
		    "the announce is latched per device", second);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "the announce is latched per device", second);
	}

	rows ++;
	if (other < 1) {
		printf("  FAIL %-38s emitted %i, want >= 1\n",
		    "a second device is still told", other);
		failures ++;
	} else {
		printf("  ok   %-38s %i\n",
		    "a second device is still told", other);
	}

	free(e.inbuf);
	free(d.inbuf);
}


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
	/*  #477 pass 2: cur_command too -- the arm below issues a REAL packet
	    command, so without it a `cur_command` conjunct blocks the arm and
	    reds these rows for the fixture's reason.  */
	d.cur_command = ATAPI_PKT_CMD;
	d.atapi_cmd_in_progress = 1;
	/*  SETUP RE-PIN, and it is INERT on the committed build: the real
	    device sets BOTH flags together when the packet command
	    arrives, so a fixture setting only atapi_cmd_in_progress
	    builds a state the device never produces.  A candidate fix
	    that keys on the PHASE would then fail here for the fixture's
	    reason rather than its own.  */
	d.atapi_phase = PHASE_CMDOUT;
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
	row_null_atapi_st();
	row_cdb_midxfer();
	row_cdb_already12();
	row_midxfer_phases();
	row_pkt_cdb_accept();
	row_cdb_overshoot();
	row_dataout_drain();
	row_pkt_drain();
	row_badlen_then_legal();
	row_partial_sector();
	row_stale_phase_write();
	row_altctl_cdb_accept();
	row_drain_announce();
	row_odd_step();
	row_odd_midwalk();
	row_odd_width();
	row_odd_multichunk();
	row_odd_bytecount();
	row_odd_zerolen();
	row_rearm_zero();
	row_q2_short_last_chunk();
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
	if (rows != 60) {
		printf("  FAIL %-38s rows = %i, want 60\n",
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
