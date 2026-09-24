# #545 repair 3 -- its own pass: does the closure of the INSTANCE axis hold, and which of my dispositions of the closing pass's findings is wrong?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  A seat that re-derives a premise from something this brief did NOT give it is worth more
than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`.**  Repair 3 touches `regress/diff_footbridge.c` and `regress/gate_offline.sh`
only; `src/devices/dev_footbridge.c` is unchanged.  File-reading seats: read the FROZEN copies in
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2e\frozen\` (md5 prefixes: dev_footbridge.c 783c0c7f, diff_footbridge.c
0263974b = the 862-row instrument under review, diff_footbridge.707.c 4d7bdcc3 = the 707-row one before it,
gate_offline.sh 51d291c3), not the working files.  There are pristine-2021-upstream copies of GXemul under the
project root (`./src/`, `_archive/`); they are NOT this fork -- if your line numbers disagree with mine by hundreds
you are reading one of them.

**If you cannot read files that is expected** -- the diff, the handler and the measurements are inlined below.  Name
any premise you cannot settle from this packet rather than guessing.  **ENUMERATE** any count or set rather than
reasoning about it, and ask what the PRODUCER of a value can emit.

**VERDICT LINE FIRST**: `VERDICT: SHIP` or `VERDICT: DO NOT SHIP -- <reason>`.  **A zero needs a denominator**: if
you find nothing, say which cells and which edit shapes you swept.

## What #545 is, and where the chain stands

#545 de-fatalised five arms of the DC21285 "footbridge" model: a guest write to IRQ_STATUS (+0x180), IRQ_RAW_STATUS
(+0x184), FIQ_STATUS (+0x280) or FIQ_RAW_STATUS (+0x284), or a read of IRQEnableClear (+0x18c), used to end the
emulator.  Now each is DECLINED (no register changes; a declined read returns 0) and ANNOUNCED ONCE per site through
a warn-once latch.  The detector is `regress/diff_footbridge.c`, an offline differential that `#include`s the real
device and calls its access function directly, pinned by `regress/gate_offline.sh`.

Passes so far: pass 1, pass 2 (-> repair 1, 491 rows), repair 1's pass (-> repair 2, the CLASS CLOSURE, 707 rows),
and repair 2's closing pass: panel `panel_20260923_172545`, a dedicated codex job, and the Opus measuring seat, which
built 136 new one-line variants of the five arms and the head predicates and found **28 real changes that pass all
707 rows and are not in the contract's NOT COVERED list** (`_scratchpad/fbd5/q2c/opus/SUMMARY.txt`,
`step3_table.txt`).  **That is the fourth pass in a row to find cells of one space.**  What repair 2 missed was not
a cell of the handler's inputs but **the INSTANCE every row runs on** -- a calloc'd struct with its interrupt fields
seeded and ONE counter pair shared by the CPU interrupt and the four timer interrupts -- and **the PRODUCER's
domains**: the widths the ARM load/store unit emits, the lines a device raises, the fields only the interrupt
producer writes.  **This pass verifies repair 3's enumeration; it is not asked to hunt cells one at a time.**

## What repair 3 changes (the full diff is inlined below)

* **X6/X7/X9/X10: width 8** at +0x180 and +0x280 -- the only two sites an LDRD/STRD can reach (the load/store path
  aligns the address down to 8 before `memory_rw`, so +0x184/+0x18c/+0x284 never see len 8).  X6 +32, X7 +8, X9 +8,
  X10 +8 rows.
* **The return value** is now required (`rv == 1`) on X7 and X10-X13 (it was captured nowhere).
* **X11** runs in all four states (+60 rows) and, after each ordered pair, RE-DECLINES both sites: nothing announced.
* **X13** (20 rows): the legal IRQ Clear write at len 1/2 with 0x70 and len 1/2/4 with all-ones data, with EVERY
  latch set (X12 has the same cells with the latches clear).
* **X14** (19 rows), the instance cells: X14 builds its own instances -- the CPU line counted on its OWN pair,
  optionally DEVINIT's timer reset values, and a device line raised through the REAL `footbridge_interrupt_assert()`:
  (1) the Clear write's drive test at its two missing operand cells (both nonzero and DISJOINT; status zero with the
  enable nonzero); (2) each of the seven lines a device raises (4-7 timers, 10 cats ISA, 11 netwinder ISA, 18 cats PCI)
  pending and enabled ALONE; (3) DEVINIT's timer values, then the same with a tick pending: the five legal reads, a
  Set then a Clear, the five declines; (4) `irq_asserted = 1` through the producer: an IRQ_STATUS read, a Clear 0x10
  (deassert) and 0x400 (assert), and a re-arm row (five declines, the legal reads and a Clear, five declines again --
  five announces in all).  Every X14 row that checks a Clear's drive also requires the SHARED pair unmoved.
* **The CONTRACT** (the comment above X6) gains the producer domains, the instance axis, the new COVERED cells and
  new NOT COVERED lines; `gate_offline.sh` pins the new counts and corrects three of #545's own comments.

## Measured (all offline; scratch trees restored and `cmp`-verified; predictions written before every run)

* **FIX: 862 rows, 0 failures, 0 compiler warnings** (`r3_20260923/R3X.log`, instrument md5 0263974b).  The gate's
  own `fb_distinct` counts on it: P 78, X[1-8] 440, X6 248, X7 148, X8 6, X9 100, X10 72, X11 80, X12 20, X13 20,
  X14 19 -- the new pins.  IDENTITY: 862 = 707 + X6 32 + X7 8 + X9 8 + X10 8 + X11 60 + X13 20 + X14 19.
* **The kill table, 652 variants** (`regress/artifacts/fbd5/q2_20260923/r3_20260923/`; `PRETABLE_Q2c.out` 18:31:14
  and `PREDICTIONS.tsv` 18:29:09, both before the 18:34 run): the Opus seat's 570 (its 434 + 136 new), the 58
  carried earlier mutants, the closing pass's S1-S14 and codex V1-V10.  **652 of 652 as predicted: 0 mismatches.**
  Killed: Opus 468 of 570, carried 56 of 58, S 9 of 14, V 9 of 10.  **No row that a variant reddened on 707 went
  green on 862** (0 lost, checked row by row).  All 28 undisclosed escapes are red; so are N_T10 (disclosed before),
  F1 (a latch guard on `!d->timer_control[0]`), V3 and 14 of the 57 earlier exact-value survivors (the X14 states
  hold `irq_status = irq_enable = 0x10`).  Green by prediction: the 51 the Opus seat showed equivalent for guests;
  the 8 disclosed (declined-write data other than 0/0x70; `!timer_value[0]`, `pending_bound[0] <= 1`; the address
  axis); 43 exact-value / case-label / fold / `writeflag != MEM_WRITE` / own-latch forms; M9, Z9 (announce TEXT);
  S1-S4 (`fbenablewidth`), S7 and V4.
* Run 1 of that table measured NOTHING (the scratch trees lacked `config.h`; every build failed; kept in
  `r3_20260923/failed_run1_noconfig/`).  A whole-line row comparison flagged 140 rows: exactly X7's, whose printed
  value went 0 -> 1 when X7's check became `ok == 1`; by name nothing is missing (`SUPERSET_NOTE.txt`).

## §C — SETTLED PREMISES (recorded resolutions; say if the diff or the handler contradicts one)

1. **The product change is settled** -- decline + once-latched announce at the five sites, 0 for the declined read.
   No repair touches `dev_footbridge.c`.
2. **The floor** (the carrier's DEPENDS-ON rule, bounded): the predicates DOMINATING each edited decline, walked to
   the function boundary, crossed with the body-read lvalues' BODY-TESTED partitions where jointly reachable; a value
   or combination the bodies never test as a case is DISCLOSED (clause e), not rowed.  The contract may claim MORE
   than the floor; a claimed cell that a measured edit passes is then a breach of the contract, and repair 3 rows it
   (or narrows the claim) rather than arguing it is above the floor.
3. **Insertion-class edits in OTHER cases** (the +0x188 Set arm, the FIQ enable pair, TIMER_1_VALUE) are outside the
   closure; their existing rows stay, ungraded as floor.  `fbenablewidth` (narrow Set/FIQ writes) is filed.
4. **`fiq_status` has NO writer** in the product: every FIQ status value the rows seed is synthetic.  **`irq_status`
   and `irq_asserted` are written ONLY by `footbridge_interrupt_assert` / `_deassert`** (below).
5. **Width 8 reaches +0x180 and +0x280 only** (the Opus seat, from `cpu_arm_instr_loadstore.c`: `addr &= ~(datalen
   - 1)` before one `memory_rw` of len 8; `memory_rw` passes len through).  An 8-byte access to +0x184, +0x18c or
   +0x284 is not a guest input; the Opus seat's five unaligned width-8 rows were therefore NOT adopted.
6. **The lines a device raises**: DEVINIT connects the four timers to lines 4-7; `bus_pci.c` routes cats ISA to line
   10 (`"%s.10.isa"`), netwinder ISA to 11 (`irq_path_isa` `.11`), and the cats dec21143 to 18 (`irq = 18`).  No
   device raises the other 25 lines, and a guest cannot set a bit of `irq_status`.
7. **DEVINIT's timer reset values**: `timer_control[i] = TIMER_MODE_PERIODIC` (0x40), `timer_load[i] = TIMER_MAX_VAL`
   (0x00FFFFFF), `pending_bound[i] = 1`; a calloc'd instance has all three at 0.

## The handler -- `DEVICE_ACCESS(footbridge)`, the parts this closure is about (verbatim, frozen copy)

NOT SHOWN: the PCI-config, UART and timer arms between `switch (relative_addr) {` and `case IRQ_STATUS:`, and the
timer arms after `case FIQ_ENABLE_CLEAR:`.  They read and write no field the five arms read, EXCEPT that a timer
tick reaches `irq_status` through the interrupt callbacks (see §C.5).

```c
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
	/* ... NOT SHOWN: VENDOR_ID, DEVICE_ID, PCI config, UART ... */

	case IRQ_STATUS:
		if (writeflag == MEM_READ)
			odata = d->irq_status & d->irq_enable;
		else if (!d->warned_irq_status_w) {
			d->warned_irq_status_w = 1;
			fatal("[ WARNING: footbridge write to irq status? "
			    "(once) ]\n");
		}
		break;

	case IRQ_RAW_STATUS:
		if (writeflag == MEM_READ)
			odata = d->irq_status;
		else if (!d->warned_irq_raw_w) {
			d->warned_irq_raw_w = 1;
			fatal("[ footbridge write to irq_raw_status (once) ]\n");
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
		} else if (!d->warned_irq_clear_r) {
			d->warned_irq_clear_r = 1;
			fatal("[ WARNING: footbridge read from "
			    "ENABLE CLEAR? (once) ]\n");
		}
		break;

	case FIQ_STATUS:
		if (writeflag == MEM_READ)
			odata = d->fiq_status & d->fiq_enable;
		else if (!d->warned_fiq_status_w) {
			d->warned_fiq_status_w = 1;
			fatal("[ WARNING: footbridge write to fiq status? "
			    "(once) ]\n");
		}
		break;

	case FIQ_RAW_STATUS:
		if (writeflag == MEM_READ)
			odata = d->fiq_status;
		else if (!d->warned_fiq_raw_w) {
			d->warned_fiq_raw_w = 1;
			fatal("[ footbridge write to fiq_raw_status (once) ]\n");
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

	/* ... NOT SHOWN: the timer arms ... */

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
(The `#545:` and `#539:` comments inside the arms are omitted here; nothing else is.)  Offsets: IRQ_STATUS 0x180,
IRQ_RAW_STATUS 0x184, IRQ_ENABLE_SET 0x188, IRQ_ENABLE_CLEAR 0x18c, FIQ_STATUS 0x280, FIQ_RAW_STATUS 0x284,
FIQ_ENABLE_SET 0x288, FIQ_ENABLE_CLEAR 0x28c; the timer range is TIMER_1_LOAD 0x300 .. TIMER_4_CLEAR 0x36c.


### The producer -- the only writers of `irq_status` and `irq_asserted` (verbatim, frozen `dev_footbridge.c`)

```c
void footbridge_interrupt_assert(struct interrupt *interrupt)
{
	struct footbridge_data *d = (struct footbridge_data *) interrupt->extra;
	d->irq_status |= interrupt->line;

	// Patch from NetBSD:
	// "fix hang interrupt issue. Always assert the irq's even if we have
	//  already asserted the global irq for the device. prevents hangs with
	//  cats."
	if ((d->irq_status & d->irq_enable) /* && !d->irq_asserted */) {
		d->irq_asserted = 1;
		INTERRUPT_ASSERT(d->irq);
	}
}

void footbridge_interrupt_deassert(struct interrupt *interrupt)
{
	struct footbridge_data *d = (struct footbridge_data *) interrupt->extra;
	d->irq_status &= ~interrupt->line;

	if (!(d->irq_status & d->irq_enable) && d->irq_asserted) {
		d->irq_asserted = 0;
		INTERRUPT_DEASSERT(d->irq);
	}
}
```


## The repair-3 diff (INLINED IN FULL, one line of context)

`regress/diff_footbridge.c`, 4d7bdcc3 -> 0263974b (23 hunks):

```diff
--- _scratchpad/fbd5/q2d/diff_footbridge.before_r3x.c	2026-09-23 18:41:24.570214500 -0500
+++ GXEMUL-SEC/regress/diff_footbridge.c	2026-09-23 18:41:24.623349700 -0500
@@ -110,2 +110,35 @@
 
+/*  #545 repair 3, X14: every other block's instance is a calloc with its interrupt fields seeded, counting calls
+    on the CPU line d->irq and the four timer interrupts on ONE pair (noop_assert/noop_deassert).  X14 builds its
+    instances here instead: the CPU line on its OWN pair, optionally DEVINIT's timer reset values, and a device
+    line raised through the real footbridge_interrupt_assert() -- the product's only writer of irq_status and of
+    irq_asserted.  (The Opus seat's scratch closure experiment, q2c pass; adapted.)  */
+static int cpu_asserts, cpu_deasserts;
+static void cpu_assert(struct interrupt *i) { (void) i; cpu_asserts++; }
+static void cpu_deassert(struct interrupt *i) { (void) i; cpu_deasserts++; }
+static struct footbridge_data *x14_new(uint32_t is, uint32_t ie, uint32_t fs, uint32_t fe, int devinit)
+{
+	struct footbridge_data *x = calloc(1, sizeof(*x));
+	int i;
+	arm_irqs(x);
+	x->irq.interrupt_assert = cpu_assert;
+	x->irq.interrupt_deassert = cpu_deassert;
+	x->irq_status = is; x->irq_enable = ie; x->fiq_status = fs; x->fiq_enable = fe;
+	if (devinit)
+		for (i = 0; i < N_FOOTBRIDGE_TIMERS; i++) {
+			x->timer_control[i] = TIMER_MODE_PERIODIC;
+			x->timer_load[i] = TIMER_MAX_VAL;
+			x->pending_bound[i] = 1;
+		}
+	return x;
+}
+static void x14_line(struct footbridge_data *x, int n)
+{
+	struct interrupt it;
+	memset(&it, 0, sizeof(it));
+	it.line = (uint32_t) 1 << n;
+	it.extra = x;
+	footbridge_interrupt_assert(&it);
+}
+
 /* --------------------------------------------------------------- harness --- */
@@ -828,41 +861,95 @@
 	 *  #545 CLASS CLOSURE (repair pass 2 -- two consecutive passes found breaches of ONE class, so the
-	 *  whole space is enumerated from the handler's own inputs and closed in one block; carrier rule).
+	 *  whole space is enumerated from the handler's own inputs and closed in one block; carrier rule).  Its own
+	 *  closing pass found the ENUMERATION wrong again -- in the cells (repair 3: X6-X13, below the CONTRACT) and in
+	 *  the INSTANCES every block is built from (repair 3: X14, the last block before IDENTITY).
 	 *
-	 *  X6: EVERY DECLINED ACCESS -- site (5) x width (1, 2, 4) x data (zero, nonzero; writes only) x state
-	 *      (seeded, all-zero, wide, ones) x occurrence (first, repeated).  Each cell, as ONE row, requires: the handler
-	 *      returns 1; the announce count moves by exactly 1 on the first access and 0 on the repeat; all four
-	 *      register fields are unchanged; the interrupt output is untouched (no assert, no deassert); and a
-	 *      declined read returns 0 over its whole width.
-	 *  X7: EVERY LEGAL ACCESS RE-ARMS NO LATCH -- with all five sites latched: each enable write (Set/Clear,
-	 *      IRQ/FIQ) with zero and nonzero data, and each legal read of the readable registers plus VENDOR_ID
-	 *      and TIMER_1_VALUE at widths 1, 2 and 4; from the seeded, all-zero, wide and ones states (so a read
-	 *      that returns 0 is covered, and so is every bit of every field).  After each, re-declining all five
-	 *      sites must announce nothing.  X7 observes the ANNOUNCE channel only; the value channel of a legal
-	 *      access with the latches set is X10's.
-	 *  X9-X12 (below X8) are the rest of the legal side: X9 with the latches still CLEAR, X10 with every latch
-	 *  SET (value and effect), X11 the cross-site latch ORDER, X12 the legal Clear write's width and data.
+	 *  X6: EVERY DECLINED ACCESS -- site (5) x width (1, 2, 4, and 8 at the two 8-byte-aligned sites) x data (zero,
+	 *      nonzero; writes only) x state (seeded, all-zero, wide, ones) x occurrence (first, repeated).  Each row
+	 *      requires: the handler returns 1; the announce count moves by exactly 1 on the first access, 0 on the
+	 *      repeat; all four register fields are unchanged; the interrupt output is untouched (no assert, no
+	 *      deassert); and a declined read returns 0 over its whole width.
+	 *  X7: EVERY LEGAL ACCESS IT SAMPLES RE-ARMS NO LATCH -- with all five sites latched: each enable write
+	 *      (Set/Clear, IRQ/FIQ) at len 4 with zero and nonzero data, and each legal read of the readable registers
+	 *      plus VENDOR_ID and TIMER_1_VALUE at widths 1, 2 and 4 (and 8 at IRQ_STATUS and FIQ_STATUS); from the four
+	 *      states, so a divert keyed on a zero field or on any one bit announces in one of them.  After each, the
+	 *      access returned 1 and re-declining all five sites announces nothing.  X7 reads NO value; the value channel
+	 *      of a legal access with the latches set is X10's.
+	 *  X9-X13 (below X8) are the rest of the legal side: X9 with the latches still CLEAR, X10 with every latch SET
+	 *  (value and effect), X11 the cross-site latch ORDER and PRESERVATION, X12 and X13 the legal Clear write's
+	 *  width and data with the latches clear and set.
 	 *
-	 *  CONTRACT (clause e).  THE SPACE, enumerated from the handler: the case label (the timer fold maps no
-	 *  address onto these five), the direction test, the width, idata (read by the legal Clear write), the four
-	 *  interrupt fields (read by the legal branches) and the five latches (each read by its own decline).  The
-	 *  bodies TEST only the direction, their own latch, and (irq_status & the new enable) in the Clear write;
-	 *  every other input is a value they compute with.  COVERED: declined x width x data {0, 0x70} x state x
-	 *  first/repeat (X6); legal x width x state x own latch clear (X9) and every latch set (X7 announce, X10
-	 *  value and effect); each ordered pair of sites for the first decline (X11); the legal Clear write at every
-	 *  width and with all-ones data (X9, X12).  STATES: seeded, all-zero, wide and ONES -- with all-zero, the
-	 *  ones state makes every single-bit condition on one field divert in one of the two.
-	 *  *** THIS SAID "the cells above are the whole class" and was measured false TWICE on 2026-09-23: first the
-	 *  reset state (legal x all-zero x latches clear -- five one-conjunct edits to the DIRECTION test passed all
-	 *  333 rows and all 37 guest rows, q2_20260923/Q2.log), then, after X9 closed that, the value channel with
-	 *  the latches set, the cross-site order, the narrow Clear write and any field bit no state set (the Opus
-	 *  seat's 434 variants, _scratchpad/fbd5/q2r/opus/; a row set it built and measured is X10-X12). ***
-	 *  NOT COVERED, stated so a later escape is "outside the contract", not a surprise: a condition on one EXACT
-	 *  field value (`d->irq_enable != 0x10`) -- the bodies test no values and no finite set of states holds them
-	 *  all; the ADDRESS axis -- a case label added for another offset, or a widened timer fold, aliasing an
-	 *  address onto an arm; joint conditions over two fields beyond the four states, or over two latches beyond
-	 *  X11's pairs; WIDE DATA on a declined write (data stays 0 / 0x70); the interrupt output after a legal
-	 *  access except where X9/X10/X12 pin it; any other register's semantics; and a latch guard conditioned on
-	 *  a field neither branch reads (measured F1: `&& !timer_control[0]` passes every row here; the guest sites
-	 *  probe catches it only because its prologue arms timer 1; table4_20260919).  fiq_status has NO writer in
-	 *  the product, so every FIQ status value these rows seed is synthetic.
+	 *  CONTRACT (clause e).  THE SPACE, from the handler and from what the PRODUCER emits: the case label (the
+	 *  timer fold maps no address onto these five -- they sit below TIMER_1_LOAD and have bits 5-6 clear); the
+	 *  direction test; the WIDTH, whose domain is what the ARM load/store unit emits -- 1, 2 and 4, and 8 at
+	 *  +0x180 and +0x280, the two 8-byte-aligned sites (an LDRD/STRD there is ONE 8-byte access:
+	 *  cpu_arm_instr_loadstore.c's `datalen = 8` and a single memory_rw call; an access to +0x184, +0x18c or
+	 *  +0x284 cannot be 8 bytes, it is aligned down first); idata (read by the four legal enable writes -- of those
+	 *  only the IRQ Clear write shares its case, and so its direction test, with a decline); the four interrupt
+	 *  fields (read by the legal branches); and the five latches (each read by its own decline).  The bodies
+	 *  compare no field or data against a constant: they test the direction, their own latch and, in the Clear
+	 *  write, whether (irq_status & the new enable) is zero.  That test's operand cells -- both zero, one zero,
+	 *  both nonzero and DISJOINT, intersecting -- are set by the PRODUCER: footbridge_interrupt_assert() is the
+	 *  only writer of irq_status, and the lines a device raises are the timers (4-7), ISA 10 (cats) and 11
+	 *  (netwinder) and PCI 18 (cats); no device raises the other 25.  And an edit can condition any of the arms'
+	 *  tests on a field NO branch of the five reads -- irq_asserted (written only by that producer), the timer
+	 *  fields (DEVINIT: PERIODIC, TIMER_MAX_VAL, a bound of 1) and the pending ticks -- so the INSTANCE a row runs
+	 *  on is part of the space.
+	 *  COVERED -- the rows named, observing the return value, the announce count, the four fields, the interrupt
+	 *  calls and the read data over the width:
+	 *    declined x width (the site's domain) x data {0, 0x70} x state x first/repeat (X6);
+	 *    the legal READS of the five readable registers x width (the site's domain) x state, every latch clear (X9)
+	 *    and every latch set (X10; X7 for the announce channel);
+	 *    the eight enable writes at len 4, data {0, 0x70}, every latch clear (X9) and set (X7);
+	 *    the IRQ Clear write -- the one legal write inside an edited case -- at len 1, 2 and 4 with 0x70 and with
+	 *    all-ones data (0xff, 0xffff, 0xffffffff), every latch clear (X12) and set (X13), and at len 4 with 0x70
+	 *    and every latch set (X10);
+	 *    each ordered pair of sites in each of the four states: latch j, then i's first decline announces once,
+	 *    returns 1, reads 0 if it is the declined read, and BOTH stay latched (X11);
+	 *    the drive test's disjoint and status-zero cells, and each of the seven raised lines pending alone, with
+	 *    the CPU line counted apart from the timer interrupts (X14); DEVINIT's timer values, without and with a
+	 *    tick pending, at the five legal reads, a Set and a Clear, and the five declines (X14); irq_asserted = 1,
+	 *    raised through the real producer, at the IRQ_STATUS read, the Clear write both ways, and a re-arm row --
+	 *    five declines, the legal reads and a Clear, five declines again, announcing 5 in all (X14).
+	 *  STATES: seeded, all-zero, wide and ONES -- with all-zero, the ones state makes every single-bit condition on
+	 *  one field divert in one of the two.
+	 *  *** THIS SAID "the cells above are the whole class" and was measured false THREE times on 2026-09-23: the
+	 *  reset state (q2_20260923/Q2.log); then the value channel with the latches set, the cross-site order, the
+	 *  narrow Clear write and any field bit no state set (the Opus seat's 434 variants; X10-X12); then, on the
+	 *  closure's OWN closing pass, an 8-byte access at the two aligned sites (grok), the return value unread on
+	 *  X10-X12 (grok), a narrow Clear write after its latch was set (codex), a decline clearing ANOTHER site's latch
+	 *  (codex) and a field x other-latch condition in any state but the seeded one (glm) -- all measured green on
+	 *  707 rows (q2_20260923/closing_20260923/CL.log, CL2.log) -- and on the same pass the Opus seat's 28 (the
+	 *  drive test's operand and single-line cells, WHICH interrupt a Clear drives, the timer fields at their
+	 *  DEVINIT values, a tick pending, and irq_asserted; q2_20260923/q2c_opus/SUMMARY.txt).  All closed by
+	 *  repair 3, X6-X14. ***
+	 *  NOT COVERED, stated so a later escape is "outside the contract", not a surprise:
+	 *    a condition on one EXACT field or data value (`d->irq_enable != 0x10`; `idata != 0x20` at the legal Clear
+	 *    write -- both measured green): the bodies compare nothing against a constant, and no practical set of
+	 *    seeded states holds every value (a field's domain is finite, 2^32, but not enumerable here);
+	 *    JOINT conditions beyond the rowed combinations: two fields beyond the four states; latch vectors other
+	 *    than none, all, the site's own and the X11 pairs (a first decline after two OTHER sites latched); a width
+	 *    and a latch outside the rowed cells;
+	 *    the Set writes (IRQ and FIQ) and the FIQ Clear write below len 4 -- arms that share no case with a decline,
+	 *    so outside the floor: a `len == 4` conjunct on their direction tests, or on the write-data fetch with the
+	 *    Clear address exempted, passes every row (measured, closing_20260923/CL.log; filed `fbenablewidth`);
+	 *    declined-write DATA other than 0 and 0x70 -- wide, 0x55, odd (measured green: q2c_opus N_D02, N_D03, N_D06,
+	 *    N_D11, N_B10);
+	 *    the ADDRESS axis -- a case label added for another offset, or a widened timer fold, aliasing an address onto
+	 *    an arm -- and what an 8-byte access means for the register above the one it lands on (the model answers
+	 *    ONE register per access: an STRD at +0x180 declines IRQ_STATUS once, and its upper word, +0x184's, is no
+	 *    second decline);
+	 *    a mask on one of the 25 bits of the drive test no device raises (a guest cannot set them in irq_status);
+	 *    the IRQ Set write's own drive test (the same `if (d->irq_status & d->irq_enable)`, in an arm that shares no
+	 *    case with a decline): X9 rows it only where (irq_status & the new enable) is nonzero or both operands are
+	 *    zero, so `&&` there passes -- X14's operand and single-line cells are the Clear write's;
+	 *    the interrupt output's LEVEL: these rows count calls on stubbed callbacks, so a line left high
+	 *    (`fbirqstuck`) is invisible here;
+	 *    any other register's semantics; and, beyond X14's cells, a condition in ANY of the arms' tests -- the
+	 *    direction test, a latch test, the write-data fetch, the drive test, a latch clearer -- on a field no branch
+	 *    of the five reads: other timer values (`!d->timer_value[0]`, `d->pending_bound[0] <= 1`: q2c_opus N_T07,
+	 *    N_T08, announce count only), irq_asserted = 1 at the other legal accesses and widths, and a pending tick
+	 *    at the other timers (measured F1:
+	 *    `&& !timer_control[0]` passes every row here; the guest sites probe catches it only because its prologue
+	 *    arms timer 1; table4_20260919).  fiq_status has NO writer in the product, so every FIQ status value these
+	 *    rows seed is synthetic.
 	 */
@@ -882,3 +969,3 @@
 			{ 0xffffffff, 0xffffffff, 0xffffffff, 0xffffffff, "ones" } };
-		static const int W[3] = { 1, 2, 4 };
+		static const int W[4] = { 1, 2, 4, 8 };
 		static const struct { uint64_t addr; int wf; uint64_t data; const char *nm; } LW[8] = {
@@ -902,3 +989,3 @@
 			for (st = 0; st < 4; st++)
-				for (wi = 0; wi < 3; wi++)
+				for (wi = 0; wi < (S5[si].addr == IRQ_STATUS || S5[si].addr == FIQ_STATUS ? 4 : 3); wi++)
 					for (dv = 0; dv < (S5[si].wf == MEM_WRITE ? 2 : 1); dv++) {
@@ -923,3 +1010,3 @@
 		for (st = 0; st < 4; st++)
-			for (k = 0; k < 8 + 9 * 3; k++) {
+			for (k = 0; k < 8 + 9 * 3 + 2; k++) {
 				x = calloc(1, sizeof(*x)); XSET(x, st);
@@ -932,8 +1019,9 @@
 					memory_writemax64(cpu, b, 4, LW[k].data);
-					dev_footbridge_access(cpu, NULL, LW[k].addr, b, 4, MEM_WRITE, x);
+					rv = dev_footbridge_access(cpu, NULL, LW[k].addr, b, 4, MEM_WRITE, x);
 					snprintf(xn, sizeof(xn), "X7 %s (%s) re-arms NO latch", LW[k].nm, ST[st].nm);
 				} else {
-					int r = (k - 8) / 3, w = W[(k - 8) % 3];
+					int r = k < 8 + 27 ? (k - 8) / 3 : (k == 8 + 27 ? 0 : 2);
+					int w = k < 8 + 27 ? W[(k - 8) % 3] : 8;
 					memset(b, 0, sizeof(b));
-					dev_footbridge_access(cpu, NULL, LR[r].addr, b, w, MEM_READ, x);
+					rv = dev_footbridge_access(cpu, NULL, LR[r].addr, b, w, MEM_READ, x);
 					snprintf(xn, sizeof(xn), "X7 legal len %d read of %s (%s) re-arms NO latch", w, LR[r].nm, ST[st].nm);
@@ -944,3 +1032,4 @@
 				}
-				check_u(xn, fatal_calls - f0, 0);
+				ok = rv == 1 && fatal_calls == f0;
+				check_u(xn, ok, 1);
 				free(x);
@@ -954,3 +1043,4 @@
 	    (the masked reads: 0x80010018 & 0x00010030 = 0x00010010, 0x40020060 & 0x000200c0 = 0x00020040).  These
-	    seeds set bits in bytes 0, 2 and 3 only; the ONES state in X6/X7/X9-X12 is what exercises byte 1.  */
+	    seeds set bits in bytes 0, 2 and 3 only; the ONES state is what exercises byte 1 -- X9, X10, X12 and X13 read
+	    or clear it, X6 and X11 require every field to keep it, X7 reads no value.  */
 	{
@@ -1015,3 +1105,3 @@
 		for (st = 0; st < 4; st++)
-			for (k = 0; k < 5 * 3 + 8; k++) {
+			for (k = 0; k < 5 * 3 + 2 + 8; k++) {
 				uint32_t is = S9[st].is, ie = S9[st].ie, fs = S9[st].fs, fe = S9[st].fe;
@@ -1024,7 +1114,7 @@
 				a0 = irq_asserts;  d0 = irq_deasserts;
-				if (k < 15) {
-					int r = k / 3, w = W9[k % 3];
+				if (k < 17) {
+					int r = k < 15 ? k / 3 : (k == 15 ? 0 : 2), w = k < 15 ? W9[k % 3] : 8;
 					uint64_t want = r == 0 ? (uint64_t) (is & ie) : r == 1 ? (uint64_t) is
 					    : r == 2 ? (uint64_t) (fs & fe) : r == 3 ? (uint64_t) fs : (uint64_t) ie;
-					want &= w == 4 ? 0xffffffffULL : w == 2 ? 0xffffULL : 0xffULL;
+					want &= w == 8 ? ~0ULL : w == 4 ? 0xffffffffULL : w == 2 ? 0xffffULL : 0xffULL;
 					memset(b, 0xa5, sizeof(b));
@@ -1037,3 +1127,3 @@
 				} else {
-					int j = k - 15;
+					int j = k - 17;
 					uint32_t old = W8[j].fiq ? fe : ie;
@@ -1066,11 +1156,20 @@
 	    was never made with a LATER site already latched), and the legal Clear write's WIDTH and DATA (every legal
-	    write was len 4 with data 0 or 0x70).  The seat measured this row set in scratch -- it reddened every in-bound
+	    write was len 4, with data 0, 0x10 -- P8's -- or 0x70).  The seat measured this row set in scratch -- it reddened every in-bound
 	    variant that passed -- and it is adopted here with the fourth state added and all-ones Clear data.
-	    X10: every latch SET, then each legal read returns its value over its width, and a legal IRQ Clear write still
-	         clears and drives the output (5 registers x 3 widths + 1 write, x 4 states).
-	    X11: each ordered pair of sites: latch j, then i's FIRST decline announces exactly once and keeps every field
-	         and the interrupt output (20 pairs, seeded).
+	    X10: every latch SET, then each legal read returns 1 and its value over its width (1, 2, 4, and 8 at IRQ_STATUS
+	         and FIQ_STATUS), and a legal IRQ Clear write of 0x70 at len 4 returns 1, clears and drives the output
+	         (5 registers x their widths + 1 write, x 4 states = 18 x 4).
+	    X11: each ordered pair of sites, in each of the four states: latch j, then i's FIRST decline returns 1,
+	         announces exactly once, keeps every field and the interrupt output and (for the declined read) reads 0;
+	         then re-declining j and i announces NOTHING -- both latches kept (20 pairs x 4 states; the seeded rows keep
+	         their original names).
 	    X12: a legal IRQ Clear write at len 1 and 2 with 0x70, and at len 1, 2 and 4 with all-ones data, latches clear
-	         (x 4 states): it clears (ne = ie & ~idata, idata the low bytes the width carries), drives the output once by
-	         (irq_status & ne), announces nothing, and the five declines that follow announce exactly 5.  */
+	         (x 4 states): it returns 1, clears (ne = ie & ~idata, idata the low bytes the width carries), drives the
+	         output once by (irq_status & ne), announces nothing, and the five declines that follow announce exactly 5.
+	    X13 (repair 3): the same five Clear writes with every latch SET: return 1, clear, drive once, announce nothing,
+	         and the five declines that follow still announce nothing.
+	    Repair 3 (the closure's own closing pass, 2026-09-23) added X14 (the instance cells, last block) and the
+	    8-byte cells (X6, X7, X9, X10), the return
+	    value on X7 and X10-X13, X11's other three states and its re-decline, and X13 -- each for a variant measured
+	    green on 707 rows (q2_20260923/closing_20260923/CL.log, CL2.log).  */
 	{
@@ -1090,6 +1189,6 @@
 			{ 2, 0xffffffffULL, "all-ones len 2" }, { 4, 0xffffffffULL, "all-ones len 4" } };
-		static const int WY[3] = { 1, 2, 4 };
+		static const int WY[4] = { 1, 2, 4, 8 };
 		unsigned char b[8];
 		char yn[200];
-		int i, j, st, r, w, c, si, a0, d0, f0, ok;
+		int i, j, st, r, w, c, si, a0, d0, f0, rv, ok;
 		struct footbridge_data *x;
@@ -1105,3 +1204,3 @@
 			for (r = 0; r < 5; r++)
-				for (w = 0; w < 3; w++) {
+				for (w = 0; w < (r == 0 || r == 2 ? 4 : 3); w++) {
 					uint32_t is = SY[st].is, ie = SY[st].ie, fs = SY[st].fs, fe = SY[st].fe;
@@ -1109,3 +1208,3 @@
 					    : r == 2 ? (uint64_t) (fs & fe) : r == 3 ? (uint64_t) fs : (uint64_t) ie;
-					want &= WY[w] == 4 ? 0xffffffffULL : WY[w] == 2 ? 0xffffULL : 0xffULL;
+					want &= WY[w] == 8 ? ~0ULL : WY[w] == 4 ? 0xffffffffULL : WY[w] == 2 ? 0xffffULL : 0xffULL;
 					YNEW(st);
@@ -1114,4 +1213,4 @@
 					memset(b, 0xa5, sizeof(b));
-					dev_footbridge_access(cpu, NULL, RY[r].addr, b, WY[w], MEM_READ, x);
-					ok = fatal_calls == f0 && memory_readmax64(cpu, b, WY[w]) == want && YSAME(st)
+					rv = dev_footbridge_access(cpu, NULL, RY[r].addr, b, WY[w], MEM_READ, x);
+					ok = rv == 1 && fatal_calls == f0 && memory_readmax64(cpu, b, WY[w]) == want && YSAME(st)
 					    && irq_asserts == a0 && irq_deasserts == d0;
@@ -1128,4 +1227,4 @@
 				memory_writemax64(cpu, b, 4, 0x70);
-				dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
-				ok = fatal_calls == f0 && x->irq_enable == ne && x->irq_status == is
+				rv = dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x);
+				ok = rv == 1 && fatal_calls == f0 && x->irq_enable == ne && x->irq_status == is
 				    && x->fiq_status == SY[st].fs && x->fiq_enable == SY[st].fe
@@ -1139,17 +1238,31 @@
 		/*  X11  */
-		for (j = 0; j < 5; j++)
-			for (i = 0; i < 5; i++) {
-				if (i == j)
-					continue;
-				YNEW(0);
-				memory_writemax64(cpu, b, 4, 0x70);
-				dev_footbridge_access(cpu, NULL, DY[j].addr, b, 4, DY[j].wf, x);
-				f0 = fatal_calls; a0 = irq_asserts; d0 = irq_deasserts;
-				memory_writemax64(cpu, b, 4, 0x70);
-				dev_footbridge_access(cpu, NULL, DY[i].addr, b, 4, DY[i].wf, x);
-				ok = fatal_calls - f0 == 1 && YSAME(0) && irq_asserts == a0 && irq_deasserts == d0;
-				snprintf(yn, sizeof(yn), "X11 first %s after %s latched: announced once", DY[i].nm, DY[j].nm);
-				check_u(yn, ok, 1);
-				free(x);
-			}
+		for (st = 0; st < 4; st++)
+			for (j = 0; j < 5; j++)
+				for (i = 0; i < 5; i++) {
+					if (i == j)
+						continue;
+					YNEW(st);
+					memory_writemax64(cpu, b, 4, 0x70);
+					dev_footbridge_access(cpu, NULL, DY[j].addr, b, 4, DY[j].wf, x);
+					f0 = fatal_calls; a0 = irq_asserts; d0 = irq_deasserts;
+					memory_writemax64(cpu, b, 4, 0x70);
+					if (DY[i].wf == MEM_READ)
+						memset(b, 0xa5, sizeof(b));
+					rv = dev_footbridge_access(cpu, NULL, DY[i].addr, b, 4, DY[i].wf, x);
+					ok = rv == 1 && fatal_calls - f0 == 1 && YSAME(st) && irq_asserts == a0 && irq_deasserts == d0
+					    && (DY[i].wf != MEM_READ || memory_readmax64(cpu, b, 4) == 0);
+					f0 = fatal_calls;
+					memory_writemax64(cpu, b, 4, 0x70);
+					dev_footbridge_access(cpu, NULL, DY[j].addr, b, 4, DY[j].wf, x);
+					memory_writemax64(cpu, b, 4, 0x70);
+					dev_footbridge_access(cpu, NULL, DY[i].addr, b, 4, DY[i].wf, x);
+					ok = ok && fatal_calls == f0 && YSAME(st) && irq_asserts == a0 && irq_deasserts == d0;
+					if (st == 0)
+						snprintf(yn, sizeof(yn), "X11 first %s after %s latched: announced once", DY[i].nm, DY[j].nm);
+					else
+						snprintf(yn, sizeof(yn), "X11 first %s after %s latched (%s): announced once",
+						    DY[i].nm, DY[j].nm, SY[st].nm);
+					check_u(yn, ok, 1);
+					free(x);
+				}
 		/*  X12  */
@@ -1162,4 +1275,4 @@
 				memory_writemax64(cpu, b, CY[c].w, CY[c].data);
-				dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, CY[c].w, MEM_WRITE, x);
-				ok = fatal_calls == 0 && x->irq_enable == ne && x->irq_status == is
+				rv = dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, CY[c].w, MEM_WRITE, x);
+				ok = rv == 1 && fatal_calls == 0 && x->irq_enable == ne && x->irq_status == is
 				    && x->fiq_status == SY[st].fs && x->fiq_enable == SY[st].fe
@@ -1173,2 +1286,22 @@
 			}
+		/*  X13  */
+		for (st = 0; st < 4; st++)
+			for (c = 0; c < 5; c++) {
+				uint64_t mask = CY[c].w == 4 ? 0xffffffffULL : CY[c].w == 2 ? 0xffffULL : 0xffULL;
+				uint32_t is = SY[st].is, ne = SY[st].ie & ~(uint32_t) (CY[c].data & mask);
+				YNEW(st);
+				YDECLINE_ALL();
+				f0 = fatal_calls; a0 = irq_asserts; d0 = irq_deasserts;
+				memory_writemax64(cpu, b, CY[c].w, CY[c].data);
+				rv = dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, CY[c].w, MEM_WRITE, x);
+				ok = rv == 1 && fatal_calls == f0 && x->irq_enable == ne && x->irq_status == is
+				    && x->fiq_status == SY[st].fs && x->fiq_enable == SY[st].fe
+				    && ((is & ne) ? (irq_asserts == a0 + 1 && irq_deasserts == d0)
+				                  : (irq_asserts == a0 && irq_deasserts == d0 + 1));
+				YDECLINE_ALL();
+				ok = ok && fatal_calls == f0;
+				snprintf(yn, sizeof(yn), "X13 IRQ Clear write %s (%s, latches SET)", CY[c].nm, SY[st].nm);
+				check_u(yn, ok, 1);
+				free(x);
+			}
 #undef YDECLINE_ALL
@@ -1178,2 +1311,137 @@
 	}
+	/*
+	 *  X14 (repair 3): the cells no block above can reach, because of HOW ITS INSTANCES ARE BUILT.  The Opus seat
+	 *  measured 28 one-line edits green on 707 rows (q2_20260923/q2c_opus/SUMMARY.txt), the smallest ONE
+	 *  character -- `&` -> `&&` in the Clear write's drive test.  Every instance above is a calloc with its
+	 *  interrupt fields seeded, so:
+	 *    the drive test (irq_status & the new enable) was only ever zero with an operand zero, or nonzero with
+	 *    bit 4 or bit 16 in it: never with both operands nonzero and DISJOINT, never with the status zero and the
+	 *    enable not, never with one of the other lines a device raises pending alone (timers 5-7, ISA 10 on cats,
+	 *    11 on netwinder, PCI 18 on cats);
+	 *    the CPU line and the four timer interrupts share one counter pair, so no row could see a Clear write
+	 *    drive the WRONG interrupt;
+	 *    the timer fields sat at 0 where DEVINIT sets PERIODIC, TIMER_MAX_VAL and a bound of 1, and no tick was
+	 *    ever pending;
+	 *    irq_asserted was never 1: its only writer is footbridge_interrupt_assert(), which no block called.
+	 *  Every row here that checks a Clear write's drive also requires the shared pair UNMOVED: the Clear drove the
+	 *  CPU line and no timer interrupt.
+	 *  Width 8 is X6/X7/X9/X10's; +0x184, +0x18c and +0x284 cannot take an 8-byte access.
+	 */
+	{
+		static const int LINE[7] = { 4, 5, 6, 7, 10, 11, 18 };
+		static const struct { uint64_t addr; uint32_t want; } RR[5] = {
+			{ IRQ_STATUS, 0x10 }, { IRQ_RAW_STATUS, 0x18 }, { FIQ_STATUS, 0x40 }, { FIQ_RAW_STATUS, 0x60 },
+			{ IRQ_ENABLE_SET, 0x30 } };
+		static const struct { uint64_t addr; int wf; } DD[5] = {
+			{ IRQ_STATUS, MEM_WRITE }, { IRQ_RAW_STATUS, MEM_WRITE }, { IRQ_ENABLE_CLEAR, MEM_READ },
+			{ FIQ_STATUS, MEM_WRITE }, { FIQ_RAW_STATUS, MEM_WRITE } };
+		static const char *TS[2] = { "DEVINIT timers", "DEVINIT timers, a tick pending" };
+		unsigned char b[8];
+		char zn[200];
+		int i, k, tk, a0, d0, f0, rv, ok;
+		struct footbridge_data *x;
+#define ZZERO() do { cpu_asserts = cpu_deasserts = 0; a0 = irq_asserts; d0 = irq_deasserts; fatal_calls = 0; } while (0)
+#define ZCPU(as, ds) (cpu_asserts == (as) && cpu_deasserts == (ds) && irq_asserts == a0 && irq_deasserts == d0)
+#define ZCLR(v) do { memory_writemax64(cpu, b, 4, (v)); \
+		rv = dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x); } while (0)
+#define ZDECLINE() do { for (i = 0; i < 5; i++) { memset(b, 0xa5, sizeof(b)); \
+		if (DD[i].wf == MEM_WRITE) memory_writemax64(cpu, b, 4, 0x70); \
+		rv = dev_footbridge_access(cpu, NULL, DD[i].addr, b, 4, DD[i].wf, x); \
+		ok = ok && rv == 1 && (DD[i].wf == MEM_WRITE || memory_readmax64(cpu, b, 4) == 0); } } while (0)
+		/*  The drive test's operand cells: both nonzero and disjoint (`&&` for `&` asserts there), and the status
+		    zero with the enable not (a test of the enable alone asserts there).  */
+		x = x14_new(0x18, 0x30, 0x60, 0xc0, 0);
+		ZZERO();
+		ZCLR(0x10);
+		check_u("X14 Clear 0x10 from 0x18/0x30 (disjoint): 0x20, CPU line deasserted once",
+		    rv == 1 && x->irq_enable == 0x20 && ZCPU(0, 1) && fatal_calls == 0, 1);
+		free(x);
+		x = x14_new(0, 0x30, 0, 0, 0);
+		ZZERO();
+		ZCLR(0x10);
+		check_u("X14 Clear 0x10 from 0/0x30 (no status): 0x20, CPU line deasserted once",
+		    rv == 1 && x->irq_enable == 0x20 && ZCPU(0, 1) && fatal_calls == 0, 1);
+		free(x);
+		/*  Each line a device raises, pending and enabled ALONE: a Clear of nothing asserts the CPU line.  */
+		for (k = 0; k < 7; k++) {
+			x = x14_new((uint32_t) 1 << LINE[k], (uint32_t) 1 << LINE[k], 0, 0, 0);
+			ZZERO();
+			ZCLR(0);
+			snprintf(zn, sizeof(zn), "X14 Clear 0, only line %d pending and enabled: CPU line asserted once",
+			    LINE[k]);
+			check_u(zn, rv == 1 && x->irq_enable == (uint32_t) 1 << LINE[k] && ZCPU(1, 0) && fatal_calls == 0, 1);
+			free(x);
+		}
+		/*  DEVINIT's timer reset values, then with a tick pending: the five legal reads return their values and
+		    announce nothing; a Set then a Clear land; the five declines announce exactly 5 and keep the fields.  */
+		for (tk = 0; tk < 2; tk++) {
+			x = x14_new(0x18, 0x30, 0x60, 0xc0, 1);
+			x->pending_timer_interrupts[0] = tk;
+			ZZERO();
+			ok = 1;
+			for (i = 0; i < 5; i++) {
+				memset(b, 0xa5, sizeof(b));
+				rv = dev_footbridge_access(cpu, NULL, RR[i].addr, b, 4, MEM_READ, x);
+				ok = ok && rv == 1 && memory_readmax64(cpu, b, 4) == RR[i].want;
+			}
+			snprintf(zn, sizeof(zn), "X14 %s: the five legal reads return their values", TS[tk]);
+			check_u(zn, ok && fatal_calls == 0, 1);
+			memory_writemax64(cpu, b, 4, 0x40);
+			rv = dev_footbridge_access(cpu, NULL, IRQ_ENABLE_SET, b, 4, MEM_WRITE, x);
+			ok = rv == 1;
+			ZCLR(0x10);
+			snprintf(zn, sizeof(zn), "X14 %s: Set 0x40 then Clear 0x10 leave 0x60", TS[tk]);
+			check_u(zn, ok && rv == 1 && x->irq_enable == 0x60 && fatal_calls == 0, 1);
+			ok = 1;
+			ZDECLINE();
+			snprintf(zn, sizeof(zn), "X14 %s: the five declines announce 5, keep the fields", TS[tk]);
+			check_u(zn, ok && fatal_calls == 5 && x->irq_status == 0x18 && x->irq_enable == 0x60
+			    && x->fiq_status == 0x60 && x->fiq_enable == 0xc0, 1);
+			free(x);
+		}
+		/*  irq_asserted = 1, through the real callback: a device raises line 4 with line 4 enabled.  */
+		x = x14_new(0, 0x10, 0, 0, 0);
+		ZZERO();
+		x14_line(x, 4);
+		ok = x->irq_asserted == 1 && x->irq_status == 0x10 && ZCPU(1, 0);
+		ZZERO();
+		memset(b, 0xa5, sizeof(b));
+		rv = dev_footbridge_access(cpu, NULL, IRQ_STATUS, b, 4, MEM_READ, x);
+		check_u("X14 line 4 raised by a device: IRQ_STATUS reads 0x10",
+		    ok && rv == 1 && memory_readmax64(cpu, b, 4) == 0x10 && fatal_calls == 0, 1);
+		free(x);
+		for (k = 0; k < 2; k++) {
+			x = x14_new(0, 0x10, 0, 0, 0);
+			x14_line(x, 4);
+			ok = x->irq_asserted == 1;
+			ZZERO();
+			ZCLR(k ? 0x400 : 0x10);
+			snprintf(zn, sizeof(zn), "X14 line 4 raised by a device: Clear %s, CPU line %s once",
+			    k ? "0x400 keeps it" : "0x10 clears it", k ? "asserted" : "deasserted");
+			check_u(zn, ok && rv == 1 && x->irq_enable == (k ? 0x10u : 0u) && (k ? ZCPU(1, 0) : ZCPU(0, 1))
+			    && fatal_calls == 0, 1);
+			free(x);
+		}
+		x = x14_new(0, 0x10, 0, 0, 0);
+		x14_line(x, 4);
+		ok = x->irq_asserted == 1;
+		ZZERO();
+		ZDECLINE();
+		f0 = fatal_calls;
+		for (i = 0; i < 5; i++) {
+			rv = dev_footbridge_access(cpu, NULL, RR[i].addr, b, 4, MEM_READ, x);
+			ok = ok && rv == 1;
+		}
+		ZCLR(0x400);
+		ok = ok && rv == 1;
+		ZDECLINE();
+		check_u("X14 line 4 raised by a device: 5 declines, then the legal reads and a Clear re-arm no latch",
+		    ok && f0 == 5 && fatal_calls == 5, 1);
+		free(x);
+#undef ZDECLINE
+#undef ZCLR
+#undef ZCPU
+#undef ZZERO
+		fatal_calls = 0;
+	}
 	/*  IDENTITY, as every differential here carries.  #545: 33 -> 333 (the 33 are the 32 timer rows and this one;
@@ -1181,3 +1449,4 @@
 	    state, X9 69); its repair's own pass 2: 491 -> 707 (the ones state: X6 +54, X7 +35, X9 +23; X10 64, X11 20,
-	    X12 20).  */
+	    X12 20); the closure's closing pass (repair 3): 707 -> 862 (the 8-byte cells: X6 +32, X7 +8, X9 +8, X10 +8;
+	    X11's other three states +60; X13 20; X14 19).  */
 	{
@@ -1185,3 +1454,3 @@
 		snprintf(buf, sizeof(buf), "%d", rows + 1);
-		check("IDENTITY row count -- guards against a stale copy", buf, "707");
+		check("IDENTITY row count -- guards against a stale copy", buf, "862");
 	}
```

`regress/gate_offline.sh`, 45d2b495 -> 51d291c3 (6 hunks):

```diff
--- _scratchpad/fbd5/q2d/gate_offline.before_r3x.sh	2026-09-23 18:41:24.552329700 -0500
+++ GXEMUL-SEC/regress/gate_offline.sh	2026-09-23 18:41:24.602836700 -0500
@@ -571,3 +571,5 @@
 #  a narrower class (a zero-guard conditioned on the prescaler bits survives D2 and dies in F1).
-#  Detection is unaffected either way: every grep below fails on a truncated log.
+#  Detection is unaffected either way: a truncated log fails the row-count, failure-count and verdict
+#  checks below, which read the file's LAST lines (a per-row presence grep can still find a row printed
+#  before the cut -- this said "every grep below fails" until #545's repair 3, which is not so).
 FBBIN=$LOGDIR/diff_footbridge
@@ -587,3 +589,3 @@
     check_min "footbridge: rows actually run" \
-              "$(grep -oE '^[0-9]+ rows' "$FBLOG" | grep -oE '^[0-9]+')" 707
+              "$(grep -oE '^[0-9]+ rows' "$FBLOG" | grep -oE '^[0-9]+')" 862
     check     "footbridge: offline verdict" "$(grep -c 'DIFF_FOOTBRIDGE_PASS' "$FBLOG")" "1"
@@ -595,3 +597,3 @@
     #  site x width x data x state x first/repeat -- keeps every field and the interrupt output and reads
-    #  0; every legal access with every latch set re-arms no latch.  X8: wide (multi-byte) seeds, so a legal read
+    #  0; each legal access X7 samples, with every latch set, re-arms no latch.  X8: wide (multi-byte) seeds, so a legal read
     #  truncated to 8 bits reds.  X9 (the adjudication pass, 2026-09-23): the legal accesses with the latches still
@@ -601,7 +603,13 @@
     #  with every latch set, X11 each ordered pair of sites' latches, X12 the legal Clear write's width and data.
-    #  STATES in X6/X7/X9/X10/X12: seeded, all-zero, wide and ONES -- the ones state sets every bit of every field,
-    #  so with all-zero a condition keyed on any single bit diverts in one of the two.  Not covered, and said so in
-    #  diff_footbridge.c's contract: a condition on one exact field value, and the address axis.
+    #  STATES in X6/X7/X9-X13: seeded, all-zero, wide and ONES -- the ones state sets every bit of every field,
+    #  so with all-zero a condition keyed on any single bit diverts in one of the two.  Repair 3 (the closure's own
+    #  closing pass): the 8-byte LDRD/STRD cells at +0x180/+0x280 (X6, X7, X9, X10), the return value (X7,
+    #  X10-X13), X11 in all four states with a re-decline, X13 the narrow Clear write with every latch set, and X14
+    #  the INSTANCE cells no other block could reach -- the drive test's disjoint and single-line cells on a CPU
+    #  counter pair of its own, DEVINIT's timer values with and without a pending tick, and irq_asserted raised
+    #  through the real footbridge_interrupt_assert().  Not covered, and said so in diff_footbridge.c's contract:
+    #  exact field or data values, the address axis, narrow Set/FIQ writes (fbenablewidth), the Set write's own
+    #  drive test, the interrupt LEVEL (fbirqstuck), and joints beyond the rowed cells.
     #  Kill tables: regress/artifacts/fbd5/{killtable,xtable,table3,table4}_20260919/ and
-    #  regress/artifacts/fbd5/q2_20260923/{repair,repair2}/.
+    #  regress/artifacts/fbd5/q2_20260923/{repair,repair2,r3_20260923}/.
     #  COUNTED AS DISTINCT GREEN ROW NAMES, not green lines (adjudication pass, G10): a duplicated green
@@ -610,10 +618,12 @@
     check "footbridge: #545 P-rows green (P0-P9), distinct names" "$(fb_distinct 'P[0-9]')" "78"
-    check "footbridge: #545 X-rows green (X1-X8), distinct names" "$(fb_distinct 'X[1-8]')" "400"
-    check "footbridge: #545 X6 every declined-access cell green" "$(fb_distinct 'X6')" "216"
-    check "footbridge: #545 X7 every legal access re-arms no latch" "$(fb_distinct 'X7')" "140"
+    check "footbridge: #545 X-rows green (X1-X8), distinct names" "$(fb_distinct 'X[1-8]')" "440"
+    check "footbridge: #545 X6 every declined-access cell green" "$(fb_distinct 'X6')" "248"
+    check "footbridge: #545 X7 every sampled legal access re-arms no latch" "$(fb_distinct 'X7')" "148"
     check "footbridge: #545 X8 wide legal reads keep all 32 bits" "$(fb_distinct 'X8')" "6"
-    check "footbridge: #545 X9 legal access, latches clear, all states" "$(fb_distinct 'X9')" "92"
-    check "footbridge: #545 X10 legal access, latches SET, value kept" "$(fb_distinct 'X10')" "64"
-    check "footbridge: #545 X11 every ordered pair of site latches" "$(fb_distinct 'X11')" "20"
+    check "footbridge: #545 X9 legal access, latches clear, all states" "$(fb_distinct 'X9')" "100"
+    check "footbridge: #545 X10 legal access, latches SET, value kept" "$(fb_distinct 'X10')" "72"
+    check "footbridge: #545 X11 every ordered pair of site latches, four states" "$(fb_distinct 'X11')" "80"
     check "footbridge: #545 X12 legal Clear write, every width and data" "$(fb_distinct 'X12')" "20"
+    check "footbridge: #545 X13 legal Clear write, latches SET" "$(fb_distinct 'X13')" "20"
+    check "footbridge: #545 X14 instance cells (drive test, DEVINIT, irq_asserted)" "$(fb_distinct 'X14')" "19"
     #  Name each row that is the SOLE detector of something.
@@ -693,5 +703,6 @@
           "$(grep -cE 'reads back as 0, not normalised|stays 0 on read-back' "$FBLOG")" "2"
-    #  The two forked end-to-end rows: these are the ones that prove the HOST SURVIVES, and
-    #  they are forked so a mutant that re-crashes is a named-row KILL rather than a census
-    #  FAULT that takes the gate binary with it.
+    #  The two forked end-to-end rows: these are the ones that prove the HOST SURVIVES.  Their
+    #  forks do NOT make every re-crash a named-row kill: an unconditional one takes the binary
+    #  down at the unforked D2 first (ON THE FORKS, CORRECTED, above).  G1's fork is load-bearing
+    #  and F1's holds a narrower class.  (This comment said otherwise until #545's repair 3.)
     check "footbridge: the end-to-end survival rows are present" \
```

## §F2 — the closing pass's findings, with MY disposition of each

*(Self-review disclosed: I wrote repairs 1-3 and every disposition below.  Seats whose finding I adopted: check that
the ROWS answer your finding, not merely that the finding was right.  The closing pass's verdicts on repair 2: codex,
grok, glm, deepseek, minimax and the kimi substitute DO NOT SHIP; agy split; the kimi CLI walled; the Opus seat
DO NOT SHIP by measurement.)*

**G1 -- width 8** (grok; my S8/S9/S10).  An LDRD/STRD at +0x180 or +0x280 is ONE 8-byte access; no row used len 8.
**ACCEPTED** -> X6/X7/X9/X10 width-8 cells at those two sites.  S8 7 red, S9 8, S10 7.
**G2 -- the handler's return value was never read** (grok S11; codex-dedicated).  **ACCEPTED** -> `rv == 1` on X7 and
X10-X13.  S11 (`if (len != 4) return 0;` after the Clear write's drive) 32 red.
**G3 -- no narrow Clear write with its latch set; no latched all-ones Clear** (codex-dedicated S12).  **ACCEPTED** ->
X13.  S12 (`writeflag == MEM_WRITE && (len == 4 || !d->warned_irq_clear_r)`) 16 red.
**G4 -- a decline clearing ANOTHER site's latch** (codex; S13 `warned_irq_raw_w = 0` in the IRQ_STATUS decline, S14
the FIQ_RAW mirror).  X11 never re-declined the earlier site.  **ACCEPTED** -> X11 re-declines both sites after each
pair.  S13, S14 red.
**G5 -- a field x other-latch joint outside the seeded state** (glm S6: `!(d->irq_status == 0 && d->warned_irq_raw_w)`;
X11 ran seeded only).  **ACCEPTED** -> X11 in all four states.  S6 red.
**G6 -- narrow Set / FIQ-enable writes** (deepseek, kimi substitute, minimax: S1-S3) **and the fetch exempting only the
Clear address** (minimax S4).  **DISCLOSED, outside the floor**: those arms share no case with a decline, and the
fetch feeds only `idata`, which no decline reads.  Filed `fbenablewidth`.  The contract's "legal x width" sentence was
a wrong record (L4) and now names them.
**G7 -- exact DATA values** (the Opus seat's `idata != 0x20`, S7) **and a narrow ZERO-data or latched zero-data Clear
write** (codex-dedicated: no row makes either).  **DISCLOSED** (clause e): the Clear body computes with `idata`, it
never tests it as a case; the contract's NOT COVERED names exact field OR DATA values and the joints.
**G8 -- the read tail `if (writeflag == MEM_READ) memory_writemax64(...)`, missing from THE SPACE** (codex-dedicated).
**NO ROW OWED**: it post-dominates rather than dominates the declines, and X6's "a declined read returns 0 over its
width" already fails if the tail skips a read.
**G9 -- three false comments in #545's own gate section** (codex-dedicated: "every grep below fails on a truncated
log"; "forked so a re-crash is a named-row KILL" -- already measured false by the section's own ON THE FORKS
paragraph; "every legal access with every latch set").  **ACCEPTED**, all three corrected.
**G10 -- "the bodies compare no field against a constant" hid that the Clear write's drive test DOES partition a
value** (codex-dedicated).  **ACCEPTED**: THE SPACE now names the drive test's operand cells.
**O1 -- the Opus seat's 28 undisclosed** (by group, enumerated: the drive test's operators and masks 10, the
interrupt calls 5, the timer fields and irq_asserted 6, the fetch 3, width 8 3, a latch re-arm 1).  **ACCEPTED** -> X14, plus
repair 3's width-8 cells for N_L06/N_L07/N_L10.  All 28 red.
**O2 -- the seat's Z6 (eleven width-8 rows, six at +0x184/+0x18c/+0x284)**.  **NOT ADOPTED**: those six are not guest
inputs (§C.5) and are the only reason N_L08/N_L11 went red in its scratch run; the aligned ones duplicate repair 3.
**O3 -- the harness's instances are not reset-faithful** (calloc leaves the timer fields 0; nothing sets
`irq_asserted`).  **ACCEPTED IN PART**: X14 adds DEVINIT-faithful and producer-driven instances FOR THE CELLS IT ROWS;
every other block keeps its calloc instance.  Re-seating all 843 older rows was not done (Q5 asks whether that was
wrong).
**O4 -- NOT COVERED's "a latch guard conditioned on a field neither branch reads" named one site of a wider class**
(the same conditions in the direction, fetch and drive tests and in a latch clearer passed too).  **ACCEPTED**: the
line now names every test, and what X14 rows of it.
**O5 -- the drive rows count calls on ONE pair shared by the CPU line and the timer interrupts**, so a Clear write
driving the WRONG interrupt was invisible (N_I05, N_I06).  **ACCEPTED**: X14's own CPU pair; the older rows keep the
shared pair, and X14's header says so.
**O6 -- sibling parity (mine): the IRQ SET write has the same drive test**, rowed by X9 only where (status & enable) is
nonzero or both are zero, so `&&` there passes.  **DISCLOSED** (outside the floor, like G6).
**O7 -- N_R05**, a legal IRQ_STATUS read clearing +0x184's latch only while `irq_asserted` (the seat's scratch rows did
not target it).  **ACCEPTED** -> X14's re-arm row (red).  It also reddens N_T10 (disclosed before: a latch guard on
`!d->irq_asserted` at +0x18c's decline), because that row's first round must announce 5.

**D1 -- DO NOT SHIP on repair 2** (all answering seats but agy).  **Settled by measurement**: every S-case the panel
raised was measured, and the Opus seat's 28 are real.

**WHERE I MIGHT BE FOOLING MYSELF**: X14's instance axis is rowed at len 4 only, at a handful of states, and only the
IRQ_STATUS read carries a value check with `irq_asserted = 1`.  The contract discloses that -- but disclosure is only
honest if the undisclosed remainder is empty, and repair 2 also believed that.

## §E -- QUESTIONS (answer each, numbered; if you are answering from this packet alone, do Q1 and Q3 first)

**Q1 -- verify the enumeration.**  The rewritten CONTRACT (the comment above X6, in the diff) states THE SPACE, what is
COVERED and what is NOT COVERED.  (a) Is every input, every body-tested partition, every PRODUCER domain and every
INSTANCE field an edit can condition on named in THE SPACE?  Name any missing.  (b) For each X14 row, name the edit it
is for and the observable that DIFFERS under that edit -- a row whose observable cannot vary under its edit holds
nothing.  (c) Is every NOT COVERED line genuinely outside the floor of §C.2 -- or a claimed cell a one-line edit
passes?
**Q2 -- the smallest edit to `dev_footbridge.c`'s five arms, the two head predicates or the producer pair that the 862
rows cannot see and the contract does not disclose.**  Name it, the rows you expect to stay green, and why.  If none,
give your denominator: which edit shapes, at which arms, in which instance states.
**Q3 -- adjudicate §F2**: G1-G10, O1-O7, D1 -- UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.
Then: **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  In particular O2 (Z6 not adopted), O3 (instances re-seated for
X14 only), O6 (the Set arm's drive test disclosed rather than rowed) and G7/G8 (no row owed).
**Q4 -- records.**  Is any sentence in the changed comments (the CONTRACT, the X10-X14 headers, the helper comment
above `x14_new`, the IDENTITY comment, the gate_offline.sh comment and pins) false as of today?  ENUMERATE the
IDENTITY arithmetic (862 = 707 + 32 + 8 + 8 + 8 + 60 + 20 + 19) and the gate pins (P 78, X[1-8] 440, X6 248, X7 148,
X8 6, X9 100, X10 72, X11 80, X12 20, X13 20, X14 19) against the loops in the diff.
**Q5 -- option-set completeness.**  For O3 and O6 I chose partial re-seating and disclosure.  Is there a disposition
I did not name?

If, while verifying a claim, you found something ELSE -- say so.

End with a seat record: model, what you read, what you ran.
