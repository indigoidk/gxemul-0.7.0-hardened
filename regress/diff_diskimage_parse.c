/*
 *  #418: offline differential of the `-d` PREFIX PARSER in diskimage_add().
 *
 *  No emulator binary, no guest, no rig.  Every row asserts diskimage_add()'s
 *  OUTPUT: d->type, the advertised block count, and diskimage_exist() under the
 *  type a controller ACTUALLY asks for -- which is the only thing that decides
 *  whether a guest can see the disk at all.
 *
 *  THE DEFECT THIS PINS.  `d:` is documented as the escape hatch ("d: DISK
 *  (this is the default)"; "the default for disks can be either SCSI or IDE"),
 *  but nothing acted on it, so a floppy-sized image stayed DISKIMAGE_FLOPPY --
 *  a type NO controller ever passes.  Every diskimage_scsicommand() call site
 *  hard-codes DISKIMAGE_SCSI (six) or DISKIMAGE_IDE (one, the ATAPI path), and
 *  both selectors match on d->type == type, so the guest got no disk at all.
 *
 *  *** WHAT THESE ROWS DO NOT COVER, stated rather than implied: ***
 *  They assert the PARSER's output.  If a later round taught dev_asc.c to also
 *  accept DISKIMAGE_FLOPPY, every row here would stay green while the
 *  reachability story flipped completely.  That needs a call-site row or a
 *  booting rig; it cannot be caught offline.  Section A row 3 is the closest
 *  available proxy and is why it exists.
 *
 *  Build (the section flags are LOAD-BEARING -- diskimage.c defines functions
 *  this file neither calls nor stubs, and the link fails without --gc-sections):
 *	cc -ffunction-sections -fdata-sections -Wl,--gc-sections \
 *	   -I<tree> -I<tree>/src/include diff_diskimage_parse.c -o t && ./t
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/stat.h>

static int quiet_stubs = 1;

/*
 *  debug_indentation and mymkstemp are NOT reachable from diskimage_add()
 *  alone -- they come in via diskimage_dump_info() and the 'R' overlay path.
 *  They are stubbed anyway because --gc-sections runs after the link decides
 *  it needs them; both facts were established by compiling, not by reading.
 */
void fatal(const char *fmt, ...)
{ va_list ap; if (quiet_stubs) return; va_start(ap,fmt); vfprintf(stderr,fmt,ap); va_end(ap); }

void debug(const char *fmt, ...)
{ va_list ap; if (quiet_stubs) return; va_start(ap,fmt); vfprintf(stderr,fmt,ap); va_end(ap); }

void debug_indentation(int diff) { (void)diff; }

int mymkstemp(char *templ) { return mkstemp(templ); }

#include "../src/disk/diskimage.c"

void debugmsg_cpu(struct cpu* cpu, int subsystem, const char *name,
	int verbosity_required, const char *fmt, ...)
{ va_list ap; (void)cpu; if (quiet_stubs) return; va_start(ap,fmt); vfprintf(stderr,fmt,ap); va_end(ap); fprintf(stderr,"\n"); }

void debugmsg(int subsystem, const char *name, int verbosity_required,
	const char *fmt, ...)
{ va_list ap; if (quiet_stubs) return; va_start(ap,fmt); vfprintf(stderr,fmt,ap); va_end(ap); fprintf(stderr,"\n"); }

/*  ---------------------------------------------------------------- */

static int failures = 0, rows = 0;

static void check(const char *rowname, long long got, long long want)
{
	rows++;
	if (got == want) printf("  ok    %-56s = %lld\n", rowname, got);
	else { failures++; printf("  FAIL  %-56s = %lld, want %lld\n", rowname, got, want); }
}

static const char *WORK = "/tmp/r418parse";

static void mkfile(const char *path, long long len)
{
	FILE *f = fopen(path, "w+");
	if (!f) { perror(path); exit(1); }
	if (len > 0) { fseek(f, len-1, SEEK_SET); fputc(0, f); }
	fclose(f);
}

/*  Parse one -d argument on a fresh machine, return the resulting disk.  */
static struct diskimage *add1(struct machine *m, int machine_type, char *arg)
{
	memset(m, 0, sizeof(*m));
	m->machine_type = machine_type;
	if (diskimage_add(m, arg) < 0) return NULL;
	return m->first_diskimage;
}

int main(void)
{
	struct machine m;
	struct diskimage *d;
	char path[512], arg[600];
	char cmd[600];
	int i, counted;
	/*  The four sizes the heuristic's floppy arm is written for.  One row
	    per size: deleting a single arm is otherwise invisible.  */
	static const long long sizes[4] = { 737280, 1228800, 1474560, 2949120 };
	static const char *names[4] = { "720K", "1.2M", "1.44M", "2.88M" };

	snprintf(cmd, sizeof(cmd), "mkdir -p %s", WORK); if (system(cmd)) {}

	printf("--- A. no-prefix CONTROL: the size heuristic must survive ---\n");
	for (i = 0; i < 4; i++) {
		snprintf(path, sizeof(path), "%s/fl%d.img", WORK, i);
		mkfile(path, sizes[i]);
		snprintf(arg, sizeof(arg), "%s", path);
		d = add1(&m, MACHINE_PMAX, arg);
		snprintf(cmd, sizeof(cmd), "[CONTROL] no prefix %s -> FLOPPY", names[i]);
		check(cmd, d ? d->type : -1, DISKIMAGE_FLOPPY);
		snprintf(cmd, sizeof(cmd), "[CONTROL] no prefix %s blocks exact", names[i]);
		check(cmd, d ? d->nr_of_logical_blocks : -1, sizes[i]/512);
		/*
		 *  #418: THE DEFECT ITSELF, and it is deliberately still red-free
		 *  because this round does NOT fix it.  A bare floppy-sized image
		 *  is invisible to the SCSI controller.  Pinning it means a later
		 *  round that changes the heuristic cannot do so silently, and it
		 *  is the closest offline proxy for the controller-side coverage
		 *  gap named in the header.
		 */
		snprintf(cmd, sizeof(cmd), "[RECORD] no prefix %s unreachable by dev_asc", names[i]);
		check(cmd, diskimage_exist(&m, 0, DISKIMAGE_SCSI), 0);
	}

	printf("--- B. 'd:' on a SCSI-default machine (pmax) ---\n");
	for (i = 0; i < 4; i++) {
		snprintf(path, sizeof(path), "%s/fl%d.img", WORK, i);
		snprintf(arg, sizeof(arg), "d:%s", path);
		d = add1(&m, MACHINE_PMAX, arg);
		snprintf(cmd, sizeof(cmd), "[PROOF] d: %s -> SCSI", names[i]);
		check(cmd, d ? d->type : -1, DISKIMAGE_SCSI);
		snprintf(cmd, sizeof(cmd), "[PROOF] d: %s exists as SCSI (dev_asc)", names[i]);
		check(cmd, diskimage_exist(&m, 0, DISKIMAGE_SCSI), 1);
		/*
		 *  EXACTNESS, and it is the row that pins the PLACEMENT rather
		 *  than the effect.  Assigning the type in the prefix block --
		 *  i.e. BEFORE diskimage_recalc_size() -- also makes d: work, but
		 *  hands the image the generic 63/16 geometry and rounds the
		 *  advertised capacity UP: 720K 1440 -> 2016 blocks (+40%), 1.2M
		 *  2400 -> 3024, 1.44M 2880 -> 3024, 2.88M 5760 -> 6048.  Under
		 *  the asymmetric bound in diskimage.c those extra blocks read
		 *  back as zeroes and refuse every write.  Only this row fails on
		 *  that variant; every other row here passes it.
		 */
		snprintf(cmd, sizeof(cmd), "[SIZE] d: %s advertised blocks exact", names[i]);
		check(cmd, d ? d->nr_of_logical_blocks : -1, sizes[i]/512);
	}

	printf("--- C. 'd:' on an IDE-default machine (malta) -- kills the hardcoded-SCSI mutant ---\n");
	/*
	 *  get_default_disk_type_for_machine() returns SCSI for exactly PMAX,
	 *  ARC, SGI, LUNA88K and MVME88K -- which are precisely the rigs this
	 *  project can boot -- and IDE for everything else.  So `d->type =
	 *  DISKIMAGE_SCSI` instead of the machine default passes every row on
	 *  every bootable rig.  These three rows are the only thing that
	 *  distinguishes the two, and MACHINE_EVBMIPS needs no image or kernel.
	 */
	snprintf(path, sizeof(path), "%s/fl2.img", WORK);
	snprintf(arg, sizeof(arg), "d:%s", path);
	d = add1(&m, MACHINE_EVBMIPS, arg);
	check("[PROOF] d: 1.44M on IDE-default -> IDE", d ? d->type : -1, DISKIMAGE_IDE);
	check("[PROOF] d: 1.44M exists as IDE (dev_wdc)", diskimage_exist(&m, 0, DISKIMAGE_IDE), 1);
	check("[PROOF] d: 1.44M NOT visible as SCSI", diskimage_exist(&m, 0, DISKIMAGE_SCSI), 0);

	printf("--- D. explicit prefixes keep precedence over 'd' ---\n");
	/*
	 *  The mutual-exclusion check in diskimage_add() tests only
	 *  i + f + s > 1 and knows nothing about 'd', so `id:` and `fd:` are
	 *  accepted arguments today.  Without the !prefix_i/!prefix_f/!prefix_s
	 *  guard, the d: assignment silently overrides an explicit request --
	 *  measured, not hypothetical: `id:` returned SCSI where it must be IDE.
	 */
	snprintf(arg, sizeof(arg), "fd:%s", path);
	d = add1(&m, MACHINE_PMAX, arg);
	check("[PREC] 'fd:' stays FLOPPY", d ? d->type : -1, DISKIMAGE_FLOPPY);
	snprintf(arg, sizeof(arg), "id:%s", path);
	d = add1(&m, MACHINE_PMAX, arg);
	check("[PREC] 'id:' stays IDE", d ? d->type : -1, DISKIMAGE_IDE);
	snprintf(arg, sizeof(arg), "s:%s", path);
	d = add1(&m, MACHINE_PMAX, arg);
	check("[CONTROL] 's:' -> SCSI", d ? d->type : -1, DISKIMAGE_SCSI);
	/*
	 *  #418 PASS 2: THE SEVENTH MUTANT, proposed by a reading seat and then
	 *  EXECUTED -- it survived all 35 rows.  Deleting only `&& !prefix_s`
	 *  leaves `fd:` and `id:` guarded by !prefix_f/!prefix_i, so every other
	 *  precedence row passes; `sd:` is the only argument that changes, and on
	 *  a SCSI-DEFAULT machine it changes SCSI to... SCSI.  Invisible unless
	 *  the row runs on an IDE-DEFAULT machine, where the mutant returns IDE
	 *  for an explicitly requested SCSI disk.  Measured, not predicted.
	 */
	d = add1(&m, MACHINE_EVBMIPS, arg);
	check("[CONTROL] 's:' -> SCSI on an IDE-default machine too",
	    d ? d->type : -1, DISKIMAGE_SCSI);
	snprintf(arg, sizeof(arg), "sd:%s", path);
	d = add1(&m, MACHINE_EVBMIPS, arg);
	check("[PREC] 'sd:' stays SCSI on an IDE-default machine",
	    d ? d->type : -1, DISKIMAGE_SCSI);

	printf("--- E. 'd:' still suppresses .iso/.cdr detection -- kills the 10-char mutant ---\n");
	/*
	 *  `&& !prefix_d` is the ONLY pre-existing use of prefix_d in the file,
	 *  so the round that gives prefix_d a second use is exactly the round in
	 *  which someone deletes the first as "now redundant".  Ten characters;
	 *  measured effect is d:*.iso becoming an unwritable CD-ROM.  A row set
	 *  using only .img filenames -- which is what the design brief specified
	 *  -- passes that mutant 100%.  These two rows are the whole defence.
	 */
	snprintf(path, sizeof(path), "%s/img.iso", WORK);
	mkfile(path, 1474560);
	snprintf(arg, sizeof(arg), "d:%s", path);
	d = add1(&m, MACHINE_PMAX, arg);
	check("[PROOF] d:*.iso is not a CD-ROM", d ? d->is_a_cdrom : -1, 0);
	check("[PROOF] d:*.iso is writable", d ? d->writable : -1, 1);
	snprintf(arg, sizeof(arg), "%s", path);
	d = add1(&m, MACHINE_PMAX, arg);
	check("[CONTROL] bare *.iso IS a CD-ROM", d ? d->is_a_cdrom : -1, 1);
	/*
	 *  RECORD, not an endorsement: the size heuristic tests only
	 *  type == DISKIMAGE_UNKNOWN and ignores is_a_cdrom, so a small ISO --
	 *  1.2M and 1.44M are standard El Torito floppy-emulation sizes --
	 *  becomes a FLOPPY CD-ROM, doubly unreachable.  Filed separately; this
	 *  row pins today's behaviour so the fix cannot land unnoticed.
	 */
	check("[RECORD] bare 1.44M *.iso is FLOPPY-typed (filed defect)",
	    d ? d->type : -1, DISKIMAGE_FLOPPY);

	/*
	 *  IDENTITY GUARD.  Two files with this name once differed only by the
	 *  case of a parent directory, and the stale one encoded a REVERSED
	 *  design decision.  A row count is the cheapest proof that the file
	 *  which ran is the file that was reviewed.
	 */
	counted = rows;
	check("[IDENTITY] row count -- guards against a stale copy", counted, 36);

	printf("\n%d rows, %d failures\n", rows, failures);
	return failures ? 1 : 0;
}
