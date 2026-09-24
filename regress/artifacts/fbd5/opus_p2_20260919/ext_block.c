	/*  OPUS P2 (scratch only, NOT for the tree): candidate repair rows for A (width-first at every site),
	    G (legal NARROW reads of the status registers) and B (a legal read must not re-arm any latch).  */
	{
		static const struct { uint64_t addr; int wf; const char *what; } s5[] = {
			{ IRQ_STATUS, MEM_WRITE, "X1 write IRQ_STATUS" }, { IRQ_RAW_STATUS, MEM_WRITE, "X1 write IRQ_RAW_STATUS" },
			{ IRQ_ENABLE_CLEAR, MEM_READ, "X1 read IRQ_ENABLE_CLEAR" }, { FIQ_STATUS, MEM_WRITE, "X1 write FIQ_STATUS" },
			{ FIQ_RAW_STATUS, MEM_WRITE, "X1 write FIQ_RAW_STATUS" } };
		static const struct { uint64_t addr; uint64_t want; const char *what; } rd5[] = {
			{ IRQ_STATUS, 0x10, "IRQ_STATUS" }, { IRQ_RAW_STATUS, 0x18, "IRQ_RAW_STATUS" },
			{ FIQ_STATUS, 0x40, "FIQ_STATUS" }, { FIQ_RAW_STATUS, 0x50, "FIQ_RAW_STATUS" },
			{ IRQ_ENABLE_SET, 0x30, "IRQ_ENABLE_SET" } };
		unsigned char b[8];
		char xn[160];
		int i, w, f0;
		struct footbridge_data *x;
#define XSEED(x) do { arm_irqs(x); (x)->irq.interrupt_assert = noop_assert; (x)->irq.interrupt_deassert = noop_deassert; \
		(x)->irq_status = 0x18; (x)->irq_enable = 0x30; (x)->fiq_status = 0x50; (x)->fiq_enable = 0xc0; } while (0)
		for (w = 1; w <= 2; w++)
			for (i = 0; i < 5; i++) {
				x = calloc(1, sizeof(*x)); XSEED(x);
				fatal_calls = 0;
				memory_writemax64(cpu, b, w, 0x70);
				dev_footbridge_access(cpu, NULL, s5[i].addr, b, w, s5[i].wf, x);
				snprintf(xn, sizeof(xn), "%s: len %d as the FIRST access announces once", s5[i].what, w);
				check_u(xn, fatal_calls, 1);
				free(x);
			}
		x = calloc(1, sizeof(*x)); XSEED(x);
		fatal_calls = 0;
		for (w = 1; w <= 2; w++)
			for (i = 0; i < 5; i++) {
				memset(b, 0, sizeof(b));
				dev_footbridge_access(cpu, NULL, rd5[i].addr, b, w, MEM_READ, x);
				snprintf(xn, sizeof(xn), "X2 legal len %d read of %s = low lanes", w, rd5[i].what);
				check_u(xn, memory_readmax64(cpu, b, w), rd5[i].want & (w == 1 ? 0xff : 0xffff));
			}
		check_u("X2 the legal narrow reads announce nothing", fatal_calls, 0);
		for (i = 0; i < 5; i++) {
			memory_writemax64(cpu, b, 4, 0x70);
			dev_footbridge_access(cpu, NULL, s5[i].addr, b, 4, s5[i].wf, x);
		}
		check_u("X3 the five declines latch (5 announces)", fatal_calls, 5);
		f0 = fatal_calls;
		for (w = 1; w <= 4; w *= 2)
			for (i = 0; i < 5; i++)
				dev_footbridge_access(cpu, NULL, rd5[i].addr, b, w, MEM_READ, x);
		for (i = 0; i < 5; i++) {
			memory_writemax64(cpu, b, 4, 0x70);
			dev_footbridge_access(cpu, NULL, s5[i].addr, b, 4, s5[i].wf, x);
		}
		check_u("X3 legal reads of every sibling re-arm NO latch", fatal_calls - f0, 0);
#undef XSEED
		free(x);
		fatal_calls = 0;
	}

