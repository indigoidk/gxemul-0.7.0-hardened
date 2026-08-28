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
/*  SECTION: an UNALIGNED read across an overlay boundary (row b115)     */
/*
 *  THE DEFECT.  fread_helper() picks an overlay layer for the block that
 *  contains curofs, then reads up to a whole block from that layer without
 *  clamping to what REMAINS in the block.  With an unaligned offset the read
 *  runs past the block's end into blocks that may live in a different layer,
 *  while buf advances on a fixed OVERLAY_BLOCK_SIZE stride.
 *
 *  THE ASYMMETRY THAT MAKES IT UNAMBIGUOUS: fwrite_helper() explicitly REFUSES
 *  a non-multiple length and an unaligned offset (both under #164).
 *  fread_helper() has no such guard anywhere.  The read path was simply never
 *  given the check the write path has.
 *
 *  CONTRACT -- what these rows are designed to catch, so a later escape is either
 *  outside the contract or a breach of it, rather than an argument about
 *  overclaiming:  they catch a read that takes bytes from the WRONG LAYER, and a
 *  read that leaves HOLES in the caller's buffer, for a SINGLE overlay whose
 *  bitmap marks one block -- at BOTH len > OVERLAY_BLOCK_SIZE and len < it, and
 *  at inblock in {0, 510, 511}.
 *
 *  THAT SPREAD IS NOT DECORATION.  An earlier version of this section had only
 *  inblock in {0,511} and len > 512, and TWO floor-clause-(d) mutants were
 *  MEASURED to survive it: `len > OVERLAY_BLOCK_SIZE ? remain : len` and
 *  `remain = inblock ? 1 : OVERLAY_BLOCK_SIZE`.  The short-unaligned row below
 *  reds on both.  The uncovered caller was real: bootblock_iso9660.c reads 256
 *  bytes at an offset snapped only to 2048.
 *
 *  They do NOT cover: the short-read path (no row forces a short fread; that
 *  debt is filed as `shortread`), or LAYER-SELECTION order (the fixture has one
 *  overlay, so there is no order to get wrong).
 *
 *  ORACLE = A COUNT, NOT A VALUE.  Base is all 'B', overlay data is all 'V',
 *  and the bitmap marks ONLY block 0.  A 1024-byte read from offset 511 covers
 *  offset 511 (block 0 -> overlay) and 512..1534 (blocks 1-2 -> base), so it
 *  must contain EXACTLY ONE 'V'.  A value-only oracle would be satisfied by
 *  reading the same byte twice; a count cannot be.
 */
/*  ------------------------------------------------------------------  */
/*  SECTION: a SHORT READ in a NON-FINAL iteration (row shortread)       */
/*
 *  THE DEFECT.  fread_helper() splits an overlayed read into
 *  OVERLAY_BLOCK_SIZE pieces.  When a piece comes up SHORT it advances by
 *  the REQUESTED length while accumulating the ACTUAL one:
 *
 *      len          -= lentoread;   <- requested
 *      totallenread += lenread;     <- actual
 *      buf          += lentoread;   <- requested
 *
 *  so the shortfall becomes a HOLE at the position where it happened, and
 *  every later iteration still lands at its correct final offset.  The
 *  caller then zero-fills the TAIL:
 *
 *      if (lendone >= 0 && lendone < (ssize_t)len)
 *              memset(buf + lendone, 0, len - lendone);
 *
 *  *** THAT ZERO-FILL IS CORRECT ONLY IF THE SHORTFALL WAS AT THE END. ***
 *  For a short read in a NON-FINAL iteration it is wrong twice over: the
 *  hole in the middle keeps whatever the caller buffer held, and the memset
 *  destroys an equal number of VALID bytes at the tail.  The access returns
 *  1, so nothing surfaces to the caller.
 *
 *  HOW THE SHORT READ IS PRODUCED -- a real construction, not an injected
 *  failure: diskimage_add_overlay() does NOT check the data file length
 *  against the image, and the bitmap alone decides which blocks are live.
 *  So an overlay whose .map claims block 0 while its data file is 200 bytes
 *  long is accepted silently, and reading block 0 returns 200.
 *
 *  *** AN EARLIER DRAFT OF THIS COMMENT SAID 'a host that ran out of space
 *  while writing an overlay leaves exactly this state'.  THAT IS FALSE, and a
 *  panel seat settled it by opening the function I had not: fwrite_helper()
 *  returns 0 on a short overlay write BEFORE calling
 *  overlay_set_block_in_use(), so the bitmap never claims the block and a
 *  later read takes the BASE. ***  GXemul's own writer cannot produce this
 *  state.  What can: a hand-made .map, a user-supplied V: overlay, truncation
 *  of an already-claimed overlay file, or a genuine read-side I/O error.
 *  R: cannot -- it starts empty+empty and unlinks both files.
 *
 *  ORACLE = TWO COUNTS AND A SENTINEL, NOT A VALUE.  The buffer is
 *  pre-filled with X.  A correct read of 1536 bytes at offset 0 leaves 200
 *  V (the overlay real bytes), 312 NUL (the unbacked remainder of block 0)
 *  and 1024 B (blocks 1-2 from base), and NO X anywhere.  The shipping code
 *  leaves 312 X in the middle and only 712 B, because the memset ate the
 *  last 312 of them.
 */
/*  Release a diskimage opened by this section: the overlay FILE handles are
    what matter, because ROW Z opens a SECOND overlay on the same struct and a
    leaked handle would make its bitmap read from the first one.  */
/*  IDEMPOTENT BY CONSTRUCTION, and that is the point rather than tidiness: this
    section opens SEVEN disks and a review seat found four of them unfreed.  A
    balancing pass that can double-free is worse than the leak -- I crashed the
    binary that way once in this round -- so the helper NULLs what it closes and
    a second call is a no-op.  */
static void altctl_shortread_free(struct diskimage *d)
{
	int k;
	for (k = 0; k < d->nr_of_overlays; k++) {
		if (d->overlays[k].f_data != NULL)
			fclose(d->overlays[k].f_data);
		if (d->overlays[k].f_bitmap != NULL)
			fclose(d->overlays[k].f_bitmap);
	}
	free(d->overlays);
	d->overlays = NULL;
	d->nr_of_overlays = 0;
	if (d->f != NULL)
		fclose(d->f);
	d->f = NULL;
}

/*
 *  ------------------------------------------------------------------
 *  CONTRACT (vacuity-floor clause (e)) -- WHAT THIS SECTION IS DESIGNED
 *  TO CATCH, and what it is NOT.  Stated so a later escape is either
 *  OUTSIDE the contract or a BREACH of it, rather than an argument about
 *  whether the round overclaimed.
 *
 *  IT CATCHES, each by a MEASURED kill recorded in the round block:
 *    * the defect itself, at three positions -- overlay layer / base
 *      layer / iteration 2 (the original rows, ROW L, ROW I);
 *    * reinstating the defect verbatim -- M1_revert, which reddens the
 *      original four rows AND ROW L, ROW I, ROW W and ROW T, because all
 *      four fire on the REAL defect and not only on their own mutants.
 *      ROW P, ROW U, ROW Z and ROW S do NOT: they are green pre-fix by
 *      design and are discharged by their mutants instead.  The pre-fix
 *      run (PREFIX_98rows.out, 18 failures) is the deriver;
 *    * weakening the fill's dominating predicate     (M2, M5_gtzero);
 *    * nulling the repair while keeping the guard   (M3_countonly);
 *    * swapping the memset's length or destination for another in-scope
 *      quantity            (M4_remain, M7_dst, M10, M12, M13);
 *    * narrowing the fill to the OVERLAY layer          (M8_layer);
 *    * narrowing the fill to the FIRST iteration    (M9_firstiter);
 *    * narrowing the fill to the first SHORT per call    (E3, ROW S);
 *    * narrowing the fill by a THRESHOLD on totallenread (E2, ROW S);
 *    * narrowing the fill by WRITABILITY                 (E1, ROW W);
 *    * narrowing the fill by disk TYPE                   (E4, ROW T).
 *
 *  *** THE FIRST THREE ARE STATED AT INSTANCE GRANULARITY ON PURPOSE. ***
 *  An earlier draft said 'narrowing by ITERATION' as a CLASS while listing
 *  a counter-instance of that same class two paragraphs down as NOT
 *  caught.  A contract written at class granularity and discharged by one
 *  instance each is an overclaim, and it contradicted itself in one
 *  comment.  Caught by a review seat on pass 2.
 *
 *  IT DOES NOT CATCH, and these are MEASURED escapes filed as coverage
 *  debt rather than hidden:
 *    * NOTHING, as of ROW S and ROW T.  Every escape either pass found is
 *      now killed -- E1 by ROW W, E4 by ROW T, and E2 AND E3 both by ROW S
 *      (`mutant_E{1,2,3,4}_*_98rows.out`, 2/3/3/2 failures).
 *
 *  ONE CLASS STAYS OPEN AND IS FILED, and it is a class rather than an
 *  escape: FITTED-THRESHOLD conjuncts.  ROW S kills `< 1024`'s instance,
 *  but `< 2048` would escape, and so on -- the ladder's limit is the fix
 *  itself, so NO FINITE ROW SET CLOSES IT and chasing it is the unbounded
 *  fix-of-fix shape.  Filed as a class, deliberately, not as a gap.
 *
 *  IT CANNOT CATCH, by construction rather than by omission: anything
 *  about REACHABILITY.  This is a rung-1 differential and every
 *  precondition in it is hand-built.  The round's reachability evidence
 *  is a separate rung-3 witness on unmodified landisk.
 *
 *  TWO MUTANTS ARE MEASURED **EQUIVALENT** and are recorded as results,
 *  not as gaps -- a mutant that will not die is a finding about the code:
 *    * `len - lenread` as the fill length: `buf + len` is invariant at the
 *      original request's end (buf rises by lentoread exactly as len
 *      falls by it), so it can never write past the request and only
 *      over-zeroes bytes later iterations rewrite.  0 differing cases in
 *      149,072.
 *    * `lenread < lentoread` for `!=`: fread cannot return more than
 *      requested.  0 differing cases in 149,072.
 */
static void section_short_read_midtransfer(void)
{
	char base[256], ovl[256], map[256];
	struct diskimage d;
	unsigned char buf[2048];
	FILE *f;
	size_t got;
	int i, nv, nb, nx, nz;

	snprintf(base, sizeof(base), "%s/shortread_base.img", WORK);
	snprintf(ovl,  sizeof(ovl),  "%s/shortread_ovl.img",  WORK);
	snprintf(map,  sizeof(map),  "%s/shortread_ovl.img.map", WORK);

	/*  Base image: 4096 bytes of B.  */
	mkfile(base, 4096, 'B');

	/*  Overlay DATA: TRUNCATED to 200 bytes of V.  This is the whole
	    construction -- the bitmap below claims a 512-byte block the file
	    cannot supply, and nothing in diskimage_add_overlay() objects.  */
	mkfile(ovl, 200, 'V');

	/*  Overlay BITMAP: 0x01 marks block 0 ONLY.  */
	f = fopen(map, "w+");
	if (f == NULL) { perror(map); exit(1); }
	fputc(0x01, f);
	fclose(f);

	mkdisk(&d, base, "r+", 1);
	if (!diskimage_add_overlay(&d, ovl, false)) {
		printf("  SETUP diskimage_add_overlay failed -- rows not run\n");
		return;
	}

	/*  [LIVE] The overlay is wired: an aligned read of block 0 returns the
	    200 bytes the file DOES have.  Without this a green defect row could
	    mean the overlay was never consulted at all.  */
	memset(buf, 'X', sizeof(buf));
	got = diskimage__internal_access(&d, 0, 0, buf, 512);
	for (i = 0, nv = 0; i < 512; i++)
		if (buf[i] == 'V') nv++;
	check("[LIVE] truncated overlay supplies its 200 real bytes", nv, 200);

	/*  [LIVE] ... and this shortfall is at the END of the read, which is the
	    case the caller tail memset was written for.  It is CORRECT here, and
	    that is exactly why the defect below is invisible in normal use.  */
	for (i = 0, nx = 0; i < 512; i++)
		if (buf[i] == 'X') nx++;
	check("[LIVE] a FINAL-iteration shortfall is zero-filled correctly", nx, 0);
	check("[LIVE] and it still reports success", (long long)got, 1);

	/*  [LIVE] The bitmap discriminates: block 1 comes from base.  Without
	    this, liveness 1 is satisfied by an overlay answering every block.  */
	memset(buf, 'X', sizeof(buf));
	(void) diskimage__internal_access(&d, 0, 512, buf, 512);
	for (i = 0, nb = 0; i < 512; i++)
		if (buf[i] == 'B') nb++;
	check("[LIVE] bitmap discriminates: block 1 is all base", nb, 512);

	/*  THE DEFECT.  1536 bytes at offset 0 crosses THREE blocks: block 0 from
	    the truncated overlay (200 of 512 bytes available), then blocks 1-2
	    from base.  The shortfall is now in the FIRST of three iterations.  */
	memset(buf, 'X', sizeof(buf));
	got = diskimage__internal_access(&d, 0, 0, buf, 1536);

	for (i = 0, nx = 0; i < 1536; i++)
		if (buf[i] == 'X') nx++;
	check("short read: caller bytes the read never wrote", nx, 0);

	for (i = 0, nb = 0; i < 1536; i++)
		if (buf[i] == 'B') nb++;
	check("short read: base bytes surviving the tail zero-fill", nb, 1024);

	/*  The two above are the SAME defect counted at its two ends, and both
	    are kept on purpose: a fix that only stops the loop early greens the
	    first and leaves the second at 712.  */
	for (i = 0, nv = 0; i < 1536; i++)
		if (buf[i] == 'V') nv++;
	check("short read: overlay bytes are the 200 that exist", nv, 200);

	for (i = 0, nz = 0; i < 1536; i++)
		if (buf[i] == 0) nz++;
	check("short read: NUL fill covers exactly the unbacked hole", nz, 312);

	/*  [CONTROL] The access reports SUCCESS either way.  This row does not
	    change under the fix and is here to record that nothing surfaces --
	    the fatal() inside fread_helper() prints, but the return value is 1
	    and the guest sees a completed read.  */
	check("short read: reports success either way [CONTROL]", (long long)got, 1);

	/*  [ANCHOR] Position, not just population.  The four counts above are
	    invariant under any permutation of the buffer, so they cannot tell a
	    hole at 200 from a hole at 1224.  These pin WHERE each region is,
	    which is what makes the section absolute rather than relative.  */
	check("[ANCHOR] byte 199 is the last real overlay byte", buf[199], 'V');
	check("[ANCHOR] byte 200 is the first unbacked byte", buf[200], 0);
	check("[ANCHOR] byte 512 is the first base byte", buf[512], 'B');
	check("[ANCHOR] byte 1535 is still a base byte", buf[1535], 'B');


	/*  ROW P -- THE FILL IS BOUNDED BY THE REQUEST, NOT BY THE BLOCK.

	    *** EVERY ROW ABOVE IS BLIND TO `lentoread - lenread` -> `remain -
	    lenread` BY CONSTRUCTION: every iteration above starts at an ALIGNED
	    offset, so inblock == 0, remain == 512 == lentoread, and the two
	    expressions are THE SAME NUMBER. ***  An EQUIVALENT mutant over the
	    probed set.  Found by two panel seats on pass 1 against a table that
	    was otherwise clean.

	    A PARTIAL-BLOCK request separates them.  300 bytes at offset 0 from
	    a 200-byte overlay:

	        inblock = 0   remain = 512   len = 300   lentoread = 300
	        lenread = 200 (the file has no more)

	        correct   memset(buf + 200, 0, 300 - 200) = 100  -> stops at 300
	        mutant    memset(buf + 200, 0, 512 - 200) = 312  -> runs to 512

	    so the mutant writes 212 bytes PAST THE END OF THE REQUEST.  That is
	    an overrun of the caller's buffer, not a mis-count, which is why the
	    oracle is THE SENTINEL SURVIVING past byte 300 rather than a total.  */
	memset(buf, 'X', sizeof(buf));
	got = diskimage__internal_access(&d, 0, 0, buf, 300);

	for (i = 300, nx = 0; i < 512; i++)
		if (buf[i] == 'X') nx++;
	check("ROW P partial block: sentinel past the request untouched", nx, 212);

	for (i = 0, nv = 0; i < 300; i++)
		if (buf[i] == 'V') nv++;
	check("ROW P partial block: the 200 real overlay bytes arrive", nv, 200);

	for (i = 200, nz = 0; i < 300; i++)
		if (buf[i] == 0) nz++;
	check("ROW P partial block: shortfall inside the request filled", nz, 100);
	check("ROW P partial block: reports success [CONTROL]", (long long)got, 1);

	/*  ROW U -- THE SAME SEPARATION BY OFFSET, WHICH IS THE STRONGER FORM.
	    ROW P has inblock == 0; here inblock != 0, so `remain` and
	    `lentoread` differ for a SECOND independent reason and a mutant that
	    survives one cannot survive both.  50 bytes at offset 150:

	        inblock = 150   remain = 362   len = 50   lentoread = 50
	        lenread = 50 of the overlay's first 200 bytes -> NOT short

	    ... so the short case needs the read to start inside the backed
	    region and run past it: 100 bytes at offset 150 gives lenread = 50
	    (bytes 150..199 exist, 200..249 do not).

	        correct   memset(buf + 50, 0, 100 - 50)  = 50  -> stops at 100
	        mutant    memset(buf + 50, 0, 362 - 50)  = 312 -> runs to 362  */
	memset(buf, 'X', sizeof(buf));
	got = diskimage__internal_access(&d, 0, 150, buf, 100);

	for (i = 100, nx = 0; i < 512; i++)
		if (buf[i] == 'X') nx++;
	check("ROW U unaligned: sentinel past the request untouched", nx, 412);

	for (i = 0, nv = 0; i < 100; i++)
		if (buf[i] == 'V') nv++;
	check("ROW U unaligned: the 50 backed bytes arrive", nv, 50);

	for (i = 50, nz = 0; i < 100; i++)
		if (buf[i] == 0) nz++;
	check("ROW U unaligned: the unbacked 50 are filled", nz, 50);
	check("ROW U unaligned: reports success [CONTROL]", (long long)got, 1);

	altctl_shortread_free(&d);

	/*  ROW Z -- AN EMPTY OVERLAY, WHICH IS THE ONLY WAY TO REACH lenread == 0.

	    *** THIS ROW IS GREEN BEFORE THE FIX AND AFTER IT, AND THAT IS
	    CORRECT. ***  A whole-read shortfall IS a final-iteration shortfall,
	    so the caller's tail memset already covers it.  The row exists to
	    REDDEN under `if (lenread != lentoread)` -> `if (lenread > 0)`, which
	    every other row in this file passes: on a full block lenread ==
	    lentoread and memset(...,0,0) is a no-op, and on the short blocks
	    above lenread is 200 or 50, both > 0.

	    An accept-side row is not discharged by EXISTING -- it is discharged
	    by a MEASURED KILL, and this one's kill is recorded in the round's
	    mutant table.  */
	snprintf(ovl,  sizeof(ovl),  "%s/shortread_empty.img",  WORK);
	snprintf(map,  sizeof(map),  "%s/shortread_empty.img.map", WORK);
	mkfile(ovl, 0, 'V');
	f = fopen(map, "w+");
	if (f == NULL) { perror(map); exit(1); }
	fputc(0x01, f);
	fclose(f);

	altctl_shortread_free(&d);
	mkdisk(&d, base, "r+", 1);
	if (!diskimage_add_overlay(&d, ovl, false)) {
		printf("  SETUP empty overlay failed -- ROW Z not run\n");
		return;
	}
	memset(buf, 'X', sizeof(buf));
	got = diskimage__internal_access(&d, 0, 0, buf, 512);
	for (i = 0, nz = 0; i < 512; i++)
		if (buf[i] == 0) nz++;
	check("ROW Z empty overlay: all 512 bytes are zero-filled", nz, 512);
	check("ROW Z empty overlay: reports success [CONTROL]", (long long)got, 1);

	/*  ROW L -- A SHORT ON THE **BASE** LAYER.

	    *** EVERY ROW ABOVE SHORTS ON THE OVERLAY, so `&& overlay_nr >= 0`
	    on the fill is invisible to all of them. ***  One conjunct, and it
	    reads like a plausible narrowing -- 'we only meant to handle the
	    overlay case'.  Found by a panel seat on pass 1.

	    Base TRUNCATED to 300 bytes; overlay claims block 1 ONLY (map 0x02).
	    A 1024-byte read at 0 then shorts on the BASE in iteration 1 and
	    succeeds on the OVERLAY in iteration 2:

	        correct   300 B, 212 NUL, 512 V
	        mutant    300 B, 212 SENTINEL, 512 V   (no fill: base layer)  */
	snprintf(base, sizeof(base), "%s/shortread_basetrunc.img", WORK);
	snprintf(ovl,  sizeof(ovl),  "%s/shortread_ovlfull.img",  WORK);
	snprintf(map,  sizeof(map),  "%s/shortread_ovlfull.img.map", WORK);
	mkfile(base, 300, 'B');
	mkfile(ovl, 4096, 'V');
	f = fopen(map, "w+");
	if (f == NULL) { perror(map); exit(1); }
	fputc(0x02, f);	/*  block 1 ONLY  */
	fclose(f);
	altctl_shortread_free(&d);
	mkdisk(&d, base, "r+", 1);
	if (!diskimage_add_overlay(&d, ovl, false)) {
		printf("  SETUP base-truncated overlay failed -- ROW L not run\n");
		return;
	}
	memset(buf, 'X', sizeof(buf));
	got = diskimage__internal_access(&d, 0, 0, buf, 1024);
	for (i = 0, nx = 0; i < 1024; i++)
		if (buf[i] == 'X') nx++;
	check("ROW L base-layer short: no sentinel survives", nx, 0);
	for (i = 0, nv = 0; i < 1024; i++)
		if (buf[i] == 'V') nv++;
	check("ROW L base-layer short: the later overlay block arrives", nv, 512);
	check("[ANCHOR] ROW L byte 300 is the first unbacked byte", buf[300], 0);
	check("[ANCHOR] ROW L byte 512 is the first overlay byte", buf[512], 'V');
	altctl_shortread_free(&d);

	/*  ROW I -- A SHORT IN ITERATION **2**.

	    *** EVERY ROW ABOVE SHORTS IN ITERATION 1, so `&& totallenread == 0`
	    -- or the equivalent `&& curofs == offset` -- is invisible to all of
	    them. ***  The other one-conjunct narrowing the seat named.

	    Overlay data 700 bytes, bitmap claims blocks 0 AND 1 (map 0x03).
	    A 1536-byte read at 0: block 0 reads its full 512, block 1 gets only
	    the remaining 188, block 2 comes from base.

	        correct   700 V, 324 NUL, 512 B
	        mutant    700 V, 324 SENTINEL, 512 B  (no fill: not iteration 1)  */
	snprintf(base, sizeof(base), "%s/shortread_base.img", WORK);
	snprintf(ovl,  sizeof(ovl),  "%s/shortread_ovl700.img",  WORK);
	snprintf(map,  sizeof(map),  "%s/shortread_ovl700.img.map", WORK);
	mkfile(base, 4096, 'B');
	mkfile(ovl, 700, 'V');
	f = fopen(map, "w+");
	if (f == NULL) { perror(map); exit(1); }
	fputc(0x03, f);	/*  blocks 0 AND 1  */
	fclose(f);
	altctl_shortread_free(&d);
	mkdisk(&d, base, "r+", 1);
	if (!diskimage_add_overlay(&d, ovl, false)) {
		printf("  SETUP 700-byte overlay failed -- ROW I not run\n");
		return;
	}
	memset(buf, 'X', sizeof(buf));
	got = diskimage__internal_access(&d, 0, 0, buf, 1536);
	for (i = 0, nx = 0; i < 1536; i++)
		if (buf[i] == 'X') nx++;
	check("ROW I short in iteration 2: no sentinel survives", nx, 0);
	for (i = 0, nv = 0; i < 1536; i++)
		if (buf[i] == 'V') nv++;
	check("ROW I short in iteration 2: all 700 overlay bytes arrive", nv, 700);
	for (i = 0, nb = 0; i < 1536; i++)
		if (buf[i] == 'B') nb++;
	check("ROW I short in iteration 2: the later base block arrives", nb, 512);
	check("[ANCHOR] ROW I byte 700 is the first unbacked byte", buf[700], 0);
	check("[ANCHOR] ROW I byte 1024 is the first base byte", buf[1024], 'B');
	check("ROW I short in iteration 2: reports success [CONTROL]", (long long)got, 1);

	/*  ROW W -- A READ-ONLY DISK, and it is the one row taken from the
	    capped ask-again.

	    *** ADDING THE SINGLE CONJUNCT `&& d->writable` TO THE FILL GUARD
	    PASSES ALL 86 ROWS ABOVE **AND** ALL 149,072 CASES OF AN
	    EQUIVALENCE SWEEP. ***  The sweep is not weak -- it varied base
	    size, overlay size, bitmap, offset and length, and it caught its
	    two controls at 69,880 and 9,686 differing cases.  It is blind
	    because NEITHER IT NOR ANY ROW EVER OPENS A DISK WITH
	    d->writable == 0.

	    Writability is not a length, an offset or a layer, so no amount of
	    sweeping those three could ever reach it.  That is this round's own
	    finding -- the fixture varies one dimension and the mutant lives in
	    another -- turned on the instrument built to enforce it.

	    Same truncated overlay, same 1536-byte read, one changed argument:
	    the disk is opened NOT writable.  Under the mutant the fill is
	    skipped and the 312 stale sentinel bytes come back.  */
	snprintf(base, sizeof(base), "%s/shortread_ro_base.img", WORK);
	snprintf(ovl,  sizeof(ovl),  "%s/shortread_ro_ovl.img",  WORK);
	snprintf(map,  sizeof(map),  "%s/shortread_ro_ovl.img.map", WORK);
	mkfile(base, 4096, 'B');
	mkfile(ovl, 200, 'V');
	f = fopen(map, "w+");
	if (f == NULL) { perror(map); exit(1); }
	fputc(0x01, f);
	fclose(f);

	/*  the ONE changed argument: mode "r" and writable 0  */
	altctl_shortread_free(&d);
	mkdisk(&d, base, "r", 0);
	if (!diskimage_add_overlay(&d, ovl, false)) {
		printf("  SETUP read-only overlay failed -- ROW W not run\n");
		return;
	}
	memset(buf, 'X', sizeof(buf));
	got = diskimage__internal_access(&d, 0, 0, buf, 1536);

	for (i = 0, nx = 0; i < 1536; i++)
		if (buf[i] == 'X') nx++;
	check("ROW W read-only disk: no sentinel survives", nx, 0);

	for (i = 0, nb = 0; i < 1536; i++)
		if (buf[i] == 'B') nb++;
	check("ROW W read-only disk: all base bytes survive", nb, 1024);

	/*  [LIVE] the disk really is read-only -- without this the row could go
	    green because the mode argument was ignored.  */
	check("[LIVE] ROW W the disk is not writable", d.writable, 0);
	check("[ANCHOR] ROW W byte 200 is the first unbacked byte", buf[200], 0);


	/*  ROW T -- AN IDE-TYPED DISK, and it is the sharpest of the three
	    unvaried-field escapes because of WHERE its mutant fires.

	    *** `&& d->type == DISKIMAGE_SCSI` ON THE FILL GUARD PASSES EVERY
	    ROW IN THIS FILE AND ALL 149,072 SWEEP CASES, because mkdisk()
	    hardcodes DISKIMAGE_SCSI and nothing ever varies it. ***

	    That much it shares with the two escapes this round FILED.  What
	    it does not share is its target: wdc__read() looks up
	    DISKIMAGE_IDE, and landisk's default disk type is IDE -- so this
	    conjunct RE-OPENS THE DEFECT ON THE ONLY GUEST PATH THE ROUND
	    ACTUALLY DROVE.  The rung-3 witness would go red while every row
	    here stayed green.  The two filed escapes do not do that; both
	    still fill on the 3-sector witness read, which shorts once in
	    iteration 1.

	    Found by a review seat on pass 2 and taken under L1 (pre-ship
	    construction), NOT under the ask-again, whose cap was already
	    spent.  Same truncated overlay, same 1536-byte read; the one
	    changed thing is the disk's TYPE.

	    Scope, so the row is not read as covering more than it does:
	    `&& d->id == 0` and `&& d->logical_block_size == 512` are the same
	    unvaried-field class but would still fill for landisk drive 0 at
	    512, so they do not re-open the witnessed path.  And
	    `&& !d->is_a_cdrom` is NOT this class -- internal_access never
	    reaches fread_helper with is_a_cdrom set, so it is EQUIVALENT
	    inside this function.  */
	snprintf(base, sizeof(base), "%s/shortread_ide_base.img", WORK);
	snprintf(ovl,  sizeof(ovl),  "%s/shortread_ide_ovl.img",  WORK);
	snprintf(map,  sizeof(map),  "%s/shortread_ide_ovl.img.map", WORK);
	mkfile(base, 4096, 'B');
	mkfile(ovl, 200, 'V');
	f = fopen(map, "w+");
	if (f == NULL) { perror(map); exit(1); }
	fputc(0x01, f);
	fclose(f);
	altctl_shortread_free(&d);
	mkdisk(&d, base, "r+", 1);
	d.type = DISKIMAGE_IDE;	/*  the ONE changed field  */
	if (!diskimage_add_overlay(&d, ovl, false)) {
		printf("  SETUP IDE overlay failed -- ROW T not run\n");
		return;
	}
	memset(buf, 'X', sizeof(buf));
	got = diskimage__internal_access(&d, 0, 0, buf, 1536);

	for (i = 0, nx = 0; i < 1536; i++)
		if (buf[i] == 'X') nx++;
	check("ROW T IDE-typed disk: no sentinel survives", nx, 0);

	for (i = 0, nb = 0; i < 1536; i++)
		if (buf[i] == 'B') nb++;
	check("ROW T IDE-typed disk: all base bytes survive", nb, 1024);

	/*  [LIVE] the type really is IDE -- without this the row could go green
	    because the assignment was optimised away or overwritten.  */
	check("[LIVE] ROW T the disk type is IDE", d.type, DISKIMAGE_IDE);
	check("[ANCHOR] ROW T byte 200 is the first unbacked byte", buf[200], 0);


	/*  ROW S -- TWO SHORTS IN ONE CALL, and it closes both of the escapes
	    this round would otherwise have filed.

	    Overlay data 200 bytes, bitmap 0x05 (blocks 0 AND 2), read 1536 at 0:

	      iter 1  block 0 -> overlay, 200 of 512                  SHORT #1
	      iter 2  block 1 -> base (bit 1 clear), 512 of 512       full
	      iter 3  block 2 -> overlay, seek 1024 into a 200-byte
	                         file, so lenread == 0                SHORT #2

	    Correct: 200 V, 312 NUL, 512 B, 512 NUL.

	    *** IT KILLS BOTH. ***  Under 'fill only the first short per call'
	    the second short is never filled -- 512 stale bytes.  Under
	    `&& totallenread < 1024` iteration 3 arrives with totallenread
	    exactly 1024, so the conjunct is false and the fill is skipped --
	    the same 512 stale bytes.

	    The reason for taking it rather than filing it is not tidiness: this
	    fatal() is unlatched and guest-floodable, the house idiom for such a
	    site is latch-plus-fatal, and THE NATURAL BAD LATCH EDIT BRACES THIS
	    MEMSET IN WITH THE FATAL -- which is precisely the first-short-only
	    shape.  It is the most plausible future edit in the round.

	    What it does NOT do is close the fitted-threshold CLASS.  Kill
	    `< 1024` with this row and `< 2048` escapes; no finite row set closes
	    that ladder, and chasing it is the unbounded-fix-chain shape.  This
	    row closes that escape's INSTANCE, and the class stays filed.  */
	snprintf(base, sizeof(base), "%s/shortread_two_base.img", WORK);
	snprintf(ovl,  sizeof(ovl),  "%s/shortread_two_ovl.img",  WORK);
	snprintf(map,  sizeof(map),  "%s/shortread_two_ovl.img.map", WORK);
	mkfile(base, 4096, 'B');
	mkfile(ovl, 200, 'V');
	f = fopen(map, "w+");
	if (f == NULL) { perror(map); exit(1); }
	fputc(0x05, f);	/*  blocks 0 AND 2, block 1 from base  */
	fclose(f);
	altctl_shortread_free(&d);
	mkdisk(&d, base, "r+", 1);
	if (!diskimage_add_overlay(&d, ovl, false)) {
		printf("  SETUP two-short overlay failed -- ROW S not run\n");
		return;
	}
	memset(buf, 'X', sizeof(buf));
	got = diskimage__internal_access(&d, 0, 0, buf, 1536);

	for (i = 0, nx = 0; i < 1536; i++)
		if (buf[i] == 'X') nx++;
	check("ROW S two shorts in one call: no sentinel survives", nx, 0);

	for (i = 0, nb = 0; i < 1536; i++)
		if (buf[i] == 'B') nb++;
	check("ROW S two shorts: the middle base block arrives", nb, 512);

	/*  [ANCHOR] the SECOND hole specifically -- a population count cannot
	    tell a hole at 1024 from one at 200, and both mutants leave the
	    second one only.  */
	check("[ANCHOR] ROW S byte 1024 is in the SECOND unbacked hole", buf[1024], 0);
	check("[ANCHOR] ROW S byte 1535 is the last unbacked byte", buf[1535], 0);
	altctl_shortread_free(&d);
}

static void section_overlay_unaligned(void)
{
	char base[256], ovl[256], map[256];
	struct diskimage d;
	/*  buf is 2048 for a 1024-byte read ON PURPOSE, and it is load-bearing:
	    under the clamp-only mutant the loop writes as far as buf[1534], so that
	    mutant is a CALLER-BUFFER OVERFLOW of up to 511 bytes, not merely holes.
	    A tight buffer here would turn a measurable row into a smashed stack.  */
	unsigned char buf[2048];
	FILE *f;
	size_t got;
	int i, nv, nb;

	snprintf(base, sizeof(base), "%s/b115_base.img", WORK);
	snprintf(ovl,  sizeof(ovl),  "%s/b115_ovl.img",  WORK);
	snprintf(map,  sizeof(map),  "%s/b115_ovl.img.map", WORK);

	/*  Base image: 4096 bytes of 'B'.  */
	f = fopen(base, "w+");
	if (f == NULL) { perror(base); exit(1); }
	for (i = 0; i < 4096; i++)
		fputc('B', f);
	fclose(f);

	/*  Overlay DATA: 4096 bytes of 'V'.  A real overlay file is full-size;
	    the bitmap, not the file length, says which blocks are live.  */
	f = fopen(ovl, "w+");
	if (f == NULL) { perror(ovl); exit(1); }
	for (i = 0; i < 4096; i++)
		fputc('V', f);
	fclose(f);

	/*  Overlay BITMAP: one bit per OVERLAY_BLOCK_SIZE block, LSB first.
	    0x01 marks block 0 ONLY -- so every other block must come from base.  */
	f = fopen(map, "w+");
	if (f == NULL) { perror(map); exit(1); }
	fputc(0x01, f);
	fclose(f);

	mkdisk(&d, base, "r+", 1);
	if (!diskimage_add_overlay(&d, ovl, false)) {
		printf("  SETUP diskimage_add_overlay failed -- rows not run\n");
		return;
	}

	/*  LIVENESS 1: an ALIGNED read of block 0 must be all overlay.  Without
	    this a green defect row could mean "the overlay was never wired".  */
	memset(buf, 0, sizeof(buf));
	got = diskimage__internal_access(&d, 0, 0, buf, 512);
	for (i = 0, nv = 0; i < 512; i++)
		if (buf[i] == 'V') nv++;
	check("[LIVE] aligned read of block 0 is all overlay", nv, 512);
	check("[LIVE] aligned read of block 0 reports success", (long long)got, 1);

	/*  LIVENESS 2: an ALIGNED read of block 1 must be all base.  This is what
	    proves the BITMAP discriminates rather than the overlay swallowing
	    everything -- without it, liveness 1 alone is satisfied by an overlay
	    that answers every block.  */
	memset(buf, 0, sizeof(buf));
	got = diskimage__internal_access(&d, 0, 512, buf, 512);
	for (i = 0, nb = 0; i < 512; i++)
		if (buf[i] == 'B') nb++;
	check("[LIVE] aligned read of block 1 is all base", nb, 512);

	/*  THE DEFECT.  1024 bytes from offset 511: offset 511 is block 0 (overlay),
	    512..1534 are blocks 1-2 (base).  Exactly ONE 'V' is correct.  The
	    unclamped read takes 512 bytes of overlay starting at 511, so it yields
	    512.  */
	memset(buf, 0, sizeof(buf));
	got = diskimage__internal_access(&d, 0, 511, buf, 1024);
	for (i = 0, nv = 0; i < 1024; i++)
		if (buf[i] == 'V') nv++;
	check("overlay unaligned: wrong-layer bytes in 1024 @ 511", nv, 1);

	/*  AND NO ERROR SURFACES.  diskimage__internal_access() documents its return
	    as "1 if the access completed successfully, 0 otherwise" -- see the header
	    comment on diskimage__internal_access() (cited by CONSTRUCT, not line:
	    that sentence moved +14 when this round inserted its own comment, and it
	    occurs TWICE in the file, so no line number is both stable and unique)
	    -- NOT a byte count, which an earlier draft of these rows assumed and was
	    corrected by the measurement.  It reports SUCCESS while handing back
	    wrong-layer bytes, which is exactly why this corrupts silently.  Pinned so
	    a fix that starts reporting failure here is noticed too.  */
	check("overlay unaligned: reports SUCCESS despite corruption", (long long)got, 1);

	/*  THE HALF-FIX ROW, and pass 1 is why it exists.  Two seats independently named
	    the same surviving mutant: apply the lentoread clamp and KEEP
	    `buf += OVERLAY_BLOCK_SIZE`.  Someone fixes the length and never notices the
	    stride.

	    IT ESCAPES EVERY ROW ABOVE.  Under it, iteration 1 reads ONE byte into buf[0]
	    and then advances buf by a whole block, so buf[1..511] are never written --
	    and the 'V' count reads 1, which is the CORRECT answer.  The buffer does not
	    receive wrong bytes; it receives HOLES.

	    So this row counts bytes the read never wrote.  The buffer was memset to 0
	    and neither 'B' nor 'V' is 0, so an untouched byte is unambiguous.  */
	for (i = 0, nb = 0; i < 1024; i++)
		if (buf[i] == 0) nb++;
	check("overlay unaligned: bytes the read never wrote", nb, 0);

	/*  THE SHORT-UNALIGNED ROW.  FLOOR CLAUSE (d): the fix INTRODUCES the
	    predicate `len > remain`, and clause (d) says weaken it to the
	    least-restrictive form that still READS like the same check.  Two were
	    found, and BOTH pass every row above:

	      len > OVERLAY_BLOCK_SIZE ? remain : len   (bound relaxed)
	      remain = inblock ? 1 : OVERLAY_BLOCK_SIZE (remainder faked)

	    They survive because the rows above only ever produce inblock in {0,511}
	    and len > 512.  This row breaks both assumptions at once: an unaligned
	    offset with a SHORT length that still crosses a block boundary.

	    THE CALLER IS REAL, not hypothetical: bootblock_iso9660.c:281-282 reads
	    256 bytes at a dirofs snapped only to 2048 (:275-276), i.e. arbitrary
	    mod 512.  This round's own census had already named that arm.

	    510..511 are block 0 (overlay); 512 is block 1 (base).  Exactly TWO
	    overlay bytes is correct.  pristine and the relaxed-bound mutant both
	    yield 3; the faked-remainder mutant yields 1.  */
	memset(buf, 0, sizeof(buf));
	got = diskimage__internal_access(&d, 0, 510, buf, 3);
	for (i = 0, nv = 0; i < 3; i++)
		if (buf[i] == 'V') nv++;
	check("overlay short-unaligned: 510+3 crosses into base", nv, 2);

	fclose(d.f);
	fclose(d.overlays[0].f_data);
	fclose(d.overlays[0].f_bitmap);
	free(d.overlays);
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

	{
		/*
		 *  SELFCHECK -- CAN THIS FILE'S COMPARATOR STILL FAIL?
		 *
		 *  Feed check() deliberate mismatches and require the failure counter to
		 *  move, then un-record them so the rows are free.  If check() has been
		 *  stubbed, neutered, or had its comparison edited away, EVERY other row in
		 *  this file is silently inert and the gate cannot tell -- the row count, the
		 *  identity row and the verdict token all survive that edit unchanged.
		 *  MEASURED once, on the five detectors that already carry this block: 118
		 *  rows stayed green under exactly that stub.  diff_timer.c holds the full
		 *  rationale and the four measurements behind this shape; it is not repeated
		 *  here.
		 *
		 *  ONE TYPE, TWO MAGNITUDES -- AND THE SECOND PROBE IS NOT PADDING.  timer's
		 *  sentinel needs a string probe AND a numeric one because its check() takes
		 *  strings and a seat defeated a string-only probe with `isdigit(got[0])`.
		 *  check() here takes long long, so a string probe cannot be written at all;
		 *  the two probes instead straddle the 32-bit boundary.  2^32 and 0 are EQUAL
		 *  in their low 32 bits, so a comparator narrowed to int -- the plausible
		 *  good-faith edit in a file whose rows compare 64-bit block counts and byte
		 *  offsets -- passes that probe while the small pair still catches it.  A
		 *  sentinel whose inputs do not resemble the rows it vouches for is a sentinel
		 *  with a whitelist.
		 *
		 *  This does NOT prove any row is correct.  It proves the comparator still
		 *  fails on inputs shaped like the ones the rows use.  A comparator that
		 *  compares SELECTIVELY -- or that special-cases these rows BY NAME -- is
		 *  still invisible to it, and only a census would see that.
		 *
		 *  @@SELFCHECK@@ IN THE ROW NAMES IS LOAD-BEARING.  These are deliberate
		 *  mismatches, so check() prints FAIL for them on the HEALTHY path;
		 *  selfmutant.py filters exactly that token when it looks for the row its
		 *  mutant killed, and without it a row id as ordinary as "fail" matches one of
		 *  these lines and reports OK for a mutant nothing caught.  gate_offline.sh
		 *  greps the SUMMARY line below for presence.
		 */
		int sc_f = failures, sc_r = rows, sc_bad = 0;

		check("@@SELFCHECK@@/small", 1, 2);
		if (failures <= sc_f)
			sc_bad++;
		failures = sc_f; rows = sc_r;

		check("@@SELFCHECK@@/wide", 4294967296LL, 0);
		if (failures <= sc_f)
			sc_bad++;
		failures = sc_f; rows = sc_r;

		if (sc_bad) {
			printf("  FAIL  SELFCHECK the comparator no longer compares (%d of 2 "
			    "mismatches went unnoticed) -- every row in this file is inert\n",
			    sc_bad);
			failures = sc_f + 1;
			rows = sc_r;
		} else {
			printf("  ok    SELFCHECK the comparator can still fail       "
			    "small+wide\n");
		}
	}

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
	section_overlay_unaligned();
	section_short_read_midtransfer();
	section_pass2_gaps();
	section_real_images();

	/*
	 *  IDENTITY GUARD.  Two files with this name once differed only by the
	 *  case of a parent directory, and the stale one encoded a REVERSED
	 *  design decision.  A row count is the cheapest proof that the file
	 *  which ran is the file that was reviewed.  Last, so it counts every
	 *  row above it.
	 */
	check("[IDENTITY] row count -- guards against a stale copy", rows + 1, 98);

	printf("\n%d rows, %d failures, %d faults\n", rows, failures, faults);
	printf("%s\n", (failures == 0 && faults == 0) ?
	    "DISKIMAGE_IO_PASS" : "DISKIMAGE_IO_FAIL");
	return 0;
}
