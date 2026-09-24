# #545 repair 3c -- its own pass: did 3c close the cells X14 claimed, and is my scope ruling on the producer pair right?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  A seat that re-derives a premise from something this brief did NOT give it is worth more
than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`.**  3c touches `regress/diff_footbridge.c` and `regress/gate_offline.sh`
only; `src/devices/dev_footbridge.c` is unchanged.  File-reading seats: read the FROZEN copies in
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2f\frozen\` (dev_footbridge.c 783c0c7f, diff_footbridge.c 8309c5b7 =
the 864-row instrument under review, diff_footbridge.862.c 0263974b = repair 3 before this, gate_offline.sh 59149a8b).
There are pristine-2021-upstream copies of GXemul under the project root (`./src/`, `_archive/`); they are NOT this
fork -- line numbers off by hundreds mean you are reading one of them.

**If you cannot read files that is expected** -- the diff, the key code and the measurements are inlined below.  Name
any premise you cannot settle from this packet rather than guessing.  **ENUMERATE** any count or set rather than
reasoning about it.  **VERDICT LINE FIRST**: `VERDICT: SHIP` or `VERDICT: DO NOT SHIP -- <reason>`.  **A zero needs a
denominator**: say which cells and edit shapes you swept.

## Where #545 stands

#545 de-fatalised five arms of the DC21285 "footbridge" model (guest writes to IRQ_STATUS +0x180, IRQ_RAW_STATUS
+0x184, FIQ_STATUS +0x280, FIQ_RAW_STATUS +0x284, and a read of IRQEnableClear +0x18c used to end the emulator; now each
is declined and announced once per site).  The detector is `regress/diff_footbridge.c`, an offline differential that
`#include`s the real device, pinned by `regress/gate_offline.sh`.  Repair 3 (862 rows) added X13 and X14 -- X14 builds
its own instances: the CPU interrupt counted apart from the timer interrupts, DEVINIT's timer values with and without
a pending tick, and a device line raised through the real `footbridge_interrupt_assert()`.

**Repair 3's own pass** (panel `panel_20260923_184633`: codex, agy, grok, glm, deepseek, the kimi substitute DO NOT
SHIP, minimax SHIP, the kimi CLI walled; a dedicated codex job; the Opus measuring seat, `_scratchpad/fbd5/q2e/opus/`)
found: (1) NINE one-line edits green on 862 rows at cells X14's COVERED list claims, on channels its rows did not read
(the Opus seat, measured); (2) FIVE edits in the producer pair `footbridge_interrupt_assert()` / `_deassert()`, green
because nothing calls `_deassert()` and `_assert()` is called once per instance from a zero status (every seat named
this); (3) width 8 also reaches the enable arms at +0x188/+0x288, and IRQEnable's 8-byte read (grok, glm, codex, the
kimi substitute); (4) WHICH interrupt a narrow Clear write drives is invisible (codex); (5) a latched Clear of 0 is
unobserved (grok); (6) a dozen false or stale sentences.

## What 3c changes (the full diff is inlined below)

* **(1) is ROWED**, by giving five X14 rows the channels they claimed and adding one row per timer state:
  the DEVINIT reads now require no interrupt call; the DEVINIT "Set 0x40 then Clear 0x10" row requires the drive
  (Set asserts, Clear deasserts: ZCPU(1, 1)); the DEVINIT declines row requires no call; NEW: "Clear 0x20 keeps 0x10
  pending and enabled: CPU line asserted once" at DEVINIT values (the other polarity); the line-4 IRQ_STATUS read
  requires the fields unchanged and no call; the re-arm row requires the five read VALUES, one CPU assert over the
  whole sequence and the final fields.  862 -> 864 rows.
* **(2) is DISCLOSED, not rowed, and filed with `fbirqstuck`** -- MY SCOPE RULING, and the one I most want challenged:
  #545 never edited the producer pair, the pair does not dominate any edited line, and rowing it would make this
  detector claim the pair's whole state space (assert/deassert x lines x enable x history), which is how a detector
  becomes a chain.  The Opus seat built 19 scratch rows including five for the pair (881 rows, all 14 escapes red); 3c
  adopts none of its producer rows.
* **(3), (4), (5) are DISCLOSED** in the contract (the enable arms are outside the floor, like `fbenablewidth`; the
  destination below len 4 and a latched Clear of 0 are joints of values the bodies do not test).
* **(6)**: THE SPACE, COVERED (per-family channels, the X12/X13 attribution), NOT COVERED (the producer pair, the
  8-byte read's upper word -- covered, not "not covered" -- the exact-value examples), the X14 header and helper
  comments, and the gate's truncation sentence.

## Measured (offline; scratch trees restored and `cmp`-verified; predictions written before the table)

* **FIX: 864 rows, 0 failures, 0 compiler warnings**; the gate's counts: P 78, X[1-8] 440, X6 248, X7 148, X8 6,
  X9 100, X10 72, X11 80, X12 20, X13 20, X14 21 (the new pins).  Every row name of the 862-row run is present.
* **The table, 711 variants** (`regress/artifacts/fbd5/q2_20260923/r3c_20260923/`; `PRETABLE_Q2d.out` 19:19:41 and
  `PREDICTIONS.tsv` 19:19:17, before the 19:19:54 run): repair 3's 652, the Opus seat's 54, and five panel shapes
  (codex's `^=` in the assert producer and its narrow-width destination, grok's `len != 8` fetch and latched Clear 0,
  deepseek's `irq_status = 0` in deassert).  **709 as predicted; 0 rows lost.**  All nine X14-cell escapes are red, so
  are IA01 and IA15 and the two `e_dir_A1_irq_*` exact-value forms (the re-arm row now reads IRQ_RAW_STATUS's value).
  The producer edits (PR01-PR07, `^=`, `= 0`) and the other disclosed shapes are green, as predicted.
* **The two mismatches were my prediction, not the detector**: S7 and `idata_A2_ne20` (`idata != 0x20` at the Clear
  arm) went RED because the new row writes the data 0x20.  So the contract's NOT COVERED example was false at 864 rows;
  corrected, comment only (`PRETABLE_Q2d.corrections`; the instrument's code is byte-identical to c187b754 and re-ran
  864/0).

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
5. **Width 8 reaches the 8-byte-aligned offsets only** (`cpu_arm_instr_loadstore.c`: `addr &= ~(datalen - 1)` before
   one `memory_rw` of len 8; `memory_rw` passes len through): of the five decline sites +0x180 and +0x280, and the
   enable arms +0x188 and +0x288.  An 8-byte access to +0x184, +0x18c or +0x284 is not a guest input.
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


## The 3c diff (INLINED IN FULL, one line of context; includes the r3b comment corrections)

`regress/diff_footbridge.c`, 0263974b -> 8309c5b7 (19 hunks):

```diff
--- _scratchpad/fbd5/q2d/diff_footbridge.before_r3b.c	2026-09-23 19:15:04.389255100 -0500
+++ GXEMUL-SEC/regress/diff_footbridge.c	2026-09-23 19:25:50.611135400 -0500
@@ -113,4 +113,4 @@
     instances here instead: the CPU line on its OWN pair, optionally DEVINIT's timer reset values, and a device
-    line raised through the real footbridge_interrupt_assert() -- the product's only writer of irq_status and of
-    irq_asserted.  (The Opus seat's scratch closure experiment, q2c pass; adapted.)  */
+    line raised through the real footbridge_interrupt_assert() -- with footbridge_interrupt_deassert(), the only
+    writers of irq_status and of irq_asserted.  (The Opus seat's scratch closure experiment, q2c pass; adapted.)  */
 static int cpu_asserts, cpu_deasserts;
@@ -882,6 +882,8 @@
 	 *  timer fold maps no address onto these five -- they sit below TIMER_1_LOAD and have bits 5-6 clear); the
-	 *  direction test; the WIDTH, whose domain is what the ARM load/store unit emits -- 1, 2 and 4, and 8 at
-	 *  +0x180 and +0x280, the two 8-byte-aligned sites (an LDRD/STRD there is ONE 8-byte access:
-	 *  cpu_arm_instr_loadstore.c's `datalen = 8` and a single memory_rw call; an access to +0x184, +0x18c or
-	 *  +0x284 cannot be 8 bytes, it is aligned down first); idata (read by the four legal enable writes -- of those
+	 *  direction test; the WIDTH, whose domain is what the ARM load/store unit emits -- 1, 2 and 4, and 8 at the
+	 *  8-byte-aligned offsets: of the five decline sites, +0x180 and +0x280 (an LDRD/STRD there is ONE 8-byte
+	 *  access: cpu_arm_instr_loadstore.c's `datalen = 8` and a single memory_rw call; an access to +0x184, +0x18c
+	 *  or +0x284 cannot be 8 bytes, it is aligned down first), and the enable arms at +0x188 and +0x288 too (grok,
+	 *  glm and codex on repair 3's pass: this said "the two 8-byte-aligned sites"); idata (read by the four legal
+	 *  enable writes -- of those
 	 *  only the IRQ Clear write shares its case, and so its direction test, with a decline); the four interrupt
@@ -890,10 +892,12 @@
 	 *  write, whether (irq_status & the new enable) is zero.  That test's operand cells -- both zero, one zero,
-	 *  both nonzero and DISJOINT, intersecting -- are set by the PRODUCER: footbridge_interrupt_assert() is the
-	 *  only writer of irq_status, and the lines a device raises are the timers (4-7), ISA 10 (cats) and 11
-	 *  (netwinder) and PCI 18 (cats); no device raises the other 25.  And an edit can condition any of the arms'
-	 *  tests on a field NO branch of the five reads -- irq_asserted (written only by that producer), the timer
-	 *  fields (DEVINIT: PERIODIC, TIMER_MAX_VAL, a bound of 1) and the pending ticks -- so the INSTANCE a row runs
-	 *  on is part of the space.
-	 *  COVERED -- the rows named, observing the return value, the announce count, the four fields, the interrupt
-	 *  calls and the read data over the width:
+	 *  both nonzero and DISJOINT, intersecting -- are set by the PRODUCER: footbridge_interrupt_assert() and
+	 *  _deassert() are the only writers of irq_status, and the lines a device raises are the timers (4-7), ISA 10
+	 *  (cats) and 11 (netwinder) and PCI 18 (cats); no device raises the other 25.  And an edit can condition any
+	 *  of the arms' tests on a field NO branch of the five reads -- irq_asserted (written only by that pair), the timer
+	 *  fields (DEVINIT: PERIODIC, TIMER_MAX_VAL, a bound of 1; timer_value 0), the pending ticks, and the rest of the
+	 *  instance (the CPU interrupt's own fields, pcibus, console_handle, the timer handles) -- so the INSTANCE a row
+	 *  runs on is part of the space.
+	 *  COVERED -- the rows named, each observing the channels it names: the return value, the announce count, the
+	 *  four fields, the interrupt calls and the read data over the width, except X7 (the return value and the
+	 *  announce count only) and X14's rows (the channels in each row's name and header):
 	 *    declined x width (the site's domain) x data {0, 0x70} x state x first/repeat (X6);
@@ -902,5 +906,5 @@
 	 *    the eight enable writes at len 4, data {0, 0x70}, every latch clear (X9) and set (X7);
-	 *    the IRQ Clear write -- the one legal write inside an edited case -- at len 1, 2 and 4 with 0x70 and with
-	 *    all-ones data (0xff, 0xffff, 0xffffffff), every latch clear (X12) and set (X13), and at len 4 with 0x70
-	 *    and every latch set (X10);
+	 *    the IRQ Clear write -- the one legal write inside an edited case -- at len 1 and 2 with 0x70 and at len 1,
+	 *    2 and 4 with all-ones data (0xff, 0xffff, 0xffffffff), every latch clear (X12) and set (X13); at len 4 with
+	 *    0 and 0x70, latches clear (X9), and with 0x70, every latch set (X10);
 	 *    each ordered pair of sites in each of the four states: latch j, then i's first decline announces once,
@@ -909,5 +913,6 @@
 	 *    the CPU line counted apart from the timer interrupts (X14); DEVINIT's timer values, without and with a
-	 *    tick pending, at the five legal reads, a Set and a Clear, and the five declines (X14); irq_asserted = 1,
-	 *    raised through the real producer, at the IRQ_STATUS read, the Clear write both ways, and a re-arm row --
-	 *    five declines, the legal reads and a Clear, five declines again, announcing 5 in all (X14).
+	 *    tick pending, at the five legal reads, a Set and a Clear (the drive in both polarities), and the five
+	 *    declines, each with the interrupt output (X14); irq_asserted = 1, raised through the real producer, at the
+	 *    IRQ_STATUS read (value, fields, output), the Clear write both ways, and a re-arm row -- five declines, the
+	 *    legal reads with their values and a Clear, five declines again: 5 announces, one CPU assert (X14).
 	 *  STATES: seeded, all-zero, wide and ONES -- with all-zero, the ones state makes every single-bit condition on
@@ -925,4 +930,6 @@
 	 *  NOT COVERED, stated so a later escape is "outside the contract", not a surprise:
-	 *    a condition on one EXACT field or data value (`d->irq_enable != 0x10`; `idata != 0x20` at the legal Clear
-	 *    write -- both measured green): the bodies compare nothing against a constant, and no practical set of
+	 *    a condition on one EXACT field or data value (`d->fiq_enable != 0x10`; `idata == 0` at a latched Clear write
+	 *    -- measured green, r3c_20260923; `idata != 0x20` and the `irq_enable`/`irq_status != 0x10` forms at +0x180
+	 *    and +0x18c are red since X14, whose rows happen to write 0x20 and hold 0x10 -- by value, not by design): the
+	 *    bodies compare nothing against a constant, and no practical set of
 	 *    seeded states holds every value (a field's domain is finite, 2^32, but not enumerable here);
@@ -931,5 +938,7 @@
 	 *    and a latch outside the rowed cells;
-	 *    the Set writes (IRQ and FIQ) and the FIQ Clear write below len 4 -- arms that share no case with a decline,
-	 *    so outside the floor: a `len == 4` conjunct on their direction tests, or on the write-data fetch with the
-	 *    Clear address exempted, passes every row (measured, closing_20260923/CL.log; filed `fbenablewidth`);
+	 *    the Set writes (IRQ and FIQ) and the FIQ Clear write below len 4, and the enable arms at len 8 -- an
+	 *    LDRD/STRD at +0x188 or +0x288, or at +0x18c/+0x28c aligned down onto them -- including IRQEnable's 8-byte
+	 *    read: arms that share no case with a decline, so outside the floor; a `len == 4` conjunct on their
+	 *    direction tests, or on the write-data fetch with the Clear address exempted, or `len != 8` on the fetch,
+	 *    passes every row (measured, closing_20260923/CL.log; filed `fbenablewidth`);
 	 *    declined-write DATA other than 0 and 0x70 -- wide, 0x55, odd (measured green: q2c_opus N_D02, N_D03, N_D06,
@@ -937,9 +946,16 @@
 	 *    the ADDRESS axis -- a case label added for another offset, or a widened timer fold, aliasing an address onto
-	 *    an arm -- and what an 8-byte access means for the register above the one it lands on (the model answers
-	 *    ONE register per access: an STRD at +0x180 declines IRQ_STATUS once, and its upper word, +0x184's, is no
-	 *    second decline);
+	 *    an arm.  (An 8-byte access answers ONE register: X9/X10 pin an 8-byte READ's upper word to 0, and an STRD at
+	 *    +0x180 is one decline of IRQ_STATUS, not a second of +0x184 -- this line said the upper word was not
+	 *    covered until the Opus seat measured it red, repair 3's pass.);
+	 *    WHICH interrupt a Clear write drives, below len 4: X14 counts the CPU line apart at len 4 only, and X9-X13
+	 *    count calls on the shared pair, so a destination conditioned on the width passes (codex, repair 3's pass);
 	 *    a mask on one of the 25 bits of the drive test no device raises (a guest cannot set them in irq_status);
 	 *    the IRQ Set write's own drive test (the same `if (d->irq_status & d->irq_enable)`, in an arm that shares no
-	 *    case with a decline): X9 rows it only where (irq_status & the new enable) is nonzero or both operands are
-	 *    zero, so `&&` there passes -- X14's operand and single-line cells are the Clear write's;
+	 *    case with a decline): X9 rows it where (irq_status & the new enable) is nonzero, where both operands are
+	 *    zero and where only the enable is set -- never with both nonzero and disjoint, so `&&` there passes;
+	 *    X14's operand and single-line cells are the Clear write's;
+	 *    the PRODUCER PAIR's own logic: X14 calls footbridge_interrupt_assert() only to BUILD its instances, and
+	 *    nothing here calls _deassert() -- deleting the `~` in its `irq_status &= ~interrupt->line` passes all 862
+	 *    rows (codex, repair 3's pass; measured, q2_20260923/r3_20260923/t_deassert.txt).  That pair is
+	 *    `fbirqstuck`'s round;
 	 *    the interrupt output's LEVEL: these rows count calls on stubbed callbacks, so a line left high
@@ -950,5 +966,5 @@
 	 *    N_T08, announce count only), irq_asserted = 1 at the other legal accesses and widths, and a pending tick
-	 *    at the other timers (measured F1:
-	 *    `&& !timer_control[0]` passes every row here; the guest sites probe catches it only because its prologue
-	 *    arms timer 1; table4_20260919).  fiq_status has NO writer in the product, so every FIQ status value these
+	 *    at the other timers.  (F1, `&& !timer_control[0]` on a latch guard, passed every row until X14's DEVINIT
+	 *    rows -- the guest sites probe caught it only because its prologue arms timer 1, table4_20260919; it is red
+	 *    on the 862 rows, r3_20260923.)  fiq_status has NO writer in the product, so every FIQ status value these
 	 *    rows seed is synthetic.
@@ -1316,13 +1332,20 @@
 	 *  interrupt fields seeded, so:
-	 *    the drive test (irq_status & the new enable) was only ever zero with an operand zero, or nonzero with
-	 *    bit 4 or bit 16 in it: never with both operands nonzero and DISJOINT, never with the status zero and the
-	 *    enable not, never with one of the other lines a device raises pending alone (timers 5-7, ISA 10 on cats,
-	 *    11 on netwinder, PCI 18 on cats);
+	 *    no row CHECKED the drive test (irq_status & the new enable) with both operands nonzero and DISJOINT --
+	 *    P8 makes exactly that access and checks only the enable (codex, repair 3's pass) -- nor with the status
+	 *    zero and the enable not, nor with one of the other lines a device raises pending alone (timers 5-7, ISA
+	 *    10 on cats, 11 on netwinder, PCI 18 on cats): where it was checked it was zero with an operand zero, or
+	 *    nonzero with bit 4 or bit 16 in it;
 	 *    the CPU line and the four timer interrupts share one counter pair, so no row could see a Clear write
 	 *    drive the WRONG interrupt;
-	 *    the timer fields sat at 0 where DEVINIT sets PERIODIC, TIMER_MAX_VAL and a bound of 1, and no tick was
-	 *    ever pending;
-	 *    irq_asserted was never 1: its only writer is footbridge_interrupt_assert(), which no block called.
-	 *  Every row here that checks a Clear write's drive also requires the shared pair UNMOVED: the Clear drove the
-	 *  CPU line and no timer interrupt.
+	 *    in the #545 blocks the timer fields sat at 0 where DEVINIT sets PERIODIC, TIMER_MAX_VAL and a bound of 1,
+	 *    and no tick was ever pending (the timer rows at the top of this file seed ticks; they test other arms);
+	 *    irq_asserted was never 1: only the producer pair writes it (assert sets it, deassert clears it), and no
+	 *    block called either.
+	 *  Every row here that checks the interrupt output also requires the shared pair UNMOVED: the CPU line was
+	 *  driven, or left alone, and no timer interrupt was touched.  Repair 3c (this block's own pass -- the Opus seat
+	 *  measured nine edits at cells this header claimed, on channels its rows did not read: a drive at DEVINIT
+	 *  values in either polarity, a decline or the status read driving or clearing while irq_asserted, the reads
+	 *  after the latches set returning 0) gave the DEVINIT reads, Set/Clear and declines, the IRQ_STATUS read and
+	 *  the re-arm row the drive, the fields and the read values they claimed, and added the DEVINIT Clear that
+	 *  keeps a line pending (q2_20260923/q2e_opus/SUMMARY.txt).
 	 *  Width 8 is X6/X7/X9/X10's; +0x184, +0x18c and +0x284 cannot take an 8-byte access.
@@ -1337,2 +1360,5 @@
 			{ FIQ_STATUS, MEM_WRITE }, { FIQ_RAW_STATUS, MEM_WRITE } };
+		static const struct { uint64_t addr; uint32_t want; } RA[5] = {
+			{ IRQ_STATUS, 0x10 }, { IRQ_RAW_STATUS, 0x10 }, { FIQ_STATUS, 0 }, { FIQ_RAW_STATUS, 0 },
+			{ IRQ_ENABLE_SET, 0x10 } };
 		static const char *TS[2] = { "DEVINIT timers", "DEVINIT timers, a tick pending" };
@@ -1387,3 +1413,3 @@
 			snprintf(zn, sizeof(zn), "X14 %s: the five legal reads return their values", TS[tk]);
-			check_u(zn, ok && fatal_calls == 0, 1);
+			check_u(zn, ok && fatal_calls == 0 && ZCPU(0, 0), 1);
 			memory_writemax64(cpu, b, 4, 0x40);
@@ -1393,3 +1419,4 @@
 			snprintf(zn, sizeof(zn), "X14 %s: Set 0x40 then Clear 0x10 leave 0x60", TS[tk]);
-			check_u(zn, ok && rv == 1 && x->irq_enable == 0x60 && fatal_calls == 0, 1);
+			check_u(zn, ok && rv == 1 && x->irq_enable == 0x60 && fatal_calls == 0 && ZCPU(1, 1), 1);
+			ZZERO();
 			ok = 1;
@@ -1398,3 +1425,12 @@
 			check_u(zn, ok && fatal_calls == 5 && x->irq_status == 0x18 && x->irq_enable == 0x60
-			    && x->fiq_status == 0x60 && x->fiq_enable == 0xc0, 1);
+			    && x->fiq_status == 0x60 && x->fiq_enable == 0xc0 && ZCPU(0, 0), 1);
+			free(x);
+			/*  repair 3c: the other polarity of the drive at these values -- a Clear that leaves an enabled line
+			    pending must ASSERT (the row above ends where the drive deasserts)  */
+			x = x14_new(0x18, 0x30, 0x60, 0xc0, 1);
+			x->pending_timer_interrupts[0] = tk;
+			ZZERO();
+			ZCLR(0x20);
+			snprintf(zn, sizeof(zn), "X14 %s: Clear 0x20 keeps 0x10 pending and enabled: CPU line asserted once", TS[tk]);
+			check_u(zn, rv == 1 && x->irq_enable == 0x10 && ZCPU(1, 0) && fatal_calls == 0, 1);
 			free(x);
@@ -1410,3 +1446,4 @@
 		check_u("X14 line 4 raised by a device: IRQ_STATUS reads 0x10",
-		    ok && rv == 1 && memory_readmax64(cpu, b, 4) == 0x10 && fatal_calls == 0, 1);
+		    ok && rv == 1 && memory_readmax64(cpu, b, 4) == 0x10 && fatal_calls == 0 && x->irq_status == 0x10
+		    && x->irq_enable == 0x10 && x->irq_asserted == 1 && ZCPU(0, 0), 1);
 		free(x);
@@ -1431,4 +1468,5 @@
 		for (i = 0; i < 5; i++) {
-			rv = dev_footbridge_access(cpu, NULL, RR[i].addr, b, 4, MEM_READ, x);
-			ok = ok && rv == 1;
+			memset(b, 0xa5, sizeof(b));
+			rv = dev_footbridge_access(cpu, NULL, RA[i].addr, b, 4, MEM_READ, x);
+			ok = ok && rv == 1 && memory_readmax64(cpu, b, 4) == RA[i].want;
 		}
@@ -1438,3 +1476,3 @@
 		check_u("X14 line 4 raised by a device: 5 declines, then the legal reads and a Clear re-arm no latch",
-		    ok && f0 == 5 && fatal_calls == 5, 1);
+		    ok && f0 == 5 && fatal_calls == 5 && ZCPU(1, 0) && x->irq_status == 0x10 && x->irq_enable == 0x10, 1);
 		free(x);
@@ -1450,3 +1488,3 @@
 	    X12 20); the closure's closing pass (repair 3): 707 -> 862 (the 8-byte cells: X6 +32, X7 +8, X9 +8, X10 +8;
-	    X11's other three states +60; X13 20; X14 19).  */
+	    X11's other three states +60; X13 20; X14 19); repair 3's own pass (3c): 862 -> 864 (X14 +2).  */
 	{
@@ -1454,3 +1492,3 @@
 		snprintf(buf, sizeof(buf), "%d", rows + 1);
-		check("IDENTITY row count -- guards against a stale copy", buf, "862");
+		check("IDENTITY row count -- guards against a stale copy", buf, "864");
 	}
```

`regress/gate_offline.sh`, 51d291c3 -> 59149a8b (3 hunks):

```diff
--- _scratchpad/fbd5/q2d/gate_offline.before_r3c.sh	2026-09-23 19:16:47.105820300 -0500
+++ GXEMUL-SEC/regress/gate_offline.sh	2026-09-23 19:16:47.164678700 -0500
@@ -571,5 +571,7 @@
 #  a narrower class (a zero-guard conditioned on the prescaler bits survives D2 and dies in F1).
-#  Detection is unaffected either way: a truncated log fails the row-count, failure-count and verdict
-#  checks below, which read the file's LAST lines (a per-row presence grep can still find a row printed
-#  before the cut -- this said "every grep below fails" until #545's repair 3, which is not so).
+#  Detection is unaffected either way: a log cut anywhere before its LAST line fails the verdict check
+#  below (DIFF_FOOTBRIDGE_PASS is printed last), and one cut before the summary line fails the row-count
+#  and failure-count checks too -- each greps the whole file, so a per-row presence grep can still find a
+#  row printed before the cut.  (This said "every grep below fails on a truncated log" until #545's repair
+#  3, and then that the counts read the file's last lines until repair 3c; neither was so.)
 FBBIN=$LOGDIR/diff_footbridge
@@ -589,3 +591,3 @@
     check_min "footbridge: rows actually run" \
-              "$(grep -oE '^[0-9]+ rows' "$FBLOG" | grep -oE '^[0-9]+')" 862
+              "$(grep -oE '^[0-9]+ rows' "$FBLOG" | grep -oE '^[0-9]+')" 864
     check     "footbridge: offline verdict" "$(grep -c 'DIFF_FOOTBRIDGE_PASS' "$FBLOG")" "1"
@@ -627,3 +629,3 @@
     check "footbridge: #545 X13 legal Clear write, latches SET" "$(fb_distinct 'X13')" "20"
-    check "footbridge: #545 X14 instance cells (drive test, DEVINIT, irq_asserted)" "$(fb_distinct 'X14')" "19"
+    check "footbridge: #545 X14 instance cells (drive test, DEVINIT, irq_asserted)" "$(fb_distinct 'X14')" "21"
     #  Name each row that is the SOLE detector of something.
```

## §F2 — repair 3's pass findings, with MY disposition of each

*(Self-review disclosed: I wrote every repair and disposition.  Seats whose finding I adopted: check the CHANGE answers
it.)*

**R1 -- nine edits at X14's claimed cells, on channels its rows did not read** (the Opus seat, measured: TD01 `&&
!timer_control[0]` and TD03 `|| timer_control[0]` in the Clear drive, TD02/TD12 the same on the pending tick, TD04 a
+0x180 decline that deasserts when `timer_control[0]`, IA12/IA13 the IRQ_STATUS read clearing the status / deasserting
while `irq_asserted`, IA14 a decline deasserting while `irq_asserted`, IA16 a latched-and-asserted read returning 0;
codex (B) and the kimi substitute reached TD01/TD03 by reading).  **ACCEPTED -> rowed (above).  All nine red.**
**R2 -- the producer pair** (every seat: PR01 `|=` -> `=`, PR02 the NetBSD `&& !d->irq_asserted` restored, PR03, PR04 the
`~` deleted, PR07; codex's `^=`; deepseek's `= 0`; minimax's multi-line and repeated assertion).  **DISCLOSED + FILED
(`fbirqstuck`), NOT ROWED** -- see "What 3c changes".  PR02 is the most realistic: it restores code the product keeps
commented out, and the Opus seat's witness shows the cats ISA interrupt never delivered.
**R3 -- width 8 at +0x188/+0x288 (the enable arms) and IRQEnable's 8-byte read; "the two 8-byte-aligned sites" was
false** (grok, glm, codex, the kimi substitute).  **ACCEPTED as records; the cells DISCLOSED** with `fbenablewidth` (the
arms share no case with a decline).  grok's `len != 8` fetch is green, as predicted.
**R4 -- WHICH interrupt a Clear drives below len 4** (codex: `INTERRUPT_ASSERT(*(len < 4 ? &d->timer_irq[0] :
&d->irq))`).  **DISCLOSED** (X14 counts the CPU line apart at len 4; X9-X13 count the shared pair).
**R5 -- a latched Clear of 0 is unobserved; X7 reads no effect** (grok: `!(idata == 0 && d->warned_irq_clear_r)`).
**DISCLOSED** (an exact data value x a latch); COVERED now says X7 observes the return value and announces only.
**R6 -- "the only writer" (irq_status / irq_asserted): `_deassert()` writes both** (codex-dedicated, codex, grok, agy).
**ACCEPTED as records.**
**R7 -- "never with both operands DISJOINT": P8 makes that access and checks only the enable** (codex-dedicated,
codex).  **ACCEPTED as records** -- the gap was observation, not reachability.
**R8 -- the Set drive's operand census was wrong: X9's all-zero Set 0x70 has status 0 and the enable nonzero**
(codex-dedicated, codex, grok).  **ACCEPTED as records.**
**R9 -- F1 (`&& !timer_control[0]`) no longer "passes every row here"**; **the `!= 0x10` exact-value example is red**
(codex-dedicated, codex, grok, glm).  **ACCEPTED as records** (and `idata != 0x20`, above).
**R10 -- "an 8-byte access ... not covered" is backwards: X9/X10 pin an 8-byte read's upper word to 0** (the Opus seat,
measured).  **ACCEPTED as records.**
**R11 -- COVERED misattributed the width-4 / 0x70 Clear to X12/X13, and its channel list overclaimed X7 and X14**
(codex).  **ACCEPTED as records.**
**R12 -- the gate's truncation sentence was still false: the count checks grep the whole file** (codex).  **ACCEPTED.**
**R13 -- "no tick was ever pending" needs a #545-block qualifier: the timer rows seed ticks** (codex).  **ACCEPTED.**
**R14 -- THE SPACE did not name the rest of the instance (timer_value, the CPU interrupt's fields, pcibus,
console_handle, the timer handles)** (agy, codex, the Opus seat).  **ACCEPTED as records**; conditions on them stay
disclosed (the Opus seat's W03-W05: green, named by the NOT COVERED line's opening clause).
**R15 -- "a mask on one of the 25 unraised bits" is covered by the seven single-line rows** (deepseek).  **REJECTED**: a
mask on ONE unraised bit leaves the seven raised lines untouched, so every single-line row stays green; the Opus
seat's 24 such N_SB variants are green on 864 too.
**R16 -- timers 2-4 ticks, other DEVINIT widths/data, multi-line seeds** (minimax, the Opus seat: TD06-TD08, TD13).
**DISCLOSED** (the NOT COVERED line's "a pending tick at the other timers", "beyond X14's cells").
**R17 -- pre-existing false comments in the timer part of the file** (codex-dedicated: "EVERY REAL ROW IN THIS FILE
COMPARES NUMBERS", the `fbclearread` paragraph in the present tense after #474 fixed it, "a DISABLED timer can never
hold a pending interrupt").  **FILED** (pre-existing text; the last also as a product question for the timer campaign).

**D4 -- DO NOT SHIP on repair 3** (six of seven answering panel seats).  Settled by measurement: R1's nine are real.

**WHERE I MIGHT BE FOOLING MYSELF**: R2 is a scope ruling, not a measurement, and I made it; the rule it rests on (the
floor is what dominates the edited lines) is this project's, but "rowing it would start a chain" is a prediction.

## §E -- QUESTIONS (answer each, numbered; if you are answering from this packet alone, do Q1 and Q3 first)

**Q1 -- did 3c close what it claims?**  (a) For each changed or new X14 row, name the edit it is for and the observable
that now differs -- and say whether any X14 row still claims a channel it does not read.  (b) Is every COVERED line
true of the 864 rows, and every NOT COVERED line outside the floor or honestly disclosed?
**Q2 -- the smallest edit to the five arms or the two head tests that the 864 rows cannot see and the contract does not
disclose.**  (The producer pair is disclosed; if you think it should not be, say so under Q3, not here.)  Name it and the
rows you expect to stay green; if none, give your denominator.
**Q3 -- adjudicate R1-R17 and D4**: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each.  Then: **WHICH OF MY
ACCEPTED DISPOSITIONS IS WRONG?**  Above all R2 -- is disclosing the producer pair and filing it with `fbirqstuck` right,
or does #545's detector owe rows for it?  Say which rule decides it.
**Q4 -- records.**  Is any sentence in the changed comments false as of today?  ENUMERATE the IDENTITY arithmetic
(864 = 862 + 2) and the gate pins against the loops.
**Q5 -- option-set completeness**: for R2 and R4, is there a disposition I did not name?

If, while verifying a claim, you found something ELSE -- say so.

End with a seat record: model, what you read, what you ran.
