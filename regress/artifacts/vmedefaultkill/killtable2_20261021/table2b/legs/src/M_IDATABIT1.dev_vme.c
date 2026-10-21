/*
 *  Copyright (C) 2007-2009  Anders Gavare.  All rights reserved.
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
 *  COMMENT: VME bus
 *
 *  TODO: Probably almost everything.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "cpu.h"
#include "device.h"
#include "emul.h"
#include "machine.h"
#include "memory.h"
#include "misc.h"

#include "thirdparty/mvme88k_vme.h"


/*  #define debug fatal  */


#define	VME_LEN			0x1000

struct vme_data {
	uint32_t	reg[VME_LEN / sizeof(uint32_t)];

	/*  #568: one bit per register WORD (relative_addr >> 2) for the
	    unimplemented-register announce below; the highest such word is
	    VME2_MISC (0x8c >> 2 == 35).  Zeroed by DEVINIT's memset, so every
	    instance starts with every announce armed.  */
	uint64_t	warned_unimpl;
};

/*  #568: a warned_unimpl narrower than VME2_MISC >> 2 + 1 bits would
    leave MISC's announce bit outside the field; make that a compile error
    (dev_pcc2.c's pcc2_w_fits_in_warned shape).  The 1ULL in the shifts
    below is not checked here.  */
typedef char vme_warned_fits[(VME2_MISC >> 2) <
    8 * sizeof(((struct vme_data *)0)->warned_unimpl) ? 1 : -1];


DEVICE_ACCESS(vme)
{
	struct vme_data *d = (struct vme_data *) extra;
	uint64_t idata = 0, odata = 0;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	if (writeflag == MEM_READ)
		odata = d->reg[relative_addr / sizeof(uint32_t)];

	switch (relative_addr) {

	case 0:	/*  Used by OpenBSD/mvme88k when probing...  */
		break;

	case VME2_GCSRCTL:
		debug("[ vme: unimplemented GCSRCTL ]\n");
		break;

	case VME2_TCR:
		if (writeflag == MEM_READ)
			debug("[ vme: unimplemented READ from TCR ]\n");
		else
			debug("[ vme: unimplemented WRITE to TCR: "
			    "0x%x ]\n", (int)idata);
		break;

	case VME2_T1CMP:
		if (writeflag == MEM_WRITE)
			d->reg[relative_addr / sizeof(uint32_t)] = idata;
		break;

	case VME2_T1COUNT:
		if (writeflag == MEM_WRITE)
			d->reg[relative_addr / sizeof(uint32_t)] = idata;
		else {
			/*  NOTE! This is a quick hack. TODO: Fix!  */
			d->reg[relative_addr / sizeof(uint32_t)] += 100;
		}
		break;

	case VME2_TCTL:
		if (writeflag == MEM_WRITE)
			d->reg[relative_addr / sizeof(uint32_t)] = idata;

		/*  TODO  */
		/*  debug("[ vme: unimplemented TCTL ]\n");  */
		break;

	case VME2_IRQEN:
		if (writeflag == MEM_READ)
			debug("[ vme: unimplemented READ from IRQEN ]\n");
		else
			debug("[ vme: unimplemented WRITE to IRQEN: "
			    "0x%x ]\n", (int)idata);
		break;

	case VME2_IRQL3:
		if (writeflag == MEM_READ)
			debug("[ vme: unimplemented READ from IRQL3 ]\n");
		else
			debug("[ vme: unimplemented WRITE to IRQL3: "
			    "0x%x ]\n", (int)idata);
		break;

	case VME2_IRQL4:
		if (writeflag == MEM_READ)
			debug("[ vme: unimplemented READ from IRQL4 ]\n");
		else
			debug("[ vme: unimplemented WRITE to IRQL4: "
			    "0x%x ]\n", (int)idata);
		break;

	case VME2_VBR:
		/*  Vector Base Register.  */
		if (writeflag == MEM_WRITE)
			d->reg[relative_addr / sizeof(uint32_t)] = idata;
		break;

	/*  #568 (vmedefaultkill): registers the header names but this model
	    does not implement.  Each ended the emulator in default: below.
	    OpenBSD 2.2's mvme88k driver (sys/arch/mvme88k/dev/vme.c) has
	    access sites at six of them.  Its attach reaches four:
	    vme2chip_init() reads MASTERCTL and writes it back and writes
	    MASTER3, MASTER4 and MASTER4MOD.  The other two, IRQSTAT and
	    IRQCLR, are in vme2abort(), the ABORT-switch interrupt handler,
	    and this model raises no VME2 interrupt.  A bus error here
	    would panic that guest's attach, so these DECLINE: a read is served
	    the word preloaded above, which is 0 because nothing writes these
	    words of d->reg[] (odata is deliberately not forced to 0, so a store
	    added by a later edit would show in a read-back); a write is
	    dropped; one fatal() per register per device, the first access's
	    direction deciding its wording (#501's shape in dev_pcc2.c).
	    Sub-word starts inside these words are not matched here and reach
	    default: (vmewidthlanes).  */
	case VME2_SADDR2:
	case VME2_SLAVELMOD1:
	case VME2_SLAVELMOD2:
	case VME2_SLAVECTL:
	case VME2_MASTER1:
	case VME2_MASTER2:
	case VME2_MASTER3:
	case VME2_MASTER4:
	case VME2_MASTER4MOD:
	case VME2_MASTERCTL:
	case VME2_DMACTL:
	case VME2_DMAMODE:
	case VME2_DMALADDR:
	case VME2_DMAVMEADDR:
	case VME2_DMACOUNT:
	case VME2_DMATABLE:
	case VME2_DMASTAT:
	case VME2_T2CMP:
	case VME2_T2COUNT:
	case VME2_PRESCALE:
	case VME2_IRQSTAT:
	case VME2_SETSOFTIRQ:
	case VME2_IRQCLR:
	case VME2_IRQL1:
	case VME2_IRQL2:
	case VME2_MISC:
		if (!(d->warned_unimpl & (1ULL << (relative_addr >> 2)))) {
			d->warned_unimpl |= 1ULL << (relative_addr >> 2);
			if (writeflag == MEM_WRITE && !(idata & 2))
				fatal("[ vme: unimplemented write to register "
				    "0x%x (len %d): 0x%llx -- declined.  (once) ]\n",
				    (unsigned) relative_addr, (int) len,
				    (unsigned long long) idata);
			else
				fatal("[ vme: unimplemented read from register "
				    "0x%x (len %d) -- served 0x%llx.  (once) ]\n",
				    (unsigned) relative_addr, (int) len,
				    (unsigned long long) odata);
		}
		break;

	default:if (writeflag == MEM_READ)
			debug("[ vme: unimplemented READ from offset 0x%x ]"
			    "\n", (int)relative_addr);
		else
			debug("[ vme: unimplemented WRITE to offset 0x%x: "
			    "0x%x ]\n", (int)relative_addr, (int)idata);
		/*  #568 (vmedefaultkill): an offset this model does not service:
		    no header-named register, or the inside of one (a sub-word
		    start).  Refuse the access -- for a guest data load or store,
		    memory_rw then raises the m88k data-access exception, the bus
		    error a badaddr() probe expects -- instead of exit(1), which
		    ended the emulator with no visible reason (debug() is silent
		    at default verbosity).  */
		return 0;
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}


DEVINIT(vme)
{
	struct vme_data *d;

	CHECK_ALLOCATION(d = (struct vme_data *) malloc(sizeof(struct vme_data)));
	memset(d, 0, sizeof(struct vme_data));

	/*  According to OpenBSD/mvme88k:  */
	d->reg[VME2_VBR / sizeof(uint32_t)] =
	    VME2_SET_VBR0(6) + VME2_SET_VBR1(7);

	memory_device_register(devinit->machine->memory, devinit->name,
	    devinit->addr, VME_LEN, dev_vme_access, (void *)d,
	    DM_DEFAULT, NULL);

	return 1;
}

