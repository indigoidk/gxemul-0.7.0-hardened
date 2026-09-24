/*
 *  Opus seat, #545 q2c -- one translation unit per device copy (the frozen device, or one variant), so one process can
 *  drive BOTH with the same sequence and compare.  Built twice: -DPFX=base_ -DDEVFILE='"base/dev_footbridge.c"' and
 *  -DPFX=var_ -DDEVFILE='"var/dev_footbridge.c"'.
 *
 *  DIFFERENCE FROM THE EARLIER q2r DIFFERENTIAL (wit_tu.c): the instance is wired the way DEVINIT wires it --
 *  timer_irq[i] -> footbridge_interrupt_assert/deassert with line 1 << (IRQ_TIMER_1 + i) and extra = the device -- and
 *  mode 1 is DEVINIT's reset state (timer_control = TIMER_MODE_PERIODIC, timer_load = TIMER_MAX_VAL, pending_bound = 1).
 *  Mode 0 is the offline harness's calloc'd instance (all zero), for comparison.
 */
#define CAT2(a, b) a##b
#define CAT(a, b) CAT2(a, b)
#define dev_footbridge_access		CAT(PFX, dev_footbridge_access)
#define dev_footbridge_isa_access	CAT(PFX, isa_access)
#define dev_footbridge_pci_access	CAT(PFX, pci_access)
#define dev_footbridge_reset_access	CAT(PFX, reset_access)
#define devinit_footbridge		CAT(PFX, devinit)
#define dev_footbridge_tick		CAT(PFX, tick)
#define footbridge_interrupt_assert	CAT(PFX, ia)
#define footbridge_interrupt_deassert	CAT(PFX, id)

#include <inttypes.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "include/misc.h"
#include "include/memory.h"
#include "include/machine.h"
#include "include/cpu.h"

#include DEVFILE

void CAT(PFX, reinit)(void *p, int mode, void (*a)(struct interrupt *), void (*dd)(struct interrupt *))
{
	struct footbridge_data *d = p;
	int i;
	memset(d, 0, sizeof(*d));
	d->irq.interrupt_assert = a;
	d->irq.interrupt_deassert = dd;
	for (i = 0; i < N_FOOTBRIDGE_TIMERS; i++) {
		d->timer_irq[i].interrupt_assert = footbridge_interrupt_assert;
		d->timer_irq[i].interrupt_deassert = footbridge_interrupt_deassert;
		d->timer_irq[i].line = (uint32_t) 1 << (IRQ_TIMER_1 + i);
		d->timer_irq[i].extra = d;
		if (mode == 1) {
			d->pending_bound[i] = 1;
			d->timer_control[i] = TIMER_MODE_PERIODIC;
			d->timer_load[i] = TIMER_MAX_VAL;
		}
	}
}

void *CAT(PFX, alloc)(void)
{
	return calloc(1, sizeof(struct footbridge_data));
}

size_t CAT(PFX, size)(void)
{
	return sizeof(struct footbridge_data);
}

void *CAT(PFX, irqptr)(void *p)
{
	return &((struct footbridge_data *) p)->irq;
}

void CAT(PFX, get)(void *p, uint32_t *o)
{
	struct footbridge_data *d = p;
	int i;
	o[0] = d->irq_status; o[1] = d->irq_enable; o[2] = d->fiq_status; o[3] = d->fiq_enable;
	o[4] = d->warned_irq_status_w; o[5] = d->warned_irq_raw_w; o[6] = d->warned_irq_clear_r;
	o[7] = d->warned_fiq_status_w; o[8] = d->warned_fiq_raw_w; o[9] = d->irq_asserted;
	for (i = 0; i < 4; i++) {
		o[10 + i] = d->timer_control[i]; o[14 + i] = d->timer_load[i];
		o[18 + i] = (uint32_t) d->pending_timer_interrupts[i]; o[22 + i] = d->timer_value[i];
	}
}

int CAT(PFX, acc)(struct cpu *cpu, void *p, uint64_t addr, unsigned char *b, size_t len, int wf)
{
	return dev_footbridge_access(cpu, NULL, addr, b, len, wf, p);
}

/*  A device interrupt line, exactly as a connected device drives it.  */
void CAT(PFX, line)(void *p, int n, int on)
{
	struct interrupt it;
	memset(&it, 0, sizeof(it));
	it.line = (uint32_t) 1 << n;
	it.extra = p;
	if (on)
		footbridge_interrupt_assert(&it);
	else
		footbridge_interrupt_deassert(&it);
}

/*  What the SIGALRM timer callback does (timer_tick0 -> footbridge_pending(d, 0)).  */
void CAT(PFX, pend)(void *p, int nr)
{
	footbridge_pending((struct footbridge_data *) p, nr);
}

/*  DEVICE_TICK, with random() re-seeded so base and variant draw the same counter value.  */
void CAT(PFX, dtick)(struct cpu *cpu, void *p)
{
	srandom(12345);
	dev_footbridge_tick(cpu, p);
}
