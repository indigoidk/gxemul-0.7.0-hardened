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

