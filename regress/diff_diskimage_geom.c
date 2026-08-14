/*
 *  regress/diff_diskimage_geom.c  --  queue #113.
 *
 *  Differential oracle for diskimage_recalc_size() geometry and for the
 *  `-d gH;S` geometry override parser.  Links against the REAL diskimage.c
 *  (SIX non-libc stubs: debug, debug_indentation, debugmsg, debugmsg_cpu,
 *  fatal, mymkstemp), so what is measured is the shipped function, not a
 *  re-implementation of it.
 *
 *  ---------------------------------------------------------------------
 *  WHAT IT ASSERTS, AND WHY IN THIS SHAPE
 *
 *  1. EVERY ROW ASSERTS THE FULL TUPLE -- cylinders, heads, sectors per
 *     track AND nr_of_logical_blocks.  A row that asserts only "capacity is
 *     no longer zero" passes on a fix that computes the wrong cylinder
 *     count, which is the single most likely way to get #113 wrong.  The
 *     prototype this file replaces already had that property; it is
 *     restated here because it is the load-bearing one.
 *
 *  2. THE BOUND CONSTANTS ARE HARDCODED HERE ON PURPOSE.  This file does
 *     NOT include DISKIMAGE_MAX_HEADS/DISKIMAGE_MAX_SPT from diskimage.h.
 *     A detector that imports the constant it is checking cannot catch a
 *     change to that constant -- edit the header and the "test" moves with
 *     it.  255 is written out below, and the derivation is in the comment
 *     next to it, so the two have to be reconciled by a human.
 *
 *  3. TWO ENTRY POINTS.  geom() rows construct a struct diskimage exactly
 *     as diskimage_add() does before it calls recalc (memset 0, then
 *     logical_block_size = 512, then the override fields) and call
 *     diskimage_recalc_size() directly.  parse() rows go through the REAL
 *     diskimage_add(), because the H/S bound lives in the parser and no
 *     amount of recalc-level testing can reach it.
 *
 *  4. THE FOUR FLOPPY ROWS CARRY FOUR DISTINCT SECTOR COUNTS -- 9, 15, 18,
 *     36.  A mutant that hardcodes any single value dies on at least three
 *     of them.  (The same trap #409/#410 hit on diff_wdc_identify.c: three
 *     rows sharing a value cover one third of what their names claim.)
 *     THEY ALSO PASS TYPE UNKNOWN, so each row covers its own
 *     AUTODETECTION PREDICATE as well as its own sector count.  When they
 *     passed DISKIMAGE_FLOPPY they entered the arm directly and left three
 *     of the four predicates untested -- see the note beside them.
 *
 *  7. MUTATION-SCORED BY EXECUTION, NOT BY INSPECTION, TWICE.
 *
 *     Pass 1, against the 26-row version: 38 mutants, 23 killed, 15
 *     survived -- 5 PROVABLY EQUIVALENT and 10 real evasions.  Five rows
 *     closed the five that mattered.
 *
 *     Pass 2, against the resulting 30-row version: 46 mutants, and TEN
 *     MORE real evasions in THREE FAMILIES that the first pass had not
 *     reached at all.  Four further rows close them, marked in place under
 *     "regions no earlier row entered".  The lesson is in the shape of the
 *     misses, not their number: each family was a whole REGION of the input
 *     space -- non-multiple floppy sizes, types SCSI and IDE, negative
 *     parse vectors -- that no row had entered, so no amount of tightening
 *     the existing rows could have found them.
 *
 *     Reporting equivalent mutants as coverage gaps would be dishonest, and
 *     reporting the real ones as "hard to reach" would be worse.  Each
 *     surviving mutant was confirmed to be a BEHAVIOUR CHANGE by a separate
 *     witness probe driving the real diskimage_add() on inputs no row uses
 *     -- a mutant nothing distinguishes is not a gap, it is a synonym.
 *     Confirmed equivalent by execution and NOT worth rows: dropping the
 *     (int64_t) cast (255*255*512 < 2^31 so the product is in range either
 *     way), substituting `size` for d->total_size at either site, strtoll
 *     -> strtol on LP64, swapping the clamp order, and swapping the two
 *     bound constants (both are 255).
 *
 *  9. ONE GUARD IN THE SUBJECT HAS NO DETECTOR, AND THAT IS RECORDED RATHER
 *     THAN PAPERED OVER.  Deleting `if (bytespercyl < 1) bytespercyl = 1;`
 *     passes all these rows AND 50 further witness probes, because the
 *     clamps upstream make it unreachable from every in-tree path.  It is
 *     kept as defence-in-depth for a future non-parser caller of the public
 *     diskimage_recalc_size(); measured, with BOTH the guard and the clamp
 *     removed the detector dies with SIGFPE.  This is the "shipped fix with
 *     no detector" vacuity class -- naming it is the honest treatment.
 *
 *  8. A CORRECTION THIS FILE CARRIES SO IT IS NOT REDISCOVERED.  Earlier
 *     records claimed "swapping the parser's heads/spt assignments
 *     survives every row".  That is FALSE for this file and was confirmed
 *     false by two independent seats: the `bound: 16;63 (the default)
 *     accepted` row goes through the REAL diskimage_add() and asserts the
 *     full tuple, so a swap yields 63/16 -- an identical bytespercyl,
 *     identical cylinder count and identical block count, but the wrong
 *     tuple.  The full-tuple assertion is what earns its keep there.  The
 *     stale note described an earlier RECALC-ONLY draft of this file.
 *
 *  5. THE OVERRIDE-EXACT ROW (39424 bytes = 7*11*512) IS THE ONLY ROW THAT
 *     KILLS AN UNCONDITIONAL ROUND-UP.  Its twin at 39425 is the only row
 *     that kills a missing one.  Neither is redundant.
 *
 *  6. THE `-d f:` ROWS EXIST BECAUSE THE PARSER BOUND DOES NOT COVER THEM.
 *     The floppy arm COMPUTES sectors-per-track from the file size, so it
 *     can exceed the same 8-bit fields the parser bound protects, without
 *     the parser ever seeing a number.  Measured: with the bound in place
 *     but no floppy clamp, `-d f:` on a 20 MB file still yields spt 256 and
 *     on a 100 MB file 1280.  A round that adds only the parser bound and
 *     claims H*S is bounded is wrong, and this row is what says so.
 *     `-d f:` on a 40 KB file is the divide-by-zero row: the naive fix,
 *     measured, dies with SIGFPE (exit 136, core dumped) because spt
 *     computes to 0 and becomes a divisor.
 *
 *  FAILURE TOKENS are distinguishable per row (the row name is printed on
 *  the FAIL line), so a mutation run can assert WHICH row killed a mutant
 *  rather than merely that something failed.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

#include "misc.h"
#include "diskimage.h"
#include "machine.h"

/*
 *  The bound, derived from the tree and NOT imported from it (see note 2).
 *
 *  The narrowest carriers of heads and sectors-per-track anywhere in this
 *  source tree are ONE BYTE each, all four in diskimage_scsicmd.c's
 *  MODE SENSE responses:
 *      heads  -- "rigid disk geometry page" (page 4) byte 5,
 *                "flexible disk page"       (page 5) byte 4;
 *      spt    -- "format device page"       (page 3) byte 11, whose
 *                companion byte 10 is hardwired to 0,
 *                "flexible disk page"       (page 5) byte 5.
 *  The other carriers are WIDER: the ATA IDENTIFY words 1, 3 and 6 in
 *  dev_wdc.c are 16-bit, and diskimage_getchs() narrows int64_t into int.
 *  255 is therefore permissive against those -- it is the largest value the
 *  tree can describe, not the largest anyone wants.
 *
 *  ONE CARRIER IS NARROWER AND IS NOT COVERED, and an earlier draft of this
 *  comment listed it among the wide ones, which was backwards: the ATA SDH
 *  register's head field is FOUR bits (dev_wdc.c, wd_sdh case,
 *  `d->head = idata & 0xf`), so an IDE guest cannot address more than 16
 *  heads at all.  g255;63 will IDENTIFY 255 heads that such a guest cannot
 *  reach.  That narrowing is pre-existing; it is recorded here and in
 *  diskimage.h as a limitation, NOT cited as support for the bound.
 */
#define	GEOM_MAX_HEADS	255
#define	GEOM_MAX_SPT	255

static int rows = 0, failures = 0;
static int fatal_calls = 0;
static char fatal_buf[512];

/*  ---- the five non-libc symbols diskimage.o imports ---- */
void debug(const char *fmt, ...) { (void)fmt; }
void debug_indentation(int i) { (void)i; }
void debugmsg(int s, const char *sub, int v, const char *fmt, ...)
{ (void)s; (void)sub; (void)v; (void)fmt; }
void debugmsg_cpu(struct cpu *c, int s, const char *sub, int v,
    const char *fmt, ...) { (void)c; (void)s; (void)sub; (void)v; (void)fmt; }
void fatal(const char *fmt, ...)
{
	va_list ap;
	fatal_calls ++;
	va_start(ap, fmt);
	vsnprintf(fatal_buf, sizeof(fatal_buf), fmt, ap);
	va_end(ap);
}
int mymkstemp(char *t) { (void)t; return -1; }

/*  ---- a real file of an exact size; recalc_size() stat()s it ---- */
static void mkfile(const char *path, int64_t nbytes)
{
	FILE *f = fopen(path, "wb");
	struct stat st;

	if (f == NULL) {
		printf("  FAULT cannot create %s\n", path);
		exit(2);
	}
	if (nbytes > 0) {
		if (fseeko(f, (off_t)(nbytes - 1), SEEK_SET) != 0 ||
		    fputc(0, f) == EOF) {
			printf("  FAULT cannot size %s\n", path);
			exit(2);
		}
	}
	fclose(f);

	if (stat(path, &st) != 0 || (int64_t)st.st_size != nbytes) {
		printf("  FAULT %s is not %lld bytes\n", path,
		    (long long)nbytes);
		exit(2);
	}
}

static const char *nextpath(void)
{
	static char path[256];
	static int seq = 0;
	snprintf(path, sizeof(path), "%s/geom_%d.img",
	    getenv("GEOMDIR") != NULL ? getenv("GEOMDIR") : "/tmp", seq++);
	return path;
}

/*
 *  A recalc-level row.  lbs is passed explicitly so the logical-block-size
 *  rounding can be exercised at values other than 512 (see the ROUNDING
 *  section at the bottom).
 */
static void geom(const char *name, int64_t filesize, int type, int override,
    int oh, int64_t os, int lbs,
    int64_t want_c, int want_h, int64_t want_s, int64_t want_blocks)
{
	struct diskimage d;
	const char *path = nextpath();

	mkfile(path, filesize);

	memset(&d, 0, sizeof(d));
	d.fname = (char *) path;
	d.type = type;
	d.logical_block_size = lbs;
	if (override) {
		d.chs_override = 1;
		d.heads = oh;
		d.sectors_per_track = os;
	}

	rows ++;

	if (!diskimage_recalc_size(&d)) {
		printf("  FAIL %-44s recalc_size() returned false\n", name);
		failures ++;
		return;
	}

	if (d.cylinders != want_c || d.heads != want_h ||
	    d.sectors_per_track != want_s ||
	    d.nr_of_logical_blocks != want_blocks) {
		printf("  FAIL %-44s C/H/S=%lld/%d/%lld blocks=%lld, want "
		    "%lld/%d/%lld blocks=%lld\n", name,
		    (long long)d.cylinders, d.heads,
		    (long long)d.sectors_per_track,
		    (long long)d.nr_of_logical_blocks,
		    (long long)want_c, want_h, (long long)want_s,
		    (long long)want_blocks);
		failures ++;
		return;
	}

	printf("  ok   %-44s C/H/S=%lld/%d/%lld blocks=%lld\n", name,
	    (long long)d.cylinders, d.heads, (long long)d.sectors_per_track,
	    (long long)d.nr_of_logical_blocks);
}

/*
 *  A parser-level row: the REAL diskimage_add(), with the prefix string the
 *  user would type.  want_accept == 0 means "must be rejected", and a
 *  rejection must also have PRINTED a diagnostic; otherwise the full tuple is
 *  asserted as above.
 */
static void parse(const char *name, int64_t filesize, const char *prefix,
    int want_accept,
    int64_t want_c, int want_h, int64_t want_s, int64_t want_blocks)
{
	struct machine *m;
	struct diskimage *d;
	const char *path = nextpath();
	char arg[512];
	int r;

	mkfile(path, filesize);
	snprintf(arg, sizeof(arg), "%s%s", prefix, path);

	m = (struct machine *) calloc(1, sizeof(struct machine));
	if (m == NULL) { printf("  FAULT calloc\n"); exit(2); }

	rows ++;
	fatal_calls = 0;
	fatal_buf[0] = '\0';

	r = diskimage_add(m, arg);

	if (!want_accept) {
		if (r >= 0) {
			d = m->first_diskimage;
			printf("  FAIL %-44s ACCEPTED (want reject); "
			    "C/H/S=%lld/%d/%lld blocks=%lld\n", name,
			    (long long)d->cylinders, d->heads,
			    (long long)d->sectors_per_track,
			    (long long)d->nr_of_logical_blocks);
			failures ++;
			return;
		}
		if (fatal_calls == 0) {
			printf("  FAIL %-44s rejected SILENTLY (no diagnostic "
			    "was printed)\n", name);
			failures ++;
			return;
		}
		printf("  ok   %-44s rejected: %s", name, fatal_buf);
		return;
	}

	if (r < 0) {
		printf("  FAIL %-44s REJECTED (want accept): %s", name,
		    fatal_calls ? fatal_buf : "(no diagnostic)\n");
		failures ++;
		return;
	}

	d = m->first_diskimage;
	if (d == NULL) {
		printf("  FAIL %-44s accepted but no disk was linked in\n",
		    name);
		failures ++;
		return;
	}

	if (d->cylinders != want_c || d->heads != want_h ||
	    d->sectors_per_track != want_s ||
	    d->nr_of_logical_blocks != want_blocks) {
		printf("  FAIL %-44s C/H/S=%lld/%d/%lld blocks=%lld, want "
		    "%lld/%d/%lld blocks=%lld\n", name,
		    (long long)d->cylinders, d->heads,
		    (long long)d->sectors_per_track,
		    (long long)d->nr_of_logical_blocks,
		    (long long)want_c, want_h, (long long)want_s,
		    (long long)want_blocks);
		failures ++;
		return;
	}

	printf("  ok   %-44s C/H/S=%lld/%d/%lld blocks=%lld\n", name,
	    (long long)d->cylinders, d->heads, (long long)d->sectors_per_track,
	    (long long)d->nr_of_logical_blocks);
}

int main(void)
{
	printf("diskimage geometry, against the REAL diskimage.c\n");
	printf("================================================================\n");

	/*
	 *  POSITIVE CONTROL.  Passes on the code as shipped TODAY, before any
	 *  #113 change.  If this row ever fails, the harness is broken, not
	 *  the subject.  10485760 / (16*63*512 = 516096) = 20.32 -> C = 21.
	 */
	printf("-- control (passes on the UNFIXED tree) --\n");
	geom("control: plain 10 MB, no override", 10485760, 0, 0, 0, 0, 512,
	    21, 16, 63, 21168);

	/*  ---- (a) the override arm never assigned cylinders ---- */
	printf("-- defect (a): the gH;S override arm --\n");

	/*  bytespercyl = 7*11*512 = 39424 exactly.  ONLY row that kills an
	    unconditional round-up.  */
	geom("override EXACT does not round up", 39424, 0, 1, 7, 11, 512,
	    1, 7, 11, 77);

	/*  One byte more needs a second cylinder.  ONLY row that kills a
	    missing round-up.  */
	geom("override non-integral rounds up", 39425, 0, 1, 7, 11, 512,
	    2, 7, 11, 154);

	/*  The override that names the tree's OWN default geometry must give
	    the same answer as no override at all -- pairs with the control.  */
	geom("override 16;63 == the default geometry", 10485760, 0, 1, 16, 63,
	    512, 21, 16, 63, 21168);

	/*  Degenerate but legal: 1 head, 1 sector.  Kills a fix that assumes
	    a minimum track size.  */
	geom("override 1;1 (degenerate, legal)", 10485760, 0, 1, 1, 1, 512,
	    20480, 1, 1, 20480);

	/*  The DEFAULT arm's own exact case: 20 * 516096 = 10321920.  The
	    round-up is shared code after #113, but a mutant can still make one
	    arm unconditional, so both arms carry an exact row.  */
	geom("default arm EXACT does not round up", 10321920, 0, 0, 0, 0, 512,
	    20, 16, 63, 20160);

	/*  ---- (b) the floppy arm read nr_of_logical_blocks before it was set ---- */
	printf("-- defect (b): the floppy arm --\n");

	/*
	 *  Four DISTINCT sector counts: 9, 15, 18, 36.  A mutant that pins any
	 *  one value dies on at least three of these.
	 *
	 *  *** THESE ROWS PASS TYPE UNKNOWN, NOT DISKIMAGE_FLOPPY, AND THAT IS
	 *  THE WHOLE POINT.  They previously passed DISKIMAGE_FLOPPY, which
	 *  enters the floppy arm directly and BYPASSES the four autodetection
	 *  predicates.  A measure seat found the consequence: changing
	 *  720*1024 to 721*1024 in that list -- ONE CHARACTER -- broke 720 KB
	 *  autodetection while all 26 rows still passed, because only ONE row
	 *  (1.44 MB) exercised autodetection at all.  Passing UNKNOWN makes
	 *  each row cover its own SIZE predicate as well as its own sector
	 *  count.  Witness for the surviving mutant: a plain ':' 737280-byte
	 *  image returned 2/16/63 blocks=2016 instead of 80/2/9 blocks=1440.
	 *
	 *  SCOPE, MEASURED AND HONEST: these rows cover the four SIZE
	 *  comparisons and NOT the type half of the same condition.  Deleting
	 *  `&& d->type == DISKIMAGE_UNKNOWN` still passes every row here --
	 *  the witness is `-d s:` on a 1.44 MB image, which then flips from
	 *  SCSI 3/16/63 to FLOPPY 80/2/18.  The s: and i: rows added further
	 *  down are what make that mutant reachable at all. ***
	 */
	geom("autodetect 720 KB  -> 80/2/9",  737280,  0, 0, 0, 0,
	    512, 80, 2, 9, 1440);
	geom("autodetect 1.2 MB  -> 80/2/15", 1228800, 0, 0, 0, 0,
	    512, 80, 2, 15, 2400);
	geom("autodetect 1.44 MB -> 80/2/18", 1474560, 0, 0, 0, 0,
	    512, 80, 2, 18, 2880);
	geom("autodetect 2.88 MB -> 80/2/36", 2949120, 0, 0, 0, 0,
	    512, 80, 2, 36, 5760);

	/*  The EXPLICIT type path, which `-d f:` reaches and autodetection
	    does not.  Keeps both entries into the floppy arm covered now that
	    the four rows above have moved to UNKNOWN.  */
	geom("explicit FLOPPY type 1.44 MB", 1474560, DISKIMAGE_FLOPPY, 0, 0, 0,
	    512, 80, 2, 18, 2880);

	/*
	 *  A ZERO-BYTE IMAGE MUST STAY EMPTY -- and this row does not guard
	 *  #414 at all, it guards #412.
	 *
	 *  diskimage_scsicmd.c's READ CAPACITY carries "if
	 *  (d->nr_of_logical_blocks < 1) size = 0;", added by #412 so an empty
	 *  disk stops announcing 2 TiB.  A measure seat showed that adding
	 *  "if (d->cylinders < 1) d->cylinders = 1;" here -- a plausible
	 *  defensive edit -- survives every other row while turning a 0-byte
	 *  disk from blocks=0 into blocks=1008, which stops #412's guard
	 *  firing on its own gate vector.  Before this row the suite contained
	 *  no zero-byte image, so a later edit could silently disable a fix
	 *  from three commits earlier.
	 */
	geom("0-byte image stays empty (guards #412)", 0, 0, 0, 0, 0, 512,
	    0, 16, 63, 0);

	/*
	 *  B2: the override on a floppy.  9 sectors on a 1.44 MB image is a
	 *  geometry the autodetect would never pick, so this row pins the
	 *  DECISION -- the override is honoured -- and it is the only floppy
	 *  row whose cylinder count is not 80, so a mutant that hardcodes
	 *  cylinders = 80 in the floppy arm dies here.  Note the capacity is
	 *  unchanged at 2880 blocks: honouring the override redescribes the
	 *  disk, it never resizes it.
	 */
	geom("floppy + override 2;9 -> 160/2/9", 1474560, DISKIMAGE_FLOPPY,
	    1, 2, 9, 512, 160, 2, 9, 2880);

	/*  ---- the H*S bound, at the parser ---- */
	printf("-- the H*S bound (parser) --\n");

	parse("bound: 255;255 is ACCEPTED", 10485760, "g255;255:", 1,
	    1, GEOM_MAX_HEADS, GEOM_MAX_SPT, 65025);
	parse("bound: 16;63 (the default) accepted", 10485760, "g16;63:", 1,
	    21, 16, 63, 21168);
	parse("bound: 256;63 rejected (one over)", 10485760, "g256;63:", 0,
	    0, 0, 0, 0);
	parse("bound: 16;256 rejected (one over)", 10485760, "g16;256:", 0,
	    0, 0, 0, 0);
	parse("bound: 65536;65536 rejected", 10485760, "g65536;65536:", 0,
	    0, 0, 0, 0);
	parse("bound: 2e9;2e9 rejected (would overflow)", 10485760,
	    "g2000000000;2000000000:", 0, 0, 0, 0, 0);

	/*
	 *  The parse must not TRUNCATE before it bounds.  2^32+16 through
	 *  atoi() yields 16, which passes every bound a 32-bit check could
	 *  state.  Measured on the shipped tree: `-d g4294967312;63` is
	 *  accepted as heads=16.  This row is the only one that distinguishes
	 *  a 64-bit parse from a 32-bit one.
	 */
	parse("bound: 2^32+16 must NOT wrap to 16", 10485760,
	    "g4294967312;63:", 0, 0, 0, 0, 0);

	/*  strtoll saturates to LLONG_MAX on ERANGE, which is outside the
	    range, so the range check subsumes the errno check.  */
	parse("bound: 1e20 rejected (parse saturates)", 10485760,
	    "g99999999999999999999;63:", 0, 0, 0, 0, 0);

	/*  The pre-existing lower bound must survive the change.  */
	parse("bound: 0 heads still rejected", 10485760, "g0;63:", 0,
	    0, 0, 0, 0);
	parse("bound: 0 spt still rejected", 10485760, "g16;0:", 0,
	    0, 0, 0, 0);

	/*
	 *  *** THE WRAP VECTOR IN THE **SPT** POSITION.  The row above it puts
	 *  the 2^32-scale value in the HEADS position only, and that asymmetry
	 *  was measurable: a mutant converting heads to strtoll while leaving
	 *  atoi on spt passed all 26 rows.  Witness: `-d g16;4294967360:` was
	 *  ACCEPTED with spt=64.  The fix touches TWO parse sites five lines
	 *  apart and this row is what says both were done. ***
	 */
	parse("bound: 2^32+64 must NOT wrap in the SPT position", 10485760,
	    "g16;4294967360:", 0, 0, 0, 0, 0);

	/*
	 *  THE BASE MUST BE 10, NOT 0.  strtoll(fname, NULL, 0) reads a
	 *  leading zero as octal, so `g010;63:` would silently become 8 heads
	 *  rather than 10, and `g0x10;63:` would flip from rejected to
	 *  accepted-as-16.  Every other row uses plain decimal with no leading
	 *  zero, so nothing else can see the difference.
	 *  10485760 / (10*63*512 = 322560) = 32.5 -> C = 33; 10*63*33 = 20790.
	 */
	parse("parse: leading zero is decimal, not octal", 10485760,
	    "g010;63:", 1, 33, 10, 63, 20790);

	/*
	 *  ---- the routes the parser bound CANNOT reach ----
	 *
	 *  `-d f:` forces FLOPPY at any file size with no override at all, so
	 *  the floppy arm's COMPUTED spt is not covered by any parser check.
	 *  Without a clamp this yields 256 at 20 MB and 1280 at 100 MB, both
	 *  past the 8-bit MODE SENSE fields the bound exists to protect.
	 */
	printf("-- what the parser bound does NOT cover --\n");
	parse("f: on 20 MB must not exceed spt 255", 20971520, "f:", 1,
	    81, 2, GEOM_MAX_SPT, 41310);
	parse("f: on 100 MB must not exceed spt 255", 104857600, "f:", 1,
	    402, 2, GEOM_MAX_SPT, 205020);

	/*
	 *  A file smaller than one 80/2 track-set computes spt 0, and spt 0
	 *  becomes a DIVISOR once the cylinder computation is shared.  The
	 *  naive fix, measured, dies here with SIGFPE (exit 136, core dumped).
	 *  This row is the reason the spt >= 1 guard is load-bearing rather
	 *  than defensive.
	 */
	parse("f: on 40 KB must not divide by zero", 40960, "f:", 1,
	    40, 2, 1, 80);
	parse("f: on 1 byte must not divide by zero", 1, "f:", 1,
	    1, 2, 1, 2);

	/*
	 *  *** THE ONE ROW THAT TESTS THE ROUND'S CONTESTED DECISION AT THE
	 *  LEVEL WHERE IT IS IMPLEMENTED.  Every other prefix here is either
	 *  `g...:` or `f:`, never both, and the override-on-a-floppy behaviour
	 *  was covered only by a geom() row that pokes d.chs_override onto the
	 *  struct directly.  A measure seat showed the gap is real: changing
	 *  the parser's `if (prefix_g)` to `if (prefix_g && !prefix_f)` -- ONE
	 *  TOKEN, and literally what the manual used to claim -- passed all 26
	 *  rows.  Witness: `-d fg2;9:` on 1.44 MB returned 80/2/18 instead of
	 *  160/2/9.
	 *
	 *  The capacity is 2880 blocks either way HERE, because 2*9*512
	 *  divides 1474560 exactly.  That coincidence is precisely why the
	 *  full tuple is asserted rather than the block count: C and S differ
	 *  even when the capacity does not.  It is also why the round's
	 *  earlier claim that an override "cannot change capacity" was wrong;
	 *  see the header note.
	 */
	parse("fg2;9 is honoured through the parser", 1474560, "fg2;9:", 1,
	    160, 2, 9, 2880);

	/*
	 *  ---- THREE FAMILIES OF EVASION A PASS-2 MEASURE SEAT FOUND ----
	 *
	 *  46 mutants were compiled and run against the 30-row version above.
	 *  Ten survived in three families; the four rows below close them.  The
	 *  point is not the individual mutants -- it is that each family was a
	 *  whole REGION of the input space that no row entered.
	 */
	printf("-- regions no earlier row entered --\n");

	/*
	 *  FAMILY A: THE FLOPPY DIVISOR WAS PINNED FROM ONE SIDE ONLY.
	 *
	 *  All four documented floppy sizes are EXACT multiples of 80*2*512 =
	 *  81920, so the floor divide is insensitive to the divisor over a wide
	 *  band -- measured, EVERY divisor in [79706, 81920] passed all 30
	 *  rows, 2215 integers, with the shipped value at the top of the
	 *  window.  So `512` -> `511` (one character), `80` -> `79`, and
	 *  ceil-instead-of-floor all survived.
	 *
	 *  736000 is deliberately NOT a multiple of 81920: spt = 736000/81920
	 *  = 8 (floor), bytespercyl = 2*8*512 = 8192, and 736000/8192 = 89.84
	 *  so cylinders round up to 90.  The mutant returns 80/2/9.
	 */
	parse("f: on a size that is NOT a multiple of 81920", 736000, "f:", 1,
	    90, 2, 8, 1440);

	/*
	 *  FAMILY B: NO ROW REACHED THE SHARED CYLINDER BLOCK AT TYPE SCSI OR
	 *  IDE -- AND THAT IS THE DEFAULT TYPE FOR EVERY PRIMARY RIG.
	 *
	 *  diskimage_add() assigns the machine-default type AFTER it calls
	 *  diskimage_recalc_size(), so every parse() row above is still
	 *  UNKNOWN when the geometry is computed, and every geom() row passes
	 *  0 or DISKIMAGE_FLOPPY.  An explicit s:/i: prefix is the only way to
	 *  enter recalc already typed.
	 *
	 *  *** CONSEQUENCE, MEASURED: wrapping the shared block in
	 *  `if (d->type != DISKIMAGE_SCSI)` passed all 30 rows, and `-d s:` on
	 *  a 10 MB image then returned 0/16/63 blocks=0 -- THIS ROUND'S OWN
	 *  DEFECT, REINSTATED, for the type get_default_disk_type_for_machine()
	 *  returns on PMAX, ARC, SGI, LUNA88K and MVME88K.  The same held for
	 *  `!= DISKIMAGE_IDE`, `!d->is_a_tape` and `!d->is_a_cdrom`. ***
	 */
	parse("s: reaches the shared cylinder block as SCSI", 10485760, "s:", 1,
	    21, 16, 63, 21168);
	parse("i: reaches the shared cylinder block as IDE", 10485760, "i:", 1,
	    21, 16, 63, 21168);

	/*
	 *  FAMILY C (the parse family): AN UNSIGNED PARSE FOLDS A NEGATIVE
	 *  VALUE BACK INTO RANGE.
	 *
	 *  strtoull() applies a leading minus in UNSIGNED arithmetic, so
	 *  "-18446744073709551615" (-ULLONG_MAX) converts to 1 and would be
	 *  accepted as spt=1.  strtoll() underflows to LLONG_MIN, which the
	 *  range check rejects.  One inserted character -- strtoll -> strtoull
	 *  at the spt site -- passed all 30 rows, because every other vector
	 *  here is non-negative.  A plain "-1" does NOT discriminate: both
	 *  parses end up below 1 and both reject.
	 */
	parse("bound: -ULLONG_MAX must not fold to 1 in the SPT position",
	    10485760, "g16;-18446744073709551615:", 0, 0, 0, 0, 0);

	/*
	 *  ---- ROUNDING AT A NON-512 LOGICAL BLOCK SIZE ----
	 *
	 *  DEFERRED, DELIBERATELY, AND THE REASON IS MEASURED.
	 *
	 *  diskimage_recalc_size() rounds the block count up with
	 *  `size & (logical_block_size - 1)`, a power-of-two MASK standing in
	 *  for a MODULO.  Every row above uses logical_block_size == 512,
	 *  where mask and modulo agree, so `& (lbs-1)` -> `% lbs` survives all
	 *  of them.  The row below at lbs = 257 does distinguish them: a
	 *  516096-byte image is 2008.15 blocks of 257 bytes, so the correct
	 *  answer is 2009 and the shipped code gives 2008.
	 *
	 *  IT IS NOT ENABLED IN THIS ROUND.  Enabling it asserting 2009 makes
	 *  the file RED before the rounding fix exists, and #113 is not that
	 *  fix; enabling it asserting 2008 would freeze the defect into the
	 *  regression suite, which is worse than not testing it.  It ships
	 *  with the rounding correction, in the same commit, and this comment
	 *  is here so that commit does not have to rediscover the vector.
	 *
	 *  Reachability, checked rather than assumed: logical_block_size is
	 *  assigned only the literal 512 in diskimage_add() (three sites), and
	 *  2048 only inside an `#if 0`.  So 257 is a UNIT-level value, not one
	 *  a command line can produce -- which is exactly why it belongs in a
	 *  differential file like this one and not in a boot gate.
	 */
#ifdef GEOM_ROW_LBS257
	printf("-- non-512 logical block size (rounding fix) --\n");
	geom("lbs 257: 516096 B is 2009 blocks", 516096, 0, 0, 0, 0, 257,
	    1, 16, 63, 2009);
#endif

	printf("================================================================\n");
	printf("%d rows, %d failures\n", rows, failures);
	if (failures == 0)
		printf("DISKIMAGE_GEOM_PASS\n");
	return failures ? 1 : 0;
}
