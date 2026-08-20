/*
 *  #437 differential: does SYNCHRONIZE CACHE actually make the guest's data durable?
 *
 *  CONSTRUCTION, same as regress/diff_diskimage_io.c: stub the externals and #include the
 *  SHIPPING diskimage.c and diskimage_scsicmd.c, then drive real CDBs through
 *  diskimage_scsicommand().  The code that runs IS the code that ships; deleting the
 *  include does not weaken the test, it fails to compile.
 *
 *  *** READ THIS BEFORE TRUSTING A GREEN RUN.  Three facts decide whether these rows mean
 *  anything, and each was established by MEASUREMENT during the round, not by argument. ***
 *
 *  1. _exit() SIMULATES PROCESS DEATH, NOT HOST DEATH.  Measured: a plain fflush with NO
 *     fsync leaves the bytes fully visible to a separate reader after _exit(), because the
 *     page cache belongs to the KERNEL and outlives the process.  So a kill-and-check byte
 *     test can only ever see a missing FFLUSH.  It cannot see a missing FSYNC -- only real
 *     power loss distinguishes that, and no test that kills a process can reach it.
 *
 *  2. THEREFORE THE CALL-TRACE ROWS ARE THE LOAD-BEARING ONES.  The bigger half of #437 is
 *     that an overlaid disk NEVER fsynced the file holding the guest's data (measured before
 *     the fix: one fsync, on the base fd that held nothing, and no fflush anywhere).  That is
 *     invisible to any byte comparison and is caught ONLY by the --wrap trace.
 *
 *     AND THE TRACE MUST NAME THE FILE, NOT COUNT THE CALLS.  A count-only version of this
 *     file shipped for one pass and a review seat killed it: four mutants that restore real
 *     data loss all passed it green, because each keeps the totals at 2 and 2.  Two are
 *     re-run as controls (v1: bitmap never synced; v4: base synced instead of bitmap) and
 *     both are now caught.
 *
 *  3. A BYTE-BASED VERSION OF THIS TEST IS VACUOUS ON THE PROJECT'S OWN FILESYSTEM.  glibc
 *     sizes the stdio buffer from st_blksize: 4096 on ext4, but 512 on drvfs -- and /mnt/c,
 *     where _scratchpad, _images and both rigs live, is drvfs.  There every 512-byte fwrite
 *     reaches the kernel immediately, so every byte row would pass with the defect fully
 *     present.  So the durability rows here assert fflush/fsync CALL TRACES, which are a
 *     property of the code rather than of the filesystem.  Two byte rows DO exist, but they
 *     check only that the guest's sector reached the file AT ALL -- not that it survived a
 *     kill -- and that check is filesystem-independent.  The buffer size is REPORTED as a
 *     standing warning to whoever adds a real byte-SURVIVAL row here.
 *
 *  *** EVERY ROW GOES THROUGH diskimage_scsicommand(), AND NONE NAMES diskimage_sync()
 *  DIRECTLY.  That is not style, it is what makes the file a DIFFERENTIAL. ***  A row
 *  calling diskimage_sync() cannot even COMPILE against the pre-fix tree, so the
 *  before/after comparison degrades into "it did not build" -- a SETUP result, never a
 *  detection.  Driving the shipping SCSI handler instead means the identical source
 *  compiles against both trees and the rows themselves report the difference.  (Learned
 *  here: the first version of this file called it directly and the pre-fix arm failed to
 *  link, which proved nothing about any row.)
 *
 *  Three separate one-line edits defeat a BYTE-SURVIVAL version of this detector: growing
 *  the write to one whole stdio buffer, using exit() instead of _exit(), and -- the one
 *  nobody predicted -- issuing ONE MORE SCSI READ after the sync, whose my_fseek flushes the
 *  pending write.  Any realistic-looking test that does anything at all after the sync is
 *  silently green.  This file therefore does not rest its verdict on byte survival.
 *
 *  THE ORDERING RULE IS GATED, and this paragraph used to say plainly that it was not.
 *  SECTION 1b injects an fsync failure on one overlay data file and asserts that THAT
 *  overlay bitmap is absent from the trace while the NEXT overlay is still synced.
 *  MEASURED on four trees before those rows existed: the whole file passed 8 rows / 0
 *  failed against the shipped source AND against every one of `continue` deleted,
 *  `continue` -> `break`, and `continue` -> `return 0`.  Nothing else here separates them.
 *
 *  IT TAKES TWO OVERLAYS, and that is the part worth remembering.  With one overlay the
 *  three mutants above are INDISTINGUISHABLE -- deleting the `continue`, breaking out of
 *  the loop and returning early all produce the same trace, because there is no next
 *  iteration to observe.  A single-overlay version of this row was built first and
 *  measured: it caught the deletion and let the other two through green.
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
#include <sys/wait.h>

/*
 *  CALL RECORDING.  -Wl,--wrap=fsync,--wrap=fflush redirects the real symbols here, so we
 *  can count what the shipping code actually asked the kernel for.  This is the only
 *  evidence that reaches defect (b), and unlike the byte rows it is filesystem-independent.
 */
int __real_fsync(int fd);
int __real_fflush(FILE *f);

/*
 *  *** RECORD WHICH FILE, NOT JUST HOW MANY.  A COUNT-ONLY VERSION OF THIS WAS VACUOUS. ***
 *
 *  Measured in pass 2: with bare counters, FOUR separate mutants that restore real data loss
 *  all passed green -- renaming f_bitmap to f_data in the bitmap branch (so the bitmap is
 *  NEVER synced), inverting the data/bitmap order, deleting the ordering `continue`, and
 *  syncing d->f instead of the bitmap.  Every one keeps the totals at 2 and 2.
 *
 *  So the trace records the fd of every call, and the rows assert the ORDERED SEQUENCE of
 *  files.  "Two fflushes happened" is not the property under test; "the data file was
 *  flushed and synced, and THEN the bitmap was" is.
 */
#define TRACE_MAX 64
static struct { char op; int fd; } trace[TRACE_MAX];
static int trace_n;
static void trace_add(char op, int fd)
{
	if (trace_n < TRACE_MAX) { trace[trace_n].op = op; trace[trace_n].fd = fd; trace_n++; }
}
/*
 *  FAULT INJECTION -- one changed RETURN VALUE, and the mechanism is chosen, not default.
 *
 *  The ordering rule in diskimage_sync() is only OBSERVABLE when an overlay data file fsync
 *  FAILS: until it does, the `continue` has nothing to skip and every mutant of it executes
 *  identically to the shipped code.  So a row for it must make an fsync fail.
 *
 *  Rejected mechanisms, and why:
 *    - a genuinely failing fsync needs a failing device (dm-error, a full filesystem, a
 *      pulled stick).  Root, non-portable, and it would make this gate depend on the
 *      machine rather than on the code -- the same class of defect as the drvfs trap in
 *      note 3 above.
 *    - close()ing the descriptor under the live FILE* does make fsync fail, but it corrupts
 *      stdio state and can later hit a RECYCLED fd.  That is a FAULT, and a fault is never
 *      a detection -- this file already carries one such lesson, at xfer_init().
 *    - an O_RDONLY fd is not a failure at all on glibc (rc 0), so it would prove nothing.
 *
 *  The wrapper is already here and already linked by the gate build line, so the injection
 *  costs one comparison and disturbs NOTHING else: no signal, no freed memory, no closed
 *  descriptor, no byte changed on disk.  The rows below therefore fail on VALUES -- a red
 *  row is a printed string that differs, not a dead process.
 *
 *  The call is recorded BEFORE the failure is returned, deliberately: the trace has to show
 *  that the data fsync was ATTEMPTED, or "the bitmap was not synced" could not be told
 *  apart from "nothing was synced at all".
 */
static int fail_fsync_fd = -1;		/*  -1 = disarmed  */

int __wrap_fsync(int fd)
{
	trace_add('S', fd);
	if (fd == fail_fsync_fd) {
		errno = EIO;
		return -1;
	}
	return __real_fsync(fd);
}
int __wrap_fflush(FILE *f) { trace_add('F', f ? fileno(f) : -1); return __real_fflush(f); }

/*  Render the trace with fds replaced by role names, so a row's expected value is readable
    and a wrong-file mutant produces a visibly different string rather than the same number. */
static const char *trace_str(int fd_data, int fd_bitmap, int fd_base)
{
	static char buf[512];
	int i;
	buf[0] = 0;
	for (i = 0; i < trace_n; i++) {
		const char *who = "other";
		if (trace[i].fd == fd_data)        who = "data";
		else if (trace[i].fd == fd_bitmap) who = "bitmap";
		else if (trace[i].fd == fd_base)   who = "base";
		snprintf(buf + strlen(buf), sizeof(buf) - strlen(buf), "%s%c(%s)",
		    i ? " " : "", trace[i].op, who);
	}
	return buf[0] ? buf : "(none)";
}

/*  The same rendering for TWO overlays.  trace_str() above cannot express what the ordering
    rule actually says -- "stop syncing THIS overlay, then carry on with the NEXT one" --
    because with a single overlay the loop has no next iteration to observe, and MEASURED:
    `continue` deleted, `continue` -> `break` and `continue` -> `return 0` then all produce
    byte-identical traces.  Two overlays separate all three.  */
static const char *trace_str2(int d0, int b0, int d1, int b1)
{
	static char buf[512];
	int i;
	buf[0] = 0;
	for (i = 0; i < trace_n; i++) {
		const char *who = "other";
		if (trace[i].fd == d0)      who = "d0";
		else if (trace[i].fd == b0) who = "b0";
		else if (trace[i].fd == d1) who = "d1";
		else if (trace[i].fd == b1) who = "b1";
		snprintf(buf + strlen(buf), sizeof(buf) - strlen(buf), "%s%c(%s)",
		    i ? " " : "", trace[i].op, who);
	}
	return buf[0] ? buf : "(none)";
}

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

/*  AFTER the include: `struct cpu` is not a known type until the tree's own headers have
    been pulled in, and defining these first produces "conflicting types" against the very
    prototype they are meant to satisfy.  Same trap diff_diskimage_io.c records.  */
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

/*  Both files define a file-static copy of this table; renaming the second is the only
    edit needed to put both translation units together.  */
#define diskimage_types diskimage_types_scsi
#include "../src/disk/diskimage_scsicmd.c"
#undef diskimage_types


/*  ------------------------------------------------------------------  */

static int fails, rows;

static void checks(const char *name, const char *got, const char *want)
{
	rows++;
	if (strcmp(got, want) == 0) {
		printf("  ok    %-46s %s\n", name, got);
	} else {
		printf("  FAIL  %-46s %s (want %s)\n", name, got, want);
		fails++;
	}
}

static void checkn(const char *name, long got, long want)
{
	rows++;
	if (got == want) {
		printf("  ok    %-54s %ld\n", name, got);
	} else {
		printf("  FAIL  %-54s %ld (want %ld)\n", name, got, want);
		fails++;
	}
}

/*  Read byte 0 through a FRESH open(), never through the code's own FILE* -- reading back
    through the same stream would see the stdio buffer and report success for data that never
    left the process.  Returns -1 if the file cannot be read at all.  */
static int first_byte_of(const char *path)
{
	unsigned char b = 0;
	int fd = open(path, O_RDONLY), n;
	if (fd < 0)
		return -1;
	n = read(fd, &b, 1);
	close(fd);
	return n == 1 ? (int)b : -1;
}

static void mkdisk(struct diskimage *d, const char *path, const char *mode, int writable)
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
	diskimage_recalc_size(d);
}

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

static void cdb10(unsigned char *cmd, int op, uint32_t lba, uint16_t nblocks)
{
	memset(cmd, 0, 10);
	cmd[0] = op;
	cmd[2] = (lba >> 24) & 255; cmd[3] = (lba >> 16) & 255;
	cmd[4] = (lba >>  8) & 255; cmd[5] = lba & 255;
	cmd[7] = (nblocks >> 8) & 255; cmd[8] = nblocks & 255;
}

/*  status/msg_in/data_in MUST start NULL: scsi_transfer_allocbuf() free()s any non-NULL
    old pointer, so handing it a stack array aborts the process -- a FAULT, not a
    detection.  Recorded by diff_diskimage_io.c after it happened.  */
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
	free(x->data_out); x->data_out = NULL;
}

static int xfer_status(struct scsi_transfer *x)
{
	return x->status == NULL ? -1 : x->status[0];
}

/*  Issue a WRITE(10) of one sector, then SYNCHRONIZE CACHE, counting the sync calls.
    fail_fd, when not -1, makes fsync() on that one descriptor return EIO.  It is armed
    AFTER the write and disarmed the instant the command returns, for two reasons.  The
    injection must reach ONLY the handler under test: the write path has its own
    fflush/fsync pair at diskimage.c:1315-1317 behind do_fsync, which is 0 here -- so it
    emits nothing today, but a row must not quietly depend on that staying true.  And an
    armed fd number outliving this call could fail a LATER sync once the descriptor had
    been recycled, which would be a false red somewhere else entirely.  */
static int sync_after_write(struct diskimage *d, int fail_fd)
{
	struct machine *m = mkmachine(d);
	struct cpu *c = mkcpu(m);
	struct scsi_transfer xfer;
	unsigned char cmd[10], sector[512];
	int status;

	/*
	 *  SCSICMD_WRITE is 0x0a -- WRITE(6).  Driving it with a 10-byte CDB parses the
	 *  wrong fields and asks for 256 blocks; and the handler refuses any transfer whose
	 *  data_out_offset != size.  The first version of this fixture did both, so it WROTE
	 *  NOTHING and left two 0-byte overlay files behind -- and with nothing written there
	 *  is no durability property to check, only call counts, which is precisely why the
	 *  wrong-file mutants survived.  WRITE_10 plus the offset, as diff_diskimage_io.c
	 *  already does at its own write sites.
	 */
	memset(sector, 0xDD, sizeof(sector));
	cdb10(cmd, SCSICMD_WRITE_10, 0, 1);
	xfer_init(&xfer, cmd, 10);
	scsi_transfer_allocbuf(&xfer.data_out_len, &xfer.data_out, sizeof(sector), 0);
	memcpy(xfer.data_out, sector, sizeof(sector));
	xfer.data_out_offset = sizeof(sector);
	diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
	xfer_free(&xfer);

	trace_n = 0;
	fail_fsync_fd = fail_fd;

	cdb10(cmd, SCSICMD_SYNCHRONIZE_CACHE, 0, 0);
	xfer_init(&xfer, cmd, 10);
	diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
	fail_fsync_fd = -1;
	status = xfer_status(&xfer);
	xfer_free(&xfer);

	free(c); free(m);
	return status;
}


int main(int argc, char *argv[])
{
	char path[256];
	int status, fd_data = -1, fd_bitmap = -1, fd_base = -1;

	(void)argc; (void)argv;
	printf("=== #437 diff_diskimage_sync: SYNCHRONIZE CACHE durability ===\n");

	{
		/*
		 *  SELFCHECK -- CAN THIS FILE'S COMPARATORS STILL FAIL?
		 *
		 *  Feed checks() and checkn() deliberate mismatches and require the failure
		 *  counter to move, then un-record them so the rows are free.  If either has
		 *  been stubbed or had its comparison edited away, every row that uses it is
		 *  silently inert and the gate cannot tell -- the row count, the identity row
		 *  and the verdict token all survive that edit unchanged.  diff_timer.c holds
		 *  the full rationale and the four measurements behind this shape.
		 *
		 *  BOTH HELPERS ARE PROBED, because they are two comparators and not one: this
		 *  file's trace rows go through checks() and its status rows through checkn(),
		 *  so a sentinel that exercised only one would vouch for rows it never touched.
		 *  The numeric probe uses 2^32 against 0 -- EQUAL in their low 32 bits -- so a
		 *  checkn() narrowed to int passes it while the string probe still catches the
		 *  comparator dying outright.
		 *
		 *  This does NOT prove any row is correct, and a comparator that special-cases
		 *  these rows BY NAME is still invisible to it.  Liveness sentinel, nothing
		 *  more.
		 *
		 *  @@SELFCHECK@@ IN THE ROW NAMES IS LOAD-BEARING: these are deliberate
		 *  mismatches, so the helpers print FAIL for them on the HEALTHY path, and
		 *  selfmutant.py filters exactly that token when it looks for the row its
		 *  mutant killed.  gate_offline.sh greps the SUMMARY line below for presence.
		 */
		int sc_f = fails, sc_r = rows, sc_bad = 0;

		checks("@@SELFCHECK@@/str", "a", "b");
		if (fails <= sc_f)
			sc_bad++;
		fails = sc_f; rows = sc_r;

		checkn("@@SELFCHECK@@/wide", 4294967296L, 0);
		if (fails <= sc_f)
			sc_bad++;
		fails = sc_f; rows = sc_r;

		if (sc_bad) {
			printf("  FAIL  SELFCHECK the comparator no longer compares (%d of 2 "
			    "mismatches went unnoticed) -- every row in this file is inert\n",
			    sc_bad);
			fails = sc_f + 1;
			rows = sc_r;
		} else {
			printf("  ok    SELFCHECK the comparator can still fail       "
			    "str+wide\n");
		}
	}

	/*
	 *  VACUITY CONTROL, load-bearing rather than decoration.
	 *
	 *  Write one buffered sector and _exit() without flushing.  Where st_blksize exceeds
	 *  512 the bytes MUST still be in the stdio buffer and MUST NOT be visible to a
	 *  separate reader.  If they ARE visible, the buffer is smaller than one sector
	 *  (drvfs: 512) and no byte-survival row could fail here.  This row does not gate the
	 *  call-recording rows below -- those are filesystem-independent -- but it tells the
	 *  operator which kind of evidence this run actually produced.
	 */
	{
		struct stat st;
		char buf[512];
		pid_t c;
		long visible;

		snprintf(path, sizeof(path), "diff_dis_sync_vac.tmp");
		unlink(path);
		memset(buf, 'V', sizeof(buf));
		c = fork();
		if (c == 0) {
			FILE *f = fopen(path, "w+b");
			if (f == NULL) _exit(9);
			fwrite(buf, 1, sizeof(buf), f);
			_exit(0);		/*  deliberately no flush  */
		}
		while (waitpid(c, NULL, 0) < 0)
			;
		visible = (stat(path, &st) == 0) ? (long)st.st_size : -1;
		unlink(path);

		/*
		 *  DIAGNOSTIC, NOT A SCORED ROW -- and the distinction is deliberate.
		 *
		 *  Every assertion in this file counts fflush/fsync CALLS, which is a
		 *  property of the CODE and not of the filesystem.  Scoring this as a
		 *  row would make the detector FAIL on drvfs for a reason having
		 *  nothing to do with the code under test, and a false FAIL is as
		 *  damaging as a false pass -- this project has already lost a
		 *  45-minute battery to a load-sensitive one.
		 *
		 *  It is printed because it is the standing warning to whoever adds
		 *  the first BYTE-SURVIVAL row here: where st_blksize is 512 such a
		 *  row cannot fail, and /mnt/c -- which holds _scratchpad, _images and
		 *  both rigs -- is exactly that filesystem.
		 */
		if (visible == 0)
			printf("  note  stdio buffer > 512 here: a byte-survival row "
			    "COULD fail on this filesystem.\n");
		else
			printf("  note  *** stdio buffer <= 512 here (drvfs?): a "
			    "byte-survival row COULD NOT FAIL here.  The rows below "
			    "count CALLS and are unaffected. ***\n");
	}

	/*
	 *  SECTION 1 -- OVERLAID DISK.  This is defect (b), the bigger half, and the only
	 *  evidence for it anywhere.  Before #437 this recorded fflush=0, fsync=1 (the base,
	 *  which holds none of the guest's data).  After: the overlay's data file AND its
	 *  bitmap are both flushed and synced.
	 */
	{
		struct diskimage d;
		char ovl[256];

		snprintf(path, sizeof(path), "diff_dis_sync_base.img");
		snprintf(ovl, sizeof(ovl), "diff_dis_sync_ovl");
		unlink(path);
		{
			FILE *f = fopen(path, "w+b");
			unsigned char z[4096];
			memset(z, 0xBB, sizeof(z));
			fwrite(z, 1, sizeof(z), f);
			fclose(f);
		}
		mkdisk(&d, path, "r+b", 1);

		{
			/*  diskimage_add_overlay() opens the data file under the
			    basename itself and the bitmap as "<basename>.map",
			    both with "r+" -- it REFUSES to create either ("Please
			    create the map file first"), so both must pre-exist.  */
			char bfn[300];
			FILE *f;
			snprintf(bfn, sizeof(bfn), "%s.map", ovl);
			unlink(ovl); unlink(bfn);
			f = fopen(ovl, "w+b"); if (f) fclose(f);
			f = fopen(bfn, "w+b"); if (f) fclose(f);
			if (!diskimage_add_overlay(&d, ovl, false)) {
				printf("  FAIL  could not attach overlay -- SETUP, not a result\n");
				return 2;
			}
		}

		fd_data   = fileno(d.overlays[0].f_data);
		fd_bitmap = fileno(d.overlays[0].f_bitmap);
		fd_base   = fileno(d.f);

		status = sync_after_write(&d, -1);
		/*
		 *  THE ORDERED SEQUENCE OF FILES, not a count.  This one row replaces two
		 *  counting rows and kills the mutants they could not see: renaming
		 *  f_bitmap to f_data yields "F(data) S(data) F(data) S(data)", inverting
		 *  the order yields the bitmap pair first, and syncing d->f yields
		 *  "F(base)".  All three keep the totals at 2 and 2.
		 */
		checks("overlay: sync flushes+syncs data, THEN bitmap",
		    trace_str(fd_data, fd_bitmap, fd_base),
		    "F(data) S(data) F(bitmap) S(bitmap)");
		checkn("overlay: a successful sync reports GOOD status", status, 0);
		/*  The guest's bytes really did reach the overlay: without this the rows
		    above are satisfied by a fixture that never wrote anything, which is
		    exactly how the first version of this file passed against four mutants. */
		checkn("overlay: the guest's sector actually reached the overlay",
		    first_byte_of(ovl), 0xDD);

		/*
		 *  SECTION 1b -- THE ORDERING RULE.  #437 shipped it reasoned and reviewed but
		 *  NOT GATED, and the header above used to say so in as many words.
		 *
		 *  A bitmap bit means "this overlay owns this block".  Publishing that bit while
		 *  the block bytes are not durable makes a later read take the overlay HOLE
		 *  instead of the good bytes still in the base -- measured during #437: the guest
		 *  read zeros where the base still held data, reported as a SUCCESSFUL read, with
		 *  no fall-through to the base.  So a data-side failure must skip THAT overlay
		 *  bitmap and go on to the next overlay, which is exactly what the `continue` at
		 *  diskimage.c:2290 does.
		 *
		 *  A SECOND OVERLAY IS WHAT MAKES THE ROW WORK, and it is not decoration.  With one
		 *  overlay there is no next iteration, so `continue`, `break` and `return 0` all
		 *  trace identically -- MEASURED: a single-overlay version of this row caught the
		 *  deletion and let the other two through green.  Two overlays separate all three:
		 *      shipped          F(d0) S(d0)       F(d1) S(d1) F(b1) S(b1)
		 *      continue deleted F(d0) S(d0) F(b0) S(b0) F(d1) S(d1) F(b1) S(b1)
		 *      break / return 0 F(d0) S(d0)
		 */
		{
			char ovl2[256], bfn2[300];
			FILE *f2;
			int d0, b0, d1, b1;

			snprintf(ovl2, sizeof(ovl2), "diff_dis_sync_ovl2");
			snprintf(bfn2, sizeof(bfn2), "%s.map", ovl2);
			unlink(ovl2); unlink(bfn2);
			f2 = fopen(ovl2, "w+b"); if (f2) fclose(f2);
			f2 = fopen(bfn2, "w+b"); if (f2) fclose(f2);
			if (!diskimage_add_overlay(&d, ovl2, false)) {
				printf("  FAIL  could not attach the 2nd overlay -- "
				    "SETUP, not a result\n");
				return 2;
			}

			/*  Re-read all four: the array is realloc()ed by the call above.  */
			d0 = fileno(d.overlays[0].f_data);
			b0 = fileno(d.overlays[0].f_bitmap);
			d1 = fileno(d.overlays[1].f_data);
			b1 = fileno(d.overlays[1].f_bitmap);

			status = sync_after_write(&d, d0);
			checks("overlay: failure skips only ITS OWN bitmap",
			    trace_str2(d0, b0, d1, b1),
			    "F(d0) S(d0) F(d1) S(d1) F(b1) S(b1)");
			/*
			 *  NOT the discriminator, and recording that is the point.  Every
			 *  mutant above sets ok = 0 too, so this row is GREEN on all of
			 *  them.  It earns its place as the independent witness THAT THE
			 *  INJECTION FIRED: if the --wrap flags were dropped from the build
			 *  line, or fail_fsync_fd never matched, this would read 0 (GOOD)
			 *  and the row above would go red for a SETUP reason.  MEASURED:
			 *  two rows red together says "instrument", the row above red
			 *  ALONE says "code".
			 */
			checkn("overlay: a failed sync reports CHECK CONDITION",
			    status, 0x02);
			/*
			 *  CONTROL, same disk, immediately after, injection disarmed: every
			 *  file syncs again.  This is what makes the row above a MEASUREMENT
			 *  rather than the observation that some trace was short -- an edit
			 *  that simply stopped syncing bitmaps, or an f_bitmap gone NULL,
			 *  would satisfy the row above and fails here.  It also proves the
			 *  arm/disarm does not LEAK into the flat section below, where a
			 *  recycled fd number could fail a sync never meant to fail.
			 */
			status = sync_after_write(&d, -1);
			checks("overlay: control -- disarmed, all files sync",
			    trace_str2(d0, b0, d1, b1),
			    "F(d0) S(d0) F(b0) S(b0) F(d1) S(d1) F(b1) S(b1)");

			unlink(ovl2); unlink(bfn2);
		}

		if (d.f) fclose(d.f);
		unlink(path);
	}

	/*
	 *  SECTION 2 -- FLAT DISK, no overlay.  Here d->f IS the file holding the data, so it
	 *  must be flushed and synced -- exactly once each.
	 */
	{
		struct diskimage d;

		snprintf(path, sizeof(path), "diff_dis_sync_flat.img");
		unlink(path);
		{
			FILE *f = fopen(path, "w+b");
			unsigned char z[4096];
			memset(z, 0xBB, sizeof(z));
			fwrite(z, 1, sizeof(z), f);
			fclose(f);
		}
		mkdisk(&d, path, "r+b", 1);

		fd_base = fileno(d.f);
		status = sync_after_write(&d, -1);
		checks("flat: sync flushes+syncs the base, and nothing else",
		    trace_str(-1, -1, fd_base), "F(base) S(base)");
		checkn("flat: a successful sync reports GOOD status", status, 0);
		checkn("flat: the guest's sector actually reached the image",
		    first_byte_of(path), 0xDD);

		if (d.f) fclose(d.f);
		unlink(path);
	}

	/*
	 *  SECTION 3 -- a disk with nothing open cannot be durable.
	 *
	 *  This pins #134 (d->f can be NULL after a failed tape reopen) AND the status half:
	 *  answering "durable" for a disk that cannot be synced is the same defect #416/#417
	 *  corrected for writes.  Asserted through diskimage_scsicommand(), NOT through
	 *  diskimage_sync() directly -- this comment said otherwise for a day
	 *  while the code did the right thing and this file's own header at
	 *  the top says no direct call exists.  A local comment that
	 *  contradicts both the code and the header is worse than none.
	 */
	{
		struct diskimage d;
		struct machine *m;
		struct cpu *c;
		struct scsi_transfer xfer;
		unsigned char cmd[10];

		memset(&d, 0, sizeof(d));
		d.type = DISKIMAGE_SCSI;
		d.id = 0;
		d.f = NULL;			/*  #134: possible after a failed reopen  */
		d.nr_of_overlays = 0;
		d.logical_block_size = 512;
		m = mkmachine(&d);
		c = mkcpu(m);

		cdb10(cmd, SCSICMD_SYNCHRONIZE_CACHE, 0, 0);
		xfer_init(&xfer, cmd, 10);
		diskimage_scsicommand(c, 0, DISKIMAGE_SCSI, &xfer);
		checkn("nothing open: sync reports CHECK CONDITION, not GOOD",
		    xfer_status(&xfer), 0x02);
		xfer_free(&xfer);
		free(c); free(m);
	}

	/*
	 *  IDENTITY -- guards against a stale copy of this file being what the gate runs.
	 *  Deliberately LAST so it counts every row above it: a count asserted first can
	 *  only ever describe a file that no longer exists.  `rows + 1` because this row
	 *  is not counted until checkn() itself increments.
	 */
	checkn("[IDENTITY] row count -- guards against a stale copy", rows + 1, 11);

	printf("\n  %d rows, %d failed\n", rows, fails);
	printf("%s\n", fails ? "DIFF_DISKIMAGE_SYNC_FAIL" : "DIFF_DISKIMAGE_SYNC_PASS");
	return fails ? 1 : 0;
}
