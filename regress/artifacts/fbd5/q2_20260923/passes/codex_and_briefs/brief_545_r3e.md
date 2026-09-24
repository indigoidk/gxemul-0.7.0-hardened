# #545 (fbdeclinefive) -- repair 3e's own pass: two classes closed in one diff; verify the enumeration, and say whether the chain closes

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  A seat that re-derives a premise from something this brief did NOT give it is worth more
than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/`.**  3e touches `regress/diff_footbridge.c` only; `src/devices/dev_footbridge.c`
and `regress/gate_offline.sh` are unchanged.  File-reading seats: read the FROZEN copies in
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fbd5\q2h\frozen\` (dev_footbridge.c 783c0c7f, diff_footbridge.c 15a1c2a2 = the
instrument under review, diff_footbridge.r3d.c 6c92d7e5 = 3d before this, gate_offline.sh 59149a8b).  There are
pristine-2021-upstream copies of GXemul under the project root (`./src/`, `_archive/`); they are NOT this fork -- line
numbers off by hundreds mean you are reading one of them.

**If you cannot read files that is expected** -- the diff, the key code and the measurements are inlined below.  Name
any premise you cannot settle from this packet rather than guessing.  **ENUMERATE** any count or set rather than
reasoning about it.  **VERDICT LINE FIRST**: `VERDICT: SHIP` or `VERDICT: DO NOT SHIP -- <reason>`.  **A zero needs a
denominator**: say which cells and edit shapes you swept.

## Where #545 stands

#545 turned five host-killing arms of the DC21285 footbridge (`dev_footbridge.c`) into decline + once-latched
announce; its offline detector `regress/diff_footbridge.c` (864 rows) #includes the device and drives the access
function directly.  Repair 3 -> 3c -> **3d** (six X14 rows read what they claim; X12/X13's buffer poisoned above the
width) -> **3d's pass**: `panel_20260923_202025` (codex, grok, glm, kimi-k3:cloud DO NOT SHIP; agy, deepseek, minimax
SHIP; the kimi CLI weekly-walled, covered), a dedicated codex job (FAIL), the Opus measuring seat (DO NOT SHIP on records
only: "no floor breach and no claimed-channel escape in 39 new edits") -> **THIS: repair 3e.**

**THE CLASS-CLOSURE RULE governs this repair and this pass** (the carrier): *when two consecutive passes find breaches of
one class, the next repair owes the class closure -- enumerate the space, close every cell in one diff, write into the
contract which cells are covered and which are not; the closing pass then VERIFIES THE ENUMERATION rather than hunting
cells.*  Two classes met that trigger:
* **(A) a claimed-KEPT channel not read where the claim holds** -- 3c's pass: the Clear 0x20 row named the pending status
  and read it nowhere; 3d's pass (codex): `else if ((d->irq_asserted ^= 1, !d->warned_irq_status_w))` toggles on every
  +0x180 decline, and the re-arm row's two batches cancel it before its end-of-row check.
* **(B) the handler's use of the caller's buffer beyond `len`** -- 3c's pass (deepseek): a fetch of 4 bytes whatever len
  is; 3d's pass (kimi-k3:cloud): a read write-back wider than len -- and a real ARM narrow load passes `data[1]`,
  `data[2]` or `data[4]` (`cpu_arm_instr_loadstore.c:104-126`), so that write-back overflows the caller's buffer.
Two disclosures 3d's pass found one axis short are widened to their classes (the CALLER context; the Clear's
DESTINATION), and one new class is disclosed (STORES to state no row reads after the access).

## What 3e changes (the full diff is inlined below) -- NO ROW ADDED; 864 rows

* **(A)** `ZSNAP()` snapshots the five fields (irq_status, irq_enable, fiq_status, fiq_enable, irq_asserted); `ZKEPT()`
  compares them.  `ZDECLINE()` snapshots at entry and checks after EACH of its five declines; the re-arm row checks
  after each legal read and after its Clear too.  Those are X14's only multi-access rows with a kept claim (the DEVINIT
  declines rows, x2, and the re-arm row); every other X14 row makes one access, so its end IS the access.
* **(B)** `pad_kept(b, w)`: the bytes above the width are still the 0xa5 fill.  Added to X6 (every declined access,
  every width, both directions), X9 and X10 (every legal read, every width).  X11-X13's reads are len-4 declines; the
  class is carried at every width by X6/X9/X10.
* **Records**: COVERED names both checks; NOT COVERED widens the CALLER line to *any caller state* (grok: byte order, pc;
  the Opus seat: ten more, CX01-CX10), the DESTINATION line to *keyed on the width or on a field X14's instances do not
  vary* (codex dedicated: `fiq_enable & 1`), adds the STORE class (the Opus seat: timer state at any legal access,
  SR01-SR11; a latch or the FIQ fields at X14's single-access rows, AS01-AS04, AS08) and FMT01 under the TEXT line;
  E3's reason, the 0xa5 fill's reason (poison, not "a real store's bytes"), FS02's condition, "six named rows at four
  check sites", W02 (not W03); the Opus seats' results copied to durable `q2_20260923/q2{e,f,g}_opus/`.

## Measured (offline; scratch trees restored and `cmp`-verified; PRETABLE and predictions written BEFORE the table)

`regress/artifacts/fbd5/q2_20260923/r3e_20260923/`: `PRETABLE_Q2f.out` 20:53:58, `PREDICTIONS.txt/.tsv` 20:54:00, table
20:54:07 on.  The records addendum after the table changes comments only: the final file (15a1c2a2) prints output
byte-identical to the tabled r3e (467078b4) and its code is identical once comments are stripped.
* **FIX (3e): 864 rows, 0 failures, 0 compiler warnings**; every ok-line of the 3d FIX run printed again: 0 missing, 0 new.
* **748 variants on the 3e instrument -- 0 rows lost, 0 unscored, every prediction held** (one analyzer artefact: WB8
  was deliberately unpredicted, see `PREDICTIONS.corrections.txt`): the 739 of 3d's table with the same kills per set,
  and 9 new, each also run on 3d:

| shape | edit | on 3d (6c92d7e5) | on 3e |
|---|---|---|---|
| R3E_CXT1 | +0x180 latch test: `else if ((d->irq_asserted ^= 1, !d->warned_irq_status_w))` (codex) | GREEN | RED 3: the two DEVINIT declines rows, the re-arm row |
| R3E_WB4 | the tail: `memory_writemax64(cpu, data, len < 4 ? 4 : len, odata)` | GREEN | RED 96: X6's declined read at len 1/2, X9/X10's reads at len 1/2 |
| R3E_WB8 | the tail: `memory_writemax64(cpu, data, 8, odata)` (kimi-k3:cloud) -- unpredicted: it also overflows the harness's own `buf[4]` | GREEN, rc 0 (the overflow was SILENT) | RED 144: every read below width 8 |
| R3E_GLM1 | Clear: `{ d->fiq_status = 0; INTERRUPT_ASSERT(d->irq); }` (glm's premise) | RED 23 | RED 23 |
| R3E_GLM2 | +0x180 decline: `d->irq_enable = 0;` (glm's premise) | RED 149 | RED 149 |
| R3E_CXS2 | end of the Clear: `if (d->irq_asserted && !d->warned_irq_clear_r) d->irq_status = 0;` (codex dedicated) | RED 2 (E3's rows) | RED 2 |
| R3E_BO1 / R3E_PC1 | +0x180 direction test `&& cpu->byte_order != EMUL_LITTLE_ENDIAN` / `&& !cpu->pc` (grok) | GREEN | GREEN -- disclosed |
| R3E_CXD1 | Clear: `{ if (d->fiq_enable & 1) INTERRUPT_ASSERT(d->timer_irq[0]); else INTERRUPT_ASSERT(d->irq); }` | GREEN | GREEN -- disclosed |

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
10. **The chain's stop condition** (the carrier's repair-chain rule, with the class-closure amendment): the chain closes
    on the first VALID pass that finds ZERO floor breaches -- the diff delivered, the roster named, the zero carried
    with its denominator; after a class closure, that pass VERIFIES THE ENUMERATION.


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

## The 3e diff (INLINED IN FULL, three lines of context)

`regress/diff_footbridge.c`, 6c92d7e5 -> 15a1c2a2 (14 hunks):

```diff
--- _scratchpad/fbd5/q2h/frozen/diff_footbridge.r3d.c	2026-09-23 20:15:21.198603400 -0500
+++ _scratchpad/fbd5/q2h/frozen/diff_footbridge.c	2026-09-23 21:01:11.606736900 -0500
@@ -132,6 +132,17 @@
 		}
 	return x;
 }
+/*  #545 3e: the caller's buffer beyond `len` is not the handler's -- a real ARM narrow load passes data[1],
+    data[2] or data[4] (cpu_arm_instr_loadstore.c) -- so every row that fills b with 0xa5 can check that a read or
+    write left the bytes above its width alone (kimi-k3:cloud, 3d's pass: a write-back of 8 bytes passed).  */
+static int pad_kept(const unsigned char *p, int w)
+{
+	int i;
+	for (i = w; i < 8; i++)
+		if (p[i] != 0xa5)
+			return 0;
+	return 1;
+}
 static void x14_line(struct footbridge_data *x, int n)
 {
 	struct interrupt it;
@@ -898,15 +909,16 @@
 	 *  instance (the CPU interrupt's own fields, pcibus, console_handle, the timer handles) -- so the INSTANCE a row
 	 *  runs on is part of the space.
 	 *  COVERED -- the rows named, each observing the channels it names: the return value, the announce count, the
-	 *  four fields, the interrupt calls and, for a read, the read data over the width, except X7 (the return
-	 *  value and the announce count only) and X14's rows (the channels in each row's name and header):
+	 *  four fields, the interrupt calls and, for a read, the read data over the width -- and in X6, X9 and X10
+	 *  the bytes above the width untouched (3e) -- except X7 (the return value and the announce count only) and
+	 *  X14's rows (the channels in each row's name and header):
 	 *    declined x width (the site's domain) x data {0, 0x70} x state x first/repeat (X6);
 	 *    the legal READS of the five readable registers x width -- 1, 2 and 4 at all five, and 8 at IRQ_STATUS
 	 *    and FIQ_STATUS (IRQEnable's 8-byte read is NOT covered, below) -- x state, every latch clear (X9) and
 	 *    every latch set (X10; X7 for the announce channel);
 	 *    the eight enable writes at len 4, data {0, 0x70}, every latch clear (X9) and set (X7);
 	 *    the IRQ Clear write -- the one legal write inside an edited case -- at len 1 and 2 with 0x70 and at len 1,
-	 *    2 and 4 with all-ones data (0xff, 0xffff, 0xffffffff) and the buffer's bytes above the width not zero,
+	 *    2 and 4 with all-ones data (0xff, 0xffff, 0xffffffff) and the buffer's bytes above the width poisoned,
 	 *    every latch clear (X12) and set (X13); at len 4 with
 	 *    0 and 0x70, latches clear (X9), and with 0x70, every latch set (X10);
 	 *    each ordered pair of sites in each of the four states: latch j, then i's first decline announces once,
@@ -914,12 +926,13 @@
 	 *    the drive test's disjoint and status-zero cells, and each of the seven raised lines pending alone, with
 	 *    the CPU line counted apart from the timer interrupts (X14); DEVINIT's timer values, without and with a
 	 *    tick pending, at the five legal reads, a Set and a Clear (the drive in both polarities, and the raw status
-	 *    kept where a Clear leaves a line pending), and the five declines, each with the interrupt output (X14);
+	 *    kept where a Clear leaves a line pending), and the five declines, each with the interrupt output and
+	 *    every field and irq_asserted checked after EACH decline (X14);
 	 *    irq_asserted = 1, raised through the real producer, at the IRQ_STATUS read (the value, the five fields --
 	 *    irq_status, irq_enable, irq_asserted, fiq_status, fiq_enable -- and the output), the Clear write both ways
 	 *    (the enable, the raw status kept, the output), and a re-arm row -- five declines, the legal reads with
-	 *    their values and a Clear, five declines again: 5 announces, one CPU assert, the fields and irq_asserted
-	 *    kept (X14).
+	 *    their values and a Clear, five declines again: 5 announces, one CPU assert, and the fields and
+	 *    irq_asserted kept -- checked after EACH of its access (3e) (X14).
 	 *  STATES: seeded, all-zero, wide and ONES -- with all-zero, the ones state makes every single-bit condition on
 	 *  one field divert in one of the two.
 	 *  *** THIS SAID "the cells above are the whole class" and was measured false THREE times on 2026-09-23: the
@@ -955,8 +968,10 @@
 	 *    an arm.  (An 8-byte access answers ONE register: X9/X10 pin an 8-byte READ's upper word to 0, and an STRD at
 	 *    +0x180 is one decline of IRQ_STATUS, not a second of +0x184 -- this line said the upper word was not
 	 *    covered until the Opus seat measured it red, repair 3's pass.);
-	 *    WHICH interrupt a Clear write drives, below len 4: X14 counts the CPU line apart at len 4 only, and X9-X13
-	 *    count calls on the shared pair, so a destination conditioned on the width passes (codex, repair 3's pass);
+	 *    WHICH interrupt a Clear write drives, outside X14's own instances: X14 counts the CPU line apart only
+	 *    there (len 4; fiq_enable 0 or 0xc0), and X9-X13 count calls on one shared pair, so a destination keyed on
+	 *    the width (codex, repair 3's pass) or on a field X14's instances do not vary (codex, 3d's pass:
+	 *    `fiq_enable & 1`) passes;
 	 *    a mask on one of the 25 bits of the drive test no device raises (a guest cannot set them in irq_status),
 	 *    except bit 16, which the wide state holds: 24 such masks pass, N_SB16 is red on X9, X10, X12 and X13
 	 *    (r3c_20260923);
@@ -970,22 +985,35 @@
 	 *    passes every row (codex, repair 3's pass; t_deassert.txt, r3_20260923, on 862 rows then; PR04, green on
 	 *    864, r3c_20260923).  The pair's bit logic (PR01, PR03, PR04) is filed under `fbirqstuck` by owner ruling
 	 *    (2026-09-23), apart from that item's stuck-high line (F13), with the Opus seat's ready rows;
-	 *    the CALLER context: every row calls the handler with mem NULL on a machine of type MACHINE_NONE, so a
-	 *    condition on `mem` or on the machine type in any test passes every row (the Opus seat, 3c's pass: MC01-
-	 *    MC05 and MC07 green on 864; a cats or netwinder caller with a real mem reddens them in its scratch,
-	 *    q2f/opus/SUMMARY.txt);
-	 *    the announce TEXT: rows count the announces and never read them (TX01);
+	 *    the CALLER context, as a class: every row passes the same calloc'd cpu -- byte order undefined, pc 0, its
+	 *    machine of type MACHINE_NONE -- and mem NULL, so a condition on ANY caller state in any test passes
+	 *    every row (the Opus seat, 3c's pass: `mem` and the machine type, MC01-MC05 and MC07; grok, 3d's pass:
+	 *    `cpu->byte_order != EMUL_LITTLE_ENDIAN`, `!cpu->pc`; a cats or netwinder caller with a real mem
+	 *    reddens the first six in the Opus seat's scratch, q2_20260923/q2f_opus/SUMMARY.txt; the Opus seat, 3d's
+	 *    pass: ten more -- cpu->running, byte_order, is_32bit, ninstrs, machine->ncpus, pc, cpsr, CX01-CX10,
+	 *    q2_20260923/q2g_opus/SUMMARY.txt);
+	 *    the announce TEXT: rows count the announces and never read them (TX01) -- including a conversion added
+	 *    to an announce that passes no argument, undefined behaviour in the real fatal(), whose vsnprintf has no
+	 *    format attribute to warn from (FMT01; the Opus seat, 3d's pass);
+	 *    a STORE to state no row reads after that access: the timer state (pending ticks, the timer registers)
+	 *    at any of the five arms' legal accesses (SR01-SR09, SR11 -- an IRQ_STATUS read that zeroes timer 1's
+	 *    pending ticks is #474's lost-interrupt class), and, at X14's single-access rows, a latch or the FIQ
+	 *    fields those rows do not name (AS01-AS04, AS08; the Opus seat, 3d's pass -- its scratch rows W1-W8 red
+	 *    28 of its 29 greens, q2_20260923/q2g_opus/); X14's multi-access rows check the five fields after every
+	 *    access since 3e;
 	 *    a latch's HISTORY beyond the rowed repeats -- X6's first and repeat, X11's pairs, P1's four declines at
 	 *    one site: a latch that re-arms after more (codex, 3c's pass: `!(d->warned_irq_status_w++ & 3)`, which
 	 *    re-announces at the fifth) passes;
 	 *    the interrupt output's LEVEL: these rows count calls on stubbed callbacks, so a line left high
-	 *    (`fbirqstuck`) is invisible here, and so is a Clear that clears irq_asserted (the Opus seat's FS02);
+	 *    (`fbirqstuck`) is invisible here, and so is a Clear that clears irq_asserted when it leaves nothing pending
+	 *    and enabled (the Opus seat's FS02): only the Clear 0x10 row reaches that state, and it leaves irq_asserted
+	 *    unread on purpose;
 	 *    any other register's semantics; and, beyond X14's cells, a condition in ANY of the arms' tests -- the
 	 *    direction test, a latch test, the write-data fetch, the drive test, a latch clearer -- on a field no branch
 	 *    of the five reads: other timer values (`!d->timer_value[0]`, `d->pending_bound[0] <= 1`: q2c_opus N_T07,
 	 *    N_T08, announce count only), irq_asserted = 1 at the other legal accesses and widths, a pending tick at
 	 *    the other timers, and the rest of the instance (the CPU interrupt's own fields, pcibus, console_handle,
-	 *    the timer handles: W03-W05, green on 864).  (F1, `&& !timer_control[0]` on a latch guard, passed every
+	 *    the timer handles: W02-W05, green on 864).  (F1, `&& !timer_control[0]` on a latch guard, passed every
 	 *    row until X14's DEVINIT
 	 *    rows -- the guest sites probe caught it only because its prologue arms timer 1, table4_20260919; it is red
 	 *    on the 862 rows, r3_20260923, and on the 864, r3c_20260923.)  fiq_status has NO writer in the product,
@@ -1038,7 +1066,7 @@
 							rv = dev_footbridge_access(cpu, NULL, S5[si].addr, b, W[wi], S5[si].wf, x);
 							ok = rv == 1 && fatal_calls - f0 == (ord == 0 ? 1 : 0) && XSAME(x, st)
 							    && irq_asserts == a0 && irq_deasserts == d0
-							    && (S5[si].wf != MEM_READ || memory_readmax64(cpu, b, W[wi]) == 0);
+							    && (S5[si].wf != MEM_READ || memory_readmax64(cpu, b, W[wi]) == 0) && pad_kept(b, W[wi]);
 							snprintf(xn, sizeof(xn), "X6 %s len %d %s %s %s: declined, fields/irq kept, once",
 							    S5[si].nm, W[wi], S5[si].wf == MEM_WRITE ? (dv ? "data 0x70" : "data 0") : "",
 							    ST[st].nm, ord ? "repeat" : "first");
@@ -1158,7 +1186,7 @@
 					want &= w == 8 ? ~0ULL : w == 4 ? 0xffffffffULL : w == 2 ? 0xffffULL : 0xffULL;
 					memset(b, 0xa5, sizeof(b));
 					rv = dev_footbridge_access(cpu, NULL, R5[r].addr, b, w, MEM_READ, x);
-					ok = rv == 1 && fatal_calls == 0 && memory_readmax64(cpu, b, w) == want
+					ok = rv == 1 && fatal_calls == 0 && memory_readmax64(cpu, b, w) == want && pad_kept(b, w)
 					    && x->irq_status == is && x->irq_enable == ie && x->fiq_status == fs
 					    && x->fiq_enable == fe && irq_asserts == a0 && irq_deasserts == d0;
 					snprintf(xn, sizeof(xn), "X9 legal len %d read of %s (%s, latches clear)",
@@ -1204,8 +1232,9 @@
 	         their original names).
 	    X12: a legal IRQ Clear write at len 1 and 2 with 0x70, and at len 1, 2 and 4 with all-ones data, latches clear
 	         (x 4 states): it returns 1, clears (ne = ie & ~idata, idata the low bytes the width carries -- 3d: the
-	         buffer's bytes above the width hold 0xa5, as a real store's are not zero, so a fetch past len clears
-	         more; deepseek's `memory_readmax64(cpu, data, 4)` passed every row while they were 0), drives the
+	         buffer's bytes above the width hold 0xa5 POISON: a real narrow store's buffer is data[1] or data[2]
+	         (cpu_arm_instr_loadstore.c), so bytes past len are not store data at all, and a fetch past len reads
+	         them; deepseek's `memory_readmax64(cpu, data, 4)` passed every row while they were 0), drives the
 	         output once by (irq_status & ne), announces nothing, and the five declines that follow announce exactly 5.
 	    X13 (repair 3): the same five Clear writes with every latch SET: return 1, clear, drive once, announce nothing,
 	         and the five declines that follow still announce nothing.
@@ -1253,7 +1282,8 @@
 					f0 = fatal_calls; a0 = irq_asserts; d0 = irq_deasserts;
 					memset(b, 0xa5, sizeof(b));
 					rv = dev_footbridge_access(cpu, NULL, RY[r].addr, b, WY[w], MEM_READ, x);
-					ok = rv == 1 && fatal_calls == f0 && memory_readmax64(cpu, b, WY[w]) == want && YSAME(st)
+					ok = rv == 1 && fatal_calls == f0 && memory_readmax64(cpu, b, WY[w]) == want && pad_kept(b, WY[w])
+					    && YSAME(st)
 					    && irq_asserts == a0 && irq_deasserts == d0;
 					snprintf(yn, sizeof(yn), "X10 legal len %d read of %s (%s, latches SET) returns its value",
 					    WY[w], RY[r].nm, SY[st].nm);
@@ -1375,11 +1405,15 @@
 	 *  the status read clearing or driving while irq_asserted, the reads after the latches set returning 0) gave
 	 *  the DEVINIT reads, Set/Clear and declines, the IRQ_STATUS read and
 	 *  the re-arm row the drive, the fields and the read values they claimed, and added the DEVINIT Clear that
-	 *  keeps a line pending (q2_20260923/q2e_opus/SUMMARY.txt).  Repair 3d (3c's own pass): five of those checks
-	 *  now read what their names and COVERED claim -- the raw status at the DEVINIT Clear 0x20 (codex, grok, glm:
+	 *  keeps a line pending (q2_20260923/q2e_opus/SUMMARY.txt).  Repair 3d (3c's own pass): six named rows, at four
+	 *  check sites, now read what their names and COVERED claim -- the raw status at the DEVINIT Clear 0x20
+	 *  (codex, grok, glm:
 	 *  a Clear zeroing it there passed) and at the asserted Clears (the Opus seat's FS01), the FIQ fields at the
 	 *  IRQ_STATUS read and the re-arm row (grok: a read setting fiq_enable passed), and irq_asserted at the
-	 *  re-arm row (a decline clearing it passed) -- with no new row (q2_20260923/r3d_20260923).
+	 *  re-arm row (a decline clearing it passed) -- with no new row (q2_20260923/r3d_20260923).  Repair 3e (3d's own
+	 *  pass) checks every field and irq_asserted after EACH access of the multi-access rows (codex: a toggle on
+	 *  each +0x180 decline cancelled across the re-arm row's two batches), again with no new row
+	 *  (q2_20260923/r3e_20260923).
 	 *  Width 8 is X6/X7/X9/X10's; +0x184, +0x18c and +0x284 cannot take an 8-byte access.
 	 */
 	{
@@ -1397,15 +1431,23 @@
 		unsigned char b[8];
 		char zn[200];
 		int i, k, tk, a0, d0, f0, rv, ok;
+		uint32_t zs[5];
 		struct footbridge_data *x;
+/*  3e: a KEPT field is checked after EACH access of a multi-access row, never only at its end -- a toggle on
+    every +0x180 decline cancelled across the re-arm row's two batches and passed (codex, 3d's pass).  */
+#define ZSNAP() do { zs[0] = x->irq_status; zs[1] = x->irq_enable; zs[2] = x->fiq_status; \
+		zs[3] = x->fiq_enable; zs[4] = (uint32_t) x->irq_asserted; } while (0)
+#define ZKEPT() (x->irq_status == zs[0] && x->irq_enable == zs[1] && x->fiq_status == zs[2] \
+		&& x->fiq_enable == zs[3] && (uint32_t) x->irq_asserted == zs[4])
 #define ZZERO() do { cpu_asserts = cpu_deasserts = 0; a0 = irq_asserts; d0 = irq_deasserts; fatal_calls = 0; } while (0)
 #define ZCPU(as, ds) (cpu_asserts == (as) && cpu_deasserts == (ds) && irq_asserts == a0 && irq_deasserts == d0)
 #define ZCLR(v) do { memory_writemax64(cpu, b, 4, (v)); \
 		rv = dev_footbridge_access(cpu, NULL, IRQ_ENABLE_CLEAR, b, 4, MEM_WRITE, x); } while (0)
-#define ZDECLINE() do { for (i = 0; i < 5; i++) { memset(b, 0xa5, sizeof(b)); \
+#define ZDECLINE() do { ZSNAP(); for (i = 0; i < 5; i++) { memset(b, 0xa5, sizeof(b)); \
 		if (DD[i].wf == MEM_WRITE) memory_writemax64(cpu, b, 4, 0x70); \
 		rv = dev_footbridge_access(cpu, NULL, DD[i].addr, b, 4, DD[i].wf, x); \
-		ok = ok && rv == 1 && (DD[i].wf == MEM_WRITE || memory_readmax64(cpu, b, 4) == 0); } } while (0)
+		ok = ok && rv == 1 && (DD[i].wf == MEM_WRITE || memory_readmax64(cpu, b, 4) == 0) && ZKEPT(); } } \
+		while (0)
 		/*  The drive test's operand cells: both nonzero and disjoint (`&&` for `&` asserts there), and the status
 		    zero with the enable not (a test of the enable alone asserts there).  */
 		x = x14_new(0x18, 0x30, 0x60, 0xc0, 0);
@@ -1492,7 +1534,8 @@
 			    k ? "0x400 keeps it" : "0x10 clears it", k ? "asserted" : "deasserted");
 			/*  3d: a Clear writes the enable only -- the raw status is the sources' (the Opus seat's FS01, a Clear
 			    dropping the masked line from it, passed).  irq_asserted is NOT pinned here: the enable arms never
-			    write it, which is `fbirqstuck`'s defect, and a row pinning it would pin that defect.  */
+			    write it, which is `fbirqstuck`'s defect -- so 1 after the DEASSERTING Clear 0x10 would pin that defect.
+			    After the asserting Clear 0x400, 1 is right, and the re-arm row pins exactly that.  */
 			check_u(zn, ok && rv == 1 && x->irq_enable == (k ? 0x10u : 0u) && x->irq_status == 0x10
 			    && (k ? ZCPU(1, 0) : ZCPU(0, 1)) && fatal_calls == 0, 1);
 			free(x);
@@ -1506,16 +1549,18 @@
 		for (i = 0; i < 5; i++) {
 			memset(b, 0xa5, sizeof(b));
 			rv = dev_footbridge_access(cpu, NULL, RA[i].addr, b, 4, MEM_READ, x);
-			ok = ok && rv == 1 && memory_readmax64(cpu, b, 4) == RA[i].want;
+			ok = ok && rv == 1 && memory_readmax64(cpu, b, 4) == RA[i].want && ZKEPT();
 		}
 		ZCLR(0x400);
-		ok = ok && rv == 1;
+		ok = ok && rv == 1 && ZKEPT();     /*  0x10 & ~0x400: nothing changes  */
 		ZDECLINE();
 		check_u("X14 line 4 raised by a device: 5 declines, then the legal reads and a Clear re-arm no latch",
 		    ok && f0 == 5 && fatal_calls == 5 && ZCPU(1, 0) && x->irq_status == 0x10 && x->irq_enable == 0x10
 		    && x->irq_asserted == 1 && x->fiq_status == 0 && x->fiq_enable == 0, 1);
 		free(x);
 #undef ZDECLINE
+#undef ZKEPT
+#undef ZSNAP
 #undef ZCLR
 #undef ZCPU
 #undef ZZERO
@@ -1526,7 +1571,8 @@
 	    state, X9 69); its repair's own pass 2: 491 -> 707 (the ones state: X6 +54, X7 +35, X9 +23; X10 64, X11 20,
 	    X12 20); the closure's closing pass (repair 3): 707 -> 862 (the 8-byte cells: X6 +32, X7 +8, X9 +8, X10 +8;
 	    X11's other three states +60; X13 20; X14 19); repair 3's own pass (3c): 862 -> 864 (X14 +2); 3c's own
-	    pass (3d): 864, no row added -- five X14 checks read more, and X12/X13's buffer bytes above the width.  */
+	    pass (3d): 864, no row added -- six X14 rows read more, and X12/X13's buffer bytes above the width; 3d's own
+	    pass (3e): 864 -- X14's kept fields after each access, and X6/X9/X10's bytes above the width.  */
 	{
 		char buf[32];
 		snprintf(buf, sizeof(buf), "%d", rows + 1);
```

## §F2 — 3d's pass findings, with MY disposition of each (the panel sharing its findings)

**Adjudicate your own findings harder than anyone else's**, and say whether the FIX is right, not only the finding.

* **T1** [codex] the toggle cancels across the re-arm row's two batches: "kept" was read only at the end.  **ACCEPTED as
  class (A)**: every field and irq_asserted after each access of X14's multi-access rows (CXT1: 0 -> 3 rows).
* **T2** [kimi-k3:cloud] the read write-back's width is unobserved, and a real narrow load's buffer is exactly len bytes.
  **ACCEPTED as class (B)**, with the fetch half 3d took: `pad_kept` in X6/X9/X10 (WB4: 0 -> 96; WB8: 0 -> 144).
* **T3** [grok: byte order, pc; the Opus seat: CX01-CX10 -- running, byte_order, is_32bit, ninstrs, machine->ncpus, pc,
  cpsr] the caller disclosure named two fields.  **DISCLOSED AS A CLASS** -- *any caller state*; the Opus seat measured
  that a row only fixes the fields it sets (CX09/CX10 stay green even against its real-caller row), so the class can
  only be closed by disclosure.  BO1/PC1 green on both, measured.
* **T4** [codex dedicated] a destination keyed on `fiq_enable & 1` passes at len 4.  **DISCLOSED AS A CLASS**; CXD1 green.
* **T5** [the Opus seat] stores to state no row reads after the access -- timer state at any legal access (SR01-SR09,
  SR11; SR02 zeroes timer 1's pending ticks on every IRQ_STATUS read -- #474's lost-interrupt class), a latch or the FIQ
  fields at X14's single-access rows (AS01-AS04, AS08).  None is in the DEPENDS-ON floor and none changes a channel a
  row or COVERED claims.  **DISCLOSED**; the Opus seat's scratch rows W1-W8 (872 rows) red 28 of its 29 greens and are
  the ready detector.
* **T6** [the Opus seat, FMT01] the announce text is a FORMAT string: a conversion added to an announce with no argument
  is undefined behaviour in the real `fatal()`.  **DISCLOSED** under the TEXT line.
* **T7** [codex, codex dedicated, the Opus seat] records: the 0xa5 fill's reason; E3's reason (the asserting sibling);
  "five checks" (six rows at four sites); FS02's condition; W02, not W03; the header cited a `q2e_opus` path that did
  not exist and the caller line a scratch path.  **ACCEPTED** -- rewritten, and the three Opus result folders copied to
  `q2_20260923/q2{e,f,g}_opus/` (each SUMMARY ends in its completion sentinel).
* **T8** [glm] premise: do X6 and X9-X13 read the four fields?  **MEASURED: yes** -- GLM1 red 23 and GLM2 red 149, on both
  instruments.
* **T9** [kimi-k3:cloud] premises: `x14_new`'s fifth argument is `devinit` (an int), not irq_asserted, so the r3d table
  is exact; the re-arm reads compare `RA[i].want`.  **Settled from the source.**
* **T10** [codex dedicated] a raw-status zeroing keyed so the re-arm row cannot see it.  **MEASURED**: CXS2 red on E3's two
  rows only -- E3 is not redundant with the re-arm row.
* **T11** [the Opus seat] `gate_offline.sh`'s footbridge "Not covered" summary lists less than the harness's NOT COVERED.
  **FILED** (records; the gate's comment, with `fbgateidentity`).
* **T12** [deepseek] D4: E3/E5 are "inside the floor".  The brief's Q2 SEARCH scope is not the DEPENDS-ON floor.  The Opus
  seat: take both, cite the row-demand rule (zero rows, measured deltas), not the addition licence.  **Kept taken.**

**DISAGREEMENTS -- both sides, in their own words:**
* **DD1** codex: *"S4 is incomplete if its acceptance means that E4 now establishes preservation throughout the
  sequence."*  I had accepted S4.  **Settled by CXT1** (green on 3d) and closed as class (A).
* **DD2** grok: *"The chain stays open on the caller bullet, which is one axis short."*  The Opus seat: *"the caller-context
  class can only be closed by disclosing it as a class."*  **Closed by the class sentence.**
* **DD3 (mine, open): is (A)'s enumeration complete?**  I claim X14's multi-access rows with a kept claim are exactly the
  DEVINIT declines rows and the re-arm row.  The DEVINIT Set/Clear row (two accesses) claims the enable and the drive,
  not kept fields; the DEVINIT reads row claims values.  Check that claim against the rows.

## §E -- QUESTIONS (answer each, numbered; if you are answering from this packet alone, do Q1 and Q3 first)

**Q1 -- VERIFY THE ENUMERATION (the closing pass's job).**  (a) Class (A): list every X14 row that makes more than one
access, what it claims kept, and whether 3e checks that claim after every access -- is any kept claim still read only at
an endpoint?  (b) Class (B): list every row that passes the device a narrow buffer, and whether a fetch past len or a
write-back past len is now observed there -- which arms and widths are covered, which are carried by another row?
(c) Is every COVERED line true of the 864 rows, and every NOT COVERED line outside the floor or honestly disclosed?
**Q2 -- THE FLOOR QUESTION, on the composite**: the smallest edit to the five arms, the two head tests, the Clear write
in the +0x18c case, or the common tail, that the 864 rows cannot see and the contract does not disclose.  **If none,
give your denominator** -- a bare zero does not close the chain.
**Q3 -- adjudicate T1-T12 and DD1-DD3**: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each.  Then: **WHICH OF MY
ACCEPTED DISPOSITIONS IS WRONG?**
**Q4 -- records.**  Is any sentence in 3e's changed comments false as of today?  `ls` every artifact the changed
comments cite.
**Q5 -- closing.**  Is this pass VALID to close the chain (diff delivered, roster, your denominator)?  If you would not
close it, name the one measurement that would let you.

If, while verifying a claim, you found something ELSE -- say so.

End with a seat record: model, what you read, what you ran.
