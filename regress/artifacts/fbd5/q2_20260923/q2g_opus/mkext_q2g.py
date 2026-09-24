#!/usr/bin/env python3
"""Opus seat, q2g: SCRATCH CLOSURE EXPERIMENT -- 8 ADDITIVE rows (W1-W8) in a copy of the FROZEN 864-row 3d harness,
one per class this pass measured green, plus a one-line addition to the fatal() STUB (W8 needs the format).  Existing
rows untouched; IDENTITY moved to 872.  A measurement of what closing each class would cost, NOT a proposed patch.
Usage: mkext_q2g.py <frozen harness> <out>."""
import io, sys

src, out = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8", newline="").read()

ROWS = r'''	/*  OPUS q2g SCRATCH CLOSURE EXPERIMENT -- NOT a proposed patch.  */
	{
		static struct memory w_mem;	/*  a non-NULL mem, as every real caller passes; the arms never read it  */
		static const struct { uint64_t addr; int wf; } WD[5] = {
			{ IRQ_STATUS, MEM_WRITE }, { IRQ_RAW_STATUS, MEM_WRITE }, { IRQ_ENABLE_CLEAR, MEM_READ },
			{ FIQ_STATUS, MEM_WRITE }, { FIQ_RAW_STATUS, MEM_WRITE } };
		static const uint64_t WR[5] = { IRQ_STATUS, IRQ_RAW_STATUS, FIQ_STATUS, FIQ_RAW_STATUS, IRQ_ENABLE_SET };
		unsigned char b[8];
		int i, a0, d0, rv, ok;
		uint64_t v1, v2, v3;
		struct footbridge_data *x;
		struct cpu *rc;
		struct machine *rm;
		uint32_t s_load[4], s_value[4], s_control[4];
		int s_pend[4], s_bound[4], tu0, ta0;
		struct timer *s_timer[4];
#define WZ() do { cpu_asserts = cpu_deasserts = 0; a0 = irq_asserts; d0 = irq_deasserts; fatal_calls = 0; } while (0)
#define WCPU(as, ds) (cpu_asserts == (as) && cpu_deasserts == (ds) && irq_asserts == a0 && irq_deasserts == d0)
#define WDECL(C, M) do { for (i = 0; i < 5; i++) { memset(b, 0xa5, sizeof(b)); \
		if (WD[i].wf == MEM_WRITE) memory_writemax64(C, b, 4, 0x70); \
		rv = dev_footbridge_access(C, M, WD[i].addr, b, 4, WD[i].wf, x); } } while (0)
		/*  W1 (AS01, AS07): line 4 raised, latches CLEAR -- the IRQ_STATUS and IRQ_RAW_STATUS reads consume no latch  */
		x = x14_new(0, 0x10, 0, 0, 0);
		x14_line(x, 4);
		WZ();
		memset(b, 0xa5, sizeof(b));
		rv = dev_footbridge_access(cpu, NULL, IRQ_STATUS, b, 4, MEM_READ, x);
		ok = rv == 1 && memory_readmax64(cpu, b, 4) == 0x10;
		memset(b, 0xa5, sizeof(b));
		rv = dev_footbridge_access(cpu, NULL, IRQ_RAW_STATUS, b, 4, MEM_READ, x);
		ok = ok && rv == 1 && memory_readmax64(cpu, b, 4) == 0x10;
		WDECL(cpu, NULL);
		check_u("W1 line 4 raised, latches clear: two legal reads, then 5 declines announce 5", ok && fatal_calls == 5
		    && WCPU(0, 0), 1);
		free(x);
		/*  W2 (AS02, AS03, AS04): line 4 raised -- the DEASSERTING Clear keeps the FIQ fields and consumes no latch  */
		x = x14_new(0, 0x10, 0, 0, 0);
		x14_line(x, 4);
		WZ();
		memory_writemax64(cpu, b, 4, 0x10);
		rv = dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		ok = rv == 1 && x->irq_enable == 0 && x->fiq_status == 0 && x->fiq_enable == 0 && WCPU(0, 1);
		WDECL(cpu, NULL);
		check_u("W2 line 4 raised: Clear 0x10 keeps the FIQ fields, then 5 declines announce 5", ok && fatal_calls == 5, 1);
		free(x);
		/*  W3 (AS08): DEVINIT timers -- the ASSERTING Clear 0x20 keeps the FIQ fields  */
		x = x14_new(0x18, 0x30, 0x60, 0xc0, 1);
		WZ();
		memory_writemax64(cpu, b, 4, 0x20);
		rv = dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		check_u("W3 DEVINIT timers: Clear 0x20 (asserting) keeps the FIQ fields", rv == 1 && x->irq_enable == 0x10
		    && x->fiq_status == 0x60 && x->fiq_enable == 0xc0 && WCPU(1, 0) && fatal_calls == 0, 1);
		free(x);
		/*  W4 (SR*): an ARMED timer 1 (and 2) -- the five arms' legal reads, a Clear and the five declines leave every
		    timer field, the pending ticks and the host timer handle alone  */
		x = x14_new(0x18, 0x30, 0x60, 0xc0, 1);
		x->timer_control[0] = TIMER_ENABLE | TIMER_MODE_PERIODIC;  x->timer_control[1] = TIMER_ENABLE;
		x->timer_load[0] = 0x1234;  x->timer_value[0] = 0x567;
		x->pending_timer_interrupts[0] = 2;  x->pending_bound[0] = 5;
		x->timer[0] = (struct timer *) (void *) &last_freq;
		memcpy(s_load, x->timer_load, sizeof(s_load));  memcpy(s_value, x->timer_value, sizeof(s_value));
		memcpy(s_control, x->timer_control, sizeof(s_control));  memcpy(s_pend, x->pending_timer_interrupts, sizeof(s_pend));
		memcpy(s_bound, x->pending_bound, sizeof(s_bound));  memcpy(s_timer, x->timer, sizeof(s_timer));
		ta0 = timer_add_calls;  tu0 = timer_update_calls;
		WZ();
		for (i = 0; i < 5; i++) {
			memset(b, 0xa5, sizeof(b));
			dev_footbridge_access(cpu, NULL, WR[i], b, 4, MEM_READ, x);
		}
		memory_writemax64(cpu, b, 4, 0x10);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		WDECL(cpu, NULL);
		check_u("W4 an armed timer: the legal reads, a Clear and the declines leave the timer fields alone",
		    !memcmp(s_load, x->timer_load, sizeof(s_load)) && !memcmp(s_value, x->timer_value, sizeof(s_value))
		    && !memcmp(s_control, x->timer_control, sizeof(s_control))
		    && !memcmp(s_pend, x->pending_timer_interrupts, sizeof(s_pend))
		    && !memcmp(s_bound, x->pending_bound, sizeof(s_bound)) && !memcmp(s_timer, x->timer, sizeof(s_timer))
		    && timer_add_calls == ta0 && timer_update_calls == tu0 && fatal_calls == 5, 1);
		free(x);
		/*  W5 (CX*): a REAL caller -- running, little-endian, 32-bit, an instruction executed, a mem, one CPU, cats  */
		rc = calloc(1, sizeof(struct cpu));
		rm = calloc(1, sizeof(struct machine));
		rc->machine = rm;  rm->emulated_hz = 100000000;  rm->machine_type = MACHINE_CATS;  rm->ncpus = 1;
		rc->running = true;  rc->byte_order = EMUL_LITTLE_ENDIAN;  rc->is_32bit = 1;  rc->ninstrs = 1;  rc->mem = &w_mem;
		x = x14_new(0x18, 0x30, 0x60, 0xc0, 1);
		WZ();
		memset(b, 0xa5, sizeof(b));
		rv = dev_footbridge_access(rc, &w_mem, IRQ_STATUS, b, 4, MEM_READ, x);
		v1 = memory_readmax64(rc, b, 4);
		ok = rv == 1;
		memset(b, 0xa5, sizeof(b));
		rv = dev_footbridge_access(rc, &w_mem, IRQ_RAW_STATUS, b, 4, MEM_READ, x);
		v2 = memory_readmax64(rc, b, 4);
		ok = ok && rv == 1;
		memory_writemax64(rc, b, 4, 0x20);
		rv = dev_footbridge_access(rc, &w_mem, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		ok = ok && rv == 1 && x->irq_enable == 0x10 && WCPU(1, 0);
		memory_writemax64(rc, b, 4, 0x40);
		rv = dev_footbridge_access(rc, &w_mem, IRQ_ENABLE_SET, b, 4, MEM_WRITE, x);
		ok = ok && rv == 1 && x->irq_enable == 0x50 && WCPU(2, 0);
		WDECL(rc, &w_mem);
		ok = ok && v1 == 0x10 && v2 == 0x18 && fatal_calls == 5 && WCPU(2, 0);
		memory_writemax64(rc, b, 4, 0x777);
		dev_footbridge_access(rc, &w_mem, TIMER_2_LOAD, b, 4, MEM_WRITE, x);
		memset(b, 0xa5, sizeof(b));
		dev_footbridge_access(rc, &w_mem, TIMER_2_LOAD, b, 4, MEM_READ, x);
		v3 = memory_readmax64(rc, b, 4);
		check_u("W5 a real caller: the reads, a Clear, a Set, the declines and a timer-2 load as for the harness",
		    ok && v3 == 0x777 && x->timer_load[1] == 0x777 && fatal_calls == 5, 1);
		free(x);  free(rm);  free(rc);
		/*  W6 (RS01, RS02): line 4 raised with line 10 pending and MASKED -- a Clear keeps the raw status  */
		x = x14_new(0x400, 0x10, 0, 0, 0);
		x14_line(x, 4);
		WZ();
		memory_writemax64(cpu, b, 4, 0x20);
		rv = dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		check_u("W6 line 4 raised, line 10 pending and masked: Clear 0x20 keeps the raw status 0x410",
		    rv == 1 && x->irq_enable == 0x10 && x->irq_status == 0x410 && WCPU(1, 0) && fatal_calls == 0, 1);
		free(x);
		/*  W7 (IAS01): no line raised -- the five declines leave irq_asserted 0 (a decline writes no interrupt state)  */
		x = x14_new(0x18, 0x30, 0x60, 0xc0, 0);
		WZ();
		WDECL(cpu, NULL);
		check_u("W7 no line raised: the five declines leave irq_asserted 0", x->irq_asserted == 0 && fatal_calls == 5, 1);
		free(x);
		/*  W8 (FMT01): the five announces are plain text -- the real fatal() is vsnprintf(buf, fmt, argp) with NO
		    arguments at these sites, so a conversion in the text reads a vararg that was never passed  */
		x = x14_new(0x18, 0x30, 0x60, 0xc0, 0);
		WZ();
		fatal_pct = 0;
		WDECL(cpu, NULL);
		check_u("W8 the five announces carry no conversion (the real fatal() formats them)", fatal_pct == 0
		    && fatal_calls == 5, 1);
		free(x);
#undef WDECL
#undef WCPU
#undef WZ
		fatal_calls = 0;
	}
'''

EDITS = [
    ("stub", "void fatal(const char *fmt, ...) { (void) fmt; fatal_calls++; }",
     "static int fatal_pct;	/*  OPUS q2g scratch: formats carrying a conversion  */\n"
     "void fatal(const char *fmt, ...) { if (strchr(fmt, '%')) fatal_pct++; fatal_calls++; }"),
    ("rows", "\t/*  IDENTITY, as every differential here carries.", ROWS + "\t/*  IDENTITY, as every differential here carries."),
    ("identity", 'check("IDENTITY row count -- guards against a stale copy", buf, "864");',
     'check("IDENTITY row count -- guards against a stale copy", buf, "872");'),
]
for tag, old, new in EDITS:
    n = s.count(old)
    if n != 1:
        print("REFUSE: anchor %s matches %d times" % (tag, n))
        sys.exit(2)
    s = s.replace(old, new)
io.open(out, "w", encoding="utf-8", newline="").write(s)
print("MKEXT_DONE")
