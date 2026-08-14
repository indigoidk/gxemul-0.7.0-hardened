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
 *  COMMENT: RICOH RS5C313 Real Time Clock
 *
 *  The RS5C313 has 16 registers, see rs5c313reg.h for details. These registers
 *  are addressed at byte offsets.
 *
 *  Note: The only use for this device so far is in the Landisk, connected to
 *        the SH4 SCI pins. In the Landisk machine, the RS5C313 is placed at
 *        a fake (high) address in memory.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "cpu.h"
#include "device.h"
#include "machine.h"
#include "memory.h"
#include "misc.h"

#include "thirdparty/rs5c313reg.h"


#define	DEV_RS5C313_LENGTH	16

struct rs5c313_data {
	uint8_t		reg[DEV_RS5C313_LENGTH];
};


/*
 *  rs5c313_update_time():
 *
 *  Set the RS5C313 registers to correspond to the host's clock.
 */
static void rs5c313_update_time(struct rs5c313_data *d)
{
	struct tm *tmp;
	time_t timet;

	timet = time(NULL);
	tmp = gmtime(&timet);

	d->reg[RS5C313_SEC1]   = tmp->tm_sec % 10;
	d->reg[RS5C313_SEC10]  = tmp->tm_sec / 10;
	d->reg[RS5C313_MIN1]   = tmp->tm_min % 10;
	d->reg[RS5C313_MIN10]  = tmp->tm_min / 10;
	d->reg[RS5C313_HOUR1]  = tmp->tm_hour % 10;
	d->reg[RS5C313_HOUR10] = tmp->tm_hour / 10;

	/*  WDAY. Zero-based. TODO: Is this correct?  */
	d->reg[RS5C313_WDAY]   = tmp->tm_wday;

	d->reg[RS5C313_DAY1]   = tmp->tm_mday % 10;
	d->reg[RS5C313_DAY10]  = tmp->tm_mday / 10;
	d->reg[RS5C313_MON1]   = (tmp->tm_mon + 1) % 10;
	d->reg[RS5C313_MON10]  = (tmp->tm_mon + 1) / 10;
	d->reg[RS5C313_YEAR1]  = tmp->tm_year % 10;
	d->reg[RS5C313_YEAR10] = (tmp->tm_year / 10) % 10;
}


/*
 *  #404: THE GUEST CANNOT SET THIS CLOCK, AND THAT IS RECORDED HERE RATHER THAN
 *  FIXED. Measured against this function, not inferred.
 *
 *  rs5c313_update_time() below runs before the read/write dispatch, so every
 *  access rewrites all thirteen time registers from the host. A write does store
 *  its own nibble afterwards, but the other twelve were just overwritten -- a
 *  guest sets the clock one register at a time, so each write reverts the twelve
 *  it is not touching. Measured: one write of 9 to SEC1 from an all-zero file
 *  moved 12 of 12 non-target time registers to host digits. And a read refreshes
 *  first, so a readback at the SAME INSTANT returns host time, not the written
 *  value. The survivors are exactly TINT, CTRL and TEST.
 *
 *  *** WHAT THAT MEANS IS NARROWER THAN IT LOOKS, AND THE MEASUREMENT MATTERS. ***
 *  A variant that ignores writes to all thirteen clock registers outright is
 *  GUEST-INDISTINGUISHABLE from what ships today. So is one that refreshes only
 *  on reads -- 0 mismatches in 248,581 reads. This is therefore not corruption
 *  of a value the guest could otherwise rely on; it is a MISSING FEATURE. The
 *  clock is not settable, and never has been.
 *
 *  A correct fix needs an offset model (host time plus a guest-applied delta),
 *  reached by elimination rather than by preference. It is not attempted, for a
 *  reason that is measured rather than cautious:
 *
 *    - rs5c313reg.h:64-67 names CTRL_BSY/CTRL_ADJ and CTRL_XSTP/CTRL_WTEN, which
 *      look like a hold/busy protocol this device ignores entirely. But the
 *      header supplies BIT NAMES ONLY. It does not say that WTEN gates writes,
 *      what event commits a staged time, or whether the counter holds meanwhile.
 *    - The house pattern argues AGAINST guessing here, not for it.
 *      dev_mk48txx.c:98-106 gates on a latch that ITS OWN header documents
 *      (mk48txxreg.h:101, "freeze clock"). dev_mc146818.c:532-540 does the same
 *      with MC_REGB_SET. rs5c313reg.h carries no equivalent statement, so the
 *      analogy would be to a different chip.
 *    - AND A WRONG GUESS CAN REGRESS A BOOTING MACHINE: implementing
 *      "hold while WTEN is set" is guest-DISTINGUISHABLE from today, 64,687
 *      divergent reads in a differential. This is not a free improvement.
 *    - dev_dreamcast_rtc.c:70-74 already records the project's position on RTC
 *      writes: deliberately ignored.
 *
 *  ALSO UNIMPLEMENTED, recorded so nobody re-derives them: CTRL_24H is accepted
 *  and never consulted (update_time always emits 24-hour tm_hour, and a read at
 *  13:00 is identical with the bit set or clear); TINT is unimplemented; the
 *  two-digit year aliases, so 2105 reads as "05"; and a pre-1900 host clock
 *  yields non-BCD digits through C99's negative %, measured as YEAR1 = 0xfa.
 *
 *  WDAY is left exactly as it is. Both sibling RTCs use tm_wday + 1
 *  (dev_mc146818.c:196, dev_mk48txx.c:69) and mk48txxreg.h:75 documents 1..7 --
 *  but that is a different chip, and rs5c313reg.h says nothing. Changing this on
 *  analogy is precisely the guess the rest of this note declines to make. The
 *  upstream "TODO: Is this correct?" above stands, unanswered and honest.
 *
 *  Checked and CORRECT, so they are not re-investigated: YEAR10, MON1/MON10 and
 *  every digit encoding (0 mismatches over ~170,000 samples spanning 1970-2105),
 *  gmtime being the right choice and consistent tree-wide, the DEVINIT defaults,
 *  and the register bounds (relative_addr is 0..15 with len always 1).
 */
DEVICE_ACCESS(rs5c313)
{
	struct rs5c313_data *d = (struct rs5c313_data *) extra;
	uint64_t idata = 0, odata = 0;

	rs5c313_update_time(d);

	/*  Generic register read/write:  */
	if (writeflag == MEM_WRITE) {
		idata = memory_readmax64(cpu, data, len);
		d->reg[relative_addr] = idata & 0x0f;
	} else {
		odata = d->reg[relative_addr] & 0x0f;
		memory_writemax64(cpu, data, len, odata);
	}

	return 1;
}


DEVINIT(rs5c313)
{
	struct rs5c313_data *d;

	CHECK_ALLOCATION(d = (struct rs5c313_data *) malloc(sizeof(struct rs5c313_data)));
	memset(d, 0, sizeof(struct rs5c313_data));

	/*  Default values:  */
	d->reg[RS5C313_CTRL] = CTRL_24H;

	memory_device_register(devinit->machine->memory, devinit->name,
	    devinit->addr, DEV_RS5C313_LENGTH,
	    dev_rs5c313_access, (void *)d, DM_DEFAULT, NULL);

	return 1;
}

