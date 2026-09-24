#!/usr/bin/env python3
"""Opus seat, #545 q2c: SCRATCH CLOSURE EXPERIMENT -- insert 28 rows (Z1-Z7) into a copy of the FROZEN 707-row
harness, each aimed at one escape class this pass measured.  A measurement for the main loop, NOT a proposed patch.
Usage: mkext.py <frozen harness> <out>.  Anchored; refuses unless each anchor matches exactly once."""
import io, sys

src, out = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8", newline="").read()

HELPERS = r'''/*  OPUS q2c SCRATCH CLOSURE EXPERIMENT helpers.  A CPU-line counter pair NOT shared with the timer interrupts,
    so a row can tell WHICH interrupt a Clear write drove; an instance with DEVINIT's timer reset values; and a
    device line raised through the real footbridge_interrupt_assert() -- the product's only writer of irq_asserted.  */
static int zc_as, zc_ds;
static void z_cpu_assert(struct interrupt *i) { (void) i; zc_as++; }
static void z_cpu_deassert(struct interrupt *i) { (void) i; zc_ds++; }
static struct footbridge_data *z_new(uint32_t is, uint32_t ie, uint32_t fs, uint32_t fe, int devinit)
{
	struct footbridge_data *x = calloc(1, sizeof(*x));
	int i;
	arm_irqs(x);
	x->irq.interrupt_assert = z_cpu_assert;
	x->irq.interrupt_deassert = z_cpu_deassert;
	x->irq_status = is; x->irq_enable = ie; x->fiq_status = fs; x->fiq_enable = fe;
	if (devinit)
		for (i = 0; i < N_FOOTBRIDGE_TIMERS; i++) {
			x->timer_control[i] = TIMER_MODE_PERIODIC;
			x->timer_load[i] = TIMER_MAX_VAL;
			x->pending_bound[i] = 1;
		}
	return x;
}
static void z_line(struct footbridge_data *x, int n)
{
	struct interrupt it;
	memset(&it, 0, sizeof(it));
	it.line = (uint32_t) 1 << n;
	it.extra = x;
	footbridge_interrupt_assert(&it);
}

'''

ROWS = r'''	/*  OPUS q2c SCRATCH CLOSURE EXPERIMENT -- NOT a proposed patch; each block names the escapes it is for.  */
	{
		static const int ZB[7] = { 4, 5, 6, 7, 10, 11, 18 };
		static const uint64_t RA[5] = { IRQ_STATUS, IRQ_RAW_STATUS, FIQ_STATUS, FIQ_RAW_STATUS, IRQ_ENABLE_SET };
		static const uint64_t RW[5] = { 0x10, 0x18, 0x40, 0x60, 0x30 };
		static const struct { uint64_t addr; int wf; } DZ[5] = {
			{ IRQ_STATUS, MEM_WRITE }, { IRQ_RAW_STATUS, MEM_WRITE }, { IRQ_ENABLE_CLEAR, MEM_READ },
			{ FIQ_STATUS, MEM_WRITE }, { FIQ_RAW_STATUS, MEM_WRITE } };
		unsigned char b[8];
		char zn[200];
		int i, k, a0, d0, f0, ok;
		struct footbridge_data *x;
		/*  Z1 (N_S01 `&&`, N_S02 drop an operand): status and new enable both nonzero, disjoint -> ONE deassert.  */
		x = z_new(0x18, 0x30, 0x60, 0xc0, 0);
		zc_as = zc_ds = 0; fatal_calls = 0;
		memory_writemax64(cpu, b, 4, 0x10);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		check_u("Z1 Clear 0x10 from 0x18/0x30: enable 0x20, disjoint from status, one deassert",
		    x->irq_enable == 0x20 && zc_as == 0 && zc_ds == 1 && fatal_calls == 0, 1);
		free(x);
		/*  Z2 (N_S06, N_S07, N_SB05..18): one WIRED line alone pending and enabled -> a Clear of nothing asserts.  */
		for (k = 0; k < 7; k++) {
			x = z_new((uint32_t) 1 << ZB[k], (uint32_t) 1 << ZB[k], 0, 0, 0);
			zc_as = zc_ds = 0; fatal_calls = 0;
			memory_writemax64(cpu, b, 4, 0);
			dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
			snprintf(zn, sizeof(zn), "Z2 Clear 0 with only line %d pending and enabled: one assert", ZB[k]);
			check_u(zn, zc_as == 1 && zc_ds == 0 && fatal_calls == 0, 1);
			free(x);
		}
		/*  Z3 (N_I05, N_I06): the Clear write drives the CPU line d->irq and no timer interrupt.  */
		for (k = 0; k < 2; k++) {
			x = z_new(0x18, 0x30, 0x60, 0xc0, 0);
			zc_as = zc_ds = 0; a0 = irq_asserts; d0 = irq_deasserts;
			memory_writemax64(cpu, b, 4, k ? 0x70 : 0);
			dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
			snprintf(zn, sizeof(zn), "Z3 Clear %s drives the CPU line and no timer interrupt", k ? "0x70" : "0");
			check_u(zn, (k ? (zc_as == 0 && zc_ds == 1) : (zc_as == 1 && zc_ds == 0))
			    && irq_asserts == a0 && irq_deasserts == d0, 1);
			free(x);
		}
		/*  Z4 (N_T04, N_T05, N_F09, N_T09): DEVINIT's timer reset values (PERIODIC, TIMER_MAX_VAL, bound 1).  */
		x = z_new(0x18, 0x30, 0x60, 0xc0, 1);
		fatal_calls = 0; ok = 1;
		for (i = 0; i < 5; i++) {
			memset(b, 0xa5, sizeof(b));
			dev_footbridge_access(cpu, NULL, RA[i], b, 4, MEM_READ, x);
			ok = ok && memory_readmax64(cpu, b, 4) == RW[i];
		}
		check_u("Z4 DEVINIT timer state: legal reads return their values, announce nothing", ok && fatal_calls == 0, 1);
		memory_writemax64(cpu, b, 4, 0x40);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_SET, b, 4, MEM_WRITE, x);
		memory_writemax64(cpu, b, 4, 0x10);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		check_u("Z4 DEVINIT timer state: Set 0x40 then Clear 0x10 leave IRQEnable 0x60",
		    x->irq_enable == 0x60 && fatal_calls == 0, 1);
		f0 = fatal_calls;
		for (i = 0; i < 5; i++) {
			memory_writemax64(cpu, b, 4, 0x70);
			dev_footbridge_access(cpu, NULL, DZ[i].addr, b, 4, DZ[i].wf, x);
		}
		check_u("Z4 DEVINIT timer state: the five declines announce 5", fatal_calls - f0, 5);
		free(x);
		/*  Z5 (N_T11, N_T12, N_F01, N_I01, N_I02, N_I04): irq_asserted = 1, reached through the real callback.  */
		x = z_new(0, 0x10, 0, 0, 0); z_line(x, 4);
		fatal_calls = 0;
		memset(b, 0xa5, sizeof(b));
		dev_footbridge_access(cpu, NULL, IRQ_STATUS, b, 4, MEM_READ, x);
		check_u("Z5 line 4 asserted by a device: IRQ_STATUS reads 0x10, announces nothing",
		    x->irq_asserted == 1 && memory_readmax64(cpu, b, 4) == 0x10 && fatal_calls == 0, 1);
		free(x);
		x = z_new(0, 0x10, 0, 0, 0); z_line(x, 4);
		zc_as = zc_ds = 0; fatal_calls = 0;
		memory_writemax64(cpu, b, 4, 0x10);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		check_u("Z5 line 4 asserted by a device: Clear 0x10 clears and deasserts once",
		    x->irq_enable == 0 && zc_as == 0 && zc_ds == 1 && fatal_calls == 0, 1);
		free(x);
		x = z_new(0, 0x10, 0, 0, 0); z_line(x, 4);
		zc_as = zc_ds = 0; fatal_calls = 0;
		memory_writemax64(cpu, b, 4, 0x400);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		check_u("Z5 line 4 asserted by a device: Clear 0x400 keeps line 4 enabled, asserts once",
		    x->irq_enable == 0x10 && zc_as == 1 && zc_ds == 0 && fatal_calls == 0, 1);
		free(x);
		/*  Z6 (N_L06, N_L07, N_L08, N_L10, N_L11): width 8, reachable by LDRD/STRD.  */
		for (i = 0; i < 5; i++) {
			x = z_new(0x18, 0x30, 0x60, 0xc0, 0);
			fatal_calls = 0;
			memset(b, 0xa5, sizeof(b));
			dev_footbridge_access(cpu, NULL, RA[i], b, 8, MEM_READ, x);
			snprintf(zn, sizeof(zn), "Z6 legal len 8 read of 0x%x returns its value, announces nothing", (int) RA[i]);
			check_u(zn, memory_readmax64(cpu, b, 8) == RW[i] && fatal_calls == 0, 1);
			free(x);
		}
		x = z_new(0x18, 0x30, 0x60, 0xc0, 0);
		zc_as = zc_ds = 0; fatal_calls = 0;
		memory_writemax64(cpu, b, 8, 0x10);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 8, MEM_WRITE, x);
		check_u("Z6 legal len 8 Clear 0x10: enable 0x20, one deassert, announces nothing",
		    x->irq_enable == 0x20 && zc_ds == 1 && zc_as == 0 && fatal_calls == 0, 1);
		free(x);
		for (i = 0; i < 5; i++) {
			int n1, n2;
			x = z_new(0x18, 0x30, 0x60, 0xc0, 0);
			fatal_calls = 0;
			memset(b, 0xa5, sizeof(b));
			if (DZ[i].wf == MEM_WRITE)
				memory_writemax64(cpu, b, 8, 0x70);
			dev_footbridge_access(cpu, NULL, DZ[i].addr, b, 8, DZ[i].wf, x);
			n1 = fatal_calls;
			ok = DZ[i].wf != MEM_READ || memory_readmax64(cpu, b, 8) == 0;
			if (DZ[i].wf == MEM_WRITE)
				memory_writemax64(cpu, b, 8, 0x70);
			dev_footbridge_access(cpu, NULL, DZ[i].addr, b, 8, DZ[i].wf, x);
			n2 = fatal_calls - n1;
			snprintf(zn, sizeof(zn), "Z6 declined len 8 access to 0x%x: announced once, then latched, fields kept",
			    (int) DZ[i].addr);
			check_u(zn, ok && n1 == 1 && n2 == 0 && x->irq_status == 0x18 && x->irq_enable == 0x30
			    && x->fiq_status == 0x60 && x->fiq_enable == 0xc0, 1);
			free(x);
		}
		/*  Z7 (N_T06, N_F15): a timer tick pending -- the state a guest's timer interrupt handler runs in.  */
		x = z_new(0x18, 0x30, 0x60, 0xc0, 0);
		x->pending_timer_interrupts[0] = 1;
		fatal_calls = 0;
		memory_writemax64(cpu, b, 4, 0x10);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		check_u("Z7 timer 1 tick pending: Clear 0x10 clears, announces nothing", x->irq_enable == 0x20 && fatal_calls == 0, 1);
		free(x);
		fatal_calls = 0;
	}
'''

EDITS = [
    ("helpers", "/*  The helper is static inside the shipped file, which is exactly why this driver includes",
     HELPERS + "/*  The helper is static inside the shipped file, which is exactly why this driver includes"),
    ("rows", "\t/*  IDENTITY, as every differential here carries.", ROWS + "\t/*  IDENTITY, as every differential here carries."),
    ("identity", 'check("IDENTITY row count -- guards against a stale copy", buf, "707");',
     'check("IDENTITY row count -- guards against a stale copy", buf, "735");'),
]
for tag, old, new in EDITS:
    n = s.count(old)
    if n != 1:
        print("REFUSE: anchor %s matches %d times" % (tag, n))
        sys.exit(2)
    s = s.replace(old, new)
io.open(out, "w", encoding="utf-8", newline="").write(s)
print("MKEXT_DONE")
