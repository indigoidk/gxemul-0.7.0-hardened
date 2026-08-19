/*
 *  r411 part C1, measure seat: offline differential of the REAL disk-image
 *  DATA PATH -- diskimage__internal_access(), fwrite_helper/fread_helper, and
 *  the SCSI READ / WRITE / READ CAPACITY handlers.
 *
 *  CONSTRUCTION, same as regress/diff_wdc_identify.c and regress/diff_sh4_tmu.c:
 *  this driver stubs the externals and #includes the shipping diskimage.c and
 *  diskimage_scsicmd.c, so the code that runs IS the code that ships. Deleting
 *  the include does not weaken the test, it fails to compile.
 *
 *  *** THE ROWS ASSERT RETURN VALUES AND GUEST-VISIBLE STATUS, NOT BUFFER
 *  CONTENTS. A row that only inspects the buffer passes on zero-fill, which is
 *  the very failure under test. ***
 *
 *  THE WRITE FAILURE IS INJECTED WITH RLIMIT_FSIZE, not with a read-only FILE*.
 *  A read-only stream would prove only that fwrite can fail; the file-size
 *  rlimit reproduces the real shape of ENOSPC/EDQUOT/EFBIG through the real
 *  filesystem, and it produces BOTH cases separately: a write that lands
 *  partially (short count) and a write that lands not at all (zero count).
 *  Those two are NOT the same defect -- see the #if 0 block, which tests
 *  `lendone <= 0` and therefore would not catch the partial one even if it
 *  were re-enabled.
 *
 *  Rows marked [CONTROL] pass on the shipping code. Rows marked [PROOF] fail on
 *  the shipping code and are the existence proof. A build failure or a signal
 *  is a FAULT, never a detection, and is scored separately.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <unistd.h>
#include <fcntl.h>
#include <signal.h>
#include <errno.h>
#include <sys/stat.h>
#include <sys/resource.h>

static int quiet_stubs = 1;

void fatal(const char *fmt, ...)
{
	va_list ap;
	if (quiet_stubs) return;
	va_start(ap, fmt); vfprintf(stderr, fmt, ap); va_end(ap);
}

void debug(const char *fmt, ...)
{
	va_list ap;
	if (quiet_stubs) return;
	va_start(ap, fmt); vfprintf(stderr, fmt, ap); va_end(ap);
}

#include "../src/disk/diskimage.c"

/*  AFTER the include: `struct cpu` is not a known type until the tree's own
    headers have been pulled in, and defining this first produces "conflicting
    types" against the very prototype it is meant to satisfy. Same trap
    regress/diff_wdc_identify.c records for its diskimage_* stubs.  */
void debugmsg_cpu(struct cpu* cpu, int subsystem, const char *name,
	int verbosity_required, const char *fmt, ...)
{
	va_list ap;
	if (quiet_stubs) return;
	va_start(ap, fmt); vfprintf(stderr, fmt, ap); va_end(ap);
	fprintf(stderr, "\n");
}

void debugmsg(int subsystem, const char *name, int verbosity_required,
	const char *fmt, ...)
{
	va_list ap;
	if (quiet_stubs) return;
	va_start(ap, fmt); vfprintf(stderr, fmt, ap); va_end(ap);
	fprintf(stderr, "\n");
}

/*  Both files define a file-static copy of this table; renaming the second is
    the only edit needed to put both translation units together.  */
#define diskimage_types diskimage_types_scsi
#include "../src/disk/diskimage_scsicmd.c"
#undef diskimage_types


/*  ------------------------------------------------------------------  */

static int failures = 0, rows = 0, faults = 0;

static void check(const char *rowname, long long got, long long want)
{
	rows ++;
	if (got == want) {
		printf("  ok    %-58s = %lld\n", rowname, got);
	} else {
		failures ++;
		printf("  FAIL  %-58s = %lld, want %lld\n", rowname, got, want);
	}
}

static const char *WORK = "/tmp/r411c1/work";

static void mkfile(const char *path, long long len, unsigned char fill)
{
	FILE *f = fopen(path, "w+");
	long long i;
	if (f == NULL) { perror(path); exit(1); }
	for (i = 0; i < len; i++)
		fputc(fill, f);
	fclose(f);
}

static long long fsize(const char *path)
{
	struct stat st;
	if (stat(path, &st) != 0) return -1;
	return (long long) st.st_size;
}

/*  A struct diskimage wired to a plain flat file, nothing else.  */
static void mkdisk(struct diskimage *d, const char *path, const char *mode,
	int writable)
{
	memset(d, 0, sizeof(*d));
	d->type = DISKIMAGE_SCSI;
	d->id = 0;
	d->fname = (char *) path;
	d->f = fopen(path, mode);
	if (d->f == NULL) { perror(path); exit(1); }
	d->writable = writable;
	d->logical_block_size = 512;
	d->nr_of_overlays = 0;
	d->nr_of_tracks = 0;
	d->is_a_cdrom = 0;
	d->is_a_tape = 0;
	diskimage_recalc_size(d);
}


/*  ------------------------------------------------------------------  */
/*  SECTION 1: does a failed write reach the caller?                     */

static void section_write_return(void)
{
	char path[256];
	struct diskimage d;
	unsigned char buf[4096];
	struct rlimit old, lim;
	int res;
	long long before, after;

	printf("\nSECTION 1 -- diskimage__internal_access(), write path\n");

	snprintf(path, sizeof(path), "%s/w1.img", WORK);
	mkfile(path, 8192, 0x11);

	/*  [CONTROL] a well-formed write really does land.  */
	mkdisk(&d, path, "r+", 1);
	memset(buf, 0xAA, 512);
	res = diskimage__internal_access(&d, 1, 0, buf, 512);
	check("[CONTROL] ordinary write returns success", res, 1);
	fflush(d.f);
	{
		unsigned char v[512];
		memset(v, 0, sizeof(v));
		diskimage__internal_access(&d, 0, 0, v, 512);
		check("[CONTROL] ordinary write actually landed", v[0] == 0xAA, 1);
	}
	fclose(d.f);

	/*  [CONTROL] a write to a non-writable disk is refused. This is the
	    return-0 path at diskimage.c:1374-1375, and it proves the row can
	    see a 0 at all -- without it, "always returns 1" would be untested
	    machinery rather than a measurement.  */
	mkdisk(&d, path, "r", 0);
	res = diskimage__internal_access(&d, 1, 0, buf, 512);
	check("[CONTROL] write to non-writable disk returns failure", res, 0);
	fclose(d.f);

	/*  Now inject a backing store that cannot absorb the write.  */
	signal(SIGXFSZ, SIG_IGN);
	getrlimit(RLIMIT_FSIZE, &old);

	/*
	 *  --- case A: the write lands PARTIALLY (short count) ---
	 *
	 *  *** #417: THE OFFSET MOVED FROM 8192 TO 4096, AND THAT IS THE WHOLE
	 *  POINT OF THIS EDIT.
	 *
	 *  #416 added a capacity bound to diskimage__internal_access().  These
	 *  two rows wrote at offset 8192 on an 8192-byte file -- exactly AT the
	 *  backed extent -- so the BOUND refused them before fwrite() was ever
	 *  called.  They kept passing and stopped testing anything: measured,
	 *  deleting #416's entire short-write check left all 31 rows green, and
	 *  the evidence line these rows print changed from "errno 27" to
	 *  "errno 0" without anyone noticing.
	 *
	 *  Call the pattern COLLATERAL VACUITY: adding an EARLIER rejection
	 *  silently disarms every row that depended on reaching a LATER
	 *  failure.  Nothing turns red, no assertion changes, the coverage just
	 *  evaporates.  The same commit that added the bound was the one whose
	 *  CHANGELOG described this exact shape happening to a rejected design.
	 *
	 *  The write now lands at 4096..5120, comfortably INSIDE the 8192-byte
	 *  extent, and RLIMIT_FSIZE is lowered to 4352 so the filesystem -- not
	 *  the bound -- is what truncates it, absorbing 256 of the 1024 bytes.
	 *  ***
	 */
	snprintf(path, sizeof(path), "%s/w2.img", WORK);
	mkfile(path, 8192, 0x22);
	lim = old; lim.rlim_cur = 4096 + 256;
	if (setrlimit(RLIMIT_FSIZE, &lim) != 0) { perror("setrlimit"); faults++; return; }

	mkdisk(&d, path, "r+", 1);
	setvbuf(d.f, NULL, _IONBF, 0);
	memset(buf, 0xBB, 1024);
	before = fsize(path);
	errno = 0;
	res = diskimage__internal_access(&d, 1, 4096, buf, 1024);
	after = fsize(path);
	printf("        (evidence: file %lld -> %lld bytes of the 1024 asked, errno %d)\n",
	    before, after, errno);
	check("[PROOF] short write (256 of 1024 absorbed) returns failure", res, 0);
	fclose(d.f);

	/*  --- case B: the write lands NOT AT ALL (zero count) ---
	    #417: same relocation as case A, and for the same reason -- the
	    rlimit is set exactly at the write's start offset, so nothing can be
	    absorbed, while the write itself is well inside the backed extent
	    and therefore reaches fwrite() rather than being refused early.  */
	/*  ORDER MATTERS AND IT BIT ME: mkfile() FIRST, rlimit SECOND.  With the
	    rlimit lowered first, mkfile()'s own writes are truncated too, the
	    image ends up 4096 bytes instead of 8192, and the write at 4096 sits
	    at the extent again -- the very masquerade this edit removes,
	    reintroduced by a different route.  The evidence line caught it:
	    "file 4096 -> 4096 ... errno 0".  */
	snprintf(path, sizeof(path), "%s/w3.img", WORK);
	/*  RESTORE the rlimit before creating the fixture: case A left it at
	    4352, which truncated this mkfile() to 4352 bytes and put the write
	    back at the extent -- the same masquerade a third time, now caused
	    by a LEFTOVER limit rather than an early one.  The evidence line is
	    what exposed each round of this: "file 4352 -> 4352 ... errno 0".  */
	setrlimit(RLIMIT_FSIZE, &old);
	mkfile(path, 8192, 0x33);
	lim = old; lim.rlim_cur = 4096;
	setrlimit(RLIMIT_FSIZE, &lim);
	mkdisk(&d, path, "r+", 1);
	setvbuf(d.f, NULL, _IONBF, 0);
	memset(buf, 0xCC, 1024);
	before = fsize(path);
	errno = 0;
	res = diskimage__internal_access(&d, 1, 4096, buf, 1024);
	after = fsize(path);
	printf("        (evidence: file %lld -> %lld bytes of the 1024 asked, errno %d)\n",
	    before, after, errno);
	check("[PROOF] write that lands 0 of 1024 bytes returns failure", res, 0);
	fclose(d.f);

	setrlimit(RLIMIT_FSIZE, &old);
}


/*  ------------------------------------------------------------------  */
/*  SECTION 2: does a read past end-of-file reach the caller?            */

static void section_read_eof(void)
{
	char path[256];
	struct diskimage d;
	unsigned char buf[4096];
	int res, allzero, i;

	printf("\nSECTION 2 -- diskimage__internal_access(), read path\n");

	snprintf(path, sizeof(path), "%s/r1.img", WORK);
	mkfile(path, 8192, 0x5A);
	mkdisk(&d, path, "r+", 1);

	/*  [CONTROL] an in-range read works and returns the real bytes.  */
	memset(buf, 0, sizeof(buf));
	res = diskimage__internal_access(&d, 0, 0, buf, 512);
	check("[CONTROL] in-range read returns success", res, 1);
	check("[CONTROL] in-range read returns the real bytes", buf[0] == 0x5A, 1);

	/*  A read that begins entirely past EOF.  */
	memset(buf, 0xEE, sizeof(buf));
	res = diskimage__internal_access(&d, 0, 1024*1024, buf, 512);
	allzero = 1;
	for (i = 0; i < 512; i++) if (buf[i] != 0) allzero = 0;
	printf("        (evidence: buffer after the past-EOF read is %s)\n",
	    allzero ? "ALL ZERO -- the guest cannot tell" : "not zero-filled");
	check("[PROOF] read starting past EOF returns failure", res, 0);

	/*
	 *  #416: THIS ROW ALREADY EXISTED AS A COMPUTATION AND WAS ONLY
	 *  PRINTED.  `allzero` was measured above and reported to the reader,
	 *  while the only ASSERTION was the return value -- so inverting the
	 *  bound's read-side zero-fill (`if (!writeflag)` -> `if (writeflag)`,
	 *  one character) passed the whole suite while handing the guest
	 *  uninitialised host memory.  A row that computes evidence and does
	 *  not assert it is the same class of defect as a check that cannot
	 *  fail.
	 *
	 *  It matters specifically because dev_wdc's read path declares a
	 *  32 KB buffer ON THE STACK, discards this function's return value,
	 *  and copies the whole buffer to the guest; the SCSI path cannot
	 *  observe it (diskimage_scsicmd.c memsets on !result), so the IDE
	 *  path is the one that leaks and only a direct call like this one
	 *  can see it.
	 */
	check("[PROOF] a refused read leaves NO caller bytes unwritten",
	    allzero, 1);

	fclose(d.f);
}


/*  ------------------------------------------------------------------  */
/*  SECTION 3: the SCSI handlers, driven through the real entry point.   */

static struct machine *mkmachine(struct diskimage *d)
{
	struct machine *m = calloc(1, sizeof(struct machine));
	if (m == NULL) { perror("calloc"); exit(1); }
	m->first_diskimage = d;
	return m;
}

static struct cpu *mkcpu(struct machine *m)
{
	struct cpu *c = calloc(1, sizeof(struct cpu));
	if (c == NULL) { perror("calloc"); exit(1); }
	c->machine = m;
	return c;
}

/*  Build a READ(10) / WRITE(10) CDB.  */
static void cdb10(unsigned char *cmd, int op, uint32_t lba, uint16_t nblocks)
{
	memset(cmd, 0, 10);
	cmd[0] = op;
	cmd[2] = (lba >> 24) & 255; cmd[3] = (lba >> 16) & 255;
	cmd[4] = (lba >>  8) & 255; cmd[5] = lba & 255;
	cmd[7] = (nblocks >> 8) & 255; cmd[8] = nblocks & 255;
}

/*
 *  status/msg_in/data_in MUST start NULL. scsi_transfer_allocbuf() free()s any
 *  non-NULL old pointer (diskimage_scsicmd.c:100-107), so handing it a stack
 *  array aborts the process -- which is a FAULT, not a detection. Found the
 *  hard way; recorded so the next harness does not repeat it.
 */
static void xfer_init(struct scsi_transfer *x, unsigned char *cmd, size_t cmdlen)
{
	memset(x, 0, sizeof(*x));
	x->cmd = cmd;
	x->cmd_len = cmdlen;
}

static void xfer_free(struct scsi_transfer *x)
{
	free(x->data_in);  x->data_in = NULL;
	free(x->status);   x->status = NULL;
	free(x->msg_in);   x->msg_in = NULL;
}

static int xfer_status(struct scsi_transfer *x)
{
	return x->status == NULL ? -1 : x->status[0];
}

static void section_scsi_lba(void)
{
	char path[256];
	struct diskimage d;
	struct machine *m;
	struct cpu *c;
	struct scsi_transfer xfer;
	unsigned char cmd[16], data_out[4096];
	int r;
	long long before, after;
	long long blocks_before, blocks_after;

	printf("\nSECTION 3 -- SCSI READ / WRITE past the reported capacity\n");

	snprintf(path, sizeof(path), "%s/s1.img", WORK);
	mkfile(path, 10*1024, 0x77);		/*  20 blocks of 512  */
	mkdisk(&d, path, "r+", 1);
	m = mkmachine(&d);
	c = mkcpu(m);

	printf("        (disk is %lld bytes; recalc says %lld blocks of %d)\n",
	    fsize(path), (long long)d.nr_of_logical_blocks, d.logical_block_size);

	/*  [CONTROL] an in-range READ(10) succeeds with GOOD status.  */
	cdb10(cmd, SCSICMD_READ_10, 0, 1);
	xfer_init(&xfer, cmd, 10);
	r = diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
	check("[CONTROL] in-range SCSI READ(10) is accepted", r, 1);
	check("[CONTROL] in-range SCSI READ(10) status is GOOD", xfer_status(&xfer), 0);
	check("[CONTROL] in-range SCSI READ(10) returns the real bytes",
	    xfer.data_in[0] == 0x77, 1);
	xfer_free(&xfer);

	/*  A READ(10) at an LBA far beyond the last block of the image.  */
	cdb10(cmd, SCSICMD_READ_10, 1000000, 1);	/*  LBA 1e6, disk has 20  */
	xfer_init(&xfer, cmd, 10);
	r = diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
	printf("        (evidence: handler returned %d, status 0x%02x, %zu bytes of"
	    " data_in, first byte 0x%02x)\n", r, xfer_status(&xfer),
	    xfer.data_in_len, xfer.data_in[0]);
	check("[PROOF] SCSI READ(10) past capacity sets CHECK CONDITION",
	    xfer_status(&xfer), 0x02);
	xfer_free(&xfer);

	/*  A WRITE(10) at an LBA far beyond the end of the image.  */
	before = fsize(path);
	blocks_before = d.nr_of_logical_blocks;
	memset(data_out, 0x99, sizeof(data_out));
	cdb10(cmd, SCSICMD_WRITE_10, 1000000, 1);
	xfer_init(&xfer, cmd, 10);
	xfer.data_out = data_out;
	xfer.data_out_len = 512;
	xfer.data_out_offset = 512;
	r = diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
	fflush(d.f);
	after = fsize(path);
	diskimage_recalc_size(&d);
	blocks_after = d.nr_of_logical_blocks;
	printf("        (evidence: image %lld -> %lld bytes; capacity %lld -> %lld"
	    " blocks; handler returned %d, status 0x%02x)\n", before, after,
	    blocks_before, blocks_after, r, xfer_status(&xfer));
	check("[PROOF] SCSI WRITE(10) past capacity does not grow the image",
	    after, before);
	check("[PROOF] SCSI WRITE(10) past capacity does not change the capacity",
	    blocks_after, blocks_before);
	check("[PROOF] SCSI WRITE(10) past capacity sets CHECK CONDITION",
	    xfer_status(&xfer), 0x02);
	xfer.data_out = NULL;
	xfer_free(&xfer);

	fclose(d.f);
	free(c); free(m);
}


/*  A SCSI WRITE whose backing store cannot absorb it: is the guest told?  */
static void section_scsi_write_fail(void)
{
	char path[256];
	struct diskimage d;
	struct machine *m;
	struct cpu *c;
	struct scsi_transfer xfer;
	unsigned char cmd[16], data_out[4096];
	struct rlimit old, lim;
	long long before, after;

	printf("\nSECTION 3b -- SCSI WRITE onto a backing store that is full\n");

	signal(SIGXFSZ, SIG_IGN);
	getrlimit(RLIMIT_FSIZE, &old);

	snprintf(path, sizeof(path), "%s/s2.img", WORK);
	mkfile(path, 10*1024, 0x77);
	lim = old; lim.rlim_cur = 10*1024;
	setrlimit(RLIMIT_FSIZE, &lim);

	mkdisk(&d, path, "r+", 1);
	setvbuf(d.f, NULL, _IONBF, 0);
	m = mkmachine(&d);
	c = mkcpu(m);

	/*  Block 19 is the LAST block that exists; writing block 19 is in
	    range, but the rlimit refuses to let the file be rewritten past
	    its current size... so aim at block 20, one past the end, which is
	    both past capacity AND past what the store will absorb.  */
	before = fsize(path);
	memset(data_out, 0x44, sizeof(data_out));
	cdb10(cmd, SCSICMD_WRITE_10, 20, 1);
	xfer_init(&xfer, cmd, 10);
	xfer.data_out = data_out;
	xfer.data_out_len = 512;
	xfer.data_out_offset = 512;
	errno = 0;
	diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
	fflush(d.f);
	after = fsize(path);
	printf("        (evidence: image %lld -> %lld bytes, errno %d, status 0x%02x)\n",
	    before, after, errno, xfer_status(&xfer));
	check("[PROOF] SCSI WRITE onto a full store sets CHECK CONDITION",
	    xfer_status(&xfer), 0x02);
	xfer.data_out = NULL;
	xfer_free(&xfer);

	setrlimit(RLIMIT_FSIZE, &old);
	fclose(d.f);
	free(c); free(m);
}


/*  ------------------------------------------------------------------  */
/*  SECTION 4: READ CAPACITY on a disk with zero blocks.                 */

static void section_read_capacity(void)
{
	char path[256];
	struct diskimage d;
	struct machine *m;
	struct cpu *c;
	struct scsi_transfer xfer;
	unsigned char cmd[16];
	uint32_t announced;

	printf("\nSECTION 4 -- READ CAPACITY when the disk has zero blocks\n");

	/*  [CONTROL] a normal disk announces (blocks - 1), the SCSI convention
	    of "address of the LAST block".  */
	snprintf(path, sizeof(path), "%s/c1.img", WORK);
	mkfile(path, 10*1024, 0x11);
	mkdisk(&d, path, "r+", 1);
	m = mkmachine(&d); c = mkcpu(m);

	memset(cmd, 0, sizeof(cmd));
	cmd[0] = SCSIBLOCKCMD_READ_CAPACITY;
	xfer_init(&xfer, cmd, 10);
	diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
	announced = (xfer.data_in[0] << 24) | (xfer.data_in[1] << 16) |
	    (xfer.data_in[2] << 8) | xfer.data_in[3];
	printf("        (evidence: %lld blocks -> announces last-block %u)\n",
	    (long long)d.nr_of_logical_blocks, announced);
	check("[CONTROL] normal disk announces blocks-1",
	    announced, d.nr_of_logical_blocks - 1);
	xfer_free(&xfer);
	fclose(d.f); free(c); free(m);

	/*  A disk with ZERO blocks. A zero-length image is used because it
	    reaches nr_of_logical_blocks == 0 without depending on the geometry
	    defect at all -- the arithmetic under test is isolated, and the row
	    stays valid after that defect is fixed.  */
	snprintf(path, sizeof(path), "%s/c2.img", WORK);
	mkfile(path, 0, 0);
	mkdisk(&d, path, "r+", 1);
	m = mkmachine(&d); c = mkcpu(m);

	memset(cmd, 0, sizeof(cmd));
	cmd[0] = SCSIBLOCKCMD_READ_CAPACITY;
	xfer_init(&xfer, cmd, 10);
	diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
	announced = (xfer.data_in[0] << 24) | (xfer.data_in[1] << 16) |
	    (xfer.data_in[2] << 8) | xfer.data_in[3];
	printf("        (evidence: %lld blocks -> announces last-block 0x%08x"
	    " = %.0f GB at %d bytes/block)\n", (long long)d.nr_of_logical_blocks,
	    announced, ((double)announced + 1) * d.logical_block_size / 1073741824.0,
	    d.logical_block_size);
	check("[PROOF] zero-block disk does not announce 0xffffffff",
	    announced != 0xffffffffu, 1);
	xfer_free(&xfer);
	fclose(d.f); free(c); free(m);
}


/*  ------------------------------------------------------------------  */
/*
 *  SECTION 5: THE SAFETY QUESTION FOR THE OBVIOUS FIX.
 *
 *  The image is rounded UP to a whole number of cylinders, so the capacity the
 *  disk ADVERTISES is larger than the backing file for any image that is not
 *  already a whole cylinder. Every block in that gap is inside the advertised
 *  capacity, is past end-of-file, and reads as zeroes today.
 *
 *  That is what makes re-enabling the `lendone <= 0` check a behaviour change
 *  rather than a pure bug fix: those reads would start returning failure, and a
 *  capacity comparison would NOT stop them, because they are IN range.
 *
 *  This section only measures the size of the exposure. It does not evaluate
 *  diskimage_recalc_size(), which is another seat's scope; the round-up is
 *  consumed here as a black box.
 */
static void section_roundup_gap(void)
{
	char path[256];
	struct diskimage d;
	unsigned char buf[512];
	int res;
	long long filebytes, advertised, lastblock;

	printf("\nSECTION 5 -- the gap between advertised capacity and the file\n");

	snprintf(path, sizeof(path), "%s/g1.img", WORK);
	mkfile(path, 10*1024, 0x77);
	mkdisk(&d, path, "r+", 1);

	filebytes  = fsize(path);
	advertised = (long long)d.nr_of_logical_blocks * d.logical_block_size;
	lastblock  = d.nr_of_logical_blocks - 1;
	printf("        (evidence: file %lld bytes, advertised %lld bytes"
	    " (%lld blocks) -- %lld bytes of the advertised disk do not exist)\n",
	    filebytes, advertised, (long long)d.nr_of_logical_blocks,
	    advertised - filebytes);

	/*  A read of the LAST block the disk claims to have.  */
	memset(buf, 0xEE, sizeof(buf));
	res = diskimage__internal_access(&d, 0, lastblock * 512, buf, 512);
	printf("        (evidence: reading block %lld -- the last one READ CAPACITY"
	    " advertises -- returns %d, buffer[0]=0x%02x)\n", lastblock, res, buf[0]);
	check("[CONTROL, and it is the warning] in-capacity read past EOF succeeds today",
	    res, 1);

	fclose(d.f);
}


/*  ------------------------------------------------------------------  */
/*
 *  SECTION 6: how big is that gap on the images this project actually boots?
 *
 *  Opened READ-ONLY. This is a measurement of the real rigs, not a test, so it
 *  prints rather than asserts -- the numbers decide whether the M1 regression
 *  risk is theoretical or routine.
 */
/*  ------------------------------------------------------------------  */
/*  SECTION G (#416): the BOUNDARY, and the gap between backed and        */
/*  advertised.  Every past-capacity row elsewhere in this file aims at   */
/*  LBA 1,000,000 on a 1,008-block disk -- a point so far outside that    */
/*  three separate mutants survived the whole suite:                      */
/*                                                                        */
/*    * a bound one block too permissive;                                 */
/*    * a bound that checks only the START offset, so a transfer may      */
/*      begin legally and run off the end;                                */
/*    * a write bounded by ADVERTISED capacity rather than the backed     */
/*      extent, which lets the host file grow into the round-up gap.      */
/*                                                                        */
/*  A far-outside row cannot distinguish any of them.  PROBE THE          */
/*  BOUNDARY, NOT A POINT FAR INSIDE IT.                                  */
/*                                                                        */
/*  The fixture is deliberately split: 1000 blocks BACKED by file, 1008   */
/*  ADVERTISED, so LBA 1000..1007 is the whole-cylinder round-up gap that */
/*  every rig image also has (480..992 blocks there).                     */

static void section_boundary(void)
{
	char path[256];
	struct diskimage d;
	unsigned char buf[1024];
	int res;
	long long before;

	printf("\nSECTION G -- the boundary, and the backed/advertised gap\n");

	snprintf(path, sizeof(path), "%s/g1.img", WORK);
	mkfile(path, 512000, 0x33);		/*  1000 blocks BACKED  */
	mkdisk(&d, path, "r+", 1);
	d.total_size = 512000;
	d.nr_of_logical_blocks = 1008;		/*  1008 ADVERTISED  */

	/*  CONTROLS first: the last BACKED block must still work both ways.
	    NOTE this says BACKED, not ADVERTISED -- an earlier draft of this
	    row asserted the last ADVERTISED block was writable, which encodes
	    the superseded symmetric design and would fail here for the right
	    reason.  */
	memset(buf, 0x77, sizeof(buf));
	res = diskimage__internal_access(&d, 1, 999 * 512, buf, 512);
	check("[CONTROL] WRITE of the last BACKED block is accepted", res, 1);
	res = diskimage__internal_access(&d, 0, 999 * 512, buf, 512);
	check("[CONTROL] READ of the last BACKED block is accepted", res, 1);

	/*  A read INSIDE the advertised gap must still succeed as zero-fill.
	    This is what all five rig images rely on and what a total_size
	    read bound was measured to break.  */
	memset(buf, 0xEE, sizeof(buf));
	res = diskimage__internal_access(&d, 0, 1000 * 512, buf, 512);
	check("[CONTROL] READ inside the advertised gap still succeeds", res, 1);
	check("[CONTROL] ... and is zero-filled", buf[0] == 0 && buf[511] == 0, 1);
	res = diskimage__internal_access(&d, 0, 1007 * 512, buf, 512);
	check("[CONTROL] READ of the last ADVERTISED block succeeds", res, 1);

	/*  THE GAP WRITE.  This is the row that distinguishes a bound against
	    the backed extent from one against advertised capacity: the block
	    is inside what READ CAPACITY reports, but past the end of the
	    file, so permitting it grows the host image.  */
	before = fsize(path);
	memset(buf, 0x99, sizeof(buf));
	res = diskimage__internal_access(&d, 1, 1000 * 512, buf, 512);
	check("[PROOF] WRITE into the advertised gap is refused", res, 0);
	check("[PROOF] ... and the host file did not grow",
	    fsize(path), before);

	/*  ONE BLOCK past advertised -- the off-by-one a far-outside row
	    cannot see.  */
	res = diskimage__internal_access(&d, 1, 1008 * 512, buf, 512);
	check("[PROOF] WRITE one block past ADVERTISED is refused", res, 0);
	res = diskimage__internal_access(&d, 0, 1008 * 512, buf, 512);
	check("[PROOF] READ one block past ADVERTISED is refused", res, 0);

	/*  STARTS LEGAL, RUNS OFF THE END.  A bound that only checks the
	    start offset accepts this and writes past the extent.  */
	before = fsize(path);
	res = diskimage__internal_access(&d, 1, 999 * 512, buf, 1024);
	check("[PROOF] WRITE starting in range but running off the end is"
	    " refused", res, 0);
	check("[PROOF] ... and that one did not grow the file either",
	    fsize(path), before);

	fclose(d.f);
}


/*  ------------------------------------------------------------------  */
/*  SECTION H (#417): the four regions a pass-2 mutation sweep found       */
/*  UNREACHED after #416 shipped.  Each closed a MEASURED survivor.        */

static void section_pass2_gaps(void)
{
	char path[256];
	struct diskimage d;
	struct machine *m;
	struct cpu *c;
	struct scsi_transfer xfer;
	unsigned char cmd[16];
	unsigned char buf[1024];
	int res;
	long long before;

	printf("\nSECTION H -- regions a pass-2 mutation sweep found unreached\n");

	/*
	 *  H1. AN UNALIGNED BACKED EXTENT.
	 *
	 *  Every other fixture here is a whole number of 512-byte blocks, so
	 *  `d->total_size` -> `d->total_size + 1` was MEASURED to survive the
	 *  entire suite: the one byte of slack is only reachable when
	 *  total_size % 512 != 0.  It falsifies the round's headline property
	 *  -- "a guest can never grow the host file by even one byte" --
	 *  literally by one byte.
	 */
	snprintf(path, sizeof(path), "%s/h1.img", WORK);
	mkfile(path, 10240 - 1, 0x44);		/*  total_size % 512 == 511  */
	mkdisk(&d, path, "r+", 1);
	before = fsize(path);
	memset(buf, 0x55, sizeof(buf));
	res = diskimage__internal_access(&d, 1, 19 * 512, buf, 512);
	check("[PROOF] WRITE ending 1 byte past an UNALIGNED extent is refused",
	    res, 0);
	check("[PROOF] ... and the host file did not grow by even one byte",
	    fsize(path), before);
	fclose(d.f);

	/*
	 *  H2. A NEGATIVE OFFSET.
	 *
	 *  Dropping `offset < 0` from the bound survived every other row.  It
	 *  is reachable: diskimage_access()'s own negative guard only fires
	 *  when override_base_offset != 0, and #204 records a guest seeking a
	 *  flat CD/ISO handle to 0xffffffff.
	 */
	snprintf(path, sizeof(path), "%s/h2.img", WORK);
	mkfile(path, 10240, 0x66);
	mkdisk(&d, path, "r+", 1);
	memset(buf, 0xEE, sizeof(buf));
	res = diskimage__internal_access(&d, 0, -4096, buf, 512);
	check("[PROOF] READ at a NEGATIVE offset is refused", res, 0);
	check("[PROOF] ... and still zero-fills the caller's buffer",
	    buf[0] == 0 && buf[511] == 0, 1);
	res = diskimage__internal_access(&d, 1, -4096, buf, 512);
	check("[PROOF] WRITE at a NEGATIVE offset is refused", res, 0);
	fclose(d.f);

	/*
	 *  H3. A ZERO-BYTE IMAGE IS REFUSED IN BOTH DIRECTIONS.
	 *
	 *  This is the round's one deliberate behaviour change and nothing
	 *  asserted it either way.  Shipped code allowed the write and grew the
	 *  file.  No escape hatch was added on purpose: a
	 *  `nr_of_logical_blocks > 0` exemption is the same shape #414 measured
	 *  letting a zero-block disk skip a bound entirely, so this row also
	 *  pins that no future round reintroduces it.
	 *
	 *  Note it is UNREADABLE as well as unwritable -- the record said only
	 *  "unwritable", which understated it.
	 */
	snprintf(path, sizeof(path), "%s/h3.img", WORK);
	mkfile(path, 0, 0);
	mkdisk(&d, path, "r+", 1);
	res = diskimage__internal_access(&d, 1, 0, buf, 512);
	check("[PROOF] WRITE to a 0-byte image is refused", res, 0);
	check("[PROOF] ... and the 0-byte file stays 0 bytes", fsize(path), 0);
	res = diskimage__internal_access(&d, 0, 0, buf, 512);
	check("[PROOF] READ from a 0-byte image is refused too", res, 0);
	fclose(d.f);

	/*
	 *  H4. THE SENSE PATH -- NO ROW ISSUED REQUEST SENSE AT ALL.
	 *
	 *  Three separate one-character mutants therefore survived: masking the
	 *  key with 0x00, dropping the latch, and dropping the clear.  A CHECK
	 *  CONDITION whose sense says "no sense" tells a guest that something
	 *  failed and then that nothing is wrong, which ARC can read as
	 *  success -- so the status and its sense are one mechanism and must be
	 *  tested together.
	 */
	snprintf(path, sizeof(path), "%s/h4.img", WORK);
	mkfile(path, 10240, 0x77);		/*  20 backed blocks  */
	mkdisk(&d, path, "r+", 1);
	m = mkmachine(&d); c = mkcpu(m);

	/*  A READ far past capacity -> CHECK CONDITION.  */
	memset(cmd, 0, sizeof(cmd));
	cmd[0] = SCSICMD_READ_10;
	cmd[2] = 0x00; cmd[3] = 0x0f; cmd[4] = 0x42; cmd[5] = 0x40;  /* LBA 1e6 */
	cmd[8] = 1;
	xfer_init(&xfer, cmd, 10);
	diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
	check("[CONTROL] the failing READ really did set CHECK CONDITION",
	    xfer.status[0], 0x02);
	xfer_free(&xfer);

	/*  ... and REQUEST SENSE must now say WHY.  */
	memset(cmd, 0, sizeof(cmd));
	cmd[0] = SCSICMD_REQUEST_SENSE;
	cmd[4] = 18;
	xfer_init(&xfer, cmd, 6);
	diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
	printf("        (evidence: key=0x%02x asc=0x%02x ascq=0x%02x)\n",
	    xfer.data_in[2], xfer.data_in[12], xfer.data_in[13]);
	check("[PROOF] REQUEST SENSE reports ILLEGAL REQUEST after the failure",
	    xfer.data_in[2] & 0x0f, 0x05);
	check("[PROOF] ... with LBA OUT OF RANGE as the additional code",
	    xfer.data_in[12], 0x21);
	xfer_free(&xfer);

	/*  Sense is "current errors" and is CONSUMED by the read: a second
	    query must not report the same failure again.  */
	memset(cmd, 0, sizeof(cmd));
	cmd[0] = SCSICMD_REQUEST_SENSE;
	cmd[4] = 18;
	xfer_init(&xfer, cmd, 6);
	diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
	check("[PROOF] a second REQUEST SENSE reports the sense CLEARED",
	    xfer.data_in[2] & 0x0f, 0x00);
	xfer_free(&xfer);

	/*
	 *  And a command that SUCCEEDS must retire the latch.  #416 latched
	 *  without clearing on success, so a refused READ followed by a GOOD
	 *  READ made the next REQUEST SENSE blame the command that worked --
	 *  a regression #416 introduced and #417 fixes.
	 */
	memset(cmd, 0, sizeof(cmd));
	cmd[0] = SCSICMD_READ_10;
	cmd[2] = 0x00; cmd[3] = 0x0f; cmd[4] = 0x42; cmd[5] = 0x40;
	cmd[8] = 1;
	xfer_init(&xfer, cmd, 10);
	diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
	xfer_free(&xfer);

	memset(cmd, 0, sizeof(cmd));		/*  now a GOOD read of LBA 0  */
	cmd[0] = SCSICMD_READ_10;
	cmd[8] = 1;
	xfer_init(&xfer, cmd, 10);
	diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
	check("[CONTROL] the following in-range READ is GOOD", xfer.status[0], 0x00);
	xfer_free(&xfer);

	memset(cmd, 0, sizeof(cmd));
	cmd[0] = SCSICMD_REQUEST_SENSE;
	cmd[4] = 18;
	xfer_init(&xfer, cmd, 6);
	diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
	check("[PROOF] a SUCCESSFUL command retires the latched sense",
	    xfer.data_in[2] & 0x0f, 0x00);
	xfer_free(&xfer);

	fclose(d.f); free(c); free(m);
}


static void section_real_images(void)
{
	static const char *imgs[] = {
	    "/mnt/c/DocumentNoSnc/cc/GXEMUL/gxemul_pmax_rig/disk.img",
	    "/mnt/c/DocumentNoSnc/cc/GXEMUL/gxemul_pmax_rig/disk_comp.img",
	    "/mnt/c/DocumentNoSnc/cc/GXEMUL/gxemul_arc_rig/disk_comp.img",
	    "/mnt/c/DocumentNoSnc/cc/GXEMUL/gxemul_arc_rig/disk_comp2.img",
	    "/mnt/c/DocumentNoSnc/cc/GXEMUL/_images/liveimage-luna88k-raw-20250518.img",
	    NULL
	};
	int i;

	printf("\nSECTION 6 -- the round-up gap on the REAL rig images (read-only)\n");

	for (i = 0; imgs[i] != NULL; i++) {
		struct diskimage d;
		long long fb, adv, gapblocks;
		unsigned char buf[512];
		int res;

		if (fsize(imgs[i]) < 0) { printf("        (absent: %s)\n", imgs[i]); continue; }

		memset(&d, 0, sizeof(d));
		d.type = DISKIMAGE_SCSI; d.id = 0;
		d.fname = (char *) imgs[i];
		d.f = fopen(imgs[i], "r");
		if (d.f == NULL) { printf("        (unreadable: %s)\n", imgs[i]); continue; }
		d.writable = 0; d.logical_block_size = 512;
		diskimage_recalc_size(&d);

		fb  = fsize(imgs[i]);
		adv = (long long)d.nr_of_logical_blocks * 512;
		gapblocks = (adv - fb) / 512;

		/*  Does a read of the LAST advertised block reach real bytes?  */
		memset(buf, 0xEE, sizeof(buf));
		res = diskimage__internal_access(&d, 0,
		    (d.nr_of_logical_blocks - 1) * 512, buf, 512);

		/*  And what does a SCSI guest see for that same block? This is
		    the number that decides whether a fix is guest-visible.  */
		{
			struct machine *m = mkmachine(&d);
			struct cpu *c = mkcpu(m);
			struct scsi_transfer xfer;
			unsigned char cmd[16];
			int st;
			cdb10(cmd, SCSICMD_READ_10,
			    (uint32_t)(d.nr_of_logical_blocks - 1), 1);
			xfer_init(&xfer, cmd, 10);
			diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
			st = xfer_status(&xfer);
			xfer_free(&xfer);
			free(c); free(m);

			printf("        %-34s file %10lld  adv %10lld  GAP %4lld blk"
			    "  internal_access->%d  SCSI status 0x%02x\n",
			    strrchr(imgs[i], '/') + 1, fb, adv, gapblocks, res, st);
		}
		fclose(d.f);
	}
}


int main(int argc, char *argv[])
{
	/*  Unbuffered, so a crash mid-run still shows how far it got -- an
	    abort() with buffered stdout looks like a build failure.  */
	setvbuf(stdout, NULL, _IONBF, 0);

	if (argc > 1 && strcmp(argv[1], "-v") == 0)
		quiet_stubs = 0;

	printf("r411-C1 disk data-path differential (real diskimage.c +"
	    " diskimage_scsicmd.c)\n");

	/*
	 *  #412: FOUR SECTIONS ARE DISABLED BY DEFAULT, AND THIS IS NOT
	 *  TIDINESS -- THEY ASSERT DEFECTS THAT ARE STILL LIVE.
	 *
	 *  They were built by a measure seat that CONFIRMED all of them, and
	 *  they fail on the shipped tree exactly as they should:
	 *
	 *    write_return   -- a short write (256 of 1024 absorbed) and a total
	 *                      failure (0 of 1024) BOTH return success, errno 27.
	 *    read_eof       -- a read starting past EOF returns success.
	 *    scsi_lba       -- one WRITE(10) past capacity GREW a 10 KB image to
	 *                      512,000,512 bytes and its capacity from 1,008 to
	 *                      1,000,944 blocks, status GOOD. Permanent host-side
	 *                      damage from a single guest command.
	 *    scsi_write_fail-- a WRITE onto a full store returns status GOOD.
	 *
	 *  *** #416 FIXED ALL FOUR AND DELETED THE GUARD.  These sections now
	 *  run unconditionally, which is the point: the -DDISKIMAGE_IO_UNFIXED
	 *  flag existed so the vectors would survive until someone fixed the
	 *  defects, and keeping it after that would be exactly the "permanent
	 *  opt-out" the original note warned about. ***
	 *
	 *  THE STAGING CONSTRAINT THAT ROUND HAD TO RESPECT, and how it was
	 *  resolved: every one of the five rig images carries a 480-992 block
	 *  whole-cylinder round-up gap, addressable but not backed by file.
	 *  Bounding reads against the backed extent was MEASURED to break all
	 *  five.  The bound #416 shipped is therefore ASYMMETRIC -- writes are
	 *  limited to d->total_size so the host file can never grow, reads run
	 *  to the advertised capacity and zero-fill past EOF, so the gap keeps
	 *  behaving exactly as the rig images have always relied on.
	 *  section_roundup_gap below still measures that gap and stays green
	 *  either way, deliberately -- it is evidence, not an assertion, and
	 *  SECTION G is where the boundary is actually asserted.
	 */
	section_write_return();
	section_read_eof();
	section_scsi_lba();
	section_scsi_write_fail();
	section_read_capacity();
	section_roundup_gap();
	section_boundary();
	section_pass2_gaps();
	section_real_images();

	/*
	 *  IDENTITY GUARD.  Two files with this name once differed only by the
	 *  case of a parent directory, and the stale one encoded a REVERSED
	 *  design decision.  A row count is the cheapest proof that the file
	 *  which ran is the file that was reviewed.  Last, so it counts every
	 *  row above it.
	 */
	check("[IDENTITY] row count -- guards against a stale copy", rows + 1, 46);

	printf("\n%d rows, %d failures, %d faults\n", rows, failures, faults);
	printf("%s\n", (failures == 0 && faults == 0) ?
	    "DISKIMAGE_IO_PASS" : "DISKIMAGE_IO_FAIL");
	return 0;
}
