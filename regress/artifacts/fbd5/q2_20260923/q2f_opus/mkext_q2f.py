#!/usr/bin/env python3
"""Opus seat, q2f: SCRATCH CLOSURE EXPERIMENT -- 7 ADDITIVE rows (W1, W2a-c per machine) in a copy of the FROZEN
864-row harness, for the classes this pass measured green.  Existing rows untouched.  A measurement, NOT a patch.
Usage: mkext_q2f.py <frozen harness> <out>."""
import io, sys

src, out = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8", newline="").read()

ROWS = r'''	/*  OPUS q2f SCRATCH CLOSURE EXPERIMENT -- NOT a proposed patch.  */
	{
		static struct memory w_mem;	/*  any non-NULL mem: every real caller passes one; the arms never read it  */
		static const struct { int mt; const char *nm; } WM[2] = { { MACHINE_CATS, "cats" }, { MACHINE_NETWINDER, "netwinder" } };
		static const struct { uint64_t addr; int wf; } WD[5] = {
			{ IRQ_STATUS, MEM_WRITE }, { IRQ_RAW_STATUS, MEM_WRITE }, { IRQ_ENABLE_CLEAR, MEM_READ },
			{ FIQ_STATUS, MEM_WRITE }, { FIQ_RAW_STATUS, MEM_WRITE } };
		unsigned char b[8];
		char wn[200];
		int i, m, a0, d0, rv, ok, saved = machine->machine_type;
		uint64_t v1, v2;
		struct footbridge_data *x;
#define WZ() do { cpu_asserts = cpu_deasserts = 0; a0 = irq_asserts; d0 = irq_deasserts; fatal_calls = 0; } while (0)
#define WCPU(as, ds) (cpu_asserts == (as) && cpu_deasserts == (ds) && irq_asserts == a0 && irq_deasserts == d0)
		/*  W1 (FS01, FS02): the asserted Clear keeps the RAW status and irq_asserted  */
		x = x14_new(0, 0x10, 0, 0, 0);
		x14_line(x, 4);
		WZ();
		memory_writemax64(cpu, b, 4, 0x10);
		rv = dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		check_u("W1 line 4 raised: Clear 0x10 keeps the raw status 0x10 and irq_asserted",
		    rv == 1 && x->irq_enable == 0 && x->irq_status == 0x10 && x->irq_asserted == 1 && WCPU(0, 1), 1);
		free(x);
		/*  W2 (MC01-MC07): the caller context every real call has -- a non-NULL mem, the machine type  */
		for (m = 0; m < 2; m++) {
			machine->machine_type = WM[m].mt;
			x = x14_new(0x418, 0x430, 0x60, 0xc0, 1);
			WZ();
			memset(b, 0xa5, sizeof(b));
			rv = dev_footbridge_access(cpu, &w_mem, IRQ_STATUS, b, 4, MEM_READ, x);
			v1 = memory_readmax64(cpu, b, 4);
			ok = rv == 1;
			memset(b, 0xa5, sizeof(b));
			rv = dev_footbridge_access(cpu, &w_mem, IRQ_RAW_STATUS, b, 4, MEM_READ, x);
			v2 = memory_readmax64(cpu, b, 4);
			snprintf(wn, sizeof(wn), "W2a %s, a real mem: IRQ_STATUS reads 0x410, IRQ_RAW_STATUS 0x418", WM[m].nm);
			check_u(wn, ok && rv == 1 && v1 == 0x410 && v2 == 0x418 && fatal_calls == 0 && WCPU(0, 0), 1);
			WZ();
			memory_writemax64(cpu, b, 4, 0x400);
			rv = dev_footbridge_access(cpu, &w_mem, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
			snprintf(wn, sizeof(wn), "W2b %s, a real mem: Clear 0x400 leaves 0x30, 0x10 pending: CPU asserted once", WM[m].nm);
			check_u(wn, rv == 1 && x->irq_enable == 0x30 && WCPU(1, 0) && fatal_calls == 0, 1);
			WZ();
			ok = 1;
			for (i = 0; i < 5; i++) {
				memset(b, 0xa5, sizeof(b));
				if (WD[i].wf == MEM_WRITE)
					memory_writemax64(cpu, b, 4, 0x70);
				rv = dev_footbridge_access(cpu, &w_mem, WD[i].addr, b, 4, WD[i].wf, x);
				ok = ok && rv == 1 && (WD[i].wf == MEM_WRITE || memory_readmax64(cpu, b, 4) == 0);
			}
			snprintf(wn, sizeof(wn), "W2c %s, a real mem: the five declines announce 5, drive nothing", WM[m].nm);
			check_u(wn, ok && fatal_calls == 5 && WCPU(0, 0) && x->irq_status == 0x418 && x->irq_enable == 0x30, 1);
			free(x);
		}
		machine->machine_type = saved;
#undef WCPU
#undef WZ
		fatal_calls = 0;
	}
'''

EDITS = [
    ("rows", "\t/*  IDENTITY, as every differential here carries.", ROWS + "\t/*  IDENTITY, as every differential here carries."),
    ("identity", 'check("IDENTITY row count -- guards against a stale copy", buf, "864");',
     'check("IDENTITY row count -- guards against a stale copy", buf, "871");'),
]
for tag, old, new in EDITS:
    n = s.count(old)
    if n != 1:
        print("REFUSE: anchor %s matches %d times" % (tag, n))
        sys.exit(2)
    s = s.replace(old, new)
io.open(out, "w", encoding="utf-8", newline="").write(s)
print("MKEXT_DONE")
