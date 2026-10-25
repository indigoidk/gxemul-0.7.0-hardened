# Reading task: F2B_PACKET_A (Gemini web; 2026-10-25)

**Ground rules.** This is a READING task on the text in this message only. Do not search the web, do not use
any tool or extension, and do not consult anything outside this message, not even to check a hardware fact.
Everything you need is inlined below with line numbers; cite `<block>:<line>` for every claim, for example
`AFTER:823`. If something cannot be settled from this message, mark it UNSETTLED and name the file that would
settle it. Treat every sentence of the commit message as a claim to test, not as evidence. Try to refute each
claim; do not confirm. This is a defensive review: say whether each changed step is correct and whether it
leaves alone every state the running code can save; do not construct an input that makes the present code
fail. Before the final line, write the prompt token `P-T19F2BA-acf3` on a line of its own.

# ADJUDICATION PASS (F2b) -- research item T19, ledger row `i8259eoiirr` (#574), PASS 2 (the diff review) -- GXemul hardened fork

Written 2026-10-25 by the main loop.  This is the THIRD pass of the round's pass 2 (template §F2): every seat's findings on
the pass-2 diff review, consolidated and numbered, with the main loop's DISPOSITION on each, the DISAGREEMENTS listed
separately with both sides in their own words, what is still OWED, and the three adjudication questions.  Tree under
review: `GXEMUL-SEC/src/` (HEAD moved to `fa66b70d` by two records commits of another row; `src/devices/dev_8259.c`,
`src/devices/dev_gt.c` and `src/include/devices.h` are byte-identical to `94b247db`).  **The fix has NOT landed: it lives
only in the scratch clone `/tmp/gxt19/fix` (binary e527ab18), and the diff in section 3 is byte-identical to the one pass 2
reviewed.**  The instrument WAS changed after pass 2 (two repairs, section 4) and re-measured; that is what this pass
adjudicates alongside the dispositions.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

Pass 2 split 1-4 on the verdict and the main loop ruled AGAINST the adjudicating seat (D1).  **Check the premises, not just
the derivations**: a seat that re-derives a fact from something this packet did NOT give it is worth more than a seat that
agrees.  **The tree under review is `GXEMUL-SEC/src/`**; a reading that disagrees with the line numbers here is reading some
other tree.  **VERDICT LINE FIRST.**

**Self-review disclosed.**  GPT-6 Astra ruled DO NOT SHIP on pass 2 and adjudicates here a ruling that overrides its own:
be HARDER on your own three grounds AND on the ruling.  Grok, GLM and DeepSeek ruled SHIP WITH CHANGES and the ruling
adopts that position: scrutinise it MORE, not less -- a ruling in your favour is the one you are least likely to test.
Every seat is also adjudicating its own pass-2 findings (F1-F21 name the seats): check that each DISPOSITION is right, not
merely that the finding was.

**You cannot read files; every fact this pass depends on is inlined in sections 1-4 -- name any premise you cannot settle rather than guessing.**

**The roster for this pass:** GPT-6 Astra (ADJUDICATES -- its answer is the ruling of record, provisional until the roster
completes), Grok 4.7, GLM 5.3 and DeepSeek (packet-fed, two firings: part A = the findings F1-F21, part B = the
disagreements D1-D5 + the owed list + Q2/Q3), Gemini 4 Argon (web route, QUEUED behind the single sender -- its pass-1, F2,
pass-2 and F2b answers are all OWED).  Fable 5.1 HELD (its question is recorded); kimi, minimax and the Opus seat
deliberately not fired; agy quota-walled (resets ~10-30).

**Answer format -- VERDICT LINE FIRST:**
~~~~
VERDICT: RATIFY | RATIFY WITH CHANGES | NOT RATIFY -- <one line>
WRONG: <the F/D numbers whose disposition you overturn, or "none">
~~~~
Then: Q1 -- one line per F1-F21 and D1-D5: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, with the reason.  Q2 -- WHICH OF MY
ACCEPTED DISPOSITIONS IS WRONG?  Of twenty-one findings I accepted ten product-code findings without a product edit,
repaired two instrument defects, disclosed or filed five, corrected four records -- and OVERTURNED NONE; I ruled all five
disagreements my own way, one of them against the adjudicating seat.  That is a suspicious number and agreement is not
evidence.  Q3 -- WHAT DID ALL OF US MISS?  Mark claims READ / DERIVED / NOT CHECKABLE.

---

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
     IRQ_HANDLED unconditionally (fetched sources, quoted in `pass1_20261025/f2_20261025/F2_PACKET.md` sections 1.7/1.8 (R2: the pass-2 brief said F2_RULINGS; the quotes live in the packet)).  NetBSD uses no PIT.
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

## 4. THE INSTRUMENT AS RE-MEASURED AFTER PASS 2 (`regress/i8259_eoi_probe.py` v2d, md5 4b3e475d1c3ee591d4c46159fe7d0e86,
## 908 lines, 84 rows in 12 sessions on the unmodified `evbmips -e malta`) -- the two repairs and every measurement

**What changed from v2c (77 rows, 11 sessions) -- the two pass-2 instrument findings, both L1 (pre-ship construction):**

* **The one-shot row.**  v2c's `poll once` read the command port after a SECOND poll made with nothing pending, so a sticky
  poll of an empty IRR and the intended IRR read both return 0x00 -- the row could not see `M_sticky` (Astra Q2, Grok Q2/Q5,
  GLM Q12).  v2d moves the one-shot row to the MASKED session: the masked poll (OCW1 0x10, then OCW3 0x0c and the poll read,
  which under the fix acknowledges NOTHING because line 4 is masked) is followed by one more command-port read.  Under the
  fix the latch has reverted, so that read returns the IRR = 0x10 (line 4 still pending, masked); under a STICKY latch it
  would return the poll byte of an empty unmasked set, 0x00; HEAD returns 0x84 (its poll byte ignores the mask).  Row
  `poll once`: HEAD 0x84 / FIX 0x10.  The v2c row is kept under the honest name `poll again` (HEAD 0x84 / FIX 0x00: it
  measures HEAD's unconsumed request, not the latch).
* **The returned line.**  No v2c row pinned the GT read's RETURNED value against a dropped `if (n >= 0) odata = n;`: the
  single-source rows `gt iack` (4) and `gtcasc iack` (8) stay green because `last_int` equals the acknowledged line there
  (Astra Q2, Grok Q2).  v2d adds the session `gtboth`: the UART (IRQ 4, level) and the mc146818 periodic interrupt (IRQ 8,
  pic2) pending TOGETHER, then one `lw` from 0xbbe00c34.  Control `gtboth irr`: IRR has bits 2 and 4 set (0x14).  Symptom
  rows: `gtboth iack` -- HEAD's flat scan in `isa_interrupt_common` skips line 2 and reports 4; the acknowledge takes the
  highest priority = line 2 and, through the cascade, line 8: HEAD 0x04 / FIX 0x08; `gtboth isr2` 0x00/0x04; `gtboth isr8`
  0x00/0x01.  Mutant `D_gt_noassign` (`if (n >= 0) odata = n;` -> `;`) is prescribed; expected killed by `gtboth iack`.

The row table of the pass-2 brief (section 4 of `packet.md`) otherwise stands: 12 sessions (`quiet`, `level`, `ack`, `ack3`,
`masked`, `nonspec`, `casc`, `pit`, `gt`, `gtcasc`, `gtboth`, `rate`); every emitted guest word checked against the
emulator's own disassembler (CONTROL 0); every session parks at its halt breakpoint with the pc verified; RAM liveness per
session; the device signature (`quiet *`); `stable:*` reads each session's IRR twice.  22 symptom rows (HEAD and FIX
columns differ), the rest controls and CONTRACT rows (same both columns).

**MEASURED, in this order (artifact paths under `regress/artifacts/i8259eoiirr/`; every number below is read from the
named file):**

* `witness_20261025c/RESULTS.txt` -- probe v2d on the UNMODIFIED HEAD clone (binary 6d1e627a), HEAD column: **84/84,
  CONTROL OK** (WSL clock 08:58, banked 09:00:53, BEFORE any v2d fix measurement -- the oracle re-pin of the two new rows;
  the v2 re-pin `witness_20261025b/`, 69/69 at 08:01, stands for the rows it carried).  Rate on HEAD: 0x2009 = 8,201
  deliveries in 180M instructions.
* `pass2_20261025/fixlegs_090053/RESULTS.txt` -- probe v2d, BOTH legs: HEAD column on the base clone **84/84**; FIX column
  on the fix clone (binary e527ab18, sources de16fa14 / 4c3bdbb1 / 9802103c, binary newer than both edited files) **84/84**;
  CONTROL OK on both.  Rate: HEAD 0x1d69 = 7,529 / FIX 0x03 = 3 deliveries in 180M instructions.
* `pass2_20261025/legs_090604/` -- the floor legs on the same frozen probe: **L0** = the PRE-FIX build in GATE mode against
  the FIX column: **62/84, CONTROL OK, exactly the 22 symptom rows red** (`poll isr`, `poll irr4`, `poll again`,
  `eoi acked`, `poll3 isr`, `eoi acked3`, `poll masked`, `poll once`, `poll second`, `isr both`, `nonspec lowest`,
  `casc isr2`, `casc isr8`, `pit poll irr0`, `gt isr`, `gt irr4 after`, `gtcasc isr2`, `gtcasc isr8`, `gtboth iack`,
  `gtboth isr2`, `gtboth isr8`, `rate storm` at 0x1e2e = 7,726) -- clause (a); **L3** = `/bin/false` in GATE mode:
  **CONTROL FAIL, 0/84**, sentinel present -- clause (c).
* `killtable_20261025/PRETABLE.out` (written 08:1x, BEFORE table 1; the CORRECTION block appended 08:5x names the wrong
  CHANNEL line for `poll once`, the unprescribed `D_gt_noassign`, and the rule that the v2c table stands as the record of
  what it measured while the table of record re-runs every mutant on v2d).
* `killtable_20261025/SCORES_v2c.txt` -- the FIRST table, on v2c (15 mutants, 08:35-09:12): **12 KILLED, 3 ESCAPED:
  `M_sticky` 77/77** (as Astra, Grok and GLM predicted -- the vacuous row), `D_gt_write` 77/77 and `D_fold` 77/77 (the two
  escapes PRETABLE.out disclosed in advance).  `D_gt_nocasc` was KILLED 75/77 with **CONTROL=FAIL**: the red rows were
  `gtcasc iack` (0x02 where both columns want 0x08 -- the mutant returns the cascade line itself, which a guest would
  dispatch on) and `gtcasc isr8`; the IACK row is a both-columns `want` row, so its red is reported under the CONTROL
  flag.  A kill, but one whose channel is a value row the probe classes as a control -- say if that classification should
  change.
* `killtable_20261025/SCORES.txt` -- **THE TABLE OF RECORD, on v2d, 16 mutants** (the 15 prescribed plus
  `D_gt_noassign`), each a fresh `cp -a` of the fix clone with a `.MUTANT` sentinel, one text edit with its pre-image
  asserted, an incremental rebuild checked newer than the edited file, the frozen v2d probe in GATE mode:

16 mutants built and measured in scratch clones against the frozen v2d probe in GATE mode (`killtable_20261025/SCORES.txt`, the table of record; the v2c table stands beside it as `SCORES_v2c.txt`): **14 KILLED, 2 ESCAPED (D_gt_write, D_fold)**.

```
  B_eoi         82/84  CONTROL=OK   KILLED   reds: eoi acked 0x00 head 0x00 ; eoi acked3 0x00 head 0x00
  B_poll        69/84  CONTROL=OK   KILLED   reds: poll isr 0x00 head 0x00 ; poll irr4 0x01 head 0x01 ; poll again 0x84 head 0x84 ; eoi acked 0x00 head 0x00 ; po
  B_gt          77/84  CONTROL=OK   KILLED   reds: gt isr 0x00 head 0x00 ; gt irr4 after 0x01 head 0x01 ; gtcasc isr2 0x00 head 0x00 ; gtcasc isr8 0x00 head 0x00
  B_nonspec     83/84  CONTROL=OK   KILLED   reds: nonspec lowest 0x00 head 0x00
  D_eoi_n4      82/84  CONTROL=OK   KILLED   reds: eoi acked 0x00 head 0x00 ; eoi acked isr 0x10 want 0x00
  D_eoi_n3      83/84  CONTROL=OK   KILLED   reds: eoi acked3 0x00 head 0x00
  D_eoi_ier     76/84  CONTROL=OK   KILLED   reds: eoi acked 0x00 head 0x00 ; eoi acked isr 0x10 want 0x00 ; eoi acked3 0x00 head 0x00 ; masked eoi 0x01 want 0x0
  D_scan_raw    81/84  CONTROL=OK   KILLED   reds: masked irr4 0x00 want 0x01 ; poll masked 0x84 head 0x84 ; poll once 0x00 head 0x84
  D_noretire    83/84  CONTROL=OK   KILLED   reds: rate storm 0x1c18 head 5000..inf
  M_sticky      83/84  CONTROL=OK   KILLED   reds: poll once 0x00 head 0x84
  M_noack_isr   71/84  CONTROL=OK   KILLED   reds: poll isr 0x00 head 0x00 ; eoi acked 0x00 head 0x00 ; poll3 isr 0x00 head 0x00 ; eoi acked3 0x00 head 0x00 ; is
  M_noack_irr   76/84  CONTROL=OK   KILLED   reds: poll irr4 0x01 head 0x01 ; poll again 0x10 head 0x84 ; poll second 0x83 head 0x83 ; isr both 0x08 head 0x00 ; 
  D_gt_nocasc   80/84  CONTROL=FAIL KILLED   reds: gtcasc iack 0x02 want 0x08 ; gtcasc isr8 0x00 head 0x00 ; gtboth iack 0x02 head 0x04 ; gtboth isr8 0x00 head 0
  D_gt_noassign 83/84  CONTROL=OK   KILLED   reds: gtboth iack 0x04 head 0x04
  D_gt_write    84/84  CONTROL=OK   ESCAPED  reds: 
  D_fold        84/84  CONTROL=OK   ESCAPED  reds: 
```

The two repairs' own mutants: M_sticky KILLED (83/84); D_gt_noassign KILLED (83/84).  Escapes beyond the two disclosed in PRETABLE.out: NONE.
**THIS FIRING ANSWERS QUESTION 1 FOR THE FINDINGS F1..F21 ONLY** (UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each, with the reason; then WHICH of the accepted dispositions is wrong).  The disagreements, the owed list and Q2/Q3 go to a separate firing; do not answer them here.  Keep hidden reasoning short; VERDICT line first.


## 5. FINDINGS F1..F21, attributed, with the main loop's DISPOSITION (from `pass2_20261025/PASS2_RULINGS.md`)

**On the DIFF (product code) -- none required a change to the shipped design:**

**F1** (Astra Q1(i), Grok (i), GLM (i), DeepSeek (i))  `d->isr & bit` is the right in-service discriminator for the contained
model: the helper is the only setter (idempotent), both EOI arms only clear.  Astra's refinement: a second acknowledge of the
same line before its EOI is permitted (no priority inhibition, `i8259priority`), so one EOI clears the bit and a second EOI
takes the legacy branch -- a consequence of the deferred priority defect.  [ACCEPTED, refinement disclosed; no edit]

**F2** (Astra (ii), Grok (ii), GLM (ii), DeepSeek (ii))  The one-shot poll: no documented guest re-reads the command port
without another OCW3; the revert to the IRR is the approximation the F2 record flagged.  GLM Q34 (4) sharpens it: the chip
reverts to the LAST RR/RIS selection, not to the IRR, so a guest that selected the ISR, polled, and re-read would see the
wrong register.  [ACCEPTED as a disclosed approximation, recorded in the contract; no edit -- see D2]

**F3** (Grok (iii) SETTLED; Astra (iii) and DeepSeek (iii) NOT CHECKABLE)  The GT read returns the LINE (0-15): Linux
programs ICW2 bases 0 and 8 (`I8259A_IRQ_BASE` 0) and dispatches on the raw IACK byte, so the byte IS the line;
`last_int`'s convention is kept; adding the model's `irq_base` would double-offset the dispatch.  [ACCEPTED on Grok's
reading of the Linux source; the model's `irq_base` stays write-only -- see D3]

**F4** (Astra Q3(c), Grok Q3(c) -- both walked `bus_isa.c`; GLM Q34 (c), DeepSeek (c) NOT CHECKABLE)  The fold-free diff
handles two pending slave requests: the slave acknowledge asserts pic2's irq = the ISA line-2 path; `isa_interrupt_assert`
samples the master mask BEFORE setting bit 2 and `isa_interrupt_common` sees the transition and raises the CPU line.
CHECKED by the main loop before the edit.  [ACCEPTED -- see D4, where the code is inlined for the two seats that could not
open it]

**F5** (Astra Q3(b), Grok, GLM, DeepSeek)  Lowest-numbered set ISR bit = highest priority in fixed mode.  [ACCEPTED]

**F6** (Astra Q3(d), Grok, GLM)  `pic1 == NULL` (MVME5500) reachable and guarded; `n2 < 0` unreachable while the fold
invariant holds; the total-function value 2 is right (hardware's spurious IR7 is not modelled; disclosed).  [ACCEPTED]

**F7** (Astra Q1 2.5, GLM Q34 (a), DeepSeek (a))  "Unconverted machines behave as HEAD" holds only where no guest POLLS:
the poll read now acknowledges on every machine, so a PReP/footbridge guest that polls would enter the ISR branch (a fix,
not a regression).  [ACCEPTED; the sibling `i8259isrnever` NARROWS, does not close]

**F8** (Astra Q5)  The GT change reaches Cobalt's GT64011 (its machine creates ISA PICs); whether a Cobalt guest reads the
IACK register is NOT CHECKABLE here.  [ACCEPTED; disclosed in the contract and the row's state note]

**F9** (Astra Q5, GLM Q34 (c))  ISR lifecycle: ICW1 does not reset ISR or `current_command`; ICW4 AEOI is unsupported while
the helper always sets ISR (an AEOI guest would accumulate ISR bits; the output never consults ISR, so no line is lost).
[ACCEPTED; FILED `i8259aeoi` (LOW) and `i8259icwreset` (LOW); not this round's edit]

**F10** (GLM Q34 Q5 (3))  Special mask mode (OCW3 0x68, an empty TODO arm) vs the helper's `~ier`.  [ACCEPTED as a note
beside `i8259ltim`; filed with `i8259aeoi`]

**On the INSTRUMENT:**

**F11** (Astra Q2, Grok Q2+Q5, GLM Q12 Q2 -- three seats)  `poll once` as built in v2c was VACUOUS (section 4).  [REPAIRED
in v2d, L1; the measured kill is in the table of record above]

**F12** (Astra Q2, Grok Q2+Q5)  No row pinned the GT read's RETURNED LINE.  [REPAIRED in v2d: the `gtboth` session and
mutant `D_gt_noassign`, L1; measured above]

**F13** (GLM Q12 Q2)  The retire guard `d == p->pic1 && n == 0`: dropping either conjunct is observable only through a race
between a host-timer fire and the next tick, so no deterministic row exists.  [DISCLOSED under clause (e) with the
derivation, in PRETABLE.out and the contract; not rowed -- see D5]

**F14** (GLM Q12 Q2)  The helper's final recompute replaced by an unconditional DEASSERT escapes every register row and the
single-line rate row; it is the CPU-line class the owed `i8259cascline` row covers.  [DISCLOSED; filed with that row]

**F15** (Astra Q4(e), GLM Q34 (e))  The pass-1 witness is SUPERSEDED, not wrong: it measured a disclosed different protocol;
`witness_20261025b/` and `witness_20261025c/` are the oracle pins, `witness_20261025/` is history; every row addition had
its HEAD column pinned on the base clone before its fix measurement.  [ACCEPTED; named in the records]

**F16** (GLM Q12 2.8)  The rate band guarantees a 5x separation at its boundaries (>= 5000 vs <= 1000); "two orders of
magnitude" is the measured gap, not the guard.  [ACCEPTED; wording corrected in the probe docstring and the records]

**F17** (GLM Q34 (b))  The storm count is cited as several numbers -- 7,415 (`rate_explore_20261025/rate_073912`), 7,397
(`witness_20261025b/`), 7,992 (`fixlegs_082756/`), 8,201 (`witness_20261025c/`), 7,529 (`fixlegs_090053/`), 7,726
(`legs_090604/L0`): each names its artifact.  [ACCEPTED; applied]

**Records corrections (L4, in place):**

**F18** (Astra Q4(e))  The pass-1 witness ran at 06:51 (WSL clock), not 03:49.  [CORRECTED in the drafts and the generator]

**F19** (Astra Q1 2.3)  The pass-2 brief cited "F2_RULINGS 1.7/1.8" for the guest-source quotes; they live in
`f2_20261025/F2_PACKET.md` 1.7/1.8.  [CORRECTED here, in section 2.3 of the copied facts]

**F20** (Astra Q1 2.7, Q4(e))  "Before the code moves" overstated the order: the fix clone was built 07:56 and the
re-pinned probe first ran on HEAD at 08:01; what every FIX measurement follows is the HEAD run of the same instrument
revision (v2 at 08:01, v2d at 08:58).  [CORRECTED in the probe docstring and F2_RULINGS A3]

**F21** (Astra Q1 2.8)  "A timer that never fires": the clamp is 1e-8 Hz -- "does not fire within any run" is the honest
sentence (`pit8253count0`).  [CORRECTED]

(End of part A.)

## Verdict

End your reply with exactly one final line of this form, and nothing after it:

`T19F2BA: <n> ATTACKS <b> BROKEN <h> HOLDS <u> UNSETTLED DRAFTABLE:<YES|NO>`

`<n>` counts the points you tested and must equal `<b> + <h> + <u>`. `DRAFTABLE:YES` means you found nothing
that must change before the diff is written into the series.
