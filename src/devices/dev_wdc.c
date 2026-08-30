/*
 *  Copyright (C) 2004-2009  Anders Gavare.  All rights reserved.
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
 *  COMMENT: Standard "wdc" IDE controller
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "cpu.h"
#include "device.h"
#include "diskimage.h"
#include "machine.h"
#include "memory.h"
#include "misc.h"

#include "thirdparty/wdcreg.h"


#define	DEV_WDC_LENGTH		8
#define	WDC_TICK_SHIFT		14
#define	WDC_MAX_SECTORS		512
#define	WDC_INBUF_SIZE		(512*(WDC_MAX_SECTORS+1))

extern int quiet_mode;

/*  #define debug fatal  */

struct wdc_data {
	struct interrupt irq;
	int		addr_mult;
	int		base_drive;
	int		data_debug;
	int		io_enabled;

	/*  Cached values:  */
	int		cyls[2];
	int		heads[2];
	int		sectors_per_track[2];

	unsigned char	*inbuf;
	int		inbuf_head;
	int		inbuf_tail;

	int		int_assert;

	/*  #337: latch each replaced exit(1) so a guest that retries in a
	    loop cannot flood the host log -- the same flood #265 caused and
	    #269 had to undo.  */
	int		warned_badlen;
	int		warned_empty_drain;
	int		warned_atapi_err;
	int		warned_null_xfer;
	int		warned_atapi_dataout;

	/*  #464 (wdcflood): the SIX fatal() this file still emitted without bound.
	    #337 latched "each replaced exit(1)"; these were always fatal()
	    and never exit(1), so they fell outside that round's enumeration.
	    Measured: 20 stores -> 20 host lines with AND without -q, and the
	    OVER-READ site at 500 iterations produced 2000 lines / 158,449
	    bytes.  Artifacts: regress/artifacts/wdcflood/witness_20260825/
	    {fr_no__q,fr_with__q,n3}.out.  (An earlier wording said "the read
	    path", which points a reader at the non-8-bit READ guard instead;
	    n3.out is 2000x "reading too much", i.e. the ring over-read.)
	    fatal() has no early-out (core/debugmsg.c:384-390, against
	    debug()'s at core/debugmsg.c:375), so -q cannot silence it.

	    SIX FLAGS, NOT FOUR.  Pairing the ring halves or the two width
	    checks was proposed and is wrong: #337's own shared warned_badlen
	    spans the two arms of ONE ENDIANNESS BRANCH (the
	    `cpu->byte_order == EMUL_LITTLE_ENDIAN` test in the wd_data write
	    arm below, and its else),
	    which are mutually exclusive at runtime, so sharing there loses
	    nothing.  These six can all fire in one session.  Measured
	    corroboration: in the session that produced the over-read, no
	    PRODUCER operation ran at all, so no overrun could have preceded
	    it -- the ring halves are causally independent.

	    (An earlier draft warranted that with "it fires with NO DISK
	    ATTACHED", which is a NON-SEQUITUR: wdc_addtoinbuf is reachable
	    from the guest DATA-WRITE path below, so a diskless guest can
	    fill the ring perfectly well.  The conclusion holds; the reason
	    given for it did not, and a wrong reason gets reused.)

	    fatal() is KEPT rather than downgraded, on this fork's own
	    recorded warrant at dev_asc.c:248-257: under -q verbosity settles
	    at VERBOSITY_ERROR, so a WARNING-level debugmsg would be INVISIBLE
	    to the boot-log hygiene grep and an ERROR-level one would trip
	    #261's break-on-ERROR.  */
	int		warned_inbuf_overrun;
	int		warned_inbuf_overread;
	int		warned_unimpl_cmd;
	int		warned_nonbyte_write;
	int		warned_nonbyte_read;
	int		warned_data_unexpected;

	int		write_in_progress;
	int		write_count;
	int64_t		write_offset;

	int		error;
	int		precomp;
	int		seccnt;
	int		sector;
	int		cyl_lo;
	int		cyl_hi;
	int		sectorsize;
	int		lba;
	int		drive;
	int		head;
	int		cur_command;

	int		atapi_cmd_in_progress;
	int		atapi_phase;
	struct scsi_transfer *atapi_st;
	int		atapi_len;
	size_t		atapi_received;

	unsigned char	identify_struct[512];
};


#define COMMAND_RESET	0x100


DEVICE_TICK(wdc)
{ 
	struct wdc_data *d = (struct wdc_data *) extra;

	if (d->int_assert)
		INTERRUPT_ASSERT(d->irq);
}


/*
 *  wdc_set_io_enabled():
 *
 *  Set io_enabled to zero to disable the I/O registers temporarily (e.g.
 *  used by PCI code in NetBSD to detect whether multiple controllers collide
 *  in I/O space).
 *
 *  Return value is old contents of the io_enabled variable.
 */
int wdc_set_io_enabled(struct wdc_data *d, int io_enabled)
{
	int old = d->io_enabled;
	d->io_enabled = io_enabled;
	return old;
}


/*
 *  wdc_addtoinbuf():
 *
 *  Write to the inbuf at its head, read at its tail.
 */
static void wdc_addtoinbuf(struct wdc_data *d, int c)
{
	/*  #484: REFUSE BEFORE THE STORE.  The invariant this establishes is
	    THE RING'S OCCUPANCY IS SOUND -- deliberately not the weaker "full is
	    distinguishable from empty".  MANY sites depend on the first and only
	    this function implements the second; the readers are derivable at any
	    commit with
	
	        grep -n 'inbuf_head [=!]= d->inbuf_tail' dev_wdc.c   (and the
	        reversed and subtractive forms; one site writes tail - head)
	
	    rather than from a number here.  An earlier draft wrote SIX while the
	    checkpoint said FOUR, and the two cannot be reconciled without first
	    deciding whether to count SITES or DECISIONS -- which is how the wrong
	    number got written in the first place.  A count in a comment ages; a
	    deriver does not.  Naming the WEAK property here would invite a later
	    edit to trade the strong one away, which is the whole reason the
	    invariant is stated as occupancy rather than as distinguishability.
	
	    One slot is sacrificed, so head == tail now means EMPTY, full stop, and
	    every reader below becomes sound with no struct change and no new field.
	    Modelled on dev_pckbc.c's pckbc_add_code(), which refuses at
	    next == tail for exactly this defect (#288).
	
	    *** THE RETURN IS OUTSIDE THE LATCH, AND THAT IS NOT A STYLE CHOICE.
	    ***  Nested inside it, the FIRST overflow is refused and every later
	    push sees warned_inbuf_overrun == 1, skips the whole condition, and
	    walks head onto tail -- the defect restored.  Measured as mutant Md3,
	    13/16 in the panel seat's own table (its Md3), and 12/15 when I rebuilt
	    it against these bytes as Md_inside -- DIFFERENT TABLES, and the figure is
	    cited with the one that produced it rather than blended.  Both tables kill
	    it, which is the claim.  wdc_get_inbuf() below already forbids the same
	    shape in the
	    CONSUMER for the same reason, so a maintainer copying that function's
	    structure into this one writes the bug by accident.
	
	    Written WITHOUT an `int next` temporary on purpose.  The obvious form
	    (`next = (head+1) % SIZE; ... head = next;`) deletes the masked advance
	    below and makes the mask inside `next` safety-critical; dropping it is a
	    one-token simplification and measured as an actual heap overflow
	    (`free(): invalid next size`).  Keeping both statements untouched makes
	    that edit inexpressible as a SINGLE change -- though not impossible: the
	    modulo in the advance statement below is still removable on its own.
	    What it closes is the obvious consolidation path, which is what a
	    maintainer actually takes.
	
	    Drop-NEWEST, not drop-oldest, by reason: the surviving consumers key on
	    the FRONT of the stream (the CDB dispatch reads bytes 0-11; the sector
	    drain reads aligned runs from tail), so overwriting the oldest byte
	    silently re-aims a 512-byte disk write at data the guest never staged
	    there.  Both in-tree ring precedents drop newest.  Measured: drop-oldest
	    scores 13/16 IN THE PANEL SEAT'S TABLE (its Md4) and is invisible to every
	    occupancy- and DRQ-shaped row there.  I did NOT rebuild that mutant against
	    these bytes, so it is cited as the seat's measurement and not as this
	    round's -- artifacts/wdcringambig/killtable_20260827/.
	
	    COST, measured and named rather than discovered later: WDC_INBUF_SIZE is
	    512*513, so the saturated occupancy 262655 is never 0 (mod 512) while the
	    old 262656 always was.  A saturated ring's pending sector write therefore
	    stalls instead of committing its oldest sector.  It is reachable only
	    through the width-mixing pathology that fills the ring in the first
	    place, and a stalled write is strictly better than a write of bytes the
	    guest did not supply.  */
	if ((d->inbuf_head + 1) % WDC_INBUF_SIZE == d->inbuf_tail) {
		if (!d->warned_inbuf_overrun) {
			d->warned_inbuf_overrun = 1;
			fatal("[ wdc_addtoinbuf(): WARNING! wdc inbuf overrun!"
			    " Increase WDC_MAX_SECTORS. ]\n");
		}
		return;
	}

	d->inbuf[d->inbuf_head] = c;

	d->inbuf_head = (d->inbuf_head + 1) % WDC_INBUF_SIZE;
	/*  #484: the #464 POST-HOC check that stood here is DELETED, and the
	    warrant is a measurement rather than an argument.

	    It tested `head == tail` AFTER the advance.  The guard at the top of
	    this function makes `(head + 1) % SIZE != tail` a precondition of
	    reaching the store, so after the advance head != tail always: the
	    branch was unreachable.  MEASURED TRUE 0 TIMES across 12,232 producer
	    refusals over the whole 122-row suite.

	    *** IT WAS KEPT AT FIRST, ON THE WARRANT THAT DEAD CODE WITH A TRUE
	    COMMENT COSTS NOTHING.  THE COMMENT WAS FALSE IN FOUR CLAIMS. ***  It
	    said head == tail means both empty and full with no disambiguator
	    (this round added one); that the corrupting store is the next one and
	    is silent (it is now refused and announced); that the bulk paths never
	    compare the pointers (one now does); and that no detector row claims
	    ring health (R1-R9 claim exactly that).  A maintainer reading it would
	    have concluded the ring is still ambiguous.  Removing code needs a
	    warrant in this fork, and a measured-dead branch under a four-times-
	    false comment is the clearest one there is.  */
}


/*
 *  wdc_get_inbuf():
 *
 *  Read from the tail of inbuf.
 */
static uint64_t wdc_get_inbuf(struct wdc_data *d)
{
	int c = d->inbuf[d->inbuf_tail];

	if (d->inbuf_head == d->inbuf_tail) {
		/*  #464: the guard wraps the fatal() ONLY.
		    *** THE `return` MUST STAY OUTSIDE IT. ***  Nested inside,
		    the SECOND over-read falls through to the tail advance
		    below and corrupts the ring pointer -- a fix strictly worse
		    than the flood it removes.  Row `overread -1` pins it.
		    See `wdcringambig`: after an overrun this predicate is
		    unsound, because a FULL ring is indistinguishable from an
		    empty one.  */
		if (!d->warned_inbuf_overread) {
			d->warned_inbuf_overread = 1;
			fatal("[ wdc: WARNING! someone is reading too much "
			    "from the wdc inbuf! ]\n");
		}
		return (uint64_t) -1;
	}

	d->inbuf_tail = (d->inbuf_tail + 1) % WDC_INBUF_SIZE;
	return c;
}


/*
 *  wdc_initialize_identify_struct():
 */
static void wdc_initialize_identify_struct(struct cpu *cpu, struct wdc_data *d)
{
	uint64_t total_size;
	int flags, cdrom = 0;
	char namebuf[40];

	total_size = diskimage_getsize(cpu->machine, d->drive + d->base_drive,
	    DISKIMAGE_IDE);
	if (diskimage_is_a_cdrom(cpu->machine, d->drive + d->base_drive,
	    DISKIMAGE_IDE))
		cdrom = 1;

	memset(d->identify_struct, 0, sizeof(d->identify_struct));

	/*  Offsets are in 16-bit WORDS!  High byte, then low.  */

	/*  0: general flags  */
	flags = 1 << 6;	/*  Fixed  */
	if (cdrom)
		flags = 0x8580;		/*  ATAPI, CDROM, removable  */
	d->identify_struct[2 * 0 + 0] = flags >> 8;
	d->identify_struct[2 * 0 + 1] = flags;

	/*  1: nr of cylinders  */
	d->identify_struct[2 * 1 + 0] = d->cyls[d->drive] >> 8;
	d->identify_struct[2 * 1 + 1] = d->cyls[d->drive];

	/*  3: nr of heads  */
	d->identify_struct[2 * 3 + 0] = d->heads[d->drive] >> 8;
	d->identify_struct[2 * 3 + 1] = d->heads[d->drive];

	/*  6: sectors per track  */
	d->identify_struct[2 * 6 + 0] = d->sectors_per_track[d->drive] >> 8;
	d->identify_struct[2 * 6 + 1] = d->sectors_per_track[d->drive];

	/*  10-19: Serial number  */
	memcpy(&d->identify_struct[2 * 10], "#0                  ", 20);

	/*  23-26: Firmware version  */
	memcpy(&d->identify_struct[2 * 23], "1.0     ", 8);

	/*  27-46: Model number  */
	if (diskimage_getname(cpu->machine, d->drive + d->base_drive,
	    DISKIMAGE_IDE, namebuf, sizeof(namebuf))) {
		size_t i;
		for (i=0; i<sizeof(namebuf); i++)
			if (namebuf[i] == 0) {
				for (; i<sizeof(namebuf); i++)
					namebuf[i] = ' ';
				break;
			}
		memcpy(&d->identify_struct[2 * 27], namebuf, 40);
	} else
		memcpy(&d->identify_struct[2 * 27],
		    "Fake GXemul IDE disk                    ", 40);

	/*  47: max sectors per multitransfer  */
	d->identify_struct[2 * 47 + 0] = 0x80;
	d->identify_struct[2 * 47 + 1] = 128;

	/*  49: capabilities:  */
	/*  (0x200 = LBA, 0x100 = DMA support.)  */
	d->identify_struct[2 * 49 + 0] = 0;
	d->identify_struct[2 * 49 + 1] = 0;

	/*  51: PIO timing mode.  */
	d->identify_struct[2 * 51 + 0] = 0x00;	/*  ?  */
	d->identify_struct[2 * 51 + 1] = 0x00;

	/*  53: 0x02 = fields 64-70 valid, 0x01 = fields 54-58 valid  */
	d->identify_struct[2 * 53 + 0] = 0x00;
	d->identify_struct[2 * 53 + 1] = 0x02;

	/*
	 *  #405: `% 255` where `& 255` is meant, on six of these eight lines.
	 *
	 *  The two that were already right are the ones whose operand is small:
	 *  `(sectors) & 255` cannot exceed a byte anyway. Every other line shifts
	 *  first and does NOT pre-mask, so its operand is a multi-byte quantity and
	 *  `% 255` is not byte extraction that occasionally coincides -- it is a
	 *  base-256 digit sum. Measured in closed form, 0 counterexamples over 2^26:
	 *      x % 255 == ((x >> 8) + (x & 255)) % 255
	 *
	 *  So this is not a rare corner. Above the threshold it is wrong 100.0000%
	 *  of the time; the 0.39% of sizes where the >>8 byte is accidentally right
	 *  are exactly the ones where >>16 is wrong. The announced capacity lands
	 *  either side of the truth, worst case reporting ZERO SECTORS.
	 *
	 *  Smallest size at which any byte diverges is 65,280 sectors -- but
	 *  diskimage_recalc_size()'s closing whole-cylinder round-up (the shared
	 *  bytespercyl block, hoisted there by #414) rounds every image up to
	 *  whole cylinders, so that exact count is unreachable. The smallest
	 *  REACHABLE divergence is 33,546,240 bytes (65 cylinders), where a 32 MB
	 *  disk announces itself as 120 KB.
	 *
	 *  The byte order is NOT a second defect and was deliberately left alone.
	 *  The convention is stated at the top of this function ("Offsets are in
	 *  16-bit WORDS!  High byte, then low"), the geometry words follow it, the
	 *  transmit loop in wdc_command()'s WDCC_IDENTIFY case pushes [i+1] before
	 *  [i+0], and dev_wdc_access()'s wd_data read reassembles (high << 8) | low.
	 *  Two panel seats called it a defect from the snippet alone; two that read
	 *  the file found it consistent, and a later pass CONFIRMED it by executing
	 *  the whole guest path: both the LE and BE branches, plus memory_writemax64,
	 *  land the SAME two bytes in guest memory, so the device layer is
	 *  byte-stream-preserving. The 57-vs-58 WORD order is not establishable from
	 *  this tree at all -- there is no ATA specification here -- so a mask-only
	 *  correction is exactly as much as the source can justify.
	 *
	 *  #408: THE CITATIONS ABOVE NAME CONSTRUCTS, NOT LINE NUMBERS, AND THAT IS
	 *  DELIBERATE.  #405 cited lines that its own inserted comment had shifted by
	 *  +31.  #407 wrote a correction saying "re-read every line reference AFTER
	 *  the edit is in place" -- and then made the identical error, because that
	 *  correction was itself +9 lines and every number it "fixed" was re-read from
	 *  the pre-edit file.  Two rounds, same mechanism, and the second one had the
	 *  lesson written down in front of it.  A line number inside a file the same
	 *  commit edits is measured against the file it was written in, not the one
	 *  that ships; naming the construct survives every future edit instead.
	 */
	/*  57-58: current capacity in sectors  */
	d->identify_struct[2 * 58 + 0] = ((total_size / 512) >> 24) & 255;
	d->identify_struct[2 * 58 + 1] = ((total_size / 512) >> 16) & 255;
	d->identify_struct[2 * 57 + 0] = ((total_size / 512) >> 8) & 255;
	d->identify_struct[2 * 57 + 1] = (total_size / 512) & 255;

	/*  60-61: total nr of addressable sectors  */
	d->identify_struct[2 * 61 + 0] = ((total_size / 512) >> 24) & 255;
	d->identify_struct[2 * 61 + 1] = ((total_size / 512) >> 16) & 255;
	d->identify_struct[2 * 60 + 0] = ((total_size / 512) >> 8) & 255;
	d->identify_struct[2 * 60 + 1] = (total_size / 512) & 255;

	/*  64: Advanced PIO mode support. 0x02 = mode4, 0x01 = mode3  */
	d->identify_struct[2 * 64 + 0] = 0x00;
	d->identify_struct[2 * 64 + 1] = 0x03;

	/*  67, 68: PIO timing  */
	d->identify_struct[2 * 67 + 0] = 0;
	d->identify_struct[2 * 67 + 1] = 120;
	d->identify_struct[2 * 68 + 0] = 0;
	d->identify_struct[2 * 68 + 1] = 120;
}


/*
 *  wdc__read():
 */
void wdc__read(struct cpu *cpu, struct wdc_data *d)
{
#define MAX_SECTORS_PER_CHUNK	64
	const int max_sectors_per_chunk = MAX_SECTORS_PER_CHUNK;
	unsigned char buf[512 * MAX_SECTORS_PER_CHUNK];
	int i, cyl = d->cyl_hi * 256+ d->cyl_lo;
	int count = d->seccnt? d->seccnt : 256;
	uint64_t offset = 512 * (d->sector - 1
	    + (int64_t)d->head * d->sectors_per_track[d->drive] +
	    (int64_t)d->heads[d->drive] * d->sectors_per_track[d->drive] * cyl);

#if 0
	/*  LBA:  */
	if (d->lba)
		offset = 512 * (((d->head & 0xf) << 24) + (cyl << 8)
		    + d->sector);
	printf("WDC read from offset %lli\n", (long long)offset);
#endif

	while (count > 0) {
		int to_read = count > max_sectors_per_chunk?
		    max_sectors_per_chunk : count;

		/*  TODO: result code from the read?  */

		/*  #484: AN OCCUPANCY BOUND.  The test below is a BUFFER bound -- does
		    the linear write fit inside the allocation -- and it is NOT an
		    occupancy bound: this arm bypasses wdc_addtoinbuf() entirely and
		    compares the two pointers nowhere, so it can step head past tail and
		    overwrite unread bytes in silence.

		    MEASURED, AND THE QUALIFIER IS PART OF THE MEASUREMENT: driving the
		    FUNCTION with a prefilled ring gives occupancy 262156 -> 1548, a
		    plausible-looking number, with 1548 bytes of unread data replaced by
		    disk contents.

		    *** BUT 'REACHABLE' IS THE WRONG WORD AND THE READING SEATS WERE RIGHT
		    ABOUT THE PRODUCT. ***  `wdc__read()` has exactly ONE caller and it sits
		    AFTER `wdc_new_command_reset()`, so the ring is EMPTY on every real
		    invocation.  The prefilled state the rows build is a FUNCTION state, not
		    a guest route.  The arm is occupancy-blind AS CODE; this guard is
		    DEFENSIVE, and it is licensed by the caller invariant being unwritten
		    anywhere else -- not by a live defect.  A second seat then MEASURED
		    that too: 512 READ/READMULTI commands driven only through the guest
		    register interface, ring pre-stuffed each time, reached this guard
		    1280 times and FIRED IT ZERO TIMES.
		
		    The `- 1` is the sacrificed slot and is load-bearing: without it this
		    guard admits a refill of exactly room+1 bytes, which is the ONLY input
		    that distinguishes the two forms (measured 15/16, one row).
		
		    It is the SAME admission predicate as the producer's, and that is the
		    reason both hunks are one round: split them and the two arms disagree
		    about what "full" means, which is an incoherence the split itself
		    creates.  */
		if (512 * to_read > (d->inbuf_tail - d->inbuf_head - 1 +
		    WDC_INBUF_SIZE) % WDC_INBUF_SIZE) {
			if (!d->warned_inbuf_overrun) {
				d->warned_inbuf_overrun = 1;
				/*  #484: names THIS function, not the producer.  The
				    shared latch already removes the only other way to
				    tell the two sites apart, so a message pointing at
				    a guard that did not fire is a wrong record in
				    product output.  */
				fatal("[ wdc__read(): WARNING! wdc inbuf would"
				    " overrun; refill refused. Increase"
				    " WDC_MAX_SECTORS. ]\n");
			}
			break;
		}

		if (d->inbuf_head + 512 * to_read <= WDC_INBUF_SIZE) {
			diskimage_access(cpu->machine, d->drive + d->base_drive,
			    DISKIMAGE_IDE, 0, offset,
			    d->inbuf + d->inbuf_head, 512 * to_read);
			d->inbuf_head += 512 * to_read;
			if (d->inbuf_head == WDC_INBUF_SIZE)
				d->inbuf_head = 0;
		} else {
			diskimage_access(cpu->machine, d->drive + d->base_drive,
			    DISKIMAGE_IDE, 0, offset, buf, 512 * to_read);
			for (i=0; i<512 * to_read; i++)
				wdc_addtoinbuf(d, buf[i]);
		}

		offset += 512 * to_read;
		count -= to_read;
	}

	d->int_assert = 1;
}


/*
 *  wdc__write():
 */
void wdc__write(struct cpu *cpu, struct wdc_data *d)
{
	int cyl = d->cyl_hi * 256+ d->cyl_lo;
	int count = d->seccnt? d->seccnt : 256;
	uint64_t offset = 512 * (d->sector - 1
	    + (int64_t)d->head * d->sectors_per_track[d->drive] +
	    (int64_t)d->heads[d->drive] * d->sectors_per_track[d->drive] * cyl);
#if 0
	/*  LBA:  */
	if (d->lba)
		offset = 512 * (((d->head & 0xf) << 24) +
		    (cyl << 8) + d->sector);
	printf("WDC write to offset %lli\n", (long long)offset);
#endif

	d->write_in_progress = d->cur_command;
	d->write_count = count;
	d->write_offset = offset;

	/*  TODO: result code?  */
}


/*
 *  status_byte():
 *
 *  Return a reasonable status byte corresponding to the controller's current
 *  state.
 */
static int status_byte(struct wdc_data *d, struct cpu *cpu)
{
	int odata = 0;
	if (diskimage_exist(cpu->machine, d->drive + d->base_drive,
	    DISKIMAGE_IDE))
		odata |= WDCS_DRDY | WDCS_DSC;
	if (d->inbuf_head != d->inbuf_tail)
		odata |= WDCS_DRQ;
	if (d->write_in_progress)
		odata |= WDCS_DRQ;
	if (d->error)
		odata |= WDCS_ERR;
	if (d->atapi_cmd_in_progress && (d->atapi_phase & WDCS_DRQ)) {
		odata |= WDCS_DRQ;
	}
	return odata;
}


/*  #481: forward-declared so the ALT-CTRL arm below can call it.  A panel seat's
    control mutant failed to compile for want of exactly this line and the failure
    was briefly read as a design constraint against calling the shared helper; it
    is one line and it builds clean.  */
static void wdc_new_command_reset(struct wdc_data *d);

DEVICE_ACCESS(wdc_altstatus)
{
	struct wdc_data *d = (struct wdc_data *) extra;
	uint64_t idata = 0, odata = 0;

	idata = data[0];

	/*  Same as the normal status byte:  */
	odata = status_byte(d, cpu);

	if (writeflag==MEM_READ)
		debug("[ wdc: read from ALTSTATUS: 0x%02x ]\n",
		    (int)odata);
	else if (relative_addr != 0) {
		/*  #494: THE HANDLER NEVER DECODED ITS OWN OFFSET.  The region is
		    registered TWO BYTES wide, so offset 1 -- the Drive Address
		    register, 0x3f7 on the PC layout -- arrived here and was treated
		    as a Device Control write.  Since #481 corrected the reset bit,
		    that meant a guest store to a READ-ONLY register aborted a live
		    ATA write and purged the queued ring.  Measured at rung 3 on an
		    unmodified evbmips -e malta; the witness is preserved under
		    regress/artifacts/wdcaltoffset/witness_20260829/.

		    THE WHOLE ACTION IS DECLINED, NOT JUST THE HELPER CALL, AND THAT
		    IS THE POINT.  The reset has two effects with two owners: the
		    cur_command assignment below, and the ring/DRQ clearing inside
		    wdc_new_command_reset().  A fix that guards only the helper leaves
		    the ATAPI signature latched.  That was MEASURED, not reasoned: it
		    escapes the witness AND the detector that replaced it with a clean
		    sweep, because every row in both observes DRQ or the ring and
		    neither varies under it.  The kill table and its scores are under
		    regress/artifacts/wdcaltoffset/killtable_20260830/ -- read TABLE.txt
		    for the counts rather than trusting a number written here, which is
		    how this sentence was wrong once already.

		    SILENT BY DESIGN, at debug() level and with no latch.  The house
		    idiom announces a guest ANOMALY, and this is not one: the tree
		    records in two places that this byte belongs to the floppy
		    controller on PCs -- wdcreg.h compiles wd_digin out under
		    an `#if 0` whose own note reads "NOT MAPPED; fd uses this
		    register on PCs" (the delimiters are dropped here on purpose:
		    a comment terminator quoted inside a comment ends it), and
		    dev_fdc.c's DEV_FDC_LENGTH carries `TODO 8, but collision with
		    wdc`.  A correct guest writes here expecting a floppy effect, so
		    a wdc diagnostic would report correct behaviour as a fault.

		    THE ACCESS STAYS HANDLED (return 1), AND THE REASON IS NOT THE ONE
		    THIS COMMENT FIRST GAVE.  It said a 0 would fall through to
		    unassigned-address handling and warn per access.  That is false: this
		    device is REGISTERED, so a 0 never reaches that path.  memory_rw sets
		    res = -1, takes its res <= 0 branch, and raises EXCEPTION_DBE --
		    measured, 19793 `device 'wdc_altstatus' ... failed` lines and ZERO
		    `non-existant` ones under -v.  The guest then loops forever
		    re-executing the faulting store, and at DEFAULT verbosity it does so
		    in SILENCE.  That is worse than a warning flood, not better, which is
		    why the wrong reason was worth correcting rather than dropping: a
		    maintainer who reads `only noisy warnings` may decide a 0 is fine.

		    The arm falls through to the common tail, which is a no-op for it --
		    the tail only assigns on the READ path.  (An earlier draft justified
		    that by the untouched-buffer hazard; #95 already zeroes the caller's
		    buffer, so that hazard cannot arise here either.)  */
		debug("[ wdc: write to DRIVE ADDRESS (read-only): 0x%02x,"
		    " ignored ]\n", (int)idata);
	} else {
		debug("[ wdc: write to ALT. CTRL: 0x%02x ]\n",
		    (int)idata);
		/*  #481: THE RESET BIT IS WDCTL_RST (0x04), NOT WDCTL_4BIT (0x08).
		
		    WDCTL_4BIT is "use four head bits (wd1003)", a head-addressing
		    mode selector that Linux libata holds as its STEADY-STATE ap->ctl.
		    Testing it here meant three measured defects at once:
		
		      * a real soft reset was MISSED.  Older OpenBSD asserts with 0x06,
		        which has bit 3 CLEAR -- measured `cur_command 0x0`.
		      * a ROUTINE control write DESTROYED THE RECORD OF WHICH COMMAND IS
		        EXECUTING -- measured `0xec -> 0x100`.  cur_command is also the
		        value assigned into write_in_progress, so this is only harmless
		        because wdc__write() has exactly ONE caller, immediately after
		        the assignment.  An accident, not an invariant.
		      * an nIEN write latched a reset.  0x0a is libata's polled-mode
		        staple -- measured `0x0a->0x100`.
		
		    COMMAND_RESET IS NOT A RESET ACTION.  It is read at exactly two
		    sites, both making the cylinder registers return the ATAPI signature
		    0xEB14 for a CD-ROM.  It is the SIGNATURE LATCH -- which is why the
		    wrong bit went unnoticed: triggering on libata's steady state kept
		    the signature on almost always.
		
		    LEVEL-TRIGGERED, DELIBERATELY, AND THE MEASURED DIFFERENCE
		    FAVOURS THIS FORM.  A channel held in reset must not carry bytes
		    out the far side, and an edge-triggered abort lets it:
		
		        assert 0x0e, 8 guest stores to DATA, rewrite 0x0e, release
		          LEVEL (this form):  occ 0, DRQ 0   -- the ring is purged
		          EDGE:               occ 8, DRQ 1   -- the bytes survive the
		                                                 whole reset, and the
		                                                 status byte still
		                                                 advertises DRQ
		
		    Measured through register writes only, with a liveness control (the
		    same traffic without a reset leaves occ 8, so the 0 is the reset
		    working and not a dead path).
		
		    *** AN EARLIER VERSION OF THIS COMMENT SAID edge and level were
		    "indistinguishable here, because the abort is idempotent and no
		    protocol-following driver issues commands while holding SRST".
		    THAT WAS MEASURED FALSE.  Three things were wrong with it:
		
		      * the differential behind it only ever asserted SRST ONCE, and
		        the forms differ only when a driver HOLDS it across two
		        control writes with something accruing in between;
		      * IDEMPOTENCE OF THE HELPER DOES NOT LICENCE THE INFERENCE.
		        It means repeating the abort is harmless.  It says nothing
		        about SKIPPING the repeat, which is what an edge does, and
		        state accrues between the writes;
		      * the scenario above ISSUES NO COMMAND.  Plain data-register
		        stores suffice -- and in a hardening fork the guest need not
		        be protocol-following at all.
		
		    The decision is unchanged and now rests on evidence that does not
		    collapse when someone builds the discriminating case. ***
		
		    Note also that a prev_ctl update mis-scoped by one brace makes
		    every LATER reset be ignored -- a failure this form cannot have --
		    but that is a secondary argument, not the reason.
		
		    THE ABORT IS #479's HELPER, not a second one: a channel reset and a
		    new command must not disagree about what gets cleared, and #479
		    already reasoned out which latches must SURVIVE (see its comment --
		    clearing warned_* would undo #337 and #464).  */
		if (idata & WDCTL_RST) {
			d->cur_command = COMMAND_RESET;
			wdc_new_command_reset(d);
		}
	}

	if (writeflag == MEM_READ)
		data[0] = odata;

	return 1;
}



/*
 *  wdc_new_command_reset():
 *
 *  #479: A COMMAND ENTERING wdc_command() STARTS WITHOUT THE PREVIOUS COMMAND'S
 *  WRITER, BUFFERED BYTES, OR PHASE.
 *
 *  #480 L4: THE SCOPE IS THIS FUNCTION, NOT THE WORD "COMMAND".  An earlier
 *  headline read "A NEW COMMAND STARTS WITHOUT..." with no qualifier, and the
 *  device falsified that in its own code: the ALT-CTRL arm assigned
 *  cur_command = COMMAND_RESET WITHOUT CALLING THIS HELPER, so the most
 *  reset-like operation the device had was not a caller at all.  The SCOPE
 *  paragraph forty lines below said so; a universal headline with its qualifier
 *  that far down is read as universal.  Named by the fable seat on #479 pass 2.
 *
 *  wdc_command() cleared the ATAPI flag and the error and nothing else, so three
 *  pieces of the previous command's state survived into the next one.  All three
 *  were reproduced with liveness controls before this was written:
 *
 *    write_in_progress   an ATA write stayed armed across a packet command, so one
 *                        shared ring served the disk-write path and the CDB path at
 *                        once.  MEASURED: a guest's own sector write put 512 CD-ROM
 *                        DATA-IN bytes and ZERO of its own on the image.
 *    the input ring      residue from an under-drained transfer was never cleared.
 *                        MEASURED: the drain then fires early and the guest's sector
 *                        arrives with the previous transfer's bytes at its head.
 *    atapi_phase         PHASE_CMDOUT survived an ordinary WRITE command.  Latent
 *                        while the dispatch tests the flag AND the phase -- and #477's
 *                        comment was pointing a future round straight at it.
 *
 *  WHY THE TOP, AND NOT THE END.  IDENTIFY loads its 512-byte response INTO the ring
 *  as part of the command, and wdc__read() does the same for every ordinary READ.  A
 *  seat measured the end-of-function form destroying both -- 256 of 256 IDENTIFY
 *  words wrong, and a freshly-read sector gone -- while every row this round pins
 *  stayed GREEN.  Clean-up-on-exit reads as the more principled placement and is the
 *  more dangerous one.
 *
 *  WHAT THIS DELIBERATELY DOES NOT TOUCH:
 *
 *    cur_command     wdc__write() reads it, and the caller sets it immediately
 *                    above.  Clearing it here would break the write it is about to
 *                    set up.
 *    the warned_*    latches.  Zeroing them alongside everything else reads as
 *                    COMPLETING this helper and is the mutant to press: it undoes
 *                    #337 and #464, and it is STRICTLY WORSE than the equivalent
 *                    mistake in dev_asc.c, because wdc_command() runs far more often
 *                    than a chip reset.  dev_asc.c says so at its own latch
 *                    declarations: "Deliberately NOT cleared by dev_asc_reset() or
 *                    dev_asc_fifo_flush(): a guest could otherwise re-arm the flood."
 *
 *  SCOPE.  TWO CALLERS: wdc_command(), and the ALT-CTRL arm on a real soft reset.
 *
 *  *** THIS PARAGRAPH SAID "Called from wdc_command() only" AND PRESCRIBED WHAT WOULD
 *  HAVE TO HAPPEN FIRST BEFORE THE OTHER CALLER COULD EXIST.  #481 DID EXACTLY THAT,
 *  so the prescription is DISCHARGED rather than merely stale. ***
 *
 *  It read: extending the helper to that arm AS IT STOOD was MEASURED to cancel a
 *  legal transfer on an ordinary 0x08 Device Control write, which real drivers hold
 *  as their steady state; so the extension "needs the arm's bit test fixed first
 *  (WDCTL_RST, not WDCTL_4BIT) and is a separate round."
 *
 *  #481 is that round.  It corrected the bit AND made the call in one change, which
 *  is why the accept rows this paragraph pointed at are GREEN on the shipped tree and
 *  still RED under `Md_bitswap` -- the same extension WITHOUT the prerequisite.
 *  Those four rows therefore MEASURED the ordering argument rather than asserting it.
 *
 *  The invariant is still not established on every path into the device: the ALT-CTRL
 *  arm calls this only for WDCTL_RST, and other decode paths into that register are
 *  filed rather than covered.  Said out loud rather than implied, as before.
 */
static void wdc_new_command_reset(struct wdc_data *d)
{
	d->atapi_cmd_in_progress = 0;
	d->atapi_phase = 0;
	d->write_in_progress = 0;

	/*  pointer reset rather than a drain loop, matching dev_asc_fifo_flush()'s
	    count-zeroing: there is no consumer to notify and nothing to hand back.  */
	d->inbuf_head = d->inbuf_tail = 0;
}
/*
 *  wdc_command():
 */
void wdc_command(struct cpu *cpu, struct wdc_data *d, int idata)
{
	size_t i;

	d->cur_command = idata;
	d->error = 0;

	/*  #479: this replaced a bare `d->atapi_cmd_in_progress = 0;`.  The flag
	    was one of three pieces of the previous command's state, and clearing
	    only the one that had been noticed is what left the other two.  */
	wdc_new_command_reset(d);

	/*
	 *  Disk images that do not exist return an ABORT error.  This also
	 *  happens with CDROM images with the WDCC_IDENTIFY command; CDROM
	 *  images must be detected with ATAPI_IDENTIFY_DEVICE instead.
	 *
	 *  TODO:  Is this correct/good behaviour?
	 */
	if (!diskimage_exist(cpu->machine, d->drive + d->base_drive,
	    DISKIMAGE_IDE)) {
		debug("[ wdc: command 0x%02x drive %i, but no disk image ]\n",
		    d->cur_command, d->drive + d->base_drive);
		d->error |= WDCE_ABRT;
		d->int_assert = 1;
		return;
	}
	if (diskimage_is_a_cdrom(cpu->machine, d->drive + d->base_drive,
	    DISKIMAGE_IDE) && d->cur_command == WDCC_IDENTIFY) {
		debug("[ wdc: IDENTIFY drive %i, but it is an ATAPI "
		    "drive ]\n", d->drive + d->base_drive);
		d->error |= WDCE_ABRT;
		d->int_assert = 1;
		return;
	}

	/*  Handle the command:  */
	switch (d->cur_command) {

	case WDCC_READ:
	case WDCC_READMULTI:
		if (!quiet_mode)
			debug("[ wdc: READ from drive %i, head %i, cyl %i, "
			    "sector %i, nsecs %i ]\n", d->drive, d->head,
			    d->cyl_hi*256+d->cyl_lo, d->sector, d->seccnt);
		wdc__read(cpu, d);
		break;

	case WDCC_WRITE:
	case WDCC_WRITEMULTI:
		if (!quiet_mode)
			debug("[ wdc: WRITE to drive %i, head %i, cyl %i, "
			    "sector %i, nsecs %i ]\n", d->drive, d->head,
			    d->cyl_hi*256+d->cyl_lo, d->sector, d->seccnt);
		wdc__write(cpu, d);
		break;

	case WDCC_IDP:	/*  Initialize drive parameters  */
		debug("[ wdc: IDP drive %i (TODO) ]\n", d->drive);
		/*  TODO  */
		d->int_assert = 1;
		break;

	case SET_FEATURES:
		debug("[ wdc: SET_FEATURES drive %i (TODO), feature 0x%02x ]\n",
		    d->drive, d->precomp);
		/*  TODO  */
		switch (d->precomp) {
		case WDSF_SET_MODE:
			debug("[ wdc: WDSF_SET_MODE drive %i, pio/dma flags "
			    "0x%02x ]\n", d->drive, d->seccnt);
			break;
		default:d->error |= WDCE_ABRT;
		}
		/*  TODO: always interrupt?  */
		d->int_assert = 1;
		break;

	case WDCC_RECAL:
		debug("[ wdc: RECAL drive %i ]\n", d->drive);
		d->int_assert = 1;
		break;

	case WDCC_IDENTIFY:
	case ATAPI_IDENTIFY_DEVICE:
		debug("[ wdc: %sIDENTIFY drive %i ]\n", d->cur_command ==
		    ATAPI_IDENTIFY_DEVICE? "ATAPI " : "", d->drive);
		wdc_initialize_identify_struct(cpu, d);
		/*  The IDENTIFY data is sent out in low/high byte order:  */
		for (i=0; i<sizeof(d->identify_struct); i+=2) {
			wdc_addtoinbuf(d, d->identify_struct[i+1]);
			wdc_addtoinbuf(d, d->identify_struct[i+0]);
		}
		d->int_assert = 1;
		break;

	case WDCC_IDLE_IMMED:
		debug("[ wdc: IDLE_IMMED drive %i ]\n", d->drive);
		/*  TODO: interrupt here?  */
		d->int_assert = 1;
		break;

	case WDCC_SETMULTI:
		debug("[ wdc: SETMULTI drive %i ]\n", d->drive);
		/*  TODO: interrupt here?  */
		d->int_assert = 1;
		break;

	case ATAPI_SOFT_RESET:
		debug("[ wdc: ATAPI_SOFT_RESET drive %i ]\n", d->drive);
		/*  TODO: interrupt here?  */
		d->int_assert = 1;
		break;

	case ATAPI_PKT_CMD:
		debug("[ wdc: ATAPI_PKT_CMD drive %i ]\n", d->drive);
		/*  TODO: interrupt here?  */
		/*  d->int_assert = 1;  */
		d->atapi_cmd_in_progress = 1;
		d->atapi_phase = PHASE_CMDOUT;
		break;

	case WDCC_DIAGNOSE:
		debug("[ wdc: WDCC_DIAGNOSE drive %i: TODO ]\n", d->drive);
		/*  TODO: interrupt here?  */
		d->int_assert = 1;
		d->error = 1;		/*  No error?  */
		break;

	/*  Unsupported commands, without warning:  */
	case WDCC_SEC_SET_PASSWORD:
	case WDCC_SEC_UNLOCK:
	case WDCC_SEC_ERASE_PREPARE:
	case WDCC_SEC_ERASE_UNIT:
	case WDCC_SEC_FREEZE_LOCK:
	case WDCC_SEC_DISABLE_PASSWORD:
		/*  #485: A TERMINAL ARM RAISES ITS COMPLETION INTERRUPT.

		    THE INVARIANT, derived over all 256 opcodes rather than from a
		    few neighbours: every command wdc_command() FINISHES raises the
		    completion interrupt.  The only opcodes that stay silent are the
		    THREE that hand control back for a data phase -- WDCC_WRITE,
		    WDCC_WRITEMULTI and ATAPI_PKT_CMD -- and each of those asserts
		    when its data phase drains.  This arm and the `default:` arm
		    below were the only violations.

		    *** THEY WERE ALSO THE ONLY TERMINAL ARMS IN THE FUNCTION WITH NO
		    INTERRUPT DECISION RECORDED AT ALL -- no assert, and no comment.
		    ***  Six arms carry a `TODO ... interrupt` hedge; in five the
		    author asserted, and in the sixth (ATAPI_PKT_CMD) he left the
		    assert COMMENTED OUT, so that decision is visible in the source.
		    A question never reached, not a decision to stay silent.

		    NO SPECIFICATION IS CITED AND NONE IS AVAILABLE -- there is no ATA
		    document in this tree.  The warrant is the invariant above plus a
		    sibling model: dev_mb89352.c asserts on ANY non-zero interrupt
		    status, without regard to whether the command succeeded.

		    nIEN CANNOT CONTRADICT THIS: WDCTL_IDS (0x02) is defined in
		    wdcreg.h and read NOWHERE in this file, so the model has no
		    interrupt-disable state.  This arm is exactly as nIEN-blind as
		    the ten arms that already assert.

		    HARM, STATED HONESTLY: none measured.  WDCS_BSY is never set
		    anywhere in this file, so a polling driver's wait returns at once
		    with DRDY|DSC|ERR.  The WDCS_BSY fact is FILE-SCOPED and this
		    comment owns it: grep the file.
		
		    *** THE REST OF THIS PARAGRAPH ONCE ASSERTED A BOOT CENSUS -- that
		    OpenBSD 7.6 completes boot and shutdown against the old behaviour,
		    that 0xF5 lands here on every attach and 0xE0 on every halt.  A
		    PANEL SEAT MEASURED ALL OF THAT AND ITS ARTIFACT WAS NOT PRESERVED,
		    so the claim rested on evidence that no longer exists.  Named by a
		    packet-fed seat on pass 2. ***
		
		    It is kept as an ATTRIBUTED REPORT rather than deleted, because the
		    reachability it describes is why this arm was worth fixing at all --
		    but it is a seat's measurement, not this comment's, and a reader
		    who wants it must re-run a boot rather than cite this line.
		
		    The licence is protocol correctness at trivial cost, NOT a hang.
		    That much stands on the WDCS_BSY reading alone.  */
		d->error |= WDCE_ABRT;
		d->int_assert = 1;
		break;

	default:/*  TODO  */
		/*  #464: `d->error |= WDCE_ABRT` STAYS OUTSIDE THE GUARD.
		    Inside it, the second unimplemented command silently
		    SUCCEEDS -- wdc_command() re-clears d->error per command,
		    so the guest is told the command worked.  A line-counting
		    oracle cannot see that; row `abrt 2nd` reads the status
		    register after the second command and can.

		    ONE LINE PER DEVICE, NOT PER OPCODE.  A per-opcode set was
		    proposed and is FILED, not shipped: the scalar is what stops
		    a guest cycling 0x00..0xff for 256 lines, which is the flood
		    #464 exists to bound.  Row `unimpl 2op` pins the
		    per-device spec by firing TWO different opcodes and
		    demanding ONE line -- which also kills a
		    "last-warned-opcode" latch, under which an alternating guest
		    would flood forever.  */
		/*  #485: see the WDCC_SEC_* arm above for the invariant and the
		    warrant.  This is the other terminal arm that never raised its
		    completion interrupt.

		    *** THE ASSERT IS OUTSIDE THE LATCH, AND THAT IS NOT A STYLE
		    CHOICE. ***  Moved inside `if (!d->warned_unimpl_cmd)` below,
		    only the FIRST unimplemented command per device would interrupt
		    and every later one would go silent again.  It is what a tidying
		    maintainer writes -- group the response with the warning -- and a
		    sweep using one fresh device per opcode CANNOT SEE IT, because
		    the latch is 0 on every leg.  Row `irq 2nd` exists for exactly
		    that mutant.
		
		    *** THAT SENTENCE NAMED A ROW `irq 2nd` THAT DOES NOT EXIST.
		    Repo-wide it occurred in this comment and nowhere else. ***  The
		    real artifact is an unnamed SUB-LEG of row_completion_irq(),
		    printing a `2nd` field inside a row named "a terminated command
		    raises its irq".  What makes the error dangerous rather than
		    untidy is the company it kept: the SAME sentence cites `abrt 2nd`,
		    which IS a real row -- so a true citation stood next to a
		    fabricated one and lent it credibility.
		
		    #464 already found the ABORT BIT wrongly inside
		    this same guard and shipped `abrt 2nd` for it; the interrupt
		    needed the same row.  */
		d->error |= WDCE_ABRT;
		d->int_assert = 1;
		if (!d->warned_unimpl_cmd) {
			d->warned_unimpl_cmd = 1;
			fatal("[ wdc: WARNING! Unimplemented command 0x%02x "
			    "(drive %i, head %i, cyl %i, sector %i, nsecs %i)"
			    " ]\n", d->cur_command, d->drive, d->head,
			    d->cyl_hi*256+d->cyl_lo, d->sector, d->seccnt);
		}
	}
}


DEVICE_ACCESS(wdc)
{
	struct wdc_data *d = (struct wdc_data *) extra;
	uint64_t idata = 0, odata = 0;
	int i;

	relative_addr /= d->addr_mult;

	if (!d->io_enabled)
		goto ret;

	if (writeflag == MEM_WRITE) {
		if (relative_addr == wd_data)
			idata = memory_readmax64(cpu, data, len);
		else {
			/*  #464: latch the announcement; `idata = data[0]`
			    is the repair and stays outside the guard.  */
			if (len != 1 && !d->warned_nonbyte_write) {
				d->warned_nonbyte_write = 1;
				fatal("[ wdc: WARNING! non-8-bit access on "
				    "WRITE! ]\n");
			}
			idata = data[0];
		}
	}

	switch (relative_addr) {

	case wd_data:	/*  0: data  */
		if (writeflag == MEM_READ) {
			odata = wdc_get_inbuf(d);

			if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {
				if (len >= 2)
					odata += (wdc_get_inbuf(d) << 8);
				if (len == 4) {
					odata += (wdc_get_inbuf(d) << 16);
					odata += (wdc_get_inbuf(d) << 24);
				}
			} else {
				if (len >= 2)
					odata = (odata << 8) + wdc_get_inbuf(d);
				if (len == 4) {
					odata = (odata << 8) + wdc_get_inbuf(d);
					odata = (odata << 8) + wdc_get_inbuf(d);
				}
			}

			if (d->data_debug) {
				const char *s = "0x%04" PRIx64" ]\n";
				if (len == 1)
					s = "0x%02" PRIx64" ]\n";
				if (len == 4)
					s = "0x%08" PRIx64" ]\n";
				if (len == 8)
					s = "0x%016" PRIx64" ]\n";
				debug("[ wdc: read from DATA: ");
				debug(s, (uint64_t) odata);
			}

			if (d->atapi_cmd_in_progress) {
				/*  #341: account for what was actually CONSUMED
				    from the buffer, not for what the guest
				    asked for. The reads above take one byte,
				    two if len >= 2, four only if len == 4 --
				    so a 3- or 8-byte access consumes 1 or 2
				    while `len` says 3 or 8. Subtracting the
				    requested length let atapi_len step PAST
				    zero, which its `== 0` test then never
				    catches, so PHASE_COMPLETED never fires and
				    the guest is told a transfer is further
				    along than the bytes it received. Same
				    truthfulness defect as #283 in the ASC and
				    #338 in the mb89352: the count reported has
				    to be the count that happened.  */
				int consumed = len == 4 ? 4 : (len >= 2 ? 2 : 1);
				/*  #475: clamp to what REMAINS, not just to what was popped.
				    #341 fixed `consumed` to count the POPS rather than the
				    requested length; it did not stop the subtraction STEPPING
				    PAST ZERO.  With an odd remainder -- and the length is a
				    guest-chosen allocation byte -- a 4-byte read of an odd
				    remainder drove atapi_len NEGATIVE, so `== 0` never fired
				    again and the command never completed, while atapi_received
				    claimed more bytes than the transfer holds.  Two distinct
				    numbers, and conflating them is easy: the 3-byte fixture
				    lands on -1; the worked INQUIRY-37 path lands on -3 (nine
				    4-byte reads leave 1, the tenth takes 4).

				    CLAMPING `consumed` RATHER THAN SATURATING atapi_len,
				    because atapi_received has two live MID-TRANSFER consumers:
				    the re-arm's length, and the refill's source offset
				    data_in[atapi_received + j].  Saturating repairs completion
				    and leaves those two reading a skewed offset, permanently
				    skipping up to 3 real bytes -- #283's defect shape,
				    re-created.

				    A NEARBY PRECEDENT, cited narrowly on purpose: dev_asc.c
				    clamps a step to a remainder before its move.  An earlier
				    draft of this comment called that #283 and called it
				    'exactly this shape'; a panel seat refuted both.  #283 tags
				    the RESIDUAL REPORTING there (`programmed`/`moved`) -- its
				    own comment says it snapshots the count 'before the clamps
				    below rewrite len2', so the clamp is untagged upstream code.
				    And the shapes differ: dev_asc clamps the TRANSFER before
				    the move, while this clamps the ACCOUNTING and lets the pop
				    happen at full width.  The in-tree precedent for clamping
				    the transfer is a DIFFERENT option, which this round
				    considered and did not take.

				    The warrant that survives is the one above: the cursor.  */
				if (consumed > d->atapi_len)
					consumed = d->atapi_len;

				d->atapi_len -= consumed;
				d->atapi_received += consumed;
				/*  #476: `atapi_st` IS DEREFERENCED ON THE NEXT LINE AND WAS NEVER
				    NULL-CHECKED.  #475's clamp made this branch REACHABLE: before it, a
				    read with atapi_len already 0 drove the counter NEGATIVE and `== 0`
				    never fired again, so the deref was dead code.  Clamping consumed to
				    0 leaves atapi_len AT 0, the test fires, and two guest register
				    accesses from a fresh device -- write ATAPI_PKT_CMD to COMMAND, then
				    read DATA -- reach `d->atapi_st->data_in_len` through NULL.

				    MEASURED: SIGSEGV at address 0x48, which is
				    offsetof(struct scsi_transfer, data_in_len).  The pre-#475 blob
				    survives the identical input, and the row for the defect #475 FIXED
				    goes the OTHER way on the same pair -- so the bisect is unambiguous.

				    The clamp was right; the branch it woke was never NULL-safe.  Decline
				    and say so once, per this file's latch idiom: a device that cannot
				    service an access must not take the emulator with it (#337, #184,
				    #186, #315, #316, #326).  */
				if (d->atapi_len == 0 && d->atapi_st == NULL) {
					if (!d->warned_null_xfer) {
						d->warned_null_xfer = 1;
						fatal("[ wdc: DATA read with no ATAPI "
						    "transfer armed (once) ]\n");
					}
				} else if (d->atapi_len == 0 &&
				    d->atapi_phase != PHASE_CMDOUT) {
					/*  #477: A STRAY DATA-PORT READ MUST NOT REWRITE THE PHASE WHILE A
					    CDB IS BEING COLLECTED.  Measured by the Fable seat as a
					    REGRESSION of the dispatch phase guard below: HEAD services
					    `PKT, stray read, CDB` after a prior completed command, and
					    without this arm's phase test the CDB never dispatches at all.

					    The ATAPI_PKT_CMD arm of wdc_command() assigns only the flag and
					    the phase, so a new packet starts with atapi_len == 0,
					    atapi_received == data_in_len and atapi_st STALE NON-NULL (it is
					    freed at the next dispatch and never NULLed).  A read then falls
					    here, finds `received < data_in_len` false, and sets
					    PHASE_COMPLETED -- moving the phase off CMDOUT before the CDB is
					    complete.

					    *** AND THE RESIDUE THAT MAKES IT UNRECOVERABLE IS A PROPERTY OF
					    THE DEVICE, NOT OF THIS REGRESSION -- an earlier draft of this
					    comment said otherwise, and the Opus seat MEASURED the
					    difference. ***  ATAPI_PKT_CMD never flushes the ring, and
					    neither reset path does either, so an under-drained DATA-IN
					    leaves occupancy at 32 -> 44 -> 56 -> 68 and every later CDB is
					    dropped forever.  That entrance is open with no stray read at
					    all; it is filed as `wdcringnoflush`, and dev_asc.c's
					    dev_asc_fifo_flush() is the in-tree idiom for closing it.

					    In CMDOUT the atapi_len/atapi_received pair describes the
					    PREVIOUS transfer, so no completion state may be derived from it
					    -- the same statement the dispatch guard below makes about the
					    flag, applied to the read arm.  Falling through BOTH arms is the
					    correct disposition: the read pops the ring and changes no
					    transfer state.  */
					if (d->atapi_received < d->atapi_st->
					    data_in_len) {
						d->atapi_phase = PHASE_DATAIN;
						/*  #473: clamp to the chunk size, NOT zero, and REFILL.  This
						    assigned 0 where the initial arm clamps to 32768 in the same
						    condition, so a transfer with >32768 left reported ZERO
						    remaining -- with no recovery, since the next read decrements
						    from 0 and `== 0` never fires again.  MEASURED band
						    [65537, 262655]; the guest saw bytecount 0 with DRQ asserted.

						    The refill is what makes the bounded push above correct: here
						    atapi_len is 0, so the guest drained the previous chunk; data_in
						    is still live, being freed only when the next command arrives.

						    #473 L4: an earlier version of this comment said the ring is
						    EMPTY here.  That is an overclaim and a panel seat broke it.
						    atapi_len counts only what the DATAIN arms pushed, and the
						    data-port WRITE arm above pushes guest bytes with no phase
						    guard and no capacity check -- its unexpected-write latch is
						    suppressed precisely because atapi_cmd_in_progress is set.  A
						    guest that WRITES to the data port mid-DATAIN therefore grows
						    head without touching atapi_len, and those bytes are still
						    queued when the refill runs.

						    What IS true: the ring is empty for any guest that only READS
						    during DATAIN, which is every driver in this tree.  An
						    adversarial interleaved write DESYNCHRONISES that guest's own
						MEASURED by a panel seat: one 2-byte store placed so the
						ring still holds the tail of chunk 1 makes all 32768 bytes of
						chunk 2 wrong on this build.

						*** AN EARLIER DRAFT CALLED THAT A REGRESSION.  A SECOND SEAT
						MEASURED IT FALSE. ***  It rested on 'and ZERO wrong pre-fix',
						which is a 0 OF 0 -- the denominator trap.  Pre-#473 there is
						no refill loop at all, so chunk 2 is NEVER DELIVERED and the
						wrongness was counted over the empty set.  Measured honestly,
						the pre-fix build delivers 0 of 32768 bytes of chunk 2 and
						returns the over-read sentinel forever.

						A regression needs a case that WORKED before and does not now,
						and there is none: the fix strictly improves the no-write case
						(0 wrong against 32640) and moves the adversarial case from
						DEAD to SHIFTED.  The honest word is a shifted failure mode,
						not a regression.

						    The arithmetic here was stated BACKWARDS in the first draft of
						    this comment: the refill route takes 229889 injected bytes and
						    the direct write route 262657, so the refill route is cheaper
						    by 32768 -- FEWER, not more.  The conclusion survives because
						    both routes are unbounded and a guest with either has the
						    other; the stated reason was false, and a wrong reason gets
						    reused.

						    TWO QUALIFICATIONS, both from a later seat, both narrowing
						    claims that were too absolute.  262657 is the EMPTY-RING
						    direct threshold -- with a chunk already queued the direct
						    route also overwrites after 229889, so these are thresholds
						    under stated starting states, not intrinsic costs.  And
						    'only that guest's own transfer' overclaims: the same shared
						    ring feeds the CDB-dispatch and disk-image-drain paths.  The
						    defensible form is that this adds no DEMONSTRATED
						    host-memory-safety primitive, and the measured case corrupts
						    returned transfer data.  Tracked as
						    `wdcaddtoinbufbound`, which names that write path as the live
						    unbounded route.  */
						d->atapi_len = d->atapi_st->
						    data_in_len -
						    d->atapi_received;
						if (d->atapi_len > 32768)
							d->atapi_len = 32768;

						/*  WHY THIS DEREFERENCE IS NOT NULL-CHECKED, and the dispatch
						    refill below IS.  The asymmetry is real and the safety here
						    rests on an invariant that lives in ANOTHER FILE, which is
						    the reason it is written down rather than left to be
						    re-derived:

						      a LIVE scsi_transfer with data_in_len > 0 always has
						      data_in != NULL.

						    scsi_transfer_alloc() memsets the whole struct, so a fresh
						    transfer is (NULL, 0).  scsi_transfer_allocbuf() either
						    installs a buffer or exit()s -- it never returns having set a
						    length without one.  The three later length mutations in the
						    tree (MODE_SENSE, READ_TOC, and dev_asc's consumed-prefix
						    subtraction) only SHRINK or preserve a live allocation.

						    *** IT IS A FUNCTION-BOUNDARY INVARIANT, NOT A CONTINUOUS
						    ONE, and an earlier draft of this note said the two fields
						    are set together.  They are not: allocbuf writes the LENGTH
						    first and the POINTER fourteen lines later, with a malloc
						    between them.  Nothing observes that window -- no callback
						    and no return to this device runs inside it -- but the
						    distinction is the whole reason this is a comment and not a
						    proof. ***

						    NOT a guard: the ADDITION LICENCE wants a measured delta or a
						    transferred warrant, and the state is not producible today.
						    What was missing is a REASON an edit elsewhere can break,
						    rather than a check that would silently never fire.  Filed
						    as `wdcdatainnull`.  */
						for (int j=0; j<d->atapi_len; j++)
							wdc_addtoinbuf(d, d->atapi_st->
								data_in[d->atapi_received + j]);
					} else
						d->atapi_phase =
						    PHASE_COMPLETED;
					d->int_assert = 1;
				}
			} else {
#if 0
				if (d->inbuf_tail != d->inbuf_head)
#else
				if (d->inbuf_tail != d->inbuf_head &&
				    ((d->inbuf_tail - d->inbuf_head) % 512)
				    == 0)
#endif
					d->int_assert = 1;
			}
		} else {
			int inbuf_len;
			/*  #478: PER-ACCESS, and a struct field here is a REGRESSION.
			    MEASURED: a latched field silences every later legal write,
			    turning a corruption defect into silent data loss, which is
			    worse.  The question is 'did THIS access push nothing', so the
			    answer must not outlive the access.  */
			int badlen_this = 0;
			if (d->data_debug) {
				const char *s = "0x%04" PRIx64" ]\n";
				if (len == 1)
					s = "0x%02" PRIx64" ]\n";
				if (len == 4)
					s = "0x%08" PRIx64" ]\n";
				if (len == 8)
					s = "0x%016" PRIx64" ]\n";
				debug("[ wdc: write to DATA: ");
				debug(s, (uint64_t) idata);
			}
			/*  #464: latched.  */
			if (!d->write_in_progress &&
			    !d->atapi_cmd_in_progress &&
			    !d->warned_data_unexpected) {
				d->warned_data_unexpected = 1;
				fatal("[ wdc: write to DATA, but not "
				    "expecting any? (len=%i): 0x%08lx ]\n",
				    (int)len, (long)idata);
			}

			if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {
				switch (len) {
				case 4:	wdc_addtoinbuf(d, idata & 0xff);
					wdc_addtoinbuf(d, (idata >> 8) & 0xff);
					wdc_addtoinbuf(d, (idata >> 16) & 0xff);
					wdc_addtoinbuf(d, (idata >> 24) & 0xff);
					break;
				case 2:	wdc_addtoinbuf(d, idata & 0xff);
					wdc_addtoinbuf(d, (idata >> 8) & 0xff);
					break;
				case 1:	wdc_addtoinbuf(d, idata); break;
				/*  #337: a 3- or 8-byte access to the data
				    port used to call exit(1) -- a GUEST
				    choosing an access width killed the host
				    process. Same halt class as #184/#186/
				    #187/#315/#316/#326. Drop the access and
				    say so once; a device that cannot honour
				    a transfer must not take the emulator
				    with it. (Unreachable from SH-4, which
				    has no 3- or 8-byte access, but reachable
				    from a 64-bit MIPS machine carrying wdc
				    over bus_isa/bus_pci.)  */
				default:/*  #478: `break` leaves the WIDTH SWITCH, not the
				            handler -- execution falls through to the
				            occupancy drain below with NOTHING pushed.  */
				        badlen_this = 1;
				        if (!d->warned_badlen) {
						d->warned_badlen = 1;
						fatal("wdc: unimplemented "
						    "write len %i (ignored)\n",
						    len);
					}
					break;
				}
			} else {
				switch (len) {
				case 4:	wdc_addtoinbuf(d, (idata >> 24) & 0xff);
					wdc_addtoinbuf(d, (idata >> 16) & 0xff);
					wdc_addtoinbuf(d, (idata >> 8) & 0xff);
					wdc_addtoinbuf(d, idata & 0xff);
					break;
				case 2:	wdc_addtoinbuf(d, (idata >> 8) & 0xff);
					wdc_addtoinbuf(d, idata & 0xff);
					break;
				case 1:	wdc_addtoinbuf(d, idata); break;
				/*  #337: a 3- or 8-byte access to the data
				    port used to call exit(1) -- a GUEST
				    choosing an access width killed the host
				    process. Same halt class as #184/#186/
				    #187/#315/#316/#326. Drop the access and
				    say so once; a device that cannot honour
				    a transfer must not take the emulator
				    with it. (Unreachable from SH-4, which
				    has no 3- or 8-byte access, but reachable
				    from a 64-bit MIPS machine carrying wdc
				    over bus_isa/bus_pci.)  */
				default:/*  #478: `break` leaves the WIDTH SWITCH, not the
				            handler -- execution falls through to the
				            occupancy drain below with NOTHING pushed.  */
				        badlen_this = 1;
				        if (!d->warned_badlen) {
						d->warned_badlen = 1;
						fatal("wdc: unimplemented "
						    "write len %i (ignored)\n",
						    len);
					}
					break;
				}
			}

			inbuf_len = d->inbuf_head - d->inbuf_tail;
			while (inbuf_len < 0)
				inbuf_len += WDC_INBUF_SIZE;

			/*  #477: THE DISPATCH KEYS ON THE PHASE IN ADDITION TO THE FLAG.

			    *** THIS HEADLINE READ "ON THE PHASE, NOT ON THE FLAG" UNTIL
			    2026-08-27, AND THAT WORDING WAS UNSAFE.  The codex seat reasoned
			    on #477's pass 2 that deleting the flag conjunct would sweep the
			    detector; MEASURED, it swept all 52 rows clean. ***

			    BOTH CONJUNCTS ARE LOAD-BEARING, and the reason is a STALE PHASE.
			    `wdc_command(ATAPI_PKT_CMD)` sets PHASE_CMDOUT; a following
			    `wdc_command(WDCC_WRITE)` clears the flag at the top of that
			    function and arms the write -- and NOTHING RESETS THE PHASE.  The
			    device then sits in exactly the state a phase-only guard cannot
			    tell from a real CDB collection.

			    Under a phase-only guard the guest's own sector payload reaches
			    occupancy 12 and is issued as a SCSI command.  MEASURED, and worse
			    than the seat predicted: the sector does not merely lose twelve
			    bytes, it NEVER REACHES THE DISK -- `0 w, 0 b` against a wanted
			    one write of 512.  `row_stale_phase_write` pins both halves.

			    The stale phase is itself a defect; it is filed with
			    `wdcwipclear` / `wdcringnoflush` -- a new command does not reset
			    what the old one left.

			    `atapi_cmd_in_progress` is set when a packet command arrives and
			    cleared only when the NEXT command does -- so it stays 1 through the
			    whole of DATAIN and past PHASE_COMPLETED.  It conflates two roles: 'a
			    packet command is active' (read at four register sites through
			    completion, and must stay set) and 'I am collecting a 12-byte CDB'
			    (what this test actually wants).

			    So a guest write during DATAIN that brought ring occupancy to exactly
			    12 re-entered this block, FREED THE LIVE TRANSFER, and issued a SCSI
			    command built from the guest's own returned DATA-IN payload.  MEASURED:
			    `freed 1 live transfer(s)`.

			    NOT guarding the data-port write instead, and two measuring seats
			    agree: this check runs on EVERY data-port write regardless of what the
			    write did -- the width switch's `default:` arm (len 3 or 8) pushes
			    ZERO bytes and falls straight through to here.  Guarding the pushes
			    was MEASURED WORSE THAN NO FIX: with occupancy already 12 the
			    suppressed push leaves it at 12, so the guard CREATES a free on an
			    input the unfixed code survives.

			    Nor clearing the flag at completion: that leaves this window untouched
			    (the flag is legitimately 1 here) and breaks the ATAPI handshake --
			    ireason and the byte-count pair are read at PHASE_COMPLETED.  */
			/*  #479: A REJECTED WIDTH MUST NOT DISPATCH EITHER.

			    `#478` added `badlen_this` and guarded the sector DRAIN with
			    it, and recorded that this finally made `#337`'s `(ignored)`
			    message true.  It did not.  Two seats found it independently
			    on `#478`'s pass 2 -- one by reading, one by measuring a
			    3-byte store allocate an `atapi_st` -- and the row
			    `a rejected width issues no command` reds without this.

			    This dispatch runs on EVERY data-port write regardless of
			    what the write did, so an access of an unimplemented width
			    -- which pushes nothing and is announced as ignored -- still
			    issued a 12-byte SCSI command whenever occupancy already
			    stood at 12.  A rejected access with a side effect is worse
			    than either accepting or refusing it cleanly, because the
			    diagnostic says the opposite of what happened.  */
			if (d->atapi_cmd_in_progress && !badlen_this &&
			    d->atapi_phase == PHASE_CMDOUT && inbuf_len == 12) {
				unsigned char *scsi_cmd;
				int x = 0, res;

				/*  #477: THE `inbuf_len == 12` IN THE GUARD ABOVE IS WHAT BOUNDS THE
			    COPY BELOW.  `x` is not checked against 12, so the equality is not
			    only selecting the dispatch -- it is the only thing keeping this
			    12-byte allocation from overflowing with guest bytes.  A pass-2
			    mutant relaxing it to `>= 12` was MEASURED under ASAN as a
			    heap-buffer-overflow WRITE here, while the 44-row detector stayed
			    green -- and this round's own kill table had first classified that
			    edit as an IMPROVEMENT.  Four readers reasoned about the guard as a
			    dispatch selector and none opened these nine lines.  Do not widen
			    the equality; flush the ring instead (`wdcringnoflush`).  */
				CHECK_ALLOCATION(scsi_cmd = (unsigned char *) malloc(12));

				if (d->atapi_st != NULL)
					scsi_transfer_free(d->atapi_st);
				d->atapi_st = scsi_transfer_alloc();

				debug("[ wdc: ATAPI command ]\n");

				while (inbuf_len > 0) {
					scsi_cmd[x++] = wdc_get_inbuf(d);
					inbuf_len --;
				}

				d->atapi_st->cmd = scsi_cmd;
				d->atapi_st->cmd_len = 12;

				if (scsi_cmd[0] == SCSIBLOCKCMD_READ_CAPACITY
				    || scsi_cmd[0] == SCSICMD_READ_10
				    || scsi_cmd[0] == SCSICMD_MODE_SENSE10)
					d->atapi_st->cmd_len = 10;

				res = diskimage_scsicommand(cpu,
				    d->drive + d->base_drive, DISKIMAGE_IDE,
				    d->atapi_st);

				/*  #337: an ATAPI command the SCSI layer
				    rejected used to exit(1). Any guest that
				    issues an unsupported or malformed packet
				    command could therefore kill the host.
				    Complete the command instead: the phase
				    goes to COMPLETED with no data, and the
				    interrupt below still fires, which is how
				    a real drive reports a failed packet
				    command to its driver.  */
				if (res == 0) {
					if (!d->warned_atapi_err) {
						d->warned_atapi_err = 1;
						fatal("wdc: ATAPI command "
						    "rejected; completing "
						    "with no data\n");
					}
					d->atapi_len = 0;
					d->atapi_received = 0;
					d->atapi_phase = PHASE_COMPLETED;
					d->int_assert = 1;
					break;
				}

				d->atapi_len = 0;
				d->atapi_received = 0;

				if (res == 1) {
					if (d->atapi_st->data_in != NULL) {
						d->atapi_phase = PHASE_DATAIN;
						/*  #473: CLAMP BEFORE THE PUSH.  This loop was unbounded and the
						    clamp sat AFTER it, so a transfer larger than the ring was pushed
						    whole: WDC_INBUF_SIZE is exactly 513 blocks, and block 514 wrapped
						    onto unread data.  MEASURED: a 514-block transfer returned block
						    513's bytes where block 0's should be, and the latch fired one
						    store EARLIER than the corruption, because head==tail cannot tell
						    full from empty.  The clamp is not new -- it was on the wrong side
						    of the loop.  */
						d->atapi_len = d->atapi_st->data_in_len;
						if (d->atapi_len > 32768)
							d->atapi_len = 32768;

						for (int j=0; j<d->atapi_len; j++)
							wdc_addtoinbuf(d, d->atapi_st->data_in[j]);
					} else {
						d->atapi_phase =
						    PHASE_COMPLETED;
					}
				} else {
					/*  #337: this arm ALREADY set the
					    right phase and then called
					    exit(1) anyway, so removing the
					    abort is the whole fix -- any
					    ATAPI command wanting a DATA OUT
					    phase (MODE SELECT, for one) took
					    the host down. The transfer
					    itself is still unimplemented,
					    which is what the warning says.  */
					if (!d->warned_atapi_dataout) {
						d->warned_atapi_dataout = 1;
						fatal("wdc: ATAPI DATA OUT "
						    "phase not implemented\n");
					}
					d->atapi_phase = PHASE_DATAOUT;
				}

				d->int_assert = 1;
			}

			/*  #478: AN EMPTY RING MUST NOT BE READ AS A FULL SECTOR.

			    `inbuf_len == 0` satisfies `0 % 512 == 0`, so this block fired
			    with NOTHING queued and handed diskimage_access 512 bytes of
			    whatever the ring held, at the guest's chosen LBA.  MEASURED:
			    `1 write(s), 512 bytes to 0x8000, first=0xdd` -- the poison, so
			    the bytes written were ones the guest never supplied.

			    BOTH conditions are load-bearing and each closes a door the
			    other leaves open -- measured, not argued:

			      `inbuf_len > 0`   closes the empty ring, and the WRITE+PKT
			                        door where a CDB dispatch has already
			                        consumed the LOCAL inbuf_len to a stale 0
			                        while pushing fresh DATA-IN into the ring.
			      `!badlen_this`    closes the LEFTOVER door: an unread payload
			                        leaves occupancy at 512, so `512 > 0` passes
			                        and the guest's own returned data is written
			                        to the image.  MEASURED first=0xbe.

			    The drain is guarded rather than the `default:` arm because the
			    WRITE+PKT door involves no bad-len access at all.  */
			if (inbuf_len > 0 && !badlen_this &&
			    (( d->write_in_progress == WDCC_WRITEMULTI &&
			    inbuf_len % (512 * d->write_count) == 0)
			    ||
			    ( d->write_in_progress == WDCC_WRITE &&
			    inbuf_len % 512 == 0)) ) {
				int count = (d->write_in_progress ==
				    WDCC_WRITEMULTI)? d->write_count : 1;
				unsigned char *buf, *b;

				CHECK_ALLOCATION(buf = (unsigned char *) malloc(512 * count));
				b = buf;

				if (d->inbuf_tail+512*count <= WDC_INBUF_SIZE) {
					b = d->inbuf + d->inbuf_tail;
					d->inbuf_tail = (d->inbuf_tail + 512
					    * count) % WDC_INBUF_SIZE;
				} else {
					for (i=0; i<512 * count; i++)
						buf[i] = wdc_get_inbuf(d);
				}

				diskimage_access(cpu->machine,
				    d->drive + d->base_drive, DISKIMAGE_IDE, 1,
				    d->write_offset, b, 512 * count);

				d->write_count -= count;
				d->write_offset += 512 * count;

				d->int_assert = 1;

				if (d->write_count == 0)
					d->write_in_progress = 0;

				free(buf);
			} else if ((( d->write_in_progress == WDCC_WRITEMULTI &&
			    inbuf_len % (512 * d->write_count) == 0)
			    ||
			    ( d->write_in_progress == WDCC_WRITE &&
			    inbuf_len % 512 == 0)) && !d->warned_empty_drain) {
				/*  #478: DECLINE AND ANNOUNCE, per this tree's own #264
				    precedent -- dev_asc.c refuses a zero-length DATA_OUT
				    and SAYS SO rather than proceeding silently.

				    The condition is the DIFFERENCE between this fix and the
				    code it replaces, not the negation of the guard: the old
				    code drained on the modulus alone, so this fires exactly
				    where a spurious sector USED to reach the disk image.
				    Announcing on every non-draining write would fire on all
				    255 partial stores of an ordinary sector.

				    Without this the guest had NO notice at all: no error
				    bit, the handler returns 1, and the interrupt is still
				    asserted -- a write silently vanishing.  N=1 per device
				    instance with `(once)`, the tree's plurality marker.

				    fatal() and not debugmsg(): under -q the verbosity
				    settles at VERBOSITY_ERROR, so a WARNING would be
				    invisible to the boot-log hygiene grep and an ERROR
				    would trip #261's break-on-ERROR.  */
				d->warned_empty_drain = 1;
				/*  *** THE TEXT SAID "no sector buffered; write dropped" AND BOTH HALVES
				    COULD BE FALSE.  Measured by the Opus seat on #478 pass 2,
				    end-to-end through the registers, no struct poking. ***

				    `inbuf_len == 0` is reached by TWO routes: an empty ring, and a
				    STALE LOCAL after a CDB dispatch has consumed it.  On the second
				    the guest's bytes were USED, not dropped.  On the leftover door a
				    whole 512-byte sector sits in the ring while the message claims
				    none is buffered.

				    THE HARM WAS NOT THE FALSE SENTENCE.  A spurious emission BURNS
				    THE N=1 LATCH, so a later GENUINE drop is announced to nobody --
				    this announce could defeat itself, which is exactly the state the
				    decline-and-announce ruling exists to prevent.

				    The CONDITION is kept: it fires where the unfixed code would have
				    put a spurious sector on the disk image, which is worth saying
				    however the ring reached that state.  The TEXT now describes what
				    happened -- a drain was refused -- instead of asserting a buffer
				    state it never checked.  */
				fatal("[ wdc: refused a sector drain the buffer "
					"cannot justify (once) ]\n");
			}
		}
		break;

	case wd_error:	/*  1: error (r), precomp (w)  */
		if (writeflag == MEM_READ) {
			odata = d->error;
			debug("[ wdc: read from ERROR: 0x%02x ]\n", (int)odata);
		} else {
			d->precomp = idata;
			debug("[ wdc: write to PRECOMP: 0x%02x ]\n",(int)idata);
		}
		break;

	case wd_seccnt:	/*  2: sector count (or "ireason" for ATAPI)  */
		if (writeflag == MEM_READ) {
			odata = d->seccnt;
			if (d->atapi_cmd_in_progress) {
				odata = d->atapi_phase & (WDCI_CMD | WDCI_IN);
			}
			debug("[ wdc: read from SECCNT: 0x%02x ]\n",(int)odata);
		} else {
			d->seccnt = idata;
			debug("[ wdc: write to SECCNT: 0x%02x ]\n", (int)idata);
		}
		break;

	case wd_sector:	/*  3: first sector  */
		if (writeflag == MEM_READ) {
			odata = d->sector;
			debug("[ wdc: read from SECTOR: 0x%02x ]\n",(int)odata);
		} else {
			d->sector = idata;
			debug("[ wdc: write to SECTOR: 0x%02x ]\n", (int)idata);
		}
		break;

	case wd_cyl_lo:	/*  4: cylinder low  */
		if (writeflag == MEM_READ) {
			odata = d->cyl_lo;
			if (d->cur_command == COMMAND_RESET &&
			    diskimage_is_a_cdrom(cpu->machine,
			    d->drive + d->base_drive, DISKIMAGE_IDE))
				odata = 0x14;
			if (d->atapi_cmd_in_progress) {
				int x = d->atapi_len;
				if (x > 32768)
					x = 32768;
				odata = x & 255;
			}
			debug("[ wdc: read from CYL_LO: 0x%02x ]\n",(int)odata);
		} else {
			d->cyl_lo = idata;
			debug("[ wdc: write to CYL_LO: 0x%02x ]\n", (int)idata);
		}
		break;

	case wd_cyl_hi:	/*  5: cylinder high  */
		if (writeflag == MEM_READ) {
			odata = d->cyl_hi;
			if (d->cur_command == COMMAND_RESET &&
			    diskimage_is_a_cdrom(cpu->machine,
			    d->drive + d->base_drive, DISKIMAGE_IDE))
				odata = 0xeb;
			if (d->atapi_cmd_in_progress) {
				int x = d->atapi_len;
				if (x > 32768)
					x = 32768;
				odata = (x >> 8) & 255;
			}
			debug("[ wdc: read from CYL_HI: 0x%02x ]\n",(int)odata);
		} else {
			d->cyl_hi = idata;
			debug("[ wdc: write to CYL_HI: 0x%02x ]\n", (int)idata);
		}
		break;

	case wd_sdh:	/*  6: sectorsize/drive/head  */
		if (writeflag==MEM_READ) {
			odata = (d->sectorsize << 6) + (d->lba << 5) +
			    (d->drive << 4) + (d->head);
			debug("[ wdc: read from SDH: 0x%02x (sectorsize %i,"
			    " lba=%i, drive %i, head %i) ]\n", (int)odata,
			    d->sectorsize, d->lba, d->drive, d->head);
		} else {
			d->sectorsize = (idata >> 6) & 3;
			d->lba   = (idata >> 5) & 1;
			d->drive = (idata >> 4) & 1;
			d->head  = idata & 0xf;
			debug("[ wdc: write to SDH: 0x%02x (sectorsize %i,"
			    " lba=%i, drive %i, head %i) ]\n", (int)idata,
			    d->sectorsize, d->lba, d->drive, d->head);
		}
		break;

	case wd_command:	/*  7: command or status  */
		if (writeflag==MEM_READ) {
			odata = status_byte(d, cpu);
			if (!quiet_mode)
				debug("[ wdc: read from STATUS: 0x%02x ]\n",
				    (int)odata);
			INTERRUPT_DEASSERT(d->irq);
			d->int_assert = 0;
		} else {
			debug("[ wdc: write to COMMAND: 0x%02x ]\n",(int)idata);
			wdc_command(cpu, d, idata);
		}
		break;

	default:
		if (writeflag==MEM_READ)
			debug("[ wdc: read from 0x%02x ]\n",
			    (int)relative_addr);
		else
			debug("[ wdc: write to  0x%02x: 0x%02x ]\n",
			    (int)relative_addr, (int)idata);
	}

	/*  Assert interrupt, if necessary:  */
	dev_wdc_tick(cpu, extra);

ret:
	if (writeflag == MEM_READ) {
		if (relative_addr == wd_data)
			memory_writemax64(cpu, data, len, odata);
		else {
			/*  #464: latch the announcement only.  This sits
			    INSIDE the function's common `ret:` tail, so
			    `data[0] = odata` and the `return 1` below must run
			    regardless -- an early return here would hand the
			    guest an untouched read buffer.  */
			if (len != 1 && !d->warned_nonbyte_read) {
				d->warned_nonbyte_read = 1;
				fatal("[ wdc: WARNING! non-8-bit access on "
				    "READ! ]\n");
			}
			data[0] = odata;
		}
	}

	return 1;
}


DEVINIT(wdc)
{
	struct wdc_data *d;
	uint64_t alt_status_addr;
	int i, tick_shift = WDC_TICK_SHIFT;

	CHECK_ALLOCATION(d = (struct wdc_data *) malloc(sizeof(struct wdc_data)));
	memset(d, 0, sizeof(struct wdc_data));

	INTERRUPT_CONNECT(devinit->interrupt_path, d->irq);
	d->addr_mult  = devinit->addr_mult;
	d->data_debug = 1;
	d->io_enabled = 1;
	d->error      = 1;

	d->inbuf = (unsigned char *) zeroed_alloc(WDC_INBUF_SIZE);

	/*  base_drive = 0 for the primary controller, 2 for the secondary.  */
	d->base_drive = 0;
	if ((devinit->addr & 0xfff) == 0x170)
		d->base_drive = 2;

	alt_status_addr = devinit->addr + 0x206;

	/*  Special hacks for individual machines:  */
	switch (devinit->machine->machine_type) {
	case MACHINE_MACPPC:
		alt_status_addr = devinit->addr + 0x160;
		break;
	case MACHINE_HPCMIPS:
		/*  TODO: Fix  */
		if (devinit->addr == 0x14000180)
			alt_status_addr = 0x14000386;
		break;
	case MACHINE_IQ80321:
		alt_status_addr = devinit->addr + 0x402;
		break;
	}

	/*  Get disk geometries:  */
	for (i=0; i<2; i++)
		if (diskimage_exist(devinit->machine, d->base_drive +i,
		    DISKIMAGE_IDE))
			diskimage_getchs(devinit->machine, d->base_drive + i,
			    DISKIMAGE_IDE, &d->cyls[i], &d->heads[i],
			    &d->sectors_per_track[i]);

	memory_device_register(devinit->machine->memory, "wdc_altstatus",
	    alt_status_addr, 2, dev_wdc_altstatus_access, d, DM_DEFAULT, NULL);
	memory_device_register(devinit->machine->memory, devinit->name,
	    devinit->addr, DEV_WDC_LENGTH * devinit->addr_mult, dev_wdc_access,
	    d, DM_DEFAULT, NULL);

	machine_add_tickfunction(devinit->machine, dev_wdc_tick,
	    d, tick_shift);

	devinit->return_ptr = d;

	return 1;
}

