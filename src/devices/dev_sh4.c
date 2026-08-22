/*
 *  Copyright (C) 2006-2020  Anders Gavare.  All rights reserved.
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
 *  COMMENT: SH4-specific memory mapped registers (0xf0000000 - 0xffffffff)
 *
 *  TODO: Among other things:
 *
 *	x)  Interrupt masks (msk register stuff). Are these really correct?
 *	x)  BSC (Bus state controller).
 *	x)  DMA: Right now there's a hack for Dreamcast emulation
 *	x)  UBC (User Break Controller)
 *	x)  ...
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "bus_pci.h"
#include "console.h"
#include "cpu.h"
#include "device.h"
#include "devices.h"
#include "interrupt.h"
#include "machine.h"
#include "memory.h"
#include "misc.h"
#include "sh4_dmacreg.h"
#include "timer.h"

#include "thirdparty/sh4_bscreg.h"
#include "thirdparty/sh4_cache.h"
#include "thirdparty/sh4_exception.h"
#include "thirdparty/sh4_intcreg.h"
#include "thirdparty/sh4_mmu.h"
#include "thirdparty/sh4_pcicreg.h"
#include "thirdparty/sh4_rtcreg.h"
#include "thirdparty/sh4_scifreg.h"
#include "thirdparty/sh4_scireg.h"
#include "thirdparty/sh4_tmureg.h"


#define	SH4_REG_BASE		0xff000000
#define	SH4_TICK_SHIFT		14
#define	N_SH4_TIMERS		3

/*  PCI stuff:  */
#define	N_PCIC_REGS			(0x224 / sizeof(uint32_t))
#define	N_PCIC_IRQS			16
#define	PCIC_REG(addr)			((addr - SH4_PCIC) / sizeof(uint32_t))

/*
 *  #443 pass 2: the latch's FAULT CLASSES.  One offset can produce two genuinely
 *  different complaints -- an unimplemented-offset access and a known register
 *  rejecting a value -- and a single flag per offset reports whichever came first
 *  and silently swallows the other.
 */
#define	SH4_PCIC_UNIMPL			0	/*  offset this device does not implement  */
#define	SH4_PCIC_BADVAL			1	/*  known register, unexpected value      */
#define	SH4_PCIC_NOCPU			2	/*  known register, CPU type not modelled */
#define	SH4_PCIC_NCLASS			3
/*
 *  #447: DEVICE_ACCESS(sh4)'s OWN value guards -- a separate cluster from the PCIC
 *  one above, in the switch #443 did not touch.  Four of them called exit(1) on one
 *  ordinary guest store; the witness is regress/sh4_val_witness.py.
 *
 *  The latch key is (class, INSTANCE, offending BIT).  All three parts are load-bearing
 *  and each was arrived at by a failure this project has already paid for:
 *
 *    - the CLASS is the kind of COMPLAINT, per #443's pass-2 finding.
 *    - the INSTANCE is which register raised it.  Three TCRs reach one `case` through
 *      fall-through and eight DMATCRs reach another, so a latch keyed on the class
 *      alone would report timer 0 and silence timers 1 and 2 -- #443's measured half
 *      fix, one level down and in a new dress.
 *    - the BIT is which unimplemented feature was asked for.  RCR1's single guard
 *      covers TWO independent features (SH_RCR1_CIE and SH_RCR1_AIE) and TCR's covers
 *      SIX, so a latch keyed on (class, instance) reports the first feature a guest
 *      asks for and silently swallows every other one at the same register.
 *
 *  Bounded by construction -- at most one line per (class, instance, bit) -- so a guest
 *  looping on a rejected write cannot burn host CPU.  That bound is the reason the
 *  latch exists at all: fatal() has no quiet_mode early-out, unlike debug(), so an
 *  unlatched complaint could not be silenced even with -q.
 */
#define	SH4_VAL_TCRBITS			0	/*  TCR: control bits not modelled       */
#define	SH4_VAL_DMATCR			1	/*  DMATCR: count wider than 24 bits     */
#define	SH4_VAL_ICRIRLM			2	/*  ICR: IRLM mode not modelled          */
#define	SH4_VAL_RCR1INT			3	/*  RCR1: RTC interrupt enable not modelled  */
/*
 *  #448: the four CHCR field decoders in sh4_dmac_transfer().  Each guarded a `default:`
 *  arm that called exit(1), so ONE ordinary guest store ended the host process -- and it
 *  was EASIER TO REACH THAN ANY #447 SITE, because only `case 0x200:` survives the RS
 *  switch.  A wholly legal configuration (4-byte transfers, both addresses incrementing)
 *  still died, on its resource-select alone.
 *
 *  *** THE KEY IS A NORMALISED FIELD VALUE, NOT A BIT AND NOT THE WHOLE REGISTER. ***
 *  TS, DM, SM and RS are ENCODINGS: `TS=5` is one value, not three set bits, so a per-bit
 *  latch would report the same rejected encoding several times over.  The other extreme is
 *  worse: latching the whole CHCR word lets a guest walk 32-bit values with TD set and
 *  draw a fresh unsilenceable line for each -- the flood this latch exists to prevent.
 *
 *  The normalised value is used as a SHIFT AMOUNT into the existing uint32_t latch, and
 *  the field mask bounds it BY CONSTRUCTION: RS >> 8 is 0..15, TS >> 4 is 0..7, DM >> 14
 *  and SM >> 12 are 0..3.  A raw field value such as 0xc000 as an index would not be.
 *
 *  The resulting ceiling is exact and small: TS has 3 unmodelled encodings, DM 1, SM 1 and
 *  RS 15 -- 20 per channel, 160 for an eight-channel controller.
 */
#define	SH4_VAL_DMACTS			4	/*  CHCR: transmit size encoding      */
#define	SH4_VAL_DMACDM			5	/*  CHCR: destination address mode    */
#define	SH4_VAL_DMACSM			6	/*  CHCR: source address mode         */
#define	SH4_VAL_DMACRS			7	/*  CHCR: resource select             */
/*
 *  #449: the refresh-timer interrupt enables, and this one is NOT reached from a store.
 *  The guest write to RTCSR lands and returns normally; sh4_timer_tick() then read the
 *  enable bits and called exit(1) -- about nine milliseconds later, at 110 Hz.  Every
 *  SH-4 probe in this tree observes the STORE SITE, so all of them were blind to it.
 *
 *  *** IT NEEDS ITS OWN CLASS AND MUST NOT REUSE SH4_VAL_RCR1INT. ***  That class is the
 *  nearest neighbour -- also "an interrupt enable this device does not model" -- and
 *  sharing it would make an earlier RCR1 complaint silence RTCSR, and the reverse.  A
 *  review seat named the collision before it was written.
 */
#define	SH4_VAL_RTCSRINT		8	/*  RTCSR: refresh interrupt enables  */
#define	SH4_VAL_NCLASS			9
/*  Instances per class: 8 DMA channels is the widest.  N_SH4_TIMERS is 3.  */
#define	N_SH4_VAL_INST			N_SH4_DMA_CHANNELS


/*  #447: the six TCR bits this device does not model, spelled ONCE so the guard and
    its diagnostic cannot drift apart.  thirdparty/sh4_tmureg.h:75-82.  */
#define	TCR_UNIMPLEMENTED		(TCR_ICPF | TCR_ICPE1 | TCR_ICPE0 | \
					 TCR_CKEG1 | TCR_CKEG0 | TCR_TPSC2)

#define	PCI_VENDOR_HITACHI		0x1054
#define	PCI_PRODUCT_HITACHI_SH7751	0x3505
#define	PCI_PRODUCT_HITACHI_SH7751R	0x350e   

#define	SCIF_TX_FIFO_SIZE	16
#define	SCIF_DELAYED_TX_VALUE	2	/*  2 to be safe, 1 = fast but buggy  */

// Clock/occilation related
#define SH4_CPG_FRQCR		0xffc00000	/* 16-bit */
#define SH4_CPG_STBCR 		0xffc00004	/* 8-bit */
#define SH4_CPG_WTCNT 		0xffc00008	/* 8/16-bit */
#define SH4_CPG_WTCSR 		0xffc0000c	/* 8/16-bit */
#define SH4_CPG_STBCR2 		0xffc00010	/* 8-bit */


struct sh4_data {
	/*  Store Queues:  */
	uint8_t		sq[32 * 2];

	/*  SCIF (Serial controller):  */
	uint16_t	scif_smr;
	uint8_t		scif_brr;
	uint16_t	scif_scr;
	uint16_t	scif_ssr;
	uint16_t	scif_fcr;
	uint16_t	scif_lsr;
	int		scif_delayed_tx;
	int		scif_console_handle;
	uint8_t		scif_tx_fifo[SCIF_TX_FIFO_SIZE + 1];
	size_t		scif_tx_fifo_cursize;
	struct interrupt scif_tx_irq;
	struct interrupt scif_rx_irq;
	int		scif_tx_irq_asserted;
	int		scif_rx_irq_asserted;

	/*  Bus State Controller:  */
	uint32_t	bsc_bcr1;
	uint16_t	bsc_bcr2;
	uint16_t	bsc_bcr3;	/*  SH7751R  */
	/*  #441: has the non-16-bit diagnostic been given for BCR2 / BCR3?
	    PER SITE, NOT SHARED: a shared flag demotes the second register's
	    FIRST report, which is #438's "1 of 4 kinds" hazard.  A two-character
	    mutant ([site] -> [0]) passed a 13-row detector until the oracle was
	    corrected -- see the comment on sh4_bsc16_report().  */
	int		bsc16_reported[2];
	uint32_t	bsc_wcr1;
	uint32_t	bsc_wcr2;
	uint32_t	bsc_wcr3;
	uint32_t	bsc_mcr;
	uint16_t	bsc_pcr;
	uint16_t	bsc_rtcsr;
	uint16_t	bsc_rtcor;
	uint16_t	bsc_rfcr;

	/*  CPG:  */
	uint16_t	cpg_frqcr;
	uint8_t		cpg_stbcr;
	uint16_t	cpg_wtcnt;
	uint16_t	cpg_wtcsr;
	uint8_t		cpg_stbcr2;

	/*  GPIO:  */
	uint32_t	pctra;		/*  Port Control Register A  */
	uint32_t	pdtra;		/*  Port Data Register A  */
	uint32_t	pctrb;		/*  Port Control Register B  */
	uint32_t	pdtrb;		/*  Port Data Register B  */
	uint16_t	bsc_gpioic;

	/*  PCIC (PCI controller):  */
	struct pci_data	*pci_data;
	struct interrupt cpu_pcic_interrupt[N_PCIC_IRQS];
	uint32_t	pcic_reg[N_PCIC_REGS];
	/*  #443: one bit per word offset, so each unsupported transaction is reported
	    ONCE and a second, DIFFERENT one is not hidden behind the first.  A
	    per-device flag would hide it (the "1 of 4 kinds" hazard #438 recorded);
	    137 named flags would be absurd.  This is five words.  */
	/*  #443 pass 2: [fault class][word].  TWO classes, not one -- see
	    sh4_pcic_first().  */
	uint32_t	pcic_reported[SH4_PCIC_NCLASS][(N_PCIC_REGS + 31) / 32];

	/*  SCI (serial interface):  */
	int		sci_bits_outputed;
	int		sci_bits_read;
	uint8_t		sci_scsptr;
	uint8_t		sci_curbyte;
	uint8_t		sci_cur_addr;

	/*  SD-RAM:  */
	uint16_t	sdmr2;
	uint16_t	sdmr3;

	/*  Timer Management Unit:  */
	struct timer	*sh4_timer;
	struct interrupt timer_irq[4];
	uint32_t	tocr;
	uint32_t	tstr;
	uint32_t	tcnt[N_SH4_TIMERS];
	uint32_t	tcor[N_SH4_TIMERS];
	uint32_t	tcr[N_SH4_TIMERS];
	int		timer_interrupts_pending[N_SH4_TIMERS];
	double		timer_hz[N_SH4_TIMERS];

	/*  #447: [class][instance] -> the offending bits already reported.  See the
	    SH4_VAL_* block near the top of this file for why the key has three parts.  */
	uint32_t	val_reported[SH4_VAL_NCLASS][N_SH4_VAL_INST];

	/*  RTC:  */
	uint32_t	rtc_reg[14];	/*  Excluding rcr1 and rcr2  */
	uint8_t		rtc_rcr1;
	uint8_t		rtc_rcr2;
};


#define	SH4_PSEUDO_TIMER_HZ	110.0


/*  #448/#449: the latch helper is defined far below, and BOTH sh4_timer_tick() and
    sh4_dmac_transfer() are above it, so the prototype lives here -- immediately after
    `struct sh4_data` and before the first user.
    It must not sit beside the SH4_VAL_* defines: a prototype naming a struct the compiler
    has not seen yet declares a NEW type in PARAMETER SCOPE.  That compiles, warns, and
    then mismatches the real definition.  Measured while writing #448.  */
static int sh4_val_first(struct sh4_data *d, int cls, int instance, uint32_t bits);


/*
 *  sh4_timer_tick():
 *
 *  This function is called SH4_PSEUDO_TIMER_HZ times per real-world second.
 *  Its job is to update the SH4 timer counters, and if necessary, increase
 *  the number of pending interrupts.
 *
 *  Also, RAM Refresh is also faked here.
 */
static void sh4_timer_tick(struct timer *t, void *extra)
{
	struct sh4_data *d = (struct sh4_data *) extra;
	int i;

	/*  Fake RAM refresh:  */
	d->bsc_rfcr ++;
	/*
	 *  #449: this called exit(1), and it is reached from a HOST TIMER CALLBACK rather
	 *  than from a guest store.  A guest write to RTCSR lands, the handler returns
	 *  normally, and the process dies here about nine milliseconds later.  MEASURED on
	 *  an unmodified -E landisk: the store alone leaves the host alive (which is why
	 *  every store-site probe in this tree was blind to it), and a bounded free run
	 *  after it kills the host with this diagnostic.  Two controls survive the same
	 *  free run -- RTCSR 0x00, and RTCSR_CMF, a DIFFERENT bit of the SAME byte.
	 *
	 *  *** FALL THROUGH.  DO NOT RETURN. ***  The rest of this function is the TMU
	 *  channel 0-2 update, which never reads bsc_rtcsr; the refresh work above is
	 *  already done.  Returning early would make every tick skip the TMU while a
	 *  DRAM-refresh enable bit stays set -- the #400 wall-clock freeze, newly gated on
	 *  an unrelated register.  A review seat named that before it was written, and
	 *  regress/diff_sh4_tmu.c now carries the row that catches it offline.
	 *
	 *  THE LATCH IS LOAD-BEARING HERE IN A WAY IT WAS NOT ON THE STORE-SITE ROUNDS.
	 *  This runs at SH4_PSEUDO_TIMER_HZ, and timer.c can burst several ticks inside one
	 *  signal; fatal() has no quiet_mode early-out, so an unlatched complaint is a
	 *  flood that -q cannot stop.  The key is (class, instance 0, enable bits), and
	 *  sh4_val_first() never clears -- so a guest that writes 0 and re-sets CMIE gets
	 *  no second line, deliberately.  At most one line per bit for the device lifetime.
	 *
	 *  THE WORDING IS NOT "write ignored", WHICH IS THE RCR1 SENTENCE AND WOULD BE A
	 *  LIE HERE: the write DID land, and the guest can read it back.  What is missing
	 *  is the delivery of the interrupt.
	 */
	if (d->bsc_rtcsr & (RTCSR_CMIE | RTCSR_OVIE)) {
		/*
		 *  TWO WORDINGS HERE WERE CORRECTED BY A PASS-2 SEAT, and both were
		 *  wrong in the same direction -- more specific than the code earns.
		 *
		 *  "the interrupt is NOT delivered" reads as though a refresh interrupt
		 *  becomes pending and is then dropped.  Nothing becomes pending: CMF and
		 *  OVF are never set on any path in this device, and RTCNT has no `case`
		 *  at all, so there is no compare-match to raise.  The honest statement is
		 *  that the GENERATION of the interrupt is not implemented.
		 *
		 *  "(once per bit)" is not quite what the latch does either: a single
		 *  store that sets BOTH enables for the first time yields ONE coalesced
		 *  line naming 0x42, not two.  Row R3 of sh4_rtcsr_probe.py measures
		 *  exactly that, so the comment and the row now agree.
		 */
		if (sh4_val_first(d, SH4_VAL_RTCSRINT, 0,
		    d->bsc_rtcsr & (RTCSR_CMIE | RTCSR_OVIE)))
			fatal("[ sh4: refresh interrupt enable(s) 0x%02x stored,"
			    " but refresh-interrupt generation is not implemented"
			    " -- each enable is reported once ]\n",
			    (int) (d->bsc_rtcsr & (RTCSR_CMIE | RTCSR_OVIE)));
		/*  TODO: Implement refresh interrupts etc.  */
	}

	/*  Timer interrupts:  */
	for (i=0; i<N_SH4_TIMERS; i++) {
		uint32_t step, cnt;

		/*  Only update timers that are currently started:  */
		if (!(d->tstr & (TSTR_STR0 << i)))
			continue;

		step = (uint32_t) (d->timer_hz[i] / SH4_PSEUDO_TIMER_HZ);
		cnt  = d->tcnt[i];

		/*
		 *  #400: THE COUNTER'S CONVENTION, kept here because this is the
		 *  only place in the tree that records it. TCNT counts
		 *  TCOR, TCOR-1, ..., 1, 0 and then underflows to TCOR, so a
		 *  period is TCOR+1 counts. That is an ASSUMPTION -- there is no
		 *  SH-4 manual in this source collection -- and it is inherited
		 *  from the comment this hunk replaces, which stated the intent as
		 *  "Set tcnt[i] to tcor[i]" on underflow. Deleting that sentence
		 *  without restating it would have removed the only evidence for
		 *  the arithmetic below.
		 *
		 *  The previous code did all of this through int32_t and then
		 *  clamped a negative result to zero, which pinned TCNT at 0
		 *  permanently once a reload could not lift it back above the sign
		 *  boundary -- measured on a booting OpenBSD/landisk guest as a
		 *  wall clock that froze after 515.4 s and never recovered. It
		 *  also landed on TCOR-1 rather than TCOR, so it did not implement
		 *  its own comment.
		 *
		 *  The 64-bit cast on `period` is load-bearing: computed in
		 *  uint32_t, TCOR == 0xffffffff makes it 0 and the modulo below is
		 *  a division by zero. Modulo rather than a loop, because a loop
		 *  does not terminate for TCOR == 0 or for a 32-bit period of 0.
		 */
		if (step <= cnt) {
			d->tcnt[i] = cnt - step;
		} else {
			uint64_t period    = (uint64_t)d->tcor[i] + 1;
			uint64_t remaining = (uint64_t)step - cnt - 1;

			d->tcnt[i] = d->tcor[i] - (uint32_t)(remaining % period);

			d->tcr[i] |= TCR_UNF;

			/*
			 *  One pending interrupt per call, which is what the
			 *  previous code did and is UNCHANGED here rather than
			 *  corrected: a call spanning several periods still counts
			 *  one. Whether the emulator should queue N or coalesce is
			 *  a separate design question that this source cannot
			 *  settle, so it is recorded rather than decided.
			 */
			if (d->tcr[i] & TCR_UNIE)
				d->timer_interrupts_pending[i] ++;
		}
	}
}


static void sh4_pcic_interrupt_assert(struct interrupt *interrupt)
{
	struct sh4_data *d = (struct sh4_data *) interrupt->extra;
	INTERRUPT_ASSERT(d->cpu_pcic_interrupt[interrupt->line]);
}
static void sh4_pcic_interrupt_deassert(struct interrupt *interrupt)
{
	struct sh4_data *d = (struct sh4_data *) interrupt->extra;
	INTERRUPT_DEASSERT(d->cpu_pcic_interrupt[interrupt->line]);
}


static void scif_reassert_interrupts(struct sh4_data *d)
{
	int old_tx_asserted = d->scif_tx_irq_asserted;
	int old_rx_asserted = d->scif_rx_irq_asserted;

	d->scif_rx_irq_asserted =
	    d->scif_scr & SCSCR2_RIE && d->scif_ssr & SCSSR2_DR;

	if (d->scif_rx_irq_asserted && !old_rx_asserted)
		INTERRUPT_ASSERT(d->scif_rx_irq);
	else if (!d->scif_rx_irq_asserted && old_rx_asserted)
		INTERRUPT_DEASSERT(d->scif_rx_irq);

	d->scif_tx_irq_asserted =
	    d->scif_scr & SCSCR2_TIE &&
	    d->scif_ssr & (SCSSR2_TDFE | SCSSR2_TEND);

	if (d->scif_tx_irq_asserted && !old_tx_asserted)
		INTERRUPT_ASSERT(d->scif_tx_irq);
	else if (!d->scif_tx_irq_asserted && old_tx_asserted)
		INTERRUPT_DEASSERT(d->scif_tx_irq);
}


DEVICE_TICK(sh4)
{
	struct sh4_data *d = (struct sh4_data *) extra;
	unsigned int i;

	/*
	 *  Serial controller interrupts:
	 *
	 *  RX: Cause interrupt if any char is available.
	 *  TX: Send entire TX FIFO contents, and interrupt.
	 */
	if (console_charavail(d->scif_console_handle))
		d->scif_ssr |= SCSSR2_DR;
	else
		d->scif_ssr &= ~SCSSR2_DR;

	if (d->scif_delayed_tx) {
		if (--d->scif_delayed_tx == 0) {
			/*  Send TX FIFO contents:  */
			for (i=0; i<d->scif_tx_fifo_cursize; i++)
				console_putchar(d->scif_console_handle,
				    d->scif_tx_fifo[i]);

			/*  Clear FIFO:  */
			d->scif_tx_fifo_cursize = 0;

			/*  Done sending; cause a transmit end interrupt:  */
			d->scif_ssr |= SCSSR2_TDFE | SCSSR2_TEND;
		}
	}

	scif_reassert_interrupts(d);

	/*  Timer interrupts:  */
	for (i=0; i<N_SH4_TIMERS; i++)
		if (d->timer_interrupts_pending[i] > 0) {
			INTERRUPT_ASSERT(d->timer_irq[i]);
			d->tcr[i] |= TCR_UNF;
		}
}


/*
 *  sh4_dmac_transfer():
 *
 *  Called whenever a DMA transfer is to be executed.
 *  Clears the lowest bit of the corresponding channel's CHCR when done.
 */
void sh4_dmac_transfer(struct cpu *cpu, struct sh4_data *d, int channel)
{
	/*  According to the SH7760 manual, bits 31..29 are ignored in  */
	/*  both the SAR and DAR.  */
	uint32_t sar = cpu->cd.sh.dmac_sar[channel] & 0x1fffffff;
	uint32_t dar = cpu->cd.sh.dmac_dar[channel] & 0x1fffffff;
	uint32_t count = cpu->cd.sh.dmac_tcr[channel] & 0x1fffffff;
	uint32_t chcr = cpu->cd.sh.dmac_chcr[channel];
	int transmit_size = 1;
	int src_delta = 0, dst_delta = 0;
	int cause_interrupt = chcr & CHCR_IE;

	/*  DMAC not enabled? Then just return.  */
	if (!(chcr & CHCR_TD))
		return;

	/*  Transfer End already set? Then don't transfer again.  */
	if (chcr & CHCR_TE)
		return;

	/*  Special case: 0 means 16777216:  */
	if (count == 0)
		count = 16777216;

	switch (chcr & CHCR_TS) {
	case CHCR_TS_8BYTE: transmit_size = 8; break;
	case CHCR_TS_1BYTE: transmit_size = 1; break;
	case CHCR_TS_2BYTE: transmit_size = 2; break;
	case CHCR_TS_4BYTE: transmit_size = 4; break;
	case CHCR_TS_32BYTE: transmit_size = 32; break;
	/*
	 *  #448: RETURN, NEVER `break`.  A review seat named `return;` -> `break;` as the
	 *  smallest edit that reintroduces a defect while a naive detector still passes:
	 *  the diagnostic and the latch both still run, so an alive-plus-diagnostic row
	 *  goes green, and execution falls out of the switch with transmit_size left at
	 *  its initialiser -- an unmodelled encoding SILENTLY TREATED AS 1 BYTE.
	 *
	 *  It is detectable, and the detector row is built on this: a `break` here falls
	 *  through to the RS switch, which for most values complains too, so the escape
	 *  shows up as a SECOND diagnostic from a single store.  Exactly one is correct.
	 */
	default:
		if (sh4_val_first(d, SH4_VAL_DMACTS, channel,
		    1u << ((chcr & CHCR_TS) >> 4)))
			fatal("[ sh4: DMA channel %i: transmit size %i not"
			    " implemented -- transfer declined.  (once per"
			    " encoding) ]\n", channel,
			    (int) ((chcr & CHCR_TS) >> 4));
		return;
	}

	switch (chcr & CHCR_DM) {
	case CHCR_DM_FIXED:       dst_delta = 0; break;
	case CHCR_DM_INCREMENTED: dst_delta = 1; break;
	case CHCR_DM_DECREMENTED: dst_delta = -1; break;
	default:
		if (sh4_val_first(d, SH4_VAL_DMACDM, channel,
		    1u << ((chcr & CHCR_DM) >> 14)))
			fatal("[ sh4: DMA channel %i: destination address mode"
			    " %i not implemented -- transfer declined.  (once"
			    " per encoding) ]\n", channel,
			    (int) ((chcr & CHCR_DM) >> 14));
		return;
	}

	switch (chcr & CHCR_SM) {
	case CHCR_SM_FIXED:       src_delta = 0; break;
	case CHCR_SM_INCREMENTED: src_delta = 1; break;
	case CHCR_SM_DECREMENTED: src_delta = -1; break;
	default:
		if (sh4_val_first(d, SH4_VAL_DMACSM, channel,
		    1u << ((chcr & CHCR_SM) >> 12)))
			fatal("[ sh4: DMA channel %i: source address mode %i"
			    " not implemented -- transfer declined.  (once per"
			    " encoding) ]\n", channel,
			    (int) ((chcr & CHCR_SM) >> 12));
		return;
	}

	src_delta *= transmit_size;
	dst_delta *= transmit_size;

#ifdef SH4_DEBUG
	fatal("|SH4 DMA transfer, channel %i\n", channel);
	fatal("|Source addr:      0x%08x (delta %i)\n", (int) sar, src_delta);
	fatal("|Destination addr: 0x%08x (delta %i)\n", (int) dar, dst_delta);
	fatal("|Count:            0x%08x\n", (int) count);
	fatal("|Transmit size:    0x%08x\n", (int) transmit_size);
	fatal("|Interrupt:        %s\n", cause_interrupt? "yes" : "no");
#endif

	switch (chcr & CHCR_RS) {
	case 0x200:
		/*
		 *  Single Address Mode
		 *  External Address Space => external device
		 */

		// Avoid compiler warnings about unused sar and dar.
		(void)sar;
		(void)dar;

		/*  Note: No transfer is done here! It is up to the
		    external device to do the transfer itself!  */
		break;

	/*
	 *  *** THIS ARM IS WHY THE DEFECT WAS BROAD.  Only `case 0x200:` above returns
	 *  normally, so FIFTEEN of the sixteen resource-select encodings reached exit(1)
	 *  -- and a wholly legal transfer configuration (4-byte, both addresses
	 *  incrementing) still ended the host, on its resource-select alone. ***
	 */
	default:
		if (sh4_val_first(d, SH4_VAL_DMACRS, channel,
		    1u << ((chcr & CHCR_RS) >> 8)))
			fatal("[ sh4: DMA channel %i: resource select %i not"
			    " implemented -- transfer declined.  (once per"
			    " encoding) ]\n", channel,
			    (int) ((chcr & CHCR_RS) >> 8));
		return;
	}

	if (cause_interrupt) {
		fatal("TODO: sh4 dmac interrupt!\n");
		exit(1);
	}
}


/*
 *  sh4_sci_cmd():
 *
 *  Handle a SCI command byte.
 *
 *  Bit:   Meaning:
 *   7      Ignored (usually 1?)
 *   6      0=Write, 1=Read
 *   5      AD: Address transfer
 *   4      DT: Data transfer
 *   3..0   Data or address bits
 */
static void sh4_sci_cmd(struct sh4_data *d, struct cpu *cpu)
{
	uint8_t cmd = d->sci_curbyte;
	int writeflag = cmd & 0x40? 0 : 1;
	int address_transfer;

	/*  fatal("[ CMD BYTE %02x ]\n", cmd);  */

	if (!(cmd & 0x80)) {
		fatal("SCI cmd bit 7 not set? TODO\n");
		exit(1);
	}

	if ((cmd & 0x30) == 0x20)
		address_transfer = 1;
	else if ((cmd & 0x30) == 0x10)
		address_transfer = 0;
	else {
		fatal("SCI: Neither data nor address transfer? TODO\n");
		exit(1);
	}

	if (address_transfer)
		d->sci_cur_addr = cmd & 0x0f;

	if (!writeflag) {
		/*  Read data from the current address:  */
		uint8_t data_byte;

		cpu->memory_rw(cpu, cpu->mem, SCI_DEVICE_BASE + d->sci_cur_addr,
		    &data_byte, 1, MEM_READ, PHYSICAL);

		debug("[ SCI: read addr=%x data=%x ]\n",
		    d->sci_cur_addr, data_byte);

		d->sci_curbyte = data_byte;

		/*  Set bit 7 right away:  */
		d->sci_scsptr &= ~SCSPTR_SPB1DT;
		if (data_byte & 0x80)
			d->sci_scsptr |= SCSPTR_SPB1DT;
	}

	if (writeflag && !address_transfer) {
		/*  Write the 4 data bits to the current address:  */
		uint8_t data_byte = cmd & 0x0f;

		debug("[ SCI: write addr=%x data=%x ]\n",
		    d->sci_cur_addr, data_byte);

		cpu->memory_rw(cpu, cpu->mem, SCI_DEVICE_BASE + d->sci_cur_addr,
		    &data_byte, 1, MEM_WRITE, PHYSICAL);
	}
}


/*
 *  sh4_sci_access():
 *
 *  Reads or writes a bit via the SH4's serial interface. If writeflag is
 *  non-zero, input is used. If writeflag is zero, a bit is outputed as
 *  the return value from this function.
 */
static uint8_t sh4_sci_access(struct sh4_data *d, struct cpu *cpu,
	int writeflag, uint8_t input)
{
	if (writeflag) {
		/*  WRITE:  */
		int clockpulse;
		uint8_t old = d->sci_scsptr;
		d->sci_scsptr = input;

		/*
		 *  Clock pulse (SCSPTR_SPB0DT going from 0 to 1,
		 *  when SCSPTR_SPB0IO was already set):
		 */
		clockpulse = old & SCSPTR_SPB0IO &&
		    d->sci_scsptr & SCSPTR_SPB0DT &&
		    !(old & SCSPTR_SPB0DT);

		if (!clockpulse)
			return 0;

		/*  Are we in output or input mode?  */
		if (d->sci_scsptr & SCSPTR_SPB1IO) {
			/*  Output:  */
			int bit = d->sci_scsptr & SCSPTR_SPB1DT? 1 : 0;
			d->sci_curbyte <<= 1;
			d->sci_curbyte |= bit;
			d->sci_bits_outputed ++;
			if (d->sci_bits_outputed == 8) {
				/*  4 control bits and 4 address/data bits have
				    been written.  */
				sh4_sci_cmd(d, cpu);
				d->sci_bits_outputed = 0;
			}
		} else {
			/*  Input:  */
			int bit;
			d->sci_bits_read ++;
			d->sci_bits_read &= 7;

			bit = d->sci_curbyte & (0x80 >> d->sci_bits_read);

			d->sci_scsptr &= ~SCSPTR_SPB1DT;
			if (bit)
				d->sci_scsptr |= SCSPTR_SPB1DT;
		}

		/*  Return (value doesn't matter).  */
		return 0;
	} else {
		/*  READ:  */
		return d->sci_scsptr;
	}
}


DEVICE_ACCESS(sh4_itlb_aa)
{
	uint64_t idata = 0, odata = 0;
	int e = (relative_addr & SH4_ITLB_E_MASK) >> SH4_ITLB_E_SHIFT;

	if (writeflag == MEM_WRITE) {
		int safe_to_invalidate = 0;
		uint32_t old_hi = cpu->cd.sh.itlb_hi[e];
		if ((cpu->cd.sh.itlb_lo[e] & SH4_PTEL_SZ_MASK)==SH4_PTEL_SZ_4K)
			safe_to_invalidate = 1;

		idata = memory_readmax64(cpu, data, len);
		cpu->cd.sh.itlb_hi[e] &=
		    ~(SH4_PTEH_VPN_MASK | SH4_PTEH_ASID_MASK);
		cpu->cd.sh.itlb_hi[e] |= (idata &
		    (SH4_ITLB_AA_VPN_MASK | SH4_ITLB_AA_ASID_MASK));
		cpu->cd.sh.itlb_lo[e] &= ~SH4_PTEL_V;
		if (idata & SH4_ITLB_AA_V)
			cpu->cd.sh.itlb_lo[e] |= SH4_PTEL_V;

		/*  Invalidate if this ITLB entry previously belonged to the
		    currently running process, or if it was shared:  */
		if (cpu->cd.sh.ptel & SH4_PTEL_SH ||
		    (old_hi & SH4_ITLB_AA_ASID_MASK) ==
		    (cpu->cd.sh.pteh & SH4_PTEH_ASID_MASK)) {
			if (safe_to_invalidate)
				cpu->invalidate_translation_caches(cpu,
				    old_hi & ~0xfff, INVALIDATE_VADDR);
			else
				cpu->invalidate_translation_caches(cpu,
				    0, INVALIDATE_ALL);
		}
	} else {
		odata = cpu->cd.sh.itlb_hi[e] &
		    (SH4_ITLB_AA_VPN_MASK | SH4_ITLB_AA_ASID_MASK);
		if (cpu->cd.sh.itlb_lo[e] & SH4_PTEL_V)
			odata |= SH4_ITLB_AA_V;
		memory_writemax64(cpu, data, len, odata);
	}

	return 1;
}


DEVICE_ACCESS(sh4_itlb_da1)
{
	uint32_t mask = SH4_PTEL_SH | SH4_PTEL_C | SH4_PTEL_SZ_MASK |
	    SH4_PTEL_PR_MASK | SH4_PTEL_V | 0x1ffffc00;
	uint64_t idata = 0, odata = 0;
	int e = (relative_addr & SH4_ITLB_E_MASK) >> SH4_ITLB_E_SHIFT;

	if (relative_addr & 0x800000) {
		fatal("sh4_itlb_da1: TODO: da2 area\n");
		exit(1);
	}

	if (writeflag == MEM_WRITE) {
		uint32_t old_lo = cpu->cd.sh.itlb_lo[e];
		int safe_to_invalidate = 0;
		if ((cpu->cd.sh.itlb_lo[e] & SH4_PTEL_SZ_MASK)==SH4_PTEL_SZ_4K)
			safe_to_invalidate = 1;

		idata = memory_readmax64(cpu, data, len);
		cpu->cd.sh.itlb_lo[e] &= ~mask;
		cpu->cd.sh.itlb_lo[e] |= (idata & mask);

		/*  Invalidate if this ITLB entry belongs to the
		    currently running process, or if it was shared:  */
		if (old_lo & SH4_PTEL_SH ||
		    (cpu->cd.sh.itlb_hi[e] & SH4_ITLB_AA_ASID_MASK) ==
		    (cpu->cd.sh.pteh & SH4_PTEH_ASID_MASK)) {
			if (safe_to_invalidate)
				cpu->invalidate_translation_caches(cpu,
				    cpu->cd.sh.itlb_hi[e] & ~0xfff,
				    INVALIDATE_VADDR);
			else
				cpu->invalidate_translation_caches(cpu,
				    0, INVALIDATE_ALL);
		}
	} else {
		odata = cpu->cd.sh.itlb_lo[e] & mask;
		memory_writemax64(cpu, data, len, odata);
	}

	return 1;
}


DEVICE_ACCESS(sh4_utlb_aa)
{
	uint64_t idata = 0, odata = 0;
	int i, e = (relative_addr & SH4_UTLB_E_MASK) >> SH4_UTLB_E_SHIFT;
	int a = relative_addr & SH4_UTLB_A;

	if (writeflag == MEM_WRITE) {
		int n_hits = 0;
		int safe_to_invalidate = 0;
		uint32_t vaddr_to_invalidate = 0;

		idata = memory_readmax64(cpu, data, len);
		if (a) {
			for (i=-SH_N_ITLB_ENTRIES; i<SH_N_UTLB_ENTRIES; i++) {
				uint32_t lo, hi;
				uint32_t mask = 0xfffff000;
				int sh;

				if (i < 0) {
					lo = cpu->cd.sh.itlb_lo[
					    i + SH_N_ITLB_ENTRIES];
					hi = cpu->cd.sh.itlb_hi[
					    i + SH_N_ITLB_ENTRIES];
				} else {
					lo = cpu->cd.sh.utlb_lo[i];
					hi = cpu->cd.sh.utlb_hi[i];
				}

				sh = lo & SH4_PTEL_SH;
				if (!(lo & SH4_PTEL_V))
					continue;

				switch (lo & SH4_PTEL_SZ_MASK) {
				case SH4_PTEL_SZ_1K:  mask = 0xfffffc00; break;
				case SH4_PTEL_SZ_64K: mask = 0xffff0000; break;
				case SH4_PTEL_SZ_1M:  mask = 0xfff00000; break;
				}

				if ((hi & mask) != (idata & mask))
					continue;

				if ((lo & SH4_PTEL_SZ_MASK) ==
				    SH4_PTEL_SZ_4K) {
					safe_to_invalidate = 1;
					vaddr_to_invalidate = hi & mask;
				}

				if (!sh && (hi & SH4_PTEH_ASID_MASK) !=
				    (cpu->cd.sh.pteh & SH4_PTEH_ASID_MASK))
					continue;

				if (i < 0) {
					cpu->cd.sh.itlb_lo[i +
					    SH_N_ITLB_ENTRIES] &= ~SH4_PTEL_V;
					if (idata & SH4_UTLB_AA_V)
						cpu->cd.sh.itlb_lo[
						    i+SH_N_ITLB_ENTRIES] |=
						    SH4_PTEL_V;
				} else {
					cpu->cd.sh.utlb_lo[i] &=
					    ~(SH4_PTEL_D | SH4_PTEL_V);
					if (idata & SH4_UTLB_AA_D)
						cpu->cd.sh.utlb_lo[i] |=
						    SH4_PTEL_D;
					if (idata & SH4_UTLB_AA_V)
						cpu->cd.sh.utlb_lo[i] |=
						    SH4_PTEL_V;
				}

				if (i >= 0)
					n_hits ++;
			}

			if (n_hits > 1)
				sh_exception(cpu,
				    EXPEVT_RESET_TLB_MULTI_HIT, 0, 0);
		} else {
			if ((cpu->cd.sh.utlb_lo[e] & SH4_PTEL_SZ_MASK) ==
			    SH4_PTEL_SZ_4K) {
				safe_to_invalidate = 1;
				vaddr_to_invalidate =
				    cpu->cd.sh.utlb_hi[e] & ~0xfff;
			}

			cpu->cd.sh.utlb_hi[e] &=
			    ~(SH4_PTEH_VPN_MASK | SH4_PTEH_ASID_MASK);
			cpu->cd.sh.utlb_hi[e] |= (idata &
			    (SH4_UTLB_AA_VPN_MASK | SH4_UTLB_AA_ASID_MASK));

			cpu->cd.sh.utlb_lo[e] &= ~(SH4_PTEL_D | SH4_PTEL_V);
			if (idata & SH4_UTLB_AA_D)
				cpu->cd.sh.utlb_lo[e] |= SH4_PTEL_D;
			if (idata & SH4_UTLB_AA_V)
				cpu->cd.sh.utlb_lo[e] |= SH4_PTEL_V;
		}

		if (safe_to_invalidate)
			cpu->invalidate_translation_caches(cpu,
			    vaddr_to_invalidate, INVALIDATE_VADDR);
		else
			cpu->invalidate_translation_caches(cpu, 0,
			    INVALIDATE_ALL);
	} else {
		odata = cpu->cd.sh.utlb_hi[e] &
		    (SH4_UTLB_AA_VPN_MASK | SH4_UTLB_AA_ASID_MASK);
		if (cpu->cd.sh.utlb_lo[e] & SH4_PTEL_D)
			odata |= SH4_UTLB_AA_D;
		if (cpu->cd.sh.utlb_lo[e] & SH4_PTEL_V)
			odata |= SH4_UTLB_AA_V;
		memory_writemax64(cpu, data, len, odata);
	}

	return 1;
}


DEVICE_ACCESS(sh4_utlb_da1)
{
	uint32_t mask = SH4_PTEL_WT | SH4_PTEL_SH | SH4_PTEL_D | SH4_PTEL_C
	    | SH4_PTEL_SZ_MASK | SH4_PTEL_PR_MASK | SH4_PTEL_V | 0x1ffffc00;
	uint64_t idata = 0, odata = 0;
	int e = (relative_addr & SH4_UTLB_E_MASK) >> SH4_UTLB_E_SHIFT;

	if (relative_addr & 0x800000) {
		fatal("sh4_utlb_da1: TODO: da2 area\n");
		exit(1);
	}

	if (writeflag == MEM_WRITE) {
		uint32_t old_lo = cpu->cd.sh.utlb_lo[e];
		int safe_to_invalidate = 0;
		if ((cpu->cd.sh.utlb_lo[e] & SH4_PTEL_SZ_MASK)==SH4_PTEL_SZ_4K)
			safe_to_invalidate = 1;

		idata = memory_readmax64(cpu, data, len);
		cpu->cd.sh.utlb_lo[e] &= ~mask;
		cpu->cd.sh.utlb_lo[e] |= (idata & mask);

		/*  Invalidate if this UTLB entry belongs to the
		    currently running process, or if it was shared:  */
		if (old_lo & SH4_PTEL_SH ||
		    (cpu->cd.sh.utlb_hi[e] & SH4_ITLB_AA_ASID_MASK) ==
		    (cpu->cd.sh.pteh & SH4_PTEH_ASID_MASK)) {
			if (safe_to_invalidate)
				cpu->invalidate_translation_caches(cpu,
				    cpu->cd.sh.utlb_hi[e] & ~0xfff,
				    INVALIDATE_VADDR);
			else
				cpu->invalidate_translation_caches(cpu,
				    0, INVALIDATE_ALL);
		}
	} else {
		odata = cpu->cd.sh.utlb_lo[e] & mask;
		memory_writemax64(cpu, data, len, odata);
	}

	return 1;
}


/*
 *  #443: an unsupported PCIC transaction called exit(1) -- ELEVEN sites.  A MEASURED
 *  census of all 137 word offsets in both directions (274 emulator processes) found
 *  116 of them kill the host on a plain 32-bit READ and 125 on a write.  ONE guest
 *  instruction, no store required.  Rung-3 witness: _scratchpad/sh4pcic_witness.py,
 *  30/30 on an unmodified -E landisk.  Guest-KERNEL reachable only: with SR.MD clear
 *  the same instruction takes an SH exception and the host survives.
 *
 *  Fixed in the #438/#441 shape -- keep the diagnostic, drop the exit(1) -- with two
 *  things about HOW that are load-bearing and would look like tidy-up to a later reader.
 *
 *  (1) *** THE STORE AT THE TOP OF THIS FUNCTION IS UPSTREAM OF EVERY GUARD. ***  A
 *  write lands in pcic_reg[] BEFORE the switch runs, so exit(1) was the only thing that
 *  ever stopped a guest reading an invalid value back.  DELETING IT ALONE WOULD TURN A
 *  HOST KILL INTO SILENT STATE CORRUPTION -- a strictly worse failure.  A pass-1 seat
 *  warned about this shape in general ("because exit was noreturn, a later assignment
 *  can become newly reachable"); in this file the assignment is not later, it is
 *  upstream, which is worse.  Every rejecting arm therefore restores the previous word.
 *
 *  (2) The complaint is latched PER WORD OFFSET *AND PER FAULT CLASS*.  fatal() has no
 *  quiet_mode early-out -- unlike debug() -- so an unlatched complaint could not be
 *  silenced even with -q, and a guest looping on a rejected write would trade a host
 *  kill for a host-CPU burn.
 *
 *  *** THE FAULT CLASS WAS ADDED IN PASS 2, BECAUSE LATCHING PER OFFSET ALONE
 *  REPRODUCED THE HAZARD THIS DESIGN EXISTS TO AVOID -- one level down. ***  #438
 *  recorded a per-device latch hiding "1 of 4 kinds"; a per-offset latch hides one of
 *  two kinds at the SAME offset, because one offset can raise two genuinely different
 *  complaints.  Measured twice on the shipped binary, one process each:
 *
 *    -C SH7750: a write to PCICONF0 printed, and the later "PCICONF0 read for
 *    unimplemented CPU type" was ABSENT -- though that read alone in a fresh process
 *    does print it.
 *
 *    a byte-write at 0xfe200015 printed "unimplemented addr", and the later
 *    "PCICONF5 unknown value" at 0xfe200014 was ABSENT, because PCIC_REG() maps both
 *    addresses to one word.
 *
 *  Severity was diagnostic-only -- the restore sits OUTSIDE the `if`, so device state
 *  stayed correct either way -- but the comment above claimed a property the code did
 *  not have, and that is the kind of wrong record this project treats as a defect
 *  rather than a wording nit.
 *
 *  *** AND TWO CLASSES WERE NOT ENOUGH: THE FIRST ATTEMPT AT THIS FIX WAS HALF A FIX,
 *  MEASURED. ***  It closed the aliasing case and left the PCICONF0 one open, because
 *  BOTH of that register's complaints -- a rejected write, and a read under a CPU type
 *  this device does not model -- were SH4_PCIC_BADVAL at the same word index, so they
 *  still shared one bit:
 *
 *    -C SH7750, read only        latched=1, "read for unimplemented CPU type" PRESENT
 *    -C SH7750, write then read  latched=1, that line ABSENT   <- STILL MERGED
 *
 *  A third class fixes it, and the general lesson is worth more than the fix: the
 *  classes are not "kinds of register", they are KINDS OF COMPLAINT, and one register
 *  can raise several.  Counting them from the register's point of view is what produced
 *  the half-fix.  Three classes cost thirty bytes.
 *
 *  THE RESTORE'S PLACEMENT OUTSIDE THE `if` IS LOAD-BEARING FOR THE SAME REASON: a
 *  pass-2 mutant that braced it INSIDE -- a brace slip, the kind a tidy-up produces --
 *  re-opened silent corruption on the second offence at all ten arms, and passed every
 *  detector row.
 */
static int sh4_pcic_first(struct sh4_data *d, uint32_t addr, int cls)
{
	size_t idx = PCIC_REG(addr);
	uint32_t bit;

	/*  #443 pass 2: this bounds check is NOT what protects the arrays, and a
	    reader should not take it for that.  pcic_reg[] is indexed with the same
	    expression at the top of dev_sh4_pcic_access() with NO check, so if the
	    registered window ever grew, THAT out-of-range access would happen first
	    and this one would never get the chance.  Kept because it is correct and
	    free; the real guarantee is that memory_device_register() registers
	    exactly N_PCIC_REGS words, MEASURED max index 136 of 137 across the full
	    census plus byte/halfword/word accesses at the window's last bytes.  */
	if (idx >= N_PCIC_REGS)
		return 0;

	bit = 1u << (idx & 31);
	if (d->pcic_reported[cls][idx >> 5] & bit)
		return 0;

	d->pcic_reported[cls][idx >> 5] |= bit;
	return 1;
}


DEVICE_ACCESS(sh4_pcic)
{
	struct sh4_data *d = (struct sh4_data *) extra;
	uint64_t idata = 0, odata = 0;
	uint32_t pcic_old;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	relative_addr += SH4_PCIC;

	/*  Register read/write:  */
	/*  #443: keep the previous word, so a rejecting arm below can put it back.  The
	    store happens HERE, before any guard runs.  */
	pcic_old = d->pcic_reg[PCIC_REG(relative_addr)];
	if (writeflag == MEM_WRITE)
		d->pcic_reg[PCIC_REG(relative_addr)] = idata;
	else
		odata = d->pcic_reg[PCIC_REG(relative_addr)];

	/*  Special cases:  */

	switch (relative_addr) {

	case SH4_PCICONF0:
		if (writeflag == MEM_WRITE) {
			if (sh4_pcic_first(d, relative_addr, SH4_PCIC_BADVAL))
				fatal("[ sh4_pcic: write to SH4_PCICONF0 --"
				    " ignored.  (once per offset) ]\n");
			d->pcic_reg[PCIC_REG(relative_addr)] = pcic_old;
		} else {
			if (strcmp(cpu->cd.sh.cpu_type.name, "SH7751") == 0) {
				odata = PCI_ID_CODE(PCI_VENDOR_HITACHI,
				    PCI_PRODUCT_HITACHI_SH7751);
			} else if (strcmp(cpu->cd.sh.cpu_type.name,
			    "SH7751R") == 0) {
				odata = PCI_ID_CODE(PCI_VENDOR_HITACHI,
				    PCI_PRODUCT_HITACHI_SH7751R);
			} else {
				/*  MEASURED unreachable on landisk, whose
				    default CPU is SH7751R and is accepted
				    above; reached with -C SH7750, an
				    already-supported type.  Nothing to
				    restore -- this is a READ, so the bad
				    state would be odata.  */
				if (sh4_pcic_first(d, relative_addr,
				    SH4_PCIC_NOCPU))
					fatal("[ sh4_pcic: PCICONF0 read for"
					    " unimplemented CPU type %s --"
					    " reads as zero.  (once per"
					    " offset) ]\n",
					    cpu->cd.sh.cpu_type.name);
				odata = 0;
			}
		}
		break;

	case SH4_PCICONF1:
	case SH4_PCICONF2:
	case SH4_PCICR:
	case SH4_PCIBCR1:
	case SH4_PCIBCR2:
	case SH4_PCIBCR3:
	case SH4_PCIWCR1:
	case SH4_PCIWCR2:
	case SH4_PCIWCR3:
	case SH4_PCIMCR:
		break;

	case SH4_PCICONF5:
		/*  Hardcoded to what OpenBSD/landisk uses:  */
		if (writeflag == MEM_WRITE && idata != 0xac000000) {
			if (sh4_pcic_first(d, relative_addr, SH4_PCIC_BADVAL))
				fatal("[ sh4_pcic: SH4_PCICONF5 unknown value"
				    " 0x%" PRIx32" -- ignored."
				    "  (once per offset) ]\n",
				    (uint32_t) idata);
			d->pcic_reg[PCIC_REG(relative_addr)] = pcic_old;
		}
		break;

	case SH4_PCICONF6:
		/*  Hardcoded to what OpenBSD/landisk uses:  */
		if (writeflag == MEM_WRITE && idata != 0x8c000000) {
			if (sh4_pcic_first(d, relative_addr, SH4_PCIC_BADVAL))
				fatal("[ sh4_pcic: SH4_PCICONF6 unknown value"
				    " 0x%" PRIx32" -- ignored."
				    "  (once per offset) ]\n",
				    (uint32_t) idata);
			d->pcic_reg[PCIC_REG(relative_addr)] = pcic_old;
		}
		break;

	case SH4_PCILSR0:
		/*  Hardcoded to what OpenBSD/landisk uses:  */
		if (writeflag == MEM_WRITE && idata != ((64 - 1) << 20)) {
			if (sh4_pcic_first(d, relative_addr, SH4_PCIC_BADVAL))
				fatal("[ sh4_pcic: SH4_PCILSR0 unknown value"
				    " 0x%" PRIx32" -- ignored."
				    "  (once per offset) ]\n",
				    (uint32_t) idata);
			d->pcic_reg[PCIC_REG(relative_addr)] = pcic_old;
		}
		break;

	case SH4_PCILAR0:
		/*  Hardcoded to what OpenBSD/landisk uses:  */
		if (writeflag == MEM_WRITE && idata != 0xac000000) {
			if (sh4_pcic_first(d, relative_addr, SH4_PCIC_BADVAL))
				fatal("[ sh4_pcic: SH4_PCILAR0 unknown value"
				    " 0x%" PRIx32" -- ignored."
				    "  (once per offset) ]\n",
				    (uint32_t) idata);
			d->pcic_reg[PCIC_REG(relative_addr)] = pcic_old;
		}
		break;

	case SH4_PCILSR1:
		/*  Hardcoded to what OpenBSD/landisk uses:  */
		if (writeflag == MEM_WRITE && idata != ((64 - 1) << 20)) {
			if (sh4_pcic_first(d, relative_addr, SH4_PCIC_BADVAL))
				fatal("[ sh4_pcic: SH4_PCILSR1 unknown value"
				    " 0x%" PRIx32" -- ignored."
				    "  (once per offset) ]\n",
				    (uint32_t) idata);
			d->pcic_reg[PCIC_REG(relative_addr)] = pcic_old;
		}
		break;

	case SH4_PCILAR1:
		/*  Hardcoded to what OpenBSD/landisk uses:  */
		if (writeflag == MEM_WRITE && idata != 0xac000000) {
			if (sh4_pcic_first(d, relative_addr, SH4_PCIC_BADVAL))
				fatal("[ sh4_pcic: SH4_PCILAR1 unknown value"
				    " 0x%" PRIx32" -- ignored."
				    "  (once per offset) ]\n",
				    (uint32_t) idata);
			d->pcic_reg[PCIC_REG(relative_addr)] = pcic_old;
		}
		break;

	case SH4_PCIMBR:
		if (writeflag == MEM_WRITE && idata != SH4_PCIC_MEM) {
			if (sh4_pcic_first(d, relative_addr, SH4_PCIC_BADVAL))
				fatal("[ sh4_pcic: PCIMBR set to 0x%" PRIx32
				    ", not 0x%" PRIx32" -- ignored."
				    "  (once per offset) ]\n",
				    (uint32_t) idata,
				    (uint32_t) SH4_PCIC_MEM);
			d->pcic_reg[PCIC_REG(relative_addr)] = pcic_old;
		}
		break;

	case SH4_PCIIOBR:
		if (writeflag == MEM_WRITE && idata != SH4_PCIC_IO) {
			if (sh4_pcic_first(d, relative_addr, SH4_PCIC_BADVAL))
				fatal("[ sh4_pcic: PCIIOBR set to 0x%" PRIx32
				    ", not 0x%" PRIx32" -- ignored."
				    "  (once per offset) ]\n",
				    (uint32_t) idata,
				    (uint32_t) SH4_PCIC_IO);
			d->pcic_reg[PCIC_REG(relative_addr)] = pcic_old;
		}
		break;

	case SH4_PCIPAR:
		/*  PCI bus access Address Register:  */
		{
			int bus  = (idata >> 16) & 0xff;
			int dev  = (idata >> 11) & 0x1f;
			int func = (idata >>  8) &    7;
			int reg  =  idata        & 0xff;
			bus_pci_setaddr(cpu, d->pci_data, bus, dev, func, reg);
		}
		break;

	case SH4_PCIPDR:
		/*  PCI bus access Data Register:  */
		bus_pci_data_access(cpu, d->pci_data, writeflag == MEM_READ?
		    &odata : &idata, len, writeflag);
		break;

	default:/*  #443: an offset this device does not implement.  Reads answer 0 and
		    writes are dropped -- deliberately NOT "let pcic_reg[] act as
		    anonymous storage", which would invent read/write registers that
		    no modelled behaviour consumes and let a guest build state
		    meaning nothing.  Zero-and-ignore is deterministic and has no
		    side effect.  */
		if (sh4_pcic_first(d, relative_addr, SH4_PCIC_UNIMPL)) {
			if (writeflag == MEM_READ)
				fatal("[ sh4_pcic: read from unimplemented"
				    " addr 0x%x -- reads as zero."
				    "  (once per offset) ]\n",
				    (int)relative_addr);
			else
				fatal("[ sh4_pcic: write to unimplemented"
				    " addr 0x%x: 0x%x -- ignored."
				    "  (once per offset) ]\n",
				    (int)relative_addr, (int)idata);
		}
		d->pcic_reg[PCIC_REG(relative_addr)] = pcic_old;
		odata = 0;
		break;
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}


DEVICE_ACCESS(sh4_sq)
{
	struct sh4_data *d = (struct sh4_data *) extra;
	size_t i;

	if (writeflag == MEM_WRITE) {
		for (i=0; i<len; i++)
			d->sq[(relative_addr + i) % sizeof(d->sq)] = data[i];
	} else {
		for (i=0; i<len; i++)
			data[i] = d->sq[(relative_addr + i) % sizeof(d->sq)];
	}

	return 1;
}


/*
 *  #441: BCR2 and BCR3 are 16-bit registers, and the committed code answered a
 *  guest access of any other width with fatal() + exit(1) -- so TWO GUEST
 *  INSTRUCTIONS ended the emulator, taking every emulated process and any
 *  unflushed disk overlay with them.  Reproduced at rung 3 on an unmodified
 *  in-tree landisk: a mov.l to 0xff800004 killed the host, while the SAME
 *  4-byte width to BCR1 four bytes away survived, because BCR1 has no length
 *  check.  The kill was the width test, not the device.
 *
 *  Fixed in the #438 shape: keep the diagnostic, drop the exit(1), service the
 *  access.  Servicing rather than ignoring is deliberate for an access that
 *  COVERS the register: these two were the only length checks in the file, and
 *  PCR/RTCSR/RTCNT/RTCOR/RFCR (all "16bit" in sh4_bscreg.h) already accept any
 *  width and service it.  A real boot reads BCR2 three times and BCR3 once,
 *  all at the legal width, so a correct guest sees no change at all.
 *
 *  TWO LIMITS, both measured by a pass-2 seat and stated rather than papered
 *  over.  (1) A PARTIAL access -- len 1 -- is dropped, so from the second one
 *  onward these registers DO silently swallow a write, and free-running the
 *  demoted line is invisible because debug() computes v = verbose - 1 = -1 and
 *  returns.  An earlier draft of this comment argued against exactly that
 *  behaviour while the code implemented it.  (2) The precedent registers named
 *  above resolve BE lanes the OTHER way (they take the last two bytes of a
 *  wide access, not the first) and they PROMOTE a 1-byte write rather than
 *  dropping it, so this fix cites them for the principle and then differs from
 *  them on both axes.  Tracked as `sh4bsclane`; not reopened here, because one
 *  round takes one site and there is no SH-4 document in this tree to settle
 *  which convention is right.
 */
static unsigned int sh4_bsc16_shift(struct cpu *cpu, size_t len)
{
	/*  Which bits of a len-byte access are the register's own two?
	    memory_rw hands the WHOLE access to one handler (measured: one call,
	    len=4, never split -- the 1024-byte page split cannot fire on a
	    4-byte aligned access), so the byte lanes are ours to resolve.  The
	    case label matched relative_addr exactly, so the register is always
	    the FIRST two bytes: bits [15:0] little-endian, the top halfword big.

	    The len <= 2 term must not be "simplified" away: len is a size_t, so
	    8 * (len - 2) at len == 1 shifts by SIZE_MAX*8.  || short-circuits, so
	    the subtraction is never evaluated for a short access.

	    HONEST SCOPE, because an earlier draft of this comment overstated it
	    and a review seat measured the overstatement: a 1-byte guest access IS
	    reachable, but it never reaches THIS function -- sh4_bsc16_report()
	    returns 0 for a partial access and the case arm breaks first.  The
	    guard is defensive, not load-bearing today.  It is kept because the
	    two are one edit apart, and a capitalised claim of reachability the
	    code prevents is a records defect either way.  */
	if (len <= sizeof(uint16_t) || cpu->byte_order != EMUL_BIG_ENDIAN)
		return 0;
	return 8 * (unsigned int) (len - sizeof(uint16_t));
}


static int sh4_bsc16_report(struct sh4_data *d, int site, const char *name,
	int writeflag, size_t len)
{
	int partial;

	if (len == sizeof(uint16_t))
		return 1;

	/*  A PARTIAL access does not cover the register, so it is diagnosed and
	    NOT serviced -- servicing it would let a 1-byte store overwrite both
	    halves.  Written the other way round first, and the D3 detector row
	    caught it on the first run: a byte write of 0xa5 left the register
	    holding 0xa5 instead of its reset 0x3ffc.  That is exactly the mutant
	    a pass-1 seat had predicted and written D3 against.  */
	partial = len < sizeof(uint16_t);

	/*  LATCHED, and per site.  fatal() is NOT debug(): debug() returns early
	    under quiet_mode, fatal() has no such early-out, so an unlatched
	    complaint here could not be silenced even with -q.  A real
	    OpenBSD/landisk boot makes ZERO non-16-bit BSC accesses (measured),
	    so the latch costs a correct guest nothing and bounds a hostile one.

	    THE ORACLE FOR THIS IS NOT THE REGISTER NAME.  A detector row that
	    asked "does the string BCR3 appear?" was passed by a mutant sharing
	    one flag between the sites, because the demoted debug() prints the
	    same name -- and under the cold debugger single_step is true, so
	    debug()'s quiet_mode early-out never fires and a probe cannot tell
	    fatal() from debug() by presence at all.  Count the latched suffix.  */
	if (!d->bsc16_reported[site]) {
		d->bsc16_reported[site] = 1;
		fatal("[ sh4: %i-byte %s of SH4_%s; it is a 16-bit register."
		    "  %s.  (reported once per register) ]\n",
		    (int) len, writeflag == MEM_WRITE ? "write" : "read", name,
		    partial ? "Ignored" : "Servicing its own two bytes");
	} else {
		debug("[ sh4: %i-byte %s of SH4_%s ]\n", (int) len,
		    writeflag == MEM_WRITE ? "write" : "read", name);
	}

	return !partial;
}


/*
 *  sh4_val_first():
 *
 *  Non-zero the first time any of `bits` is reported for (cls, instance); records
 *  them either way.  `bits` is the OFFENDING bits, not the whole written value --
 *  passing the value would make every distinct write look like a fresh complaint and
 *  hand a looping guest an unbounded host-CPU burn, which is the thing this latch is
 *  here to prevent.
 */
static int sh4_val_first(struct sh4_data *d, int cls, int instance, uint32_t bits)
{
	uint32_t fresh;

	/*  Unreachable by construction: every caller passes a class from the SH4_VAL_*
	    list and an instance bounded by its own `case` fall-through.  Kept because
	    getting it wrong would be an out-of-bounds WRITE, not a wrong message, and
	    because it is free.  It SILENCES rather than reports, matching
	    sh4_pcic_first(); an unbounded key must not become an unbounded print.  */
	if (cls < 0 || cls >= SH4_VAL_NCLASS ||
	    instance < 0 || instance >= N_SH4_VAL_INST)
		return 0;

	fresh = bits & ~d->val_reported[cls][instance];
	d->val_reported[cls][instance] |= bits;

	return fresh != 0;
}


/*
 *  #447: four value guards in the switch below ended the host process with exit(1) on
 *  ONE ordinary guest store -- TCR, DMATCR, ICR and RCR1.  MEASURED on an unmodified
 *  -E landisk, each with a matched surviving control at the SAME address and the SAME
 *  width, so it is the VALUE that kills and not the address or the access width.
 *
 *  Fixed in the #438/#441/#443 shape -- keep the diagnostic, drop the exit(1), ignore
 *  the write -- and the four arms differ in a way that is invisible at the call site:
 *
 *    RCR1    the store was UPSTREAM of the guard.  Dropping exit(1) alone would have
 *            turned a host kill into SILENT STATE CORRUPTION.  Moved below the guard.
 *    TCR     `timer_hz` was set from `idata & 3` BEFORE the guard and the debug() line
 *            had already announced it, so the naive fix installs a timer frequency the
 *            guest never asked for.  The guard moved ABOVE the prescaler switch.
 *    DMATCR  the store is already downstream; nothing to move.
 *    ICR     nothing is stored on any path, so there is no state to corrupt.
 *
 *  Saying "the store is upstream" once for the file would have been wrong three times
 *  out of four.  Check it per site.
 */
DEVICE_ACCESS(sh4)
{
	struct sh4_data *d = (struct sh4_data *) extra;
	uint64_t idata = 0, odata = 0;
	int timer_nr = 0, dma_channel = 0;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	relative_addr += SH4_REG_BASE;

	/*  SD-RAM access uses address only:  */
	if (relative_addr >= 0xff900000 && relative_addr <= 0xff97ffff) {
		/*  Possibly not 100% correct... TODO  */
		int v = (relative_addr >> 2) & 0xffff;
		if (relative_addr & 0x00040000)
			d->sdmr3 = v;
		else
			d->sdmr2 = v;
		debug("[ sh4: sdmr%i set to 0x%04" PRIx16" ]\n",
		    relative_addr & 0x00040000? 3 : 2, v);
		return 1;
	}


	switch (relative_addr) {

	/*************************************************/

	case SH4_PVR_ADDR:
		odata = cpu->cd.sh.cpu_type.pvr;
		break;

	case SH4_PRR_ADDR:
		odata = cpu->cd.sh.cpu_type.prr;
		break;

	case SH4_PTEH:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.pteh;
		else {
			unsigned int old_asid = cpu->cd.sh.pteh
			    & SH4_PTEH_ASID_MASK;
			cpu->cd.sh.pteh = idata;

			if ((idata & SH4_PTEH_ASID_MASK) != old_asid) {
				/*
				 *  TODO: Don't invalidate everything,
				 *  only those pages that belonged to the
				 *  old asid.
				 */
				cpu->invalidate_translation_caches(
				    cpu, 0, INVALIDATE_ALL);
			}
		}
		break;

	case SH4_PTEL:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.ptel;
		else
			cpu->cd.sh.ptel = idata;
		break;

	case SH4_TTB:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.ttb;
		else
			cpu->cd.sh.ttb = idata;
		break;

	case SH4_TEA:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.tea;
		else
			cpu->cd.sh.tea = idata;
		break;

	case SH4_PTEA:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.ptea;
		else
			cpu->cd.sh.ptea = idata;
		break;

	case SH4_MMUCR:
		if (writeflag == MEM_READ) {
			odata = cpu->cd.sh.mmucr;
		} else {
			if (idata & SH4_MMUCR_TI) {
				/*  TLB invalidate.  */
				int i;
				for (i = 0; i < SH_N_ITLB_ENTRIES; i++)
					cpu->cd.sh.itlb_lo[i] &=
					    ~SH4_PTEL_V;

				for (i = 0; i < SH_N_UTLB_ENTRIES; i++)
					cpu->cd.sh.utlb_lo[i] &=
					    ~SH4_PTEL_V;

				cpu->invalidate_translation_caches(cpu,
				    0, INVALIDATE_ALL);

				/*  The TI bit should always read as 0.  */
				idata &= ~SH4_MMUCR_TI;
			}

			cpu->cd.sh.mmucr = idata;
		}
		break;

	case SH4_CCR:
		if (writeflag == MEM_READ) {
			odata = cpu->cd.sh.ccr;
		} else {
			cpu->cd.sh.ccr = idata;
		}
		break;

	case SH4_QACR0:
		if (writeflag == MEM_READ) {
			odata = cpu->cd.sh.qacr0;
		} else {
			cpu->cd.sh.qacr0 = idata;
		}
		break;

	case SH4_QACR1:
		if (writeflag == MEM_READ) {
			odata = cpu->cd.sh.qacr1;
		} else {
			cpu->cd.sh.qacr1 = idata;
		}
		break;

	case SH4_TRA:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.tra;
		else
			cpu->cd.sh.tra = idata;
		break;

	case SH4_EXPEVT:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.expevt;
		else
			cpu->cd.sh.expevt = idata;
		break;

	case SH4_INTEVT:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.intevt;
		else
			cpu->cd.sh.intevt = idata;
		break;


	/********************************/
	/*  UBC: User Break Controller  */

	case 0xff000014:    /*  SH4_UBC_BASRA  */
	case 0xff000018:    /*  SH4_UBC_BASRB  */

	case 0xff200000:    /*  SH4_UBC_BARA  */
	case 0xff200004:    /*  SH4_UBC_BAMRA  */
	case 0xff200008:    /*  SH4_UBC_BBRA  */
	case 0xff20000c:    /*  SH4_UBC_BARB  */
	case 0xff200010:    /*  SH4_UBC_BAMRB  */
	case 0xff200014:    /*  SH4_UBC_BBRB  */
	case 0xff200018:    /*  SH4_UBC_BDRB  */
	case 0xff20001c:    /*  SH4_UBC_BDMRB  */
	case 0xff200020:    /*  SH4_UBC_BRCR  */
		/*  TODO  */
		break;


	/********************************/
	/*  TMU: Timer Management Unit  */

	case SH4_TOCR:
		/*  Timer Output Control Register  */
		if (writeflag == MEM_WRITE) {
			d->tocr = idata;
			if (idata & TOCR_TCOE)
				fatal("[ sh4 timer: TCOE not yet "
				    "implemented ]\n");
		} else {
			odata = d->tocr;
		}
		break;

	case SH4_TSTR:
		/*  Timer Start Register  */
		if (writeflag == MEM_READ) {
			odata = d->tstr;
		} else {
			if (idata & 1 && !(d->tstr & 1))
				debug("[ sh4 timer: starting timer 0 ]\n");
			if (idata & 2 && !(d->tstr & 2))
				debug("[ sh4 timer: starting timer 1 ]\n");
			if (idata & 4 && !(d->tstr & 4))
				debug("[ sh4 timer: starting timer 2 ]\n");
			if (!(idata & 1) && d->tstr & 1)
				debug("[ sh4 timer: stopping timer 0 ]\n");
			if (!(idata & 2) && d->tstr & 2)
				debug("[ sh4 timer: stopping timer 1 ]\n");
			if (!(idata & 4) && d->tstr & 4)
				debug("[ sh4 timer: stopping timer 2 ]\n");
			d->tstr = idata;
		}
		break;

	case SH4_TCOR2:
		timer_nr ++;
		// fall through
	case SH4_TCOR1:
		timer_nr ++;
		// fall through
	case SH4_TCOR0:
		/*  Timer Constant Register  */
		if (writeflag == MEM_READ)
			odata = d->tcor[timer_nr];
		else
			d->tcor[timer_nr] = idata;
		break;

	case SH4_TCNT2:
		timer_nr ++;
		// fall through
	case SH4_TCNT1:
		timer_nr ++;
		// fall through
	case SH4_TCNT0:
		/*  Timer Counter Register  */
		if (writeflag == MEM_READ)
			odata = d->tcnt[timer_nr];
		else
			d->tcnt[timer_nr] = idata;
		break;

	case SH4_TCR2:
		timer_nr ++;
		// fall through
	case SH4_TCR1:
		timer_nr ++;
		// fall through
	case SH4_TCR0:
		/*  Timer Control Register  */
		if (writeflag == MEM_READ) {
			odata = d->tcr[timer_nr];
		} else {
			if (cpu->cd.sh.pclock == 0) {
				fatal("INTERNAL ERROR: pclock must be set"
				    " for this machine. Aborting.\n");
				exit(1);
			}

			/*
			 *  #447: THIS GUARD MOVED UP, above the prescaler switch,
			 *  and that is not tidy-up.  It used to sit below, by which
			 *  time `timer_hz` had already been set from `idata & 3` --
			 *  a divisor the guest did not ask for, because TPSC2 selects
			 *  a clock source outside the two bits that switch decodes --
			 *  and the debug() line had already announced it.  exit(1)
			 *  hid that.  Drop the exit and leave the guard where it was
			 *  and the write installs a WRONG timer frequency instead,
			 *  which is a silent fault where the old one was loud.
			 *
			 *  The whole write is rejected, not just the bits we do not
			 *  model: substituting a prescaler for a clock source we
			 *  cannot provide would be inventing a rate.  The guest can
			 *  see the rejection by reading TCR back.
			 *
			 *  `break` leaves the enclosing switch (relative_addr) -- no
			 *  loop or inner switch is open at this point -- so nothing
			 *  below runs and no state is touched.
			 */
			if (idata & TCR_UNIMPLEMENTED) {
				if (sh4_val_first(d, SH4_VAL_TCRBITS, timer_nr,
				    (uint32_t) (idata & TCR_UNIMPLEMENTED)))
					fatal("[ sh4: timer %i: unimplemented TCR"
					    " bits 0x%04x -- write ignored."
					    "  (once per bit) ]\n", timer_nr,
					    (int) (idata & TCR_UNIMPLEMENTED));
				break;
			}

			switch (idata & 3) {
			case TCR_TPSC_P4:
				d->timer_hz[timer_nr] = cpu->cd.sh.pclock/4.0;
				break;
			case TCR_TPSC_P16:
				d->timer_hz[timer_nr] = cpu->cd.sh.pclock/16.0;
				break;
			case TCR_TPSC_P64:
				d->timer_hz[timer_nr] = cpu->cd.sh.pclock/64.0;
				break;
			case TCR_TPSC_P256:
				d->timer_hz[timer_nr] = cpu->cd.sh.pclock/256.0;
				break;
			}

			debug("[ sh4 timer %i clock set to %f Hz ]\n",
			    timer_nr, d->timer_hz[timer_nr]);

			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);

			if (d->tcr[timer_nr] & TCR_UNF && !(idata & TCR_UNF)) {
				if (d->timer_interrupts_pending[timer_nr] > 0)
					d->timer_interrupts_pending[timer_nr]--;
			}

			d->tcr[timer_nr] = idata;
		}
		break;


	/*************************************************/
	/*  DMAC: DMA Controller                         */
	/*  4 channels on SH7750                         */
	/*  8 channels on SH7760                         */

	case SH4_SAR7:	dma_channel ++;
			// fall through
	case SH4_SAR6:	dma_channel ++;
			// fall through
	case SH4_SAR5:	dma_channel ++;
			// fall through
	case SH4_SAR4:	dma_channel ++;
			// fall through
	case SH4_SAR3:	dma_channel ++;
			// fall through
	case SH4_SAR2:	dma_channel ++;
			// fall through
	case SH4_SAR1:	dma_channel ++;
			// fall through
	case SH4_SAR0:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.dmac_sar[dma_channel];
		else
			cpu->cd.sh.dmac_sar[dma_channel] = idata;
		break;

	case SH4_DAR7:	dma_channel ++;
			// fall through
	case SH4_DAR6:	dma_channel ++;
			// fall through
	case SH4_DAR5:	dma_channel ++;
			// fall through
	case SH4_DAR4:	dma_channel ++;
			// fall through
	case SH4_DAR3:	dma_channel ++;
			// fall through
	case SH4_DAR2:	dma_channel ++;
			// fall through
	case SH4_DAR1:	dma_channel ++;
			// fall through
	case SH4_DAR0:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.dmac_dar[dma_channel];
		else
			cpu->cd.sh.dmac_dar[dma_channel] = idata;
		break;

	case SH4_DMATCR7: dma_channel ++;
			// fall through
	case SH4_DMATCR6: dma_channel ++;
			// fall through
	case SH4_DMATCR5: dma_channel ++;
			// fall through
	case SH4_DMATCR4: dma_channel ++;
			// fall through
	case SH4_DMATCR3: dma_channel ++;
			// fall through
	case SH4_DMATCR2: dma_channel ++;
			// fall through
	case SH4_DMATCR1: dma_channel ++;
			// fall through
	case SH4_DMATCR0:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.dmac_tcr[dma_channel] & 0x00ffffff;
		else {
			/*
			 *  #447: the store below is DOWNSTREAM of this guard, so
			 *  dropping exit(1) already rejects the value -- unlike RCR1
			 *  and unlike every arm of dev_sh4_pcic_access(), where the
			 *  store runs first and a restore is needed.  Recorded because
			 *  the difference is invisible at the call site and a reader
			 *  generalising from #443 would add a restore that is not
			 *  merely redundant but wrong.
			 *
			 *  A GUEST READ-BACK CANNOT SEE THIS REJECTION BY ITSELF: the
			 *  read arm above masks with 0x00ffffff, so the top bits are
			 *  invisible whether they were stored or not.  The consumer
			 *  that would see them is sh4_dmac_transfer(), which masks with
			 *  0x1fffffff -- FIVE BITS WIDER than the read arm.  A detector
			 *  row here has to compare the LOW 24 bits against a value the
			 *  device accepted earlier; a plain read-back is vacuous.
			 */
			if (idata & ~0x00ffffff) {
				if (sh4_val_first(d, SH4_VAL_DMATCR, dma_channel,
				    (uint32_t) ((idata >> 24) & 0xff)))
					fatal("[ sh4: DMA channel %i: transfer"
					    " count 0x%08" PRIx32" exceeds 24"
					    " bits -- write ignored."
					    "  (once per bit) ]\n", dma_channel,
					    (uint32_t) idata);
			} else
				cpu->cd.sh.dmac_tcr[dma_channel] = idata;
		}
		break;

	case SH4_CHCR7:	dma_channel ++;
			// fall through
	case SH4_CHCR6:	dma_channel ++;
			// fall through
	case SH4_CHCR5:	dma_channel ++;
			// fall through
	case SH4_CHCR4:	dma_channel ++;
			// fall through
	case SH4_CHCR3:	dma_channel ++;
			// fall through
	case SH4_CHCR2:	dma_channel ++;
			// fall through
	case SH4_CHCR1:	dma_channel ++;
			// fall through
	case SH4_CHCR0:
		if (writeflag == MEM_READ) {
			odata = cpu->cd.sh.dmac_chcr[dma_channel];
		} else {
			/*  CHCR_CHSET always reads back as 0:  */
			idata &= ~CHCR_CHSET;

			cpu->cd.sh.dmac_chcr[dma_channel] = idata;

			/*  Perform a transfer?  */
			if (idata & CHCR_TD)
				sh4_dmac_transfer(cpu, d, dma_channel);
		}
		break;

	case SH4_DMAOR:
		if (writeflag == MEM_READ) {
			odata = cpu->cd.sh.dmaor;
		} else {
			// Only some bits are writable:
			idata &= (DMAOR_DDT | DMAOR_PR1 | DMAOR_PR0 | DMAOR_DME);
			cpu->cd.sh.dmaor = idata;
		}
		break;

	/*************************************************/
	/*  BSC: Bus State Controller                    */

	case SH4_BCR1:
		if (writeflag == MEM_WRITE)
			d->bsc_bcr1 = idata & 0x033efffd;
		else {
			odata = d->bsc_bcr1;
			if (cpu->byte_order == EMUL_LITTLE_ENDIAN)
				odata |= BCR1_LITTLE_ENDIAN;
		}
		break;

	case SH4_BCR2:
		if (!sh4_bsc16_report(d, 0, "BCR2", writeflag, len))
			break;
		if (writeflag == MEM_WRITE)
			d->bsc_bcr2 = (idata >> sh4_bsc16_shift(cpu, len))
			    & 0x3ffd;
		else
			odata = (uint64_t) d->bsc_bcr2
			    << sh4_bsc16_shift(cpu, len);
		break;

	case SH4_BCR3:
		if (!sh4_bsc16_report(d, 1, "BCR3", writeflag, len))
			break;
		if (writeflag == MEM_WRITE)
			d->bsc_bcr3 = (idata >> sh4_bsc16_shift(cpu, len));
		else
			odata = (uint64_t) d->bsc_bcr3
			    << sh4_bsc16_shift(cpu, len);
		break;

	case SH4_WCR1:
		if (writeflag == MEM_WRITE)
			d->bsc_wcr1 = idata & 0x77777777;
		else
			odata = d->bsc_wcr1;
		break;

	case SH4_WCR2:
		if (writeflag == MEM_WRITE)
			d->bsc_wcr2 = idata & 0xfffeefff;
		else
			odata = d->bsc_wcr2;
		break;

	case SH4_WCR3:
		if (writeflag == MEM_WRITE)
			d->bsc_wcr3 = idata & 0x77777777;
		else
			odata = d->bsc_wcr3;
		break;

	case SH4_MCR:
		if (writeflag == MEM_WRITE)
			d->bsc_mcr = idata & 0xf8bbffff;
		else
			odata = d->bsc_mcr;
		break;

	case SH4_PCR:
		if (writeflag == MEM_WRITE)
			d->bsc_pcr = idata;
		else
			odata = d->bsc_pcr;
		break;

	case SH4_RTCSR:
		/*
		 *  Refresh Time Control/Status Register. Called RTCSR in
		 *  NetBSD, but RTSCR in the SH7750 manual?
		 */
		if (writeflag == MEM_WRITE) {
			idata &= 0x00ff;
			if (idata & RTCSR_CMF) {
				idata = (idata & ~RTCSR_CMF)
				    | (d->bsc_rtcsr & RTCSR_CMF);
			}
			d->bsc_rtcsr = idata & 0x00ff;
		} else
			odata = d->bsc_rtcsr;
		break;

	case SH4_RTCOR:
		/*  Refresh Time Constant Register (8 bits):  */
		if (writeflag == MEM_WRITE)
			d->bsc_rtcor = idata & 0x00ff;
		else
			odata = d->bsc_rtcor & 0x00ff;
		break;

	case SH4_RFCR:
		/*  Refresh Count Register (10 bits):  */
		if (writeflag == MEM_WRITE)
			d->bsc_rfcr = idata & 0x03ff;
		else
			odata = d->bsc_rfcr & 0x03ff;
		break;


	/*******************************************/
	/*  GPIO:  General-purpose I/O controller  */

	case SH4_PCTRA:
		if (writeflag == MEM_WRITE) {
			d->pctra = idata;
			
			// Hack: Makes the Dreamcast BIOS pass "cable select"
			// detection, it seems, without hanging in an endless
			// loop.
			d->pdtra |= 0x03;
		} else {
			odata = d->pctra;
		}
		break;

	case SH4_PDTRA:
		if (writeflag == MEM_WRITE) {
			// debug("[ sh4: pdtra: write 0x%08x (while pctra = 0x%08x) ]\n", (int)idata, (int)d->pctra);
			d->pdtra = idata;

			// Hack: Makes the Dreamcast BIOS pass "cable select"
			// detection, it seems, without hanging in an endless
			// loop.
			if ((idata & 1) == 0 || (idata & 2) == 0)
				d->pdtra &= ~3;
		} else {
			// debug("[ sh4: pdtra: read ]\n");
			odata = d->pdtra;

			// bits 8..9 on Dreamcast mean:
			//  00 = VGA, 10 = RGB, 11 = composite.
			odata |= (0 << 8);
		}
		break;

	case SH4_PCTRB:
		if (writeflag == MEM_WRITE)
			d->pctrb = idata;
		else
			odata = d->pctrb;
		break;

	case SH4_PDTRB:
		if (writeflag == MEM_WRITE) {
			debug("[ sh4: pdtrb: write: TODO ]\n");
			d->pdtrb = idata;
		} else {
			debug("[ sh4: pdtrb: read: TODO ]\n");
			odata = d->pdtrb;
		}
		break;

	case SH4_GPIOIC:
		if (writeflag == MEM_WRITE)
			d->bsc_gpioic = idata;
		else
			odata = d->bsc_gpioic;
		break;


	/****************************/
	/*  SCI:  Serial Interface  */

	case SHREG_SCSPTR:
		odata = sh4_sci_access(d, cpu,
		    writeflag == MEM_WRITE? 1 : 0, idata);

		/*
		 *  TODO
		 *
		 *  Find out the REAL way to make OpenBSD/landisk 4.1 run
		 *  in a stable manner! This is a SUPER-UGLY HACK which
		 *  just side-steps the real bug.
		 *
		 *  NOTE:  Snapshots of OpenBSD/landisk _after_ 4.1 seem
		 *  to work WITHOUT this hack, but NOT with it!
		 */
		cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);

		break;


	/*********************************/
	/*  INTC:  Interrupt Controller  */

	case SH4_ICR:
		/*
		 *  #447: ICR is not modelled on ANY path -- no arm of this case
		 *  stores anything, and a read answers the odata this function was
		 *  entered with, i.e. 0.  So there is no state to corrupt and none
		 *  to restore, and a detector row that writes ICR and reads it back
		 *  is VACUOUS here by construction: it answers 0 before the fix,
		 *  after it, and under every mutant.  The diagnostic is the only
		 *  observable this arm has.
		 */
		if (writeflag == MEM_WRITE && (idata & 0x80)) {
			if (sh4_val_first(d, SH4_VAL_ICRIRLM, 0,
			    (uint32_t) (idata & 0x80)))
				fatal("[ sh4: INTC: ICR IRLM bit 0x%04x not"
				    " implemented -- write ignored."
				    "  (once per bit) ]\n", (int) (idata & 0x80));
		}
		break;

	case SH4_IPRA:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.intc_ipra;
		else {
			cpu->cd.sh.intc_ipra = idata;
			sh_update_interrupt_priorities(cpu);
		}
		break;

	case SH4_IPRB:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.intc_iprb;
		else {
			cpu->cd.sh.intc_iprb = idata;
			sh_update_interrupt_priorities(cpu);
		}
		break;

	case SH4_IPRC:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.intc_iprc;
		else {
			cpu->cd.sh.intc_iprc = idata;
			sh_update_interrupt_priorities(cpu);
		}
		break;

	case SH4_IPRD:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.intc_iprd;
		else {
			cpu->cd.sh.intc_iprd = idata;
			sh_update_interrupt_priorities(cpu);
		}
		break;

	case SH4_INTPRI00:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.intc_intpri00;
		else {
			cpu->cd.sh.intc_intpri00 = idata;
			sh_update_interrupt_priorities(cpu);
		}
		break;

	case SH4_INTPRI00 + 4:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.intc_intpri04;
		else {
			cpu->cd.sh.intc_intpri04 = idata;
			sh_update_interrupt_priorities(cpu);
		}
		break;

	case SH4_INTPRI00 + 8:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.intc_intpri08;
		else {
			cpu->cd.sh.intc_intpri08 = idata;
			sh_update_interrupt_priorities(cpu);
		}
		break;

	case SH4_INTPRI00 + 0xc:
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.intc_intpri0c;
		else {
			cpu->cd.sh.intc_intpri0c = idata;
			sh_update_interrupt_priorities(cpu);
		}
		break;

	case SH4_INTMSK00:
		/*  Note: Writes can only set bits, not clear them.  */
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.intc_intmsk00;
		else
			cpu->cd.sh.intc_intmsk00 |= idata;
		break;

	case SH4_INTMSK00 + 4:
		/*  Note: Writes can only set bits, not clear them.  */
		if (writeflag == MEM_READ)
			odata = cpu->cd.sh.intc_intmsk04;
		else
			cpu->cd.sh.intc_intmsk04 |= idata;
		break;

	case SH4_INTMSKCLR00:
		/*  Note: Writes can only clear bits, not set them.  */
		if (writeflag == MEM_WRITE)
			cpu->cd.sh.intc_intmsk00 &= ~idata;
		break;

	case SH4_INTMSKCLR00 + 4:
		/*  Note: Writes can only clear bits, not set them.  */
		if (writeflag == MEM_WRITE)
			cpu->cd.sh.intc_intmsk04 &= ~idata;
		break;


	/*************************************************/
	/*  SCIF: Serial Controller Interface with FIFO  */

	case SH4_SCIF_BASE + SCIF_SMR:
		if (writeflag == MEM_WRITE) {
			d->scif_smr = idata;
		} else {
			odata = d->scif_smr;
		}
		break;

	case SH4_SCIF_BASE + SCIF_BRR:
		if (writeflag == MEM_WRITE) {
			d->scif_brr = idata;
		} else {
			odata = d->scif_brr;
		}
		break;

	case SH4_SCIF_BASE + SCIF_SCR:
		if (writeflag == MEM_WRITE) {
			d->scif_scr = idata;
			scif_reassert_interrupts(d);
		} else {
			odata = d->scif_scr;
		}
		break;

	case SH4_SCIF_BASE + SCIF_FTDR:
		if (writeflag == MEM_WRITE) {
			/*  Add to TX fifo:  */
			if (d->scif_tx_fifo_cursize >=
			    sizeof(d->scif_tx_fifo)) {
				fatal("[ SCIF TX fifo overrun! ]\n");
				d->scif_tx_fifo_cursize = 0;
			}

			d->scif_tx_fifo[d->scif_tx_fifo_cursize++] = idata;
			d->scif_delayed_tx = SCIF_DELAYED_TX_VALUE;
		}
		break;

	case SH4_SCIF_BASE + SCIF_SSR:
		if (writeflag == MEM_READ) {
			odata = d->scif_ssr;
		} else {
			d->scif_ssr = idata;
			scif_reassert_interrupts(d);
		}
		break;

	case SH4_SCIF_BASE + SCIF_FRDR:
		{
			int x = console_readchar(d->scif_console_handle);
			if (x == 13)
				x = 10;
			odata = x < 0? 0 : x;
			if (console_charavail(d->scif_console_handle))
				d->scif_ssr |= SCSSR2_DR;
			else
				d->scif_ssr &= ~SCSSR2_DR;
			scif_reassert_interrupts(d);
		}
		break;

	case SH4_SCIF_BASE + SCIF_FCR:
		if (writeflag == MEM_WRITE) {
			d->scif_fcr = idata;
		} else {
			odata = d->scif_fcr;
		}
		break;

	case SH4_SCIF_BASE + SCIF_FDR:
		/*  Nr of bytes in the TX and RX fifos, respectively:  */
		{
			int chars_avail = console_charavail(d->scif_console_handle);
			if (chars_avail > 255) {
				fatal("[ SH4: Too many chars avail; dropping some ]\n");
				chars_avail = 255;
			}
			
			odata = chars_avail | (d->scif_tx_fifo_cursize << 8);
		}
		break;

	case SH4_SCIF_BASE + SCIF_SPTR:
		/*  TODO: Implement all bits.  */
		odata = 0;
		break;

	case SH4_SCIF_BASE + SCIF_LSR:
		/*  TODO: Implement all bits.  */
		odata = 0;
		break;


	/*************************************************/

	case SH4_CPG_FRQCR:	// 0xffc00000	16-bit
		if (writeflag == MEM_WRITE)
			d->cpg_frqcr = idata;
		else
			odata = d->cpg_frqcr;
		break;

	case SH4_CPG_STBCR: 	// 0xffc00004	8-bit
		if (writeflag == MEM_WRITE)
			d->cpg_stbcr = idata;
		else
			odata = d->cpg_stbcr;
		break;

	case SH4_CPG_WTCNT:	// 0xffc00008	8/16-bit
		if (writeflag == MEM_WRITE)
			d->cpg_wtcnt = idata;
		else
			odata = d->cpg_wtcnt;
		break;

	case SH4_CPG_WTCSR:	// 0xffc0000c	8/16-bit
		if (writeflag == MEM_WRITE)
			d->cpg_wtcsr = idata;
		else
			odata = d->cpg_wtcsr;
		break;

	case SH4_CPG_STBCR2:	// 0xffc00010	8-bit
		if (writeflag == MEM_WRITE)
			d->cpg_stbcr2 = idata;
		else
			odata = d->cpg_stbcr2;
		break;


	/*************************************************/

	case SH4_RSECCNT:
	case SH4_RMINCNT:
	case SH4_RHRCNT:
	case SH4_RWKCNT:
	case SH4_RDAYCNT:
	case SH4_RMONCNT:
	case SH4_RYRCNT:
	case SH4_RSECAR:
	case SH4_RMINAR:
	case SH4_RHRAR:
	case SH4_RWKAR:
	case SH4_RDAYAR:
	case SH4_RMONAR:
		if (writeflag == MEM_WRITE) {
			d->rtc_reg[(relative_addr - 0xffc80000) / 4] = idata;
		} else {
			/*  TODO: Update rtc_reg based on host's date/time.  */
			odata = d->rtc_reg[(relative_addr - 0xffc80000) / 4];
		}
		break;

	case SH4_RCR1:
		if (writeflag == MEM_READ)
			odata = d->rtc_rcr1;
		else {
			/*
			 *  #447: *** THE STORE WAS UPSTREAM OF THE GUARD. ***  It ran
			 *  first and the guard second, so a rejected value had ALREADY
			 *  landed in rtc_rcr1 and exit(1) was the only thing stopping
			 *  the guest reading it back.  Dropping the exit and nothing
			 *  else turns a host kill into SILENT STATE CORRUPTION -- the
			 *  guest writes CIE|AIE, reads CIE|AIE back, and believes the
			 *  RTC will interrupt it.  It never will.  Same shape as #443
			 *  found in dev_sh4_pcic_access(), and the ONLY one of #447's
			 *  four sites that has it.  The store therefore moved below.
			 *
			 *  The mask is spelled from the header (thirdparty/sh4_rtcreg.h
			 *  :72-73) rather than as 0x18, because it is TWO independent
			 *  features and the latch keys on which one was asked for.
			 *
			 *  Values outside those two bits are accepted exactly as before.
			 */
			if (idata & (SH_RCR1_CIE | SH_RCR1_AIE)) {
				if (sh4_val_first(d, SH4_VAL_RCR1INT, 0,
				    (uint32_t) (idata &
				    (SH_RCR1_CIE | SH_RCR1_AIE))))
					fatal("[ sh4: RTC: RCR1 interrupt enable"
					    " 0x%02x not implemented -- write"
					    " ignored.  (once per bit) ]\n",
					    (int) (idata &
					    (SH_RCR1_CIE | SH_RCR1_AIE)));
			} else
				d->rtc_rcr1 = idata;
		}
		break;

	case SH4_RCR2:
		if (writeflag == MEM_READ)
			odata = d->rtc_rcr2;
		else {
			d->rtc_rcr2 = idata;
			// bit 1 (i.e. idata == 0x02) means reset.
			if (idata != 0x02) {
				debug("[ SH4: TODO: RTC RCR2 value 0x%02x ignored. ]\n", (int)idata);
			}
		}
		break;


	/*************************************************/

	default:if (writeflag == MEM_READ) {
			fatal("[ sh4: read from addr 0x%x ]\n",
			    (int)relative_addr);
		} else {
			fatal("[ sh4: write to addr 0x%x: 0x%x ]\n",
			    (int)relative_addr, (int)idata);
		}

#ifdef SH4_DEBUG
		exit(1);
#endif
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}


DEVINIT(sh4)
{
	char tmp[200], n[200];
	int i;
	struct machine *machine = devinit->machine;
	struct sh4_data *d;

	CHECK_ALLOCATION(d = (struct sh4_data *) malloc(sizeof(struct sh4_data)));
	memset(d, 0, sizeof(struct sh4_data));


	/*
	 *  Main SH4 device, and misc memory stuff:
	 */

	memory_device_register(machine->memory, devinit->name,
	    SH4_REG_BASE, 0x01000000, dev_sh4_access, d, DM_DEFAULT, NULL);

	/*  On-chip RAM/cache:  */
	dev_ram_init(machine, 0x1e000000, 0x8000, DEV_RAM_RAM, 0x0, NULL);

	/*  0xe0000000: Store queues:  */
	memory_device_register(machine->memory, "sh4_sq",
	    0xe0000000, 0x04000000, dev_sh4_sq_access, d, DM_DEFAULT, NULL);


	/*
	 *  SCIF (Serial console):
	 */

	d->scif_console_handle = console_start_slave(devinit->machine,
	    "SH4 SCIF", 1);

	/*  #293: claim the machine's main console, or typed input is STOLEN.
	    Nothing on landisk ever set main_console_handle, so it stayed 0 --
	    and handle 0 also reads the host's stdin (the main loop polls it
	    for CTRL-C every tick, and console_charavail() imports up to 100
	    bytes into whichever handle polls first).  Two consumers raced for
	    every line typed at the guest: when handle 0 won, the line never
	    reached the SCIF at all -- no echo, no execution.  Measured on
	    OpenBSD/landisk: 10 of 12 commands vanished whole, and a
	    side-effect probe (touch /tmp/mNN) confirmed the vanished ones
	    never ran; with this line, 0 losses.  The instrumented counter
	    pair that first looked like proof of delivery (77 chars into the
	    console layer, 77 out) was an artifact: the counters were global,
	    and the debugger's exit-time drain of handle 0 balanced the books.
	    This is the same claim dev_dreamcast_maple.c, dev_luna88k.c and
	    dev_vr41xx.c already make.  On the Dreamcast this device is
	    created with the CPU (cpu_sh.c), BEFORE machine_dreamcast.c adds
	    dreamcast_maple, so the maple keyboard still overrides this and
	    Dreamcast behaviour is unchanged.  */
	devinit->machine->main_console_handle = d->scif_console_handle;

	snprintf(tmp, sizeof(tmp), "%s.irq[0x%x]",
	    devinit->interrupt_path, SH4_INTEVT_SCIF_RXI);
	INTERRUPT_CONNECT(tmp, d->scif_rx_irq);
	snprintf(tmp, sizeof(tmp), "%s.irq[0x%x]",
	    devinit->interrupt_path, SH4_INTEVT_SCIF_TXI);
	INTERRUPT_CONNECT(tmp, d->scif_tx_irq);


	/*
	 *  Caches (fake):
 	 *
	 *  0xf0000000	SH4_CCIA	I-Cache address array
	 *  0xf1000000	SH4_CCID	I-Cache data array
	 *  0xf4000000	SH4_CCDA	D-Cache address array
	 *  0xf5000000	SH4_CCDD	D-Cache data array
	 *
	 *  TODO: Implement more correct cache behavior?
	 */

	dev_ram_init(machine, SH4_CCIA, SH4_ICACHE_SIZE * 2, DEV_RAM_RAM, 0x0, NULL);
	dev_ram_init(machine, SH4_CCID, SH4_ICACHE_SIZE,     DEV_RAM_RAM, 0x0, NULL);
	dev_ram_init(machine, SH4_CCDA, SH4_DCACHE_SIZE * 2, DEV_RAM_RAM, 0x0, NULL);
	dev_ram_init(machine, SH4_CCDD, SH4_DCACHE_SIZE,     DEV_RAM_RAM, 0x0, NULL);

	/*  0xf2000000	SH4_ITLB_AA  */
	memory_device_register(machine->memory, "sh4_itlb_aa", SH4_ITLB_AA,
	    0x01000000, dev_sh4_itlb_aa_access, d, DM_DEFAULT, NULL);

	/*  0xf3000000	SH4_ITLB_DA1  */
	memory_device_register(machine->memory, "sh4_itlb_da1", SH4_ITLB_DA1,
	    0x01000000, dev_sh4_itlb_da1_access, d, DM_DEFAULT, NULL);

	/*  0xf6000000	SH4_UTLB_AA  */
	memory_device_register(machine->memory, "sh4_utlb_aa", SH4_UTLB_AA,
	    0x01000000, dev_sh4_utlb_aa_access, d, DM_DEFAULT, NULL);

	/*  0xf7000000	SH4_UTLB_DA1  */
	memory_device_register(machine->memory, "sh4_utlb_da1", SH4_UTLB_DA1,
	    0x01000000, dev_sh4_utlb_da1_access, d, DM_DEFAULT, NULL);


	/*
	 *  PCIC (PCI controller) at 0xfe200000:
	 */

	memory_device_register(machine->memory, "sh4_pcic", SH4_PCIC,
	    N_PCIC_REGS * sizeof(uint32_t), dev_sh4_pcic_access, d,
	    DM_DEFAULT, NULL);

	/*  Initial PCI control register contents:  */
	d->bsc_bcr2 = BCR2_PORTEN;
	d->pcic_reg[PCIC_REG(SH4_PCICONF2)] = PCI_CLASS_CODE(PCI_CLASS_BRIDGE,
	    PCI_SUBCLASS_BRIDGE_HOST, 0);

	/*  Register 16 PCIC interrupts:  */
	for (i=0; i<N_PCIC_IRQS; i++) {
		struct interrupt templ;
		snprintf(n, sizeof(n), "%s.pcic.%i",
		    devinit->interrupt_path, i);
		memset(&templ, 0, sizeof(templ));
		templ.line = i;
		templ.name = n;
		templ.extra = d;
		templ.interrupt_assert = sh4_pcic_interrupt_assert;
		templ.interrupt_deassert = sh4_pcic_interrupt_deassert;
		interrupt_handler_register(&templ);

		snprintf(tmp, sizeof(tmp), "%s.irq[0x%x]",
		    devinit->interrupt_path, SH4_INTEVT_IRQ0 + 0x20 * i);
		INTERRUPT_CONNECT(tmp, d->cpu_pcic_interrupt[i]);
	}

	/*  Register the PCI bus:  */
	snprintf(tmp, sizeof(tmp), "%s.pcic", devinit->interrupt_path);
	d->pci_data = bus_pci_init(
	    devinit->machine,
	    tmp,			/*  pciirq  */
	    0,				/*  pci device io offset  */
	    0,				/*  pci device mem offset  */
	    SH4_PCIC_IO,		/*  PCI portbase  */
	    SH4_PCIC_MEM,		/*  PCI membase  */
	    tmp,			/*  PCI irqbase  */
	    0x00000000,			/*  ISA portbase  */
	    0x00000000,			/*  ISA membase  */
	    "TODOisaIrqBase");		/*  ISA irqbase  */

	/*  Return PCI bus pointer, to allow per-machine devices
	    to be added later:  */
	devinit->return_ptr = d->pci_data;


	/*
	 *  Timer:
	 */

	d->sh4_timer = timer_add(SH4_PSEUDO_TIMER_HZ, sh4_timer_tick, d);
	machine_add_tickfunction(devinit->machine, dev_sh4_tick, d,
	    SH4_TICK_SHIFT);

	/*  Initial Timer values, according to the SH7750 manual:  */
	d->tcor[0] = 0xffffffff; d->tcnt[0] = 0xffffffff;
	d->tcor[1] = 0xffffffff; d->tcnt[1] = 0xffffffff;
	d->tcor[2] = 0xffffffff; d->tcnt[2] = 0xffffffff;

	snprintf(tmp, sizeof(tmp), "machine[0].cpu[0].irq[0x%x]",
	    SH_INTEVT_TMU0_TUNI0);
	if (!interrupt_handler_lookup(tmp, &d->timer_irq[0])) {
		fatal("Could not find interrupt '%s'.\n", tmp);
		exit(1);
	}
	snprintf(tmp, sizeof(tmp), "machine[0].cpu[0].irq[0x%x]",
	    SH_INTEVT_TMU1_TUNI1);
	if (!interrupt_handler_lookup(tmp, &d->timer_irq[1])) {
		fatal("Could not find interrupt '%s'.\n", tmp);
		exit(1);
	}
	snprintf(tmp, sizeof(tmp), "machine[0].cpu[0].irq[0x%x]",
	    SH_INTEVT_TMU2_TUNI2);
	if (!interrupt_handler_lookup(tmp, &d->timer_irq[2])) {
		fatal("Could not find interrupt '%s'.\n", tmp);
		exit(1);
	}


	// The RTC RCR2 register is "basically" initialized to 0x09, with
	// some bit undefined. :-) According to the manual.
	d->rtc_rcr2 = 0x09;


	/*
	 *  Bus State Controller initial values, according to the
	 *  SH7760 manual:
	 */

	d->bsc_bcr2 = 0x3ffc;
	d->bsc_wcr1 = 0x77777777;
	d->bsc_wcr2 = 0xfffeefff;
	d->bsc_wcr3 = 0x77777777;

	return 1;
}

