# #545 (fbdeclinefive) -- repair 3d's own pass: does the 864-row detector now read every channel it claims, and does the chain close?

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  A seat that re-derives a premise from something this brief did NOT give it is worth more
than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`.**  3d touches `regress/diff_footbridge.c` only; `src/devices/dev_footbridge.c`
and `regress/gate_offline.sh` are unchanged.  File-reading seats: read the FROZEN copies in
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2g\frozen\` (dev_footbridge.c 783c0c7f, diff_footbridge.c 6c92d7e5 = the
instrument under review, diff_footbridge.864r3c.c 8309c5b7 = 3c before this, gate_offline.sh 59149a8b).  There are
pristine-2021-upstream copies of GXemul under the project root (`./src/`, `_archive/`); they are NOT this fork -- line
numbers off by hundreds mean you are reading one of them.

**If you cannot read files that is expected** -- the diff, the key code and the measurements are inlined below.  Name
any premise you cannot settle from this packet rather than guessing.  **ENUMERATE** any count or set rather than
reasoning about it.  **VERDICT LINE FIRST**: `VERDICT: SHIP` or `VERDICT: DO NOT SHIP -- <reason>`.  **A zero needs a
denominator**: say which cells and edit shapes you swept.

## Where #545 stands

#545 turned five host-killing arms of the DC21285 footbridge (`dev_footbridge.c`) into decline + once-latched
announce.  Its offline detector `regress/diff_footbridge.c` #includes the device and drives the access function
directly (rows counted by name; the gate pins the counts).  Repair 3 (862 rows) -> its pass -> **3c (864: nine X14
cells the Opus seat measured open, two rows added)** -> **3c's pass**: `panel_20260923_192724` (codex, grok and glm DO
NOT SHIP; agy, deepseek, minimax and kimi-k3:cloud SHIP; the kimi CLI walled on its weekly limit, covered by
kimi-k3:cloud), a dedicated codex job (FAIL), and the Opus measuring seat (DO NOT SHIP: 8 edits green on 864, 7 of
them closable by scratch rows).  **Four seats independently: the new "Clear 0x20 keeps 0x10 pending" row names the
pending status and never reads it.**  -> **THIS: repair 3d.**

**The chain rule this pass is judged by** (the carrier's repair-chain rule): one pass per floor-bound diff; the chain
closes on the first VALID pass that finds ZERO floor breaches -- the diff delivered, the roster named, and the zero
carried with its denominator.  Review EFFORT is scoped to 3d's diff; the FLOOR QUESTION (a clean-sweep mutant in the
DEPENDS-ON enumeration, or a claimed cell a measured edit passes) is asked of the SHIPPED COMPOSITE.

## What 3d changes (the full diff is inlined below) -- NO ROW ADDED; 864 rows, X14's 21 names

* **E1** the DEVINIT "Clear 0x20 keeps 0x10 pending and enabled" rows (both timer states) now read `irq_status == 0x18`
  -- the raw status a Clear must not touch.
* **E2** the line-4 "IRQ_STATUS reads 0x10" row now reads the FIQ fields too (`fiq_status == 0 && fiq_enable == 0`),
  so its COVERED claim "(value, fields, output)" names all five fields it reads.
* **E3** both asserted-Clear rows ("line 4 raised by a device: Clear 0x10 clears it / Clear 0x400 keeps it") now read
  the raw status (`irq_status == 0x10`) and are RENAMED "..., the raw status kept, ...".  `irq_asserted` is left
  UNPINNED there on purpose: the enable arms never write it (`fbirqstuck`'s F13 defect), so pinning 1 after a
  deasserting Clear pins the defect and pinning 0 is false of today's code.
* **E4** the re-arm row now reads `irq_asserted == 1` and the FIQ fields at its end.
* **E5** X12 and X13 fill the buffer with 0xa5 before each narrow Clear write, so the bytes above the width are not
  zero (a real store's are not): a write-data fetch that reads past `len` now clears more of the enable.
* Records: COVERED (the reads' widths spelled out -- IRQEnable's 8-byte read NOT covered; "for a read, the read data";
  X14's channels), NOT COVERED (the exact-value example rewritten from the Opus seat's measured forms; bit 16 of the
  unraised 25 is caught; the producer pair's text and its filing by owner ruling; NEW: the CALLER context, the announce
  TEXT, a latch's HISTORY; FS02 on the LEVEL line; the rest of the instance), the X14 header, the IDENTITY comment.

## Measured (offline; scratch trees restored and `cmp`-verified; PRETABLE and predictions written BEFORE the table)

`regress/artifacts/fbd5/q2_20260923/r3d_20260923/`: `PRETABLE_Q2e.out` 20:08:10, `PREDICTIONS.txt/.tsv` 20:08:12, table
20:08:18-20:14:47.
* **FIX (3d): 864 rows, 0 failures, 0 compiler warnings**; every ok-line of the 3c FIX run printed again (the two
  renamed rows under their new names): 0 missing, 0 new.
* **739 variants on the 3d instrument -- 0 mismatches against the predictions, 0 rows lost, 0 unscored**: the 3c
  table's 711 (569 red, 5 died, 137 green -- every one as on 864r3c), the Opus seat's 22 q2f shapes (13 red as before;
  **FS01 now red**; MC01-MC05, MC07, TX01, FS02 green, as disclosed), and 6 new:

| shape | edit | on 3c (8309c5b7) | on 3d |
|---|---|---|---|
| R3D_CXC1 | at the end of the Clear write: `if (d->timer_control[0] && (d->irq_status & d->irq_enable)) d->irq_status = 0;` (codex, glm) | GREEN | RED, the two Clear 0x20 rows |
| R3D_GF1 | IRQ_STATUS read: `odata = ..., d->fiq_enable |= (uint32_t) d->irq_asserted;` (grok) | GREEN | RED, the status-read and re-arm rows |
| R3D_DA1 | +0x180 decline: `d->irq_asserted = 0;` after the latch | GREEN | RED, the re-arm row |
| OQ_FS01 | Clear: `d->irq_status &= d->irq_asserted ? d->irq_enable : ~0u` (the Opus seat) | GREEN | RED, the Clear 0x10 row |
| R3D_CXA1 | control: the same as CXC1 keyed on `irq_asserted` | RED, the re-arm row | RED, + the Clear 0x400 row |
| R3D_FW1 | the head fetch: `memory_readmax64(cpu, data, 4)` (deepseek) | GREEN | RED, 16 rows: X12/X13's four narrow Clears x {wide, ones} |
| R3D_LH1 | +0x180 latch: `!(d->warned_irq_status_w++ & 3)` (codex dedicated; re-announces at the 5th) | GREEN | GREEN -- disclosed |

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
8. **The producer pair is DISCLOSED and FILED, not rowed** -- owner ruling 2026-09-23 (under `fbirqstuck`, MED).
9. **The fork's `fatal()` returns**; the detector stubs it and counts calls.


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

## The 3d diff (INLINED IN FULL, three lines of context)

`regress/diff_footbridge.c`, 8309c5b7 -> 6c92d7e5 (12 hunks):

```diff
--- _scratchpad/fbd5/q2g/frozen/diff_footbridge.864r3c.c	2026-09-23 19:25:50.611135400 -0500
+++ _scratchpad/fbd5/q2g/frozen/diff_footbridge.c	2026-09-23 20:15:21.198603400 -0500
@@ -898,23 +898,28 @@
 	 *  instance (the CPU interrupt's own fields, pcibus, console_handle, the timer handles) -- so the INSTANCE a row
 	 *  runs on is part of the space.
 	 *  COVERED -- the rows named, each observing the channels it names: the return value, the announce count, the
-	 *  four fields, the interrupt calls and the read data over the width, except X7 (the return value and the
-	 *  announce count only) and X14's rows (the channels in each row's name and header):
+	 *  four fields, the interrupt calls and, for a read, the read data over the width, except X7 (the return
+	 *  value and the announce count only) and X14's rows (the channels in each row's name and header):
 	 *    declined x width (the site's domain) x data {0, 0x70} x state x first/repeat (X6);
-	 *    the legal READS of the five readable registers x width (the site's domain) x state, every latch clear (X9)
-	 *    and every latch set (X10; X7 for the announce channel);
+	 *    the legal READS of the five readable registers x width -- 1, 2 and 4 at all five, and 8 at IRQ_STATUS
+	 *    and FIQ_STATUS (IRQEnable's 8-byte read is NOT covered, below) -- x state, every latch clear (X9) and
+	 *    every latch set (X10; X7 for the announce channel);
 	 *    the eight enable writes at len 4, data {0, 0x70}, every latch clear (X9) and set (X7);
 	 *    the IRQ Clear write -- the one legal write inside an edited case -- at len 1 and 2 with 0x70 and at len 1,
-	 *    2 and 4 with all-ones data (0xff, 0xffff, 0xffffffff), every latch clear (X12) and set (X13); at len 4 with
+	 *    2 and 4 with all-ones data (0xff, 0xffff, 0xffffffff) and the buffer's bytes above the width not zero,
+	 *    every latch clear (X12) and set (X13); at len 4 with
 	 *    0 and 0x70, latches clear (X9), and with 0x70, every latch set (X10);
 	 *    each ordered pair of sites in each of the four states: latch j, then i's first decline announces once,
 	 *    returns 1, reads 0 if it is the declined read, and BOTH stay latched (X11);
 	 *    the drive test's disjoint and status-zero cells, and each of the seven raised lines pending alone, with
 	 *    the CPU line counted apart from the timer interrupts (X14); DEVINIT's timer values, without and with a
-	 *    tick pending, at the five legal reads, a Set and a Clear (the drive in both polarities), and the five
-	 *    declines, each with the interrupt output (X14); irq_asserted = 1, raised through the real producer, at the
-	 *    IRQ_STATUS read (value, fields, output), the Clear write both ways, and a re-arm row -- five declines, the
-	 *    legal reads with their values and a Clear, five declines again: 5 announces, one CPU assert (X14).
+	 *    tick pending, at the five legal reads, a Set and a Clear (the drive in both polarities, and the raw status
+	 *    kept where a Clear leaves a line pending), and the five declines, each with the interrupt output (X14);
+	 *    irq_asserted = 1, raised through the real producer, at the IRQ_STATUS read (the value, the five fields --
+	 *    irq_status, irq_enable, irq_asserted, fiq_status, fiq_enable -- and the output), the Clear write both ways
+	 *    (the enable, the raw status kept, the output), and a re-arm row -- five declines, the legal reads with
+	 *    their values and a Clear, five declines again: 5 announces, one CPU assert, the fields and irq_asserted
+	 *    kept (X14).
 	 *  STATES: seeded, all-zero, wide and ONES -- with all-zero, the ones state makes every single-bit condition on
 	 *  one field divert in one of the two.
 	 *  *** THIS SAID "the cells above are the whole class" and was measured false THREE times on 2026-09-23: the
@@ -929,10 +934,13 @@
 	 *  repair 3, X6-X14. ***
 	 *  NOT COVERED, stated so a later escape is "outside the contract", not a surprise:
 	 *    a condition on one EXACT field or data value (`d->fiq_enable != 0x10`; `idata == 0` at a latched Clear write
-	 *    -- measured green, r3c_20260923; `idata != 0x20` and the `irq_enable`/`irq_status != 0x10` forms at +0x180
-	 *    and +0x18c are red since X14, whose rows happen to write 0x20 and hold 0x10 -- by value, not by design): the
-	 *    bodies compare nothing against a constant, and no practical set of
-	 *    seeded states holds every value (a field's domain is finite, 2^32, but not enumerable here);
+	 *    -- measured green, r3c_20260923): the bodies compare nothing against a constant, and no practical set of
+	 *    seeded states holds every value (a field's domain is finite, 2^32, but not enumerable here).  Some such
+	 *    forms are red only because a row happens to hold the value, not because a row was written to pin it: the
+	 *    `irq_enable`/`irq_status != 0x10` forms at the direction tests of +0x180, +0x184 (since 3c) and +0x18c
+	 *    and at all five latch tests (X14 holds 0x10), and `idata != 0x20` at +0x18c since 3c's Clear 0x20 row;
+	 *    the same forms at +0x280/+0x284's direction tests, and every `fiq_*` form, are green (the Opus seat,
+	 *    3c's pass);
 	 *    JOINT conditions beyond the rowed combinations: two fields beyond the four states; latch vectors other
 	 *    than none, all, the site's own and the X11 pairs (a first decline after two OTHER sites latched); a width
 	 *    and a latch outside the rowed cells;
@@ -949,24 +957,39 @@
 	 *    covered until the Opus seat measured it red, repair 3's pass.);
 	 *    WHICH interrupt a Clear write drives, below len 4: X14 counts the CPU line apart at len 4 only, and X9-X13
 	 *    count calls on the shared pair, so a destination conditioned on the width passes (codex, repair 3's pass);
-	 *    a mask on one of the 25 bits of the drive test no device raises (a guest cannot set them in irq_status);
+	 *    a mask on one of the 25 bits of the drive test no device raises (a guest cannot set them in irq_status),
+	 *    except bit 16, which the wide state holds: 24 such masks pass, N_SB16 is red on X9, X10, X12 and X13
+	 *    (r3c_20260923);
 	 *    the IRQ Set write's own drive test (the same `if (d->irq_status & d->irq_enable)`, in an arm that shares no
 	 *    case with a decline): X9 rows it where (irq_status & the new enable) is nonzero, where both operands are
 	 *    zero and where only the enable is set -- never with both nonzero and disjoint, so `&&` there passes;
 	 *    X14's operand and single-line cells are the Clear write's;
-	 *    the PRODUCER PAIR's own logic: X14 calls footbridge_interrupt_assert() only to BUILD its instances, and
-	 *    nothing here calls _deassert() -- deleting the `~` in its `irq_status &= ~interrupt->line` passes all 862
-	 *    rows (codex, repair 3's pass; measured, q2_20260923/r3_20260923/t_deassert.txt).  That pair is
-	 *    `fbirqstuck`'s round;
+	 *    the PRODUCER PAIR's own logic: X14 calls footbridge_interrupt_assert() to build its line-4 instances and
+	 *    checks only that one raise from an empty status (irq_status 0x10, irq_asserted 1, one CPU assert -- PR09
+	 *    reds it), and nothing here calls _deassert(): deleting the `~` in its `irq_status &= ~interrupt->line`
+	 *    passes every row (codex, repair 3's pass; t_deassert.txt, r3_20260923, on 862 rows then; PR04, green on
+	 *    864, r3c_20260923).  The pair's bit logic (PR01, PR03, PR04) is filed under `fbirqstuck` by owner ruling
+	 *    (2026-09-23), apart from that item's stuck-high line (F13), with the Opus seat's ready rows;
+	 *    the CALLER context: every row calls the handler with mem NULL on a machine of type MACHINE_NONE, so a
+	 *    condition on `mem` or on the machine type in any test passes every row (the Opus seat, 3c's pass: MC01-
+	 *    MC05 and MC07 green on 864; a cats or netwinder caller with a real mem reddens them in its scratch,
+	 *    q2f/opus/SUMMARY.txt);
+	 *    the announce TEXT: rows count the announces and never read them (TX01);
+	 *    a latch's HISTORY beyond the rowed repeats -- X6's first and repeat, X11's pairs, P1's four declines at
+	 *    one site: a latch that re-arms after more (codex, 3c's pass: `!(d->warned_irq_status_w++ & 3)`, which
+	 *    re-announces at the fifth) passes;
 	 *    the interrupt output's LEVEL: these rows count calls on stubbed callbacks, so a line left high
-	 *    (`fbirqstuck`) is invisible here;
+	 *    (`fbirqstuck`) is invisible here, and so is a Clear that clears irq_asserted (the Opus seat's FS02);
 	 *    any other register's semantics; and, beyond X14's cells, a condition in ANY of the arms' tests -- the
 	 *    direction test, a latch test, the write-data fetch, the drive test, a latch clearer -- on a field no branch
 	 *    of the five reads: other timer values (`!d->timer_value[0]`, `d->pending_bound[0] <= 1`: q2c_opus N_T07,
-	 *    N_T08, announce count only), irq_asserted = 1 at the other legal accesses and widths, and a pending tick
-	 *    at the other timers.  (F1, `&& !timer_control[0]` on a latch guard, passed every row until X14's DEVINIT
+	 *    N_T08, announce count only), irq_asserted = 1 at the other legal accesses and widths, a pending tick at
+	 *    the other timers, and the rest of the instance (the CPU interrupt's own fields, pcibus, console_handle,
+	 *    the timer handles: W03-W05, green on 864).  (F1, `&& !timer_control[0]` on a latch guard, passed every
+	 *    row until X14's DEVINIT
 	 *    rows -- the guest sites probe caught it only because its prologue arms timer 1, table4_20260919; it is red
-	 *    on the 862 rows, r3_20260923.)  fiq_status has NO writer in the product, so every FIQ status value these
+	 *    on the 862 rows, r3_20260923, and on the 864, r3c_20260923.)  fiq_status has NO writer in the product,
+	 *    so every FIQ status value these
 	 *    rows seed is synthetic.
 	 */
 	{
@@ -1180,7 +1203,9 @@
 	         then re-declining j and i announces NOTHING -- both latches kept (20 pairs x 4 states; the seeded rows keep
 	         their original names).
 	    X12: a legal IRQ Clear write at len 1 and 2 with 0x70, and at len 1, 2 and 4 with all-ones data, latches clear
-	         (x 4 states): it returns 1, clears (ne = ie & ~idata, idata the low bytes the width carries), drives the
+	         (x 4 states): it returns 1, clears (ne = ie & ~idata, idata the low bytes the width carries -- 3d: the
+	         buffer's bytes above the width hold 0xa5, as a real store's are not zero, so a fetch past len clears
+	         more; deepseek's `memory_readmax64(cpu, data, 4)` passed every row while they were 0), drives the
 	         output once by (irq_status & ne), announces nothing, and the five declines that follow announce exactly 5.
 	    X13 (repair 3): the same five Clear writes with every latch SET: return 1, clear, drive once, announce nothing,
 	         and the five declines that follow still announce nothing.
@@ -1288,6 +1313,7 @@
 				uint32_t is = SY[st].is, ne = SY[st].ie & ~(uint32_t) (CY[c].data & mask);
 				YNEW(st);
 				fatal_calls = 0; a0 = irq_asserts; d0 = irq_deasserts;
+				memset(b, 0xa5, sizeof(b));      /*  3d: the bytes above the width are NOT zero  */
 				memory_writemax64(cpu, b, CY[c].w, CY[c].data);
 				rv = dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, CY[c].w, MEM_WRITE, x);
 				ok = rv == 1 && fatal_calls == 0 && x->irq_enable == ne && x->irq_status == is
@@ -1308,6 +1334,7 @@
 				YNEW(st);
 				YDECLINE_ALL();
 				f0 = fatal_calls; a0 = irq_asserts; d0 = irq_deasserts;
+				memset(b, 0xa5, sizeof(b));      /*  3d: the bytes above the width are NOT zero  */
 				memory_writemax64(cpu, b, CY[c].w, CY[c].data);
 				rv = dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, CY[c].w, MEM_WRITE, x);
 				ok = rv == 1 && fatal_calls == f0 && x->irq_enable == ne && x->irq_status == is
@@ -1343,11 +1370,16 @@
 	 *    block called either.
 	 *  Every row here that checks the interrupt output also requires the shared pair UNMOVED: the CPU line was
 	 *  driven, or left alone, and no timer interrupt was touched.  Repair 3c (this block's own pass -- the Opus seat
-	 *  measured nine edits at cells this header claimed, on channels its rows did not read: a drive at DEVINIT
-	 *  values in either polarity, a decline or the status read driving or clearing while irq_asserted, the reads
-	 *  after the latches set returning 0) gave the DEVINIT reads, Set/Clear and declines, the IRQ_STATUS read and
+	 *  measured nine edits at cells this header claimed, on channels its rows did not read: a Clear's drive at
+	 *  DEVINIT values in either polarity, a decline driving at those values (TD04) or while irq_asserted (IA14),
+	 *  the status read clearing or driving while irq_asserted, the reads after the latches set returning 0) gave
+	 *  the DEVINIT reads, Set/Clear and declines, the IRQ_STATUS read and
 	 *  the re-arm row the drive, the fields and the read values they claimed, and added the DEVINIT Clear that
-	 *  keeps a line pending (q2_20260923/q2e_opus/SUMMARY.txt).
+	 *  keeps a line pending (q2_20260923/q2e_opus/SUMMARY.txt).  Repair 3d (3c's own pass): five of those checks
+	 *  now read what their names and COVERED claim -- the raw status at the DEVINIT Clear 0x20 (codex, grok, glm:
+	 *  a Clear zeroing it there passed) and at the asserted Clears (the Opus seat's FS01), the FIQ fields at the
+	 *  IRQ_STATUS read and the re-arm row (grok: a read setting fiq_enable passed), and irq_asserted at the
+	 *  re-arm row (a decline clearing it passed) -- with no new row (q2_20260923/r3d_20260923).
 	 *  Width 8 is X6/X7/X9/X10's; +0x184, +0x18c and +0x284 cannot take an 8-byte access.
 	 */
 	{
@@ -1426,13 +1458,15 @@
 			    && x->fiq_status == 0x60 && x->fiq_enable == 0xc0 && ZCPU(0, 0), 1);
 			free(x);
 			/*  repair 3c: the other polarity of the drive at these values -- a Clear that leaves an enabled line
-			    pending must ASSERT (the row above ends where the drive deasserts)  */
+			    pending must ASSERT (the row above ends where the drive deasserts); 3d: and the raw status stays
+			    0x18, as the name says (codex, grok, glm: a Clear that zeroed it here passed every row)  */
 			x = x14_new(0x18, 0x30, 0x60, 0xc0, 1);
 			x->pending_timer_interrupts[0] = tk;
 			ZZERO();
 			ZCLR(0x20);
 			snprintf(zn, sizeof(zn), "X14 %s: Clear 0x20 keeps 0x10 pending and enabled: CPU line asserted once", TS[tk]);
-			check_u(zn, rv == 1 && x->irq_enable == 0x10 && ZCPU(1, 0) && fatal_calls == 0, 1);
+			check_u(zn, rv == 1 && x->irq_enable == 0x10 && x->irq_status == 0x18 && ZCPU(1, 0) && fatal_calls == 0,
+			    1);
 			free(x);
 		}
 		/*  irq_asserted = 1, through the real callback: a device raises line 4 with line 4 enabled.  */
@@ -1445,7 +1479,8 @@
 		rv = dev_footbridge_access(cpu, NULL, IRQ_STATUS, b, 4, MEM_READ, x);
 		check_u("X14 line 4 raised by a device: IRQ_STATUS reads 0x10",
 		    ok && rv == 1 && memory_readmax64(cpu, b, 4) == 0x10 && fatal_calls == 0 && x->irq_status == 0x10
-		    && x->irq_enable == 0x10 && x->irq_asserted == 1 && ZCPU(0, 0), 1);
+		    && x->irq_enable == 0x10 && x->irq_asserted == 1 && x->fiq_status == 0 && x->fiq_enable == 0
+		    && ZCPU(0, 0), 1);
 		free(x);
 		for (k = 0; k < 2; k++) {
 			x = x14_new(0, 0x10, 0, 0, 0);
@@ -1453,10 +1488,13 @@
 			ok = x->irq_asserted == 1;
 			ZZERO();
 			ZCLR(k ? 0x400 : 0x10);
-			snprintf(zn, sizeof(zn), "X14 line 4 raised by a device: Clear %s, CPU line %s once",
+			snprintf(zn, sizeof(zn), "X14 line 4 raised by a device: Clear %s, the raw status kept, CPU line %s once",
 			    k ? "0x400 keeps it" : "0x10 clears it", k ? "asserted" : "deasserted");
-			check_u(zn, ok && rv == 1 && x->irq_enable == (k ? 0x10u : 0u) && (k ? ZCPU(1, 0) : ZCPU(0, 1))
-			    && fatal_calls == 0, 1);
+			/*  3d: a Clear writes the enable only -- the raw status is the sources' (the Opus seat's FS01, a Clear
+			    dropping the masked line from it, passed).  irq_asserted is NOT pinned here: the enable arms never
+			    write it, which is `fbirqstuck`'s defect, and a row pinning it would pin that defect.  */
+			check_u(zn, ok && rv == 1 && x->irq_enable == (k ? 0x10u : 0u) && x->irq_status == 0x10
+			    && (k ? ZCPU(1, 0) : ZCPU(0, 1)) && fatal_calls == 0, 1);
 			free(x);
 		}
 		x = x14_new(0, 0x10, 0, 0, 0);
@@ -1474,7 +1512,8 @@
 		ok = ok && rv == 1;
 		ZDECLINE();
 		check_u("X14 line 4 raised by a device: 5 declines, then the legal reads and a Clear re-arm no latch",
-		    ok && f0 == 5 && fatal_calls == 5 && ZCPU(1, 0) && x->irq_status == 0x10 && x->irq_enable == 0x10, 1);
+		    ok && f0 == 5 && fatal_calls == 5 && ZCPU(1, 0) && x->irq_status == 0x10 && x->irq_enable == 0x10
+		    && x->irq_asserted == 1 && x->fiq_status == 0 && x->fiq_enable == 0, 1);
 		free(x);
 #undef ZDECLINE
 #undef ZCLR
@@ -1486,7 +1525,8 @@
 	    then 78 P-rows + 222 X-rows); the adjudication pass, 2026-09-23: 333 -> 491 (X6 +54 and X7 +35 for the wide
 	    state, X9 69); its repair's own pass 2: 491 -> 707 (the ones state: X6 +54, X7 +35, X9 +23; X10 64, X11 20,
 	    X12 20); the closure's closing pass (repair 3): 707 -> 862 (the 8-byte cells: X6 +32, X7 +8, X9 +8, X10 +8;
-	    X11's other three states +60; X13 20; X14 19); repair 3's own pass (3c): 862 -> 864 (X14 +2).  */
+	    X11's other three states +60; X13 20; X14 19); repair 3's own pass (3c): 862 -> 864 (X14 +2); 3c's own
+	    pass (3d): 864, no row added -- five X14 checks read more, and X12/X13's buffer bytes above the width.  */
 	{
 		char buf[32];
 		snprintf(buf, sizeof(buf), "%d", rows + 1);
```

## §F2 — 3c's pass findings, with MY disposition of each (the panel sharing its findings)

Every seat answered blind to the others.  Here is each finding, who raised it, and what I did.  **Adjudicate your own
findings harder than anyone else's**, and say whether the FIX is right, not only whether the finding was.

* **S1** [codex, grok, glm, codex-dedicated; the Opus seat's FS01 is its asserted twin] the Clear 0x20 row names the
  pending status and never reads it; a Clear zeroing it at DEVINIT values passed 864.  **ACCEPTED -> E1** (CXC1 green
  -> red x2).
* **S2** [grok; glm secondary; codex-dedicated for the re-arm row] the IRQ_STATUS read row claims "(value, fields,
  output)" and never read the FIQ fields.  **ACCEPTED -> E2 + E4** (GF1 green -> red x2).
* **S3** [the Opus seat, FS01] a Clear dropping the masked line from the RAW status while irq_asserted -- guest-visible
  in 4 steps -- passed; the asserted-Clear rows named only the enable and the CPU line.  **ACCEPTED -> E3**, zero rows
  (FS01 green -> red x1).  `irq_asserted` deliberately unpinned there (E3's reason).
* **S4** [agy; codex-dedicated] the re-arm row's final check omitted `irq_asserted` (and the FIQ fields).  **ACCEPTED ->
  E4** (a decline clearing irq_asserted, DA1: green -> red x1).
* **S5** [deepseek] a fetch of 4 bytes whatever `len` is passed: every narrow write left the bytes above its width 0.
  **ACCEPTED -> E5** (FW1 green -> red x16).  The fetch is NOT an edited line, so this is above the floor; I took it
  because the fill costs no row and the delta is measured (the addition licence).  **A seat may say that is wrong.**
* **S6** [the Opus seat, MC01-MC05, MC07] every row calls the handler with mem NULL on a machine of type MACHINE_NONE,
  so a condition on `mem` or on the machine type passes.  **DISCLOSED, clause (e)**: no body of the five reads `mem` or
  the machine type (the joint-cells rule: a selector that touches nothing the guarded body reads is (e)).  Filed with
  the Opus seat's scratch rows (a cats and a netwinder caller with a real mem: 871 rows, 8 of its 9 greens red) as the
  ready detector.  Measured green on 3d, 6 of 6.
* **S7** [the Opus seat TX01; kimi-k3:cloud] the announce TEXT is unread.  **DISCLOSED.**
* **S8** [codex-dedicated] a latch that re-arms after four repeats passes (no instance declines one site five times).
  **DISCLOSED, clause (e)**: the latch test partitions {0, nonzero}, and both are rowed.  LH1 green on both, measured.
* **S9** [the Opus seat FS02] a Clear clearing irq_asserted passes.  **DISCLOSED** on the LEVEL line.
* **S10** [grok, the Opus seat] records: "X14 calls ... only to BUILD its instances" was false (PR09 reds the
  status-read row); "That pair is fbirqstuck's round" conflated F13's stuck-high line with the pair's bit logic
  (PR01/PR03/PR04); "passes all 862 rows" and F1's "red on the 862 rows" were stale.  **ACCEPTED -> rewritten.**
* **S11** [codex, the Opus seat] COVERED's reads line claimed IRQEnable x width 8 while NOT COVERED named it.
  **ACCEPTED** -> widths spelled out.
* **S12** [the Opus seat, codex] the exact-value example undercounted (the irq_* `!= 0x10` forms are red at +0x184
  since 3c and at all five latch tests; every fiq_* form is green) and `idata != 0x20` is red since 3c, not since X14;
  [minimax] "by value, not by design" was ambiguous.  **ACCEPTED** -> rewritten from the measured forms.
* **S13** [codex] bit 16 of the 25 unraised bits IS caught (N_SB16 reds ten rows: one each in X9/X10, four each in
  X12/X13); 24 masks pass.  **ACCEPTED.**
* **S14** [grok] NOT COVERED's field list omitted the rest of the instance THE SPACE names.  **ACCEPTED.**
* **S15** [glm] the X14 header's recap of the nine did not name TD04 (a decline driving at DEVINIT values, NOT
  asserted).  **ACCEPTED.**
* **S16** [kimi-k3:cloud] COVERED's "the read data over the width" read as a channel of the write rows.  **ACCEPTED** ->
  "for a read".
* **S17** [codex-dedicated] three PRE-EXISTING false comments (fbclearread's `case TIMER_1_CLEAR` sentence, "EVERY
  REAL ROW IN THIS FILE COMPARES NUMBERS", the DISABLED-timer sentence also in gate_offline.sh).  **FILED with R17**
  (pre-existing, the timer campaign's), not edited here.
* **S18** [R4 options: codex, grok, agy, minimax, kimi-k3:cloud, the Opus seat] a one-row len-1 Clear on X14's split
  counters, or re-wiring X9-X13's `d->irq` to X14's CPU counter pair (zero rows), would close the destination gap.
  **KEPT DISCLOSED** (the Clear write's body is not an edited line); both options go into the filing.
* **S19** [R2 options: kimi-k3:cloud, minimax, codex, grok, agy, the Opus seat] a bounded producer block.  **OWNER
  RULING 2026-09-23: disclose + file under `fbirqstuck`** (MED); the options and the Opus seat's ready rows go there,
  with the pair's bit logic named apart from F13 (grok).
* **S20** [glm] does the fork's `fatal()` exit?  It does not: `debugmsg.c`'s `fatal()` returns (it has no exit at all;
  the carrier records this).  No change.
* **S21** [kimi-k3:cloud] the family pins sum to 831, not 864: the other 33 are the 32 timer rows and IDENTITY
  (codex and grok enumerated 864).  No change.
* **S22** [agy, Q2] `(len & 1) == 0` on the Clear direction test: len 1 is odd, so X12's len-1 rows red it; the
  `len == 3` variant is not a guest input.  Not an escape.

**DISAGREEMENTS -- both sides, in their own words:**
* **D1** kimi-k3:cloud: *"'keeps 0x10 pending' is observed via the drive, exactly."*  codex, grok, glm: *"The drive
  proves bit 4 was live at drive time, not that the field retains it afterwards."*  **Settled by measurement**: CXC1
  zeroes the status AFTER the drive and passed all 864 rows on 3c.
* **D2** agy: *"No X14 row claims a channel it does not read."*  codex, grok, glm: the Clear 0x20 row and the status-read
  row do.  **Settled by CXC1 and GF1.**
* **D3** kimi-k3:cloud: *"disclosure + file is right iff fbirqstuck is a real, owned round."*  The other seats upheld
  R2 on the DEPENDS-ON function-boundary rule.  `fbirqstuck` is an open MED item and the owner ruled.
* **D4 (mine, open): E3 and E5 are rows/fills ABOVE the floor** -- the Clear write's body and the head fetch are not
  edited lines.  I took both because each costs no row and each has a measured delta.  The alternative is to disclose
  them, as S6/S8 are disclosed.  Which is right, and does taking them change what the CONTRACT claims (COVERED now
  names the raw status at the asserted Clears)?

## §E -- QUESTIONS (answer each, numbered; if you are answering from this packet alone, do Q1 and Q3 first)

**Q1 -- did 3d close what it claims?**  (a) For each strengthened check (E1-E4) and the fill (E5), name the edit it is
for and the observable that now differs -- and say whether ANY row still claims a channel it does not read.  (b) Is
every COVERED line true of the 864 rows, and every NOT COVERED line outside the floor or honestly disclosed?
**Q2 -- THE FLOOR QUESTION, on the composite**: the smallest edit to the five arms, the two head tests, or the Clear
write inside the edited case, that the 864 rows cannot see and the contract does not disclose.  Name it and the rows you
expect to stay green; **if none, give your denominator** -- a bare zero does not close the chain.
**Q3 -- adjudicate S1-S22 and D1-D4**: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each.  Then: **WHICH OF MY
ACCEPTED DISPOSITIONS IS WRONG?**  Above all D4 and S6 (caller context disclosed rather than rowed).
**Q4 -- records.**  Is any sentence in the changed comments false as of today?  Check the two renamed row names against
their checks, and the IDENTITY comment's history.
**Q5 -- closing.**  Is this pass VALID to close the chain if it finds zero breaches (diff delivered, roster, your
denominator)?  If you would not close, name the one measurement that would let you.

If, while verifying a claim, you found something ELSE -- say so.

End with a seat record: model, what you read, what you ran.
