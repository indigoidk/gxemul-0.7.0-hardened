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
 *  COMMENT: National Semiconductor DP8390 "NE2000" ISA ethernet controller
 *
 *  A minimal-but-functional NE2000 (16-bit)/DP8390 implementation, enough for
 *  the OpenBSD/arc (and NetBSD/arc) "ed" driver to probe, configure and run:
 *
 *	ed0 at isa? port 0x280 iomem 0xd0000 irq 9	# NE[12]000
 *
 *  The card is pure programmed-I/O against a host-private 16 KB ring buffer:
 *  there is no bus-master DMA into guest RAM, so (unlike a real SONIC) the
 *  entire guest-visible surface is index arithmetic which is masked/clamped to
 *  the card's own memory here.  All accesses to the on-card memory go through
 *  ne_mem_readb()/ne_mem_writeb(), which enforce the PROM / RAM / unmapped
 *  layout, so a mis-programmed (or hostile) guest can only ever touch this
 *  device's own buffer -- never host memory.
 *
 *  References: National Semiconductor DP8390 datasheet; the OpenBSD 2.2
 *  dev/isa/if_ed.c + dev/ic/dp8390reg.h driver this device must satisfy; and
 *  the gxemul dev_le.c NIC idiom (tick-driven rx poll + irq recompute).
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
#include "net.h"


#define	NE2000_TICK_SHIFT	14

/*  I/O port layout (32 ports): 0x00-0x0f = DP8390 NIC registers (page-selected
    via the command register), 0x10 = ASIC remote-DMA data window, 0x1f = ASIC
    reset.  (asic base 0x10 + data 0x00 / reset 0x0f.)  */
#define	NE2000_IO_PORTS		32
#define	NE_DATA_PORT		0x10
#define	NE_RESET_PORT		0x1f

/*  On-card memory: 32 KB address space.  The 32-byte station-address PROM is
    at 0x0000-0x001f; the 16 KB RAM ring buffer is at 0x4000-0x7fff; everything
    else is unmapped (reads return 0xff, writes are dropped) -- this is what
    lets the driver's "is there RAM at 8 KB?" probe fail and pick NE2000.  */
#define	NE_MEM_SIZE		0x8000
#define	NE_PROM_SIZE		0x20
#define	NE_RAM_START		0x4000
#define	NE_RAM_END		0x8000
#define	NE_PAGE_SIZE		256

/*  Command register (CR), all pages, offset 0x00:  */
#define	ED_CR_STP	0x01	/*  stop  */
#define	ED_CR_STA	0x02	/*  start  */
#define	ED_CR_TXP	0x04	/*  transmit packet  */
#define	ED_CR_RD0	0x08	/*  remote DMA: read  */
#define	ED_CR_RD1	0x10	/*  remote DMA: write  */
#define	ED_CR_RD2	0x20	/*  remote DMA: abort / no-DMA  */
#define	ED_CR_PAGESHIFT	6	/*  PS0/PS1 select register page  */

/*  Interrupt status (ISR) / mask (IMR):  */
#define	ED_ISR_PRX	0x01	/*  packet received  */
#define	ED_ISR_PTX	0x02	/*  packet transmitted  */
#define	ED_ISR_RXE	0x04	/*  receive error  */
#define	ED_ISR_TXE	0x08	/*  transmit error  */
#define	ED_ISR_OVW	0x10	/*  receive ring overwrite  */
#define	ED_ISR_CNT	0x20	/*  counter overflow  */
#define	ED_ISR_RDC	0x40	/*  remote DMA complete  */
#define	ED_ISR_RST	0x80	/*  reset / stopped status  */

/*  Data configuration (DCR):  */
#define	ED_DCR_WTS	0x01	/*  word transfer select (16-bit)  */

/*  Receive configuration (RCR):  */
#define	ED_RCR_PRO	0x10	/*  promiscuous physical  */
#define	ED_RCR_MON	0x20	/*  monitor mode (do not store packets)  */

/*  Transmit status (TSR) / receive status (RSR):  */
#define	ED_TSR_PTX	0x01	/*  transmitted ok  */
#define	ED_RSR_PRX	0x01	/*  received ok  */

/*  Receive ring header (prepended by the NIC to each received packet):  */
#define	ED_RING_RSR		0	/*  copy of receive status  */
#define	ED_RING_NEXT_PACKET	1	/*  page of the next packet  */
#define	ED_RING_COUNT		2	/*  byte count incl. this 4-byte header  */
#define	ED_RING_HDRSZ		4

/*  Largest frame we will read out of the tx buffer for net_ethernet_tx():  */
#define	NE_MAX_TX		2048


struct ne2000_data {
	struct nic_data	nic;
	int		subsys;		/*  for debugmsg  */

	struct interrupt irq;
	int		irq_asserted;

	/*  DP8390 register state.  The low bits of the command register are
	    shared across all pages; PS0/PS1 (bits 6-7) select the page for
	    subsequent accesses to offsets 0x01-0x0f.  */
	uint8_t		cr;
	uint8_t		isr, imr;
	uint8_t		dcr, rcr, tcr;
	uint8_t		rsr, tsr, ncr;

	/*  Receive ring page pointers (page numbers, i.e. addr >> 8):  */
	uint8_t		pstart, pstop, bnry, curr;

	/*  Transmit:  */
	uint8_t		tpsr;		/*  tx page start  */
	uint16_t	tbcr;		/*  tx byte count  */

	/*  Remote DMA (live pointers; loaded from RSAR/RBCR register writes and
	    advanced by each access to the data window):  */
	uint16_t	rsar;
	uint16_t	rbcr;

	/*  Page-1 address filters (readback only; net.c does the filtering by
	    nic.mac_address):  */
	uint8_t		par[6];
	uint8_t		mar[8];

	/*  On-card memory (PROM + RAM); see the NE_MEM_* layout above.  */
	uint8_t		mem[NE_MEM_SIZE];
};


/*
 *  ne_mem_readb(), ne_mem_writeb():
 *
 *  All on-card memory access funnels through these two.  They implement the
 *  PROM / RAM / unmapped layout AND bound every access to the device's own
 *  buffer, so no guest-programmed address can ever escape into host memory.
 */
static uint8_t ne_mem_readb(struct ne2000_data *d, uint16_t addr)
{
	if (addr < NE_PROM_SIZE)
		return d->mem[addr];
	if (addr >= NE_RAM_START && addr < NE_RAM_END)
		return d->mem[addr];
	return 0xff;
}

static void ne_mem_writeb(struct ne2000_data *d, uint16_t addr, uint8_t val)
{
	/*  The PROM and the unmapped gap ignore writes; only the RAM ring is
	    writable.  */
	if (addr >= NE_RAM_START && addr < NE_RAM_END)
		d->mem[addr] = val;
}


/*
 *  ne_dma_readb(), ne_dma_writeb():
 *
 *  One byte of a remote-DMA transfer through the data window.  Advance the
 *  remote start address, decrement the remote byte count, and raise ISR_RDC
 *  when the programmed count is exhausted (the driver polls RDC after every
 *  remote-DMA write, and would hang forever without it).
 */
static uint8_t ne_dma_readb(struct ne2000_data *d)
{
	uint8_t v = ne_mem_readb(d, d->rsar);
	d->rsar++;
	if (d->rbcr > 0)
		d->rbcr--;
	if (d->rbcr == 0)
		d->isr |= ED_ISR_RDC;
	return v;
}

static void ne_dma_writeb(struct ne2000_data *d, uint8_t v)
{
	ne_mem_writeb(d, d->rsar, v);
	d->rsar++;
	if (d->rbcr > 0)
		d->rbcr--;
	if (d->rbcr == 0)
		d->isr |= ED_ISR_RDC;
}


/*
 *  ne2000_update_irq():
 *
 *  Recompute the interrupt line from (ISR & IMR).  Idempotent; called at the
 *  end of every register access and every tick so a level that was briefly
 *  dropped by an EOI/latch race self-heals (the dev_le idiom).
 */
static void ne2000_update_irq(struct ne2000_data *d)
{
	int new_assert = (d->isr & d->imr & 0x7f) ? 1 : 0;

	/*  Assert unconditionally while the level is high.  The Jazz ISA bridge's
	    8259-style EOI writes (dev_jazz.c) clear the latched ISA line state, so
	    a transition-gated assert would leave a still-pending level dropped
	    until the next 0->1 edge -- wedging RX under bursts.  INTERRUPT_ASSERT
	    is idempotent (jazz_isa_interrupt_assert just sets a bit and
	    recomputes), so re-asserting each call cheaply self-heals the latch.  */
	if (new_assert)
		INTERRUPT_ASSERT(d->irq);
	else if (d->irq_asserted)
		INTERRUPT_DEASSERT(d->irq);

	d->irq_asserted = new_assert;
}


/*
 *  ne2000_reset():
 *
 *  Triggered by the ASIC reset port.  Puts the NIC in the stopped state with
 *  the reset-status bit set (the driver's edstop() polls ISR_RST).  The PROM
 *  and the programmed station address are left intact.
 */
static void ne2000_reset(struct ne2000_data *d)
{
	d->isr = ED_ISR_RST;
	d->cr = ED_CR_RD2 | ED_CR_STP;
	d->imr = 0;
	d->rbcr = 0;
}


/*
 *  ne2000_do_tx():
 *
 *  A transmit was requested (CR_TXP).  The frame has already been copied into
 *  the tx page buffer by the driver's remote-DMA write, so read tbcr bytes out
 *  of on-card memory at (tpsr << 8) and hand them to the network layer, then
 *  flag PTX so the driver frees its mbuf instead of timing out.
 */
static void ne2000_do_tx(struct net *net, struct ne2000_data *d)
{
	unsigned char buf[NE_MAX_TX];
	int i, len = d->tbcr;
	uint32_t src = ((uint32_t)d->tpsr) << 8;

	if (len > (int)sizeof(buf)) {
		debugmsg(d->subsys, "tx", VERBOSITY_WARNING,
		    "oversized tx length %i clamped to %i", len, (int)sizeof(buf));
		len = sizeof(buf);
	}

	for (i = 0; i < len; i++)
		buf[i] = ne_mem_readb(d, (uint16_t)(src + i));

	debugmsg(d->subsys, "tx", VERBOSITY_DEBUG,
	    "transmitting %i bytes from page 0x%02x", len, d->tpsr);

	if (len > 0)
		net_ethernet_tx(net, &d->nic, buf, len);

	d->tsr = ED_TSR_PTX;
	d->ncr = 0;
	d->isr |= ED_ISR_PTX;
	d->cr &= ~ED_CR_TXP;		/*  TXP self-clears on completion  */
}


/*
 *  ne2000_receive():
 *
 *  Store one received frame into the receive ring at CURR, prepending the
 *  4-byte NIC ring header, advancing CURR, and flagging PRX.  If the ring is
 *  full the frame is dropped and OVW is raised (rather than overwriting unread
 *  packets or -- worse -- running off the buffer).
 */
static void ne2000_receive(struct ne2000_data *d,
	const unsigned char *pkt, int pktlen)
{
	int i, total, npages, ringpages, used, avail;
	uint8_t start = d->curr, next;
	uint32_t addr, stopaddr, startaddr;

	if (pktlen < 1)
		return;

	/*  The ring buffer only spans whole pages within the RAM window.  If
	    the driver has mis-programmed PSTART/PSTOP, refuse to store rather
	    than compute a bogus wrap.  */
	if (d->pstop <= d->pstart ||
	    (uint32_t)(d->pstop << 8) > NE_RAM_END ||
	    (uint32_t)(d->pstart << 8) < NE_RAM_START ||
	    d->curr < d->pstart || d->curr >= d->pstop ||
	    d->bnry < d->pstart || d->bnry >= d->pstop) {
		debugmsg(d->subsys, "rx", VERBOSITY_WARNING,
		    "bogus ring pstart=0x%02x pstop=0x%02x curr=0x%02x bnry=0x%02x;"
		    " dropping packet", d->pstart, d->pstop, d->curr, d->bnry);
		return;
	}

	total = pktlen + ED_RING_HDRSZ;
	/*  The real DP8390 also stores the 4-byte FCS after the data, so page
	    allocation must reserve it even though the header's count field
	    (written below) excludes it.  Without the +4, ed_rint()'s length
	    recomputation from the next-packet pointer comes out 256 short
	    whenever (total & 0xff) is 0 or >= 253 -- losing, truncating, or
	    triggering a guest NIC reset for those packet sizes.  */
	npages = (total + 4 + NE_PAGE_SIZE - 1) >> 8;
	ringpages = d->pstop - d->pstart;

	/*  Free pages = ring size minus the pages between BNRY and CURR.  */
	used = (int)start - (int)d->bnry;
	if (used < 0)
		used += ringpages;
	avail = ringpages - used;

	if (npages >= avail) {
		debugmsg(d->subsys, "rx", VERBOSITY_WARNING,
		    "receive ring full (need %i pages, %i free); packet dropped",
		    npages, avail);
		d->isr |= ED_ISR_OVW;
		return;
	}

	next = start + npages;
	if (next >= d->pstop)
		next -= ringpages;

	/*  4-byte ring header at the start page.  */
	addr = ((uint32_t)start) << 8;
	ne_mem_writeb(d, (uint16_t)(addr + ED_RING_RSR), ED_RSR_PRX);
	ne_mem_writeb(d, (uint16_t)(addr + ED_RING_NEXT_PACKET), next);
	ne_mem_writeb(d, (uint16_t)(addr + ED_RING_COUNT), total & 0xff);
	ne_mem_writeb(d, (uint16_t)(addr + ED_RING_COUNT + 1), (total >> 8) & 0xff);

	/*  Payload, wrapping PSTOP -> PSTART.  */
	addr = (((uint32_t)start) << 8) + ED_RING_HDRSZ;
	stopaddr  = ((uint32_t)d->pstop)  << 8;
	startaddr = ((uint32_t)d->pstart) << 8;
	for (i = 0; i < pktlen; i++) {
		if (addr >= stopaddr)
			addr = startaddr;
		ne_mem_writeb(d, (uint16_t)addr, pkt[i]);
		addr++;
	}

	d->curr = next;
	d->rsr = ED_RSR_PRX;
	d->isr |= ED_ISR_PRX;

	debugmsg(d->subsys, "rx", VERBOSITY_DEBUG,
	    "received %i bytes -> pages 0x%02x..0x%02x, curr now 0x%02x",
	    pktlen, start, (uint8_t)(next - 1), next);
}


/*
 *  ne2000_cr_write():
 *
 *  Handle a write to the command register: reset-status tracking, the transmit
 *  trigger, and the (implicit) page/remote-DMA selection.  The remote-DMA start
 *  address and byte count have already been loaded via the RSAR/RBCR registers,
 *  so RD0/RD1 need no extra work here; the data-window accesses drive them.
 */
static void ne2000_cr_write(struct net *net, struct ne2000_data *d, uint8_t val)
{
	uint8_t old = d->cr;
	d->cr = val;

	/*  RST is cleared by a START command and (re)set by STOP.  */
	if (val & ED_CR_STA)
		d->isr &= ~ED_ISR_RST;
	else if (val & ED_CR_STP)
		d->isr |= ED_ISR_RST;

	/*  Transmit on the rising edge of TXP, but only when started: the real
	    8390 ignores TXP in the stopped (reset) state.  RST is already updated
	    above, so a single STA|TXP write (which if_ed uses) works.  */
	if ((val & ED_CR_TXP) && !(old & ED_CR_TXP)) {
		if (!(d->isr & ED_ISR_RST))
			ne2000_do_tx(net, d);
		else
			debugmsg(d->subsys, "tx", VERBOSITY_WARNING,
			    "TXP while stopped; ignored");
	}
}


/*
 *  dev_ne2000_tick():
 *
 *  Poll the network for incoming packets and recompute the interrupt.  Runs
 *  both periodically (machine_add_tickfunction) and at the end of every
 *  register access, matching the dev_le idiom.
 */
DEVICE_TICK(ne2000)
{
	struct ne2000_data *d = (struct ne2000_data *) extra;
	struct net *net = cpu->machine->emul->net;

	/*  Only receive when the NIC is started and not in monitor mode.  This
	    also naturally suppresses reception during the driver's memory probe
	    (which leaves RCR in monitor mode).  */
	if ((d->cr & ED_CR_STA) && !(d->cr & ED_CR_STP) &&
	    !(d->rcr & ED_RCR_MON)) {
		while (net_ethernet_rx_avail(net, &d->nic)) {
			unsigned char *pkt = NULL;
			int pktlen = 0;

			if (!net_ethernet_rx(net, &d->nic, &pkt, &pktlen))
				break;
			if (pkt == NULL)
				break;

			/*  If the ring is full, leave the packet dropped and
			    stop pulling more until the driver drains it.  */
			if (d->isr & ED_ISR_OVW) {
				free(pkt);
				break;
			}

			ne2000_receive(d, pkt, pktlen);
			free(pkt);

			if (d->isr & ED_ISR_OVW)
				break;
		}
	}

	ne2000_update_irq(d);
}


DEVICE_ACCESS(ne2000)
{
	struct ne2000_data *d = (struct ne2000_data *) extra;
	struct net *net = cpu->machine->emul->net;
	uint64_t idata = 0, odata = 0;
	int page, reg, i;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	/*
	 *  Remote-DMA data window.  A byte stream: for a little-endian guest the
	 *  first byte of each word is the low byte (the dev_wdc.c data-port
	 *  idiom).  Fill/drain 'len' bytes and return directly.
	 */
	if (relative_addr == NE_DATA_PORT) {
		if (writeflag == MEM_WRITE) {
			if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {
				for (i = 0; i < (int)len; i++)
					ne_dma_writeb(d, (idata >> (8*i)) & 0xff);
			} else {
				for (i = (int)len - 1; i >= 0; i--)
					ne_dma_writeb(d, (idata >> (8*i)) & 0xff);
			}
		} else {
			if (cpu->byte_order == EMUL_LITTLE_ENDIAN) {
				for (i = 0; i < (int)len; i++)
					odata |= (uint64_t)ne_dma_readb(d) << (8*i);
			} else {
				for (i = 0; i < (int)len; i++)
					odata = (odata << 8) | ne_dma_readb(d);
			}
			memory_writemax64(cpu, data, len, odata);
		}
		/*  Return here WITHOUT running the full tick: the remote-DMA data
		    window is hit once per word during bulk transfers, and polling
		    the network on every word would be needlessly costly.  The
		    periodic tick and the register-access tick both cover RX.  */
		ne2000_update_irq(d);
		return 1;
	}

	/*  ASIC reset port: any access resets and returns 0.  */
	if (relative_addr == NE_RESET_PORT) {
		ne2000_reset(d);
		if (writeflag == MEM_READ)
			memory_writemax64(cpu, data, len, 0);
		ne2000_update_irq(d);
		return 1;
	}

	/*  Remaining ASIC ports (0x11-0x1e) are unused on an NE2000.  */
	if (relative_addr > 0x0f) {
		if (writeflag == MEM_READ)
			memory_writemax64(cpu, data, len, 0);
		goto done;
	}

	/*  DP8390 NIC registers.  Offset 0 is always the command register; the
	    page selected by CR's PS0/PS1 bits governs offsets 0x01-0x0f.  */
	reg = relative_addr;
	page = (d->cr >> ED_CR_PAGESHIFT) & 3;

	if (reg == 0x00) {
		if (writeflag == MEM_WRITE)
			ne2000_cr_write(net, d, idata & 0xff);
		else
			odata = d->cr;
		goto reg_done;
	}

	if (page == 0) {
		if (writeflag == MEM_WRITE) {
			switch (reg) {
			case 0x01: d->pstart = idata; break;
			case 0x02: d->pstop = idata; break;
			case 0x03: d->bnry = idata; break;
			case 0x04: d->tpsr = idata; break;
			case 0x05: d->tbcr = (d->tbcr & 0xff00) | (idata & 0xff); break;
			case 0x06: d->tbcr = (d->tbcr & 0x00ff) | ((idata & 0xff) << 8); break;
			case 0x07: d->isr &= ~(idata & 0x7f); break;   /*  write-1-to-clear  */
			case 0x08: d->rsar = (d->rsar & 0xff00) | (idata & 0xff); break;
			case 0x09: d->rsar = (d->rsar & 0x00ff) | ((idata & 0xff) << 8); break;
			case 0x0a: d->rbcr = (d->rbcr & 0xff00) | (idata & 0xff); break;
			case 0x0b: d->rbcr = (d->rbcr & 0x00ff) | ((idata & 0xff) << 8); break;
			case 0x0c: d->rcr = idata;
				/*  Mirror promiscuous mode so a tap network
				    (net_tap.c) delivers all frames to a guest
				    running tcpdump / IFF_PROMISC.  */
				d->nic.promiscuous_mode =
				    (idata & ED_RCR_PRO) ? 1 : 0;
				break;
			case 0x0d: d->tcr = idata; break;
			case 0x0e: d->dcr = idata; break;
			case 0x0f: d->imr = idata; break;
			}
		} else {
			switch (reg) {
			case 0x01: odata = d->rsar & 0xff; break;   /*  CLDA0  */
			case 0x02: odata = d->rsar >> 8; break;     /*  CLDA1  */
			case 0x03: odata = d->bnry; break;
			case 0x04: odata = d->tsr; break;
			case 0x05: odata = d->ncr; break;
			case 0x06: odata = 0; break;                /*  FIFO  */
			case 0x07: odata = d->isr; break;
			case 0x08: odata = d->rsar & 0xff; break;   /*  CRDA0  */
			case 0x09: odata = d->rsar >> 8; break;     /*  CRDA1  */
			case 0x0c: odata = d->rsr; break;
			case 0x0d:
			case 0x0e:
			case 0x0f: odata = 0; break;                /*  tally counters  */
			}
		}
	} else if (page == 1) {
		if (writeflag == MEM_WRITE) {
			if (reg >= 0x01 && reg <= 0x06)
				d->par[reg - 0x01] = idata;
			else if (reg == 0x07)
				d->curr = idata;
			else if (reg >= 0x08 && reg <= 0x0f)
				d->mar[reg - 0x08] = idata;
		} else {
			if (reg >= 0x01 && reg <= 0x06)
				odata = d->par[reg - 0x01];
			else if (reg == 0x07)
				odata = d->curr;
			else if (reg >= 0x08 && reg <= 0x0f)
				odata = d->mar[reg - 0x08];
		}
	} else {
		/*  Page 2 is mostly a read-back of page-0 config; give the driver
		    sane values instead of warning noisily.  */
		if (writeflag == MEM_READ) {
			switch (reg) {
			case 0x01: odata = d->pstart; break;
			case 0x02: odata = d->pstop; break;
			case 0x03: odata = d->curr; break;   /*  RNPP  */
			case 0x04: odata = d->tpsr; break;
			case 0x0c: odata = d->rcr; break;
			case 0x0d: odata = d->tcr; break;
			case 0x0e: odata = d->dcr; break;
			case 0x0f: odata = d->imr; break;
			default:   odata = 0; break;
			}
		} else {
			/*  if_ed never writes page 2/3; warn loudly if some
			    other guest does, rather than swallowing it.  */
			debugmsg(d->subsys, "register", VERBOSITY_WARNING,
			    "ignored write 0x%02x to page-%i register 0x%02x",
			    (int)(idata & 0xff), page, reg);
		}
	}

reg_done:
	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

done:
	dev_ne2000_tick(cpu, extra);
	return 1;
}


DEVINIT(ne2000)
{
	char *name2;
	size_t nlen = 55;
	struct ne2000_data *d;
	int i;

	CHECK_ALLOCATION(d = (struct ne2000_data *) malloc(sizeof(struct ne2000_data)));
	memset(d, 0, sizeof(struct ne2000_data));

	d->subsys = debugmsg_register_subsystem("ne2000");

	INTERRUPT_CONNECT(devinit->interrupt_path, d->irq);

	net_generate_unique_mac(devinit->machine, d->nic.mac_address);

	/*  Station-address PROM: the "ed" driver reads 16 bytes from card
	    address 0 and takes every other byte (16-bit cards double each MAC
	    byte).  Also lay down the NE2000 signature bytes (0x57,0x57).  */
	for (i = 0; i < 6; i++)
		d->mem[i * 2] = d->mem[i * 2 + 1] = d->nic.mac_address[i];
	d->mem[0x1c] = d->mem[0x1d] = d->mem[0x1e] = d->mem[0x1f] = 0x57;

	/*  Copy the MAC into the page-1 PAR readback too.  */
	memcpy(d->par, d->nic.mac_address, sizeof(d->par));

	ne2000_reset(d);

	CHECK_ALLOCATION(name2 = (char *) malloc(nlen));
	snprintf(name2, nlen, "%s [%02x:%02x:%02x:%02x:%02x:%02x]",
	    devinit->name, d->nic.mac_address[0], d->nic.mac_address[1],
	    d->nic.mac_address[2], d->nic.mac_address[3],
	    d->nic.mac_address[4], d->nic.mac_address[5]);

	memory_device_register(devinit->machine->memory, name2,
	    devinit->addr, NE2000_IO_PORTS,
	    dev_ne2000_access, (void *)d, DM_DEFAULT, NULL);

	machine_add_tickfunction(devinit->machine, dev_ne2000_tick, d,
	    NE2000_TICK_SHIFT);

	net_add_nic(devinit->machine->emul->net, &d->nic);

	return 1;
}
