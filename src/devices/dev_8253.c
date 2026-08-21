/*
 *  Copyright (C) 2005-2020  Anders Gavare.  All rights reserved.
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
 *  COMMENT: Intel 8253/8254 Programmable Interval Timer
 *
 *  TODO/NOTE:
 *	The timers don't really count down. Timer 0 causes clock interrupts
 *	at a specific frequency, but reading the counter register would not
 *	result in anything meaningful.
 *
 *  (Split counter[] into reset value and current value.)
 *
 *  #439: A consequence of the above, stated here because it is what a guest
 *  actually notices: the counter-latch command has nothing to latch, so a
 *  latched read returns 0 -- NOT the reload value.  Sub-tick interpolation,
 *  which is why guests issue the latch at all, is therefore unmodelled.
 *  Returning the reload value instead would be worse than useless: a guest
 *  that calibrates by dividing by (reload - latched_count), as OpenBSD's
 *  findcpuspeed() does, would divide by zero.  The latch is accepted and, as
 *  of #439, leaves the counter's programming intact.
 *
 *  #440: ...and, as of #440, is CONSUMED by the reads that follow it, per the
 *  programmed byte format.  #439 set the flag and cleared it only on a mode
 *  write, so one latch command made every later read of that counter return 0
 *  indefinitely.  Found by the #439 pass-2 review (Codex 5.6-SOL).
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "cpu.h"
#include "device.h"
#include "emul.h"
#include "interrupt.h"
#include "machine.h"
#include "memory.h"
#include "misc.h"
#include "timer.h"

#include "thirdparty/i8253reg.h"


/*  #define debug fatal  */

#define	DEV_8253_LENGTH		4
#define	TICK_SHIFT		14


struct pit8253_data {
	int		in_use;

	int		counter_select;
	uint8_t		mode_byte;

	int		mode[3];
	int		counter[3];
	int		latched[3];	/*  #439: latch command pending  */

	/*
	 *  #440: the read/write flip-flops.  1 means "the MSB is the half the
	 *  next access refers to".  READS AND WRITES GET SEPARATE ONES -- and
	 *  that is INFERRED from an observable sequence, not quoted: the local
	 *  i8254 text never uses the phrase "read/write flip-flop" at all (its
	 *  only "flip-flop" hits are the GATE edge detector).  What it does
	 *  give, at _scratchpad/i8254.txt p. 8, is
	 *
	 *	1) Read least significant byte	2) Write new least significant byte
	 *	3) Read most significant byte	4) Write new most significant byte
	 *
	 *  as a valid sequence, and one shared flip-flop cannot produce it --
	 *  step 1 would advance it past step 2's LSB.
	 */
	int		rd_msb[3];
	int		wr_msb[3];

	int		hz[3];

	struct timer	*timer0;
	struct interrupt irq;
	int		pending_interrupts_timer0;
};


static void timer0_tick(struct timer *t, void *extra)
{
	struct pit8253_data *d = (struct pit8253_data *) extra;
	d->pending_interrupts_timer0 ++;

	/*  printf("%i ", d->pending_interrupts_timer0); fflush(stdout);  */
}


DEVICE_TICK(8253)
{
	struct pit8253_data *d = (struct pit8253_data *) extra;

	if (!d->in_use)
		return;

	// Generate interrupts regardless of (d->mode[0] & 0x0e)?
	// (It seems like Linux/MALTA kernels like this.)
	if (d->pending_interrupts_timer0 > 0)
		INTERRUPT_ASSERT(d->irq);
}


DEVICE_ACCESS(8253)
{
	struct pit8253_data *d = (struct pit8253_data *) extra;
	uint64_t idata = 0, odata = 0;
	int rw = 0;		/*  #440: the half THIS access refers to  */

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	d->in_use = 1;

	switch (relative_addr) {

	case I8253_TIMER_CNTR0:
	case I8253_TIMER_CNTR1:
	case I8253_TIMER_CNTR2:
		/*
		 *  #440: in the 16-bit format it is the counter's read/write
		 *  flip-flop -- not mode_byte -- that says which half an access
		 *  refers to, and it ALTERNATES: LSB, MSB, LSB, ...
		 *
		 *  The old code cleared I8253_TIMER_LSB in mode_byte instead,
		 *  and nothing ever set it back, so the selector stuck at MSB
		 *  after one access and took the record of the programmed
		 *  format with it (the test below could then never match).  A
		 *  second 16-bit write pair therefore put BOTH of its bytes in
		 *  the high half: an extra, unasked-for reprogramming, and with
		 *  a low byte of 0x00 a transient count of ZERO from a guest
		 *  that never programmed one.
		 *
		 *  Resolving the half here means the switches below can no
		 *  longer see I8253_TIMER_16BIT; their default arms still catch
		 *  a counter touched before any control word (rw == LATCH == 0).
		 */
		rw = d->mode_byte & 0x30;
		if (rw == I8253_TIMER_16BIT)
			rw = (writeflag == MEM_WRITE ? d->wr_msb[relative_addr]
			    : d->rd_msb[relative_addr]) ?
			    I8253_TIMER_MSB : I8253_TIMER_LSB;

		if (writeflag == MEM_WRITE) {
			switch (rw) {
			case I8253_TIMER_LSB:
				d->counter[relative_addr] &= 0xff00;
				d->counter[relative_addr] |= (idata & 0xff);
				break;
			case I8253_TIMER_MSB:
				d->counter[relative_addr] &= 0x00ff;
				d->counter[relative_addr] |= ((idata&0xff)<<8);
				if (d->counter[relative_addr] != 0)
					d->hz[relative_addr] = (int) (
					    I8253_TIMER_FREQ / (float)
					    d->counter[relative_addr] + 0.5);
				else
					d->hz[relative_addr] = 0;
				debug("[ 8253: counter %i set to %i (%i Hz) "
				    "]\n", relative_addr, d->counter[
				    relative_addr], d->hz[relative_addr]);
				switch (relative_addr) {
				case 0:	if (d->timer0 == NULL)
						d->timer0 = timer_add(
						    d->hz[0], timer0_tick, d);
					else
						timer_update_frequency(
						    d->timer0, d->hz[0]);
					break;
				case 1:	fatal("TODO: DMA refresh?\n");
					break;	/*  #223: (Codex/Fable) warn+ignore, don't exit() the host  */
				case 2:	fatal("TODO: 8253 tone generation?\n");
					break;
				}
				break;
			default:fatal("[ 8253: huh? writing to counter"
				    " %i but neither from msb nor lsb? ]\n",
				    relative_addr);
				break;	/*  #223: (Codex/Fable) don't exit() the host  */
			}
		} else if (d->latched[relative_addr]) {
			/*  #439: Reading a counter that the latch
			    command latched.  gxemul models this timer's
			    RATE, not a count that decrements (see the
			    TODO at the top of this file), so there is no
			    captured count to hand back.  Return 0 to say
			    so, rather than returning the reload value,
			    which would look like a count that has not
			    started -- guests divide by (reload - this).  */
			odata = 0;

			/*
			 *  #440: CONSUME the latch.  i8254 p. 8: "the count
			 *  must be read according to the programmed format
			 *  specifically if the Counter is programmed for two
			 *  byte counts two bytes must be read"; p. 7: the
			 *  count "is held in the latch until it is read by
			 *  the CPU (or until the Counter is reprogrammed)
			 *  The count is then unlatched automatically".
			 *
			 *  So the last byte the format calls for releases it.
			 *  #439 cleared the flag only on a mode write, which
			 *  left one latch command making EVERY later read of
			 *  that counter return 0.  This byte counts against
			 *  the format, so the flip-flop below advances for it
			 *  too.
			 *
			 *  #440 pass 2, and the sentence this replaces was
			 *  MEASURED FALSE: it claimed "#439's measured
			 *  behaviour is unchanged".  Two toggles preserve the
			 *  starting phase, so a gettick() entered at EVEN read
			 *  parity is indeed a no-op -- but at ODD parity the
			 *  first read already has rw == MSB, consumes the
			 *  latch, and the second returns the live counter LSB:
			 *  0x9c00 where #439 gave 0x0000.  That is a change,
			 *  and it is the shape closer to the hardware (the
			 *  first read takes the byte the format calls for and
			 *  unlatches).  #439's reason for existing survives
			 *  either way -- the divisor is non-zero in both.
			 *
			 *  Left as a KNOWN OPEN QUESTION, not settled here: a
			 *  byte read BEFORE the latch command cannot be a byte
			 *  of the newly latched value, so consuming the latch
			 *  after one post-latch read arguably contradicts
			 *  p. 8's "two bytes must be read".  The local i8254
			 *  text does not say whether a latch command rewinds
			 *  the read flip-flop, and with no other 8253/8254
			 *  source in the tree this is an honest UNKNOWN rather
			 *  than a defect either way.  Tracked as `pitlatch2`.
			 */
			if ((d->mode_byte & 0x30) != I8253_TIMER_16BIT ||
			    rw == I8253_TIMER_MSB)
				d->latched[relative_addr] = 0;
		} else {
			switch (rw) {
			case I8253_TIMER_LSB:
				odata = d->counter[relative_addr] & 0xff;
				break;
			case I8253_TIMER_MSB:
				odata = (d->counter[relative_addr] >> 8) & 0xff;
				break;
			default:fatal("[ 8253: huh? reading from counter"
				    " %i but neither from msb nor lsb? ]\n",
				    relative_addr);
				break;	/*  #223: (Codex/Fable) don't exit() the host  */
			}
		}

		/*  #440: advance the flip-flop -- ALTERNATE, never latch.  This
		    used to be `d->mode_byte &= ~I8253_TIMER_LSB', a one-way
		    clear that also destroyed the programmed format.  */
		if ((d->mode_byte & 0x30) == I8253_TIMER_16BIT) {
			if (writeflag == MEM_WRITE)
				d->wr_msb[relative_addr] ^= 1;
			else
				d->rd_msb[relative_addr] ^= 1;
		}

		break;

	case I8253_TIMER_MODE:
		if (writeflag == MEM_WRITE) {
			d->counter_select = (idata >> 6) & 3;
			if (d->counter_select > 2) {
				debug("[ 8253: attempt to select counter 3,"
				    " which doesn't exist. ]\n");
				d->counter_select = 0;
			}

			/*  #439: The counter-latch command (RW == 00) latches a
			    counter so it can be read; it does NOT reprogram it, so
			    the RW format in mode_byte and the counting mode in
			    mode[] have to survive it.  Writing idata through here
			    unconditionally used to destroy both.  */
			if ((idata & 0x30) == I8253_TIMER_LATCH) {
				d->latched[d->counter_select] = 1;
				debug("[ 8253: latch counter %i ]\n",
				    d->counter_select);
				break;
			}

			d->mode_byte = idata;
			d->latched[d->counter_select] = 0;
			d->mode[d->counter_select] = idata & 0x0e;

			/*  #440: a Control Word programs "least significant
			    byte first then most significant byte" (i8254
			    Figure 7, RW1 RW0 = 1 1), so it rewinds this
			    counter's flip-flops.  Per counter, like the
			    hardware: Figure 8's sequences interleave control
			    words and count bytes across all three.  */
			d->rd_msb[d->counter_select] = 0;
			d->wr_msb[d->counter_select] = 0;

			debug("[ 8253: select=%i mode=0x%x ",
			    d->counter_select, d->mode[d->counter_select]);
			if (idata & 0x30) {
				switch (idata & 0x30) {
				case I8253_TIMER_LSB:
					debug("LSB ");
					break;
				case I8253_TIMER_16BIT:
					debug("LSB+");
					// fall through
				case I8253_TIMER_MSB:
					debug("MSB ");
				}
			}
			debug("]\n");

			if (idata & I8253_TIMER_BCD) {
				/*  #223: (Codex/Fable) warn+ignore BCD mode instead of
				    exit()ing the host.  */
				fatal("[ 8253: BCD not yet implemented ]\n");
			}
		} else {
			debug("[ 8253: read; can this actually happen? ]\n");
			odata = d->mode_byte;
		}
		break;

	default:if (writeflag == MEM_WRITE) {
			fatal("[ 8253: unimplemented write to address 0x%x"
			    " data=0x%02x ]\n", (int)relative_addr, (int)idata);
		} else {
			fatal("[ 8253: unimplemented read from address 0x%x "
			    "]\n", (int)relative_addr);
		}
		break;	/*  #223: (Codex/Fable) warn+ignore, don't exit() the host  */
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}


DEVINIT(8253)
{
	struct pit8253_data *d;

	CHECK_ALLOCATION(d = (struct pit8253_data *) malloc(sizeof(struct pit8253_data)));
	memset(d, 0, sizeof(struct pit8253_data));

	d->in_use = devinit->in_use;

	INTERRUPT_CONNECT(devinit->interrupt_path, d->irq);

	/*  Don't cause interrupt, by default.  */
	d->mode[0] = I8253_TIMER_RATEGEN;
	d->mode[1] = I8253_TIMER_RATEGEN;
	d->mode[2] = I8253_TIMER_RATEGEN;

	devinit->machine->isa_pic_data.pending_timer_interrupts =
	    &d->pending_interrupts_timer0;

	memory_device_register(devinit->machine->memory, devinit->name,
	    devinit->addr, DEV_8253_LENGTH, dev_8253_access, (void *)d,
	    DM_DEFAULT, NULL);

	machine_add_tickfunction(devinit->machine, dev_8253_tick,
	    d, TICK_SHIFT);

	return 1;
}

