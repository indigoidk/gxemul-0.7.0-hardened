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
 *  COMMENT: LCA PCI bus, for Alpha machines
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "bus_isa.h"
#include "bus_pci.h"
#include "cpu.h"
#include "device.h"
#include "emul.h"
#include "interrupt.h"
#include "machine.h"
#include "memory.h"
#include "misc.h"

#include "thirdparty/alpha_lcareg.h"

#define	LCA_ISA_BASE	(LCA_PCI_SIO + 0x10000000)
#define	LCA_ISA_MEMBASE	(LCA_PCI_SIO + 0x18000000)


/*  #516: warn-once latch bits, one per stub.  PER-INSTANCE, reached through
    `interrupt->extra' -- see the comment on lca_interrupt_assert().  */
#define	LCA_W_IRQ_ASSERT	0	/*  #516  */
#define	LCA_W_IRQ_DEASSERT	1	/*  #516  */
#define	LCA_W_IOC_CONF_CFG1	2	/*  #518: IOC_CONF<1> set -- CFG AD<1:0> = 10/11, not a cycle type  */
#define	LCA_W_IOC_WMASK0	3	/*  #518: unsupported W_MASK0 encoding declined  */
#define	LCA_W_IOC_WMASK1	4	/*  #518: unsupported W_MASK1 encoding declined  */
#define	LCA_W_IOC_WEN		5	/*  #518: a DMA window enabled -- translation not modelled  */
#define	LCA_W_IOC_DEF_W	6	/*  #518: default-arm write declined  */
#define	LCA_W_IOC_DEF_R	7	/*  #518: default-arm read answered with zero  */

struct lca_data {
	struct pci_data		*pci_data;

	unsigned int		warned;		/*  #516  */

	uint64_t		ioc_conf;
	uint64_t		tlb_enable;
	uint64_t		window_base_0;
	uint64_t		window_mask_0;
	uint64_t		window_t_base_0;
	uint64_t		window_base_1;
	uint64_t		window_mask_1;
	uint64_t		window_t_base_1;
};


/*
 *  lca_interrupt_assert():
 *
 *  Line 0 = ISA interrupt.
 */
void lca_interrupt_assert(struct interrupt *interrupt)
{
	struct lca_data *d = (struct lca_data *) interrupt->extra;	/*  #516  */

	/*  #516: this was `fatal(); exit(1)' with NO GUARD -- not a refused value,
	    an unimplemented path -- and DEVINIT below installs it as the ISA
	    interrupt callback that `bus_isa_init' wires to BUS_ISA_IDE0|IDE1.  So an
	    ordinary ISA interrupt ended the host, needing no unusual value anywhere.
	    MEASURED on two independent guest paths: one store to the 8042 command
	    port (regress/lca_irqstub_probe.py, 3/4) and three byte stores to the
	    ns16550 on IRQ 4 (regress/lca_irqstub_uart_probe.py, 2/4).

	    *** THE STUB IS NOT REPLACED BY A FORWARD, BECAUSE A FORWARD WOULD BE A
	    NO-OP.  ALPHA HAS NO INTERRUPT DELIVERY AT ALL. ***  `cd.alpha.irq_asserted'
	    is written by `cpu_alpha.c' and read NOWHERE.  `cpu_dyntrans.c' turns a
	    pending interrupt into a delivered one for FIVE architectures -- ARM and
	    M88K and PPC through their own `irq_asserted', MIPS through the COP0
	    exception model, and SH through `int_to_assert' -- and ALPHA IS ABSENT
	    FROM THAT LIST.  (An earlier draft of this comment said "ARM, M88K and
	    PPC only": that enumeration was made by grepping for `irq_asserted', which
	    is a CORRELATE of delivering rather than the property, and it missed the
	    two architectures that deliver by another mechanism.  The Alpha conclusion
	    is unchanged and is strengthened -- it is the outlier among five, not
	    three.)  Calling `cpu_interrupt()' here would set
	    a field nothing consumes.  Implementing delivery is a SUBSYSTEM -- the
	    dyntrans dispatch, the PALcode entry and the IPL check -- and is its own
	    round, not this one.

	    So the disposition is DECLINE plus a bounded announce, and what it buys is
	    stated narrowly on purpose: THE HOST STOPS DYING.  Interrupts do not start
	    working; they were never delivered on this architecture and still are not.

	    The latch is PER-INSTANCE (`interrupt->extra'), not function-static: a
	    function-static bit would let one guest access to one device instance
	    silence the diagnostic for every other instance, which is a class already
	    filed against this tree.  */
	if (d != NULL && !(d->warned & (1u << LCA_W_IRQ_ASSERT))) {	/*  #516  */
		d->warned |= 1u << LCA_W_IRQ_ASSERT;
		fatal("[ lca: ISA interrupt assert not implemented (Alpha has no "
		    "interrupt delivery); ignored  (once) ]\n");
	}
}


/*
 *  lca_interrupt_deassert():
 *
 *  Line 0 = ISA interrupt.
 */
void lca_interrupt_deassert(struct interrupt *interrupt)
{
	struct lca_data *d = (struct lca_data *) interrupt->extra;	/*  #516  */

	/*  #516: the sibling of lca_interrupt_assert() above, same reasoning.  A
	    SEPARATE latch bit, so the two are distinguishable: a driver normally
	    reaches both within one interrupt cycle, and one shared bit would report
	    whichever arrived first and hide the other entirely.  */
	if (d != NULL && !(d->warned & (1u << LCA_W_IRQ_DEASSERT))) {	/*  #516  */
		d->warned |= 1u << LCA_W_IRQ_DEASSERT;
		fatal("[ lca: ISA interrupt deassert not implemented (Alpha has no "
		    "interrupt delivery); ignored  (once) ]\n");
	}
}


DEVICE_ACCESS(lca_pci_conf)
{
	uint64_t idata = 0, odata = 0;
	int tag, type1, bus, dev, func, reg;	/*  #515  */
	struct lca_data *d = (struct lca_data *) extra;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	/*
	 *  1. Decompose the address into a tag.
	 *
	 *  According to NetBSD's lca_pci.c, the address is composed like this:
	 *
	 *	addr = tag << 5 | (regoffset & ~0x03) << 5 | 0x3 << 3
	 */
	reg = (relative_addr >> 5) & 0xfc;
	tag = (relative_addr >> 5) & ~0xff;

	/*
	 *  2. Decompose the tag into bus, dev, and func.
	 *
	 *  The tag can be constructed in one of two ways. On the primary
	 *  bus (nr 0):
	 *
	 *	tag = (1 << (device + 11)) | (function << 8);
	 *
	 *  and on other busses, the tag is a normal:
	 *
	 *	tag = (bus << 16) | (device << 11) | (function << 8)
	 */
	/*  printf("tag = 0x%x\n", (int)tag);  */

	/*  #515: `bus' used to be BOTH the configuration CYCLE TYPE and the
	    DESTINATION BUS, and conflating them is the whole defect.  IOC_CONF bit 0
	    selects the cycle type only -- 21066/21066A HRM S6.2.9: "PCI address bits
	    ad<1:0> come directly from configuration cycle type register (IOC_CONF,
	    Section 6.4.2) bits <1:0>" -- and it does NOT carry a bus number.  The
	    destination bus of a type-1 cycle lives in the ADDRESS, per the PCI Local
	    Bus specification's type-1 layout (bus 23..16, dev 15..11, fn 10..8,
	    reg 7..2), which S6.2.9 defers to explicitly.

	    Before this, a guest that merely SET bit 0 -- a value the CONF guard
	    ACCEPTS -- made any subsequent access in this window reach
	    `fatal("TODO. Non-zero bus."); exit(1)'.  MEASURED: two ordinary guest
	    accesses, nothing refused anywhere on the path
	    (regress/lca_confbus_probe.py, 3/4 pre-fix; artifacts/lcaconfbus1kill/).  */
	type1 = d->ioc_conf & 1;	/*  #515  */
	bus = 0;			/*  #515  */

	if (!type1) {			/*  #515  */
		/*  #511: was `0x800 << dev'.  `0x800' is a plain int (2^11) and `dev'
		    reaches 20, so the last iteration evaluates 2^31 -- a SIGNED
		    OVERFLOW, undefined by C99 6.5.7p4, not merely
		    implementation-defined.  MEASURED under UBSAN before the change:
		    "dev_lca.c:125:21: runtime error: left shift of 2048 by 20 places
		    cannot be represented in type 'int'", reached by an ordinary guest
		    ldq into the PCI config window (regress/lca_confbus_probe.py against
		    build-asan; artifacts/lcashiftub/ubsan_HEAD_20260907.raw).

		    `0x800U' makes the operand unsigned, so 2048U << 20 is 0x80000000U --
		    inside unsigned int -- and NOTHING ELSE MOVES.

		    *** THE REASON, CORRECTED: AN EARLIER DRAFT SAID `tag' IS "ALREADY A
		    WIDER UNSIGNED QUANTITY".  THAT IS FALSE -- `tag' is a plain signed
		    `int' (:92) -- AND FOUR PASS-2 SEATS CAUGHT IT.  Worse, the claim was
		    backwards: being WIDER is what would CREATE a difference, not remove
		    one.  Had `tag' been `uint64_t', the old `int' 0x80000000 is NEGATIVE
		    and would SIGN-EXTEND to 0xffffffff80000000 for the `&', while
		    `0x800U << 20' zero-extends to 0x0000000080000000 -- two different
		    masks.  The seats were right about the mechanism and it does not fire
		    here only because of the type.

		    WHAT ACTUALLY HOLDS: both operands are 32-bit, so the `&' is performed
		    at 32 bits either way -- `int & int' before, and after, `tag' converted
		    to `unsigned int' by the usual arithmetic conversions.  The RESULT'S
		    BIT PATTERN IS IDENTICAL; only its type changes, and it is consumed
		    solely as a truth test in `if (...)'.  So no guest-visible value moves,
		    and the repair is owed purely by the LANGUAGE. ***

		    *** THE LOOP THIS SITS IN IS THIS FILE'S OWN GRACEFUL-DEGRADATION
		    PRECEDENT -- the `dev >= 21' arm below has a commented-out
		    fatal()/exit(1) and substitutes `dev = 0' instead, and `lcabadval'
		    cites it as a transferable warrant.  The safe path contained the UB. ***  */
		for (dev=0; dev<21; dev++)
			if (tag & (0x800U << dev))	/*  #511  */
				break;
		if (dev >= 21) {
			/*  fatal("[ LCA: No bus 0 device? TODO ]\n");
			exit(1);  */
			dev = 0;
		}
	} else {
		/*  #515: a type-1 cycle carries its destination in the address.  */
		bus = (tag >> 16) & 0xff;	/*  #515  */
		dev = (tag >> 11) & 0x1f;	/*  #515  */
	}

	func = (tag >> 8) & 7;
	/*  printf("bus=%i dev=%i func=%i reg=%i\n", bus,dev,func,reg);  */

	/*  #515: a type-1 cycle whose bus field is zero selects NOTHING.  Type-1 is
	    how a bridge is asked to reach a bus BEHIND it; the primary bus is reached
	    with type-0 cycles, whose IDSEL encoding is decoded above.  Forwarding this
	    case would set cur_bus = 0 and hand the access to whichever primary-bus
	    device matched -- `i82378zb' is registered at 0:7:0 by DEVINIT below -- so
	    simply decoding `bus' and stopping there would replace a host kill with a
	    NEW MISROUTING.  Refuse it instead, matching `bus_pci_data_access''s own
	    empty-slot contract (bus_pci.c, the `dev == NULL' arm: all-ones at register
	    0, zero elsewhere) so the guest sees the ordinary "nothing there" answer.
	    Writes are discarded, which leaves backend state untouched.  */
	if (type1 && bus == 0) {		/*  #515  */
		odata = reg == 0? (uint64_t) -1 : 0;
	} else {
		/*  Pass PCI accesses onto bus_pci:  */
		bus_pci_setaddr(cpu, d->pci_data, bus, dev, func, reg);
		bus_pci_data_access(cpu, d->pci_data, writeflag == MEM_READ?
		    &odata : &idata, len, writeflag);
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}


DEVICE_ACCESS(lca_isa)
{
	unsigned int ofs, i;
	uint8_t byte;

	relative_addr >>= 5;

	/*
	 *  #530: the byte for ISA port P sits at buffer position (P & 3) % len
	 *  on BOTH arms -- the lane for the 21066's own len 4/8 accesses, and
	 *  the rule the write arm already applied wherever the old guard let
	 *  it run.  That guard's `ofs > len' exit(1) ended the host on a guest
	 *  byte access to a port 2 or 3 mod 4 or a word access to a port 3 mod
	 *  4 (ungated BWX; and at a port 3 mod 4 also the 1- or 2-byte head
	 *  of an unaligned load or store that memory_rw splits at 1 KB),
	 *  and the read arm discarded the
	 *  fetched byte at ofs == len.
	 *  One byte is forwarded whatever len is (the size field a<4:3> is
	 *  not decoded here).  len 0 has no producer; refuse it before the %.
	 */
	if (len == 0)
		return 0;
	ofs = (relative_addr & 3) % len;

	if (writeflag == MEM_WRITE) {
		byte = data[ofs];
		return cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +
		    relative_addr, &byte, 1, writeflag, CACHE_NONE);
	}

	cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,
	    &byte, 1, MEM_READ, CACHE_NONE);

	for (i=0; i<len; i++)
		data[i] = i == ofs? byte : 0x00;

	return 1;
}


/*
 *  #518 (lcabadval): one bounded announce per (device instance, reason).  Six
 *  IOC write arms used to end the host with fatal()+exit(1) on any value outside
 *  a tiny accepted set -- and the sets were WRONG, not merely harsh: the 21066
 *  HRM (Table 6-6) lists THIRTEEN legal W_MASK encodings where the model took
 *  one, and S6.4.14 REQUIRES SROM to write ZERO to W_BASE1, which was fatal.
 *  The arms below store the ARCHITECTED FIELDS, ignore reserved bits (type X),
 *  validate W_MASK by its field rule, and decline what the model cannot honour
 *  with this announce -- fatal() prints and returns (it cannot be silenced by
 *  -q, which is why a latch and not a verbosity flag).
 */
static void lca_ioc_announce(struct lca_data *d, int bit, const char *what,
	uint64_t v)
{
	if (d->warned & (1u << bit))
		return;
	d->warned |= 1u << bit;
	fatal("[ lca_ioc: %s: 0x%" PRIx64 "  (once) ]\n", what, v);
}


DEVICE_ACCESS(lca_ioc)
{
	uint64_t idata = 0, odata = 0;
	struct lca_data *d = (struct lca_data *) extra;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	switch (relative_addr + LCA_IOC_BASE) {

	case LCA_IOC_BASE:
		/*  Ignore? Linux reads from the base at startup.  */
		break;

	case LCA_IOC_CONF:
		if (writeflag == MEM_READ) {
			odata = d->ioc_conf;
		} else {
			/*  #518: was `if (idata & ~1) { fatal(); exit(1); }' with the
			    store BEFORE the check (#506 had widened its diagnostic).
			    HRM S6.2.9: IOC_CONF<1:0> is the CFG AD<1:0> field, and
			    bit 0 selects the configuration cycle TYPE; everything
			    above is reserved and is IGNORED, not fatal.  Bit 0
			    selects type-1 cycles and is what lca_pci_conf
			    reads (#515); bit 1 selects the CFG AD<1:0> encodings 10/11,
			    which are not configuration-cycle types -- stored and
			    announced once, not modelled.  (Pass 2: this comment first
			    called bit 1 the type-1 select; grok read lca_pci_conf.)  */
			d->ioc_conf = idata & 0x3ULL;
			if (idata & 0x2ULL)
				lca_ioc_announce(d, LCA_W_IOC_CONF_CFG1, "IOC_CONF<1> set"
				    " (CFG AD<1:0> = 10/11, not a configuration-cycle type):"
				    " stored, not modelled", idata);
		}
		break;

	case LCA_IOC_TBIA:
		/*  TLB Invalidate All.  */
		/*  TODO: For now, let's just ignore it.  */
		break;

	case LCA_IOC_TB_ENA:
		if (writeflag == MEM_READ) {
			odata = d->tlb_enable;
		} else {
			/*  #518: TEN is the only architected bit (HRM Table 6-13);
			    the rest are type X -- IGNORED on write, never fatal.  The
			    old arm stored the whole value and then died on it.  */
			d->tlb_enable = idata & IOC_TB_ENA_TEN;
		}
		break;

	case LCA_IOC_W_BASE0:
		if (writeflag == MEM_READ) {
			odata = d->window_base_0;
		} else {
			/*  #518: was a two-value whitelist + exit(1).  The HRM defines
			    this register by FIELDS -- W_BASE<31:20>, SG<32>, WEN<33> --
			    not by a list of numbers, and S6.4.14 REQUIRES SROM to write
			    zero here.  Store the fields (reserved bits dropped); the
			    window is not translated by this model, which is announced
			    once when any window is ENABLED.  */
			d->window_base_0 = idata & (IOC_W_BASE_W_BASE | IOC_W_BASE_SG | IOC_W_BASE_WEN);
			if (idata & IOC_W_BASE_WEN)
				lca_ioc_announce(d, LCA_W_IOC_WEN, "a DMA window was"
				    " enabled; window translation is not modelled", idata);
		}
		break;

	case LCA_IOC_W_MASK0:
		if (writeflag == MEM_READ) {
			odata = d->window_mask_0;
		} else {
			/*  #518: was `!= 0x700000ULL' + exit(1): ONE accepted value where
			    HRM Table 6-6 lists THIRTEEN (W_MASK<31:20> = 0, 1, 3, 7, ...
			    0xfff: a contiguous low-ones field), and the old arm STORED
			    before it checked.  Validate the field, store only when it is
			    legal, decline once otherwise with the previous value kept.  */
			{
				uint64_t v = idata & 0xfff00000ULL, f = v >> 20;
				if ((f & (f + 1)) == 0)
					d->window_mask_0 = v;
				else
					lca_ioc_announce(d, LCA_W_IOC_WMASK0, "unsupported"
					    " IOC_W_MASK0 encoding declined (HRM Table 6-6);"
					    " previous value kept", idata);
			}
		}
		break;

	case LCA_IOC_W_T_BASE0:
		if (writeflag == MEM_READ) {
			odata = d->window_t_base_0;
		} else {
			d->window_t_base_0 = idata;
			/*  TODO: Actually implement this.  */
		}
		break;

	case LCA_IOC_W_BASE1:
		if (writeflag == MEM_READ) {
			odata = d->window_base_1;
		} else {
			/*  #518: was a ONE-value whitelist + exit(1) -- and the one value
			    was not zero, which S6.4.14 item 3 requires SROM to write.
			    Same disposition as W_BASE0 above.  */
			d->window_base_1 = idata & (IOC_W_BASE_W_BASE | IOC_W_BASE_SG | IOC_W_BASE_WEN);
			if (idata & IOC_W_BASE_WEN)
				lca_ioc_announce(d, LCA_W_IOC_WEN, "a DMA window was"
				    " enabled; window translation is not modelled", idata);
		}
		break;

	case LCA_IOC_W_MASK1:
		if (writeflag == MEM_READ) {
			odata = d->window_mask_1;
		} else {
			/*  #518: was `!= 0x3ff00000ULL' + exit(1): ONE accepted value where
			    HRM Table 6-6 lists THIRTEEN (W_MASK<31:20> = 0, 1, 3, 7, ...
			    0xfff: a contiguous low-ones field), and the old arm STORED
			    before it checked.  Validate the field, store only when it is
			    legal, decline once otherwise with the previous value kept.  */
			{
				uint64_t v = idata & 0xfff00000ULL, f = v >> 20;
				if ((f & (f + 1)) == 0)
					d->window_mask_1 = v;
				else
					lca_ioc_announce(d, LCA_W_IOC_WMASK1, "unsupported"
					    " IOC_W_MASK1 encoding declined (HRM Table 6-6);"
					    " previous value kept", idata);
			}
		}
		break;

	case LCA_IOC_W_T_BASE1:
		if (writeflag == MEM_READ) {
			odata = d->window_t_base_1;
		} else {
			d->window_t_base_1 = idata;
			/*  TODO: Actually implement this.  */
		}
		break;

	default:
		/*  #518: was fatal()+exit(1) for ANY offset the switch does not
		    list.  Decline the write (no IOC register changes; only the announce
		    latch moves), answer a read with
		    zero (odata is already 0), announce each direction once.  The
		    value keeps #506's full width.  NOT all of these offsets are
		    unimplemented HOLES: STAT0 (+0x040), STAT1 (+0x060), SFT_RST
		    (+0x0c0) and PAR_DIS (+0x0e0) are DOCUMENTED registers this
		    model has never had, and S6.4.14 items 1-2 require SROM to
		    write SFT_RST and STAT0 -- those now survive as declined writes
		    instead of ending the process, and are filed (lcaiocstat0) for
		    an implementation, which this decline is not.  (grok, pass 2)  */
		{
			int bit = writeflag == MEM_WRITE ?
			    LCA_W_IOC_DEF_W : LCA_W_IOC_DEF_R;
			if (!(d->warned & (1u << bit))) {
				d->warned |= 1u << bit;
				fatal("[ lca_ioc: unimplemented %s to offset 0x%x",
				    writeflag == MEM_WRITE? "write" : "read", (int)
				    relative_addr);
				if (writeflag == MEM_WRITE)
					fatal(": 0x%" PRIx64 " -- declined",
					    (uint64_t)idata);	/*  #506  */
				else
					fatal(" -- answered with zero");
				fatal("  (once per direction) ]\n");
			}
		}
		break;
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}


DEVINIT(lca)
{
	char *interrupt_path;
	struct interrupt interrupt_template;
	struct lca_data *d;

	CHECK_ALLOCATION(d = (struct lca_data *) malloc(sizeof(struct lca_data)));
	memset(d, 0, sizeof(struct lca_data));

	/*  Register a PCI bus:  */
	d->pci_data = bus_pci_init(
	    devinit->machine,
	    "TODO: irq"		/*  pciirq: TODO  */,
	    LCA_PCI_SIO,	/*  pci device io offset  */
	    0x00000000,		/*  pci device mem offset: TODO  */
	    0x00000000,		/*  PCI portbase: TODO  */
	    0x00000000,		/*  PCI membase: TODO  */
	    "TODO: pci irq base",	/*  PCI irqbase: TODO  */
	    LCA_ISA_BASE,	/*  ISA portbase  */
	    LCA_ISA_MEMBASE,	/*  ISA membase  */
	    "TODO: irqbase isa");                /*  ISA irqbase: TODO  */

	/*  Add the "sio0" controller (as seen by NetBSD):  */
	bus_pci_add(devinit->machine, d->pci_data, devinit->machine->memory,
	    0, 7, 0, "i82378zb");

	memory_device_register(devinit->machine->memory, "lca_pci_conf",
	    LCA_PCI_CONF, 0x20000000, dev_lca_pci_conf_access, (void *)d,
	    DM_DEFAULT, NULL);

	memory_device_register(devinit->machine->memory, "lca_isa",
	    LCA_PCI_SIO, 0x10000 << 5, dev_lca_isa_access, (void *)d,
	    DM_DEFAULT, NULL);

	memory_device_register(devinit->machine->memory, "lca_ioc",
	    LCA_IOC_BASE, 0x20000000, dev_lca_ioc_access, (void *)d,
	    DM_DEFAULT, NULL);

	CHECK_ALLOCATION(interrupt_path = (char *)
	    malloc(strlen(devinit->machine->path) + 10));
	snprintf(interrupt_path, strlen(devinit->machine->path) + 10,
	    "%s.lca", devinit->machine->path);

	memset(&interrupt_template, 0, sizeof(interrupt_template));
	interrupt_template.line = 0;
	interrupt_template.name = interrupt_path;
	interrupt_template.extra = d;
	interrupt_template.interrupt_assert = lca_interrupt_assert;
	interrupt_template.interrupt_deassert = lca_interrupt_deassert;
	interrupt_handler_register(&interrupt_template);

	bus_isa_init(devinit->machine, interrupt_path,
	    BUS_ISA_IDE0 | BUS_ISA_IDE1, LCA_ISA_BASE, LCA_ISA_MEMBASE);

	return 1;
}

