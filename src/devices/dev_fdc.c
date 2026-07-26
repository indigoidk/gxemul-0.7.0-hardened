/*
 *  Copyright (C) 2003-2009  Anders Gavare.  All rights reserved.
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
 *  COMMENT: PC-style floppy controller
 *
 *  TODO!  (This is just a dummy skeleton right now.)
 *
 *  TODO 2: Make it work nicely with both ARC and PC emulation.
 *
 *  See http://members.tripod.com/~oldboard/assembly/765.html for a
 *  quick overview.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "device.h"
#include "interrupt.h"
#include "machine.h"
#include "memory.h"
#include "misc.h"


#define	DEV_FDC_LENGTH		6	/*  TODO 8, but collision with wdc  */


struct fdc_data {
	uint8_t			reg[DEV_FDC_LENGTH];
	struct interrupt	irq;
};


DEVICE_ACCESS(fdc)
{
	struct fdc_data *d = (struct fdc_data *) extra;
	uint64_t idata = 0, odata = 0;
	size_t i;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	switch (relative_addr) {
	case 0x04:
		break;
	default:/*
		 *  #280: this dummy skeleton models exactly one register --
		 *  0x04, the Main Status Register, handled above -- so every
		 *  other offset lands here, and an ungated fatal() emitted one
		 *  host line per guest access (measured: 1.00 lines/access,
		 *  read and write alike).
		 *
		 *  Gated at DEBUG like #276, NOT latched like #277/#279,
		 *  because the guest IS told: the probe fails through modelled
		 *  behaviour and the OS draws the right conclusion by itself
		 *  ("fdc at pica0 slot 2 offset 0x0 not configured"). A latch
		 *  would be actively wrong here -- fdcprobe's reset pulse is
		 *  TWO writes to reg 2 (0x00, then FDO_FRST), and a latch
		 *  would suppress the second one, the only interesting thing
		 *  this site shows.
		 *
		 *  The write arm's 2+len fatal() calls built ONE line between
		 *  them (only the closer carried the newline); they collapse
		 *  into a single debugmsg with the bytes pre-formatted into a
		 *  buffer sized from the register array, never from len.
		 */
		if (writeflag==MEM_READ) {
			debugmsg(SUBSYS_DEVICE, "fdc", VERBOSITY_DEBUG,
			    "read from reg %i", (int)relative_addr);
			odata = d->reg[relative_addr];
		} else {
			char buf[3 * DEV_FDC_LENGTH + 1];
			size_t p = 0;

			buf[0] = '\0';
			for (i=0; i<len && i<DEV_FDC_LENGTH; i++)
				p += snprintf(buf + p, sizeof(buf) - p,
				    " %02x", data[i]);

			debugmsg(SUBSYS_DEVICE, "fdc", VERBOSITY_DEBUG,
			    "write to reg %i:%s", (int)relative_addr, buf);
			d->reg[relative_addr] = idata;
		}
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}


DEVINIT(fdc)
{
	struct fdc_data *d;

	CHECK_ALLOCATION(d = (struct fdc_data *) malloc(sizeof(struct fdc_data)));
	memset(d, 0, sizeof(struct fdc_data));

	INTERRUPT_CONNECT(devinit->interrupt_path, d->irq);

	memory_device_register(devinit->machine->memory, devinit->name,
	    devinit->addr, DEV_FDC_LENGTH, dev_fdc_access, d,
	    DM_DEFAULT, NULL);

	return 1;
}

