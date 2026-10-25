# ADJUDICATION PASS (F2) -- research item T19, ledger row `i8259eoiirr` (#574), pass 1 -- GXemul hardened fork

Written 2026-10-25 07:4x by the main loop.  This is the THIRD pass of the round's pass 1 (template §F2): every seat's
findings on the pass-1 design brief, consolidated and numbered, with the main loop's DISPOSITION on each, the
DISAGREEMENTS listed separately with both sides, and the three adjudication questions.  Tree under review:
`GXEMUL-SEC/src/` at HEAD `94b247db` (`src/devices/dev_8259.c` and `src/devices/bus_isa.c` unchanged since the upstream
import `39748e3c`; identical in the working tree and in `est/`).  **No product edit has been made yet.**

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

The pass-1 brief stated at least FOUR premises wrongly and the seats caught them (F1, F2, F4, F9 below); the main loop
then found a fifth in its own instrument (F11).  **Check the premises, not just the derivations.**  A seat that
re-derives a fact from something this packet did NOT give it is worth more than a seat that agrees.  **The tree under
review is `GXEMUL-SEC/src/`** (no pristine-upstream copy sits under the project root any more; a reading that
disagrees with the line numbers here is reading some other tree).  **VERDICT LINE FIRST.**

**Self-review disclosed.**  A seat whose own finding appears below is adjudicating its own work: be HARDER on it, and
check that the DISPOSITION is right, not merely that the finding was.  A ruling that ADOPTS your position is the one
you are least likely to test -- test it.  The design in section 4 adopts Grok's and Astra's missing member; those two
seats should scrutinise it MORE.

**Reading scope (file-reading seats):** `GXEMUL-SEC/src/`; `GXEMUL-SEC/regress/artifacts/i8259eoiirr/pass1_20261025/`
(`packet.md` = the pass-1 brief; the eight seat answers `codex_t19p1.txt`, `grok_t19p1.txt`, `ollama_glm_t19p1_QA/QB/QC.txt`,
`ollama_deepseek_t19p1_QA/QB/QC.txt`; `PASS1_RULINGS.md`; `timer_explore_20261025/RUN_IDENTITY.txt`);
`GXEMUL-SEC/regress/artifacts/i8259eoiirr/witness_20261025/` (`RESULTS_base.txt`, `i8259_eoi_probe.frozen.py.txt`); the
datasheet text by ABSOLUTE path `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\i8259\8259A.txt`.  **Do not read other files
under `regress/artifacts/`, nor `tools/pipeline/ledger.json`, `CHANGELOG.md` or `OUTSTANDING_BUGS.md`.**  Do not build or
run anything; do not propose reproduction recipes.

**The roster for this pass:** GPT-6 Astra (ADJUDICATES -- its answer is the ruling of record, provisional until the
roster completes), Grok 4.7, GLM 5.3 and DeepSeek (packet-fed, two firings: part A = the findings F1-F26, part B = the
disagreements D1-D5 + the design + Q2/Q3), Gemini 4 Argon (web route, QUEUED behind another sender; its pass-1 answer
is OWED -- F26 holds its place).  Fable 5.1 HELD (its question is recorded); kimi, minimax and the Opus seat
deliberately not fired; agy quota-walled (resets ~10-30).

**Answer format -- VERDICT LINE FIRST:**
~~~~
VERDICT: RATIFY | RATIFY WITH CHANGES | NOT RATIFY -- <one line>
WRONG: <the F/D numbers whose disposition you overturn, or "none">
~~~~
Then: Q1 -- one line per F1-F26 and D1-D5: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, with the reason.  Q2 -- WHICH
OF MY ACCEPTED DISPOSITIONS IS WRONG?  I accepted twenty-four of twenty-six findings (one refined, one owed) and ruled
all five disagreements my own way; that is a suspicious number and agreement is not evidence.  Q3 -- WHAT DID ALL OF
US MISS?  Mark claims READ / DERIVED / NOT CHECKABLE.

---

## 1. The facts this pass rests on -- VERIFIED by the main loop after pass 1 (each a reading of a file, a fetch of a
## guest's source, or a measurement; artifacts named)

**1.1 The model's EOI arms and poll arms** (`dev_8259.c`, `DEVICE_ACCESS(8259)`, HEAD; relative_addr 0, write path):

```c
 96:			if (idata == 0x0a) {                d->current_command = 0x0a;
 98:			} else if (idata == 0x0b) {         d->current_command = 0x0b;
100:			} else if (idata == 0x0c) {         /*  Put Master in Buffered Mode  */  d->current_command = 0x0c;
103:			} else if (idata == 0x20) {
104:				int old_irr = d->irr;
105:				/*  End Of Interrupt  */
106:				/*  TODO: in buffered mode, is this an EOI 0? */
107:				d->irr &= ~d->isr;
108:				d->isr = 0;
111:				if ((old_irr & ~d->ier) != (d->irr & ~d->ier)) {
112:					if (d->irr & ~d->ier) INTERRUPT_ASSERT(d->irq); else INTERRUPT_DEASSERT(d->irq); }
117:			} else if ((idata >= 0x21 && idata <= 0x27) ||
118:			    (idata >= 0x60 && idata <= 0x67) ||
119:			    (idata >= 0xe0 && idata <= 0xe7)) {
120:				/*  Specific EOI  */
121:				int old_irr = d->irr;
122:				d->irr &= ~(1 << (idata & 7));
123:				d->isr &= ~(1 << (idata & 7));
125:				if ((old_irr & ~d->ier) != (d->irr & ~d->ier)) {
126:					if (d->irr & ~d->ier) INTERRUPT_ASSERT(d->irq); else INTERRUPT_DEASSERT(d->irq); }
131:			} else if (idata == 0x68) {         /*  Set Special Mask Mode  */  /*  TODO  */
134:			} else if (idata >= 0xc0 && idata <= 0xc7) {   /*  Set IRQ Priority Order  */  /*  TODO  */
137:			} else {
138:				fatal("[ 8259: unimplemented command 0x%02x ]\n", (int)idata);
140:				cpu->running = 0;
141:			}
```
(read path, relative_addr 0:) `case 0x0a: odata = d->irr;` / `case 0x0b: odata = d->isr;` / `case 0x0c:` and
`default:` both scan `d->irr` from bit 0 up and return `0x80 | i` for the first set bit, else 0x00 -- **no `& ~d->ier`,
no ISR set, nothing cleared**.  ICW1 bit 3 (LTIM) only prints a `fatal("TODO: Level triggered")` (:74-76); `fatal()`
in this tree prints and returns.  `struct pic8259_data` (`devices.h:63-75`): `irq, irq_base, current_command,
init_state, priority_reg, irr, isr, ier` -- `ier` is MASK polarity (the output is `irr & ~ier`).  The only ISR writes
anywhere in the file are `d->isr = 0` and `d->isr &= ~bit`; nothing sets ISR.

**1.2 How a line reaches the PIC** (`bus_isa.c`, HEAD): `isa_interrupt_assert` sets `pic1->irr |= mask` (or pic2);
`isa_interrupt_deassert` clears it, and then (:133-138) *"If IRQ 0 has been cleared, then this is a timer interrupt.
Let's ack it here:"* `if (old_irr1 & 1 && !(d->pic1->irr & 1) && d->ptr_to_pending_timer_interrupts != NULL &&
(*d->ptr_to_pending_timer_interrupts) > 0) (*d->ptr_to_pending_timer_interrupts) --;`.  `isa_interrupt_common` folds
pic2 into pic1 bit 2 (`pic1->irr |= 0x04` iff `pic2->irr & ~pic2->ier`), returns if `irr & ~ier` did not change, else
DEASSERTs the CPU line when it is 0 or writes `*d->ptr_to_last_int = x` (the lowest pending unmasked line, skipping 2)
and ASSERTs.  **The pointer capture order** (`bus_isa.c:222-225` vs `:241-244`; `dev_8253.c:383-384`): `bus_isa_init`
copies `machine->isa_pic_data.pending_timer_interrupts` right after the 8259's `device_add` and BEFORE the 8253's;
`DEVINIT(8253)` publishes `&d->pending_interrupts_timer0` afterwards; `machine_new` zero-fills -> the bus copy is NULL
on every ISA machine; `dev_v3.c:297-298` snapshots the same way.  **The decrement is dead everywhere.**

**1.3 The 8253** (`dev_8253.c`, HEAD): `timer0_tick` (a `timer_add` host-timer callback at `hz[0]`) does
`d->pending_interrupts_timer0 ++` (:112); `DEVICE_TICK(8253)` (every 2^14 instructions) does `if (!d->in_use) return;
if (d->pending_interrupts_timer0 > 0) INTERRUPT_ASSERT(d->irq);` (:122-128); the file contains NO `INTERRUPT_DEASSERT`
and no other writer of the count (its sites are :105 :112 :114 :127 :384).  `in_use` is set on any access; the host
timer is created on the counter-0 MSB write (:181-197).

**1.4 MEASURED on the unmodified HEAD clone** (`timer_explore_20261025/RUN_IDENTITY.txt`; binary 6d1e627a; two runs):
counter 0 programmed 0x34 then 0x00, 0x10 (count 0x1000 -> the emulator's own `[ 8253: counter 0 set to 4096 (291 Hz) ]`
in the -v log); after ~54M guest instructions IRR bit 0 reads **1**; specific EOI 0x60 then an IRR read two
instructions later reads **0**; after another ~54M instructions IRR bit 0 reads **1** again; ISR reads 0x00 at every
point; the poll byte reads 0x80.  (A short variant, ~5 ms of guest time, read 0 everywhere: the host timer had not
fired -- not a statement about the model.)

**1.5 The witness, MEASURED (pass 1, rung 3, unmodified `evbmips -e malta`; `witness_20261025/RESULTS_base.txt`,
19/19 CONTROL=OK):** with the ISA ns16550 holding IRQ 4 (`level irr4` = 1, ISR 0x00), ONE specific EOI 0x64 clears the
request bit two instructions later (`eoi irr4` HEAD 0x00; FIX column wants 1), eight repetitions all clear it (`eoi x8`
HEAD 0x00; FIX wants 0xff); the non-specific EOI 0x20 leaves IRR (inert: ISR empty); OCW1 masking leaves IRR; `poll
byte` read 0x84 -- and that read was made AFTER the OCW1 0x10 write (the probe's `build_other()` order), i.e. with
line 4 MASKED (F11).

**1.6 The malta ISA census, CHECKED** (`machine_evbmips.c:72`: `bus_isa_init(machine, tmpstr, 0, 0x18000000,
0x10000000)`, flags 0; `bus_isa.c:220-310`): the 8259 pair (+0x20/+0xa0), the 8253 (+0x40, irq 0), pccmos/mc146818
(irq 8), ns16550 x2 (irq 4, irq 3), lpt (irq 7, no assert in `dev_lpt.c`), and -- unconditionally, `bus_isa.c:306-310`
-- a pckbc on irq 1/12; no fdc, no ISA wdc (piix4 IDE by PCI with a disk image); the GT64120 at `0x1be00000`
(`machine_evbmips.c:84`) with its timer on ISA irq 9.  Assert habits (Astra + Grok, CHECKED where cited): ns16550 asserts
every tick while a condition holds and DEASSERTs in the else arm when `int_asserted` (`dev_ns16550.c:96-104`); wdc
asserts every tick while `int_assert`, deasserts on the status read; mc146818 asserts every tick while PIE and its
count > 0, retires one event and deasserts on the register-C read (`dev_mc146818.c:111/118/562-563`); gt asserts
while its count > 0, the `GT_INTR_CAUSE` read deasserts and decrements; pckbc asserts only when `!currently_asserted`
and deasserts when its queue is empty (`dev_pckbc.c:618-637`); the 8253 never deasserts (1.3).

**1.7 NetBSD/malta, READ at source** (`sys/arch/evbmips/malta/pci/pcib.c`, `malta_intr.c`, raw.githubusercontent.com,
2026-10-25): ICW1 = `ICW1_SELECT | ICW1_IC4` (0x11, LTIM clear = EDGE), ICW4_8086; at attach, OCW3 writes
`OCW3_SELECT | OCW3_SSMM | OCW3_SMM` (0x68) then `OCW3_SELECT | OCW3_RR` (0x0a); `pcib_intr`: write `OCW3_SELECT |
OCW3_POLL` to the master and read the poll byte; `if ((irq & OCW3_POLL_PENDING) == 0) return (1);`; `irq =
OCW3_POLL_IRQ(irq); if (irq == 2) { poll icu2 ...; irq = OCW3_POLL_IRQ(irq) + 8 ... }`; run the handlers; then
`if (irq > 7) { write icu2 PIC_OCW2, OCW2_SELECT | OCW2_EOI | OCW2_SL | OCW2_ILS(irq & 7); irq = 2; }` and `write icu1
PIC_OCW2, OCW2_SELECT | OCW2_EOI | OCW2_SL | OCW2_ILS(irq)` -- SPECIFIC EOIs only, slave then master; the IRR/ISR-reading
branch is `#else`'d out; it also writes an ELCR (0x4d0/0x4d1).  `malta_intr.c` calibrates the CP0 count by POLLING the
mc146818's status register and never touches 0x40-0x43: NetBSD never uses ISA irq 0.

**1.8 Linux/malta, READ at source** (`drivers/irqchip/irq-i8259.c`, `arch/mips/mti-malta/malta-int.c`, `malta-time.c`,
`arch/mips/kernel/i8253.c`, `arch/mips/Kconfig`): ICW1 `outb_p(0x11, PIC_MASTER_CMD)` and the same for the slave (edge);
`mask_and_ack_8259A`: `cached_irq_mask |= irqmask; ... outb(cached_master_mask, PIC_MASTER_IMR); outb(0x60+irq,
PIC_MASTER_CMD);` (slave: `outb(0x60+(irq&7), PIC_SLAVE_CMD); outb(0x60+PIC_CASCADE_IR, PIC_MASTER_CMD);`) -- MASK
FIRST, then the specific EOI; the spurious path (`i8259A_irq_real`) writes 0x0B, reads ISR, restores 0x0A.  The vector:
`static int (*i8259_poll)(void) = i8259_irq;` is REPLACED on malta by `i8259_set_poll(mips_pcibios_iack)` in
`arch_init_irq()`, and `mips_pcibios_iack()` reads `GT_READ(GT_PCI0_IACK_OFS)` on the GT64120 (MSC01/Bonito on the
others) -- **it never writes OCW3 0x0c**.  In the model that read is `dev_gt.c:154-157`: `case GT_PCI0_INTR_ACK: odata =
cpu->machine->isa_pic_data.last_int; /* TODO: Actually ack the interrupt? */`.  **The PIT:** `config MIPS_MALTA` carries
`select I8253` and `select I8259`; `malta-time.c`: `#ifdef CONFIG_I8253 /* Only Malta has a PIT. */ setup_pit_timer();
#endif`; `setup_pit_timer()`: `clockevent_i8253_init(true);` then `if (request_irq(0, timer_interrupt, IRQF_NOBALANCING |
IRQF_TIMER, "timer", NULL)) pr_err(...)`; `timer_interrupt`: `i8253_clockevent.event_handler(&i8253_clockevent);
return IRQ_HANDLED;` -- unconditionally HANDLED, so the kernel's spurious-interrupt guard can never disable line 0.

**1.9 The datasheet** (Intel 8259A, `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\i8259\8259A.txt`): IRR/ISR (:166-173) "The
IRR is used to store all the interrupt levels which are requesting service and the ISR is used to store all the
interrupt levels which are being serviced"; the sequence (:223-256) -- at the acknowledge "the highest priority ISR bit
is set and the corresponding IRR bit is reset ... the ISR bit remains set until an appropriate EOI command is issued";
OCW2 (:491-566) -- the EOI commands reset an ISR bit; nothing in OCW2 touches the IRR; 0x21-0x27 have SL=0 and are
NON-specific on hardware; 0xe0-0xe7 rotate on specific EOI; trigger modes (:415, :666-672) -- LTIM=1 level, LTIM=0 edge
("the IR input can remain high without generating another interrupt"); the poll (:596-612) -- the read following P=1
is treated as an interrupt acknowledge and "sets the appropriate IS bit".

**1.10 Three IACK-shaped readers of `isa_pic_data.last_int`** (`git grep last_int`): `dev_gt.c:155` (malta, Linux's
path), `dev_prep.c:57`, `dev_footbridge.c:432`.  Provenance: `dev_8259.c` and `bus_isa.c` have ONE commit each (the
import); `dev_8253.c` was touched by #439/#440 (the counter latch) and the early hardening commits, none at the tick.

---

## 2. Findings F1..F26, attributed, with the main loop's DISPOSITION

Legend: [accepted] / [refined] / [rejected] / [owed].  "Checked" = the main loop opened the file or ran the thing.

F1  (Astra, Grok)  `dev_v3.c` is Algor's V3, not the Iyonix's, and its handlers are not a verbatim copy (dummy line
    16; no `pic2 != NULL` test; `secondary_mask1` routing).  [accepted; records; the EOI arms serve both PIC pairs]
F2  (Astra, Grok)  mc146818 is level-while-count>0, retired by the register-C read -- not one-shot.  [accepted; checked]
F3  (Astra, Grok)  The pending-count pointer is captured before publication; the decrement is dead on every machine;
    the count is a ratchet.  [accepted; CHECKED 1.2/1.3; filed `pit8253pendingptr`; design G2 reads the machine field
    at call time instead]
F4  (Grok)  Linux/malta obtains the vector from the GT IACK read, not OCW3 0x0c.  [accepted; CHECKED 1.8 -- the brief's
    premise was false for Linux and true for NetBSD]
F5  (Astra)  The brief's "~2e-4 interference probability" for the two-instruction read window is unsupported (ticks
    dispatch at batch boundaries).  [accepted; the phrase is withdrawn; the row's evidence is eight agreeing repetitions]
F6  (Astra, Grok)  The "specific EOI" arm also captures 0x21-0x27 (non-specific on hardware) and 0xe0-0xe7 (rotate not
    done); other OCW2/OCW3 bytes reach `cpu->running = 0`.  [accepted; CHECKED; filed `i8259ocw2nonspec` and
    `i8259cmdhalt` (emulation-stop class, HELD with the HIGH rows); not this round's edit]
F7  (Astra, GLM)  Linux's ICW1 0x11 is edge mode; `handle_level_irq` says nothing about the PIC.  [accepted]
F8  (Grok)  Census misses on malta: the GT timer (irq 9), ns16550 #2 (irq 3), lpt (irq 7, no assert), piix4 wdc only with
    a disk.  [accepted; and the main loop adds: the pckbc IS on malta, unconditionally -- 1.6]
F9  (Grok, Astra)  NetBSD/malta EOIs SPECIFICALLY after a POLL, slave then master.  [accepted; CHECKED by fetch 1.7;
    Q6 answered -- every seat that said NOT CHECKABLE was right to from a packet]
F10 (Grok)  `ier` is mask polarity despite the struct comment.  [accepted]
F11 (GLM QA)  The witness's `poll byte 0x84` row ran with line 4 MASKED and the model's poll ignores IMR -- pinning a
    mask-blind poll as a contract value.  [accepted; CHECKED `build_other()`; L1 re-cut before the detector ships;
    filed `i8259pollmask` (fixed by construction under G3 if (G) is ruled)]
F12 (Astra, Grok, GLM QA, DeepSeek QA -- four seats independently)  The three named clause-(d) variants (`if (d->ier &
    bit)`, `if (n != 4)`, `if (d->isr & bit)` around a reinstated IRR clear) all leave the 19 rows green; `eoi irr4` is
    the row that stays green in every case.  [accepted; rows owed: EOI-while-masked (R5); an n != 4 held-level EOI on
    line 0 (R6); `isr & bit` recorded EQUIVALENT under any design that never sets ISR and ROWED under (G), which sets it]
F13 (Grok)  A fourth hole: reinstating only the non-specific arm's `irr &= ~isr` is a no-op while ISR is never set.
    [accepted; equivalent under HEAD's never-set ISR; under (G) a `nonspec after ack` row catches it]
F14 (Astra, GLM QA)  The planned PIC2 line-12 row does NOT discriminate `n != 4` (slave-local n is 4 again; 0x60|12 =
    0x6c would hit the stop path).  [accepted; the n != 4 anchor moves to line 0 (the 8253) -- R6]
F15 (Astra, Grok, GLM QC, DeepSeek QB/QC)  Under (A) alone nothing ever clears IRR bit 0 for a PIT-programming guest; the
    pulse the guest sees today is MANUFACTURED by the defect being fixed (EOI clears, tick re-sets); (A) alone converts
    one interrupt per 2^14-instruction tick into a permanent level.  [accepted; MEASURED 1.4 (HEAD's half) and CHAINED
    to a documented guest 1.8 (the consequence); the central finding of the pass]
F16 (Grok)  With (A) alone, NetBSD's `for (;;)` poll loop returns the same irq again for a still-asserted line.
    [accepted as READ; under (G) the poll acknowledges and the loop exits on the next poll]
F17 (GLM QB, Astra)  (B) as sketched is incomplete: its poll selection ignores the mask; it does not clear IRR at the
    ack; Linux never polls; the non-specific EOI clears ALL ISR bits; the `irr & ~ier & ~isr` formula is multi-site.
    [accepted; (B) rejected as written; its correct core (ISR set at the ack) is inside (G)]
F18 (Astra: "the SOURCE owns assertion lifetime and pending-event retirement" -- bt459, dev_rtc, mc146818, gt;
    Grok: "clear the request at the ACKNOWLEDGE the guest performs; refill from a pin shadow only for a level pin; the
    sites: the poll read, GT_PCI0_INTR_ACK, DEVICE_ACCESS(prep), Algor's reads"; GLM QB: member (F) = (A) + an
    8253-side consumer)  The option set was missing the acknowledge member.  [accepted; it is the design, section 4]
F19 (Grok, DeepSeek QB)  (C) collapses into the acknowledge design once "edge" is the model's own pulse table; (D)
    would restore the 8253's bit too; (E) is a pckbc change that moves no symptom row.  [accepted]
F20 (Astra, Grok, GLM QB, DeepSeek QB)  `i8259isrnever` stays its own row.  [refined: not merged as a row, but (G) sets
    ISR at the poll and the GT read, so the sibling NARROWS to the PReP and footbridge IACK readers (1.10), which have no
    witness machine here -- filed `isaiackreaders`]
F21 (GLM QA/QB, GLM QC)  Under (A) the EOI arms' recalc blocks are dead code (`old_irr == d->irr`).  [accepted; (G)
    REMOVES them from the EOI arms; the helper recalcs]
F22 (GLM QB)  Under (A), for Linux's mask-then-EOI-then-unmask sequence, a tick-deasserting source (ns16550) churns:
    the unmask finds the bit still set until the device's next tick.  [accepted, and it is the reason (G) clears the
    request at the ACK rather than leaving it to the device: a serviced source whose model deasserts late causes no
    spurious re-entry under (G), exactly as it causes none on HEAD -- section 4]
F23 (Astra, Grok)  `dev_algor.c`'s LOCINT/ISAINT READS clear PIC request bits -- a read-acknowledge outside the PIC, same
    class, different producer, no witness machine.  [accepted; filed `algorisaintclear`]
F24 (Grok)  ICW1 LTIM only prints; the model has no level mode; NetBSD writes an ELCR nothing models.  [accepted; (G)
    is edge-only by design (both guests program 0x11); filed `i8259ltim`]
F25 (Astra)  The access function does not enforce `len == 1`; `irq_base` is write-only; the 0x0c poll byte is "Buffered
    mode" in the comment.  [accepted as records; no edit this round]
F26 (Argon, OWED)  Holds the place of the Argon web-route pass-1 answer (queued behind another sender).  [owed]

---

## 3. Disagreements D1..D5 -- both sides in their own words; the main loop's ruling and its warrant

D1  **(A) alone this round?**  GLM QA: "READY WITH CHANGES -- ship (A) ... resolve the §3(A)/§4 floor contradiction on
    the 8253 before (A) ships alone"; GLM QB: "ship (A) alone this round; file (B)'s acknowledge as its own round";
    DeepSeek QA: "ship (A) ... do not close until the 8253/PIT never-deassert path is settled".  Against: Astra "NOT
    READY -- (A) ... needs a defined PIT lifetime/accounting resolution"; Grok "Shipping that edit alone removes the
    only request-consume this model has"; GLM QC "(A) alone breaches the brief's own floor"; DeepSeek QB/QC "NOT READY
    -- (A) alone leaves 8253 IRR bit 0 permanently asserted".
    RULING: REJECT (A) alone.  WARRANT: 1.4 (the HEAD half, measured) + 1.8 (Linux/malta selects I8253, requests IRQ 0,
    `timer_interrupt` returns IRQ_HANDLED unconditionally): under (A) alone a documented guest's IRQ 0 never falls
    after its first unmask.  The "(A) alone" seats conditioned their verdicts on settling exactly this, and it is
    settled against them.
D2  **Where the acknowledge lives.**  GLM QB: "(B) is not one candidate; it is a family with an undecided,
    machine-dependent site (poll / selection / IACK read)" and proposes selection time (`*ptr_to_last_int` is written
    there).  Grok: the sites "actually in src/" -- the poll read, `GT_PCI0_INTR_ACK`, `DEVICE_ACCESS(prep)`, Algor's
    reads.  Astra: "A accompanied by a separately specified PIT lifetime/accounting correction ... not yet a complete
    construction: event consumption, pulse lifetime, and pointer ownership remain unresolved".
    RULING: the acknowledge is performed at the two sites a malta guest actually drives -- the poll read (NetBSD, 1.7)
    and the GT IACK read (Linux, 1.8) -- NOT at selection time (selection happens inside `isa_interrupt_common` on
    every assert; acknowledging there would set ISR on a request the guest has not yet taken, and would be invisible to
    the guest's own sequence).  PReP/footbridge/Algor are filed.  QUESTION FOR THE ADJUDICATOR: the GT read is a
    different device file (`dev_gt.c`) -- is it inside the round-scope rule (same semantic class, one detector, both
    sites witnessed on the same machine by one guest program) or a second round that must ship BEFORE this one?
D3  **Edge-only at the acknowledge.**  (G) clears the IRR bit at the ack for every line and relies on the devices'
    per-tick re-assert to re-request a still-pending level source.  Astra: "`INTERRUPT_ASSERT` invokes the callback
    unconditionally; it neither remembers a level nor suppresses repeated assertions ... a callback invocation cannot
    automatically be interpreted as a new electrical edge" -- i.e. a re-assert from a still-held condition is NOT a new
    edge on hardware.  Grok: LTIM is printed and ignored; "there is no per-line register in this tree".
    RULING: accept edge-only semantics with LTIM filed (`i8259ltim`), on three grounds: both documented guests program
    0x11; the model's devices already re-assert every tick while a condition holds, so a still-pending source is
    re-requested within one tick (more generous than edge hardware, never less); and on HEAD the EOI-consume already
    gives exactly this behaviour, so no guest sees a new shape.  Astra's point is recorded in the contract as the
    disclosed difference (a held line re-requests after the ack within one tick; hardware edge mode would not).
D4  **The dead recalc blocks.**  GLM: "dead code outright; fix the sentence before it becomes the detector's contract".
    RULING: REMOVE the two EOI-arm recalc blocks (the EOI no longer changes `irr`), keep the OCW1 arm's; the helper
    recalcs after the ack.  Warrant: a recalc keyed to a comparison that cannot differ is the check-that-cannot-fail
    shape in product code.
D5  **Severity and exposure of #574 as filed.**  The brief: "a still-asserted level source is lost until the device
    re-asserts (it will not)".  1.6: on malta the re-asserting sources lose a tick of latency, the one-shot pckbc can
    lose a queued byte's request; the LIVE guest-visible defect on malta today is the 8253's rate (one interrupt per
    2^14-instruction tick, forever, 1.4) and the mask-blind poll (F11).  RULING: keep the row at MED WRONG-RESULT with
    its exposure record REWRITTEN to those three channels; no split.  QUESTION: does the adjudicator read the 8253 rate
    defect as THIS row's consequence (one fix, one detector) or as `pit8253pendingptr`'s?  The main loop says this
    row's: the rate is wrong because the EOI stands in for an acknowledge that never retires the event, and (G)
    retires it at the real acknowledge; `pit8253pendingptr` records only the dead pointer.

---

## 4. The design taken to this pass -- (G) "acknowledge": EOI touches ISR only; the guest's acknowledge moves the
## request to service; the 8253's event is retired at that acknowledge

Edits (all in `dev_8259.c` except G4; sketches, each to be run against the enclosing function before it is a fix):
 G1  the two EOI arms: delete `d->irr &= ~d->isr;` (0x20) and `d->irr &= ~(1 << (idata & 7));` (the specific arm);
     keep `d->isr = 0;` / `d->isr &= ~(1 << (idata & 7));`; delete both recalc blocks (D4).
 G2  a static helper `pic8259_acknowledge(struct pic8259_data *d, struct machine *m)`: `pending = d->irr & ~d->ier`;
     none -> return -1 and change nothing; `n` = the lowest set bit; `d->isr |= bit; d->irr &= ~bit;` if `d ==
     m->isa_pic_data.pic1 && n == 0 && m->isa_pic_data.pending_timer_interrupts != NULL &&
     *m->isa_pic_data.pending_timer_interrupts > 0` then `(*m->isa_pic_data.pending_timer_interrupts)--` (read through
     the MACHINE at call time, F3); if `d == m->isa_pic_data.pic2` recompute pic1's cascade bit (`pic1->irr |= 4` iff
     `pic2->irr & ~pic2->ier`, else `&= ~4`, the `bus_isa.c:55-61` fold); then `if (d->irr & ~d->ier)
     INTERRUPT_ASSERT(d->irq); else INTERRUPT_DEASSERT(d->irq);`; return `n`.
 G3  the poll read (`current_command == 0x0c`, and the `default` read arm that emits the same byte today): `n =
     pic8259_acknowledge(d, cpu->machine); odata = n < 0 ? 0x00 : 0x80 | n;`.  (Selection becomes mask-aware as a
     by-product -- F11's defect closes by construction.)
 G4  `dev_gt.c:154-157` (`GT_PCI0_INTR_ACK`): `n = pic8259_acknowledge(pic1, machine)`; if `n == 2` and pic2 exists,
     `n2 = pic8259_acknowledge(pic2, machine)`, `odata = 8 + n2` when `n2 >= 0`; `odata = n` for a master line;
     `odata = last_int` unchanged when nothing was pending (the spurious case is NOT re-designed here).  The helper is
     exported for this one caller (a declaration in `devices.h` beside `struct pic8259_data`).  Witnessed on the same
     machine as the rest: a guest load from `0xbbe00c34` (GT base `0x1be00000` + `GT_PCI0_INTR_ACK` 0xc34, `gtreg.h:114`).
 NOT in this round: `dev_prep.c:57`, `dev_footbridge.c:432` (filed `isaiackreaders`); the ELCR; LTIM=1 level mode
     (`i8259ltim`); the OCW2 census (F6 rows); the Algor read-clears (`algorisaintclear`); the dead decrement in
     `bus_isa.c`/`dev_v3.c` (left in place; `pit8253pendingptr` records it; nothing live depends on the stale copy).

**Why (G) and not "(A) + a line-0 special case at the EOI"** (the smaller edit, which also fixes the rate): the EOI-as-
consume for lines other than 0 leaves every request bit set until the device's own deassert, and ns16550/wdc/gt/
mc146818 deassert on a TICK or on a register read the handler makes BEFORE the EOI -- so under that design Linux's
unmask after the EOI finds the UART's bit still set until the UART's next tick and re-enters the handler with nothing
pending (F22), up to one tick's worth per real interrupt.  HEAD has no such churn because its EOI clears the bit; (G)
keeps that property by moving the clear to where the datasheet puts it (the acknowledge), and the 8253 is covered by
the same move.

**Guest sequences under (G), derived:** NetBSD -- poll (ack: ISR set, IRR cleared) -> handlers -> specific EOIs (ISR
cleared) -> poll again -> nothing pending unless a device re-asserted -> return.  Linux -- GT IACK read (ack) -> handler
-> mask, EOI (ISR cleared) -> unmask -> no re-interrupt unless a device re-asserted.  8253 under Linux -- tick asserts
IRR0 (count > 0) -> IACK read: IRR0 cleared, ISR0 set, count-- -> handler -> EOI -> next tick asserts only if count > 0
-> interrupts at the programmed rate.  pckbc -- ack clears IRR1; `currently_asserted` stays 1 until the queue drains
(the one-shot shape, unchanged from HEAD's EOI-consume; (E) stays filed).

**The detector (L1, rows owed before it is a detector), from PASS1_RULINGS.md §5:** R1 re-cut `poll byte` (poll BEFORE
the mask) + `poll masked` (want 0x00 under (G); HEAD 0x84 -- the pinned defect becomes a red row); R2 `poll acks` (ISR
bit 4 set, IRR bit 4 clear two instructions after the poll); R3 `eoi after ack` (ISR 0x00; IRR bit 4 re-set after the
UART's tick); R4 `eoi irr4`/`eoi x8` unchanged (no poll before the EOI: bit 4 stays 1 under (G)); R5 `masked eoi`
(OCW1 0x10, EOI 0x64, IRR read within two instructions, want 1); R6 the 8253 rows: program the counter, wait ~18M
instructions, control IRR bit 0 = 1; (a) poll -> 0x80 and IRR bit 0 reads 0 two instructions later (HEAD 1); (b) a
separate session, no poll: EOI 0x60 -> IRR bit 0 reads 1 (HEAD 0) -- the n != 4 held-level anchor; (c) poll, then IRR
bit 0 after a short wait (under one host-timer period) wants 0 (HEAD 1: its count never falls); R7 `gt iack` (the load
from `0xbbe00c34` returns 4 in both columns; under (G) ISR 0x10 / IRR bit 4 = 0 afterwards; HEAD ISR 0 / IRR 1);
R8 `nonspec after ack` (poll, then 0x20 -> ISR 0x00; IRR unchanged); R9 cascade via the mc146818 PIE level on line 8
(owed only if the adjudication keeps the cascade inside the round).  Floor: (a) the witness red; (b) verbatim
reinstatement at every edited site (the two EOI clears; the poll's raw scan; the GT read's `last_int` body); (c) a null
medium; (d) DEPENDS-ON over the helper's predicates (`irr & ~ier`; the pic1/line-0 count guard; the cascade fold) and
the EOI arms (ISR only); (e) the contract names LTIM, PReP/footbridge, the spurious IACK case and the cascade as
OUTSIDE unless rowed.

**Owed, and where the main loop may be fooling itself:** the exact sequence of `clockevent_i8253_init(true)`'s PIT
writes is not inlined (it is `drivers/clocksource/i8253.c`; the claim that it programs counter 0's MSB -- the model's
`in_use` and host-timer trigger -- rests on `pit_shutdown`/`pit_set_periodic` writing `PIT_CH0` twice, READ in an
earlier kernel, NOT re-fetched today); whether a malta Linux image this fork's users boot is built with the default
`select I8253` is CHECKED at the Kconfig level only; the `dev_footbridge.c:432` reader's role (cats) was not read;
no mutant has been built yet; the GT IACK row needs the GT's own decode to be reachable from the guest (`memory_device_register` at `dev_gt.c:303` with `DEV_GT_LENGTH`), not yet measured.

---

## 5. The three questions

1. Adjudicate F1..F26 and D1..D5 -- UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.  On D2
   and D3 answer the QUESTIONS posed there explicitly.
2. WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?  I accepted twenty-four of twenty-six findings (one refined, one owed)
   and ruled all five disagreements my own way; that is a suspicious number and agreement is not evidence.  Name the
   count you overturn.
3. WHAT DID ALL OF US MISS?  You now have the whole panel's output, the measurement (1.4) and both guests' sources
   (1.7, 1.8).  In particular: is there a guest sequence (poll with nothing pending; EOI without a preceding ack; an
   ack of a masked line; the cascade) under which (G) is WORSE than HEAD?
