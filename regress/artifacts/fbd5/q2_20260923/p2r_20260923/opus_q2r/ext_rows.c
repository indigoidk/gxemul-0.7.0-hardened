	/*  OPUS SCRATCH EXPERIMENT (q2r) -- NOT a proposed patch, a MEASUREMENT of what closing the three
	    measured holes would cost.  Inserted before IDENTITY in a scratch copy only.
	    Y1: CROSS-LATCH ORDER.  Every multi-site sequence above declines the sites in ONE fixed order, so the
	        first decline of site i was never made with a LATER-ordered site j already latched.  Each ordered
	        pair (j, i): latch j, then i's FIRST decline announces exactly once and keeps fields and irq.
	    Y2: LEGAL x LATCH-SET, THE VALUE HALF.  X7 checks only that a legal access re-arms nothing; with every
	        latch set, each legal read must still return its value over its width, and a legal IRQ Clear
	        write must still clear and drive the output.  (P7 carries this for +0x180/+0x284 and P8 for
	        +0x18c, one seeded cell each; nothing carried it for +0x184 or +0x280.)
	    Y3: LEGAL NARROW WRITE at +0x18c -- every legal write above is len 4.  */
	{
		static const struct { uint32_t is, ie, fs, fe; const char *nm; } SY[3] = {
			{ 0x18, 0x30, 0x60, 0xc0, "seeded" }, { 0, 0, 0, 0, "all-zero" },
			{ 0x80010018, 0x00010030, 0x40020060, 0x000200c0, "wide" } };
		static const struct { uint64_t addr; int wf; const char *nm; } DY[5] = {
			{ IRQ_STATUS, MEM_WRITE, "write IRQ_STATUS" }, { IRQ_RAW_STATUS, MEM_WRITE, "write IRQ_RAW_STATUS" },
			{ IRQ_ENABLE_CLEAR, MEM_READ, "read IRQ_ENABLE_CLEAR" }, { FIQ_STATUS, MEM_WRITE, "write FIQ_STATUS" },
			{ FIQ_RAW_STATUS, MEM_WRITE, "write FIQ_RAW_STATUS" } };
		static const struct { uint64_t addr; const char *nm; } RY[5] = {
			{ IRQ_STATUS, "IRQ_STATUS" }, { IRQ_RAW_STATUS, "IRQ_RAW_STATUS" }, { FIQ_STATUS, "FIQ_STATUS" },
			{ FIQ_RAW_STATUS, "FIQ_RAW_STATUS" }, { IRQ_ENABLE_SET, "IRQEnable" } };
		static const int WY[3] = { 1, 2, 4 };
		unsigned char b[8];
		char yn[200];
		int i, j, st, r, w, si, a0, d0, f0, ok;
		struct footbridge_data *x;
#define YNEW(s) do { x = calloc(1, sizeof(*x)); arm_irqs(x); x->irq.interrupt_assert = noop_assert; \
		x->irq.interrupt_deassert = noop_deassert; x->irq_status = SY[s].is; x->irq_enable = SY[s].ie; \
		x->fiq_status = SY[s].fs; x->fiq_enable = SY[s].fe; } while (0)
#define YSAME(s) (x->irq_status == SY[s].is && x->irq_enable == SY[s].ie && x->fiq_status == SY[s].fs \
		&& x->fiq_enable == SY[s].fe)
		for (j = 0; j < 5; j++)
			for (i = 0; i < 5; i++) {
				if (i == j)
					continue;
				YNEW(0);
				memory_writemax64(cpu, b, 4, 0x70);
				dev_footbridge_access(cpu, NULL, DY[j].addr, b, 4, DY[j].wf, x);
				f0 = fatal_calls; a0 = irq_asserts; d0 = irq_deasserts;
				memory_writemax64(cpu, b, 4, 0x70);
				dev_footbridge_access(cpu, NULL, DY[i].addr, b, 4, DY[i].wf, x);
				ok = fatal_calls - f0 == 1 && YSAME(0) && irq_asserts == a0 && irq_deasserts == d0;
				snprintf(yn, sizeof(yn), "Y1 first %s after %s latched: announced once", DY[i].nm, DY[j].nm);
				check_u(yn, ok, 1);
				free(x);
			}
		for (st = 0; st < 3; st++) {
			for (r = 0; r < 5; r++)
				for (w = 0; w < 3; w++) {
					uint32_t is = SY[st].is, ie = SY[st].ie, fs = SY[st].fs, fe = SY[st].fe;
					uint64_t want = r == 0 ? (uint64_t) (is & ie) : r == 1 ? (uint64_t) is
					    : r == 2 ? (uint64_t) (fs & fe) : r == 3 ? (uint64_t) fs : (uint64_t) ie;
					want &= WY[w] == 4 ? 0xffffffffULL : WY[w] == 2 ? 0xffffULL : 0xffULL;
					YNEW(st);
					for (si = 0; si < 5; si++) {
						memory_writemax64(cpu, b, 4, 0x70);
						dev_footbridge_access(cpu, NULL, DY[si].addr, b, 4, DY[si].wf, x);
					}
					f0 = fatal_calls; a0 = irq_asserts; d0 = irq_deasserts;
					memset(b, 0xa5, sizeof(b));
					dev_footbridge_access(cpu, NULL, RY[r].addr, b, WY[w], MEM_READ, x);
					ok = fatal_calls == f0 && memory_readmax64(cpu, b, WY[w]) == want && YSAME(st)
					    && irq_asserts == a0 && irq_deasserts == d0;
					snprintf(yn, sizeof(yn), "Y2 legal len %d read of %s (%s, latches SET) returns its value",
					    WY[w], RY[r].nm, SY[st].nm);
					check_u(yn, ok, 1);
					free(x);
				}
			{
				uint32_t is = SY[st].is, ne = SY[st].ie & ~0x70u;
				YNEW(st);
				for (si = 0; si < 5; si++) {
					memory_writemax64(cpu, b, 4, 0x70);
					dev_footbridge_access(cpu, NULL, DY[si].addr, b, 4, DY[si].wf, x);
				}
				f0 = fatal_calls; a0 = irq_asserts; d0 = irq_deasserts;
				memory_writemax64(cpu, b, 4, 0x70);
				dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
				ok = fatal_calls == f0 && x->irq_enable == ne && x->irq_status == is
				    && ((is & ne) ? (irq_asserts == a0 + 1 && irq_deasserts == d0)
				                  : (irq_asserts == a0 && irq_deasserts == d0 + 1));
				snprintf(yn, sizeof(yn), "Y2 IRQ Clear write 0x70 (%s, latches SET) clears and drives", SY[st].nm);
				check_u(yn, ok, 1);
				free(x);
			}
			for (w = 0; w < 2; w++) {
				uint32_t is = SY[st].is, ne = SY[st].ie & ~0x70u;
				YNEW(st);
				fatal_calls = 0; a0 = irq_asserts; d0 = irq_deasserts;
				memory_writemax64(cpu, b, WY[w], 0x70);
				dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, WY[w], MEM_WRITE, x);
				ok = fatal_calls == 0 && x->irq_enable == ne && x->irq_status == is
				    && ((is & ne) ? (irq_asserts == a0 + 1 && irq_deasserts == d0)
				                  : (irq_asserts == a0 && irq_deasserts == d0 + 1));
				for (si = 0; si < 5; si++) {
					memory_writemax64(cpu, b, 4, 0x70);
					dev_footbridge_access(cpu, NULL, DY[si].addr, b, 4, DY[si].wf, x);
				}
				ok = ok && fatal_calls == 5;
				snprintf(yn, sizeof(yn), "Y3 IRQ Clear write 0x70 len %d (%s, latches clear)", WY[w], SY[st].nm);
				check_u(yn, ok, 1);
				free(x);
			}
		}
#undef YSAME
#undef YNEW
		fatal_calls = 0;
	}
