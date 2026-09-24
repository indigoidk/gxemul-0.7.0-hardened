/*
 *  Opus seat, #545 q2r -- one translation unit per device copy (baseline or variant), so a single
 *  process can drive BOTH copies with the same access sequence and compare what each one does.
 *  Built twice: -DPFX=base_ -DDEVFILE='"base/dev_footbridge.c"' and -DPFX=var_ -DDEVFILE='"var/..."'.
 *  The renames below apply before any header, so declarations and definitions agree.
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

void *CAT(PFX, new)(void (*a)(struct interrupt *), void (*dd)(struct interrupt *))
{
	struct footbridge_data *d = calloc(1, sizeof(*d));
	int i;
	for (i = 0; i < N_FOOTBRIDGE_TIMERS; i++) {
		d->timer_irq[i].interrupt_assert = a;
		d->timer_irq[i].interrupt_deassert = dd;
	}
	d->irq.interrupt_assert = a;
	d->irq.interrupt_deassert = dd;
	return d;
}

void CAT(PFX, set)(void *p, uint32_t is, uint32_t ie, uint32_t fs, uint32_t fe)
{
	struct footbridge_data *d = p;
	d->irq_status = is; d->irq_enable = ie; d->fiq_status = fs; d->fiq_enable = fe;
}

void CAT(PFX, get)(void *p, uint32_t *o)
{
	struct footbridge_data *d = p;
	o[0] = d->irq_status; o[1] = d->irq_enable; o[2] = d->fiq_status; o[3] = d->fiq_enable;
	o[4] = d->warned_irq_status_w; o[5] = d->warned_irq_raw_w; o[6] = d->warned_irq_clear_r;
	o[7] = d->warned_fiq_status_w; o[8] = d->warned_fiq_raw_w; o[9] = d->irq_asserted;
}

void *CAT(PFX, irqptr)(void *p)
{
	return &((struct footbridge_data *) p)->irq;
}

int CAT(PFX, acc)(struct cpu *cpu, void *p, uint64_t addr, unsigned char *b, size_t len, int wf)
{
	return dev_footbridge_access(cpu, NULL, addr, b, len, wf, p);
}

/*  A device interrupt line, exactly as a connected device drives it: footbridge_interrupt_assert()
    with interrupt->line = 1 << n and extra = the device.  This is the ONLY writer of irq_status.  */
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
