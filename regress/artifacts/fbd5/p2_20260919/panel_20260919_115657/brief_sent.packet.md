# fbdeclinefive (#545) -- PASS 2: review the REAL DIFF (six files) and the measured kill table

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly, and THIS round's pass-1
packet itself carried two wrong premises ("ten live exit(1)", "HEAD 9c28ca5") that every seat caught.  **Check the
premises, not just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a
premise from something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\src\` at HEAD f685d75 (source of every file below
byte-identical to 9c28ca5/f685d75 -- records-only commits since).**  Copies of `dev_footbridge.c` that are NOT this fork
exist under the project root (`_scratchpad/r6pass2_fb/`, 744 lines, a stale fork copy; three pristine-2021 copies under
`./src/` and `_archive/`).  If your line numbers disagree with mine by tens or hundreds you are reading one of them -- say
so rather than reconciling.

**If you cannot read files that is expected** -- every fact you need is inlined: the WHOLE diff, the whole fixed
enclosing function, the kill-table summary.  Name any premise you cannot settle from this packet rather than guessing.

**Where this brief states an ARITHMETIC claim -- a register offset, an ARM encoding, a row count, a mutant score --
ENUMERATE it rather than reasoning about it.**  Walk the values.  For an ARM word, decode the fields (cond, I, P, U, B,
W, L, Rn, Rd, imm12) rather than pattern-matching the mnemonic.

**VERDICT LINE FIRST**, so your answer survives truncation.  Ordinary engineering language: declines, terminating
calls, latches, detector rows.  This is a bounds-and-correctness review of a device model and its regression rows.

## 1. WHAT THIS ROUND DOES (the design pass 1 converged on; nine seats + the Fable adjudication)

`dev_footbridge.c` (DC21285 "footbridge", CATS machine) ended the emulator process with `exit(1)` when a guest accessed
five interrupt-controller registers in the direction the datasheet does not define: writes to IRQ_STATUS +0x180,
IRQ_RAW_STATUS +0x184, FIQ_STATUS +0x280, FIQ_RAW_STATUS +0x284 (`:6803`: "The Status and RawStatus are read-only, and
EnableClear and Soft are write-only"), and a read of IRQ_ENABLE_CLEAR +0x18c (Table 7-10's read column at 18Ch is `--`).
The fix is option-set member 3 -- DECLINE (no state change; a declined read returns 0 as the fork's POLICY, the nearest
datasheet support being `:1652` "nonexistent CSR ... zeros are read" and Figure 7-2 `:6814`) + a per-site latched
`fatal()` announce carrying `(once)`; five per-site `int` latch fields (fable5 Q3; the file had no latch of any kind); the
+0x18c arm drops its `odata = d->irq_enable` leak (that value is 188h's answer, not 18Ch's).  Four live `exit(1)` remain
in the file: the two SDRAM reads (+0x100/+0x104, `fbsdrampair`) and two construction-time ones in DEVINIT.  NOT touched,
by ruling: +0x28c (FIQ_ENABLE_CLEAR read) already declines silently -- `fiqenableread` facet (2), with the Opus seat's
dissent ("fix it in the same commit") recorded verbatim there; 190h/290h (IRQSoft/FIQSoft) reach `default:` --
`fbirqsoftunimpl`.

In the SAME commit the three probes' kill control (a +0x18c read that relied on the process dying) is RETIRED and
replaced by two HARNESS LEGS through each probe's own launcher: **H1** (an unknown `-E` name: NO prompt AND the
diagnostic `Sorry, emulation "<name>" is unknown.` naming THIS run's input AND `WIFEXITED && == 1`) and **H2** (`quit`
after a prologue VERIFIED by a fresh `reg` -- r3 bit 0 clear, r5 = 0x11223344, r6 = 0x1011, the timer-mask value
0x00345678 in r1 (sites) / r7 (drain, witness) -- then ONE more ordinary `reg` that must fail with `dead` set BEFORE
teardown, and a reap of exit 0).  Both non-obvious H2 clauses are load-bearing: a child dead BEFORE the prologue shows
`next send fails` and `dead` IDENTICALLY (measured, pass 1).

The detector: (a) `footbridge_sites_probe.py` arm S -- the five sites in ONE process, each accessed twice with a legal
sibling read between (rows S1-S5 values, SF1/SF2 final raw reads, N0 five distinct once-announces, N1-N5 per-site
access-local text counts, controls SC1/SA1); (b) `diff_footbridge.c` P-rows (rung-1 DETECTOR, never a witness): a
calloc'd instance seeded BY DIRECT FIELD WRITE (irq_status 0x18, irq_enable 0x30, fiq_status 0x50, fiq_enable 0xc0 -- so
masked != raw), each declined access at three widths, preservation, the read EXPRESSIONS, the announce count (fatal() is a
counter there), a byte-FIRST fresh instance (P9); (c) H1/H2 in all three launchers; (d) gate_arm.sh pins on the legs'
DISCRIMINATING tokens and the arm-S rows.  Two clause-(e) disclosures stand: no GUEST row observes a nonzero status
(irq_status stays 0 under single-step even with a timer armed -- host timers stop at the prompt), and the FIQ read
expressions are pinned only against seeded values no product code produces (`fiq_status` has no writer in the tree).

## 2. SETTLED PREMISES, RE-INLINED SO NOBODY SPENDS AN ANSWER RE-DERIVING THEM (scope: this round)

* `fatal()` PRINTS and returns; it does not exit and is not gated by `-q` (`src/core/debugmsg.c:384-391`; `debug()` is
  gated at `:375`).  Every process death in this device is an explicit `exit(1)`.
* The five sites and directions are TRUE 5/5 (Table 7-10 `dc21285.txt:6821-6833`; §7.3.29-7.3.33; the one-sentence
  form `:6803`).  Table 7-1's "R = Read only. Writes have no effect." is §7.1's PCI-CONFIGURATION legend (`:4505-4520`,
  extracted staggered) -- it TRANSFERS to the CSR tables but is not a sentence about these registers.
* FAULT (member 5) is NOT available on ARM: `memory_rw.c:603-625` dispatches a device-access exception for MIPS and M88K
  only (no `MEM_ARM` arm).  `dev_unreadable.c`'s `return 0` yields MEMORY_ACCESS_FAILED with no abort delivered.
* The file had NO latch field (15 fields, `:60-85`); `struct footbridge_data` is zeroed by DEVINIT's memset (`:771`) AND
  by the offline differentials' `calloc` (`regress/diff_footbridge.c:151`, `diff_fbpending_bound.c:143`).
* The differential's instance has NULL `d->irq` interrupt callbacks under calloc; the enable arms call
  INTERRUPT_ASSERT(d->irq) -- so P-rows seed by direct field write and never through +0x188/+0x18c writes (the P-rows
  install counting no-ops on `d->irq` too, so a legal EnableClear write (P8) is safe).
* Five DIFFERENT startup refusals (`-E nosuch`, no file, missing file, bad option, `-M notanumber`) ALL exit 1 with no
  prompt (Opus, pass 1, s10_legmut.out); only the diagnostic text naming the input discriminates H1.  Two of them print
  the banner first, so the text search covers the whole buffer.
* Unknown `-E`: `machine.c:240` `fatal("\nSorry, emulation \"%s\"", stype)` ... `fatal(" is unknown.\n")`, returns 0 at
  `:258`; `main.c:543-544` `if (!res) exit(1);` -- before any prompt.  `quit`: `debugger_cmds.c:1636-1637` sets the
  shutdown flags; `main.c:807-821` cleans up and returns 0.
* The pass-1 packet's per-site row design was BELOW THE FLOOR: a two-site shared latch and an aggregate latch each swept
  it 29/29 because every row ran one site in its own process (Opus, s6_table.out); the one-process arm S with the N0
  count row is the measured repair (5 / 4 / 1).  A constant-0 IRQ_STATUS read (`m_swallow`) and a dropped `&` at FIQ_STATUS
  (`m_fiqraw`) also swept the guest rows -- the offline P-rows are the repair for the first and a NARROWING for the second.
* The FIQ enable is unobservable from the guest by any route today (+0x288 reads 0: `fiqenableread` facet 1).
* Rows named A1/A2/D1/K1 already existed on the sites probe and are gate-pinned (K1 is RETIRED by this diff; its old
  gate check would read 0, which is why the gate edit is forced).

## 3. THE DIFF -- six files, 34 hunks, against SEC HEAD f685d75 (frozen copies under `_scratchpad/fbd5/p2/`; md5 of the
concatenation 600f9c4b).  THE PRODUCT CHANGE IS ONE FILE and it is inlined WHOLE, as the entire enclosing function:

### 3a. src/devices/dev_footbridge.c -- the struct and the WHOLE DEVICE_ACCESS(footbridge), as a unified diff

```diff
--- a/src/devices/dev_footbridge.c
+++ b/src/devices/dev_footbridge.c
@@ struct footbridge_data (whole) @@
 struct footbridge_data {
 	struct interrupt irq;
 
 	struct pci_data *pcibus;
 
 	int		console_handle;
 
 	uint32_t	timer_load[N_FOOTBRIDGE_TIMERS];
 	uint32_t	timer_value[N_FOOTBRIDGE_TIMERS];
 	uint32_t	timer_control[N_FOOTBRIDGE_TIMERS];
 
 	struct interrupt timer_irq[N_FOOTBRIDGE_TIMERS];
 	struct timer	*timer[N_FOOTBRIDGE_TIMERS];
 	int		pending_timer_interrupts[N_FOOTBRIDGE_TIMERS];
 	/*  #442: the per-timer bound on the counter above, one emulated second of
 	    that timer's delivered rate, recomputed by reload_timer_value().  */
 	int		pending_bound[N_FOOTBRIDGE_TIMERS];
 
 	int		irq_asserted;
 
 	uint32_t	irq_status;
 	uint32_t	irq_enable;
 
 	uint32_t	fiq_status;
 	uint32_t	fiq_enable;
+
+	/*  #545: one warn-once latch per undefined-direction access that used
+	    to end the process (DC21285 7.3.29-7.3.33: "The Status and RawStatus
+	    are read-only, and EnableClear and Soft are write-only").  Zeroed by
+	    DEVINIT's memset and by the offline differentials' calloc.  */
+	int		warned_irq_status_w;
+	int		warned_irq_raw_w;
+	int		warned_irq_clear_r;
+	int		warned_fiq_status_w;
+	int		warned_fiq_raw_w;
 };
@@ DEVICE_ACCESS(footbridge) (the WHOLE enclosing function, every exit path and the common tail) @@
 DEVICE_ACCESS(footbridge)
 {
 	struct footbridge_data *d = (struct footbridge_data *) extra;
 	uint64_t idata = 0, odata = 0;
 	int timer_nr = 0;
 
 	if (writeflag == MEM_WRITE)
 		idata = memory_readmax64(cpu, data, len);
 
 	if (relative_addr >= TIMER_1_LOAD && relative_addr <= TIMER_4_CLEAR) {
 		timer_nr = (relative_addr >> 5) & (N_FOOTBRIDGE_TIMERS - 1);
 		relative_addr &= ~0x060;
 	}
 
 	switch (relative_addr) {
 
 	case VENDOR_ID:
 		odata = 0x1011;  /*  DC21285_VENDOR_ID  */
 		break;
 
 	case DEVICE_ID:
 		odata = 0x1065;  /*  DC21285_DEVICE_ID  */
 		break;
 
 	case 0x04:
 	case 0x0c:
 	case 0x10:
 	case 0x14:
 	case 0x18:
 		/*  TODO. Written to by Linux.  */
 		break;
 
 	case REVISION:
 		odata = 3;  /*  footbridge revision number  */
 		break;
 
 	case PCI_ADDRESS_EXTENSION:
 		/*  TODO: Written to by Linux.  */
 		if (writeflag == MEM_WRITE && idata != 0)
 			fatal("[ footbridge: TODO: write to PCI_ADDRESS_"
 			    "EXTENSION: 0x%llx ]\n", (long long)idata);
 		break;
 
 	case SA_CONTROL:
 		/*  Read by Linux:  */
 		odata = PCI_CENTRAL_FUNCTION;
 		break;
 
 	case UART_DATA:
 		if (writeflag == MEM_WRITE)
 			console_putchar(d->console_handle, idata);
 		break;
 
 	case UART_RX_STAT:
 		/*  TODO  */
 		odata = 0;
 		break;
 
 	case UART_FLAGS:
 		odata = UART_TX_EMPTY;
 		break;
 
 	case IRQ_STATUS:
 		if (writeflag == MEM_READ)
 			odata = d->irq_status & d->irq_enable;
-		else {
-			fatal("[ WARNING: footbridge write to irq status? ]\n");
-			exit(1);
+		else if (!d->warned_irq_status_w) {
+			/*  #545: read-only register (7.3.29); the write is
+			    declined -- no state changes -- and announced once.  */
+			d->warned_irq_status_w = 1;
+			fatal("[ WARNING: footbridge write to irq status? "
+			    "(once) ]\n");
 		}
 		break;
 
 	case IRQ_RAW_STATUS:
 		if (writeflag == MEM_READ)
 			odata = d->irq_status;
-		else {
-			fatal("[ footbridge write to irq_raw_status ]\n");
-			exit(1);
+		else if (!d->warned_irq_raw_w) {
+			/*  #545: read-only (7.3.30); declined, announced once.  */
+			d->warned_irq_raw_w = 1;
+			fatal("[ footbridge write to irq_raw_status (once) ]\n");
 		}
 		break;
 
 	case IRQ_ENABLE_SET:
 		if (writeflag == MEM_WRITE) {
 			d->irq_enable |= idata;
 			if (d->irq_status & d->irq_enable)
 				INTERRUPT_ASSERT(d->irq);
 			else
 				INTERRUPT_DEASSERT(d->irq);
 		} else {
 			/*  #539: a read of 188h is documented -- IRQEnable is
 			    "read-only ... can only be changed by writing to
 			    the EnableSet and EnableClear registers", reset 0
 			    (DC21285 Table 7-10, 7.3.31).  The value below was
 			    always right; the exit(1) that followed it is gone.  */
 			odata = d->irq_enable;
 		}
 		break;
 
 	case IRQ_ENABLE_CLEAR:
 		if (writeflag == MEM_WRITE) {
 			d->irq_enable &= ~idata;
 			if (d->irq_status & d->irq_enable)
 				INTERRUPT_ASSERT(d->irq);
 			else
 				INTERRUPT_DEASSERT(d->irq);
-		} else {
-			odata = d->irq_enable;
+		} else if (!d->warned_irq_clear_r) {
+			/*  #545: IRQEnableClear is write-only (7.3.33) and Table
+			    7-10 names no register at 18Ch for reads, so the read
+			    is declined with 0 -- the IRQEnable value that used to
+			    be computed here is 188h's answer, not 18Ch's.  */
+			d->warned_irq_clear_r = 1;
 			fatal("[ WARNING: footbridge read from "
-			    "ENABLE CLEAR? ]\n");
-			exit(1);
+			    "ENABLE CLEAR? (once) ]\n");
 		}
 		break;
 
 	case FIQ_STATUS:
 		if (writeflag == MEM_READ)
 			odata = d->fiq_status & d->fiq_enable;
-		else {
-			fatal("[ WARNING: footbridge write to fiq status? ]\n");
-			exit(1);
+		else if (!d->warned_fiq_status_w) {
+			/*  #545: read-only (7.3.29); declined, announced once.  */
+			d->warned_fiq_status_w = 1;
+			fatal("[ WARNING: footbridge write to fiq status? "
+			    "(once) ]\n");
 		}
 		break;
 
 	case FIQ_RAW_STATUS:
 		if (writeflag == MEM_READ)
 			odata = d->fiq_status;
-		else {
-			fatal("[ footbridge write to fiq_raw_status ]\n");
-			exit(1);
+		else if (!d->warned_fiq_raw_w) {
+			/*  #545: read-only (7.3.30); declined, announced once.  */
+			d->warned_fiq_raw_w = 1;
+			fatal("[ footbridge write to fiq_raw_status (once) ]\n");
 		}
 		break;
 
 	case FIQ_ENABLE_SET:
 		if (writeflag == MEM_WRITE)
 			d->fiq_enable |= idata;
 		break;
 
 	case FIQ_ENABLE_CLEAR:
 		if (writeflag == MEM_WRITE)
 			d->fiq_enable &= ~idata;
 		break;
 
 	case TIMER_1_LOAD:
 		if (writeflag == MEM_READ)
 			odata = d->timer_load[timer_nr];
 		else {
 			d->timer_load[timer_nr] = idata & TIMER_MAX_VAL;
 			reload_timer_value(cpu, d, timer_nr);
 			/*  debug("[ footbridge: timer %i (1-based), "
 			    "value %i ]\n", timer_nr + 1,
 			    (int)d->timer_value[timer_nr]);  */
 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
 		}
 		break;
 
 	case TIMER_1_VALUE:
 		if (writeflag == MEM_READ)
 			odata = d->timer_value[timer_nr];
 		else
 			d->timer_value[timer_nr] = idata & TIMER_MAX_VAL;
 		break;
 
 	case TIMER_1_CONTROL:
 		if (writeflag == MEM_READ)
 			odata = d->timer_control[timer_nr];
 		else {
 			d->timer_control[timer_nr] = idata;
 			/*  #432: both prescaler bits set is TIMER_EXTERNAL
 			    (0x0C, dc21285reg.h:364) -- a LEGAL named encoding,
 			    and it used to reach fatal()+exit(1) right here, so a
 			    guest selecting the external clock source KILLED THE
 			    HOST.  Arguably likelier than the zero load, since it
 			    is a documented mode rather than a malformed value.
 			    The rate an external clock would actually give is
 			    UNKNOWN and is NOT invented: footbridge_effective_cycles()
 			    now gives the encoding a defined, survivable meaning
 			    (the unprescaled period), and the real semantics are
 			    filed for a round that has a datasheet.  */
 			if (idata & TIMER_ENABLE) {
 				reload_timer_value(cpu, d, timer_nr);
 			} else {
 				d->pending_timer_interrupts[timer_nr] = 0;
 			}
 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
 		}
 		break;
 
 	case TIMER_1_CLEAR:
 		/*  #474: a READ must not perform the clear.  This case carried no
 		    writeflag test at all, while TIMER_1_CONTROL immediately above it
 		    does -- so a guest READ reloaded the counter, decremented the
 		    pending count and DEASSERTED the interrupt.  A guest that merely
 		    read the register silently acknowledged a pending timer interrupt;
 		    the guest-visible consequence is a LOST interrupt, not a bad value.
 
 		    FOUR addresses, not one: the fold above normalises 0x30C/0x32C/
 		    0x34C/0x36C onto this single case.
 
 		    GUARD THE BODY, KEEP THE break.  An early return here would skip
 		    the function's common tail, which writes odata back on a read, and
 		    would hand a guest an untouched buffer -- a defect this code does
 		    not currently have.  */
 		if (writeflag == MEM_WRITE) {
 			if (d->timer_control[timer_nr] & TIMER_MODE_PERIODIC) {
 				reload_timer_value(cpu, d, timer_nr);
 			}
 
 			if (d->pending_timer_interrupts[timer_nr] > 0) {
 				d->pending_timer_interrupts[timer_nr] --;
 			}
 
 			INTERRUPT_DEASSERT(d->timer_irq[timer_nr]);
 		}
 		break;
 
 	case SDRAM_BA_MASK:
 		if (writeflag == MEM_READ) {
 			fatal("[ footbridge read from sdram_ba_mask ]\n");
 			exit(1);
 		} else {
 			switch (idata) {
 			case SDRAM_MASK_256KB:
 			case SDRAM_MASK_512KB:
 			case SDRAM_MASK_1MB:
 			case SDRAM_MASK_2MB:
 			case SDRAM_MASK_4MB:
 			case SDRAM_MASK_8MB:
 			case SDRAM_MASK_16MB:
 			case SDRAM_MASK_32MB:
 			case SDRAM_MASK_64MB:
 			case SDRAM_MASK_128MB:
 			case SDRAM_MASK_256MB:
 				break;
 			default:
 				fatal("[ footbridge write to sdram_ba_mask "
 				    "%#llx ]\n", (long long)idata);
 				break;
 			}
 		}
 		break;
 	case SDRAM_BA_OFFSET:
 		if (writeflag == MEM_READ) {
 			fatal("[ footbridge read from sdram_ba_offset ]\n");
 			exit(1);
 		} else {
 			if (idata != 0)
 				fatal("[ footbridge write to sdram_ba_offset "
 				    "%#llx ]\n", (long long)idata);
 		}
 		break;
 
 	default:if (writeflag == MEM_READ) {
 			fatal("[ footbridge: read from 0x%x ]\n",
 			    (int)relative_addr);
 		} else {
 			fatal("[ footbridge: write to 0x%x: 0x%llx ]\n",
 			    (int)relative_addr, (long long)idata);
 		}
 	}
 
 	if (writeflag == MEM_READ)
 		memory_writemax64(cpu, data, len, odata);
 
 	return 1;
 }
```

### 3b. regress/diff_footbridge.c -- the offline P-rows (1 hunk)

```diff
--- a/regress/diff_footbridge.c
+++ b/regress/diff_footbridge.c
@@ -609,11 +609,113 @@
 		free(h);
 	}
 
-	/*  IDENTITY, as every differential here carries.  */
+	/*
+	 *  #545 P-ROWS -- the five undefined-direction accesses that used to end the process are
+	 *  DECLINED with a latched announce.  These rows pin what no stepped guest can (the guest
+	 *  rows live in footbridge_sites_probe.py, arm S): PRESERVATION under a NONZERO status, the
+	 *  read EXPRESSIONS, the widths, and the latch -- fatal() is a counter here, so the announce
+	 *  is counted, never read (the misname check is the guest rows' job).
+	 *
+	 *  SEEDED BY DIRECT FIELD WRITE, NEVER THROUGH +0x188/+0x18c: this instance's d->irq
+	 *  callbacks are NULL (calloc), and the enable arms call INTERRUPT_ASSERT(d->irq).
+	 *  fiq_status has no writer in the product; seeding it pins the +0x280/+0x284 expressions
+	 *  against a value the product never produces -- a NARROWING of that gap, not its closure.
+	 */
+	{
+		struct footbridge_data *h = calloc(1, sizeof(struct footbridge_data));
+		unsigned char buf[8];
+		char nm[96], nm2[128];
+		int f0, i;
+		static const struct { uint64_t addr; int wf; int len; const char *what; } dec[] = {
+			{ IRQ_STATUS,       MEM_WRITE, 4, "P1 write IRQ_STATUS"       },
+			{ IRQ_RAW_STATUS,   MEM_WRITE, 4, "P2 write IRQ_RAW_STATUS"   },
+			{ IRQ_ENABLE_CLEAR, MEM_READ,  4, "P3 read IRQ_ENABLE_CLEAR"  },
+			{ FIQ_STATUS,       MEM_WRITE, 4, "P4 write FIQ_STATUS"       },
+			{ FIQ_RAW_STATUS,   MEM_WRITE, 4, "P5 write FIQ_RAW_STATUS"   },
+		};
+		arm_irqs(h);
+		h->irq.interrupt_assert = noop_assert;
+		h->irq.interrupt_deassert = noop_deassert;
+		/*  seeds chosen so MASKED != RAW: a dropped `&` (raw returned as status) reds P0  */
+		h->irq_status = 0x18;  h->irq_enable = 0x30;	/*  masked 0x10, raw 0x18  */
+		h->fiq_status = 0x50;  h->fiq_enable = 0xc0;	/*  masked 0x40, raw 0x50  */
+		fatal_calls = 0;	/*  this block counts announces from a clean baseline  */
+#define P_STATE_OK(tag) do { \
+		snprintf(nm2, sizeof(nm2), "%s -- irq_status preserved", tag); check_u(nm2, h->irq_status, 0x18); \
+		snprintf(nm2, sizeof(nm2), "%s -- irq_enable preserved", tag); check_u(nm2, h->irq_enable, 0x30); \
+		snprintf(nm2, sizeof(nm2), "%s -- fiq_status preserved", tag); check_u(nm2, h->fiq_status, 0x50); \
+		snprintf(nm2, sizeof(nm2), "%s -- fiq_enable preserved", tag); check_u(nm2, h->fiq_enable, 0xc0); } while (0)
+#define PN(suffix) (snprintf(nm, sizeof(nm), "%s: %s", dec[i].what, suffix), nm)
+		/*  the legal reads FIRST, on the seeded state: the expressions, not a constant 0  */
+		memset(buf, 0, sizeof(buf));
+		dev_footbridge_access(cpu, NULL, IRQ_STATUS, buf, 4, MEM_READ, h);
+		check_u("P0 IRQ_STATUS read = irq_status & irq_enable (0x10)", memory_readmax64(cpu, buf, 4), 0x10);
+		dev_footbridge_access(cpu, NULL, IRQ_RAW_STATUS, buf, 4, MEM_READ, h);
+		check_u("P0 IRQ_RAW_STATUS read = irq_status (0x18)", memory_readmax64(cpu, buf, 4), 0x18);
+		dev_footbridge_access(cpu, NULL, FIQ_STATUS, buf, 4, MEM_READ, h);
+		check_u("P0 FIQ_STATUS read = fiq_status & fiq_enable (0x40)", memory_readmax64(cpu, buf, 4), 0x40);
+		dev_footbridge_access(cpu, NULL, FIQ_RAW_STATUS, buf, 4, MEM_READ, h);
+		check_u("P0 FIQ_RAW_STATUS read = fiq_status (0x50)", memory_readmax64(cpu, buf, 4), 0x50);
+		check_u("P0 the legal reads announce nothing", fatal_calls, 0);
+		for (i = 0; i < 5; i++) {
+			int a0 = irq_asserts, d0 = irq_deasserts, rv;
+			f0 = fatal_calls;
+			memory_writemax64(cpu, buf, 4, 0x70);	/*  a value inside BOTH enables  */
+			rv = dev_footbridge_access(cpu, NULL, dec[i].addr, buf, dec[i].len, dec[i].wf, h);
+			check_u(PN("handler returned 1 (declined, not failed)"), rv, 1);
+			check_u(PN("announced exactly once"), fatal_calls - f0, 1);
+			if (dec[i].wf == MEM_READ)
+				check_u(PN("the declined read returns 0"), memory_readmax64(cpu, buf, 4), 0);
+			P_STATE_OK(PN("after #1"));
+			check_u(PN("interrupt output untouched"), (irq_asserts - a0) + (irq_deasserts - d0), 0);
+			f0 = fatal_calls;
+			memory_writemax64(cpu, buf, 4, 0x70);
+			dev_footbridge_access(cpu, NULL, dec[i].addr, buf, dec[i].len, dec[i].wf, h);
+			check_u(PN("#2 announced nothing more (latched)"), fatal_calls - f0, 0);
+			memory_writemax64(cpu, buf, 4, 0x70);
+			dev_footbridge_access(cpu, NULL, dec[i].addr, buf, 1, dec[i].wf, h);
+			memory_writemax64(cpu, buf, 4, 0x70);
+			dev_footbridge_access(cpu, NULL, dec[i].addr, buf, 2, dec[i].wf, h);
+			check_u(PN("byte and halfword accesses: still latched"), fatal_calls - f0, 0);
+			P_STATE_OK(PN("after #2, byte, halfword"));
+		}
+		/*  the latches are per SITE: five accesses, five announces, none shared  */
+		check_u("P6 five sites announced five times in one instance", fatal_calls, 5);
+		/*  a legal read after the declines still reads the seeded expressions  */
+		dev_footbridge_access(cpu, NULL, IRQ_STATUS, buf, 4, MEM_READ, h);
+		check_u("P7 IRQ_STATUS read after the declines (0x10)", memory_readmax64(cpu, buf, 4), 0x10);
+		dev_footbridge_access(cpu, NULL, FIQ_RAW_STATUS, buf, 4, MEM_READ, h);
+		check_u("P7 FIQ_RAW_STATUS read after the declines (0x50)", memory_readmax64(cpu, buf, 4), 0x50);
+		/*  a LEGAL EnableClear write still works, next to the declined read of the same address  */
+		memory_writemax64(cpu, buf, 4, 0x10);
+		dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, buf, 4, MEM_WRITE, h);
+		check_u("P8 legal EnableClear write: 0x30 & ~0x10", h->irq_enable, 0x20);
+		check_u("P8 ... announced nothing", fatal_calls, 5);
+#undef PN
+#undef P_STATE_OK
+		free(h);
+		/*  P9: a FRESH instance whose FIRST access to a site is a BYTE write.  A decline that fires only
+		    for len == 4 would let the byte fall through silently -- indistinguishable above, where the
+		    word access had already latched the site.  Here it must announce.  */
+		h = calloc(1, sizeof(struct footbridge_data));
+		arm_irqs(h);
+		h->irq.interrupt_assert = noop_assert;
+		h->irq.interrupt_deassert = noop_deassert;
+		h->irq_status = 0x18;  h->irq_enable = 0x30;
+		fatal_calls = 0;
+		memory_writemax64(cpu, buf, 1, 0x70);
+		dev_footbridge_access(cpu, NULL, IRQ_STATUS, buf, 1, MEM_WRITE, h);
+		check_u("P9 a BYTE write as the first access is declined AND announced", fatal_calls, 1);
+		check_u("P9 ... and stores nothing", h->irq_status, 0x18);
+		free(h);
+		fatal_calls = 0;
+	}
+
+	/*  IDENTITY, as every differential here carries.  #545: 33 -> 111 (78 P-rows).  */
 	{
 		char buf[32];
 		snprintf(buf, sizeof(buf), "%d", rows + 1);
-		check("IDENTITY row count -- guards against a stale copy", buf, "33");
+		check("IDENTITY row count -- guards against a stale copy", buf, "111");
 	}
 
 	printf("\n%d rows, %d failures\n", rows, fails);
```

### 3c. regress/gate_arm.sh -- the footbridge pins (1 hunk; the working tree ALSO carries an unrelated uncommitted
section at :1728+ from another round, which is NOT part of this diff and will not be staged)

```diff
--- a/regress/gate_arm.sh
+++ b/regress/gate_arm.sh
@@ -1095,14 +1095,41 @@
     #  RAM, or any decode that merely absorbed the store, returns 0x12345678 unchanged.
     check "footbridge: TIMER_1_LOAD masked to 24 bits by the handler" \
           "$(grep -cE '^A2 .*got=0x00345678 .*ok$' "$FBLOG")" "1"
-    #  THE PROBE'S OWN FAILABILITY CONTROL.  Arms L and K differ by ONE instruction; K reads
-    #  IRQ_ENABLE_CLEAR (+0x18c, write-only per the DC21285), an UNFIXED fatal()+exit(1) in its
-    #  `case IRQ_ENABLE_CLEAR` read branch.  Without it, "SURVIVED" on every row is satisfied
-    #  by a probe whose guest code never reached the device at all.  #539 moved it here from
-    #  +0x188 (IRQEnable, documented read-only, now readable -- the E rows below); the round
-    #  that declines +0x18c retires this bridge and builds the harness legs in its place.
-    check "footbridge: the one-instruction kill arm still dies" \
-          "$(grep -cE '^K1 .*ok$' "$FBLOG")" "1"
+    #  THE PROBE'S OWN FAILABILITY CONTROLS -- #545 replaced the kill bridge (arm K, a +0x18c read
+    #  the device used to answer with exit(1); #545 declines it) with two HARNESS legs, pinned by
+    #  their DISCRIMINATING tokens, not by the rows existing:
+    #    H1 an unknown -E name: NO prompt, the diagnostic NAMING the input, WIFEXITED && == 1.
+    #       Five different startup refusals all exit 1 with no prompt, so the text is the pin.
+    #    H2 quit after a VERIFIED prologue (fresh-reg values), the next send dead BEFORE
+    #       teardown, reaped exit 0 -- a child dead before the prologue shows `dead` identically,
+    #       so the prologue clause and exit 0 are both required, and both are in the row.
+    check "footbridge: H1 startup leg green (unknown -E named, exit 1)" \
+          "$(grep -cE '^H1 .*named=True .*ok$' "$FBLOG")" "1"
+    check "footbridge: H1's diagnostic names the rejected input" \
+          "$(grep -c 'Sorry, emulation "no-such-machine-fbd5" is unknown' "$FBLOG")" "1"
+    check "footbridge: H2 quit leg green (prologue verified, dead, exit 0)" \
+          "$(grep -cE '^H2 .*prologue=True next=False dead=True exit=0 .*ok$' "$FBLOG")" "1"
+    #  #545: the five declined sites, ONE process (arm S).  N0 counts five DISTINCT once-announces
+    #  (a shared or aggregate latch reads 4 or 1); N1-N5 are per-site and access-local; S1-S5 and
+    #  SF1/SF2 pin every interrupt register unchanged through the declines, with the FINAL raw
+    #  reads after the last write of every pair.
+    check "footbridge: arm S controls (SC1 liveness, SA1 vendor) green" \
+          "$(grep -cE '^S(C1|A1) .*ok$' "$FBLOG")" "2"
+    check "footbridge: N0 five sites, one process, five distinct once" \
+          "$(grep -cE '^N0 .*distinct-once=5 fatals=5 exit=0 .*ok$' "$FBLOG")" "1"
+    check "footbridge: N1-N5 each announced exactly once (count=1)" \
+          "$(grep -cE '^N[1-5] .*count=1.*ok$' "$FBLOG")" "5"
+    check "footbridge: N1-N5 are five DISTINCT green row ids" \
+          "$(grep -oE '^N[1-5] .*ok$' "$FBLOG" | cut -c1-2 | sort -u | wc -l)" "5"
+    check "footbridge: S1-S5 the legal reads between the declines" \
+          "$(grep -cE '^S[1-5] .*ok$' "$FBLOG")" "5"
+    check "footbridge: S3 IRQEnable intact at 0x30 through the declines" \
+          "$(grep -cE '^S3 .*got=0x00000030 .*ok$' "$FBLOG")" "1"
+    check "footbridge: SF1/SF2 final raw status reads after every decline" \
+          "$(grep -cE '^SF[12] .*got=0x00000000 .*ok$' "$FBLOG")" "2"
+    #  #545: the corrected controls -- C4 now requires the key present; C5 requires arm T's exit 0.
+    check "footbridge: C5 the MMU-on control arm survives, exit 0" \
+          "$(grep -cE '^C5 .*ok$' "$FBLOG")" "1"
     #  #539: IRQEnable (+0x188) is readable -- reset 0, Set ORs, Clear clears, byte and
     #  halfword reads return the low lanes -- and arm E raises no footbridge diagnostic.
     #  Seven value/text rows, pinned by count AND by the two that carry the datasheet claims.
```

### 3d. regress/footbridge_sites_probe.py -- the 11 CODE hunks (arm S program, legs H1/H2, rows; the 3 header-prose
hunks are omitted here, their content is section 1).  The two pending probes replace their arm K with the same legs
through their own Session class (drain: r7 = LOADBACK; witness: r7 = LOADBACK) -- not inlined here.

```diff
--- a/regress/footbridge_sites_probe.py
+++ b/regress/footbridge_sites_probe.py
@@ -157,9 +205,54 @@
     (0x24, 0xE5802300, "str r2,[r0,#768]",      "A2: TIMER_1_LOAD <- 0x12345678"),
     (0x28, 0xE5901300, "ldr r1,[r0,#768]",      "A2: read it back"),
 ]
-KILL_NOP  = (0x2c, NOP,        NOPTXT,             "arm L: no kill site")
-KILL_LOAD = (0x2c, 0xE590718C, "ldr r7,[r0,#396]", "arm K: read IRQ_ENABLE_CLEAR (0x18c)")
+KILL_NOP  = (0x2c, NOP,        NOPTXT,             "arm L: no kill site (the +0x18c kill retired by #545)")
 TAIL = [(0x30, NOP, NOPTXT, "landing pad -- planted, never stepped")]
+REG = dict(r0=0, r1=1, r2=2, r3=3, r4=4, r5=5, r6=6, r7=7, r8=8, r9=9, sl=10, fp=11, ip=12, sp=13, lr=14)
+def _mov(rd, imm):                          # imm < 256, rotate 0
+    return 0xE3A00000 | (REG[rd] << 12) | imm, "mov %s,#0x%x" % (rd, imm)
+def _ldr(rd, off):
+    return 0xE5900000 | (REG[rd] << 12) | off, "ldr %s,[r0,#%d]" % (rd, off)
+def _str(rd, off):
+    return 0xE5800000 | (REG[rd] << 12) | off, "str %s,[r0,#%d]" % (rd, off)
+def _w(off, wt, comment):
+    return (off, wt[0], wt[1], comment)
+#  #545: arm S -- the five declined sites, twice each, one legal sibling read between, one process.
+SITES = [
+    _w(0x2c, _mov("r8", 0x30),  "IRQ enable <- 0x30 (bits 4,5)"),
+    _w(0x30, _str("r8", 0x188), ""),
+    _w(0x34, _mov("r9", 0xc0),  "FIQ enable <- 0xc0 (bits 6,7)"),
+    _w(0x38, _str("r9", 0x288), ""),
+    _w(0x3c, _mov("r2", 0x10),  "the IRQ decline value, inside 0x30"),
+    _w(0x40, _str("r2", 0x180), "N1: write IRQ_STATUS (read-only) #1"),
+    _w(0x44, _ldr("r7", 0x184), "S2: legal IRQ_RAW_STATUS read between -> 0"),
+    _w(0x48, _str("r2", 0x180), "N1: write IRQ_STATUS #2 -- must NOT announce again"),
+    _w(0x4c, _str("r2", 0x184), "N2: write IRQ_RAW_STATUS (read-only) #1"),
+    _w(0x50, _ldr("sl", 0x180), "S1: legal IRQ_STATUS read between -> 0 (0 & 0x30)"),
+    _w(0x54, _str("r2", 0x184), "N2: write IRQ_RAW_STATUS #2"),
+    _w(0x58, _ldr("r9", 0x18c), "N3: read IRQ_ENABLE_CLEAR (write-only) #1 -> 0"),
+    _w(0x5c, _ldr("fp", 0x188), "S3: legal IRQEnable read between -> 0x30 (intact)"),
+    _w(0x60, _ldr("r8", 0x18c), "N3: read IRQ_ENABLE_CLEAR #2 -> 0"),
+    _w(0x64, _mov("ip", 0x40),  "the FIQ decline value, inside 0xc0"),
+    _w(0x68, _str("ip", 0x280), "N4: write FIQ_STATUS (read-only) #1"),
+    _w(0x6c, _ldr("r2", 0x280), "S4: legal FIQ_STATUS read between -> 0 (0 & 0xc0)"),
+    _w(0x70, _str("ip", 0x280), "N4: write FIQ_STATUS #2"),
+    _w(0x74, _str("ip", 0x284), "N5: write FIQ_RAW_STATUS (read-only) #1"),
+    _w(0x78, _ldr("lr", 0x284), "S5: legal FIQ_RAW_STATUS read between -> 0"),
+    _w(0x7c, _str("ip", 0x284), "N5: write FIQ_RAW_STATUS #2"),
+    _w(0x80, _ldr("r1", 0x184), "SF1: FINAL raw IRQ status after every decline -> 0"),
+    _w(0x84, _ldr("sp", 0x284), "SF2: FINAL raw FIQ status after every decline -> 0"),
+    (0x88, NOP, NOPTXT, "landing pad -- planted, never stepped"),
+]
+#  #545: the five announce texts, one per site, in the device's own spelling.  ACCESS-LOCAL: each N row
+#  counts ITS text, so a misnamed register reds the row for the site that misnamed it.
+TEXTS = {
+    "N1": "footbridge write to irq status? (once)",
+    "N2": "footbridge write to irq_raw_status (once)",
+    "N3": "footbridge read from ENABLE CLEAR? (once)",
+    "N4": "footbridge write to fiq status? (once)",
+    "N5": "footbridge write to fiq_raw_status (once)",
+}
+H1_NAME = "no-such-machine-fbd5"      # the unknown -E name for leg H1; the diagnostic must name it
 P, Q = 0x00002002, 0x60000000           # #539 arm E values; loaded from DATA+8 / DATA+12
 ENABLE = [                              # #539: the ACCEPT rows, order E0,E1,E2,E3,E6,E5
     (0x2c, 0xE5907188, "ldr r7,[r0,#392]",   "E0: read IRQ_ENABLE_SET before any write"),
@@ -176,14 +269,17 @@
     (0x58, 0xE590C188, "ldr ip,[r0,#392]",   "E5: read back -> Q"),
     (0x5c, NOP, NOPTXT, "landing pad -- planted, never stepped"),
 ]
-REGNAME = {10: "sl", 11: "fp", 12: "ip"}   # the emulator's spellings (cpu_arm.h ARM_REG_NAMES)
+REGNAME = {10: "sl", 11: "fp", 12: "ip", 13: "sp", 14: "lr"}   # the emulator's spellings (cpu_arm.h ARM_REG_NAMES)
 
 
-def run_arm(label, prog):
-    """Plant `prog`, step it one instruction at a time, report registers and liveness."""
+def run_arm(label, prog, emul="cats", quit_leg=False):
+    """Plant `prog`, step it one instruction at a time, report registers and liveness.
+    #545: `emul` is the -E name (leg H1 passes an unknown one and expects NO prompt); `quit_leg`
+    runs leg H2 after the register read -- quit, then one more ordinary interaction, observed
+    BEFORE teardown."""
     pid, fd = pty.fork()
     if pid == 0:
-        os.execvp(BIN, [BIN, "-V", "-T", "-E", "cats", "-M", "32",
+        os.execvp(BIN, [BIN, "-V", "-T", "-E", emul, "-M", "32",
                         "0x%x:%s" % (CODE, STUB)])
         os._exit(127)
     buf = ""
@@ -232,9 +328,10 @@
         except OSError:
             dead[0] = True
             return False
-        return wait(mark=_mark, echo=x if x else None)
+        return wait(mark=_mark, echo=x if x else None, timeout=timeout)
 
     status, regs, badis = "?", {}, []
+    h2 = {}                        # #545 leg H2 observations, all taken BEFORE teardown
     #  KEYWORD, and this is not style.  A positional wait(120) silently becomes mark=120 under
     #  the pinned parameter order -- a real behaviour change, and the exact mistake the
     #  m8820x probe's conversion had to fix in the same commit.
@@ -265,13 +362,25 @@
         if status == "SURVIVED":
             mark = len(buf)
             if send("reg", timeout=30) and not dead[0]:
-                for n in (0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12):
+                for n in (0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14):
                     mm = re.search(r"\b%s\s*=\s*0x([0-9a-fA-F]+)"
                                    % REGNAME.get(n, "r%d" % n), buf[mark:])
                     if mm:
                         regs[n] = int(mm.group(1), 16)
             else:
                 status = "HOST-DIED" if dead[0] else "NO-REG"
+        if status == "SURVIVED" and quit_leg:
+            #  #545 leg H2.  The prologue is VERIFIED from the fresh `reg` above (values, not the fact
+            #  that steps were issued), then `quit`, then ONE MORE ordinary interaction.  `dead` is
+            #  read here, before any teardown, and the reap below must say exit 0.  Do not
+            #  short-circuit the second send because `dead` is already set: the observation IS that
+            #  send() reports the death.
+            h2["prologue_ok"] = (len(badis) == 0 and 3 in regs and (regs[3] & 1) == 0
+                                 and regs.get(5) == 0x11223344 and regs.get(6) == 0x1011
+                                 and regs.get(1) == 0x00345678)
+            h2["quit_rc"] = send("quit", timeout=10)
+            h2["next_rc"] = send("reg", timeout=10)
+            h2["dead_before_close"] = dead[0]
     #  #539 (pass 2): the SAME teardown as the two pending probes -- quit, DRAIN to EOF (bounded), close
     #  the master, then a BOUNDED reap (poll 10 s, kill, wait).  The old sleep-0.3-then-close could SIGHUP a
     #  child still shutting down and then block forever in waitpid; and fatals are collected AFTER the
@@ -323,8 +432,11 @@
     print("  arm %-36s %-9s exit=%-5s signal=%s" % (label, status, code, sig))
     for b in badis:
         print("      DISASSEMBLY MISMATCH: %s" % b)
+    #  #545 leg H1: the startup-rejection diagnostic must name THIS run's -E input (machine.c:240).
+    reject = ('Sorry, emulation "%s" is unknown' % emul) in buf
     return {"status": status, "regs": regs, "exit": code, "signal": sig,
-            "fatals": fatals, "badis": badis}
+            "fatals": fatals, "badis": badis, "reject": reject, "h2": h2,
+            "prompt": "GXemul>" in buf}
 
 
 def hexs(v):
@@ -344,8 +456,10 @@
 
 L = run_arm("L  live      (MMU off)",      MMU_OFF + BODY + [KILL_NOP] + TAIL)
 T = run_arm("T  trap ctrl (MMU LEFT ON)",  MMU_NOP + BODY + [KILL_NOP] + TAIL)
-K = run_arm("K  kill      (MMU off,+18c)", MMU_OFF + BODY + [KILL_LOAD] + TAIL)
 E = run_arm("E  enable    (MMU off,#539)", MMU_OFF + BODY + ENABLE)
+S = run_arm("S  declines  (MMU off,#545)", MMU_OFF + BODY + SITES)
+QL = run_arm("Q  quit leg  (MMU off,#545)", MMU_OFF + BODY + [KILL_NOP] + TAIL, quit_leg=True)   # not `Q`: that is arm E's constant
+H = run_arm("H  startup reject (-E %s)" % H1_NAME, [], emul=H1_NAME)
 print()
 
 results = []
@@ -362,7 +476,8 @@
 #  is never acceptable is arm T producing the device's answer, because then arm L's 0x1011 is
 #  not evidence of anything.  ***
 t_vendor = T["regs"].get(6)
-c4 = t_vendor != 0x1011
+#  #545: the key must be PRESENT -- `None != 0x1011` is True, so a register-parse miss used to green this row.
+c4 = 6 in T["regs"] and t_vendor != 0x1011
 print("%-4s %-40s got=%-12s want=%-12s %s"
       % ("C4", "MMU-on arm CANNOT see the device", hexs(t_vendor), "!= 0x1011",
          "ok" if c4 else "FAIL"))
@@ -372,6 +487,12 @@
     print("      *** cats translation table changed (machine_cats.c:131, cpu_arm.c:239-255)")
     print("      *** or the device moved into the low 256 MB.  Re-derive before believing A1/A2.")
 results.append(c4)
+#  #545: arm T's exit status was recorded and never required; a control arm that died is not a control.
+c5 = T["status"] == "SURVIVED" and T["exit"] == 0
+print("%-4s %-40s %-30s %s"
+      % ("C5", "MMU-on arm SURVIVES, exit 0", "status=%s exit=%s" % (T["status"], T["exit"]),
+         "ok" if c5 else "FAIL"))
+results.append(c5)
 
 #  ---- the reachability rows.  VALUES, not survival. ----
 a1 = row("A1", "VENDOR_ID through a real guest ldr", L["regs"].get(6), 0x1011)
@@ -397,18 +518,68 @@
 results.append(row("A2b", "the value the guest actually stored",
                    L["regs"].get(2), 0x12345678))
 
-#  ---- the kill pair: this probe's own failability control. ----
+#  ---- the isolation arm, and the two HARNESS LEGS (#545) that replaced the kill bridge. ----
 l_ok = L["status"] == "SURVIVED" and L["exit"] == 0 and not L["fatals"]
-k_ok = any("ENABLE CLEAR" in f for f in K["fatals"]) and K["exit"] == 1
 print("%-4s %-40s %-30s %s"
       % ("I1", "isolation arm SURVIVES untouched",
          "status=%s exit=%s" % (L["status"], L["exit"]), "ok" if l_ok else "FAIL"))
-print("%-4s %-40s %-30s %s"
-      % ("K1", "kill arm dies at 0x18c, exit 1",
-         "exit=%s" % K["exit"], "ok" if k_ok else "FAIL"))
-print("      kill arm said: %s" % ((K["fatals"] or ["(nothing)"])[-1]))
 results.append(l_ok)
-results.append(k_ok)
+#  H1: no prompt AND the diagnostic naming this run's input AND WIFEXITED && == 1 (a signal death has
+#  exit None).  Five different startup refusals all exit 1 with no prompt, so the TEXT clause is the one
+#  that discriminates (measured, pass 1).
+h1_ok = (H["status"] == "NO-PROMPT" and not H["prompt"] and H["reject"]
+         and H["exit"] == 1 and H["signal"] is None)
+print("%-4s %-40s %-30s %s"
+      % ("H1", "startup leg: unknown -E named, exit 1",
+         "status=%s exit=%s named=%s" % (H["status"], H["exit"], H["reject"]),
+         "ok" if h1_ok else "FAIL"))
+print("      startup leg said: %s" % ('Sorry, emulation "%s" is unknown.' % H1_NAME if H["reject"]
+                                        else "(the diagnostic did not name the input)"))
+results.append(h1_ok)
+#  H2: the fresh-reg prologue check AND exit 0 are both load-bearing -- a child dead BEFORE the prologue
+#  finished shows `next send fails` and `dead` identically (measured, pass 1).
+q2 = QL["h2"]
+h2_ok = (QL["status"] == "SURVIVED" and q2.get("prologue_ok") is True and q2.get("next_rc") is False
+         and q2.get("dead_before_close") is True and QL["exit"] == 0 and QL["signal"] is None
+         and not QL["fatals"])
+print("%-4s %-40s %-30s %s"
+      % ("H2", "quit leg: verified prologue, dead, exit 0",
+         "prologue=%s next=%s dead=%s exit=%s" % (q2.get("prologue_ok"), q2.get("next_rc"),
+                                                  q2.get("dead_before_close"), QL["exit"]),
+         "ok" if h2_ok else "FAIL"))
+results.append(h2_ok)
+
+#  ---- #545: arm S -- the five declined sites, one process. ----
+sc1 = row("SC1", "arm S liveness: plain RAM readback", S["regs"].get(5), 0x11223344)
+sa1 = row("SA1", "arm S reaches the device: VENDOR_ID", S["regs"].get(6), 0x1011)
+results += [sc1, sa1]
+results.append(row("S1", "IRQ_STATUS read (0 & 0x30) between declines", S["regs"].get(10), 0))
+results.append(row("S2", "IRQ_RAW_STATUS read between declines", S["regs"].get(7), 0))
+results.append(row("S3", "IRQEnable intact through the declines", S["regs"].get(11), 0x30))
+results.append(row("S4", "FIQ_STATUS read (0 & 0xc0) between declines", S["regs"].get(2), 0))
+results.append(row("S5", "FIQ_RAW_STATUS read between declines", S["regs"].get(14), 0))
+results.append(row("SF1", "FINAL raw IRQ status after all declines", S["regs"].get(1), 0))
+results.append(row("SF2", "FINAL raw FIQ status after all declines", S["regs"].get(13), 0))
+n3v_ok = S["regs"].get(9) == 0 and S["regs"].get(8) == 0 and 9 in S["regs"] and 8 in S["regs"]
+s_alive = S["status"] == "SURVIVED" and S["exit"] == 0 and S["signal"] is None
+n_ok = {}
+for tag in ("N1", "N2", "N3", "N4", "N5"):
+    cnt = sum(1 for f in S["fatals"] if TEXTS[tag] in f)
+    ok = s_alive and cnt == 1 and (n3v_ok if tag == "N3" else True)
+    n_ok[tag] = ok
+    print("%-4s %-40s %-30s %s"
+          % (tag, "%s announced ONCE over two accesses" % TEXTS[tag].split(" (once)")[0][11:],
+             "count=%d%s" % (cnt, " r9=%s r8=%s" % (hexs(S["regs"].get(9)), hexs(S["regs"].get(8)))
+                                if tag == "N3" else ""),
+             "ok" if ok else "FAIL"))
+    results.append(ok)
+n0_cnt = sum(1 for t in TEXTS.values() if sum(1 for f in S["fatals"] if t in f) == 1)
+n0_ok = s_alive and n0_cnt == 5 and len(S["fatals"]) == 5
+print("%-4s %-40s %-30s %s"
+      % ("N0", "five sites, one process, five distinct once",
+         "distinct-once=%d fatals=%d exit=%s" % (n0_cnt, len(S["fatals"]), S["exit"]),
+         "ok" if n0_ok else "FAIL"))
+results.append(n0_ok)
 
 #  ---- #539: IRQEnable is readable.  Arm E first proves it reached the device (its own C1
 #  and A1: E0 == 0 is ALSO what an absent device returns), then the value rows. ----
@@ -428,7 +599,7 @@
          "ok" if e_ok else "FAIL"))
 results.append(e_ok)
 
-nbad = sum(len(a["badis"]) for a in (L, T, K, E))
+nbad = sum(len(a["badis"]) for a in (L, T, E, S, QL))
 print("%-4s %-40s %-30s %s"
       % ("D1", "every planted word disassembled as meant",
          "%d mismatches" % nbad, "ok" if nbad == 0 else "FAIL"))
@@ -437,9 +608,9 @@
 #  Named, not indexed.  The first version wrote `results[0] and results[1] ...`, which silently
 #  re-points at different rows the moment a row is inserted above -- the same class as pinning a
 #  row by an id that names a family.
-ctrl_ok = c1 and c2 and c3 and c4 and ec1 and ea1
+ctrl_ok = c1 and c2 and c3 and c4 and c5 and ec1 and ea1 and sc1 and sa1
 print()
 print("ROWS=%d of %d" % (sum(1 for r in results if r), len(results)))
 print("FOOTBRIDGE_SITES_CONTROL=%s" % ("OK" if ctrl_ok else "BAD"))
 print("FOOTBRIDGE_SITES_%s" % ("PASS" if all(results) else "FAIL"))
-print("PROBE_WALL=%.1fs for 4 cold-debugger arms" % (time.time() - t0))
+print("PROBE_WALL=%.1fs for 6 cold-debugger arms" % (time.time() - t0))
```

## 5. THE KILL TABLE (scratch clone /tmp/gxfbd5 of build/; PRETABLE.out written before table 1)

PRETABLE -- fbdeclinefive (#545), written BEFORE table 1 (this file's mtime is the order proof)
Tree: GXEMUL-SEC at HEAD f685d75 (source identical to 9c28ca5); fix = _scratchpad/fbd5/impl/patch_fbd5.py
Detector = footbridge_sites_probe.py arm S (guest rows S1-S5, SF1/SF2, N0-N5, controls SC1/SA1) + legs H1/H2 in all
three launchers + diff_footbridge.c P-rows (P0-P9, 78 rows, IDENTITY 111; seeds irq_status 0x18/enable 0x30,
fiq_status 0x50/enable 0xc0 so masked != raw -- applied BEFORE this file was finalised, per M8/M11 below) + gate pins.
DRY RUNS BEFORE TABLE 1 (scratch copies, no tree written): differential on the FIXED device 111 rows PASS; the SAME
file on the HEAD device dies at P1 (RUN_RC 1, 52 lines) -- the pre-fix red for the offline detector.

== SIBLING PARITY (the arms the diff de-fatalises vs their nearest siblings) ==
  IRQ_STATUS/IRQ_RAW_STATUS/FIQ_STATUS/FIQ_RAW_STATUS write arms  vs  the READ arms of the same cases: the read arms
    have a VALUE channel (masked / raw); the write arms after #545 have a DECLINE channel (announce count, state
    unchanged).  Rows: S1/S2/S4/S5 (value, between declines), N1/N2/N4/N5 (count), SF1/SF2 (final raw), P-rows (seeded).
  IRQ_ENABLE_CLEAR read arm  vs  IRQ_ENABLE_SET read arm (#539 accepted it, E0-E6): SET returns the value, CLEAR
    declines with 0 -- asymmetry BY DESIGN (Table 7-10 names no read register at 18Ch); rows N3 (both reads 0, count 1),
    S3 (enable intact), E5 (the legal Clear write still works), P3/P8.
  IRQ_ENABLE_CLEAR read  vs  FIQ_ENABLE_CLEAR read (+0x28c): the twin ALREADY declines silently; NOT touched -- no
    witness (0 before and after), fiqenableread facet (2) carries the Opus dissent verbatim.  OWED SENTENCE, in the
    probe header: written.
  IRQSoft/FIQSoft (190h/290h) reach default: and announce every access: fbirqsoftunimpl, not this round.

== CLAIM -> ROW (added comment sentences asserting an observable) ==
  dev_footbridge.c "the write is declined -- no state changes -- and announced once"  -> N1..N5 (once), S*/SF*/P (state)
  dev_footbridge.c "the read is declined with 0 -- the IRQEnable value ... is 188h's answer, not 18Ch's" -> N3, P3
  struct comment "Zeroed by DEVINIT's memset and by the offline differentials' calloc" -> P-rows run on a calloc'd
    instance and announce exactly 5 (a non-zeroed latch would announce 0)
  probe header "five different startup refusals ALL exit 1" -> H1 keys on the TEXT (measured pass 1, opus s10)
  probe header "a child dead BEFORE the prologue ... IDENTICALLY" -> H2 requires prologue values AND exit 0
  probe header "Widths ... rowed OFFLINE" -> P-rows len 1/2 per site

== GUARD FIELD vs BODY FIELD ==
  Guard operands (new): warned_irq_status_w, warned_irq_raw_w, warned_irq_clear_r, warned_fiq_status_w,
    warned_fiq_raw_w -- each written at exactly ONE site (its own decline), read at exactly one site.  grep -c
    'warned_.*= 1' == 5 after the patch; no other writer.  A guard testing the WRONG field (copy-paste) = mutant M4.
  Body fields: none (the decline body does nothing but latch + announce); the legal-direction bodies read
    irq_status/irq_enable/fiq_status/fiq_enable -- pinned by P0/P7 seeded reads and S1-S5.
  Disagreeing-state row owed: irq_status != 0 with a decline in flight -> P-rows (seeded 0x10), since no guest row
    can reach it (Q2 f, disclosed for GUEST rows).

== CHANNEL: mutant -> row that reds, and the observable that differs ==
  M1 keepexit    keep exit(1) at FIQ_RAW_STATUS write     -> arm S HOST-DIED: N0/N1-N5/S*/SF* red (exit 1, missing
                                                             rows); P5 rows missing (process dies, RUN_RC 1)
  M2 unlatch     announce on every access at IRQ_STATUS   -> N1 count=2; P1 "#2 announced nothing more" 1 != 0
  M3 sharelatch  IRQ_STATUS and IRQ_RAW_STATUS share warned_irq_status_w -> N0 distinct-once=4, N2 count=0;
                                                             P6 fatal_calls 4 != 5, P2 "announced exactly once" 0
  M4 wrongfield  FIQ_RAW_STATUS tests/sets warned_fiq_status_w (copy-paste) -> same shape as M3 on the FIQ pair:
                                                             N0=4, N5 count=0; P6 4
  M5 leak18c     keep odata = d->irq_enable at the 18c read -> N3 r9/r8 = 0x30 not 0; P3 "declined read returns 0" 48
  M6 store180    the IRQ_STATUS decline stores idata into irq_status -> S1 (0x10&0x30=0x10) / S2 / SF1 = 0x10;
                                                             P1 "irq_status preserved" 0x70 != 0x10
  M7 swallow     IRQ_STATUS READ returns constant 0        -> GUEST rows CANNOT see it (disclosed); P0 "IRQ_STATUS read
                                                             = 0x10" reads 0 -> RED (the reason the P-rows exist)
  M8 fiqraw      FIQ_STATUS read drops the & (returns fiq_status) -> guest rows blind (fiq_status 0); P0 FIQ_STATUS
                                                             read = 0x40 vs seeded fiq_status 0x40 -> NOT distinguished
                                                             (0x40 & 0xc0 == 0x40).  Re-seed: fiq_status 0x50, enable
                                                             0xc0 -> masked 0x40, raw 0x50 -> RED.  ** SEEDS CHANGED
                                                             BEFORE TABLE 1: fiq_status = 0x50; irq_status = 0x18,
                                                             irq_enable = 0x30 -> masked 0x10, raw 0x18. **
  M9 misname     IRQ_RAW_STATUS announce text says "irq status" -> N2 count=0 (access-local text), N1 count=2;
                                                             P-rows blind (fatal() counted, not read) -- guest-only
  M10 latchrd    the 18c read clears warned_irq_clear_r    -> N3 count=2; P3 "#2 announced nothing more" 1
  M11 lenguard   decline only when len == 4 (byte/half fall through silently) -> P "byte and halfword: still latched"
                                                             fatal delta 0 either way -> BLIND; state rows: a fallen-
                                                             through write does nothing -> BLIND.  ** So a len-guarded
                                                             decline is OBSERVATIONALLY EQUIVALENT to the fix on every
                                                             channel here (both decline, both change nothing, both
                                                             announce once via the word access).  Disposition:
                                                             EQUIVALENT MUTANT, recorded, not a hole -- unless the byte
                                                             access is the FIRST access to the site: add P9: a fresh
                                                             instance, byte write FIRST -> announced once. **
  M12 quitless   (harness) H2 leg without the quit         -> H2: next_rc True, dead False -> RED (legmut)
  M13 closefirst (harness) teardown before the observation -> H2 must red: with close() first, send("reg") raises on
                                                             the closed fd -> dead True, next False, exit 0 -> GREEN.
                                                             ** The sites implementation takes h2 BEFORE the teardown
                                                             code by construction; this mutant is a REORDER of the
                                                             probe, i.e. a harness edit; it is the codex Q4 "smallest
                                                             vacuous change".  Measured as a probe mutant in the
                                                             clone, not as a product mutant. **
  M14 h1anyexit  (harness) H1 keyed on exit != 0 only      -> on a correct build stays green; negative control: launch
                                                             with `-M notanumber` -> exit 1, no prompt, no naming text
                                                             -> the shipped H1 predicate REDS, the mutant predicate
                                                             GREENS.  Measured as a harness negative control.

  Rows whose channel cannot vary under any listed mutant: SC1/SA1 (controls, by design), C5.  No vacuous-by-
  construction row found: every S/N/SF/P row names a mutant above.

== PRESCRIBED ROWS (carried forward; a later row list is DIFFED against this) ==
  guest: SC1 SA1 S1 S2 S3 S4 S5 SF1 SF2 N0 N1 N2 N3 N4 N5 H1 H2 C5 (+ existing C1-C4 A1 A2 A2b I1 EC1 EA1 E0-E6 D1)
  offline: P0(5) P1..P5(13/14 each) P6 P7(2) P8(2) + P9 (byte-first fresh instance, from M11)
  legs in drain/witness: H1 H2 rows replacing K
  gate: H1 green, H1 text, H2 green, SC1/SA1, N0 exact, N1-5 count=1 (5), N distinct ids (5), S1-5 (5), S3 value,
        SF1/2 values, C5

== TABLE 1 (09:51, frozen driver run-085140): INSTRUMENT DEFECTS, found by the run, recorded before table 2 ==
  I1 footbridge_sites_probe.py: the quit-leg arm was bound to the name `Q`, shadowing arm E's constant Q = 0x60000000,
     so `P | Q` in row E2 raised TypeError after the N rows printed -- every sites run in table 1 lacks its ROWS= and
     PASS/FAIL lines.  Fix: the arm is `QL`.  (The S/N/H row lines printed before the crash are real but table 1 is
     NOT the round's table.)
  I2 fbpending_witness.py: the R0 detail tuple still named the retired `K` -> NameError in main().  Fix: `("H2", H2)`.
  Both fixed in the patchers (re-applied to fresh scratch copies, compiled, an AST scan finds no `K`/`run_kill` use);
  the pass-2 diff regenerated (34 hunks, md5 14665812).  Table 2 runs the corrected instrument from a fresh clone; table 1's
  logs are kept as table1_instrumentdefect/ for the record.

### Measured results

# #545 fbdeclinefive -- kill table 2 (the round's table), 2026-09-19 08:58-09:03

Scratch clone /tmp/gxfbd5 = `cp -a build/`; baseline dev_footbridge.c cmp == SEC HEAD f685d75; every build FRESH
(`[ gxemul -nt dev_footbridge.c ]`); instruments FROZEN in the clone before the first run; clone-local .MUTANT dropped
first and cleared only after the restore verified (source == SEC HEAD, binary fresh, md5 e5d18154 == the HEAD build).
Table 1 (08:51) found two defects in the INSTRUMENT (a quit-leg arm named `Q` shadowed arm E's constant; the witness
rollup still named the retired `K`) -- recorded in PRETABLE.out, fixed, and table 1 kept as table1_instrumentdefect/.
The patched probes in GXEMUL-SEC are byte-identical to the copies table 2 measured.

| build | sites probe (36 rows) | offline differential (111 rows) | pending probes |
|---|---|---|---|
| HEAD (pre-fix) | **21/36 FAIL** -- SC1 SA1 S1-S5 SF1 SF2 N0-N5 red (arm S dies at its first decline, exit 1) | **dies at P1** (rc 1) | witness H1/H2 ok (legs are product-independent) |
| FIX | **36/36 PASS**, controls OK | **111/111 PASS** | witness PASS, drain H1/H2/R0 ok |
| M1 keep exit(1) at FIQ_RAW_STATUS write | 21/36 (arm S dies) | dies (rc 1) | |
| M2 unlatched announce, IRQ_STATUS | 34/36: N1 N0 | 4 red: P1 latch, P6, P8 | |
| M3 IRQ_STATUS/IRQ_RAW_STATUS share a latch | 34/36: N2 N0 | 3 red: P2 once, P6, P8 | |
| M4 FIQ_RAW_STATUS tests the FIQ_STATUS latch | 34/36: N5 N0 | 3 red: P5 once, P6, P8 | |
| M5 the +0x18c read keeps leaking irq_enable | 35/36: N3 | 1 red: P3 read returns 0 | |
| M6 IRQ_STATUS decline stores into irq_status | 33/36: S1 S2 SF1 | 12 red: preservation | |
| M7 legal IRQ_STATUS read -> constant 0 (Q2 f) | **36/36 -- guest-blind, as DISCLOSED** | 2 red: P0, P7 | |
| M8 FIQ_STATUS read drops the `&` | **36/36 -- guest-blind, as DISCLOSED** | 1 red: P0 FIQ_STATUS | |
| M9 IRQ_RAW_STATUS text misnames the register | 33/36: N1 N2 N0 | **0 red -- offline-blind, as PREDICTED** (fatal() is a counter there) | |
| M10 the +0x18c read clears its own latch | 34/36: N3 N0 | 4 red: P3 latch, P6, P8 | |
| M11 IRQ_STATUS decline only for len == 4 | **36/36 -- guest-blind** | 1 red: P9 byte-first | |
| M12 (harness) H2 without the quit | 35/36: H2 | | |
| M14 (harness) H1 on any nonzero exit, `-M notanumber` launch | weakened H1 **ok** (the vacuity is real) | | |
| M14ctl the SHIPPED H1 predicate, same launch | shipped H1 **FAIL** (named=False) -- the text clause discriminates | | |

**Every product mutant M1-M11 is killed by the COMPOSITE detector** (sites guest rows + offline P-rows).  Three are
killed only offline (M7, M8, M11) and one only by the guest rows (M9) -- each exactly as PRETABLE.out predicted, and the
split is the contract the probe header states: guest rows = reachability, survival, latch count, TEXT; differential
rows = preservation, expression, width.  M13 (teardown moved before the observation) was NOT built: the sites
implementation observes `dead` inside run_arm before the teardown code by construction; recorded as a harness-reorder
mutant owed to pass 2's review, not measured.

Logs: `regress/artifacts/fbd5/killtable_20260919/` (sites_*.log, diff_*.log, witness/drain logs, build logs, the
frozen instruments, TABLE2.log, PRETABLE.out); table 1 under `table1_instrumentdefect/`.  Propagation:
`propagate545.out` -- build/ d19184ee (== the FIX binary above), build-asan/ 0c1fd857, /tmp/gxsec-build c9b4340a, all
part 1 CLEAN + part 2 FRESH; est/ source CLEAN, part 2 N/A.

## 6. QUESTIONS (answer all; number them)

Q1 THE PREMISE AUDIT.  Every load-bearing premise in sections 1-2, stated as a question: TRUE / FALSE / NOT CHECKABLE,
   with the anchor that settles it.  In particular: does the fixed function's common tail still run for every declined
   access (odata 0 for the read, `return 1`)?  Does any of the five arms change state?  Is the +0x18c read's leak gone?
Q2 THE SMALLEST EDIT THAT BREAKS THIS AND STILL PASSES.  Against the diff as written and the table as measured: name the
   edit, the row you expect to stay green, and why.  Candidates the table did NOT build: a `&& len == 4` conjunct on
   ANOTHER site than IRQ_STATUS (P9 covers only IRQ_STATUS); a latch cleared by a LEGAL read of a sibling register; a
   decline that stores into the OTHER family's status; an announce text that names the right register but drops
   `(once)`; a gate pin regex that a duplicated green line satisfies.
Q3 THE FLOOR.  Walk clauses (a)-(f) against the SHIPPED composite detector: (a) fails on the pre-fix build, (b) fails
   on a verbatim reinstatement at EVERY site (the table reinstated ONE), (c) fails on a null medium, (d) DEPENDS-ON
   closure -- enumerate the predicates dominating the edited lines (the five latch tests, `writeflag`) and the
   operand-swap forms drawn from the bodies' read fields; (e) is the contract's disclosure list complete and honest;
   (f) is any row relative-only (anchored?).  A breach is L2 -- say so plainly.
Q4 THE HARNESS LEGS.  Do H1/H2 as implemented in the THREE launchers establish what the kill arm established?  Read
   each launcher's H2 code path: is `dead` observed BEFORE teardown in all three?  Is the prologue verification scored
   (drain/witness: `bad` empty, `len(ex) == PROLOGUE_N`, four register values)?  Does the sites probe's `send()` now
   forward its timeout, and does anything else in the tree depend on the old form?  Name the smallest edit to a leg that
   leaves it green while proving nothing (the table measured "omit quit" and "any nonzero exit"; what else?).
Q5 OPTION-SET AND RECORDS.  Is member 3 still the right disposition given what pass 2 sees?  Is anything in the
   comments or the probe header a WRONG RECORD (a claim the diff or the table refutes)?  Row counts: the differential's
   IDENTITY pin is 111 -- enumerate the P-rows to check it.
STANDING LICENCE: if, while verifying a claim, you found something ELSE -- say so.

End with a seat record: model, files read (with their md5 if you can compute one), nothing run / what you ran.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
