	/*  #545 pass 2 (L2 floor repair, measured by the Opus seat): the P-rows above pinned width and latch at ONE site
	    each, so a `len == 4` conjunct on any of the other four decline guards, a legal read that re-arms a latch, and
	    a decline guard widened to swallow a LEGAL narrow read all passed every row.  X1: every site at len 1 and 2 as
	    the FIRST access announces once (and the narrow declined read returns 0).  X2: legal narrow reads of the
	    five readable registers return the low lanes and announce nothing.  X3: legal reads of every sibling at every
	    width, legal enable writes, and reads of other registers re-arm NO latch.  X4/X5 (pass 2, codex): ZERO data
	    or a zero enable as the first access still declines AND announces; a legal zero Clear write does not.  */
	{
		static const struct { uint64_t addr; int wf; const char *what; } s5[] = {
			{ IRQ_STATUS, MEM_WRITE, "X1 write IRQ_STATUS" }, { IRQ_RAW_STATUS, MEM_WRITE, "X1 write IRQ_RAW_STATUS" },
			{ IRQ_ENABLE_CLEAR, MEM_READ, "X1 read IRQ_ENABLE_CLEAR" }, { FIQ_STATUS, MEM_WRITE, "X1 write FIQ_STATUS" },
			{ FIQ_RAW_STATUS, MEM_WRITE, "X1 write FIQ_RAW_STATUS" } };
		static const struct { uint64_t addr; uint64_t want; const char *what; } rd5[] = {
			{ IRQ_STATUS, 0x10, "IRQ_STATUS" }, { IRQ_RAW_STATUS, 0x18, "IRQ_RAW_STATUS" },
			{ FIQ_STATUS, 0x40, "FIQ_STATUS" }, { FIQ_RAW_STATUS, 0x60, "FIQ_RAW_STATUS" },
			{ IRQ_ENABLE_SET, 0x30, "IRQ_ENABLE_SET" } };
		unsigned char b[8];
		char xn[160];
		int i, w, f0;
		struct footbridge_data *x;
#define XSEED(x) do { arm_irqs(x); (x)->irq.interrupt_assert = noop_assert; (x)->irq.interrupt_deassert = noop_deassert; \
		(x)->irq_status = 0x18; (x)->irq_enable = 0x30; (x)->fiq_status = 0x60; (x)->fiq_enable = 0xc0; } while (0)
		for (w = 1; w <= 2; w++)
			for (i = 0; i < 5; i++) {
				x = calloc(1, sizeof(*x)); XSEED(x);
				fatal_calls = 0;
				memory_writemax64(cpu, b, w, 0x70);
				dev_footbridge_access(cpu, NULL, s5[i].addr, b, w, s5[i].wf, x);
				snprintf(xn, sizeof(xn), "%s: len %d as the FIRST access announces once", s5[i].what, w);
				check_u(xn, fatal_calls, 1);
				if (s5[i].wf == MEM_READ) {	/*  the narrow declined read's VALUE (pass 2)  */
					snprintf(xn, sizeof(xn), "X1 read IRQ_ENABLE_CLEAR: len %d declined read returns 0", w);
					check_u(xn, memory_readmax64(cpu, b, w), 0);
				}
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
		/*  X3, widened (pass 2): legal WRITES to the four enable registers, and reads of registers outside the
		    five above (VENDOR_ID, TIMER_1_VALUE, the silent FIQEnableClear read), re-arm no latch either.  */
		f0 = fatal_calls;
		memory_writemax64(cpu, b, 4, 0);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_SET, b, 4, MEM_WRITE, x);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		dev_footbridge_access(cpu, NULL, FIQ_ENABLE_SET, b, 4, MEM_WRITE, x);
		dev_footbridge_access(cpu, NULL, FIQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		dev_footbridge_access(cpu, NULL, VENDOR_ID, b, 4, MEM_READ, x);
		dev_footbridge_access(cpu, NULL, TIMER_1_VALUE, b, 4, MEM_READ, x);
		dev_footbridge_access(cpu, NULL, FIQ_ENABLE_CLEAR, b, 4, MEM_READ, x);
		for (i = 0; i < 5; i++) {
			memory_writemax64(cpu, b, 4, 0x70);
			dev_footbridge_access(cpu, NULL, s5[i].addr, b, 4, s5[i].wf, x);
		}
		check_u("X3 legal writes and other-register reads re-arm NO latch", fatal_calls - f0, 0);
		free(x);
		/*  X4 (codex, pass 2): the FIRST access carries ZERO -- a zero-data write, or the +0x18c read with
		    IRQEnable 0.  A latch guard conditioned on the data (`&& idata`) or on irq_enable, or a direction test
		    rewritten as `!idata`, lets such an access through without an announce; each must announce once and
		    change no field.  */
		for (i = 0; i < 5; i++) {
			x = calloc(1, sizeof(*x)); XSEED(x);
			if (s5[i].wf == MEM_READ)
				x->irq_enable = 0;
			fatal_calls = 0;
			memory_writemax64(cpu, b, 4, 0);
			dev_footbridge_access(cpu, NULL, s5[i].addr, b, 4, s5[i].wf, x);
			snprintf(xn, sizeof(xn), "X4 %s: ZERO data/enable as the FIRST access announces once", s5[i].what + 3);
			check_u(xn, fatal_calls, 1);
			snprintf(xn, sizeof(xn), "X4 %s: ZERO data/enable changes no field", s5[i].what + 3);
			check_u(xn, (x->irq_status == 0x18) + (x->irq_enable == (s5[i].wf == MEM_READ ? 0u : 0x30u))
			    + (x->fiq_status == 0x60) + (x->fiq_enable == 0xc0), 4);
			free(x);
		}
		/*  X5 (codex, pass 2): a LEGAL ZERO EnableClear write is a write, not a declined read -- a direction test
		    rewritten as `idata` sends it to the decline and announces.  */
		x = calloc(1, sizeof(*x)); XSEED(x);
		fatal_calls = 0;
		memory_writemax64(cpu, b, 4, 0);
		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
		check_u("X5 a legal ZERO EnableClear write announces nothing", fatal_calls, 0);
		check_u("X5 ... and leaves IRQEnable at 0x30", x->irq_enable, 0x30);
#undef XSEED
		free(x);
		fatal_calls = 0;
	}

	/*
	 *  #545 CLASS CLOSURE (repair pass 2 -- two consecutive passes found breaches of ONE class, so the
	 *  whole space is enumerated from the handler's own inputs and closed in one block; carrier rule).
	 *
	 *  X6: EVERY DECLINED ACCESS -- site (5) x width (1, 2, 4) x data (zero, nonzero; writes only) x state
	 *      (seeded, all-zero) x occurrence (first, repeated).  Each cell, as ONE row, requires: the handler
	 *      returns 1; the announce count moves by exactly 1 on the first access and 0 on the repeat; all four
	 *      register fields are unchanged; the interrupt output is untouched (no assert, no deassert); and a
	 *      declined read returns 0 over its whole width.
	 *  X7: EVERY LEGAL ACCESS RE-ARMS NO LATCH -- with all five sites latched: each enable write (Set/Clear,
	 *      IRQ/FIQ) with zero and nonzero data, and each legal read of the readable registers plus VENDOR_ID
	 *      and TIMER_1_VALUE at widths 1, 2 and 4; from the seeded state and from the all-zero state (so a
	 *      read that returns 0 is covered).  After each, re-declining all five sites must announce nothing.
	 *
	 *  CONTRACT (clause e): the cells above are the whole class for these five sites.  Not in it: the
	 *  interrupt output after a LEGAL access (the #539 rows), and any other register's semantics.
	 */
	{
		static const struct { uint64_t addr; int wf; const char *nm; } S5[] = {
			{ IRQ_STATUS, MEM_WRITE, "write IRQ_STATUS" }, { IRQ_RAW_STATUS, MEM_WRITE, "write IRQ_RAW_STATUS" },
			{ IRQ_ENABLE_CLEAR, MEM_READ, "read IRQ_ENABLE_CLEAR" }, { FIQ_STATUS, MEM_WRITE, "write FIQ_STATUS" },
			{ FIQ_RAW_STATUS, MEM_WRITE, "write FIQ_RAW_STATUS" } };
		static const struct { uint32_t is, ie, fs, fe; const char *nm; } ST[2] = {
			{ 0x18, 0x30, 0x60, 0xc0, "seeded" }, { 0, 0, 0, 0, "all-zero" } };
		static const int W[3] = { 1, 2, 4 };
		static const struct { uint64_t addr; int wf; uint64_t data; const char *nm; } LW[8] = {
			{ IRQ_ENABLE_SET, MEM_WRITE, 0, "IRQ Set write 0" }, { IRQ_ENABLE_SET, MEM_WRITE, 0x70, "IRQ Set write 0x70" },
			{ IRQ_ENABLE_CLEAR, MEM_WRITE, 0, "IRQ Clear write 0" }, { IRQ_ENABLE_CLEAR, MEM_WRITE, 0x70, "IRQ Clear write 0x70" },
			{ FIQ_ENABLE_SET, MEM_WRITE, 0, "FIQ Set write 0" }, { FIQ_ENABLE_SET, MEM_WRITE, 0x70, "FIQ Set write 0x70" },
			{ FIQ_ENABLE_CLEAR, MEM_WRITE, 0, "FIQ Clear write 0" }, { FIQ_ENABLE_CLEAR, MEM_WRITE, 0x70, "FIQ Clear write 0x70" } };
		static const struct { uint64_t addr; const char *nm; } LR[9] = {
			{ IRQ_STATUS, "IRQ_STATUS" }, { IRQ_RAW_STATUS, "IRQ_RAW_STATUS" }, { FIQ_STATUS, "FIQ_STATUS" },
			{ FIQ_RAW_STATUS, "FIQ_RAW_STATUS" }, { IRQ_ENABLE_SET, "IRQ_ENABLE_SET" }, { FIQ_ENABLE_SET, "FIQ_ENABLE_SET" },
			{ FIQ_ENABLE_CLEAR, "FIQ_ENABLE_CLEAR" }, { VENDOR_ID, "VENDOR_ID" }, { TIMER_1_VALUE, "TIMER_1_VALUE" } };
		unsigned char b[8];
		char xn[200];
		int si, st, wi, dv, ord, k, f0, a0, d0, rv, ok;
		struct footbridge_data *x;
#define XSET(x, s) do { arm_irqs(x); (x)->irq.interrupt_assert = noop_assert; (x)->irq.interrupt_deassert = noop_deassert; \
		(x)->irq_status = ST[s].is; (x)->irq_enable = ST[s].ie; (x)->fiq_status = ST[s].fs; (x)->fiq_enable = ST[s].fe; } while (0)
#define XSAME(x, s) ((x)->irq_status == ST[s].is && (x)->irq_enable == ST[s].ie && (x)->fiq_status == ST[s].fs \
		&& (x)->fiq_enable == ST[s].fe)
		for (si = 0; si < 5; si++)
			for (st = 0; st < 2; st++)
				for (wi = 0; wi < 3; wi++)
					for (dv = 0; dv < (S5[si].wf == MEM_WRITE ? 2 : 1); dv++) {
						x = calloc(1, sizeof(*x)); XSET(x, st);
						fatal_calls = 0;
						for (ord = 0; ord < 2; ord++) {
							a0 = irq_asserts; d0 = irq_deasserts; f0 = fatal_calls;
							memset(b, 0xa5, sizeof(b));
							if (S5[si].wf == MEM_WRITE)
								memory_writemax64(cpu, b, W[wi], dv ? 0x70 : 0);
							rv = dev_footbridge_access(cpu, NULL, S5[si].addr, b, W[wi], S5[si].wf, x);
							ok = rv == 1 && fatal_calls - f0 == (ord == 0 ? 1 : 0) && XSAME(x, st)
							    && irq_asserts == a0 && irq_deasserts == d0
							    && (S5[si].wf != MEM_READ || memory_readmax64(cpu, b, W[wi]) == 0);
							snprintf(xn, sizeof(xn), "X6 %s len %d %s %s %s: declined, fields/irq kept, once",
							    S5[si].nm, W[wi], S5[si].wf == MEM_WRITE ? (dv ? "data 0x70" : "data 0") : "",
							    ST[st].nm, ord ? "repeat" : "first");
							check_u(xn, ok, 1);
						}
						free(x);
					}
		for (st = 0; st < 2; st++)
			for (k = 0; k < 8 + 9 * 3; k++) {
				x = calloc(1, sizeof(*x)); XSET(x, st);
				for (si = 0; si < 5; si++) {
					memory_writemax64(cpu, b, 4, 0x70);
					dev_footbridge_access(cpu, NULL, S5[si].addr, b, 4, S5[si].wf, x);
				}
				f0 = fatal_calls;
				if (k < 8) {
					memory_writemax64(cpu, b, 4, LW[k].data);
					dev_footbridge_access(cpu, NULL, LW[k].addr, b, 4, MEM_WRITE, x);
					snprintf(xn, sizeof(xn), "X7 %s (%s) re-arms NO latch", LW[k].nm, ST[st].nm);
				} else {
					int r = (k - 8) / 3, w = W[(k - 8) % 3];
					memset(b, 0, sizeof(b));
					dev_footbridge_access(cpu, NULL, LR[r].addr, b, w, MEM_READ, x);
					snprintf(xn, sizeof(xn), "X7 legal len %d read of %s (%s) re-arms NO latch", w, LR[r].nm, ST[st].nm);
				}
				for (si = 0; si < 5; si++) {
					memory_writemax64(cpu, b, 4, 0x70);
					dev_footbridge_access(cpu, NULL, S5[si].addr, b, 4, S5[si].wf, x);
				}
				check_u(xn, fatal_calls - f0, 0);
				free(x);
			}
#undef XSAME
#undef XSET
		fatal_calls = 0;
	}
