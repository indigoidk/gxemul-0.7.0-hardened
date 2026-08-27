/*
 *  Copyright (C) 2006-2011  Anders Gavare.  All rights reserved.
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
 *  COMMENT: Dreamcast-specific ASIC
 *
 *  A simple device which forwards various Dreamcast device events as
 *  interrupts 13, 11, or 9, to the CPU.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

#include "cpu.h"
#include "device.h"
#include "machine.h"
#include "memory.h"
#include "misc.h"

#include "thirdparty/dreamcast_sysasicvar.h"
#include "thirdparty/sh4_exception.h"


// #define debug fatal

#define	DREAMCAST_ASIC_TICK_SHIFT	15

struct dreamcast_asic_data {
	uint32_t	pending_irq[3];
	uint32_t	mask_13[3];
	uint32_t	mask_11[3];
	uint32_t	mask_9[3];

	int		asserted_13;
	int		asserted_11;
	int		asserted_9;

	struct interrupt irq_13;
	struct interrupt irq_11;
	struct interrupt irq_9;
};


DEVICE_TICK(dreamcast_asic)
{
	struct dreamcast_asic_data *d = (struct dreamcast_asic_data *) extra;
	int i, old_asserted_13 = d->asserted_13, old_asserted_11 =
	    d->asserted_11, old_asserted_9 = d->asserted_9;

	d->asserted_13 = d->asserted_11 = d->asserted_9 = 0;

	for (i=0; i<3; i++) {
		if (d->pending_irq[i] & d->mask_13[i])
			d->asserted_13 = 1;

		if (d->pending_irq[i] & d->mask_11[i])
			d->asserted_11 = 1;

		if (d->pending_irq[i] & d->mask_9[i])
			d->asserted_9 = 1;
	}

	if (d->asserted_13 != old_asserted_13) {
		if (d->asserted_13)
			INTERRUPT_ASSERT(d->irq_13);
		else
			INTERRUPT_DEASSERT(d->irq_13);
	}
	if (d->asserted_11 != old_asserted_11) {
		if (d->asserted_11)
			INTERRUPT_ASSERT(d->irq_11);
		else
			INTERRUPT_DEASSERT(d->irq_11);
	}
	if (d->asserted_9 != old_asserted_9) {
		if (d->asserted_9)
			INTERRUPT_ASSERT(d->irq_9);
		else
			INTERRUPT_DEASSERT(d->irq_9);
	}
}


DEVICE_ACCESS(dreamcast_asic)
{
	struct dreamcast_asic_data *d = (struct dreamcast_asic_data *) extra;
	uint64_t idata = 0, odata = 0;
	int r;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	r = (relative_addr / 4) & 3;

	/*  #463: the whole `if (r == 3)` block is gone, not just its exit(1).
	    It ended the host process on a SINGLE GUEST LOAD at any of SIXTY-FOUR
	    byte addresses -- `r == 3` is exactly (relative_addr & 0x0c) == 0x0c,
	    the fourth word of every 16-byte group, and relative_addr need not be
	    word-aligned (memory_rw.c passes the raw sub-word offset), so a byte
	    access at +0x0d dies like +0x0c.  Not merely reserved space either:
	    an SZ=1 fmov.d based at +0x18 reaches +0x1c and dies, whichever half
	    it issues first.  ISSUE ORDER IS NOT UNIFORM and is NOT load-bearing:
	    cpu_sh_instr.c:790-798 is the @Rm form only, which reads addr+4 first,
	    while fmov @Rm+,DRn and fmov @(R0,Rm),DRn read the low word first.
	    An earlier draft of this comment asserted addr+4-first as a general
	    decoder fact and used it as a warrant; it is neither.

	    THAT IS A CLASS, NOT ONE EXAMPLE -- TRANSACTION CLOSURE.  A base
	    OUTSIDE the 64 dies when any LANE of its transaction lands inside:
	    16 eight-byte bases (0x08, 0x18, 0x28 ...) die on their high word,
	    and all 8 aligned 32-byte store-queue bases span exactly TWO killing
	    words (base 0 hits 0x0c and 0x1c), dying MID-BURST with earlier words
	    already committed.  So 64 is a FLOOR on reachability, not the total.

	    All THREE parts had to go.  exit(1) is the kill.  fatal() has no
	    early-out (core/debugmsg.c:384-390, against debug()'s in that
	    same file at core/debugmsg.c:375), so
	    keeping it turns a host kill into an unsilenceable guest-drivable
	    flood.  And `r = 0` is a latent clamp hazard: dead today, but it is
	    exactly what a later widening would use to alias offsets silently.

	    Deleting the block is a TRADE, not parity: r == 3 now falls to
	    `default:` arm below, which prints the ADDRESS that "Bad address"
	    never did -- but via debug(), so -q silences it and free-running at
	    verbose 0 it says nothing, where fatal() printed unconditionally.

	    THE INVARIANT.  r indexes uint32_t[3], and the struct above declares
	    pending_irq[3], mask_13[3], mask_11[3], mask_9[3] CONSECUTIVELY --
	    so mask_13[4] LANDS ON mask_11[1] under this toolchain -- the
	    subscript is UNDEFINED BEHAVIOUR whatever the members' adjacency,
	    so this is a measured layout outcome and not a fact of C -- and a
	    stray index corrupts a neighbour
	    silently.  Staying in bounds needs BOTH:
	      (i)  every `case` label satisfies (label & 0x0c) != 0x0c; and
	      (ii) the WHOLE index expression `(relative_addr / 4) & 3` is
	           preserved -- divisor AND mask, not the mask alone.
	    Half (i) is ENUMERATED, not asserted: all twelve labels (0, 4, 8,
	    0x10/14/18, 0x20/24/28, 0x30/34/38) give MAX r = 2.  Half (ii) is
	    stated as the whole expression because three measured escapes keep
	    (i) textually satisfied while breaking the mapping: `& 2` aliases
	    +0x14 onto +0x10, `& 1` and `/ 2` both alias +0x18 onto +0x10, and
	    `& 7` walks out of bounds.  Rows alias, alias2 and crossarr pin them.

	    Note the exit(1) was ALSO doing bounds duty.  r == 3 reaching the
	    switch is a NEW PAIRING, not a new path: `default:` was already
	    reachable for 180 of the 256 offsets (256 - 12 labels - 64
	    killing) and it ignores r entirely.  Computing r == 3
	    is not itself out of bounds -- only array[r] would be -- and nothing
	    on that path indexes: `default:` is two debug() calls.  A future
	    edit adding an INDEXING case at an r == 3 offset would be a silent
	    out-of-bounds access that no detector row sees; filed, `asicindexcase`.

	    Deliberately a comment, not a runtime guard: configure:312-314 adds
	    -DNDEBUG unless DEBUG=YES, so an assert() compiles out of every
	    default build and protects nothing shipped.

	    Governs THIS FILE ONLY.  SYSASIC_EVENT_TO_ADDR() reaches a fourth
	    word via a header #define no comment here can reach:
	    dreamcast_sysasicvar.h's SYSASIC_EVENT_TO_ADDR is 4*((e)>>5), which
	    lands on an r == 3
	    offset exactly when (e>>5) & 3 == 3 -- e in [96,127] -> +0x0c, then
	    [224,255] -> +0x1c, [352,383] -> +0x2c.  It is the SAME fourth-word
	    pattern one level up, NOT a single range: an earlier draft said
	    "any event >= 96", which is false ([128,159] -> +0x10, r == 0).
	    Max over all 21 defines is 67 (dreamcast_sysasicvar.h:72) and 67>>5 == 2, so it
	    is LATENT, not live.  Filed as `asiceventaddr`.  */

	switch (relative_addr) {

	case 0:
	case 4:
	case 8:	if (writeflag == MEM_READ) {
			odata = d->pending_irq[r];
		} else {
			/*  Should only be used interally by GXemul:  */
			if (idata & 0x100000000ULL) {
				/*  Set specific bits:  */
				d->pending_irq[r] |= idata;
			} else {
				/*  Clear interrupt assertions:  */
				d->pending_irq[r] &= ~idata;
			}
			dev_dreamcast_asic_tick(cpu, d);
		}
		break;

	case 0x10:
	case 0x14:
	case 0x18:
		if (writeflag == MEM_WRITE) {
			d->mask_13[r] = idata;
			dev_dreamcast_asic_tick(cpu, d);
		} else {
			odata = d->mask_13[r];
		}
		break;

	case 0x20:
	case 0x24:
	case 0x28:
		if (writeflag == MEM_WRITE) {
			d->mask_11[r] = idata;
			dev_dreamcast_asic_tick(cpu, d);
		} else {
			odata = d->mask_11[r];
		}
		break;

	case 0x30:
	case 0x34:
	case 0x38:
		if (writeflag == MEM_WRITE) {
			d->mask_9[r] = idata;
			dev_dreamcast_asic_tick(cpu, d);
		} else {
			odata = d->mask_9[r];
		}
		break;

	default:if (writeflag == MEM_READ) {
			debug("[ dreamcast_asic: read from addr 0x%x ]\n",
			    (int)relative_addr);
		} else {
			debug("[ dreamcast_asic: write to addr 0x%x: 0x%x ]\n",
			    (int)relative_addr, (int)idata);
		}
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}


DEVINIT(dreamcast_asic)
{
	char tmpstr[300];
	struct machine *machine = devinit->machine;
	struct dreamcast_asic_data *d;

	CHECK_ALLOCATION(d = (struct dreamcast_asic_data *) malloc(sizeof(struct dreamcast_asic_data)));
	memset(d, 0, sizeof(struct dreamcast_asic_data));

	/*  Connect to SH4 interrupt levels 13, 11, and 9:  */
	snprintf(tmpstr, sizeof(tmpstr), "%s.irq[0x%x]",
	    devinit->interrupt_path, SH_INTEVT_IRL13);
	INTERRUPT_CONNECT(tmpstr, d->irq_13);
	snprintf(tmpstr, sizeof(tmpstr), "%s.irq[0x%x]",
	    devinit->interrupt_path, SH_INTEVT_IRL11);
	INTERRUPT_CONNECT(tmpstr, d->irq_11);
	snprintf(tmpstr, sizeof(tmpstr), "%s.irq[0x%x]",
	    devinit->interrupt_path, SH_INTEVT_IRL9);
	INTERRUPT_CONNECT(tmpstr, d->irq_9);

	memory_device_register(machine->memory, devinit->name, SYSASIC_BASE,
	    SYSASIC_SIZE, dev_dreamcast_asic_access, d, DM_DEFAULT, NULL);

	machine_add_tickfunction(devinit->machine, dev_dreamcast_asic_tick, d,
	    DREAMCAST_ASIC_TICK_SHIFT);

	return 1;
}

