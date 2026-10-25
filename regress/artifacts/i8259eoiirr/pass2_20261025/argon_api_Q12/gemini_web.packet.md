# Reading task: packet_Q12 (Gemini web; 2026-10-25)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-T19P2Q12-7149` on a line of its own.

# T19 / `i8259eoiirr` (#574, MED, WRONG-RESULT) -- PASS 2: the DIFF REVIEW (the fix is built and measured in a scratch
# clone; NOTHING is committed yet)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

The pass-1 brief stated five premises wrongly and the seats caught them; the F2 adjudication then overturned six of the
main loop's dispositions and found three defects in the design SKETCH, all repaired here.  **Check the premises, not
just the derivations.**  A seat that re-derives a fact from something this packet did NOT give it is worth more than a
seat that agrees.  **THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` at HEAD `94b247db`**; the fix lives in a scratch clone
(`/tmp/gxt19/fix`, a git-archive of HEAD plus the diff below) and in no project tree.  **If you cannot read files that
is expected** -- the diff, the row table and every measurement are inlined; name any premise you cannot settle rather
than guessing.  **VERDICT LINE FIRST.**

**Language and scope.**  Ordinary correctness engineering on an emulator's interrupt-controller model: a register
write had the wrong side effect on another register, and an acknowledge the model lacked is added.  Scope your reading
to `GXEMUL-SEC/src/`, `GXEMUL-SEC/regress/*.py`, and under `GXEMUL-SEC/regress/artifacts/i8259eoiirr/`: `pass1_20261025/`
(`PASS1_RULINGS.md`, `f2_20261025/F2_RULINGS.md`, `timer_explore_20261025/`, `rate_explore_20261025/`),
`witness_20261025/`, `witness_20261025b/`, `pass2_20261025/` (`fixlegs_082756/`, `legs_083333/`) and
`killtable_20261025/PRETABLE.out`; the datasheet text by ABSOLUTE path `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\i8259\8259A.txt`.
Do not read `tools/pipeline/ledger.json`, `CHANGELOG.md` or `OUTSTANDING_BUGS.md`.  Do not build or run anything; do not
propose a mutant -- section 5 names the mutants already prescribed and asks whether the list is complete.  Cite by grep
anchor or construct name (the citation-form rule).

**The roster for this pass:** Grok 4.7, GLM 5.3 and DeepSeek (packet-fed, two firings: Q12 = questions 1-2, Q34 =
questions 3-4), GPT-6 Astra (reviews here; ADJUDICATES the next pass from the consolidated packet), Gemini 4 Argon (web
route, queued behind another sender).  Fable 5.1 HELD (its question recorded); kimi, minimax and the Opus seat
deliberately not fired; agy quota-walled.

## 1. The defect and the fix, in one paragraph each

**Defect.**  `dev_8259.c` had no interrupt acknowledge: the OCW3 poll read returned a mask-blind poll byte and set no
in-service (ISR) bit, the GT64120 IACK read (`dev_gt.c`, `GT_PCI0_INTR_ACK`) returned the last asserted line and
acknowledged nothing, and the specific EOI stood in for the acknowledge by clearing the REQUEST bit (IRR) of the EOI'd
line (on the chip an EOI resets an ISR bit; the request bit is cleared by the acknowledge).  Measured on malta: the EOI
drops a request a device still holds (`witness_20261025/`), and the 8253 timer -- its pending-event count never retired,
because the only decrement sat in a bus deassert the 8253 never issues -- was re-delivered once per 2^14-instruction
tick: **7,415 IRQ 0 deliveries in 180M guest instructions at a programmed 18 Hz** (`rate_explore_20261025/`).

**Fix (design (G'), ruled at F2).**  A helper `pic8259_acknowledge()` moves the highest-priority UNMASKED request to
service (ISR bit set, IRR bit cleared, the 8253's event retired on pic1 line 0 through the machine's published pointer)
and recomputes the PIC's output line; the read after an OCW3 poll calls it and is ONE-SHOT (later reads return the IRR);
the GT IACK READ calls it (master, then the slave through the cascade) and returns the line; the specific EOI resets the
ISR bit when the line is in service and otherwise CONSUMES the request as before (the legacy path for machines whose
vector read acknowledges nothing -- PReP, footbridge); the non-specific EOI resets the lowest set ISR bit.  Edge-only
(both documented guests program ICW1 0x11); the `default` read arm is byte-identical to HEAD.

## 2. SETTLED PREMISES (recorded resolutions, each with its warrant; the F2 record is `pass1_20261025/f2_20261025/F2_RULINGS.md`)

2.1  `dev_8259.c` and `bus_isa.c` have ONE commit each (the upstream import); `dev_8253.c` was touched at the counter
     latch (#439/#440), never at the tick.  `CHANGELOG.md` has no `i8259eoiirr` hit before this round.  (git log)
2.2  The 8253's count has one writer (`++` in the host-timer callback) and no reset; `bus_isa.c`'s decrement is dead on
     every machine because `bus_isa_init` snapshots `isa_pic_data.pending_timer_interrupts` BEFORE `DEVINIT(8253)`
     publishes it (Astra, Grok; checked).  The fix reads the machine field at call time.
2.3  Both documented malta guests program ICW1 0x11 (edge) and EOI SPECIFICALLY (slave then master); NetBSD acquires the
     vector by the OCW3 poll (`pcib_intr`), Linux by the GT IACK read (`mips_pcibios_iack`, installed by
     `i8259_set_poll`); Linux selects I8253/I8259, programs the PIT, requests IRQ 0, and its `timer_interrupt` returns
     IRQ_HANDLED unconditionally (fetched sources, quoted in F2_RULINGS 1.7/1.8).  NetBSD uses no PIT.
2.4  The malta ISA census: 8259 pair, 8253 (irq 0), mc146818 (irq 8), ns16550 x2 (irq 4, irq 3 -- the second interrupts
     although `in_use=0`), lpt (no assert), pckbc (irq 1/12, unconditional); the GT64120 at 0x1be00000 (timer on irq 9).
     The ns16550 deasserts SYNCHRONOUSLY on a register access (its access function calls its tick) -- Astra's F22
     overturn, checked; Grok's contrary F22 was wrong.
2.5  F2's three sketch defects, all repaired in the diff: the manual cascade pre-fold is GONE (the helper only
     asserts/deasserts `d->irq`; pic2's irq IS the ISA line-2 path, whose assert/deassert folds); the `default` read arm
     does NOT acknowledge and the 0x0c poll is one-shot; the EOI keeps the legacy consume where no acknowledge preceded
     it (so PReP/footbridge, unconverted, behave as HEAD).
2.6  The witness's `poll byte 0x84` row ran MASKED on pass 1 (pin-the-bug); the re-pinned probe polls unmasked and rows
     the masked poll as a symptom (`poll masked`: HEAD 0x84, FIX 0x00).
2.7  The oracle was RE-PINNED FIRST: probe v2 ran on the unmodified HEAD clone (`witness_20261025b/`, 69/69 HEAD column,
     08:01) before any fix measurement; the pass-1 symptom rows `eoi irr4`/`eoi x8` (an EOI with no acknowledge) became
     the CONTRACT row `eoi noack` (both columns 0 -- the legacy consume).
2.8  Host timers: base 65 Hz, batching; a short guest wait after an acknowledge is NOT a retirement oracle (Astra Q3.5);
     the retirement is pinned by the RATE row (a band two orders of magnitude apart).  A zero 8253 count maps to hz 0 in
     this model (a timer that never fires) -- filed `pit8253count0`; the probe uses 0xffff and 0x1000.

## 3. THE DIFF -- `git diff --numstat` of the scratch clone against HEAD, and every hunk INLINED

```
78	29	src/devices/dev_8259.c      INLINED (verbatim below)
18	1	src/devices/dev_gt.c        INLINED (verbatim below)
2	0	src/include/devices.h       INLINED (verbatim below)
```
(tabs rendered as four spaces; the files are otherwise byte-identical to the clone's)

```diff
--- /tmp/gxt19/base/src/devices/dev_8259.c
+++ /tmp/gxt19/fix/src/devices/dev_8259.c
@@ -49,6 +49,42 @@
 /*  #define DEV_8259_DEBUG  */
 
 
+/*
+ *  pic8259_acknowledge():
+ *
+ *  #574: The acknowledge this model never had.  The chip moves the highest-priority
+ *  unmasked request to service when the CPU acknowledges it (the INTA cycle, or the
+ *  read that follows an OCW3 poll): the ISR bit is set and, in edge mode -- the only
+ *  mode this tree's guests program (ICW1 0x11) -- the IRR bit is reset.  Called from
+ *  the poll read below and from the GT64120 interrupt-acknowledge read (dev_gt.c).
+ *  Line 0 of pic1 is the 8253, whose pending-event count is retired here: dev_8253.c
+ *  publishes it through machine->isa_pic_data, and bus_isa.c's own decrement runs
+ *  only inside a deassert the 8253 never issues.  Returns the acknowledged line, or
+ *  -1 when no unmasked request is pending (nothing changes).
+ */
+int pic8259_acknowledge(struct pic8259_data *d, struct machine *m)
+{
+    struct isa_pic_data *p = &m->isa_pic_data;
+    int pending = d->irr & ~d->ier, n = 0;
+
+    if (pending == 0)
+        return -1;
+    while (!(pending & (1 << n)))
+        n ++;
+    d->isr |= 1 << n;
+    d->irr &= ~(1 << n);
+    if (d == p->pic1 && n == 0 && p->pending_timer_interrupts != NULL &&
+        *p->pending_timer_interrupts > 0)
+        (*p->pending_timer_interrupts) --;
+    /*  pic2's irq is the cascade line (bus_isa.c folds it into pic1 bit 2).  */
+    if (d->irr & ~d->ier)
+        INTERRUPT_ASSERT(d->irq);
+    else
+        INTERRUPT_DEASSERT(d->irq);
+    return n;
+}
+
+
 DEVICE_ACCESS(8259)
 {
     struct pic8259_data *d = (struct pic8259_data *) extra;
@@ -101,32 +137,42 @@
                 /*  Put Master in Buffered Mode  */
                 d->current_command = 0x0c;
             } else if (idata == 0x20) {
-                int old_irr = d->irr;
-                /*  End Of Interrupt  */
+                /*  Non-specific End Of Interrupt.  #574: resets
+                    the highest-priority in-service bit (the lowest
+                    set ISR bit, fixed priority) and nothing else;
+                    the request bits belong to the lines and to the
+                    acknowledge (pic8259_acknowledge).  This arm
+                    also did irr &= ~isr; isr = 0 -- a no-op on
+                    irr while nothing set isr.  */
                 /*  TODO: in buffered mode, is this an EOI 0? */
-                d->irr &= ~d->isr;
-                d->isr = 0;
-                /*  Recalculate interrupt assertions,
-                    if necessary:  */
-                if ((old_irr & ~d->ier) != (d->irr & ~d->ier)) {
-                    if (d->irr & ~d->ier)
-                        INTERRUPT_ASSERT(d->irq);
-                    else
-                        INTERRUPT_DEASSERT(d->irq);
-                }
+                if (d->isr)
+                    d->isr &= ~(d->isr & -d->isr);
             } else if ((idata >= 0x21 && idata <= 0x27) ||
                 (idata >= 0x60 && idata <= 0x67) ||
                 (idata >= 0xe0 && idata <= 0xe7)) {
-                /*  Specific EOI  */
-                int old_irr = d->irr;
-                d->irr &= ~(1 << (idata & 7));
-                d->isr &= ~(1 << (idata & 7));
-                /*  Recalc. int assertions, if necessary:  */
-                if ((old_irr & ~d->ier) != (d->irr & ~d->ier)) {
-                    if (d->irr & ~d->ier)
-                        INTERRUPT_ASSERT(d->irq);
-                    else
-                        INTERRUPT_DEASSERT(d->irq);
+                /*  Specific EOI.  #574: when the line is in
+                    service (an acknowledge -- the poll read, or
+                    the GT IACK read -- moved its request to ISR),
+                    the EOI resets that ISR bit and leaves the
+                    request bit alone, as on the chip.  When it is
+                    NOT (a guest whose vector read acknowledges
+                    nothing -- dev_prep.c, dev_footbridge.c -- or
+                    none at all), the EOI still consumes the
+                    request as it always did here: that consume
+                    is the only one those machines have.  */
+                int bit = 1 << (idata & 7);
+                if (d->isr & bit) {
+                    d->isr &= ~bit;
+                } else {
+                    int old_irr = d->irr;
+                    d->irr &= ~bit;
+                    if ((old_irr & ~d->ier) !=
+                        (d->irr & ~d->ier)) {
+                        if (d->irr & ~d->ier)
+                            INTERRUPT_ASSERT(d->irq);
+                        else
+                            INTERRUPT_DEASSERT(d->irq);
+                    }
                 }
             } else if (idata == 0x68) {
                 /*  Set Special Mask Mode  */
@@ -148,13 +194,16 @@
                 odata = d->isr;
                 break;
             case 0x0c:
-                /*  Buffered mode.  */
-                odata = 0x00;
-                for (i=0; i<8; i++)
-                    if ((d->irr >> i) & 1) {
-                        odata = 0x80 | i;
-                        break;
-                    }
+                /*  The read after an OCW3 poll.  #574: it is the
+                    interrupt acknowledge (the datasheet's "sets
+                    the appropriate IS bit"), of the highest
+                    unmasked request -- the raw irr scan that stood
+                    here returned masked lines too.  One read per
+                    poll: later reads return the IRR until the next
+                    OCW3.  */
+                i = pic8259_acknowledge(d, cpu->machine);
+                odata = i < 0 ? 0x00 : (0x80 | i);
+                d->current_command = 0x0a;
                 break;
             default:
                 odata = 0x00;
--- /tmp/gxt19/base/src/devices/dev_gt.c
+++ /tmp/gxt19/fix/src/devices/dev_gt.c
@@ -152,8 +152,25 @@
         break;
 
     case GT_PCI0_INTR_ACK:
+        /*  #574: a PCI interrupt-acknowledge READ is the acknowledge
+            (Linux/malta's mips_pcibios_iack reads it in place of an
+            OCW3 poll): move the request to service in pic1, then in
+            pic2 through the cascade, and return the LINE (0-15, as
+            last_int).  Nothing pending, no ISA PICs on this machine
+            (MVME5500), or a write: last_int, as before.  */
         odata = cpu->machine->isa_pic_data.last_int;
-        /*  TODO: Actually ack the interrupt?  */
+        if (writeflag == MEM_READ &&
+            cpu->machine->isa_pic_data.pic1 != NULL) {
+            struct isa_pic_data *p = &cpu->machine->isa_pic_data;
+            int n = pic8259_acknowledge(p->pic1, cpu->machine);
+            if (n == 2 && p->pic2 != NULL) {
+                int n2 = pic8259_acknowledge(p->pic2, cpu->machine);
+                if (n2 >= 0)
+                    n = 8 + n2;
+            }
+            if (n >= 0)
+                odata = n;
+        }
         break;
 
     case GT_TIMER_CTRL:
--- /tmp/gxt19/base/src/include/devices.h
+++ /tmp/gxt19/fix/src/include/devices.h
@@ -73,6 +73,8 @@
     uint8_t        isr;        /*  interrupt in-service register  */
     uint8_t        ier;        /*  interrupt enable register  */
 };
+struct machine;
+int pic8259_acknowledge(struct pic8259_data *d, struct machine *m);    /*  #574  */
 
 /*  dev_dec_ioasic.c:  */
 #define    DEV_DEC_IOASIC_LENGTH        0xc0000
```

The enclosing function's tail (unchanged, so the sketch rule is satisfied): after the `switch (relative_addr)` the
function ends `if (writeflag == MEM_READ) memory_writemax64(cpu, data, len, odata); return 1;`.  The `default:` read arm
(the raw scan) is untouched.  `fatal()` in this tree prints and returns.

## 4. THE DETECTOR (`regress/i8259_eoi_probe.py`, v2c, md5 13490a35e2592dfb876189c4e55695aa, 77 rows, 11 sessions on the
## unmodified `evbmips -e malta`) and WHAT WAS MEASURED

Every emitted guest word is checked against the emulator's own disassembler (CONTROL 0); every session parks at its halt
breakpoint with the pc verified; RAM liveness per session; the device signature (`quiet *`).  Sessions and rows:

```
session  rows (kind)                                          HEAD    FIX     channel
quiet    quiet irr/isr/poll/imr (control)                     0 0 0 0 same    nothing pending reads 0 everywhere
level    level irr4 (control) 1; level isr (contract) 0; eoi noack (CONTRACT) 0 / 0 -- the un-acknowledged EOI's
         legacy consume, both columns; reassert irr4 (control) 1; eoi noack isr (contract) 0
ack      ack irr4 1; poll byte 0x84 (control); poll isr 0x00/0x10; poll irr4 1/0; poll once 0x84/0x00 (a second read
         of the command port right after the poll); in-service irr4 (control, after a tick) 1; eoi acked 0/1 (EOI 0x64
         with the line in service and re-asserted); eoi acked isr (contract) 0
ack3     ack3 irr3 1; poll3 byte 0x83; poll3 isr 0x00/0x08; in-service irr3 1; eoi acked3 0/1       (the n != 4 anchor)
masked   masked irr4 (contract) 1; masked imr 0x10; poll masked 0x84/0x00; masked eoi (contract) 0/0
nonspec  both irr 0x18 (control); poll first 0x83; poll second 0x83/0x84; isr both 0x00/0x18; nonspec lowest 0x00/0x10
         (0x20 resets the lowest ISR bit); nonspec twice (contract) 0
casc     mc146818 periodic (irq 8, pic2) after ~54M instructions: casc irr2 1; casc poll 0x82; casc isr2 0x00/0x04;
         casc slave poll 0x80; casc isr8 0x00/0x01; casc eoi isr / isr8 (contract) 0 after EOI 0x60 (slave), 0x62
pit      8253 counter 0 at 291 Hz after ~54M instructions: pit irr0 1; pit poll 0x80; pit poll irr0 1/0
gt       UART level + a `lw` from 0xbbe00c34: gt irr4 1; gt iack 4 (control, both); gt isr 0x00/0x10; gt irr4 after 1/0
gtcasc   RTC pending + the GT IACK read: gtcasc irr2 1; gtcasc iack 8 (both); gtcasc isr2 0x00/0x04; gtcasc isr8
         0x00/0x01; the two EOIs clear both (contract)
rate     a handler at the general exception vector (poll + specific EOI, counts in s2), only line 0 unmasked, counter 0
         = 0xffff (18 Hz), 180M instructions: rate imr 0xfe; rate delivered >= 1; rate poll byte 0x80; rate storm
         (BAND) HEAD >= 5000 / FIX 1..1000
stable:* each session's IRR read twice (control)
```

MEASURED (artifact paths under `regress/artifacts/i8259eoiirr/`):
* `witness_20261025b/RESULTS.txt` -- probe v2 on the UNMODIFIED HEAD clone (binary 6d1e627a), HEAD column: 69/69,
  CONTROL OK (08:01, before any fix measurement; the oracle re-pin).  Rate: 7,397 deliveries.
* `pass2_20261025/fixlegs_082756/RESULTS.txt` -- probe v2c, BOTH legs: HEAD column on base 77/77; FIX column on the fix
  clone (binary e527ab18, sources de16fa14/4c3bdbb1/9802103c, binary newer than both edited files) 77/77; CONTROL OK on
  both.  Rate: HEAD 7,992 / FIX 4 deliveries in 180M instructions.
* `pass2_20261025/legs_083333/` -- the floor legs on the same frozen probe: L0 = the PRE-FIX build in GATE mode against
  the FIX column: **59/77, CONTROL OK, exactly the 18 symptom rows red** (clause (a)); L3 = `/bin/false` in GATE mode:
  CONTROL FAIL, 0/77, sentinel present (clause (c)).
* `killtable_20261025/PRETABLE.out` (written 08:1x, BEFORE table 1) -- sibling parity, claim->row, guard/body fields,
  the CHANNEL per symptom row, and the PRESCRIBED table: (b) B_eoi, B_poll, B_gt, B_nonspec; (d) D_eoi_n4, D_eoi_n3,
  D_eoi_ier, D_scan_raw, D_noretire, M_sticky, M_noack_isr, M_noack_irr, D_gt_nocasc, plus two EXPECTED ESCAPES
  disclosed (D_gt_write: no row writes the IACK register; D_fold: the F2 cascade defect is a CPU-line observable with two
  slave sources, which no register row reads -- owed as a filed row).  The table is RUNNING as this brief goes out
  (`/tmp/gxt19/killtable_083400/`, scratch clones `/tmp/gxt19/m_*` each with a `.MUTANT` sentinel); its SCORES.txt goes
  to the adjudication pass.  Two rows the fix depends on are rowed for the line partition the body induces (lines 4 and
  3 on both EOI forms; line 0 via the PIT; the slave via the RTC).

**THIS FIRING ANSWERS QUESTIONS 1 AND 2 ONLY** (the premise audit; the smallest edit).  Questions 3-5 go to a separate firing; do not answer them here.  Keep hidden reasoning short; VERDICT line first.

## 5. The three fixed questions, then the round's

**Q1 -- PREMISE AUDIT.**  Mark each claim READ / DERIVED / NOT CHECKABLE.  Which of 2.1-2.8 is wrong?  In particular:
(i) is `d->isr & bit` the right discriminator for "in service" given that nothing else sets ISR (the helper is the only
setter) -- can a guest reach the legacy branch on a line that IS in service, or the ISR branch on one that is not?
(ii) the one-shot latch: `current_command = 0x0a` after the acknowledging read -- does any supported guest expect the
poll byte on a SECOND read without re-issuing OCW3?  (iii) does the GT IACK read's returned LINE (0-15) match what
Linux's `mips_pcibios_iack` consumer expects from `GT_PCI0_IACK_OFS` on real hardware (the vector byte the PIIX4 returns
is the 8259's vector, `irq_base + n`), and does the model's `last_int` convention (which the fix preserves) matter?

**Q2 -- THE SMALLEST EDIT THAT BREAKS THIS AND STILL PASSES THE 77 ROWS AND THE PRESCRIBED TABLE.**  Name the edit, the
row that should have caught it, and the row that stays green.  PRETABLE.out already discloses two: a WRITE to the GT IACK
register acknowledging (no row writes it) and the manual cascade pre-fold (a CPU-line observable).  Is there a third?

**Q3 -- OPTION-SET AND DESIGN COMPLETENESS, NOW ON THE REAL DIFF.**  (a) The hybrid EOI: is "consume when not in
service" the right contained form, or should the legacy branch ALSO run a recalc only when the line was unmasked (it
does: `old_irr & ~ier` vs new)?  (b) The non-specific EOI resets the LOWEST set ISR bit: the datasheet's "highest
priority" in fixed-priority mode -- is lowest-numbered right when rotation is unimplemented?  (c) The helper recomputes
only `d->irq`; for pic2 that is ISA line 2 -- walk `isa_interrupt_assert`/`isa_interrupt_deassert`/`isa_interrupt_common`
for the two-slave-requests case and say whether a request can be left pending with the CPU line low.  (d) The GT read
on MVME5500 (`pic1 == NULL`) and the `n2 < 0` cell: reachable?  (e) ISR does not inhibit equal/lower requests (no
priority logic): what does a guest see when a second line's request arrives while one is in service, compared with
HEAD?

**Q4 -- SCOPE, RECORDS AND LANDING.**  (a) `i8259isrnever` NARROWS to the PReP/footbridge readers (filed
`isaiackreaders`) -- right, or does the hybrid make those readers' behaviour HEAD-identical enough that the sibling can
close?  (b) The exposure record for #574 becomes: the EOI consume (one-shot sources), the 8253 rate storm (measured), the
mask-blind poll; MED WRONG-RESULT kept.  (c) Rows to file: `pit8253pendingptr`, `pit8253count0`, `i8259cmdhalt`
(HIGH-class, HELD), `i8259ocw2nonspec`, `i8259pollmask` (closed by construction if this lands), `algorisaintclear`,
`isaiackreaders`, `i8259ltim`, `i8259priority`, a cascade CPU-line row (D_fold's owed observable).  (d) The landing: the
probe into `regress/`, a `gate_arm.sh` block (`check "i8259eoi rows run" ... 77` by equality, the house idiom), two
MANIFEST keys, hygiene pins, SCORE_CLAIMS_MANIFEST 41 -> 42; the probe runs ~2.5 minutes per leg (two long-wait sessions
and the rate session) -- acceptable in the weekly battery?  (e) The witness term: `probe:regress/i8259_eoi_probe.py`
with ORDER evidence `witness_20261025/` (pass 1, 03:49, 19 rows) and `witness_20261025b/` (the re-pin, 08:01) both before
any fix measurement -- is the re-pin honestly recorded, and is anything in the pass-1 witness now a WRONG RECORD?

**Q5 -- WHAT DID EVERYONE MISS?**  You have the diff, the rows, the measurements and both guests' sequences.

## 6. Answer format

~~~~
VERDICT: SHIP | SHIP WITH CHANGES | DO NOT SHIP -- <one line>
~~~~
Then Q1 .. Q5 in order, each claim marked READ / DERIVED / NOT CHECKABLE, with the single file or fact that would settle
anything you cannot.  Keep hidden reasoning short; put the answer in the response.

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`T19P2Q12: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
