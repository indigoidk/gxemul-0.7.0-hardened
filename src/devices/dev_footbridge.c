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
 *  COMMENT: DC21285 "Footbridge" controller; used in Netwinder and Cats
 *
 *  TODO:
 *	o)  Add actual support for the fcom serial port.
 *	o)  FIQs.
 *	o)  Pretty much everything else as well :)  (This entire thing
 *	    is a quick hack to work primarily with NetBSD and OpenBSD
 *	    as guest OSes.)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "bus_pci.h"
#include "console.h"
#include "cpu.h"
#include "device.h"
#include "devices.h"
#include "machine.h"
#include "memory.h"
#include "misc.h"
#include "timer.h"

#include "thirdparty/dc21285reg.h"


#define	DEV_FOOTBRIDGE_TICK_SHIFT	14
#define	DEV_FOOTBRIDGE_LENGTH		0x400

#define	N_FOOTBRIDGE_TIMERS		4

struct footbridge_data {
	struct interrupt irq;

	struct pci_data *pcibus;

	int		console_handle;

	uint32_t	timer_load[N_FOOTBRIDGE_TIMERS];
	uint32_t	timer_value[N_FOOTBRIDGE_TIMERS];
	uint32_t	timer_control[N_FOOTBRIDGE_TIMERS];

	struct interrupt timer_irq[N_FOOTBRIDGE_TIMERS];
	struct timer	*timer[N_FOOTBRIDGE_TIMERS];
	int		pending_timer_interrupts[N_FOOTBRIDGE_TIMERS];
	/*  #442: the per-timer bound on the counter above, one emulated second of
	    that timer's delivered rate, recomputed by reload_timer_value().  */
	int		pending_bound[N_FOOTBRIDGE_TIMERS];

	int		irq_asserted;

	uint32_t	irq_status;
	uint32_t	irq_enable;

	uint32_t	fiq_status;
	uint32_t	fiq_enable;
};


/*
 *  #442: the counter above was incremented without a bound, so a guest that armed
 *  a timer and never acked overflowed it -- and on overflow the int goes negative,
 *  DEVICE_TICK's `> 0` is false, and THE EMULATED CLOCK DELIVERS NOTHING FOR 2^31
 *  FURTHER TICKS.  Reproduced at rung 3 on an unmodified -E cats: two MMIO writes,
 *  then 42.95 s to the wrap and a 40 s dead window, measured three times.
 *
 *  THE COMPARISON PRECEDES THE INCREMENT, and that is not a style choice.  An
 *  increment-then-check form -- which is what the one in-tree precedent for this
 *  (dev_luna88k.c:252) actually does -- reintroduces the UB it is meant to remove
 *  if the counter ever reaches INT_MAX, because the ++ has already executed by the
 *  time the check runs.  luna88k is safe only because its own reset keeps the
 *  counter far below INT_MAX; the FORM is still the wrong one to copy.
 *
 *  Reset to 1 rather than 0, so one interrupt is still owed -- coalescing the debt
 *  rather than discarding it.  MEASURED to matter: a reset-to-0 mutant survives the
 *  rung-3 drain probe and two of the three offline rows; only the trough row
 *  separates them (0 against 1).
 *
 *  NO MESSAGE FROM HERE.  These run in the SIGALRM handler and debugmsg() is
 *  printf underneath, so copying luna88k's diagnostic would put four printf paths
 *  inside a signal handler -- and timer.c:274-279 states that nothing in that file
 *  prints from the handler.  (luna88k's own callback does, which is a defect there;
 *  filed, not fixed here.)  If a diagnostic is ever wanted, latch a flag here and
 *  report from DEVICE_TICK, which runs in the main loop.
 */
static void footbridge_pending(struct footbridge_data *d, int nr)
{
	if (d->pending_timer_interrupts[nr] >= d->pending_bound[nr])
		d->pending_timer_interrupts[nr] = 1;
	else
		d->pending_timer_interrupts[nr] ++;
}

static void timer_tick0(struct timer *t, void *extra)
{ footbridge_pending((struct footbridge_data *)extra, 0); }
static void timer_tick1(struct timer *t, void *extra)
{ footbridge_pending((struct footbridge_data *)extra, 1); }
static void timer_tick2(struct timer *t, void *extra)
{ footbridge_pending((struct footbridge_data *)extra, 2); }
static void timer_tick3(struct timer *t, void *extra)
{ footbridge_pending((struct footbridge_data *)extra, 3); }


/*
 *  #432: ONE interpretation of the load register, used by BOTH consumers.
 *
 *  THE CRASH.  DEVICE_TICK computed `random() % timer_load[i]`, and TIMER_x_LOAD accepts a
 *  guest-written zero (`idata & TIMER_MAX_VAL`), so a guest could divide by zero and take the
 *  HOST process down -- reproduced as SIGFPE, exit 136, by two seats independently.
 *
 *  THERE ARE TWO ROUTES TO IT, and only one is ours.  Route 1: a zero load makes the rate
 *  +INF, which before #427/#428 meant interval 0.0 and a catch-up loop that never advanced,
 *  so the machine froze before this function ran; the clamp and the bound opened that path.
 *  ROUTE 2 PREDATES BOTH: TIMER_x_LOAD does not clear pending_timer_interrupts (TIMER_x_CONTROL
 *  below does), so an ORDINARY LEGAL timer accrues a backlog and a later write of zero divides
 *  -- measured on the pre-#427 core, it crashes there too.  DEVICE_TICK runs from machine_run(),
 *  the main loop, not from the signal handler, so the CPU reaches the divide between signals.
 *
 *  WHY A HELPER RATHER THAN TWO GUARDS.  Three seats converged on this independently, and the
 *  measuring seat REFUTED each single-site alternative: guarding only this function still
 *  SIGFPEs by route 2 (and is the most dangerous option precisely because it passes the obvious
 *  test); guarding only the modulo leaves the backlog growing 1048576 per signal, reaching
 *  INT_MAX in ~31 s; and normalising at the guest write corrupts read-back -- TIMER_x_LOAD
 *  returns the stored value, so the guest would read something it never wrote, which invents an
 *  answer to a question the hardware documentation we lack would have to settle.
 *
 *  THE REGISTER STAYS RAW.  timer_load[] keeps exactly what the guest wrote, masked to 24 bits.
 *  Only the DERIVED quantities are interpreted here, and they are model-internal.
 *
 *  ZERO MEANS FULL PERIOD (2^24), and it is a CHOICE UNDER A DOCUMENTED UNKNOWN, not a fact.
 *
 *  The 21285 datasheet was obtained for this round (_scratchpad/dc21285.pdf, Intel order
 *  278115-001, Sept 1998).  SS 7.3.39 (p. 7-50) specifies TimerNLoad and its reset value without
 *  saying what a count of zero does, and a search of the full extraction for "minimum count" /
 *  "nonzero" / "reaches zero" turns up no equivalent of the 8254's Figure 22.  So the absence is
 *  MEASURED, not assumed -- a stronger thing to say than the guess it replaces.
 *
 *  BUT "SILENT" OVERSTATES IT BY HALF, and the pass-2 review caught that in this round's favour.
 *  SS 7.3.41 bit 6 says a FREE-RUNNING timer "will wrap to FFFFFFh and continue to decrement",
 *  which together with SS 6.4's 24-bit down counter DETERMINES the free-run case: a load of zero
 *  gives a period of exactly 2^24, i.e. the mapping below is datasheet-IMPLIED there -- and
 *  free-running is bit 6 == 0, the reset mode.  It is genuinely unknown only for PERIODIC.
 *
 *  The choice therefore rests on failure asymmetry, and there are THREE candidate truths rather
 *  than the two first written here.  Implement full-period when the truth is "disabled" and a
 *  guest gets a few unwanted interrupts on a timer it explicitly enabled -- noisy, visible,
 *  recoverable.  Implement "disabled" when the truth is full-period and the guest waits forever
 *  on a tick that never comes -- silent, and it hangs at boot.  And the third, which the first
 *  draft omitted: read mechanically, PERIODIC mode with a zero load reloads zero and interrupts
 *  every prescaled clock -- a max-rate storm, the DANGEROUS branch rather than the silent one.
 *  Full-period is the only choice that survives all three, so the argument was understating its
 *  own robustness.
 *
 *  A SECOND SUPPORT WAS ALSO WITHDRAWN, for the same reason as the third and by a seat whose
 *  answer sat unread for a day.  It said the 24-bit mask aliases "a legitimate guest write of
 *  0x1000000 -- one full wrap -- to zero, so this mapping keeps the rate continuous across the
 *  register's own truncation".  The datasheet closes it: SS 7.3.39 gives TimerNLoad as bits 23:0
 *  R/W with "31:24 -- R Read only as 0", so bit 24 is not a truncated write at all, it is OUTSIDE
 *  THE WRITABLE FIELD.  There is no wrap to be continuous across, and continuity beyond a
 *  register's own width is a modelling preference dressed up as arithmetic.  Zero -> 2^24 stands
 *  on the three-way argument above and on nothing else; what silicon does with a zero load
 *  remains UNKNOWN, and SS 7.3.39 is silent on it.
 *
 *  A THIRD ARGUMENT WAS WITHDRAWN WHEN THE DATASHEET ARRIVED, and it is recorded because the
 *  withdrawal matters more than the argument did.  An earlier draft of this comment said
 *  "devinit resets every load to TIMER_MAX_VAL, so the model's own convention is full width".
 *  The datasheet says TimerNLoad and TimerNControl BOTH reset to 0 (SS 7.3.39, SS 7.3.41), so
 *  this model's reset values are themselves wrong -- that line was citing a model bug as
 *  evidence.  The divergence is filed; it is not fixed here.
 *
 *  THE WIDTH FIX IS NOT SEPARABLE FROM THE ZERO FIX.  The old `int cycles` with `cycles <<= 8`
 *  overflowed for exactly half the legal 24-bit range (first bad load 0x800000), yielding a
 *  NEGATIVE frequency that the core's floor clamp silently turned into one tick per ~3.2 years
 *  -- reachable with NO load write at all, since the reset load is TIMER_MAX_VAL and a single
 *  write of ENABLE|FCLK_256 gets there.  And mapping zero to 2^24 while leaving `int` gives
 *  2^24 << 8 == 2^32 == 0, which is +INF AGAIN: the obvious zero-guard RE-CREATES the bug it
 *  removes.  Hence uint64_t, and multiplication rather than a signed shift.  Found independently
 *  by three seats.
 *
 *  (8253 maps a zero divisor to "disabled" instead -- and a pass-2 seat caught that an earlier
 *  version of this parenthetical argued the point BACKWARDS.  It said the 8253's 16-bit counter
 *  "has no equivalent of the 24-bit aliasing above", but writing 0x10000 to a 16-bit latch aliases
 *  to zero in exactly the same way -- which is precisely WHY the Intel 8254 datasheet defines a
 *  programmed count of 0 as 2^16 (231164-005, p. 17).  So the aliasing argument REINFORCES this
 *  mapping rather than distinguishing it, and dev_8253.c's "disabled" is the one that looks wrong
 *  against its own hardware.  Filed as its own item; not changed here.)
 */
/*
 *  with_prescaler distinguishes the two consumers, and it is NOT a convenience flag -- getting
 *  it wrong is a defect the measuring seat caught in its own first proposal.  The prescaler
 *  slows the RATE; it does not widen the COUNTER.  Feeding the prescaled period to the modulo
 *  put values up to 0x7fffca11 into a 24-bit register that the guest can read back -- measured,
 *  19833 of 20000 ticks out of range.  So: the rate consumer prescales, the counter consumer
 *  does not, and both get their never-zero span from this one function.
 */
static uint64_t footbridge_effective_cycles(uint32_t load, uint32_t control,
	int with_prescaler)
{
	uint64_t cycles = load;

	if (cycles == 0)
		cycles = (uint64_t)TIMER_MAX_VAL + 1;	/*  0x1000000 == 2^24  */

	if (!with_prescaler)
		return cycles;

	/*  The prescaler scales the PERIOD.  It must not be a signed shift, and the order
	    matters: TIMER_EXTERNAL is FCLK_16|FCLK_256, so test the pair first or 0x0C reads
	    as a bare FCLK_16 by luck of the `else if`.  */
	if ((control & (TIMER_FCLK_16 | TIMER_FCLK_256))
	    == (TIMER_FCLK_16 | TIMER_FCLK_256)) {
		/*  TIMER_EXTERNAL (0x0C): a LEGAL encoding, and this is now DATASHEET-BACKED
		    rather than inferred from the header.  The 21285 datasheet obtained for this
		    round gives TimerNControl bits 3:2 as 00=fclk_in, 01=fclk_in/16,
		    10=fclk_in/256, 11=External event (SS 7.3.41, p. 7-51; SS 6.4, p. 6-11 lists
		    the same four).  It used to reach fatal()+exit(1) below, so a CONFORMING guest
		    selecting the external clock source killed the host -- the same defect class as
		    the divide and arguably likelier, being a documented mode rather than a
		    malformed value.  The RATE an external source would give depends on a pin this
		    model has no signal for (irq_in_l), so it is genuinely not derivable here and
		    is NOT invented: the unprescaled period keeps the timer sane and the emulator
		    alive.  Modelling the external event properly is filed.  */
		;
	} else if (control & TIMER_FCLK_16)
		cycles *= 16;
	else if (control & TIMER_FCLK_256)
		cycles *= 256;

	return cycles;
}


static void reload_timer_value(struct cpu *cpu, struct footbridge_data *d,
	int timer_nr)
{
	double freq = (double)cpu->machine->emulated_hz;

	freq /= (double) footbridge_effective_cycles(d->timer_load[timer_nr],
	    d->timer_control[timer_nr], 1);

	d->timer_value[timer_nr] = d->timer_load[timer_nr];

	/*
	 *  #442: one emulated second of THIS timer's delivered rate, clamped.
	 *
	 *  The ceiling is DERIVED, not chosen: TIMER_MAX_CATCHUP ticks per timer
	 *  per signal at TIMER_BASE_FREQUENCY signals per second is the most the
	 *  timer core can ever deliver to one timer in one wall second, so a cap
	 *  at that value can never throttle a legitimately fast timer.
	 *
	 *  IT IS ALSO NOT OPTIONAL, which a purely rate-relative bound hides.
	 *  MEASURED: with `-I 2147483647` and load 1 the requested rate is
	 *  2147483647.0, so (int)freq is INT_MAX and a bound of "the timer's own
	 *  rate" never fires -- the overflow returns, reachable through a
	 *  documented command-line flag.  Deleting these two lines is the
	 *  smallest edit that still passes the rung-3 probe.
	 *
	 *  Floor 1, because a 0.0116 Hz timer would otherwise bound at 0 and the
	 *  counter would be pinned there.  Comparisons are negated so a NaN freq
	 *  lands on the ceiling rather than falling through, matching
	 *  timer_clamp_freq()'s idiom.
	 *
	 *  Set BEFORE timer_add()/timer_update_frequency() below: the SIGALRM can
	 *  land between them, and a callback that fires against a stale or zero
	 *  bound is the window this whole round exists to close.
	 */
	{
		double bound = freq;
		if (!(bound <= (double)TIMER_MAX_CATCHUP * TIMER_BASE_FREQUENCY))
			bound = (double)TIMER_MAX_CATCHUP * TIMER_BASE_FREQUENCY;
		if (!(bound >= 1.0))
			bound = 1.0;
		d->pending_bound[timer_nr] = (int) bound;
	}

	/*  printf("%i: %i -> %f Hz\n", timer_nr,
	    d->timer_load[timer_nr], freq);  */

	if (d->timer[timer_nr] == NULL) {
		switch (timer_nr) {
		case 0:	d->timer[0] = timer_add(freq, timer_tick0, d); break;
		case 1:	d->timer[1] = timer_add(freq, timer_tick1, d); break;
		case 2:	d->timer[2] = timer_add(freq, timer_tick2, d); break;
		case 3:	d->timer[3] = timer_add(freq, timer_tick3, d); break;
		}
	} else {
		timer_update_frequency(d->timer[timer_nr], freq);
	}
}


/*
 *  The 4 footbridge timers should decrease and cause interrupts. Periodic
 *  interrupts restart as soon as they are acknowledged, non-periodic
 *  interrupts need to be "reloaded" to restart.
 *
 *  TODO: Hm. I thought I had solved this, but it didn't quite work.
 *        This needs to be re-checked against documentation, sometime.
 */
DEVICE_TICK(footbridge)
{
	struct footbridge_data *d = (struct footbridge_data *) extra;
	int i;

	for (i=0; i<N_FOOTBRIDGE_TIMERS; i++) {
		if (d->timer_control[i] & TIMER_ENABLE) {
			if (d->pending_timer_interrupts[i] > 0) {
				/*  #432: the same never-zero span, WITHOUT the
				    prescaler -- this is a 24-bit counter, and the
				    prescaler slows the rate rather than widening
				    it.  */
				d->timer_value[i] = random() %
				    footbridge_effective_cycles(d->timer_load[i],
				    d->timer_control[i], 0);
				INTERRUPT_ASSERT(d->timer_irq[i]);
			}
		}
	}
}


/*
 *  footbridge_interrupt_assert():
 */
void footbridge_interrupt_assert(struct interrupt *interrupt)
{
	struct footbridge_data *d = (struct footbridge_data *) interrupt->extra;
	d->irq_status |= interrupt->line;

	// Patch from NetBSD:
	// "fix hang interrupt issue. Always assert the irq's even if we have
	//  already asserted the global irq for the device. prevents hangs with
	//  cats."
	if ((d->irq_status & d->irq_enable) /* && !d->irq_asserted */) {
		d->irq_asserted = 1;
		INTERRUPT_ASSERT(d->irq);
	}
}


/*
 *  footbridge_interrupt_deassert():
 */
void footbridge_interrupt_deassert(struct interrupt *interrupt)
{
	struct footbridge_data *d = (struct footbridge_data *) interrupt->extra;
	d->irq_status &= ~interrupt->line;

	if (!(d->irq_status & d->irq_enable) && d->irq_asserted) {
		d->irq_asserted = 0;
		INTERRUPT_DEASSERT(d->irq);
	}
}


/*
 *  Reading the byte at 0x79000000 is a quicker way to figure out which ISA
 *  interrupt has occurred (and acknowledging it at the same time), than
 *  dealing with the legacy 0x20/0xa0 ISA ports.
 */
DEVICE_ACCESS(footbridge_isa)
{
	/*  struct footbridge_data *d = extra;  */
	uint64_t idata = 0, odata = 0;
	int x;

	if (writeflag == MEM_WRITE) {
		idata = memory_readmax64(cpu, data, len);
		fatal("[ footbridge_isa: WARNING/TODO: write! idata = 0x%016" PRIx64" ]\n", idata);
	}

	x = cpu->machine->isa_pic_data.last_int;
	if (x < 8)
		odata = cpu->machine->isa_pic_data.pic1->irq_base + x;
	else
		odata = cpu->machine->isa_pic_data.pic2->irq_base + x - 8;

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}


/*
 *  Reset pin at ISA port 0x338, at least in the NetWinder:
 *
 *  TODO: NOT WORKING YET!
 */
DEVICE_ACCESS(footbridge_reset)
{
	uint64_t idata = 0;

	if (writeflag == MEM_WRITE) {
		idata = memory_readmax64(cpu, data, len);
		if (idata & 0x40) {
			debug("[ footbridge_reset: GP16: Halting. ]\n");
			/*  #220: (Codex/Fable) cpu->running=0 already halts cleanly;
			    the col-0 exit(1) was a debug hack that kills the host.  */
			cpu->running = 0;
		}
	}

	return 1;
}


/*
 *  The Footbridge PCI configuration space is implemented as a direct memory
 *  space (i.e. not one port for addr and one port for data). This function
 *  translates that into bus_pci calls.
 */
DEVICE_ACCESS(footbridge_pci)
{
	struct footbridge_data *d = (struct footbridge_data *) extra;
	uint64_t idata = 0, odata = 0;
	int bus, dev, func, reg;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len|MEM_PCI_LITTLE_ENDIAN);

	/*  Decompose the (direct) address into its components:  */
	bus_pci_decompose_1(relative_addr, &bus, &dev, &func, &reg);
	bus_pci_setaddr(cpu, d->pcibus, bus, dev, func, reg);

	if (bus == 255) {
		fatal("[ footbridge DEBUG ERROR: bus 255 unlikely,"
		    " pc (might not be updated) = 0x%08x ]\n", (int)cpu->pc);
		/*  #220: (Codex/Fable) don't exit() the host on a guest PCI
		    access to the (unlikely) bus 255; treat it as handled.  */
		return 1;
	}

	debug("[ footbridge pci: %s bus %i, device %i, function %i, register "
	    "%i ]\n", writeflag == MEM_READ? "read from" : "write to", bus,
	    dev, func, reg);

	bus_pci_data_access(cpu, d->pcibus, writeflag == MEM_READ?
	    &odata : &idata, len, writeflag);

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len|MEM_PCI_LITTLE_ENDIAN, odata);

	return 1;
}


DEVICE_ACCESS(footbridge)
{
	struct footbridge_data *d = (struct footbridge_data *) extra;
	uint64_t idata = 0, odata = 0;
	int timer_nr = 0;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	if (relative_addr >= TIMER_1_LOAD && relative_addr <= TIMER_4_CLEAR) {
		timer_nr = (relative_addr >> 5) & (N_FOOTBRIDGE_TIMERS - 1);
		relative_addr &= ~0x060;
	}

	switch (relative_addr) {

	case VENDOR_ID:
		odata = 0x1011;  /*  DC21285_VENDOR_ID  */
		break;

	case DEVICE_ID:
		odata = 0x1065;  /*  DC21285_DEVICE_ID  */
		break;

	case 0x04:
	case 0x0c:
	case 0x10:
	case 0x14:
	case 0x18:
		/*  TODO. Written to by Linux.  */
		break;

	case REVISION:
		odata = 3;  /*  footbridge revision number  */
		break;

	case PCI_ADDRESS_EXTENSION:
		/*  TODO: Written to by Linux.  */
		if (writeflag == MEM_WRITE && idata != 0)
			fatal("[ footbridge: TODO: write to PCI_ADDRESS_"
			    "EXTENSION: 0x%llx ]\n", (long long)idata);
		break;

	case SA_CONTROL:
		/*  Read by Linux:  */
		odata = PCI_CENTRAL_FUNCTION;
		break;

	case UART_DATA:
		if (writeflag == MEM_WRITE)
			console_putchar(d->console_handle, idata);
		break;

	case UART_RX_STAT:
		/*  TODO  */
		odata = 0;
		break;

	case UART_FLAGS:
		odata = UART_TX_EMPTY;
		break;

	case IRQ_STATUS:
		if (writeflag == MEM_READ)
			odata = d->irq_status & d->irq_enable;
		else {
			fatal("[ WARNING: footbridge write to irq status? ]\n");
			exit(1);
		}
		break;

	case IRQ_RAW_STATUS:
		if (writeflag == MEM_READ)
			odata = d->irq_status;
		else {
			fatal("[ footbridge write to irq_raw_status ]\n");
			exit(1);
		}
		break;

	case IRQ_ENABLE_SET:
		if (writeflag == MEM_WRITE) {
			d->irq_enable |= idata;
			if (d->irq_status & d->irq_enable)
				INTERRUPT_ASSERT(d->irq);
			else
				INTERRUPT_DEASSERT(d->irq);
		} else {
			odata = d->irq_enable;
			fatal("[ WARNING: footbridge read from "
			    "ENABLE SET? ]\n");
			exit(1);
		}
		break;

	case IRQ_ENABLE_CLEAR:
		if (writeflag == MEM_WRITE) {
			d->irq_enable &= ~idata;
			if (d->irq_status & d->irq_enable)
				INTERRUPT_ASSERT(d->irq);
			else
				INTERRUPT_DEASSERT(d->irq);
		} else {
			odata = d->irq_enable;
			fatal("[ WARNING: footbridge read from "
			    "ENABLE CLEAR? ]\n");
			exit(1);
		}
		break;

	case FIQ_STATUS:
		if (writeflag == MEM_READ)
			odata = d->fiq_status & d->fiq_enable;
		else {
			fatal("[ WARNING: footbridge write to fiq status? ]\n");
			exit(1);
		}
		break;

	case FIQ_RAW_STATUS:
		if (writeflag == MEM_READ)
			odata = d->fiq_status;
		else {
			fatal("[ footbridge write to fiq_raw_status ]\n");
			exit(1);
		}
		break;

	case FIQ_ENABLE_SET:
		if (writeflag == MEM_WRITE)
			d->fiq_enable |= idata;
		break;

	case FIQ_ENABLE_CLEAR:
		if (writeflag == MEM_WRITE)
			d->fiq_enable &= ~idata;
		break;

	case TIMER_1_LOAD:
		if (writeflag == MEM_READ)
			odata = d->timer_load[timer_nr];
		else {
			d->timer_load[timer_nr] = idata & TIMER_MAX_VAL;
			reload_timer_value(cpu, d, timer_nr);
			/*  debug("[ footbridge: timer %i (1-based), "
			    "value %i ]\n", timer_nr + 1,
			    (int)d->timer_value[timer_nr]);  */
			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
		}
		break;

	case TIMER_1_VALUE:
		if (writeflag == MEM_READ)
			odata = d->timer_value[timer_nr];
		else
			d->timer_value[timer_nr] = idata & TIMER_MAX_VAL;
		break;

	case TIMER_1_CONTROL:
		if (writeflag == MEM_READ)
			odata = d->timer_control[timer_nr];
		else {
			d->timer_control[timer_nr] = idata;
			/*  #432: both prescaler bits set is TIMER_EXTERNAL
			    (0x0C, dc21285reg.h:364) -- a LEGAL named encoding,
			    and it used to reach fatal()+exit(1) right here, so a
			    guest selecting the external clock source KILLED THE
			    HOST.  Arguably likelier than the zero load, since it
			    is a documented mode rather than a malformed value.
			    The rate an external clock would actually give is
			    UNKNOWN and is NOT invented: footbridge_effective_cycles()
			    now gives the encoding a defined, survivable meaning
			    (the unprescaled period), and the real semantics are
			    filed for a round that has a datasheet.  */
			if (idata & TIMER_ENABLE) {
				reload_timer_value(cpu, d, timer_nr);
			} else {
				d->pending_timer_interrupts[timer_nr] = 0;
			}
			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
		}
		break;

	case TIMER_1_CLEAR:
		if (d->timer_control[timer_nr] & TIMER_MODE_PERIODIC) {
			reload_timer_value(cpu, d, timer_nr);
		}

		if (d->pending_timer_interrupts[timer_nr] > 0) {
			d->pending_timer_interrupts[timer_nr] --;
		}

		INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
		break;

	case SDRAM_BA_MASK:
		if (writeflag == MEM_READ) {
			fatal("[ footbridge read from sdram_ba_mask ]\n");
			exit(1);
		} else {
			switch (idata) {
			case SDRAM_MASK_256KB:
			case SDRAM_MASK_512KB:
			case SDRAM_MASK_1MB:
			case SDRAM_MASK_2MB:
			case SDRAM_MASK_4MB:
			case SDRAM_MASK_8MB:
			case SDRAM_MASK_16MB:
			case SDRAM_MASK_32MB:
			case SDRAM_MASK_64MB:
			case SDRAM_MASK_128MB:
			case SDRAM_MASK_256MB:
				break;
			default:
				fatal("[ footbridge write to sdram_ba_mask "
				    "%#llx ]\n", (long long)idata);
				break;
			}
		}
		break;
	case SDRAM_BA_OFFSET:
		if (writeflag == MEM_READ) {
			fatal("[ footbridge read from sdram_ba_offset ]\n");
			exit(1);
		} else {
			if (idata != 0)
				fatal("[ footbridge write to sdram_ba_offset "
				    "%#llx ]\n", (long long)idata);
		}
		break;

	default:if (writeflag == MEM_READ) {
			fatal("[ footbridge: read from 0x%x ]\n",
			    (int)relative_addr);
		} else {
			fatal("[ footbridge: write to 0x%x: 0x%llx ]\n",
			    (int)relative_addr, (long long)idata);
		}
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}


DEVINIT(footbridge)
{
	struct footbridge_data *d;
	char irq_path[300], irq_path_isa[400];
	uint64_t pci_addr = 0x7b000000;
	int i;

	CHECK_ALLOCATION(d = (struct footbridge_data *) malloc(sizeof(struct footbridge_data)));
	memset(d, 0, sizeof(struct footbridge_data));

	/*
	 *  #442: the memset leaves pending_bound[] at 0, and a bound of 0 would pin
	 *  the counter at 1 rather than bounding it.  That is UNREACHABLE today --
	 *  reload_timer_value() sets the bound, and it is also the only thing that
	 *  ever creates a struct timer, so no callback can fire before a bound
	 *  exists.  Initialised here anyway, because that is a two-step argument
	 *  about a signal handler and a later edit that adds a timer elsewhere would
	 *  silently break it.  The ceiling is the safe default: it can never
	 *  throttle, only bound.
	 */
	for (i = 0; i < N_FOOTBRIDGE_TIMERS; i++)
		d->pending_bound[i] = TIMER_MAX_CATCHUP * TIMER_BASE_FREQUENCY;

	/*  Connect to the CPU which this footbridge will interrupt:  */
	INTERRUPT_CONNECT(devinit->interrupt_path, d->irq);

	/*  DC21285 register access:  */
	memory_device_register(devinit->machine->memory, devinit->name,
	    devinit->addr, DEV_FOOTBRIDGE_LENGTH,
	    dev_footbridge_access, d, DM_DEFAULT, NULL);

	/*  ISA interrupt status/acknowledgement:  */
	memory_device_register(devinit->machine->memory, "footbridge_isa",
	    0x79000000, 8, dev_footbridge_isa_access, d, DM_DEFAULT, NULL);

	/*  The "fcom" console:  */
	d->console_handle = console_start_slave(devinit->machine, "fcom", 0);

	/*  Register 32 footbridge interrupts:  */
	snprintf(irq_path, sizeof(irq_path), "%s.footbridge",
	    devinit->interrupt_path);
	for (i=0; i<32; i++) {
		struct interrupt interrupt_template;
		char tmpstr[600];

		memset(&interrupt_template, 0, sizeof(interrupt_template));
		interrupt_template.line = (uint32_t)1 << i;
		snprintf(tmpstr, sizeof(tmpstr), "%s.%i", irq_path, i);
		interrupt_template.name = tmpstr;

		interrupt_template.extra = d;
		interrupt_template.interrupt_assert =
		    footbridge_interrupt_assert;
		interrupt_template.interrupt_deassert =
		    footbridge_interrupt_deassert;
		interrupt_handler_register(&interrupt_template);

		/*  Connect locally to some interrupts:  */
		if (i>=IRQ_TIMER_1 && i<=IRQ_TIMER_4)
			INTERRUPT_CONNECT(tmpstr, d->timer_irq[i-IRQ_TIMER_1]);
	}

	switch (devinit->machine->machine_type) {
	case MACHINE_CATS:
		snprintf(irq_path_isa, sizeof(irq_path_isa), "%s.10", irq_path);
		break;
	case MACHINE_NETWINDER:
		snprintf(irq_path_isa, sizeof(irq_path_isa), "%s.11", irq_path);
		break;
	default:fatal("footbridge unimpl machine type\n");
		exit(1);
	}

	/*  A PCI bus:  */
	d->pcibus = bus_pci_init(
	    devinit->machine,
	    irq_path,
	    0x7c000000,		/*  PCI device io offset  */
	    0x80000000,		/*  PCI device mem offset  */
	    0x00000000,		/*  PCI port base  */
	    0x00000000,		/*  PCI mem base  */
	    irq_path,		/*  PCI irq base  */
	    0x7c000000,		/*  ISA port base  */
	    0x80000000,		/*  ISA mem base  */
	    irq_path_isa);	/*  ISA port base  */

	/*  ... with some default devices for known machine types:  */
	switch (devinit->machine->machine_type) {
	case MACHINE_CATS:
		bus_pci_add(devinit->machine, d->pcibus,
		    devinit->machine->memory, 0xc0, 7, 0, "ali_m1543");
		bus_pci_add(devinit->machine, d->pcibus,
		    devinit->machine->memory, 0xc0, 10, 0, "dec21143");
		bus_pci_add(devinit->machine, d->pcibus,
		    devinit->machine->memory, 0xc0, 16, 0, "ali_m5229");
		break;
	case MACHINE_NETWINDER:
		bus_pci_add(devinit->machine, d->pcibus,
		    devinit->machine->memory, 0xc0, 11, 0, "symphony_83c553");
		bus_pci_add(devinit->machine, d->pcibus,
		    devinit->machine->memory, 0xc0, 11, 1, "symphony_82c105");
		memory_device_register(devinit->machine->memory,
		    "footbridge_reset", 0x7c000338, 1,
		    dev_footbridge_reset_access, d, DM_DEFAULT, NULL);
		break;
	default:fatal("footbridge: unimplemented machine type.\n");
		exit(1);
	}

	/*  PCI configuration space:  */
	memory_device_register(devinit->machine->memory,
	    "footbridge_pci", pci_addr, 0x1000000,
	    dev_footbridge_pci_access, d, DM_DEFAULT, NULL);

	/*  Timer ticks:  */
	for (i=0; i<N_FOOTBRIDGE_TIMERS; i++) {
		d->timer_control[i] = TIMER_MODE_PERIODIC;
		d->timer_load[i] = TIMER_MAX_VAL;
	}

	machine_add_tickfunction(devinit->machine,
	    dev_footbridge_tick, d, DEV_FOOTBRIDGE_TICK_SHIFT);

	devinit->return_ptr = d->pcibus;
	return 1;
}

