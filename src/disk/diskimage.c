/*
 *  Copyright (C) 2003-2021  Anders Gavare.  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions are met:
 *
 *  1. Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright  
 *     notice, this list of conditions and the following disclaimer in the 
 *     documentation and/or other materials provided with the distribution.
 *  3. The name of the author may not be used to endorse or promote products
 *     derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 *  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE   
 *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 *  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 *  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 *  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 *  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 *  SUCH DAMAGE.
 *
 *
 *  Disk image support.
 *
 *  TODO:  diskimage_remove()? This would be useful for floppies in PC-style
 *	   machines, where disks may need to be swapped during boot etc.
 */

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

#include "cpu.h"
#include "diskimage.h"
#include "machine.h"
#include "misc.h"


/*  Set by the -f command line option; see main.c.  */
int do_fsync = 0;

/*  #define debug fatal  */

static const char *diskimage_types[] = DISKIMAGE_TYPES;

/*  Bytes of user data per CD-ROM sector, as seen by the guest:  */
#define	CDROM_SECTOR_SIZE	2048


/**************************************************************************/

/*
 *  my_fseek():
 *
 *  A helper function, like fseek() but takes off_t.  If the system has
 *  fseeko, then that is used. Otherwise I try to fake off_t offsets here.
 *
 *  The correct position is reached by seeking 2 billion bytes at a time
 *  (or less).  Note: This method is only used for SEEK_SET, for SEEK_CUR
 *  and SEEK_END, normal fseek() is used!
 *
 *  TODO: It seemed to work on Linux/i386, but not on Solaris/sparc (?).
 *  Anyway, most modern systems have fseeko(), so it shouldn't be a problem.
 */
static int my_fseek(FILE *f, off_t offset, int whence)
{
#ifdef HACK_FSEEKO
	if (whence == SEEK_SET) {
		int res = 0;
		off_t curoff = 0;
		off_t cur_step;

		fseek(f, 0, SEEK_SET);
		while (curoff < offset) {
			/*  How far to seek?  */
			cur_step = offset - curoff;
			if (cur_step > 2000000000)
				cur_step = 2000000000;
			res = fseek(f, cur_step, SEEK_CUR);
			if (res)
				return res;
			curoff += cur_step;
		}
		return 0;
	} else
		return fseek(f, offset, whence);
#else
	return fseeko(f, offset, whence);
#endif
}


/**************************************************************************/


/*
 *  diskimage_exist():
 *
 *  Returns 1 if the specified disk id (for a specific type) exists, 0
 *  otherwise.
 */
int diskimage_exist(struct machine *machine, int id, int type)
{
	struct diskimage *d = machine->first_diskimage;

	while (d != NULL) {
		if (d->type == type && d->id == id)
			return 1;
		d = d->next;
	}
	return 0;
}


/*
 *  diskimage_add_overlay():
 *
 *  Opens an overlay data file and its corresponding bitmap file, and adds
 *  the overlay to a disk image.
 */
bool diskimage_add_overlay(struct diskimage *d, char *overlay_basename, bool remove_after_open)
{
	struct diskimage_overlay overlay;
	size_t bitmap_name_len = strlen(overlay_basename) + 20;
	char *bitmap_name;

	CHECK_ALLOCATION(bitmap_name = (char *) malloc(bitmap_name_len));
	snprintf(bitmap_name, bitmap_name_len, "%s.map", overlay_basename);

	CHECK_ALLOCATION(overlay.overlay_basename = strdup(overlay_basename));
	overlay.f_data = fopen(overlay_basename, d->writable? "r+" : "r");
	if (overlay.f_data == NULL) {
		perror(overlay_basename);

		if (remove_after_open) {
			unlink(overlay_basename);
			unlink(bitmap_name);
		}

		free(overlay.overlay_basename);
		free(bitmap_name);
		return false;
	}

	overlay.f_bitmap = fopen(bitmap_name, d->writable? "r+" : "r");
	if (overlay.f_bitmap == NULL) {
		perror(bitmap_name);
		fprintf(stderr, "Please create the map file first.\n");
		fclose(overlay.f_data);

		if (remove_after_open) {
			unlink(overlay_basename);
			unlink(bitmap_name);
		}

		free(overlay.overlay_basename);
		free(bitmap_name);
		return false;
	}

	d->nr_of_overlays ++;

	CHECK_ALLOCATION(d->overlays = (struct diskimage_overlay *) realloc(d->overlays,
	    sizeof(struct diskimage_overlay) * d->nr_of_overlays));

	d->overlays[d->nr_of_overlays - 1] = overlay;

	if (remove_after_open) {
		if (unlink(overlay_basename) != 0)
			perror(overlay_basename);

		if (unlink(bitmap_name) != 0)
			perror(bitmap_name);
	}

	free(bitmap_name);

	return true;
}


/*
 *  diskimage_recalc_size():
 *
 *  Recalculate a disk's size by stat()-ing it.
 *  d is assumed to be non-NULL.
 */
bool diskimage_recalc_size(struct diskimage *d)
{
	struct stat st;
	int res;
	int64_t size = 0;

	if (d->nr_of_tracks > 0) {
		/*
		 *  Multi-track (CUE/BIN) image: the file named by d->fname
		 *  is only the small cue sheet text file, so its size is
		 *  meaningless here.  The logical size spans from the start
		 *  of the first data track to the end of the disc, as
		 *  computed when the cue sheet was parsed.
		 */
		size = (d->total_disc_sectors - d->first_data_track_lba)
		    * CDROM_SECTOR_SIZE;
	} else {
		res = stat(d->fname, &st);
		if (res)
			return false;

		size = st.st_size;

		/*
		 *  TODO:  CD-ROM devices, such as /dev/cd0c, how can one
		 *  check how much data is on that cd-rom without reading it?
		 *  For now, assume some large number, hopefully it will be
		 *  enough to hold any cd-rom image.
		 */
		if (d->is_a_cdrom && size == 0)
			size = 762048000;
	}

	d->total_size = size;

	if (d->nr_of_tracks == 0 &&
	    (d->total_size == 720*1024 || d->total_size == 1474560
	    || d->total_size == 2949120 || d->total_size == 1228800)
	    && d->type == DISKIMAGE_UNKNOWN)
		d->type = DISKIMAGE_FLOPPY;

	switch (d->type) {
	case DISKIMAGE_FLOPPY:
		if (d->total_size < 737280) {
			debugmsg(SUBSYS_DISK, "", VERBOSITY_WARNING,
			    "TODO: small (non-80-cylinder) floppies?");
		}

		if (!d->chs_override) {
			d->cylinders = 80;
			d->heads = 2;
			d->sectors_per_track = d->nr_of_logical_blocks * d->logical_block_size
				/ (d->cylinders * d->heads * 512);
		}
		break;

	default:/*  Non-floppies:  */
		if (!d->chs_override) {
			d->heads = 16;
			d->sectors_per_track = 63;

			int64_t bytespercyl = d->heads * d->sectors_per_track * 512;
			d->cylinders = size / bytespercyl;
			if (d->cylinders * bytespercyl < size)
				d->cylinders ++;
		}
	}

	// printf("c=%i h=%i s=%i\n", d->cylinders, d->heads, d->sectors_per_track);

	// Update size to full cylinders.
	size = d->heads * d->sectors_per_track * d->cylinders * 512;

	d->nr_of_logical_blocks = size / d->logical_block_size;
	if (size & (d->logical_block_size - 1))
		d->nr_of_logical_blocks ++;

	return true;
}


/*
 *  diskimage_getsize():
 *
 *  Returns -1 if the specified disk id/type does not exists, otherwise
 *  the size of the disk image is returned.
 */
int64_t diskimage_getsize(struct machine *machine, int id, int type)
{
	struct diskimage *d = machine->first_diskimage;

	while (d != NULL) {
		if (d->type == type && d->id == id)
			return d->nr_of_logical_blocks * d->logical_block_size;
		d = d->next;
	}
	return -1;
}


/*
 *  diskimage_get_baseoffset():
 *
 *  Returns -1 if the specified disk id/type does not exists, otherwise
 *  the base offset of the disk image is returned.
 */
int64_t diskimage_get_baseoffset(struct machine *machine, int id, int type)
{
	struct diskimage *d = machine->first_diskimage;

	while (d != NULL) {
		if (d->type == type && d->id == id)
			return d->override_base_offset;

		d = d->next;
	}
	return -1;
}


/*
 *  diskimage_set_baseoffset():
 *
 *  Sets the base offset for a disk image. Useful e.g. when booting directly
 *  from NetBSD/dreamcast or Linux/dreamcast ISO images.
 */
void diskimage_set_baseoffset(struct machine *machine, int id, int type, int64_t offset)
{
	struct diskimage *d = machine->first_diskimage;

	while (d != NULL) {
		if (d->type == type && d->id == id) {
			d->override_base_offset = offset;
			return;
		}
		
		d = d->next;
	}

	fatal("diskimage_set_baseoffset(): disk id %i (type %s) not found?\n",
	    id, diskimage_types[type]);
	exit(1);
}


/*
 *  diskimage_getchs():
 *
 *  Returns the current CHS values of a disk image.
 */
void diskimage_getchs(struct machine *machine, int id, int type,
	int *c, int *h, int *s)
{
	struct diskimage *d = machine->first_diskimage;

	while (d != NULL) {
		if (d->type == type && d->id == id) {
			*c = d->cylinders;
			*h = d->heads;
			*s = d->sectors_per_track;
			return;
		}
		d = d->next;
	}
	fatal("diskimage_getchs(): disk id %i (type %s) not found?\n",
	    id, diskimage_types[type]);
	exit(1);
}


/*
 *  diskimage_access__cdrom():
 *
 *  This is a special-case function, called from diskimage__internal_access().
 *  On my FreeBSD 4.9 system, the cdrom device /dev/cd0c seems to not be able
 *  to handle something like "fseek(512); fread(512);" but it handles
 *  "fseek(2048); fread(512);" just fine.  So, if diskimage__internal_access()
 *  fails in reading a block of data, this function is called as an attempt to
 *  align reads at 2048-byte sectors instead.
 *
 *  (Ugly hack.  TODO: how to solve this cleanly?)
 *
 *  NOTE:  Returns the number of bytes read, 0 if nothing was successfully
 *  read. (These are not the same as diskimage_access()).
 */
static size_t diskimage_access__cdrom(struct diskimage *d, off_t offset,
	unsigned char *buf, size_t len)
{
	off_t aligned_offset;
	size_t bytes_read, total_copied = 0;
	unsigned char cdrom_buf[CDROM_SECTOR_SIZE];
	off_t buf_ofs, i = 0;

	/*  printf("diskimage_access__cdrom(): offset=0x%llx size=%lli\n",
	    (long long)offset, (long long)len);  */

	/*  #204: (Codex/Fable) a negative offset (a guest can seek an opened
	    flat CD/ISO handle to 0xffffffff) truncates toward zero, leaving
	    buf_ofs negative below -> cdrom_buf[-1] OOB stack read.  */
	if (offset < 0)
		return 0;

	aligned_offset = (offset / CDROM_SECTOR_SIZE) * CDROM_SECTOR_SIZE;
	my_fseek(d->f, aligned_offset, SEEK_SET);

	while (len != 0) {
		bytes_read = fread(cdrom_buf, 1, CDROM_SECTOR_SIZE, d->f);
		if (bytes_read != CDROM_SECTOR_SIZE)
			return 0;

		/*  Copy (part of) cdrom_buf into buf:  */
		buf_ofs = offset - aligned_offset;
		while (buf_ofs < CDROM_SECTOR_SIZE && len != 0) {
			buf[i ++] = cdrom_buf[buf_ofs ++];
			total_copied ++;
			len --;
		}

		aligned_offset += CDROM_SECTOR_SIZE;
		offset = aligned_offset;
	}

	return total_copied;
}


/**************************************************************************/

/*
 *  Multi-track CD-ROM (CUE/BIN) image support:
 *
 *  A cue sheet (".cue" file) is a small text file which describes the track
 *  layout of a CD, and refers to one or more "bin" files containing the
 *  actual sector data.  This makes it possible to use CD images which
 *  contain a mixture of data and audio tracks (e.g. Dreamcast or live-CD
 *  images), instead of only flat single-track .iso images.
 *
 *  When a cue sheet has been parsed successfully, d->nr_of_tracks is set to
 *  the number of tracks (>= 1), and all reads are translated using the
 *  track table (see diskimage_access__cue() below).  Logical byte offset 0
 *  of the disk image corresponds to the first sector of the FIRST DATA
 *  TRACK, so booting from an ISO9660 filesystem path boots from the first
 *  data track by default, exactly as if a flat .iso image of that track had
 *  been supplied.  (A consequence is that tracks _before_ the first data
 *  track, e.g. leading audio tracks, are not reachable via the logical
 *  offset space; tracks after it are.)
 *
 *  For all other (non-cue) images, nr_of_tracks remains 0, and the flat
 *  file code paths are used, completely unchanged.
 */

#define	CUE_MAX_TRACKS		99
#define	CUE_MAX_FILES		99
#define	CUE_MAX_LINE_LEN	512

/*  Temporary per-track data while parsing a cue sheet:  */
struct cue_parse_track {
	int	track_nr;
	int	is_data;
	int	file_index;
	int	sector_size;
	int	data_offset;
	int64_t	index01_frame;		/*  -1 = no INDEX 01 seen (yet)  */
};


/*
 *  diskimage__cue_get_token():
 *
 *  Copies the next whitespace-separated (or double-quoted) token from *pp
 *  into buf, advancing *pp past it.  Returns false if the rest of the line
 *  is empty.  Over-long tokens are silently truncated.
 */
static bool diskimage__cue_get_token(char **pp, char *buf, size_t buflen)
{
	char *p = *pp;
	size_t n = 0;

	while (*p == ' ' || *p == '\t')
		p ++;

	if (*p == '\0' || *p == '\r' || *p == '\n')
		return false;

	if (*p == '"') {
		p ++;
		while (*p != '\0' && *p != '"' && *p != '\r' && *p != '\n') {
			if (n < buflen - 1)
				buf[n ++] = *p;
			p ++;
		}
		if (*p == '"')
			p ++;
	} else {
		while (*p != '\0' && *p != ' ' && *p != '\t' &&
		    *p != '\r' && *p != '\n') {
			if (n < buflen - 1)
				buf[n ++] = *p;
			p ++;
		}
	}

	buf[n] = '\0';
	*pp = p;
	return true;
}


/*
 *  diskimage__cue_resolve_path():
 *
 *  Returns a newly allocated string with the host path of a bin file
 *  referenced from a cue sheet.  Relative names are resolved against the
 *  directory containing the cue sheet itself.
 *
 *  Returns NULL if the referenced name is rejected (absolute path, drive
 *  prefix, or a ".." path component); the cue sheet is untrusted input and
 *  must not be able to name host files outside the cue sheet's directory.
 */
static char *diskimage__cue_resolve_path(const char *cuename,
	const char *binname)
{
	const char *slash = strrchr(cuename, '/');
	const char *backslash = strrchr(cuename, '\\');
	const char *p;
	char *result;
	size_t dirlen;

	/*  #158: (Codex/Fable) default-deny path escape
	    from cue sheets: reject absolute paths and drive prefixes...  */
	if (binname[0] == '/' || binname[0] == '\\' ||
	    (((binname[0] >= 'A' && binname[0] <= 'Z') ||
	      (binname[0] >= 'a' && binname[0] <= 'z')) && binname[1] == ':')) {
		debugmsg(SUBSYS_DISK, "cue", VERBOSITY_ERROR,
		    "%s: refusing absolute FILE path \"%s\"",
		    cuename, binname);
		return NULL;
	}

	/*  ...and reject any ".." path component:  */
	for (p = binname; *p != '\0'; p ++) {
		if (p[0] == '.' && p[1] == '.' &&
		    (p == binname || p[-1] == '/' || p[-1] == '\\') &&
		    (p[2] == '\0' || p[2] == '/' || p[2] == '\\')) {
			debugmsg(SUBSYS_DISK, "cue", VERBOSITY_ERROR,
			    "%s: refusing FILE path \"%s\" containing \"..\"",
			    cuename, binname);
			return NULL;
		}
	}

	if (backslash != NULL && (slash == NULL || backslash > slash))
		slash = backslash;

	if (slash == NULL) {
		CHECK_ALLOCATION(result = strdup(binname));
		return result;
	}

	dirlen = slash - cuename + 1;
	CHECK_ALLOCATION(result = (char *) malloc(dirlen + strlen(binname) + 1));
	memcpy(result, cuename, dirlen);
	strcpy(result + dirlen, binname);
	return result;
}


/*
 *  diskimage__looks_like_cue():
 *
 *  Content sniffing, for CD-ROM images supplied without a ".cue" filename
 *  extension: returns true if the file begins (possibly after a UTF-8 BOM
 *  and whitespace) with a well-known cue sheet keyword.
 */
static bool diskimage__looks_like_cue(const char *fname)
{
	static const char *cue_keywords[] = { "REM", "FILE", "CATALOG",
	    "CDTEXTFILE", "TITLE", "PERFORMER", "SONGWRITER", "TRACK", NULL };
	char buf[64];
	char *p = buf;
	FILE *f = fopen(fname, "r");
	size_t n;
	int i;

	if (f == NULL)
		return false;

	n = fread(buf, 1, sizeof(buf) - 1, f);
	fclose(f);
	buf[n] = '\0';

	if (n >= 3 && (unsigned char)p[0] == 0xef &&
	    (unsigned char)p[1] == 0xbb && (unsigned char)p[2] == 0xbf)
		p += 3;
	while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n')
		p ++;

	for (i = 0; cue_keywords[i] != NULL; i ++) {
		size_t l = strlen(cue_keywords[i]);
		if (strncasecmp(p, cue_keywords[i], l) == 0 &&
		    (p[l] == ' ' || p[l] == '\t'))
			return true;
	}

	return false;
}


/*
 *  diskimage__parse_cue():
 *
 *  Parses d->fname as a cue sheet, opens the bin file(s) it refers to, and
 *  fills in the track table (d->track etc).  Understands at least:
 *
 *	FILE "name.bin" BINARY
 *	TRACK nn AUDIO | MODE1/2048 | MODE1/2352 | MODE2/2336 | MODE2/2352
 *	INDEX 01 mm:ss:ff
 *
 *  Comments (REM), CD-TEXT commands, FLAGS, ISRC etc. are skipped.  Both
 *  the common single-bin multi-track layout and multiple FILE lines are
 *  handled; with multiple files, each file's tracks are laid out
 *  sequentially on the disc.  (PREGAP/POSTGAP commands, i.e. gaps which are
 *  not stored in any bin file, are ignored with a warning.)
 *
 *  Returns true if the cue sheet was parsed successfully.  On failure a
 *  warning is printed and false is returned, with d completely unmodified,
 *  so that the caller can fall back to treating the file as a flat image.
 */
static bool diskimage__parse_cue(struct diskimage *d)
{
	FILE *cue;
	char line[CUE_MAX_LINE_LEN];
	char *file_name[CUE_MAX_FILES];
	FILE *bin_file[CUE_MAX_FILES];
	char *bin_name[CUE_MAX_FILES];
	int64_t bin_size[CUE_MAX_FILES];
	struct cue_parse_track pt[CUE_MAX_TRACKS];
	struct diskimage_track *tt = NULL;
	int nr_of_files = 0, nr_of_pt = 0, nr_open = 0;
	int lineno = 0, i, cur_file;
	int64_t disc_cursor, file_base_lba, first_data_lba;
	bool warned_gap = false;

	cue = fopen(d->fname, "r");
	if (cue == NULL) {
		debugmsg(SUBSYS_DISK, "cue", VERBOSITY_WARNING,
		    "%s: could not open cue sheet: %s",
		    d->fname, strerror(errno));
		return false;
	}

	while (fgets(line, sizeof(line), cue) != NULL) {
		char keyword[64];
		char *p = line;

		lineno ++;

		if (!diskimage__cue_get_token(&p, keyword, sizeof(keyword)))
			continue;	/*  blank line  */

		if (strcasecmp(keyword, "REM") == 0 ||
		    strcasecmp(keyword, "CATALOG") == 0 ||
		    strcasecmp(keyword, "CDTEXTFILE") == 0 ||
		    strcasecmp(keyword, "TITLE") == 0 ||
		    strcasecmp(keyword, "PERFORMER") == 0 ||
		    strcasecmp(keyword, "SONGWRITER") == 0 ||
		    strcasecmp(keyword, "FLAGS") == 0 ||
		    strcasecmp(keyword, "ISRC") == 0)
			continue;

		if (strcasecmp(keyword, "PREGAP") == 0 ||
		    strcasecmp(keyword, "POSTGAP") == 0) {
			if (!warned_gap)
				debugmsg(SUBSYS_DISK, "cue",
				    VERBOSITY_WARNING, "%s: line %i: PREGAP/"
				    "POSTGAP ignored (unstored gaps are not"
				    " supported; track positions may be off"
				    " for absolutely-addressed filesystems)",
				    d->fname, lineno);
			warned_gap = true;
			continue;
		}

		if (strcasecmp(keyword, "FILE") == 0) {
			char fname_token[CUE_MAX_LINE_LEN];
			char type_token[64];

			if (!diskimage__cue_get_token(&p, fname_token,
			    sizeof(fname_token)) ||
			    !diskimage__cue_get_token(&p, type_token,
			    sizeof(type_token))) {
				debugmsg(SUBSYS_DISK, "cue",
				    VERBOSITY_WARNING, "%s: line %i:"
				    " malformed FILE command",
				    d->fname, lineno);
				goto fail;
			}

			if (strcasecmp(type_token, "BINARY") != 0) {
				debugmsg(SUBSYS_DISK, "cue",
				    VERBOSITY_WARNING, "%s: line %i:"
				    " unsupported FILE type \"%s\" (only"
				    " BINARY is supported)",
				    d->fname, lineno, type_token);
				goto fail;
			}

			if (nr_of_files >= CUE_MAX_FILES) {
				debugmsg(SUBSYS_DISK, "cue",
				    VERBOSITY_WARNING, "%s: line %i: too"
				    " many FILE commands", d->fname, lineno);
				goto fail;
			}

			CHECK_ALLOCATION(file_name[nr_of_files] =
			    strdup(fname_token));
			nr_of_files ++;
			continue;
		}

		if (strcasecmp(keyword, "TRACK") == 0) {
			char nr_token[64], mode_token[64];
			struct cue_parse_track *t;

			if (!diskimage__cue_get_token(&p, nr_token,
			    sizeof(nr_token)) ||
			    !diskimage__cue_get_token(&p, mode_token,
			    sizeof(mode_token))) {
				debugmsg(SUBSYS_DISK, "cue",
				    VERBOSITY_WARNING, "%s: line %i:"
				    " malformed TRACK command",
				    d->fname, lineno);
				goto fail;
			}

			if (nr_of_files == 0) {
				debugmsg(SUBSYS_DISK, "cue",
				    VERBOSITY_WARNING, "%s: line %i: TRACK"
				    " command before any FILE command",
				    d->fname, lineno);
				goto fail;
			}

			if (nr_of_pt >= CUE_MAX_TRACKS) {
				debugmsg(SUBSYS_DISK, "cue",
				    VERBOSITY_WARNING, "%s: line %i: too"
				    " many TRACK commands", d->fname, lineno);
				goto fail;
			}

			t = &pt[nr_of_pt];
			memset(t, 0, sizeof(*t));
			t->track_nr = atoi(nr_token);
			t->file_index = nr_of_files - 1;
			t->index01_frame = -1;

			if (strcasecmp(mode_token, "AUDIO") == 0) {
				t->is_data = 0;
				t->sector_size = 2352;
				t->data_offset = 0;
			} else if (strcasecmp(mode_token, "MODE1/2048") == 0) {
				/*  Cooked sectors; user data only:  */
				t->is_data = 1;
				t->sector_size = 2048;
				t->data_offset = 0;
			} else if (strcasecmp(mode_token, "MODE1/2352") == 0) {
				/*  Raw sectors; 12 sync + 4 header bytes
				    before the 2048 user data bytes:  */
				t->is_data = 1;
				t->sector_size = 2352;
				t->data_offset = 16;
			} else if (strcasecmp(mode_token, "MODE2/2352") == 0) {
				/*  Raw XA sectors; assume Form 1: 16 header
				    + 8 subheader bytes before user data:  */
				t->is_data = 1;
				t->sector_size = 2352;
				t->data_offset = 24;
			} else if (strcasecmp(mode_token, "MODE2/2336") == 0) {
				/*  XA sectors without sync/header; assume
				    Form 1: 8 subheader bytes first:  */
				t->is_data = 1;
				t->sector_size = 2336;
				t->data_offset = 8;
			} else {
				debugmsg(SUBSYS_DISK, "cue",
				    VERBOSITY_WARNING, "%s: line %i:"
				    " unsupported TRACK mode \"%s\"",
				    d->fname, lineno, mode_token);
				goto fail;
			}

			nr_of_pt ++;
			continue;
		}

		if (strcasecmp(keyword, "INDEX") == 0) {
			char nr_token[64], msf_token[64];
			int mm, ss, ff;

			if (!diskimage__cue_get_token(&p, nr_token,
			    sizeof(nr_token)) ||
			    !diskimage__cue_get_token(&p, msf_token,
			    sizeof(msf_token))) {
				debugmsg(SUBSYS_DISK, "cue",
				    VERBOSITY_WARNING, "%s: line %i:"
				    " malformed INDEX command",
				    d->fname, lineno);
				goto fail;
			}

			if (nr_of_pt == 0) {
				debugmsg(SUBSYS_DISK, "cue",
				    VERBOSITY_WARNING, "%s: line %i: INDEX"
				    " command before any TRACK command",
				    d->fname, lineno);
				goto fail;
			}

			if (sscanf(msf_token, "%d:%d:%d", &mm, &ss, &ff) != 3
			    || mm < 0 || ss < 0 || ss > 59 || ff < 0 ||
			    ff > 74) {
				debugmsg(SUBSYS_DISK, "cue",
				    VERBOSITY_WARNING, "%s: line %i: bad"
				    " INDEX time \"%s\" (expected mm:ss:ff)",
				    d->fname, lineno, msf_token);
				goto fail;
			}

			/*  Only INDEX 01 (the track start) is used; INDEX 00
			    (pregap start) and higher indices are ignored:  */
			if (atoi(nr_token) == 1)
				pt[nr_of_pt - 1].index01_frame =
				    ((int64_t)mm * 60 + ss) * 75 + ff;
			continue;
		}

		/*  Unknown keywords are ignored, for robustness.  */
	}

	fclose(cue);
	cue = NULL;

	if (nr_of_pt == 0) {
		debugmsg(SUBSYS_DISK, "cue", VERBOSITY_WARNING,
		    "%s: no TRACK commands found", d->fname);
		goto fail;
	}

	for (i = 0; i < nr_of_pt; i ++) {
		if (pt[i].index01_frame < 0) {
			debugmsg(SUBSYS_DISK, "cue", VERBOSITY_WARNING,
			    "%s: track %i has no INDEX 01",
			    d->fname, pt[i].track_nr);
			goto fail;
		}
	}

	/*  Open the bin file(s):  */
	for (i = 0; i < nr_of_files; i ++) {
		struct stat st;
		char *resolved = diskimage__cue_resolve_path(d->fname,
		    file_name[i]);
		FILE *bf;

		/*  #158: (Codex/Fable) NULL means the
		    FILE path was rejected (path escape attempt).  */
		if (resolved == NULL)
			goto fail;

		bf = fopen(resolved, "r");

		if (bf == NULL) {
			debugmsg(SUBSYS_DISK, "cue", VERBOSITY_WARNING,
			    "%s: could not open bin file \"%s\": %s",
			    d->fname, resolved, strerror(errno));
			free(resolved);
			goto fail;
		}

		if (fstat(fileno(bf), &st) != 0) {
			debugmsg(SUBSYS_DISK, "cue", VERBOSITY_WARNING,
			    "%s: could not stat bin file \"%s\": %s",
			    d->fname, resolved, strerror(errno));
			fclose(bf);
			free(resolved);
			goto fail;
		}

		bin_file[i] = bf;
		bin_name[i] = resolved;
		bin_size[i] = st.st_size;
		nr_open ++;
	}

	/*
	 *  Lay out the tracks on the disc, and compute each track's byte
	 *  offset within its bin file.  Within one file, INDEX 01 times are
	 *  frame offsets from the start of that file, so the byte offset
	 *  advances by (frame delta) * (previous track's sector size).
	 *  Multiple files are laid out sequentially on the disc.
	 */
	CHECK_ALLOCATION(tt = (struct diskimage_track *)
	    malloc(sizeof(struct diskimage_track) * nr_of_pt));

	disc_cursor = 0;
	file_base_lba = 0;
	cur_file = -1;

	for (i = 0; i < nr_of_pt; i ++) {
		struct cue_parse_track *ct = &pt[i];
		int64_t byte_off, nr_sectors;

		if (ct->file_index != cur_file) {
			cur_file = ct->file_index;
			file_base_lba = disc_cursor;
			byte_off = ct->index01_frame * ct->sector_size;
		} else {
			if (ct->index01_frame < pt[i-1].index01_frame) {
				debugmsg(SUBSYS_DISK, "cue",
				    VERBOSITY_WARNING, "%s: track %i:"
				    " INDEX 01 goes backwards",
				    d->fname, ct->track_nr);
				goto fail;
			}
			byte_off = tt[i-1].file_byte_offset +
			    (ct->index01_frame - pt[i-1].index01_frame) *
			    pt[i-1].sector_size;
		}

		if (byte_off > bin_size[cur_file]) {
			debugmsg(SUBSYS_DISK, "cue", VERBOSITY_WARNING,
			    "%s: track %i starts beyond the end of \"%s\"",
			    d->fname, ct->track_nr, bin_name[cur_file]);
			goto fail;
		}

		if (i+1 < nr_of_pt && pt[i+1].file_index == cur_file) {
			/*  Frame deltas within one file are sector counts: */
			nr_sectors = pt[i+1].index01_frame -
			    ct->index01_frame;
		} else {
			int64_t bytes_left = bin_size[cur_file] - byte_off;
			nr_sectors = bytes_left / ct->sector_size;
			if (bytes_left % ct->sector_size != 0)
				debugmsg(SUBSYS_DISK, "cue",
				    VERBOSITY_WARNING, "%s: \"%s\" does not"
				    " contain a whole number of %i-byte"
				    " sectors for track %i; %i trailing"
				    " bytes ignored", d->fname,
				    bin_name[cur_file], ct->sector_size,
				    ct->track_nr,
				    (int) (bytes_left % ct->sector_size));
		}

		if (nr_sectors == 0)
			debugmsg(SUBSYS_DISK, "cue", VERBOSITY_WARNING,
			    "%s: track %i is empty",
			    d->fname, ct->track_nr);

		tt[i].track_nr = ct->track_nr;
		tt[i].is_data = ct->is_data;
		tt[i].file_index = cur_file;
		tt[i].file_byte_offset = byte_off;
		tt[i].start_lba = file_base_lba + ct->index01_frame;
		tt[i].nr_of_sectors = nr_sectors;
		tt[i].sector_size = ct->sector_size;
		tt[i].data_offset = ct->data_offset;

		disc_cursor = tt[i].start_lba + nr_sectors;
	}

	/*  Logical offset 0 shall map to the first data track:  */
	first_data_lba = -1;
	for (i = 0; i < nr_of_pt; i ++) {
		if (tt[i].is_data) {
			first_data_lba = tt[i].start_lba;
			break;
		}
	}
	if (first_data_lba < 0) {
		debugmsg(SUBSYS_DISK, "cue", VERBOSITY_WARNING,
		    "%s: no data track found; using track %i as the boot"
		    " origin", d->fname, tt[0].track_nr);
		first_data_lba = tt[0].start_lba;
	}

	if (disc_cursor <= first_data_lba) {
		debugmsg(SUBSYS_DISK, "cue", VERBOSITY_WARNING,
		    "%s: no readable sectors at/after the first data track",
		    d->fname);
		goto fail;
	}

	/*  Success. Move everything into the diskimage struct:  */
	CHECK_ALLOCATION(d->track_file = (FILE **)
	    malloc(sizeof(FILE *) * nr_of_files));
	CHECK_ALLOCATION(d->track_file_name = (char **)
	    malloc(sizeof(char *) * nr_of_files));
	for (i = 0; i < nr_of_files; i ++) {
		d->track_file[i] = bin_file[i];
		d->track_file_name[i] = bin_name[i];
		free(file_name[i]);
	}
	d->nr_of_track_files = nr_of_files;
	d->track = tt;
	d->nr_of_tracks = nr_of_pt;
	d->first_data_track_lba = first_data_lba;
	d->total_disc_sectors = disc_cursor;

	return true;

fail:
	if (cue != NULL)
		fclose(cue);
	for (i = 0; i < nr_open; i ++) {
		fclose(bin_file[i]);
		free(bin_name[i]);
	}
	for (i = 0; i < nr_of_files; i ++)
		free(file_name[i]);
	free(tt);

	debugmsg(SUBSYS_DISK, "cue", VERBOSITY_WARNING,
	    "%s: cue sheet could not be used; treating the file as a flat"
	    " image", d->fname);

	return false;
}


/*
 *  diskimage_access__cue():
 *
 *  Read handler for multi-track (CUE/BIN) CD-ROM images; only used when
 *  d->nr_of_tracks > 0.  Logical byte offsets are translated so that
 *  logical sector 0 is the first sector of the first data track; the
 *  matching track's bin file is then read at
 *
 *	file_byte_offset + (sector - start_lba) * sector_size
 *	                 + data_offset + intra-sector offset
 *
 *  so that raw (2352-byte) data sectors have their 2048 user data bytes
 *  extracted, and the guest always sees clean 2048-byte logical sectors.
 *  For audio tracks, the first 2048 bytes of each raw 2352-byte sector are
 *  returned.  Sectors inside a gap covered by no track (e.g. a pregap
 *  before the first track's INDEX 01) read as zero-filled.
 *
 *  NOTE:  Returns the number of bytes read; reads beyond the end of the
 *  disc stop short, and the caller zero-fills the rest of the buffer (the
 *  same behavior as reading beyond the end of a flat image).
 */
static size_t diskimage_access__cue(struct diskimage *d, off_t offset,
	unsigned char *buf, size_t len)
{
	size_t total_copied = 0;

	if (offset < 0)
		return 0;

	while (len != 0) {
		int64_t sector = d->first_data_track_lba +
		    offset / CDROM_SECTOR_SIZE;
		int intra = (int) (offset % CDROM_SECTOR_SIZE);
		size_t chunk = CDROM_SECTOR_SIZE - intra;
		struct diskimage_track *t = NULL;
		int i;

		if (chunk > len)
			chunk = len;

		if (sector >= d->total_disc_sectors)
			break;

		for (i = 0; i < d->nr_of_tracks; i ++) {
			if (sector >= d->track[i].start_lba &&
			    sector < d->track[i].start_lba +
			    d->track[i].nr_of_sectors) {
				t = &d->track[i];
				break;
			}
		}

		if (t == NULL) {
			/*  Sector belongs to no track:  */
			memset(buf + total_copied, 0, chunk);
		} else {
			FILE *f = d->track_file[t->file_index];
			off_t file_ofs = t->file_byte_offset +
			    (sector - t->start_lba) *
			    (int64_t) t->sector_size + t->data_offset + intra;
			size_t bytes_read;

			if (my_fseek(f, file_ofs, SEEK_SET) != 0) {
				fatal("[ diskimage_access__cue(): fseek()"
				    " failed on disk id %i ]\n", d->id);
				break;
			}

			bytes_read = fread(buf + total_copied, 1, chunk, f);
			if (bytes_read != chunk) {
				fatal("[ diskimage_access__cue(): short read"
				    " on disk id %i, track %i, file offset"
				    " %lli ]\n", d->id, t->track_nr,
				    (long long) file_ofs);
				total_copied += bytes_read;
				break;
			}
		}

		total_copied += chunk;
		offset += chunk;
		len -= chunk;
	}

	return total_copied;
}


/**************************************************************************/


/*  Helper function.  */
static void overlay_set_block_in_use(struct diskimage *d,
	int overlay_nr, off_t ofs)
{
	off_t bit_nr = ofs / OVERLAY_BLOCK_SIZE;
	off_t bitmap_file_offset = bit_nr / 8;
	int res;
	unsigned char data;

	res = my_fseek(d->overlays[overlay_nr].f_bitmap,
	    bitmap_file_offset, SEEK_SET);
	if (res) {
		perror("my_fseek");
		fprintf(stderr, "Could not seek in bitmap file?"
		    " offset = %lli, read\n", (long long)bitmap_file_offset);
		exit(1);
	}

	/*  Read the original bitmap data, and OR in the new bit:  */
	res = fread(&data, 1, 1, d->overlays[overlay_nr].f_bitmap);
	if (res != 1)
		data = 0x00;

	data |= (1 << (bit_nr & 7));

	/*  Write it back:  */
	res = my_fseek(d->overlays[overlay_nr].f_bitmap,
	    bitmap_file_offset, SEEK_SET);
	if (res) {
		perror("my_fseek");
		fprintf(stderr, "Could not seek in bitmap file?"
		    " offset = %lli, write\n", (long long)bitmap_file_offset);
		exit(1);
	}
	res = fwrite(&data, 1, 1, d->overlays[overlay_nr].f_bitmap);
	if (res != 1) {
		fprintf(stderr, "Could not write to bitmap file. Aborting.\n");
		exit(1);
	}
	
	if (do_fsync) {
		/*  fflush first: fsync only flushes kernel buffers, not
		    stdio's userspace buffer.  */
		fflush(d->overlays[overlay_nr].f_bitmap);
		fsync(fileno(d->overlays[overlay_nr].f_bitmap));
	}
}


/*  Helper function.  */
static int overlay_has_block(struct diskimage *d, int overlay_nr, off_t ofs)
{
	off_t bit_nr = ofs / OVERLAY_BLOCK_SIZE;
	off_t bitmap_file_offset = bit_nr / 8;
	int res;
	unsigned char data;

	res = my_fseek(d->overlays[overlay_nr].f_bitmap,
	    bitmap_file_offset, SEEK_SET);
	if (res != 0)
		return 0;

	/*  The seek succeeded, now read the bit:  */
	res = fread(&data, 1, 1, d->overlays[overlay_nr].f_bitmap);
	if (res != 1)
		return 0;

	if (data & (1 << (bit_nr & 7)))
		return 1;

	return 0;
}


/*
 *  fwrite_helper():
 *
 *  Internal helper function. Writes to a disk image file, or if the
 *  disk image has overlays, to the last overlay.
 */
static size_t fwrite_helper(off_t offset, unsigned char *buf,
	size_t len, struct diskimage *d)
{
	off_t curofs;

	/*  Fast return-path for the case when no overlays are used:  */
	if (d->nr_of_overlays == 0) {
		int res = my_fseek(d->f, offset, SEEK_SET);
		if (res != 0) {
			fatal("[ diskimage__internal_access(): fseek() failed"
			    " on disk id %i \n", d->id);
			return 0;
		}

		size_t written = fwrite(buf, 1, len, d->f);

		if (do_fsync) {
			fflush(d->f);
			fsync(fileno(d->f));
		}

		return written;
	}

	if ((len & (OVERLAY_BLOCK_SIZE-1)) != 0) {
		fatal("TODO: overlay access (write), len not multiple of "
		    "overlay block size. not yet implemented.\n");
		fatal("len = %lli\n", (long long) len);
		/*  #164: (Codex/Fable) guest-controlled
		    length must not abort() the emulator; fail the I/O.  */
		return 0;
	}
	if ((offset & (OVERLAY_BLOCK_SIZE-1)) != 0) {
		fatal("TODO: unaligned overlay access\n");
		fatal("offset = %lli\n", (long long) offset);
		/*  #164: (Codex/Fable) same as above.  */
		return 0;
	}

	/*  Split the write into OVERLAY_BLOCK_SIZE writes:  */
	for (curofs = offset; curofs < (off_t) (offset+len);
	     curofs += OVERLAY_BLOCK_SIZE) {
		/*  Always write to the last overlay:  */
		int overlay_nr = d->nr_of_overlays-1;
		off_t lenwritten;
		int res = my_fseek(d->overlays[overlay_nr].f_data,
		    curofs, SEEK_SET);
		if (res != 0) {
			fatal("[ diskimage: fwrite_helper(): fseek()"
			    " failed on disk id %i ]\n", d->id);
			return 0;
		}

		lenwritten = fwrite(buf, 1, OVERLAY_BLOCK_SIZE,
		    d->overlays[overlay_nr].f_data);
		if (lenwritten != OVERLAY_BLOCK_SIZE) {
			fatal("[ diskimage: fwrite_helper(): fwrite to"
			    " overlay failed on disk id %i ]\n", d->id);
			exit(1);
		}

		buf += OVERLAY_BLOCK_SIZE;

		if (do_fsync) {
			fflush(d->overlays[overlay_nr].f_data);
			fsync(fileno(d->overlays[overlay_nr].f_data));
		}

		/*  Mark this block in the last overlay as in use:  */
		overlay_set_block_in_use(d, overlay_nr, curofs);
	}

	return len;
}


/*
 *  fread_helper():
 *
 *  Internal helper function. Reads from a disk image file, or if the
 *  disk image has overlays, from the last overlay that has the specific
 *  data (or the disk image file itself).
 */
static size_t fread_helper(off_t offset, unsigned char *buf,
	size_t len, struct diskimage *d)
{
	off_t curofs;
	size_t totallenread = 0;

	/*  Fast return-path for the case when no overlays are used:  */
	if (d->nr_of_overlays == 0) {
		int res = my_fseek(d->f, offset, SEEK_SET);
		if (res != 0) {
			fatal("[ diskimage__internal_access(): fseek() failed"
			    " on disk id %i \n", d->id);
			return 0;
		}

		return fread(buf, 1, len, d->f);
	}

	/*  Split the read into OVERLAY_BLOCK_SIZE reads:  */
	for (curofs=offset; len != 0;
	    curofs = (curofs | (OVERLAY_BLOCK_SIZE-1)) + 1) {
		/*  Find the overlay, if any, that has this block:  */
		off_t lenread, lentoread;
		int overlay_nr;
		for (overlay_nr = d->nr_of_overlays-1;
		    overlay_nr >= 0; overlay_nr --) {
			if (overlay_has_block(d, overlay_nr, curofs))
				break;
		}

		lentoread = len > OVERLAY_BLOCK_SIZE? OVERLAY_BLOCK_SIZE : len;

		if (overlay_nr >= 0) {
			/*  Read from overlay:  */
			int res = my_fseek(d->overlays[overlay_nr].f_data,
			    curofs, SEEK_SET);
			if (res != 0) {
				fatal("[ diskimage__internal_access(): fseek()"
				    " failed on disk id %i \n", d->id);
				return 0;
			}
			lenread = fread(buf, 1, lentoread,
			    d->overlays[overlay_nr].f_data);
		} else {
			/*  Read from the base disk image:  */
			int res = my_fseek(d->f, curofs, SEEK_SET);
			if (res != 0) {
				fatal("[ diskimage__internal_access(): fseek()"
				    " failed on disk id %i \n", d->id);
				return 0;
			}
			lenread = fread(buf, 1, lentoread, d->f);
		}

		if (lenread != lentoread) {
			fatal("[ INCOMPLETE READ from disk id %i, offset"
			    " %lli ]\n", d->id, (long long)curofs);
		}

		len -= lentoread;
		totallenread += lenread;
		buf += OVERLAY_BLOCK_SIZE;
	}

	return totallenread;
}


/*
 *  diskimage__internal_access():
 *
 *  Read from or write to a struct diskimage.
 *
 *  Returns 1 if the access completed successfully, 0 otherwise.
 */
int diskimage__internal_access(struct diskimage *d, int writeflag,
	off_t offset, unsigned char *buf, size_t len)
{
	ssize_t lendone;

	/*  #206: (Codex/Fable) a legal zero-length access (e.g. SCSI WRITE(10)
	    with transfer length 0) arrives with buf==NULL; treat it as a no-op
	    before the NULL check so it can't exit() the host.  */
	if (len == 0)
		return 1;
	if (buf == NULL) {
		fprintf(stderr, "diskimage__internal_access(): buf = NULL\n");
		exit(1);
	}
	if (d->f == NULL)
		return 0;

	if (writeflag) {
		if (!d->writable)
			return 0;

		lendone = fwrite_helper(offset, buf, len, d);
	} else {
		/*
		 *  Multi-track (CUE/BIN) CD-ROM images use the parsed track
		 *  table to map logical offsets to the right bin file and
		 *  sector; all other (flat file) images use the unchanged
		 *  code paths below.
		 */
		/*
		 *  Special case for CD-ROMs. Actually, this is not needed
		 *  for .iso images, only for physical CDROMS on some OSes,
		 *  such as FreeBSD.
		 */
		if (d->nr_of_tracks > 0)
			lendone = diskimage_access__cue(d, offset, buf, len);
		else if (d->is_a_cdrom)
			lendone = diskimage_access__cdrom(d, offset, buf, len);
		else
			lendone = fread_helper(offset, buf, len, d);

		if (lendone >= 0 && lendone < (ssize_t)len)
			memset(buf + lendone, 0, len - lendone);
	}

	/*
	 *  Incomplete data transfer?
	 *
	 *  If we could not read anything at all, then return failure.
	 *  If we could read a partial block, then return success (with
	 *  the resulting buffer zero-filled at the end).
	 */
#if 0
// TODO: check against full cylinder-size instead
	if (lendone <= 0) {
		fatal("[ diskimage__internal_access(): disk_id %i, offset %lli"
		    ", transfer not completed. len=%i, len_done=%i ]\n",
		    d->id, (long long)offset, (int)len, (int)lendone);
		return 0;
	}
#endif
	return 1;
}


/*
 *  diskimage_access():
 *
 *  Read from or write to a disk image on a machine.
 *
 *  Returns 1 if the access completed successfully, 0 otherwise.
 */
int diskimage_access(struct machine *machine, int id, int type, int writeflag,
	off_t offset, unsigned char *buf, size_t len)
{
	struct diskimage *d = machine->first_diskimage;

	while (d != NULL) {
		if (d->type == type && d->id == id)
			break;
		d = d->next;
	}

	if (d == NULL) {
		fatal("[ diskimage_access(): ERROR: trying to access a "
		    "non-existant %s disk image (id %i)\n",
		    diskimage_types[type], id);
		return 0;
	}

	offset -= d->override_base_offset;
	if (offset < 0 && offset + d->override_base_offset >= 0) {
		debug("[ reading before start of disk image ]\n");
		/*  Returning zeros.  */
		memset(buf, 0, len);
		return 1;
	}

	return diskimage__internal_access(d, writeflag, offset, buf, len);
}


int get_default_disk_type_for_machine(struct machine *machine)
{
	if (machine->machine_type == MACHINE_PMAX ||
	    machine->machine_type == MACHINE_ARC ||
	    machine->machine_type == MACHINE_SGI ||
	    machine->machine_type == MACHINE_LUNA88K ||
	    machine->machine_type == MACHINE_MVME88K)
		return DISKIMAGE_SCSI;

	return DISKIMAGE_IDE;
}


/*
 *  diskimage_add():
 *
 *  Add a disk image.  fname is the filename of the disk image.
 *  The filename may be prefixed with one or more modifiers, followed
 *  by a colon.
 *
 *	b	specifies that this is a bootable device
 *	c	CD-ROM (instead of a normal DISK)
 *	d	DISK (this is the default)
 *	f	FLOPPY (instead of SCSI)
 *	gH;S;	set geometry (H=heads, S=sectors per track, cylinders are
 *		automatically calculated). (This is ignored for floppies.)
 *	i	IDE (instead of SCSI)
 *	oOFS;	set base offset in bytes, when booting from an ISO9660 fs
 *	r       read-only (don't allow changes to the file)
 *	s	SCSI (this is the default)
 *	t	tape
 *	V	add an overlay to a disk image
 *	0-7	force a specific SCSI ID number
 *
 *  machine is assumed to be non-NULL.
 *
 *  Returns an integer >= 0 identifying the disk image. On error, a value less
 *  than zero is returned.
 */
int diskimage_add(struct machine *machine, char *fname)
{
	struct diskimage *d, *d2;
	int id = 0, override_heads=0, override_spt=0;
	int64_t override_base_offset=0;
	char *cp;
	int prefix_b=0, prefix_c=0, prefix_d=0, prefix_f=0, prefix_g=0;
	int prefix_i=0, prefix_r=0, prefix_s=0, prefix_t=0, prefix_id=-1;
	int prefix_o=0, prefix_V=0;
	bool prefix_R = false;

	if (fname == NULL) {
		debugmsg(SUBSYS_DISK, "diskimage_add()", VERBOSITY_ERROR,
		    "NULL ptr");
		return -1;
	}

	/*  Get prefix from fname:  */
	cp = strchr(fname, ':');
	if (cp != NULL) {
		while (fname <= cp) {
			char c = *fname++;
			switch (c) {
			case '0':
			case '1':
			case '2':
			case '3':
			case '4':
			case '5':
			case '6':
			case '7':
				prefix_id = c - '0';
				break;
			case 'b':
				prefix_b = 1;
				break;
			case 'c':
				prefix_c = 1;
				break;
			case 'd':
				prefix_d = 1;
				break;
			case 'f':
				prefix_f = 1;
				break;
			case 'g':
				prefix_g = 1;
				override_heads = atoi(fname);
				while (*fname != '\0' && *fname != ';')
					fname ++;
				if (*fname == ';')
					fname ++;
				override_spt = atoi(fname);
				while (*fname != '\0' && *fname != ';' &&
				    *fname != ':')
					fname ++;
				if (*fname == ';')
					fname ++;
				if (override_heads < 1 ||
				    override_spt < 1) {
					fatal("Bad geometry: heads=%i "
					    "spt=%i\n", override_heads,
					    override_spt);
					return -1;
				}
				break;
			case 'i':
				prefix_i = 1;
				break;
			case 'o':
				prefix_o = 1;
				override_base_offset = atoi(fname);
				while (*fname != '\0' && *fname != ':'
				    && *fname != ';')
					fname ++;
				if (*fname == ':' || *fname == ';')
					fname ++;
				if (override_base_offset < 0) {
					fatal("Bad base offset: %" PRIi64
					    "\n", override_base_offset);
					return -1;
				}
				break;
			case 'R':
				prefix_R = true;
				break;
			case 'r':
				prefix_r = 1;
				break;
			case 's':
				prefix_s = 1;
				break;
			case 't':
				prefix_t = 1;
				break;
			case 'V':
				prefix_V = 1;
				break;
			case ':':
				break;
			default:
				fprintf(stderr, "diskimage_add(): invalid "
				    "prefix char '%c'\n", c);
				return -1;
			}
		}
	}

	/*  Allocate a new diskimage struct:  */
	CHECK_ALLOCATION(d = (struct diskimage *) malloc(sizeof(struct diskimage)));
	memset(d, 0, sizeof(struct diskimage));

	if (prefix_i + prefix_f + prefix_s > 1) {
		fprintf(stderr, "Invalid disk image prefix(es). You can"
		    "only use one of i, f, and s\nfor each disk image.\n");
		exit(1);
	}

	if (prefix_i)
		d->type = DISKIMAGE_IDE;
	if (prefix_f)
		d->type = DISKIMAGE_FLOPPY;
	if (prefix_s)
		d->type = DISKIMAGE_SCSI;

	if (prefix_V && prefix_R) {
		debugmsg(SUBSYS_DISK, "", VERBOSITY_ERROR,
		    "'V' and 'R' prefixes can not be combined!");
		return -1;
	}

	/*  Special case: Add an overlay for an already added disk image:  */
	if (prefix_V) {
		struct diskimage *dx = machine->first_diskimage;

		if (prefix_id < 0) {
			debugmsg(SUBSYS_DISK, "", VERBOSITY_ERROR,
			    "The 'V' disk image prefix requires"
			    " a disk ID to also be supplied.");
			return -1;
		}

		if (d->type == DISKIMAGE_UNKNOWN)
			d->type = get_default_disk_type_for_machine(machine);

		while (dx != NULL) {
			if (d->type == dx->type && prefix_id == dx->id)
				break;
			dx = dx->next;
		}

		/*  Free the preliminary d struct:  */
		free(d);

		if (dx == NULL) {
			fprintf(stderr, "Bad ID supplied for overlay?\n");
			return -1;
		}

		if (!diskimage_add_overlay(dx, fname, false)) {
			debugmsg(SUBSYS_DISK, "", VERBOSITY_ERROR,
			    "could not add overlay name '%s'",
			    fname);
			return -1;
		}

		/*  Return the ID of the disk image, even though no disk
		    image was added.  */
		return dx->id;
	}

	/*  Add the new disk image in the disk image chain:  */
	d2 = machine->first_diskimage;
	if (d2 == NULL) {
		machine->first_diskimage = d;
	} else {
		while (d2->next != NULL)
			d2 = d2->next;
		d2->next = d;
	}

	if (prefix_o)
		d->override_base_offset = override_base_offset;

	CHECK_ALLOCATION(d->fname = strdup(fname));

	d->logical_block_size = 512;

	/*
	 *  Is this a tape, CD-ROM or a normal disk?
	 *
	 *  An intelligent guess, if no prefixes are used, would be that
	 *  filenames ending with .iso or .cdr are CD-ROM images.
	 */
	if (prefix_t) {
		d->is_a_tape = 1;
	} else {
		if (prefix_c ||
		    ((strlen(d->fname) > 4 &&
		    (strcasecmp(d->fname + strlen(d->fname) - 4, ".cdr") == 0 ||
		    strcasecmp(d->fname + strlen(d->fname) - 4, ".iso") == 0))
		    && !prefix_d)
		   ) {
			d->is_a_cdrom = 1;

			/*
			 *  This is tricky. Should I use 512 or 2048 here?
			 *  NetBSD/pmax 1.6.2 and Ultrix likes 512 bytes
			 *  per sector, but NetBSD 2.0_BETA suddenly ignores
			 *  this value and uses 2048 instead.
			 *
			 *  OpenBSD/arc doesn't like 2048, it requires 512
			 *  to work correctly.
			 *
			 *  TODO
			 */

#if 0
			if (machine->machine_type == MACHINE_PMAX)
				d->logical_block_size = 512;
			else
				d->logical_block_size = 2048;
#endif
			d->logical_block_size = 512;
		}
	}

	/*
	 *  Multi-track CD-ROM image in CUE/BIN format?
	 *
	 *  Detected by a ".cue" filename extension, or, for files explicitly
	 *  marked as CD-ROM using the 'c' prefix, by the file contents
	 *  beginning with a cue sheet keyword.  On successful parsing, reads
	 *  are mapped through the parsed track table (see
	 *  diskimage_access__cue()), and logical offset 0 corresponds to the
	 *  first data track, so ISO9660 booting uses that track by default.
	 *  On failure, a warning has already been printed, nr_of_tracks
	 *  remains 0, and the file is treated as a flat image, as before.
	 */
	if (!d->is_a_tape) {
		bool looks_like_cue = strlen(d->fname) > 4 &&
		    strcasecmp(d->fname + strlen(d->fname) - 4, ".cue") == 0;

		if (!looks_like_cue && prefix_c)
			looks_like_cue = diskimage__looks_like_cue(d->fname);

		if (looks_like_cue && diskimage__parse_cue(d)) {
			d->is_a_cdrom = 1;

			/*  Same logical block size as for other CD-ROM
			    images; see the comment above:  */
			d->logical_block_size = 512;
		}
	}

	if (prefix_g) {
		d->chs_override = 1;
		d->heads = override_heads;
		d->sectors_per_track = override_spt;
	}

	if (!diskimage_recalc_size(d))
		debugmsg(SUBSYS_DISK, "", VERBOSITY_WARNING,
		    "diskimage_recalc_size() failed!");

	if (d->type == DISKIMAGE_UNKNOWN)
		d->type = get_default_disk_type_for_machine(machine);

	d->rpms = 3600;

	if (prefix_b)
		d->is_boot_device = 1;

	bool readable = access(fname, R_OK) == 0? 1 : 0;
	d->writable = access(fname, W_OK) == 0? 1 : 0;

	if (!readable) {
		debugmsg(SUBSYS_DISK, "", VERBOSITY_ERROR,
		    "could not access '%s': %s", fname, strerror(errno));
		return -1;
	}

	if (d->is_a_cdrom || prefix_r) {
		d->writable = 0;
	} else if (!d->writable) {
		if (prefix_R) {
			d->writable = 1;
		} else {
			debugmsg(SUBSYS_DISK, "", VERBOSITY_ERROR,
			    "'%s' is read-only in the host file system.\n"
			    "Use the r: prefix to indicate that the file should be treated\n"
			    "as read-only, the R: prefix to use a temporary overlay (allowing\n"
			    "guest operating systems to write to that temporary overlay), or\n"
			    "make the file writable.",
			    d->fname);
			return -1;
		}
	}

	d->f = fopen(fname, d->writable && !prefix_R ? "r+" : "r");
	if (d->f == NULL) {
		debugmsg(SUBSYS_DISK, "", VERBOSITY_ERROR,
		    "could not open '%s' for reading%s: %s",
		    fname,
		    d->writable? " and writing" : "",
		    strerror(errno));
		return -1;
	}

	/*  Calculate which ID to use:  */
	if (prefix_id == -1) {
		int start = 0;
		int delta = 1;
		
		if (machine->machine_type == MACHINE_LUNA88K) {
			start = 6;
			delta = -1;
		}
		
		int free = start;
		
		bool collision = true;

		while (collision) {
			collision = false;
			d2 = machine->first_diskimage;
			while (d2 != NULL) {
				/*  (don't compare against ourselves :)  */
				if (d2 == d) {
					d2 = d2->next;
					continue;
				}
				if (d2->id == free && d2->type == d->type) {
					collision = true;
					break;
				}
				d2 = d2->next;
			}
			if (!collision)
				id = free;
			else
				free += delta;
		}
		
		if (id < 0) {
			fprintf(stderr, "Too many IDs used?\n");
			exit(1);
		}
	} else {
		id = prefix_id;
		d2 = machine->first_diskimage;
		while (d2 != NULL) {
			/*  (don't compare against ourselves :)  */
			if (d2 == d) {
				d2 = d2->next;
				continue;
			}
			if (d2->id == id && d2->type == d->type) {
				fprintf(stderr, "disk image id %i "
				    "already in use\n", id);
				exit(1);
			}
			d2 = d2->next;
		}
	}

	d->id = id;

	if (prefix_R) {
		char tmpname[1000];
		const char* tmpdir = getenv("TMPDIR");
		if (tmpdir == NULL)
			tmpdir = "/tmp";
		
		int old_umask = umask(077);

		/*  #115 (OB-25): create the overlay data file with an
		    UNPREDICTABLE name via mymkstemp() (random suffix from
		    /dev/urandom, atomic O_CREAT|O_EXCL create), then create its
		    ".map" exclusively.  A guessable name let a local attacker
		    pre-plant a symlink at the path before diskimage_add_overlay()
		    reopens the files by name (TOCTOU).  */
		snprintf(tmpname, sizeof(tmpname),
		    "%s/gxemul.%i.overlay.XXXXXXXX", tmpdir, d->id);
		{
			int ovfd = mymkstemp(tmpname);
			if (ovfd < 0) {
				perror(tmpname);
				umask(old_umask);
				return -1;
			}
			close(ovfd);
		}

		{
			char mapname[1040];
			FILE* f_img_map;
			snprintf(mapname, sizeof(mapname), "%s.map", tmpname);
			f_img_map = fopen(mapname, "wx");
			if (f_img_map == NULL) {
				perror(mapname);
				unlink(tmpname);
				umask(old_umask);
				return -1;
			}
			fclose(f_img_map);
		}

		umask(old_umask);

		if (!diskimage_add_overlay(d, tmpname, true)) {
			debugmsg(SUBSYS_DISK, "", VERBOSITY_ERROR,
			    "could not add overlay name '%s'",
			    fname);
			return -1;
		}
	}

	return id;
}


/*
 *  diskimage_bootdev():
 *
 *  Returns the disk id of the device which we're booting from.  If typep is
 *  non-NULL, the type is returned as well.
 *
 *  If no disk was used as boot device, then -1 is returned. (In practice,
 *  this is used to fake network (tftp) boot.)
 */
int diskimage_bootdev(struct machine *machine, int *typep)
{
	struct diskimage *d;

	d = machine->first_diskimage;
	while (d != NULL) {
		if (d->is_boot_device) {
			if (typep != NULL)
				*typep = d->type;
			return d->id;
		}
		d = d->next;
	}

	d = machine->first_diskimage;
	if (d != NULL) {
		if (typep != NULL)
			*typep = d->type;
		return d->id;
	}

	return -1;
}


/*
 *  diskimage_getname():
 *
 *  Returns 1 if a valid disk image name was returned, 0 otherwise.
 */
int diskimage_getname(struct machine *machine, int id, int type,
	char *buf, size_t bufsize)
{
	struct diskimage *d = machine->first_diskimage;

	if (buf == NULL)
		return 0;

	while (d != NULL) {
		if (d->type == type && d->id == id) {
			char *p = strrchr(d->fname, '/');
			if (p == NULL)
				p = d->fname;
			else
				p ++;
			snprintf(buf, bufsize, "%s", p);
			return 1;
		}
		d = d->next;
	}
	return 0;
}


/*
 *  diskimage_is_a_cdrom():
 *
 *  Returns 1 if a disk image is a CDROM, 0 otherwise.
 */
int diskimage_is_a_cdrom(struct machine *machine, int id, int type)
{
	struct diskimage *d = machine->first_diskimage;

	while (d != NULL) {
		if (d->type == type && d->id == id)
			return d->is_a_cdrom;
		d = d->next;
	}
	return 0;
}


/*
 *  diskimage_is_a_tape():
 *
 *  Returns 1 if a disk image is a tape, 0 otherwise.
 *
 *  (Used in src/machine.c, to select 'rz' vs 'tz' for DECstation
 *  boot strings.)
 */
int diskimage_is_a_tape(struct machine *machine, int id, int type)
{
	struct diskimage *d = machine->first_diskimage;

	while (d != NULL) {
		if (d->type == type && d->id == id)
			return d->is_a_tape;
		d = d->next;
	}
	return 0;
}


/*
 *  diskimage_dump_info():
 *
 *  Debug dump of all diskimages that are loaded for a specific machine.
 */
void diskimage_dump_info(struct machine *machine)
{
	struct diskimage *d = machine->first_diskimage;

	while (d != NULL) {
		debugmsg(SUBSYS_MACHINE, "diskimage", VERBOSITY_INFO, "%s", d->fname);

		debug_indentation(1);

		switch (d->type) {
		case DISKIMAGE_SCSI:
			debug("SCSI");
			break;
		case DISKIMAGE_IDE:
			debug("IDE");
			break;
		case DISKIMAGE_FLOPPY:
			debug("FLOPPY");
			break;
		default:
			debug("UNKNOWN type %i", d->type);
		}

		debug(" %s", d->is_a_tape? "TAPE" :
			(d->is_a_cdrom? "CD-ROM" : "DISK"));
		debug(" id %i, ", d->id);
		debug("%s, ", d->writable? "read/write" : "read-only");

		int64_t s = d->nr_of_logical_blocks * d->logical_block_size;

		if (d->type == DISKIMAGE_FLOPPY)
			debug("%lli KB", (long long) (s / 1024));
		else
			debug("%lli MB", (long long) (s / 1048576));

		if (d->type == DISKIMAGE_FLOPPY || d->chs_override)
			debug(" (CHS=%i,%i,%i)", d->cylinders, d->heads,
			    d->sectors_per_track);
		else
			debug(" (%lli %i-byte blocks)", (long long)d->nr_of_logical_blocks, d->logical_block_size);

		if (d->is_boot_device)
			debug(" (BOOT)");
		debug("\n");

		debug_indentation(1);

		for (int i=0; i<d->nr_of_overlays; i++) {
			debug("overlay %i: %s\n",
			    i, d->overlays[i].overlay_basename);
		}

		if (d->nr_of_tracks > 0) {
			debug("%i track(s); first data track at disc sector"
			    " %lli = logical offset 0:\n",
			    d->nr_of_tracks,
			    (long long) d->first_data_track_lba);

			for (int i=0; i<d->nr_of_tracks; i++) {
				struct diskimage_track *t = &d->track[i];
				debug("track %2i: %s, disc sectors %lli-%lli,"
				    " %i bytes/sector, \"%s\" @ 0x%llx\n",
				    t->track_nr,
				    t->is_data? "DATA " : "AUDIO",
				    (long long) t->start_lba,
				    (long long) (t->start_lba +
					t->nr_of_sectors - 1),
				    t->sector_size,
				    d->track_file_name[t->file_index],
				    (long long) t->file_byte_offset);
			}
		}

		debug_indentation(-2);

		d = d->next;
	}
}

