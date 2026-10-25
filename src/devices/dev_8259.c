/*
 *  Copyright (C) 2005-2009  Anders Gavare.  All rights reserved.
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
 *  COMMENT: Intel 8259 Programmable Interrupt Controller
 *
 *  See the following URL for more details:
 *	http://www.nondot.org/sabre/os/files/MiscHW/8259pic.txt
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "cpu.h"
#include "device.h"
#include "devices.h"
#include "emul.h"
#include "machine.h"
#include "memory.h"
#include "misc.h"


#define	DEV_8259_LENGTH		2

/*  #define DEV_8259_DEBUG  */


/*
 *  pic8259_acknowledge():
 *
 *  #574: The acknowledge this model never had.  The chip moves the highest-priority
 *  unmasked request to service when the CPU acknowledges it (the INTA cycle, or the
 *  read that follows an OCW3 poll): the ISR bit is set and, in edge mode -- the only
 *  mode this tree's guests program (ICW1 0x11) -- the IRR bit is reset.  Called from
 *  the poll read below and from the GT64120 interrupt-acknowledge read (dev_gt.c).
 *  Line 0 of pic1 is the 8253, whose pending-event count is retired here: dev_8253.c
 *  publishes it through machine->isa_pic_data, and bus_isa.c's own decrement runs
 *  only inside a deassert the 8253 never issues.  Returns the acknowledged line, or
 *  -1 when no unmasked request is pending (nothing changes).
 */
int pic8259_acknowledge(struct pic8259_data *d, struct machine *m)
{
	struct isa_pic_data *p = &m->isa_pic_data;
	int pending = d->irr & ~d->ier, n = 0;

	if (pending == 0)
		return -1;
	while (!(pending & (1 << n)))
		n ++;
	d->isr |= 1 << n;
	d->irr &= ~(1 << n);
	if (d == p->pic1 && n == 0 && p->pending_timer_interrupts != NULL &&
	    *p->pending_timer_interrupts > 0)
		(*p->pending_timer_interrupts) --;
	/*  pic2's irq is the cascade line (bus_isa.c folds it into pic1 bit 2).  */
	if (d->irr & ~d->ier)
		INTERRUPT_ASSERT(d->irq);
	else
		INTERRUPT_DEASSERT(d->irq);
	return n;
}


DEVICE_ACCESS(8259)
{
	struct pic8259_data *d = (struct pic8259_data *) extra;
	uint64_t idata = 0, odata = 0;
	int i;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

#ifdef DEV_8259_DEBUG
	if (writeflag == MEM_READ)
		fatal("[ 8259: read from 0x%x ]\n", (int)relative_addr);
	else
		fatal("[ 8259: write to 0x%x: 0x%x ]\n",
		    (int)relative_addr, (int)idata);
#endif

	switch (relative_addr) {
	case 0x00:
		if (writeflag == MEM_WRITE) {
			if ((idata & 0x10) == 0x10) {
				/*  Bit 3: 0=edge, 1=level  */
				if (idata & 0x08)
					fatal("[ 8259: TODO: Level "
					    "triggered (MCA bus) ]\n");
				if (idata & 0x04)
					fatal("[ 8259: WARNING: Bit 2 set ]\n");
				/*  Bit 1: 0=cascade, 1=single  */
				/*  Bit 0: 1=4th init byte  */
				/*  This happens on non-x86 systems:
				    if (!(idata & 0x01))
					fatal("[ 8259: WARNING: Bit 0 NOT set!"
					    "!! ]\n");  */
				d->init_state = 1;
				break;
			}

			/*  TODO: Is it ok to abort init state when there
			    is a non-init command?  */
			if (d->init_state)
				fatal("[ 8259: WARNING: Was in init-state, but"
				    " it was aborted? ]\n");
			d->init_state = 0;

			if (idata == 0x0a) {
				d->current_command = 0x0a;
			} else if (idata == 0x0b) {
				d->current_command = 0x0b;
			} else if (idata == 0x0c) {
				/*  Put Master in Buffered Mode  */
				d->current_command = 0x0c;
			} else if (idata == 0x20) {
				/*  Non-specific End Of Interrupt.  #574: resets
				    the highest-priority in-service bit (the lowest
				    set ISR bit, fixed priority) and nothing else;
				    the request bits belong to the lines and to the
				    acknowledge (pic8259_acknowledge).  This arm
				    also did irr &= ~isr; isr = 0 -- a no-op on
				    irr while nothing set isr.  */
				/*  TODO: in buffered mode, is this an EOI 0? */
				if (d->isr)
					d->isr &= ~(d->isr & -d->isr);
			} else if ((idata >= 0x21 && idata <= 0x27) ||
			    (idata >= 0x60 && idata <= 0x67) ||
			    (idata >= 0xe0 && idata <= 0xe7)) {
				/*  Specific EOI.  #574: when the line is in
				    service (an acknowledge -- the poll read, or
				    the GT IACK read -- moved its request to ISR),
				    the EOI resets that ISR bit and leaves the
				    request bit alone, as on the chip.  When it is
				    NOT (a guest whose vector read acknowledges
				    nothing -- dev_prep.c, dev_footbridge.c -- or
				    none at all), the EOI still consumes the
				    request as it always did here: that consume
				    is the only one those machines have.  */
				int bit = 1 << (idata & 7);
				if (d->isr & bit) {
					d->isr &= ~bit;
				} else {
					int old_irr = d->irr;
					d->irr &= ~bit;
					if ((old_irr & ~d->ier) !=
					    (d->irr & ~d->ier)) {
						if (d->irr & ~d->ier)
							INTERRUPT_ASSERT(d->irq);
						else
							INTERRUPT_DEASSERT(d->irq);
					}
				}
			} else if (idata == 0x68) {
				/*  Set Special Mask Mode  */
				/*  TODO  */
			} else if (idata >= 0xc0 && idata <= 0xc7) {
				/*  Set IRQ Priority Order  */
				/*  TODO  */
			} else {
				fatal("[ 8259: unimplemented command 0x%02x"
				    " ]\n", (int)idata);
				cpu->running = 0;
			}
		} else {
			switch (d->current_command) {
			case 0x0a:
				odata = d->irr;
				break;
			case 0x0b:
				odata = d->isr;
				break;
			case 0x0c:
				/*  The read after an OCW3 poll.  #574: it is the
				    interrupt acknowledge (the datasheet's "sets
				    the appropriate IS bit"), of the highest
				    unmasked request -- the raw irr scan that stood
				    here returned masked lines too.  One read per
				    poll: later reads return the IRR until the next
				    OCW3.  */
				i = pic8259_acknowledge(d, cpu->machine);
				odata = i < 0 ? 0x00 : (0x80 | i);
				d->current_command = 0x0a;
				break;
			default:
				odata = 0x00;
				for (i=0; i<8; i++)
					if ((d->irr >> i) & 1) {
						odata = 0x80 | i;
						break;
					}
				break;
			/*
			 *  TODO: The "default" label should really do
			 *  something like this:
			 *
			 *	fatal("[ 8259: unimplemented command 0x%02x"
			 *	    " while reading ]\n", d->current_command);
			 *	cpu->running = 0;
			 *
			 *  but Linux seems to read from the secondary PIC
			 *  in a manner which works better the way things
			 *  are coded right now.
			 */
			}
		}
		break;
	case 0x01:
		if (d->init_state > 0) {
			if (d->init_state == 1) {
				d->irq_base = idata & 0xf8;
				/*  This happens on non-x86 machines:
				    if (idata & 7)
					fatal("[ 8259: WARNING! Lowest"
					    " bits in Init Cmd 1 are"
					    " non-zero! ]\n");  */
				d->init_state = 2;
			} else if (d->init_state == 2) {
				/*  Slave attachment. TODO  */
				d->init_state = 3;
			} else if (d->init_state == 3) {
				if (idata & 0x02) {
					/*  Should not be set in PCs, but
					    on CATS, for example, it is set.  */
					debug("[ 8259: WARNING! Bit 1 i"
					    "n Init Cmd 4 is set! ]\n");
				}
				if (!(idata & 0x01))
					fatal("[ 8259: WARNING! Bit 0 "
					    "in Init Cmd 4 is not"
					    " set! ]\n");
				d->init_state = 0;
			}
			break;
		}

		if (writeflag == MEM_WRITE) {
			int old_ier = d->ier;
			d->ier = idata;

			/*  Recalculate interrupt assertions,
			    if necessary:  */
			if ((d->irr & ~old_ier) != (d->irr & ~d->ier)) {
				if (d->irr & ~d->ier)
					INTERRUPT_ASSERT(d->irq);
				else
					INTERRUPT_DEASSERT(d->irq);
			}
		} else {
			odata = d->ier;
		}
		break;
	default:
		if (writeflag == MEM_WRITE) {
			fatal("[ 8259: unimplemented write to address 0x%x"
			    " data=0x%02x ]\n", (int)relative_addr, (int)idata);
			cpu->running = 0;
		} else {
			fatal("[ 8259: unimplemented read from address 0x%x "
			    "]\n", (int)relative_addr);
			cpu->running = 0;
		}
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}


/*
 *  devinit_8259():
 *
 *  Initialize an 8259 PIC. Important notes:
 *
 *	x)  Most systems use _TWO_ 8259 PICs. These should be registered
 *	    as separate devices.
 *
 *	x)  The irq number specified is the number used to re-calculate
 *	    CPU interrupt assertions.  It is _not_ the irq number at
 *	    which the PIC is connected. (That is left to machine specific
 *	    code in src/machine.c.)
 */
DEVINIT(8259)
{
	struct pic8259_data *d;
	char *name2;
	size_t nlen = strlen(devinit->name) + 20;

	CHECK_ALLOCATION(d = (struct pic8259_data *) malloc(sizeof(struct pic8259_data)));
	memset(d, 0, sizeof(struct pic8259_data));

	INTERRUPT_CONNECT(devinit->interrupt_path, d->irq);

	CHECK_ALLOCATION(name2 = (char *) malloc(nlen));
	snprintf(name2, nlen, "%s", devinit->name);
	if ((devinit->addr & 0xfff) == 0xa0) {
		strlcat(name2, " [secondary]", nlen);
		d->irq_base = 8;
	}

	memory_device_register(devinit->machine->memory, name2,
	    devinit->addr, DEV_8259_LENGTH, dev_8259_access, d,
	    DM_DEFAULT, NULL);

	devinit->return_ptr = d;
	return 1;
}

