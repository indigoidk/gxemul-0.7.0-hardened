#!/usr/bin/env python3
"""Opus seat, q2e: SCRATCH CLOSURE EXPERIMENT -- 19 ADDITIVE rows (Y1-Y15) in a copy of the FROZEN 862-row harness,
each aimed at a class this pass measured green.  Existing rows are untouched, so no existing kill can be lost.
A measurement for the main loop, NOT a proposed patch.  Usage: mkext_q2e.py <frozen harness> <out>."""
import io, sys

src, out = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8", newline="").read()

HELPERS = r'''/*  OPUS q2e SCRATCH: an instance with EVERYTHING DEVINIT leaves behind (timer values, d->irq connected -- line 0,
    extra = the cpu -- a PCI bus and a console slot; sentinels, never dereferenced by the five arms), and the deassert
    half of the producer.  */
static struct footbridge_data *y_new(uint32_t is, uint32_t ie, uint32_t fs, uint32_t fe, int devinit)
{
	struct footbridge_data *x = x14_new(is, ie, fs, fe, devinit);
	if (devinit) {
		x->irq.line = 0;
		x->irq.extra = (void *) x;
		x->pcibus = (struct pci_data *) (void *) x;
		x->console_handle = 1;
	}
	return x;
}
static void y_unline(struct footbridge_data *x, int n)
{
	struct interrupt it;
	memset(&it, 0, sizeof(it));
	it.line = (uint32_t) 1 << n;
	it.extra = x;
	footbridge_interrupt_deassert(&it);
}

'''

ROWS = r'''	/*  OPUS q2e SCRATCH CLOSURE EXPERIMENT -- NOT a proposed patch.  */
	{
		static const struct { uint64_t addr; uint32_t want; } YR[5] = {
			{ IRQ_STATUS, 0x10 }, { IRQ_RAW_STATUS, 0x18 }, { FIQ_STATUS, 0x40 }, { FIQ_RAW_STATUS, 0x60 },
			{ IRQ_ENABLE_SET, 0x30 } };
		static const struct { uint64_t addr; uint32_t want; } YA[5] = {
			{ IRQ_STATUS, 0x10 }, { IRQ_RAW_STATUS, 0x10 }, { FIQ_STATUS, 0 }, { FIQ_RAW_STATUS, 0 },
			{ IRQ_ENABLE_SET, 0x10 } };
		static const struct { uint64_t addr; int wf; } YD[5] = {
			{ IRQ_STATUS, MEM_WRITE }, { IRQ_RAW_STATUS, MEM_WRITE }, { IRQ_ENABLE_CLEAR, MEM_READ },
			{ FIQ_STATUS, MEM_WRITE }, { FIQ_RAW_STATUS, MEM_WRITE } };
		static const char *YT[2] = { "DEVINIT timers", "DEVINIT timers, a tick pending" };
		unsigned char b[8];
		char yn[200];
		int i, tk, a0, d0, rv, ok;
		struct footbridge_data *x;
#define YZ() do { cpu_asserts = cpu_deasserts = 0; a0 = irq_asserts; d0 = irq_deasserts; fatal_calls = 0; } while (0)
#define YCPU(as, ds) (cpu_asserts == (as) && cpu_deasserts == (ds) && irq_asserts == a0 && irq_deasserts == d0)
#define YCLR(v) do { memory_writemax64(cpu, b, 4, (v)); \
		rv = dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x); } while (0)
#define YDECL() do { for (i = 0; i < 5; i++) { memset(b, 0xa5, sizeof(b)); \
		if (YD[i].wf == MEM_WRITE) memory_writemax64(cpu, b, 4, 0x70); \
		rv = dev_footbridge_access(cpu, NULL, YD[i].addr, b, 4, YD[i].wf, x); \
		ok = ok && rv == 1 && (YD[i].wf == MEM_WRITE || memory_readmax64(cpu, b, 4) == 0); } } while (0)
#define YREADS(tab) do { ok = 1; for (i = 0; i < 5; i++) { memset(b, 0xa5, sizeof(b)); \
		rv = dev_footbridge_access(cpu, NULL, tab[i].addr, b, 4, MEM_READ, x); \
		ok = ok && rv == 1 && memory_readmax64(cpu, b, 4) == tab[i].want; } } while (0)
		for (tk = 0; tk < 2; tk++) {
			/*  TD01-03, TD12, W03: the Clear's DRIVE under DEVINIT (and a tick): keep, then drop  */
			x = y_new(0x18, 0x30, 0x60, 0xc0, 1);
			x->pending_timer_interrupts[0] = tk;
			YZ(); YCLR(0x20);
			snprintf(yn, sizeof(yn), "Y1 %s: Clear 0x20 keeps 0x10 pending and enabled: CPU asserted once", YT[tk]);
			check_u(yn, rv == 1 && x->irq_enable == 0x10 && YCPU(1, 0) && fatal_calls == 0, 1);
			YZ(); YCLR(0x10);
			snprintf(yn, sizeof(yn), "Y2 %s: then Clear 0x10 drops the last: CPU deasserted once", YT[tk]);
			check_u(yn, rv == 1 && x->irq_enable == 0 && YCPU(0, 1) && fatal_calls == 0, 1);
			free(x);
			/*  W04: reads on the full DEVINIT instance; TD04, W05: its declines drive nothing  */
			x = y_new(0x18, 0x30, 0x60, 0xc0, 1);
			x->pending_timer_interrupts[0] = tk;
			YZ(); YREADS(YR);
			snprintf(yn, sizeof(yn), "Y3 %s, full DEVINIT instance: the five legal reads return their values", YT[tk]);
			check_u(yn, ok && fatal_calls == 0 && YCPU(0, 0), 1);
			YZ(); ok = 1; YDECL();
			snprintf(yn, sizeof(yn), "Y4 %s, full DEVINIT instance: the five declines announce 5, drive nothing", YT[tk]);
			check_u(yn, ok && fatal_calls == 5 && YCPU(0, 0) && x->irq_status == 0x18 && x->irq_enable == 0x30
			    && x->fiq_status == 0x60 && x->fiq_enable == 0xc0, 1);
			free(x);
		}
		/*  IA12, IA13: the asserted IRQ_STATUS read changes no field and drives nothing  */
		x = y_new(0, 0x10, 0, 0, 0); x14_line(x, 4);
		YZ(); memset(b, 0xa5, sizeof(b));
		rv = dev_footbridge_access(cpu, NULL, IRQ_STATUS, b, 4, MEM_READ, x);
		check_u("Y5 line 4 raised: the IRQ_STATUS read keeps the fields and drives nothing", rv == 1
		    && memory_readmax64(cpu, b, 4) == 0x10 && x->irq_status == 0x10 && x->irq_enable == 0x10
		    && x->irq_asserted == 1 && YCPU(0, 0) && fatal_calls == 0, 1);
		free(x);
		/*  IA14: asserted declines drive nothing; IA16: then, every latch set, the reads return their values  */
		x = y_new(0, 0x10, 0, 0, 0); x14_line(x, 4);
		YZ(); ok = 1; YDECL();
		check_u("Y6 line 4 raised: the five declines announce 5 and drive nothing", ok && fatal_calls == 5 && YCPU(0, 0), 1);
		YZ(); YREADS(YA);
		check_u("Y7 line 4 raised, every latch set: the five legal reads return their values",
		    ok && fatal_calls == 0 && YCPU(0, 0), 1);
		free(x);
		/*  PR01, PR02, PR04, PR06, PR07: the producer pair -- two lines up, then down one at a time  */
		x = y_new(0, 0x410, 0, 0, 0);
		YZ(); x14_line(x, 4); x14_line(x, 10);
		check_u("Y8 lines 4 and 10 raised, both enabled: status 0x410, CPU asserted twice",
		    x->irq_status == 0x410 && x->irq_asserted == 1 && YCPU(2, 0), 1);
		YZ(); y_unline(x, 4);
		check_u("Y9 then line 4 lowered: status 0x400, the CPU line not deasserted",
		    x->irq_status == 0x400 && x->irq_asserted == 1 && YCPU(0, 0), 1);
		YZ(); y_unline(x, 10);
		check_u("Y10 then line 10 lowered: status 0, CPU deasserted once, irq_asserted 0",
		    x->irq_status == 0 && x->irq_asserted == 0 && YCPU(0, 1), 1);
		free(x);
		/*  PR02 (the NetBSD form): irq_asserted left 1 by a Clear, then a newly enabled line is raised  */
		x = y_new(0, 0x10, 0, 0, 0); x14_line(x, 4);
		YCLR(0x10);
		memory_writemax64(cpu, b, 4, 0x400);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_SET, b, 4, MEM_WRITE, x);
		YZ(); x14_line(x, 10);
		check_u("Y11 line 4 raised, Clear 0x10, Set 0x400, line 10 raised: CPU asserted once",
		    x->irq_status == 0x410 && YCPU(1, 0), 1);
		free(x);
		/*  PR03: a raised line that is not enabled drives nothing  */
		x = y_new(0, 0x10, 0, 0, 0);
		YZ(); x14_line(x, 10);
		check_u("Y12 line 10 raised while only line 4 is enabled: no CPU assert",
		    x->irq_status == 0x400 && x->irq_asserted == 0 && YCPU(0, 0), 1);
		free(x);
		/*  TD08, TD09 (disclosed today): every timer enabled and every tick pending -- reads, the drive, declines  */
		x = y_new(0x18, 0x30, 0x60, 0xc0, 1);
		for (i = 0; i < N_FOOTBRIDGE_TIMERS; i++) {
			x->timer_control[i] = TIMER_ENABLE | TIMER_MODE_PERIODIC;
			x->pending_timer_interrupts[i] = 1;
		}
		YZ(); YREADS(YR);
		check_u("Y13 every timer enabled, every tick pending: the five legal reads return their values",
		    ok && fatal_calls == 0 && YCPU(0, 0), 1);
		YZ(); YCLR(0x20);
		check_u("Y14 every timer enabled, every tick pending: Clear 0x20 keeps 0x10: CPU asserted once",
		    rv == 1 && x->irq_enable == 0x10 && YCPU(1, 0) && fatal_calls == 0, 1);
		YZ(); ok = 1; YDECL();
		check_u("Y15 every timer enabled, every tick pending: the five declines announce 5, drive nothing",
		    ok && fatal_calls == 5 && YCPU(0, 0), 1);
		free(x);
#undef YREADS
#undef YDECL
#undef YCLR
#undef YCPU
#undef YZ
		fatal_calls = 0;
	}
'''

EDITS = [
    ("helpers", "/* --------------------------------------------------------------- harness --- */",
     HELPERS + "/* --------------------------------------------------------------- harness --- */"),
    ("rows", "\t/*  IDENTITY, as every differential here carries.", ROWS + "\t/*  IDENTITY, as every differential here carries."),
    ("identity", 'check("IDENTITY row count -- guards against a stale copy", buf, "862");',
     'check("IDENTITY row count -- guards against a stale copy", buf, "881");'),
]
for tag, old, new in EDITS:
    n = s.count(old)
    if n != 1:
        print("REFUSE: anchor %s matches %d times" % (tag, n))
        sys.exit(2)
    s = s.replace(old, new)
io.open(out, "w", encoding="utf-8", newline="").write(s)
print("MKEXT_DONE")
