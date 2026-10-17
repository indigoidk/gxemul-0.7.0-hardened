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
	if (strstr(fmt, "refused a sector drain") != NULL)
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
/*  #563 repair (F3): the two dispatch results the stub could not produce.  `stub_res_nodata'
    returns 1 with NO data_in (TEST UNIT READY, START STOP UNIT); `stub_res_dataout' returns 2
    (WRITE(10), MODE SELECT).  Both inert by default; the stub reads them first.  */
static int stub_res_nodata = 0, stub_res_dataout = 0;
static int stub_res_nodata_hits = 0;	/*  #563 REPAIR2: counts the no-data branch actually taken  */
/*  #563 REPAIR3: two more results, each counting its own branch.  `stub_res_reject' returns 0 (a
    rejected command; without it the stub returns 0 anyway, so only the count names the branch).
    `stub_res_zerolen' returns 1 with data_in ALLOCATED and data_in_len 0 -- what the real READ TOC
    does with allocation bytes 7-8 both zero (diskimage_scsicmd.c's READ TOC case allocates at least
    12 bytes, then sets data_in_len = retlen).  Both inert by default.  */
static int stub_res_reject = 0, stub_res_reject_hits = 0;
static int stub_res_zerolen = 0, stub_res_zerolen_hits = 0;
/*  #563 REPAIR3: the twelve bytes the last dispatch copied (scsi_cmd is malloc(12)), so a row can read
    the CDB the ring delivered.  */
static unsigned char stub_last_cmd[12];
/*  #563: a POSITIONAL fill for the rows that compare pushed bytes by position (0, the default,
    keeps the constant 0xc3 body every other row was written against), and STUB_SLACK bytes of
    0xee after: every transfer this stub fabricates; row_rearm_zero's payload and its dirty-ring
    payload; and the bound, long-transfer and repair fixtures.  An edit that reads up to STUB_SLACK
    bytes past data_in_len then reads 0xee instead of faulting, so it cannot take the rows after it
    down with it -- the slack bounds an over-read, it does not make an arbitrary index edit safe.
    q2's payload is EXACT on purpose (an over-read there is a real heap-buffer-overflow under
    ASan), and the small odd, width, zero-length and packet fixtures carry none.  [#563 repair
    (F13): this said "after the payload of each #563 re-arm row" while row_rearm_zero's tail was
    calloc's zeroes and the dirty-ring payload had no slack at all.]  */
#define STUB_SLACK 262144
static int stub_datain_pattern = 0;
static unsigned char stub_pat(size_t i)
{
	uint32_t x = (uint32_t) i * 2654435761u;

	x ^= x >> 15; x *= 0x2c1b3c6du; x ^= x >> 12;
	return (unsigned char) x;
}
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
	if (xferp->cmd != NULL)		/*  #563 REPAIR3: the CDB the dispatch copied  */
		memcpy(stub_last_cmd, xferp->cmd, 12);

	if (stub_res_reject) {		/*  #563 REPAIR3  */
		stub_res_reject_hits ++;
		return 0;
	}
	if (stub_res_zerolen) {		/*  #563 REPAIR3: READ TOC, allocation length 0  */
		stub_res_zerolen_hits ++;
		xferp->data_in = (unsigned char *) malloc(12 + STUB_SLACK);
		if (xferp->data_in == NULL)
			return 0;
		memset(xferp->data_in, 0, 12);
		xferp->data_in[1] = 10;		/*  the TOC header the real case writes  */
		memset(xferp->data_in + 12, 0xee, STUB_SLACK);
		xferp->data_in_len = 0;
		return 1;
	}
	if (stub_res_nodata) {		/*  #563 repair (F3)  */
		stub_res_nodata_hits ++;	/*  REPAIR2: names the branch  */
		return 1;
	}
	if (stub_res_dataout)
		return 2;
	if (stub_datain_len <= 0)
		return 0;

	/*  One DATA-IN transfer, marked so the caller can tell WHICH bytes
	    survived: byte 0 alone carries 0x5a, everything else 0xc3 -- or stub_pat(i)
	    while stub_datain_pattern is set (#563).  A ring
	    overrun wraps block 514 onto block 0, so the first byte popped
	    becomes 0xc3 and the marker is destroyed.  */
	xferp->data_in = (unsigned char *) malloc(stub_datain_len + STUB_SLACK);
	if (xferp->data_in == NULL)
		return 0;
	for (i = 0; i < (size_t) stub_datain_len; i++)
		xferp->data_in[i] = stub_datain_pattern ? stub_pat(i) : 0xc3;
	memset(xferp->data_in + stub_datain_len, 0xee, STUB_SLACK);
	xferp->data_in[0] = 0x5a;
	xferp->data_in_len = stub_datain_len;
	return 1;
}

static int stub_disk_exists = 0;

/*  #484: a READ FILL for the bulk-refill rows.  R7/R8 have to tell DISK bytes
    from RING bytes -- the defect is disk contents landing on unread guest data
    -- and a stub that returns an untouched buffer cannot show that.  0 keeps it
    inert, so every pre-existing row is unaffected.  */
static int stub_read_fill = 0;	/*  inert by default  */

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
	if (!writeflag && stub_read_fill && buf != NULL)
		memset(buf, stub_read_fill, len);
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

/*  *** EVERY ROW IN THIS FILE TESTED ONE ENDIANNESS ARM UNTIL 2026-08-27.
 *
 *  `stub_cpu` is memset to zero and nothing ever set `byte_order`, while the
 *  device branches on `cpu->byte_order == EMUL_LITTLE_ENDIAN`.  So the BIG-endian
 *  arm ran for every row -- and for every kill table measured against them.
 *
 *  A seat proved it the only way that settles it: deleting `badlen_this = 1;`
 *  from the LITTLE-endian default alone produced a detector run BYTE-IDENTICAL
 *  to the unmutated one, same md5.  Not one row could tell them apart.
 *
 *  The sting is that the rung-3 witness machine for this defect family,
 *  `evbmips -e malta`, is LITTLE-endian.  The detector was testing the opposite
 *  arm from the machine the defect was witnessed on.
 *
 *  THE DEFAULT IS DELIBERATELY UNCHANGED.  Flipping it would silently re-point
 *  every existing row at the other arm, and any row that then failed would be
 *  indistinguishable from a real defect.  New rows opt IN by setting this.
 */
static int stub_byte_order = 0;	/*  0 = the arm this file always ran  */

static struct cpu *fake_cpu(void)
{
	static int done = 0;
	if (!done) {
		memset(&stub_machine, 0, sizeof(stub_machine));
		memset(&stub_cpu, 0, sizeof(stub_cpu));
		stub_cpu.machine = &stub_machine;
		done = 1;
	}
	stub_cpu.byte_order = stub_byte_order;
	return &stub_cpu;
}

/*  adj_20261016 Fable 5.1 scratch harness for F4 / question 2:
    does D2_and_st (`if (flag && atapi_st != NULL)` at the read-arm) differ from HEAD
    on a GUEST channel (INTRQ) in the (flag 1, atapi_st NULL, phase CMDOUT) cell,
    with the ring driven to occupancy 514 through real data-port stores that step
    PAST the 12-byte dispatch point without landing on it?  Drives the real handler;
    nothing here pokes transfer state the writers do not produce.  */
int quiet_mode = 0;

static int g_sink = 0;
static void f4_assert(struct interrupt *a)   { (void)a; g_sink++; }
static void f4_deassert(struct interrupt *a) { (void)a; }

static void push(struct wdc_data *d, int w)
{
	unsigned char buf[8];
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, w, MEM_WRITE, d);
}

int main(void)
{
	struct wdc_data d;
	unsigned char buf[8];
	int occ, i;

	setvbuf(stdout, NULL, _IONBF, 0);
	stub_byte_order = EMUL_LITTLE_ENDIAN;

	memset(&d, 0, sizeof(d));
	d.addr_mult  = 1;
	d.io_enabled = 1;
	d.inbuf = (unsigned char *) calloc(1, WDC_INBUF_SIZE);
	d.irq.interrupt_assert   = f4_assert;
	d.irq.interrupt_deassert = f4_deassert;

	/*  Enter CMDOUT exactly as ATAPI_PKT_CMD leaves it: the reset has flushed the
	    ring (head=tail=0), the flag and phase are set, atapi_st is still NULL,
	    atapi_len is 0.  */
	d.cur_command           = ATAPI_PKT_CMD;
	d.atapi_cmd_in_progress = 1;
	d.atapi_phase           = PHASE_CMDOUT;
	d.atapi_st              = NULL;
	d.atapi_len             = 0;
	d.atapi_received        = 0;

	/*  Step occupancy 0 -> 2 -> 6 -> 10 -> 14 (skips 12), then 2-byte stores to 514.
	    Every store runs the dispatch guard `inbuf_len == 12'; none lands on 12.  */
	push(&d, 2);			/*  occ 2   */
	push(&d, 4);			/*  occ 6   */
	push(&d, 4);			/*  occ 10  */
	push(&d, 4);			/*  occ 14  -- passed 12 without touching it  */
	for (i = 14; i < 514; i += 2)	/*  occ 16,18,...,514  */
		push(&d, 2);

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0) occ += WDC_INBUF_SIZE;

	printf("STATE occ=%d phase=0x%x st=%s atapi_len=%d dispatched=%s\n",
	    occ, d.atapi_phase, d.atapi_st ? "NON-NULL" : "NULL",
	    d.atapi_len, d.atapi_st ? "YES" : "no");

	/*  The measured read: one width-2 DATA read.  Pops 2 (occ 514 -> 512), then the
	    arm.  Clear int_assert and the sink so only THIS read is observed.  */
	d.int_assert = 0;
	g_sink = 0;
	memset(buf, 0, sizeof(buf));
	dev_wdc_access(fake_cpu(), NULL, wd_data, buf, 2, MEM_READ, &d);

	occ = d.inbuf_head - d.inbuf_tail;
	while (occ < 0) occ += WDC_INBUF_SIZE;

	printf("READ  int_assert=%d sink=%d warned_null_xfer=%d occ_after=%d\n",
	    d.int_assert, g_sink, d.warned_null_xfer, occ);
	return 0;
}
