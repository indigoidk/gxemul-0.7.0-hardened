# T19 / `i8259eoiirr` (#574, MED, WRONG-RESULT) -- PASS 1: the DESIGN BRIEF, before any edit

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated
wrongly.  **Check the premises, not just the derivations.**  Where I state something as
fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream
copies of GXemul under the project root (`./src/` and two under
`_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers
disagree with mine by hundreds you are reading one of them — say so rather than
reconciling.

**If you cannot read files that is expected** — every fact you need is inlined.  Name any
premise you cannot settle from this packet rather than guessing at it.

**Where this brief states an ARITHMETIC claim — an index range, an offset, a count of
reachable addresses — ENUMERATE it rather than reasoning about it.**  Walk the values.
A derivation that skips one masking line reads exactly like a correct one.

**And ENUMERATE THE RIGHT DOMAIN — a domain is itself a premise.**  Ask what the PRODUCER of
these values can actually emit before you walk them.  Walking every member of a set you have
not audited is not enumeration; it is a derivation with more steps, and it reads exactly like
a correct one.

**VERDICT LINE FIRST**, so your answer survives truncation.

**Language and scope.**  This is ordinary correctness engineering on an emulator's interrupt-controller
model: a register write has the wrong side effect on another register.  Scope your reading to
`GXEMUL-SEC/src/` and `GXEMUL-SEC/regress/*.py`; do not read `regress/artifacts/` or `tools/pipeline/ledger.json`.
Do not propose a mutant, a witness program, or "the smallest edit that re-opens this": where a design question
needs a construction, this brief SUPPLIES the candidates and asks which are equivalent and what each changes.
Cite by grep anchor or construct name, not by line number (the citation-form rule).

## 1. The defect, in one paragraph

`src/devices/dev_8259.c`, `DEVICE_ACCESS(8259)`, the OCW2 write arm at offset 0: a SPECIFIC End-Of-Interrupt
(`0x60 | n`, also `0x21-0x27` and `0xe0-0xe7`) executes `d->irr &= ~(1 << (idata & 7)); d->isr &= ~(1 << (idata & 7));`
and recomputes the CPU line from `irr & ~ier`.  In this model the IRR IS the interrupt line's level:
`src/devices/bus_isa.c`'s `isa_interrupt_assert()` sets `pic->irr |= 1 << line` and `isa_interrupt_deassert()` clears
it, and no acknowledge cycle exists.  So an EOI drops the request of a line the device still holds asserted; the
device, believing it is already asserted, does not call deassert-then-assert, and the request stays dropped until
the device's next tick re-asserts it (ns16550, wdc, 8253, ne2000) or until its next event (one-shot sources: pckbc,
mc146818).  The non-specific EOI (`0x20`) does `d->irr &= ~d->isr; d->isr = 0;` and is INERT on the IRR today
because nothing in the model ever sets ISR (the sibling row `i8259isrnever`).  On the Intel 8259A an EOI resets an
IN-SERVICE bit only; the request bit is cleared by the acknowledge (edge mode) or follows the line (level mode).

## 2. SETTLED PREMISES -- first brief of this campaign; every item below is a READING or a MEASUREMENT made today
## (2026-10-25) with its warrant.  Nothing is carried from another round.

### 2.1 Has this round already shipped?  (§C0, run and pasted)

    git log -1 -- src/devices/dev_8259.c   -> 39748e3c 2026-06-28 Import GXemul 0.7.0 (unmodified upstream baseline)
    git log -1 -- src/devices/bus_isa.c    -> 39748e3c 2026-06-28 Import GXemul 0.7.0 (unmodified upstream baseline)
    grep -c i8259eoiirr CHANGELOG.md       -> 0          (OUTSTANDING_BUGS.md: 1, the filing)
    ls regress/ | grep -iE '8259|pic'      -> nothing: no 8259 probe or gate block exists

Neither file has been touched by any round of this fork.  The round has NOT run.

### 2.2 The model, inlined (HEAD 94b247db; `src/devices/dev_8259.c`, the whole access function -- §D: edits are
### proposed below, so the enclosing function is shown entire, every exit path included)

```c
DEVICE_ACCESS(8259)
{
	struct pic8259_data *d = (struct pic8259_data *) extra;
	uint64_t idata = 0, odata = 0;
	int i;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

#ifdef DEV_8259_DEBUG
	... (debug prints)
#endif

	switch (relative_addr) {
	case 0x00:
		if (writeflag == MEM_WRITE) {
			if ((idata & 0x10) == 0x10) {
				/*  Bit 3: 0=edge, 1=level  */
				if (idata & 0x08)
					fatal("[ 8259: TODO: Level "
					    "triggered (MCA bus) ]\n");
				if (idata & 0x04)
					fatal("[ 8259: WARNING: Bit 2 set ]\n");
				/*  Bit 1: 0=cascade, 1=single  */
				/*  Bit 0: 1=4th init byte  */
				/*  This happens on non-x86 systems:
				    if (!(idata & 0x01))
					fatal("[ 8259: WARNING: Bit 0 NOT set!"
					    "!! ]\n");  */
				d->init_state = 1;
				break;
			}

			/*  TODO: Is it ok to abort init state when there
			    is a non-init command?  */
			if (d->init_state)
				fatal("[ 8259: WARNING: Was in init-state, but"
				    " it was aborted? ]\n");
			d->init_state = 0;

			if (idata == 0x0a) {
				d->current_command = 0x0a;
			} else if (idata == 0x0b) {
				d->current_command = 0x0b;
			} else if (idata == 0x0c) {
				/*  Put Master in Buffered Mode  */
				d->current_command = 0x0c;
			} else if (idata == 0x20) {
				int old_irr = d->irr;
				/*  End Of Interrupt  */
				/*  TODO: in buffered mode, is this an EOI 0? */
				d->irr &= ~d->isr;
				d->isr = 0;
				/*  Recalculate interrupt assertions,
				    if necessary:  */
				if ((old_irr & ~d->ier) != (d->irr & ~d->ier)) {
					if (d->irr & ~d->ier)
						INTERRUPT_ASSERT(d->irq);
					else
						INTERRUPT_DEASSERT(d->irq);
				}
			} else if ((idata >= 0x21 && idata <= 0x27) ||
			    (idata >= 0x60 && idata <= 0x67) ||
			    (idata >= 0xe0 && idata <= 0xe7)) {
				/*  Specific EOI  */
				int old_irr = d->irr;
				d->irr &= ~(1 << (idata & 7));
				d->isr &= ~(1 << (idata & 7));
				/*  Recalc. int assertions, if necessary:  */
				if ((old_irr & ~d->ier) != (d->irr & ~d->ier)) {
					if (d->irr & ~d->ier)
						INTERRUPT_ASSERT(d->irq);
					else
						INTERRUPT_DEASSERT(d->irq);
				}
			} else if (idata == 0x68) {
				/*  Set Special Mask Mode  */
				/*  TODO  */
			} else if (idata >= 0xc0 && idata <= 0xc7) {
				/*  Set IRQ Priority Order  */
				/*  TODO  */
			} else {
				fatal("[ 8259: unimplemented command 0x%02x"
				    " ]\n", (int)idata);
				cpu->running = 0;
			}
		} else {
			switch (d->current_command) {
			case 0x0a:
				odata = d->irr;
				break;
			case 0x0b:
				odata = d->isr;
				break;
			case 0x0c:
				/*  Buffered mode.  */
				odata = 0x00;
				for (i=0; i<8; i++)
					if ((d->irr >> i) & 1) {
						odata = 0x80 | i;
						break;
					}
				break;
			default:
				odata = 0x00;
				for (i=0; i<8; i++)
					if ((d->irr >> i) & 1) {
						odata = 0x80 | i;
						break;
					}
				break;
			/* (a TODO comment: the default label "should really" stop the cpu, "but Linux seems to read from
			    the secondary PIC in a manner which works better the way things are coded right now") */
			}
		}
		break;
	case 0x01:
		if (d->init_state > 0) {
			if (d->init_state == 1) {
				d->irq_base = idata & 0xf8;
				d->init_state = 2;
			} else if (d->init_state == 2) {
				/*  Slave attachment. TODO  */
				d->init_state = 3;
			} else if (d->init_state == 3) {
				if (idata & 0x02)
					debug("[ 8259: WARNING! Bit 1 i" "n Init Cmd 4 is set! ]\n");
				if (!(idata & 0x01))
					fatal("[ 8259: WARNING! Bit 0 " "in Init Cmd 4 is not" " set! ]\n");
				d->init_state = 0;
			}
			break;
		}

		if (writeflag == MEM_WRITE) {
			int old_ier = d->ier;
			d->ier = idata;

			/*  Recalculate interrupt assertions,
			    if necessary:  */
			if ((d->irr & ~old_ier) != (d->irr & ~d->ier)) {
				if (d->irr & ~d->ier)
					INTERRUPT_ASSERT(d->irq);
				else
					INTERRUPT_DEASSERT(d->irq);
			}
		} else {
			odata = d->ier;
		}
		break;
	default:
		if (writeflag == MEM_WRITE) {
			fatal("[ 8259: unimplemented write to address 0x%x" " data=0x%02x ]\n", (int)relative_addr, (int)idata);
			cpu->running = 0;
		} else {
			fatal("[ 8259: unimplemented read from address 0x%x " "]\n", (int)relative_addr);
			cpu->running = 0;
		}
	}

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}
```

(Condensed only inside the `#ifdef DEV_8259_DEBUG` block and three wrapped `fatal`/`debug` strings; every statement that
touches `irr`, `isr`, `ier`, `init_state`, `current_command` or the CPU line is verbatim.)  The struct: `irr`, `isr`,
`ier` (the mask), `irq_base`, `init_state`, `current_command`, and `irq` -- the interrupt object the PIC asserts.
`DEVINIT(8259)` connects `d->irq` to the path in the device string, names a device at `addr & 0xfff == 0xa0`
`[secondary]` with `irq_base = 8`, and registers one byte-wide window of `DEV_8259_LENGTH` with `DM_DEFAULT`.

### 2.3 How a line reaches the PIC (`src/devices/bus_isa.c`, verbatim; every ISA machine)

```c
void isa_interrupt_common(struct bus_isa_data *d, int old_isa_assert)
{
	int new_isa_assert, x;
	/*  Any interrupt assertions on PIC2 go to irq 2 on PIC1  */
	/*  (TODO: don't hardcode this here)  */
	if (d->pic2->irr & ~d->pic2->ier)
		d->pic1->irr |= 0x04;
	else
		d->pic1->irr &= ~0x04;
	new_isa_assert = d->pic1->irr & ~d->pic1->ier;
	if (old_isa_assert == new_isa_assert)
		return;
	if (!new_isa_assert) {
		INTERRUPT_DEASSERT(d->irq);
		return;
	}
	for (x=0; x<16; x++) {
		if (x == 2)
			continue;
		if (x < 8 && (d->pic1->irr & ~d->pic1->ier & (1 << x)))
			break;
		if (x >= 8 && (d->pic2->irr & ~d->pic2->ier & (1 << (x&7))))
			break;
	}
	*d->ptr_to_last_int = x;
	INTERRUPT_ASSERT(d->irq);
}

void isa_interrupt_assert(struct interrupt *interrupt)
{
	struct bus_isa_data *d = (struct bus_isa_data *) interrupt->extra;
	int old_isa_assert, line = interrupt->line;
	int mask = 1 << (line & 7);
	old_isa_assert = d->pic1->irr & ~d->pic1->ier;
	if (line < 8)
		d->pic1->irr |= mask;
	else if (d->pic2 != NULL)
		d->pic2->irr |= mask;
	isa_interrupt_common(d, old_isa_assert);
}

void isa_interrupt_deassert(struct interrupt *interrupt)
{
	struct bus_isa_data *d = (struct bus_isa_data *) interrupt->extra;
	int line = interrupt->line, mask = 1 << (line & 7);
	int old_irr1 = d->pic1->irr, old_isa_assert;
	old_isa_assert = old_irr1 & ~d->pic1->ier;
	if (line < 8)
		d->pic1->irr &= ~mask;
	else if (d->pic2 != NULL)
		d->pic2->irr &= ~mask;
	/*  If IRQ 0 has been cleared, then this is a timer interrupt.
	    Let's ack it here:  */
	if (old_irr1 & 1 && !(d->pic1->irr & 1) &&
	    d->ptr_to_pending_timer_interrupts != NULL &&
            (*d->ptr_to_pending_timer_interrupts) > 0)
                (*d->ptr_to_pending_timer_interrupts) --;
	isa_interrupt_common(d, old_isa_assert);
}
```

`bus_isa_init()` registers the sixteen ISA interrupt objects with these two handlers, then adds `8259 irq=<base>`
at `portbase + 0x20` (pic1, whose `d->irq` is the CPU line the bus was given) and `8259 irq=<base>.isa.2` at
`+0xa0` (pic2, whose `d->irq` is ISA line 2 of pic1 through the same handlers), then `8253 ... in_use=0` at `+0x40`,
`pccmos` (the mc146818) at `+0x70` on line 8, and `ns16550 irq=<base>.isa.4` at `+0x3f8`.  Note the TWO roads to the
CPU line: the ISA handlers' `INTERRUPT_ASSERT(d->irq)` on the BUS object, and the PIC's own `INTERRUPT_ASSERT(d->irq)`
inside the EOI / mask arms -- for pic1 both name the same CPU line; for pic2 the PIC's own call re-enters the ISA
handlers as line 2.

**Who instantiates this** (grep `bus_isa_init(` across `src/`): `machine_evbmips.c` (malta, `0x18000000`),
`machine_cobalt.c`, `machine_iyonix.c`, `machine_algor.c` (with `BUS_ISA_EXTERNAL_PIC`, so bus_isa registers no
handlers there), `bus_pci.c` (two PCI-ISA bridges), `dev_eagle.c` (PReP), `dev_lca.c` (the Alpha AXPpci33),
`dev_prep.c`.  The malta rig boots NetBSD and Linux through this pair.

**TWO MORE ROADS TO A PIC's IRR, found by grepping `->irr` across `src/` (READ today; a premise I first stated
too narrowly):** `src/devices/dev_v3.c` (the Iyonix's V3 bridge) registers its own two `8259` devices and carries a
VERBATIM COPY of the three handlers above (`d->pic1->irr |= mask`, `&= ~mask`, the cascade fold into bit 2, the
IRQ-0 pending-count decrement) -- so any change that assumes `bus_isa.c` is the only line-state writer must be read
against `dev_v3.c` too; and `src/devices/dev_algor.c` reads `isa_pic_data.pic1->irr & ~ier & 0x10 / 0x08` for its own
interrupt-status register and CLEARS `pic1->irr &= ~0x18` (and `pic2->irr &= ~0xc0`) on its own write path -- an
EOI-shaped request clear outside the PIC, on a machine whose bus has no ISA handlers.  Neither file sets a PIC's
`isr`; `grep -rn 'isr |=' src/` hits only `dev_ne2000.c` and `dev_i80321.c`, which are those devices' own registers.

### 2.4 The ISA sources' assert/deassert habits (READ today; the device files named)

| source | asserts | deasserts | shape |
|---|---|---|---|
| `dev_ns16550.c` (`DEVICE_TICK`, every 2^14 instructions) | when `(ier & ETXRDY && iir & TXRDY) or (ier & ERXRDY && iir & RXRDY)` and `mcr & MCR_IENABLE` | when neither, if `int_asserted` | LEVEL, re-asserted on every tick |
| `dev_wdc.c` (`DEVICE_TICK`) | `if (d->int_assert) INTERRUPT_ASSERT` | on a STATUS read (`int_assert = 0`) | LEVEL, re-asserted on every tick |
| `dev_8253.c` (`DEVICE_TICK`) | `if (d->pending_interrupts_timer0 > 0) INTERRUPT_ASSERT` -- the host-timer callback increments the count; `in_use` is 0 at init and becomes 1 on the first guest access | NEVER (no `INTERRUPT_DEASSERT` in the file) | one-way; `bus_isa.c` decrements the pending count only inside `isa_interrupt_deassert`, which the 8253 never calls |
| `dev_ne2000.c` (`DEVICE_TICK`) | `if (new_assert) INTERRUPT_ASSERT` -- "Assert unconditionally while the level is high.  The Jazz ISA bridge's 8259-style EOI writes (dev_jazz.c) clear the latched ISA line state, so a transition-gated assert would leave a still-pending level dropped until the next 0->1 edge -- wedging RX under bursts" | `else if (d->irq_asserted) INTERRUPT_DEASSERT` | LEVEL, re-asserted on every tick -- the fork's own earlier handling of THIS class, done on the device side for the arc/Jazz bridge |
| `dev_pckbc.c` | `if (!d->currently_asserted[port]) INTERRUPT_ASSERT` when the queue is non-empty and enabled | when the queue drains | ONE-SHOT: transition-gated, no re-assert while the condition holds |
| `dev_mc146818.c` (`DEVICE_TICK`) | the periodic/alarm event | on a register-C read, or PIE cleared | one event per period |

### 2.5 The witness -- MEASURED today, rung 3 (banked at `regress/artifacts/i8259eoiirr/witness_20261025/`,
### RUN_IDENTITY.txt; RESULTS_base.txt; the probe copy `i8259_eoi_probe.frozen.py.txt`, md5 226fc359, 526 lines)

Unmodified `evbmips -e malta` (little-endian), a fresh git-archive clone of HEAD 94b247db built in WSL (binary md5
6d1e627a; `dev_8259.c` md5 dbbb0e90 with the specific-EOI `irr &= ~(1 << (idata & 7))` present once), the cold
debugger loading three guest programs (141 words, every word verified against the emulator's own disassembler; each
session parked at its halt breakpoint with the pc verified).  ISA I/O at KSEG1 `0xb8000000 + port`; the level source is
the ISA ns16550: `sb 0x08 -> 0x3fc` (MCR_IENABLE), `sb 0x02 -> 0x3f9` (IER_ETXRDY), then a 12000-iteration counted loop
(more than two UART ticks).  Reads are `sb OCW3 -> 0x20; lbu <- 0x20`.

```
  row            got      head     fix     
  ram:quiet      0x5a     want 0x5a     ok
  ram:level      0x5a     want 0x5a     ok
  ram:other      0x5a     want 0x5a     ok
  quiet irr4     0x00     want 0x00     ok      (no source enabled: IRR 0x00, ISR 0x00, poll byte 0x00, IMR 0x00, PIC2 IRR 0x00)
  quiet isr      0x00     want 0x00     ok
  quiet poll     0x00     want 0x00     ok
  level irr4     0x01     want 0x01     ok      (raw IRR 0x10 with the UART level on)
  level isr      0x00     want 0x00     ok      (ISR stays 0 -- the sibling defect)
  eoi irr4       0x00     head 0x00   fix 0x01   [HEAD] ok    <- specific EOI 0x64, IRR read two instructions later: bit 4 CLEARED
  eoi x8         0x00     head 0x00   fix 0xff   [HEAD] ok    <- the EOI+read pair repeated eight times: cleared every time
  eoi isr        0x00     want 0x00     ok
  other irr4     0x01     want 0x01     ok
  nonspec irr4   0x01     want 0x01     ok      (non-specific EOI 0x20 leaves IRR: inert because ISR is empty)
  masked irr4    0x01     want 0x01     ok      (OCW1 0x10 masks line 4; IRR unchanged -- the mask does not touch IRR)
  masked imr     0x10     want 0x10     ok
  poll byte      0x84     want 0x84     ok      (OCW3 0x0c read: 0x80 | 4)
  stable:quiet   0x00     want 0x00     ok
  stable:level   0x10     want 0x10     ok
  stable:other   0x10     want 0x10     ok
  19/19 passed   CONTROL=PASS   I8259EOI_RESULT_base=19/19  I8259EOI_CONTROL_base=OK
```

The two SYMPTOM rows' FIX column (`eoi irr4` 1, `eoi x8` 0xff) is the DESIGN SKETCH -- EOI leaves the request bit of a
still-asserted line -- and is what this brief asks you to confirm or re-pin.  The `eoi x8` row's timing premise: the
read is two instructions after the EOI store and the UART tick period is 2^14 instructions, so a tick re-asserting the
line inside that window is a ~2e-4 event per repetition (disclosed; eight repetitions, all cleared).

### 2.6 The datasheet (Intel 8259A, `C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/i8259/8259A.txt`, pdftotext of the
### datasheet fetched today; absolute path so a file-reading seat does not browse for it)

* IRR/ISR (:166-173): "The IRR is used to store all the interrupt levels which are requesting service and the ISR is
  used to store all the interrupt levels which are being serviced."
* The interrupt sequence (:223-256): at the acknowledge "the highest priority ISR bit is set and the corresponding
  IRR bit is reset ... Otherwise the ISR bit remains set until an appropriate EOI command is issued at the end of
  the interrupt sequence" (AEOI: reset at the end of the acknowledge).
* OCW2 (:491-566): the EOI commands reset an ISR bit -- "a non-specific EOI ... the 8259A will automatically reset
  the highest priority ISR bit"; "A specific EOI can be issued with OCW2 ... the ISR bit to be reset".  Nothing in
  OCW2 touches the IRR.
* Trigger modes (:415, :666-672): LTIM=1 level -- recognised by a high level on an IR input; LTIM=0 edge --
  recognised by a low-to-high transition and "the IRR bit set until the acknowledge".
* The poll command (:596-612): the read following P=1 acknowledges the highest request and "sets the appropriate IS bit".

### 2.7 How the guests drive it (READ today from the kernel sources on GitHub, named per line)

* Linux `drivers/irqchip/irq-i8259.c` (master): `mask_and_ack_8259A()` masks the line then writes
  `outb(0x60+irq, PIC_MASTER_CMD); /* 'Specific EOI to master */` (slave: `0x60+(irq&7)` to the slave, then
  `0x60+PIC_CASCADE_IR` to the master); the spurious check reads the ISR (`outb(0x0B, PIC_MASTER_CMD); value =
  inb(PIC_MASTER_CMD)`); ICW1 is `0x11`; the lines are `handle_level_irq`.  The malta port obtains the vector with the
  poll command (OCW3 0x0C) in `i8259_irq()` -- the function body was not in the fetched file; a file-reading seat with
  web access may confirm it, a packet-fed seat should treat the poll claim as a premise to flag.
* NetBSD `sys/arch/evbmips/malta/malta_intr.c` delegates the ISA controller to `pcib_ic` / `isa_intr_establish()`;
  its EOI form was NOT established today (NOT CHECKABLE from the packet; a question below).
* The rs6000/PReP fork this row was filed from (three commits, READ via their patches today):
  `ae2240b` ("Checkpoint here: going to add proper support for pci IO space") comments out both IRR clears in the EOI
  arms -- `// EOI shouldn't change irr` -- adds `dev_8259_recalc_interrupts()`, `dev_8259_assert()/deassert()`
  (`irr |= / &= ~(1 << line)` then recalc), chains pic2 to pic1 line 2, and routes `bus_isa.c`'s handlers through
  them; `598ab10` ("New pic impl") sets ISR inside the recalc when the highest unmasked IRR bit is not yet in service,
  overwrites ISR from IRR on a poll read and clears the acknowledged bit, makes the init sequence honour SNGL/IC4,
  drops the level-trigger `fatal`, and rewrites OCW2 (rotation etc.); `174448c` ("Add interrupt identification early")
  decodes the PReP IACK vector from `last_int`.  None of the three cites a datasheet; whether that fork also changed
  `dev_8253.c` to deassert was NOT checked.

### 2.8 The fork's own precedent for this class

`src/devices/dev_jazz.c` (the arc/Jazz ISA bridge) keeps a latched `isa_int_asserted` mask that its register writes
clear (`isa_int_asserted &= 0xff` / `&= 0xff00`); the `dev_ne2000.c` comment quoted in 2.4 records that a transition-
gated device assert "would leave a still-pending level dropped until the next 0->1 edge -- wedging RX under bursts",
and the fork fixed it on the DEVICE side by re-asserting on every tick.  That is the same class as this row seen from
the device, and it is why most ISA sources here are tick re-asserters.

## 3. The design question, with the candidates SUPPLIED (do not invent an edit; say what each does)

The floor for this round's detector will be the probe above, extended; the fix must keep `isa_interrupt_*` and
every tick re-asserter working, and must not make a never-deasserting source (the 8253 once `in_use`) a permanent
level.  Candidates:

* **(A) EOI clears ISR only.**  Delete the two IRR clears (`d->irr &= ~d->isr;` and `d->irr &= ~(1 << (idata & 7));`),
  keep the ISR clears and the recalculation of the CPU line (which becomes a no-op on IRR but not on ISR -- today the
  CPU line is `irr & ~ier`, so after (A) an EOI never deasserts the CPU line; the DEVICE's deassert does).  This is
  the rs6000 fork's `ae2240b`.  Consequence to check: a source that never deasserts (the 8253 with `in_use` set and
  a pending count that nothing decrements) keeps the CPU line asserted after its handler returns -- today the specific
  EOI is the only thing that drops it (for one tick).  Which machines/guests program the 8253 at all is a question.
* **(B) = (A) + an acknowledge that sets ISR**: the poll read (`current_command 0x0c`, today `0x80 | lowest irr bit`)
  sets `isr |= bit` (the datasheet's "sets the appropriate IS bit"), the EOI clears it, and the CPU line becomes
  `irr & ~ier & ~isr`-driven so an in-service level does not re-interrupt until EOI.  This is `598ab10`'s shape
  (which sets ISR at selection time instead of at the poll) and the rows `i8259isrnever` + `i8259eoiirr` together.
  Consequence to check: guests that never poll (they read the vector from a machine register -- PReP IACK, the
  Jazz vector, `*ptr_to_last_int` readers) would never get ISR set, so for them (B) degrades to (A).
* **(C) = (A) + edge emulation for one-way sources**: the ISA layer treats a line whose device never deasserts as a
  PULSE -- `isa_interrupt_assert` for the 8253's line sets IRR and the EOI (or the acknowledge) clears it, i.e. keep
  the IRR clear ONLY for lines registered as edge/pulse.  Consequence: a per-line mode the model does not have today
  (ICW1 bit 3 is a TODO `fatal`); which lines are edge on real hardware (ISA: all except PCI-routed lines via ELCR).
* **(D) narrowest: keep the arms, but re-set the IRR bit immediately when the device's line is still asserted** --
  requires a shadow of the line level separate from IRR (`bus_isa_data` has none today), so it is (A) with extra
  state; named so the set is complete, not recommended.
* **(E) do nothing in the PIC; make every ONE-SHOT source re-assert on its tick** (the `dev_ne2000.c` precedent, applied
  to pckbc and mc146818).  Treats the symptom at each device; leaves the EOI's IRR clear in place.

The option-set question (§E 3) is open: is there a member not named here -- the fork's own idioms for an interrupt
controller that tracks in-service state (grep `isr` / `in_service` across `src/devices/`), or a per-line level shadow
somewhere (the Jazz bridge's `isa_int_asserted` is one)?

## 4. The detector plan and the floor (so the panel can object to the instrument before it exists)

* Instrument: the witness probe extended -- the FIX column re-pinned to the ruled design; rows added for (B)'s ISR
  (if ruled): `poll sets isr`, `eoi clears isr`; for the 8253 (if reachable on malta: program counter 0 and read IRR
  bit 0 across an EOI); for PIC2 (line 12 via the cascade bit 2).  Each session a fresh emulator, one frozen script.
* (a) the pre-fix build in GATE mode (the FIX column) red on the symptom rows; (b) the verbatim reinstatement of the
  removed IRR clear(s) BUILT inside the landed structure and measured red (the #573 L4 precedent); (c) the null medium
  `/bin/false` in GATE mode, `(c): measured at <artifact>`; (d) the DEPENDS-ON enumeration: the fix REMOVES a
  statement under the dominating predicate `(idata >= 0x60 && idata <= 0x67) || ...`, so the (d) variants are the clear
  RE-INTRODUCED under a different predicate -- conditioned on the mask (`if (d->ier & bit)`), on the line number
  (`if (n != 4)`), on `isr` -- and, for (B), the acknowledge conditioned on `current_command` only; (e) the contract
  names what the rows catch.  The clause-(d) table is built by the main loop in small steps (no bulk variant text).
* Gate: `regress/gate_arm.sh` is the device-probe gate by accretion (the `#497`/`#498` reason line; `gatedevicesplit`
  stays OWED); `SCORE_CLAIMS_MANIFEST` 41 -> 42; MANIFEST keys for the probe and its witness copy; the hygiene pins
  re-derived.

**THIS FIRING ANSWERS QUESTIONS 3 AND 4 ONLY** (option-set completeness; the scope question).  Questions 1-2 and 5-6 go to separate firings of this same packet; treat section 2 as given and do not answer them here.  Keep hidden reasoning short and put the VERDICT line and the answers in the response itself.

## 5. The three fixed questions, then the round's

1. **The premise audit.**  Treat every sentence of section 2 as a question.  In particular: (i) "the IRR is the line
   state" -- the writers of `pic->irr` I found are `isa_interrupt_assert/deassert`, `isa_interrupt_common`'s
   cascade fold, the two EOI arms, `dev_v3.c`'s copy of the three handlers, and `dev_algor.c`'s own `&= ~0x18` /
   `&= ~0xc0` clears: is that list complete, and does `dev_algor.c`'s clear belong to THIS round's class (an
   EOI-shaped clear of a line the device may still hold) or to its own row?  (ii) "nothing sets the PIC's ISR" --
   `grep -rn 'isr |=' src/` hits only other devices' own `isr` registers; confirm from `dev_8259.c` itself.
   (iii) the device census in 2.4 -- which of those shapes is wrong, and is any ISA source missing (pccmos is the
   mc146818; the floppy dummy; VGA)?  (iv) the 8253: once `in_use`, is there any path that decrements
   `pending_interrupts_timer0` or deasserts line 0?  (v) is the malta rig's NetBSD or Linux boot driving the 8253
   at all (the Linux comment in `dev_8253.c` says "Linux/MALTA kernels like this")?
2. **"What is the smallest EDIT that breaks this and still passes?"** -- answered in the enumerate form: of the
   clause-(d) variants named in section 4 (the IRR clear re-introduced under `d->ier & bit`, under `n != 4`, under
   `d->isr & bit`), which would the 19 witness rows plus the planned rows catch, and which row reds for each?  Name
   the row you expect to stay green.
3. **Option-set completeness** for section 3: is there a member this brief did not name?  Grep the fork for the
   existing idiom.
4. **Scope.**  Does `i8259isrnever` (ISR never set; the PReP IACK) join this round -- same file, same IRR/ISR class,
   one detector -- or does the round ship (A) alone and file (B)'s acknowledge?  State the consequence for the
   malta Linux flow (poll -> specific EOI, `handle_level_irq`): with (A) alone, a level source that stays asserted
   after its handler re-interrupts at once (correct for level lines); with the 8253 never deasserting, what happens?
5. **The 8253.**  If (A) ships, what clears IRR bit 0 for a guest that programs the PIT?  Is the existing behaviour
   (re-assert every tick while a never-decremented count is > 0) itself a defect to file, and does (A) make it
   guest-visible where it was masked by the EOI?
6. **NetBSD/malta's EOI form** (specific or non-specific; where in `sys/arch/evbmips/malta/pci/` or
   `sys/dev/isa/`), for the exposure record.  A seat with web access may read it; a packet-fed seat names it NOT
   CHECKABLE.

**If, while verifying a claim, you found something ELSE — say so.**

## 6. Answer format

VERDICT line first: `READY` (design (X) as written) | `READY WITH CHANGES` | `NOT READY`, naming the candidate letter
you would ship and the one-line reason.  Then the questions in order, each claim labelled READ (you opened the file),
DERIVED (from this packet), or NOT CHECKABLE (name the one fact that would settle it).  Packet-fed seats: do not plan
to read files; everything a question depends on is inlined above.  File-reading seats: the tree is `GXEMUL-SEC/src/`
at HEAD 94b247db; permitted reading `src/devices/dev_8259.c`, `src/devices/bus_isa.c`, `src/devices/dev_8253.c`,
`src/devices/dev_ns16550.c`, `src/devices/dev_pckbc.c`, `src/devices/dev_mc146818.c`, `src/devices/dev_ne2000.c`,
`src/devices/dev_jazz.c`, `src/devices/dev_prep.c`, `src/devices/dev_eagle.c`, `src/devices/dev_v3.c`,
`src/devices/dev_algor.c`, `src/machines/machine_evbmips.c`, `src/include/devices.h`, and the datasheet text at the
absolute path above.
