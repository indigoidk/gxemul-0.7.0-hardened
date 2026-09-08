/*
 *  Copyright (C) 2007-2014  Anders Gavare.  All rights reserved.
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
 *  COMMENT: Peripheral Channel Controller (PCC2) bus (used in MVME machines)
 *
 *  See "Single Board Computers Programmer's Reference Guide (Part 2 of 2)",
 *  "VMESBCA2/PG1" (vmesbcp2.pdf) for more details.
 *
 *  Note: This is somewhat MVME187-specific, at the moment.
 *
 *  Implemented so far:
 *	Timers 1 and 2.
 *	The interrupt controller mechanism (partially!)
 *
 *  TODO:
 *	All devices appart from the timers.
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

#include "thirdparty/mvme187.h"
#include "thirdparty/mvme_pcctworeg.h"


#define	INTERRUPT_LEVEL_MASK	0x07

#define	PCC_TIMER_TICK_HZ	100.0
#define DEV_PCC2_TICK_SHIFT	14


// #define	debug fatal

/*  pcc2widthkills: TWELVE width-guard blocks in DEVICE_ACCESS(pcc2) -- TEN of them
    `fatal(); exit(1)' kills that ended the host on a guest-chosen access width, and
    two (IPL, MASK) #119 warn-once latches that declined it process-globally -- an ordinary aligned halfword load of a documented
    register.  Same class as #337 (dev_wdc.c) and #497 (dev_sgi_re.c).

    THE TREE ALREADY KNEW THE WIDTH IS LEGAL: mvme_pcctworeg.h says the PCCchip2
    registers "can be accessed as bytes (8 bits), two-bytes (16 bits), or four-bytes
    (32 bits)".  So this is not a fault to model; it is an access the model declines
    to IMPLEMENT on one side and already implements on the other:

      READS   are served BEFORE the switch by memcpy(data, pcctwo_reg + addr, len),
              raw bytes in address order -- width-correct by construction.  The old
              guard discarded a correct answer.  Now: ACCEPT (fall through).
      WRITES  ten of the twelve arms use `idata', the composed value (SCCERR stores a
              constant and IPL ignores it; both decline too -- a wide write's other
              lanes have no home), and `idata' is "the addressed
              byte" ONLY at len == 1: memory_readmax64 composes big-endian, so
              (uint8_t) idata is the HIGHEST-address lane.  Deleting the guard would
              store the neighbour's byte -- st.h 0xAABB to GENCTL would set GENCTL to
              0xBB, VECBASE's lane.  And eight arms mask, read-modify-write or clear
              on write, and seven of the twelve blocks call reassert_interrupts()
              (five of those eight; a seat measured the earlier "six" wrong).  Now: DECLINE +
              latched announce.  Per-lane composition through each arm (COMPOSE) is
              the faithful upgrade and is FILED as pcc2widecompose; not taken here
              because the hardware's lane semantics are not on disk and no driver
              MEASUREMENT exists either way: the only consumer is mvme187, no mvme187
              boot runs in this harness, and the one OS source in the tree (OpenBSD
              2.2) declares these registers `volatile u_char' and byte-accesses them
              -- a reading, not a measurement.

    ONE BIT PER BLOCK, twelve, per instance: a driver bringing up the chip touches
    several of these in one pass, and one latch would announce the first and silence
    the rest (#497's own reasoning).  Auto-incremented rather than `1 << N' literals,
    which this fork records as collision-prone; PCC2_W_NBITS names the count, and the
    typedef after the enum makes the build fail if it ever exceeds the 32-bit field.

    REACHABILITY, verified: every non-byte m88k access is alignment-checked BEFORE
    memory_rw, and `relative_addr %= PCC2_SIZE' keeps parity, so only the SIX
    EVEN-offset blocks (GENCTL, TxCTL, TxICR, SCCERR, SCCTX, IPL) are GUEST-reachable
    (this said "five" until pass 2; IPL at 0x3e is even, and a seat counted); the
    eight odd OFFSETS -- the six odd-only blocks VECBASE, PSCALEADJ, SCCICR, SCCRX,
    SCSIICR, MASK, plus the T1CTL/T1ICR labels of the shared TxCTL/TxICR blocks --
    are OPERATOR-reachable -- the debugger's `put h' warns on a
    misaligned address and stores anyway, MEASURED (artifacts/pcc2widthkills/
    operator_reach_20260903.out: `put h 0xfff42003' ended the host).  All twelve are
    converted; the detector reaches the odd ones through that path.

    NOT FIXED HERE, cited so "twelve kills removed" is not read as "file clean":
    pcc2c040kill (a LEGAL byte write of 0x04 to GENCTL still ends the host in
    reassert_interrupts).  pcc2defaultkill -- an unlisted offset ended it -- was
    fixed by #501 (the default: arm below); this sentence said "still ends it"
    until #501's pass 4 (Opus).  */
enum {
	PCC2_W_GENCTL_LEN,
	PCC2_W_VECBASE_LEN,
	PCC2_W_PSCALEADJ_LEN,
	PCC2_W_TXCTL_LEN,	/*  one block serves T1CTL and T2CTL  */
	PCC2_W_TXICR_LEN,	/*  one block serves T1ICR and T2ICR  */
	PCC2_W_SCCERR_LEN,
	PCC2_W_SCCICR_LEN,
	PCC2_W_SCCTX_LEN,
	PCC2_W_SCCRX_LEN,
	PCC2_W_SCSIICR_LEN,
	PCC2_W_IPL_LEN,		/*  was a #119 function-static: process-global  */
	PCC2_W_MASK_LEN,	/*  was a #119 function-static: process-global  */
	PCC2_W_C040,		/*  #512: not a _LEN -- the C040 delivery decline  */
	PCC2_W_NBITS
};

struct pcc2_data {
	struct interrupt	cpu_irq;

	uint8_t			pcctwo_reg[PCC2_SIZE];

	/*  pcc2widthkills: one bit per width-guard block, see the enum.  Zeroed by
	    the init memset, so every instance starts with every announce armed.  */
	uint32_t		warned;
	/*  #501: one bit per BYTE OFFSET (0..0x3f) for the default: arm's announce;
	    relative_addr is folded to PCC2_SIZE above the switch, so the shift is
	    always defined.  Zeroed by the same memset.  */
	uint64_t		warned_unimpl;

	uint8_t			cur_int_vec[8];

	/*  Timers:  */
	struct timer		*timer;
	int			pending_timer1_interrupts;
	int			pending_timer2_interrupts;
};
/*  pcc2widthkills: the enum must fit the field.  A seat pointed out that a bare
    `<= 32' tested a literal, not the field, so narrowing `warned' would compile
    silently; this is dev_dreamcast_gdrom.c's own form.  Negative array size is a
    compile-time error, C99, no assert.h.  */
typedef char pcc2_w_fits_in_warned[(PCC2_W_NBITS <= 8 * sizeof(((struct pcc2_data *)0)->warned)
    && PCC2_W_NBITS <= 8 * sizeof(1u)) ? 1 : -1];


static uint32_t read32(unsigned char *p)
{
	uint32_t x = 0;
	size_t i;

	for (i=0; i<sizeof(x); i++) {
		x <<= 8;
		x |= p[i];
	}

	return x;
}


static void write32(unsigned char *p, uint32_t x)
{
	size_t i;

	for (i=0; i<sizeof(x); i++) {
		p[sizeof(x) - 1 - i] = x;
		x >>= 8;
	}
}


static void pcc_timer_tick(struct timer *t, void *extra)
{
	struct pcc2_data *d = (struct pcc2_data *) extra;

	/*  The PCC2 timers run at 1 MHz.  */
	int steps = (int) (1000000.0 / PCC_TIMER_TICK_HZ);

	uint32_t count1, count2, compare1, compare2;
	int interrupt1 = 0, interrupt2 = 0;

	/*  Read values:  */
	count1 = read32(&d->pcctwo_reg[PCCTWO_T1COUNT]);
	count2 = read32(&d->pcctwo_reg[PCCTWO_T2COUNT]);
	compare1 = read32(&d->pcctwo_reg[PCCTWO_T1CMP]);
	compare2 = read32(&d->pcctwo_reg[PCCTWO_T2CMP]);

	/*  Timer enabled? Then count...  */
	if (d->pcctwo_reg[PCCTWO_T1CTL] & PCC2_TCTL_CEN) {
		uint32_t old_count1 = count1;
		count1 += steps;

		/*  Did we pass the compare value?  */
		if ((old_count1 < compare1 && count1 >= compare1) ||
		    (old_count1 < compare1 && count1 < old_count1)) {
			interrupt1 = 1;

			if (d->pcctwo_reg[PCCTWO_T1CTL] & PCC2_TCTL_COC) {
				while (count1 >= compare1) {
					count1 -= compare1;
					interrupt1 ++;
				}
				interrupt1 --;
			}
		}

		/*  Overflow?  */
		if ((int32_t) old_count1 >= 0 && (int32_t) count1 < 0) {
			int oc = 1 + (d->pcctwo_reg[PCCTWO_T1CTL] >> 4);
			d->pcctwo_reg[PCCTWO_T1CTL] &= ~PCC2_TCTL_OVF;
			d->pcctwo_reg[PCCTWO_T1CTL] |= (oc << 4);
		}
	}

	/*  ... and the same for timer 2:  */
	if (d->pcctwo_reg[PCCTWO_T2CTL] & PCC2_TCTL_CEN) {
		uint32_t old_count2 = count2;
		count2 += steps;

		if ((old_count2 < compare2 && count2 >= compare2) ||
		    (old_count2 < compare2 && count2 < old_count2)) {
			interrupt2 = 1;
			if (d->pcctwo_reg[PCCTWO_T2CTL] & PCC2_TCTL_COC) {
				while (count2 >= compare2) {
					count2 -= compare2;
					interrupt2 ++;
				}
				interrupt2 --;
			}
		}

		if ((int32_t) old_count2 >= 0 && (int32_t) count2 < 0) {
			int oc = 1 + (d->pcctwo_reg[PCCTWO_T2CTL] >> 4);
			d->pcctwo_reg[PCCTWO_T2CTL] &= ~PCC2_TCTL_OVF;
			d->pcctwo_reg[PCCTWO_T2CTL] |= (oc << 4);
		}
	}

	/*  Should we cause interrupts?  */
	if (interrupt1 && d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_IEN)
		d->pending_timer1_interrupts += interrupt1;
	if (interrupt2 && d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_IEN)
		d->pending_timer2_interrupts += interrupt2;

	/*  Write back values:  */
	write32(&d->pcctwo_reg[PCCTWO_T1COUNT], count1);
	write32(&d->pcctwo_reg[PCCTWO_T2COUNT], count2);
}


static void reassert_interrupts(struct pcc2_data *d)
{
	int assert = 0;

	/*  #512: the C040 test used to sit HERE and was a fatal()+exit(1), so one
	    legal guest byte write of 0x04 to GENCTL ended the host.  It now lives
	    beside the MIEN test at the foot of this function, where declining to
	    assert does not skip the recalculation below.  */

	/*
	 *  Recalculate current interrupt level:
	 */
	d->pcctwo_reg[PCCTWO_IPL] = 0;

	/*  Timer interrupts?  */
	if (d->pending_timer1_interrupts > 0 &&
	    d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_IEN)
		d->pcctwo_reg[PCCTWO_T1ICR] |= PCC2_TTIRQ_INT;
	if (d->pending_timer2_interrupts > 0 &&
	    d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_IEN)
		d->pcctwo_reg[PCCTWO_T2ICR] |= PCC2_TTIRQ_INT;

	if (d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_IL;
		d->cur_int_vec[intlevel] = PCC2V_TIMER1;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}
	if (d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_IL;
		d->cur_int_vec[intlevel] = PCC2V_TIMER2;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	if (d->pcctwo_reg[PCCTWO_SCCTX] & PCC2_IRQ_IEN &&
	    d->pcctwo_reg[PCCTWO_SCCTX] & PCC2_IRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_SCCTX] & PCC2_IRQ_IPL;
		d->cur_int_vec[intlevel] = PCC2V_SCC_TX;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	if (d->pcctwo_reg[PCCTWO_SCCRX] & PCC2_IRQ_IEN &&
	    d->pcctwo_reg[PCCTWO_SCCRX] & PCC2_IRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_SCCRX] & PCC2_IRQ_IPL;
		d->cur_int_vec[intlevel] = PCC2V_SCC_RX;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	if (d->pcctwo_reg[PCCTWO_SCSIICR] & PCC2_IRQ_IEN &&
	    d->pcctwo_reg[PCCTWO_SCSIICR] & PCC2_IRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_SCSIICR] & PCC2_IRQ_IPL;
		d->cur_int_vec[intlevel] = PCC2V_SCSI;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	/*  TODO: Other interrupt sources.  */

	/*  Assert interrupt on the CPU if the IPL is higher than the mask:  */
	if ((d->pcctwo_reg[PCCTWO_IPL] & INTERRUPT_LEVEL_MASK) >
	    (d->pcctwo_reg[PCCTWO_MASK] & INTERRUPT_LEVEL_MASK))
		assert = 1;

	debug("[ pcc2: IPL = %i, MASK = %i => %s ]\n", d->pcctwo_reg[PCCTWO_IPL]& INTERRUPT_LEVEL_MASK,
		d->pcctwo_reg[PCCTWO_MASK] & INTERRUPT_LEVEL_MASK,
		assert ? "ASSERT" : "no assert");

	/*  ... but only allow interrupts if Master Interrupt Enable is on:  */
	if (!(d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_MIEN))
		assert = 0;

	/*  #512: ... and not while C040 selects a delivery pin this model does not
	    have.  This was a fatal()+exit(1) at the TOP of this function, and
	    reassert_interrupts() is called from ten sites -- the GENCTL write arm
	    calls it in the SAME access -- so ONE legal guest `st.b' of 0x04 to
	    GENCTL ended the host, with no driver and no interrupt involved
	    (witness: regress/pcc2_c040_probe.py).

	    DECLINING TO ASSERT, rather than returning, is what the MIEN test above
	    already does for the other GENCTL interrupt-control bit.  A `return' AT
	    THIS SITE would skip only the INTERRUPT_DEASSERT below -- the IPL
	    recalculation and the cur_int_vec[] updates have already run by here.
	    (It is a return at the OLD site, above the recalculation, that would skip
	    all three; an earlier draft of this comment attached that reason to this
	    placement, which is a wrong reason for a right position, and a wrong
	    reason gets reused -- `assert = 0' -> `return' at THIS line is a
	    one-token mutant every shipped row passes.)

	    VMESBCP2 (the MVME187 board manual) settles the shape in two places.
	    The General Control Register page ($FFF42002) puts C040 at bit 10 of the
	    word view -- 0x04, matching this fork's header -- and says a set C040
	    sends the request "via the EIPL* pins at the level that is programmed
	    ... in the SCSI Interrupt Control Register"; the Interrupt Priority
	    Level Register page adds that IPL2-IPL0 "always reflect the encoded
	    request level".  So C040 selects the DELIVERY PIN and not the level,
	    which is why the recalculation above must stay.  MIEN, by contrast,
	    disables "both the EIPL* pins and the INT pin" -- so the two tests are
	    siblings gating one output, not a nest.  */
	if (d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_C040) {
		if (!(d->warned & (1u << PCC2_W_C040))) {
			d->warned |= (1u << PCC2_W_C040);
			fatal("[ pcc2: C040 (MC68040 EIPL) interrupt delivery not "
			    "implemented; assertion suppressed  (once) ]\n");
		}
		assert = 0;
	}

	if (assert)
		INTERRUPT_ASSERT(d->cpu_irq);
	else
		INTERRUPT_DEASSERT(d->cpu_irq);
}


void pcctwo_interrupt_common(struct interrupt *interrupt, int assert)
{
	struct pcc2_data *d = (struct pcc2_data *) interrupt->extra;

	switch (interrupt->line) {

	case PCC2V_SCSI:
		if (assert)
			d->pcctwo_reg[PCCTWO_SCSIICR] |= PCC2_IRQ_INT;
		else
			d->pcctwo_reg[PCCTWO_SCSIICR] &= ~PCC2_IRQ_INT;
		break;

	case PCC2V_SCC_TX:
		if (assert)
			d->pcctwo_reg[PCCTWO_SCCTX] |= PCC2_IRQ_INT;
		else
			d->pcctwo_reg[PCCTWO_SCCTX] &= ~PCC2_IRQ_INT;
		break;

	case PCC2V_SCC_RX:
		if (assert)
			d->pcctwo_reg[PCCTWO_SCCRX] |= PCC2_IRQ_INT;
		else
			d->pcctwo_reg[PCCTWO_SCCRX] &= ~PCC2_IRQ_INT;
		break;

	default:fatal("[ pcctwo_interrupt_common: TODO: line = %i ]\n",
		    interrupt->line);
		exit(1);
	}

	reassert_interrupts(d);
}


static void pcctwo_interrupt_assert(struct interrupt *interrupt)
{
	pcctwo_interrupt_common(interrupt, 1);
}
static void pcctwo_interrupt_deassert(struct interrupt *interrupt)
{
	pcctwo_interrupt_common(interrupt, 0);
}


DEVICE_TICK(pcc2)
{
	struct pcc2_data *d = (struct pcc2_data *) extra;
	reassert_interrupts(d);
}


/*  pcc2widthkills: decline a wide WRITE to a byte register, announcing once per
    block per instance.  The caller `break's after this; the read side of the same
    block never reaches here.  */
static void pcc2_width_decline(struct pcc2_data *d, int bit, const char *name, int len)
{
	if (!(d->warned & (1u << bit))) {
		d->warned |= (1u << bit);
		fatal("[ pcc2: unimplemented len=%i write to %s -- declined."
		    "  (once) ]\n", len, name);
	}
}

DEVICE_ACCESS(pcc2)
{
	uint64_t idata = 0;
	struct pcc2_data *d = (struct pcc2_data *) extra;

	/*  0xfff42000..0xfff42fff, but only 0x40 unique registers:  */
	relative_addr %= PCC2_SIZE;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	if (writeflag == MEM_READ) {
		if (relative_addr + len <= PCC2_SIZE)	/* OB-11: end-span */
			memcpy(data, d->pcctwo_reg + relative_addr, len);
		else {
			static int warned = 0;	/* #119: loud-once (course-correction) */
			if (!warned) {
				fatal("[ pcc2: read 0x%x+%i beyond reg space 0x%x; "
				    "zero-filled ]\n", (int)relative_addr, (int)len,
				    (int)PCC2_SIZE);
				warned = 1;
			}
			memset(data, 0, len);	/* OB-11b: don't leak uninit host memory */
		}
	}

	switch (relative_addr) {

	case PCCTWO_CHIPID:
	case PCCTWO_CHIPREV:
		if (writeflag == MEM_WRITE) {
			fatal("[ IGNORING write to read-only PCCTWO_CHIPID/"
			    "CHIPREV register ]\n");
		}
		break;

	case PCCTWO_GENCTL:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_GENCTL_LEN, "PCCTWO_GENCTL", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata;
			reassert_interrupts(d);
		}
		break;

	case PCCTWO_VECBASE:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata & 0xf0;
			if (idata & ~0xf0)
				fatal("[ pcc2: HUH? write to PCCTWO_VECBASE"
				    " with value 0x%02x. ]\n", (int) idata);
		}
		break;

	case PCCTWO_T1CMP:
	case PCCTWO_T2CMP:
	case PCCTWO_T1COUNT:
	case PCCTWO_T2COUNT:
		if (writeflag == MEM_WRITE &&
		    relative_addr + len <= PCC2_SIZE)	/* OB-11: end-span */
			memcpy(d->pcctwo_reg + relative_addr, data, len);
		break;

	case PCCTWO_PSCALEADJ:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_PSCALEADJ_LEN, "PCCTWO_PSCALEADJ", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			fatal("[ pcc2: write to PSCALEADJ ignored (value "
			    "0x%02x) ]\n", (int)idata);
		}
		break;

	case PCCTWO_T2CTL:
	case PCCTWO_T1CTL:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_TXCTL_LEN, "PCCTWO_TxCTL", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			/*  PCC2_TCTL_CEN and PCC2_TCTL_COC:  */
			d->pcctwo_reg[relative_addr] &= 0xfc;
			d->pcctwo_reg[relative_addr] |= (idata & 3);

			if (idata & PCC2_TCTL_COVF)
				d->pcctwo_reg[relative_addr] &=
				    ~(PCC2_TCTL_OVF | PCC2_TCTL_COVF);

			if (idata & ~7)
				fatal("[ pcc2: HUH? write to PCCTWO_TxCTL"
				    " with value 0x%02x. ]\n", (int) idata);
		}
		break;

	case PCCTWO_T2ICR:
	case PCCTWO_T1ICR:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_TXICR_LEN, "PCCTWO_TxICR", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] &= ~0x17;
			d->pcctwo_reg[relative_addr] |= (idata & 0x17);

			if (relative_addr == PCCTWO_T1ICR &&
			    !(idata & PCC2_TTIRQ_IEN))
				d->pending_timer1_interrupts = 0;
			if (relative_addr == PCCTWO_T2ICR &&
			    !(idata & PCC2_TTIRQ_IEN))
				d->pending_timer2_interrupts = 0;

			if (relative_addr == PCCTWO_T1ICR && (idata & PCC2_TTIRQ_ICLR)
			    && d->pcctwo_reg[relative_addr] & PCC2_TTIRQ_INT
			    && d->pending_timer1_interrupts > 0)
				d->pending_timer1_interrupts --;

			if (relative_addr == PCCTWO_T2ICR && (idata & PCC2_TTIRQ_ICLR)
			    && d->pcctwo_reg[relative_addr] & PCC2_TTIRQ_INT
			    && d->pending_timer2_interrupts > 0)
				d->pending_timer2_interrupts --;

			if (idata & PCC2_TTIRQ_ICLR)
				d->pcctwo_reg[relative_addr] &= ~PCC2_TTIRQ_INT;

			if (idata & 0xe0)
				fatal("[ pcc2: HUH? write to PCCTWO_TxICR"
				    " with value 0x%02x. ]\n", (int) idata);

			reassert_interrupts(d);
		}
		break;

	case PCCTWO_SCCERR:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_SCCERR_LEN, "PCCTWO_SCCERR", len);
			break;
		}
		if (writeflag == MEM_WRITE)
			d->pcctwo_reg[relative_addr] = 0;	/*  clear  */
		break;

	case PCCTWO_SCCICR:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_SCCICR_LEN, "PCCTWO_SCCICR", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata & 0x1f;
			if (idata & ~0x1f)
				fatal("[ pcc2: HUH? write to PCCTWO_SCCICR"
				    " with value 0x%02x. ]\n", (int) idata);
			reassert_interrupts(d);
		}
		break;

	case PCCTWO_SCCTX:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_SCCTX_LEN, "PCCTWO_SCCTX", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata & 0x1f;
			if (idata & ~0x1f)
				fatal("[ pcc2: HUH? write to PCCTWO_SCCTX"
				    " with value 0x%02x. ]\n", (int) idata);
			reassert_interrupts(d);
		}
		break;

	case PCCTWO_SCCRX:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_SCCRX_LEN, "PCCTWO_SCCRX", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata & 0xdf;
			if (idata & ~0xdf)
				fatal("[ pcc2: HUH? write to PCCTWO_SCCRX"
				    " with value 0x%02x. ]\n", (int) idata);
			reassert_interrupts(d);
		}
		break;

	case PCCTWO_SCCRXIACK:
		/*  TODO. Hm. Is this enough?  */
		d->pcctwo_reg[PCCTWO_SCCRX] &= ~PCC2_IRQ_INT;
		reassert_interrupts(d);
		break;

	case PCCTWO_SCSIICR:
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_SCSIICR_LEN, "PCCTWO_SCSIICR", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata & 0xdf;
			if (idata & ~0xdf)
				fatal("[ pcc2: HUH? write to PCCTWO_SCSIICR"
				    " with value 0x%02x. ]\n", (int) idata);
			reassert_interrupts(d);
		}
		break;

	case PCCTWO_IPL:
		/*  pcc2widthkills: was a #119 `static int w' -- process-global, and it
		    said "ignored" about a READ the memcpy above had already served.
		    Now per-instance, write-only, like the ten blocks above -- that is
		    the WIDTH latch; the body's own #119 `static int w' below stays
		    process-global (pcc2pscaleflood's family; not this round's).  */
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			static int w = 0;	/* #119: was exit(1) (IPL is read-only) */
			if (!w) { fatal("[ pcc2: write to read-only PCCTWO_IPL; "
			    "ignored ]\n"); w = 1; }
		} else {
			if (d->pcctwo_reg[PCCTWO_IPL] == 0) {
				static int w = 0;	/* #119: was exit(1) */
				if (!w) { fatal("[ pcc2: IPL == 0 on read ]\n");
				    w = 1; }
			}
		}
		break;

	case PCCTWO_MASK:
		/*  pcc2widthkills: was a #119 `static int w' -- process-global, and it
		    said "ignored" about a READ the memcpy above had already served.
		    Now per-instance, write-only, like the ten blocks above -- that is
		    the WIDTH latch.  (pcc2widthkills pass 7: this comment once claimed a
		    #119 static of MASK's own "below" -- there is none; the body stores
		    the byte and reasserts.  The static belongs to IPL's arm above.)  */
		if (len != 1 && writeflag == MEM_WRITE) {
			pcc2_width_decline(d, PCC2_W_MASK_LEN, "PCCTWO_MASK", len);
			break;
		}
		if (writeflag == MEM_WRITE) {
			d->pcctwo_reg[relative_addr] = idata;
			reassert_interrupts(d);
		}
		break;

	default:
		/*  #501 (pcc2defaultkill): this arm ended the host with exit(1) on ANY
		    access to an offset with no case -- 43 of the 0x40 byte offsets:
		    eighteen documented registers the model does not implement (IEICR,
		    IEERR, IEBERR, GPIO, SCSIERR, the printer block, SPEED, the *IACKs),
		    the bytes inside the four counter/compare words, and the unnamed
		    ones -- READS included, though the memcpy above the switch had
		    already served them.  A guest ld.bu or st.b at any of them was a host
		    kill (rung-3 witness).  Now: a READ keeps the served byte (the array's
		    current byte, said so -- inside a running COUNT word that is the
		    tick's value, not a default); a WRITE is DECLINED.  Not a
		    backed store: the cased siblings contradict one (SCCERR clears on
		    write, the ICRs mask and reassert, PSCALECNT/SPEED/the IACKs are
		    read-only), no inspected OpenBSD driver path reaches them (if_ie never
		    attaches: unreadable sits at its 82596 address), and a store from the
		    one arm 43 offsets reach would add a bounded-write surface.  One
		    latched fatal() per offset per instance, the house `(once)' shape --
		    unlike PSCALEADJ's UNLATCHED print above (pcc2pscaleflood).  The
		    IACK offsets 0x23/0x25 are declined like the rest: modelling them (on
		    the SCCRXIACK shape) would open two new entries into the C040 path,
		    so pcc2c040kill goes first.  The %= fold above IS the real part's:
		    Motorola VMESBCP2 Table 6-1 lists $FFF42040-$FFF42FFF as repeated
		    PCCchip2 registers.  */
		if (!(d->warned_unimpl & (1ULL << relative_addr))) {
			d->warned_unimpl |= 1ULL << relative_addr;
			if (writeflag == MEM_WRITE)
				fatal("[ pcc2: unimplemented write to offset "
				    "0x%x (len %d): 0x%x -- declined.  (once) ]\n",
				    (int) relative_addr, (int) len, (int) idata);
			else
				/*  data[0] is the byte actually SERVED; a reload of the
				    array could differ: on the end-span path (zero-filled,
				    the array byte kept) and inside a running COUNT word,
				    whose SIGALRM-driven tick (timer.c) can land between
				    the copy and this line.  A wide read is labelled.  */
				fatal("[ pcc2: unimplemented read from offset "
				    "0x%x (len %d) -- served 0x%02x.  (once) ]\n",
				    (int) relative_addr, (int) len, data[0]);
		}
		break;
	}

	return 1;
}


DEVICE_ACCESS(mvme187_iack)
{
	uint64_t odata = 0;
	struct pcc2_data *d = (struct pcc2_data *) extra;

	if (writeflag == MEM_WRITE) {
		fatal("[ pcc2: write to mvme187_iack? ]\n");
	} else {
		odata = d->pcctwo_reg[PCCTWO_VECBASE] + d->cur_int_vec[
		    (relative_addr >> 2) & INTERRUPT_LEVEL_MASK];
		debug("[ pcc2: mvme187_iack level %i => vector 0x%02x ]\n",
		    (int)(relative_addr >> 2), (int)odata);

		memory_writemax64(cpu, data, len, odata);
	}

	return 1;
}


DEVINIT(pcc2)
{
	struct pcc2_data *d;
	int i;

	CHECK_ALLOCATION(d = (struct pcc2_data *) malloc(sizeof(struct pcc2_data)));
	memset(d, 0, sizeof(struct pcc2_data));

	/*
	 *  Initial values, according to the manual:
	 *
	 *  VECBASE is 0x0f after a reset, although the lowest four bits
	 *  cannot be manually written to after startup.
	 */
	d->pcctwo_reg[PCCTWO_CHIPID] = PCC2_ID;
	d->pcctwo_reg[PCCTWO_CHIPREV] = 0x00;
	d->pcctwo_reg[PCCTWO_GENCTL] = 0x00;
	d->pcctwo_reg[PCCTWO_VECBASE] = 0x0f;
	d->pcctwo_reg[PCCTWO_PSCALEADJ] = 256 - 33;	// 256 - MHz (fake)

	/*  Connect to the CPU's interrupt pin:  */
	INTERRUPT_CONNECT(devinit->interrupt_path, d->cpu_irq);

	/*
	 *  Register the 16 PCC2 interrupt vectors:
	 */
	for (i=0; i<16; i++) {
		struct interrupt templ;
		char n[300];
		snprintf(n, sizeof(n), "%s.pcc2.%i",
		    devinit->interrupt_path, i);

		memset(&templ, 0, sizeof(templ));
		templ.line = i;
		templ.name = n;
		templ.extra = d;
		templ.interrupt_assert = pcctwo_interrupt_assert;
		templ.interrupt_deassert = pcctwo_interrupt_deassert;

		interrupt_handler_register(&templ);
	}

	memory_device_register(devinit->machine->memory, "pcc2",
	    devinit->addr, 4096, dev_pcc2_access, (void *)d,
	    DM_DEFAULT, NULL);

	memory_device_register(devinit->machine->memory, "mvme187_iack",
	    M187_IACK, 32, dev_mvme187_iack_access, (void *)d,
	    DM_DEFAULT, NULL);

	d->timer = timer_add(PCC_TIMER_TICK_HZ, pcc_timer_tick, d);

	machine_add_tickfunction(devinit->machine,
	    dev_pcc2_tick, d, DEV_PCC2_TICK_SHIFT);

	return 1;
}

