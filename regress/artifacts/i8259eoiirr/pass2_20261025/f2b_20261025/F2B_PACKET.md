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

**Reading scope (file-reading seats):** `GXEMUL-SEC/src/`; `GXEMUL-SEC/regress/i8259_eoi_probe.py` (the v2d instrument, in
the working tree; md5 4b3e475d); `GXEMUL-SEC/regress/artifacts/i8259eoiirr/pass2_20261025/` (`packet.md` = the pass-2 brief;
the six seat answers `codex_t19p2.txt`, `grok_t19p2.txt`, `ollama_glm_t19p2_Q12/Q34.txt`, `ollama_deepseek_t19p2_Q12/Q34.txt`;
`PASS2_RULINGS.md`; `fixlegs_090053/`, `legs_090604/`); `witness_20261025c/`; `killtable_20261025/` (`PRETABLE.out`,
`SCORES.txt`, `SCORES_v2c.txt`, the per-mutant dirs and `.diff` files); the datasheet text by ABSOLUTE path
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\i8259\8259A.txt`.  **Do not read `tools/pipeline/ledger.json`, `CHANGELOG.md` or
`OUTSTANDING_BUGS.md`.**  Do not build or run anything; do not propose reproduction recipes.

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

## 6. DISAGREEMENTS D1..D5 -- both sides in their own words; the main loop's ruling and its warrant

**D1 -- THE VERDICT.**  GPT-6 Astra (the pass-2 adjudicator), verbatim: *"VERDICT: DO NOT SHIP -- the one-shot coverage
claim is false, GT consumer compatibility remains unproved, and the provenance record needs correction."*  Grok: SHIP WITH
CHANGES (the one-shot row vacuous as built; the GT returned-line escape; F3 settled by the Linux dispatch).  GLM Q12,
verbatim: *"SHIP WITH CHANGES -- no premise in 2.1-2.8 falls from the packet and the inlined diff is consistent with every
stated warrant, but the row table leaves at least one clause of the fix (the one-shot latch) unobserved"*; GLM Q34: *"SHIP
WITH CHANGES -- the diff is internally sound and the row arithmetic verifies, but one design-bearing fact (the bus_isa
cascade fold's re-entrancy) is unsettled and reachable on malta's own device census"*.  DeepSeek Q12: *"SHIP WITH CHANGES
-- Q1(iii) unverified, Q2 third escape uncovered."*; DeepSeek Q34: *"SHIP WITH CHANGES -- Q3(c) unresolved CPU-line stall
with two slave requests; Q1(iii) unresolved GT IACK line vs vector byte."*
**RULING: SHIP WITH CHANGES, the diff unchanged.**  Warrant, ground by ground: (1) the one-shot coverage claim WAS false
and is now REPAIRED AND MEASURED -- `M_sticky`'s score in the table of record (section 4) is the test of this ground; if it
still escapes, this ruling falls; (2) GT consumer compatibility is settled by the Linux source as Grok read it (D3) and
disclosed for Cobalt (F8); (3) the provenance record is corrected in place (F18-F21).  **Astra: adjudicate your own three
grounds against the measurements; say which of them, if any, survives.**  Count the arguments, not the seats: the four SHIP
verdicts each carried a condition, and every condition is discharged or disclosed above -- name the one that is not.

**D2 -- THE ONE-SHOT REVERT TARGET.**  GLM Q34 (4): the chip reverts to the LAST RR/RIS selection after a poll, not to the
IRR; the diff writes `current_command = 0x0a` unconditionally.  The main loop: a disclosed approximation, NO product edit --
both documented guests re-select explicitly (NetBSD writes OCW3 0x0a at attach and 0x0c before every poll; Linux's spurious
path writes 0x0b, reads, and restores 0x0a), so no supported guest observes the difference, and a remembered-selection
field is a product ADDITION that the addition licence refuses on "cannot hurt" alone.  **Question for the seats:** is the
disclosure the right member, or is one remembered byte (`last_rr`, set at 0x0a/0x0b, restored after the acknowledging read)
owed before landing as a correctness matter rather than a nicety?  Which guest would observe it?

**D3 -- THE GT READ RETURNS THE LINE, NOT A VECTOR.**  Grok (SETTLED): Linux's `irq-i8259.c` programs ICW2 bases
`I8259A_IRQ_BASE + 0` and `+ 8` with `I8259A_IRQ_BASE` 0, and `malta-int.c` dispatches `do_IRQ(MALTA_INT_BASE + irq)` on the
byte `mips_pcibios_iack()` returns -- so the byte IS the line, and `last_int`'s convention (HEAD returned the line too) is
preserved.  Astra (iii) and DeepSeek (iii): NOT CHECKABLE from the packet -- on real hardware the PIIX4 returns the 8259's
VECTOR, `irq_base + n`.  The main loop ACCEPTED Grok's reading; the quotes it rests on, verbatim from the pass-1 F2 packet:

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


**RULING: the line.**  Where ICW2's base is 0 the two readings coincide, and the model's `irq_base` field (written by ICW2,
never read) stays write-only in this diff.  **Question for the seats:** does any supported guest that READS the GT IACK
register program a non-zero ICW2 base -- and if the honest form is `irq_base + n`, is that a change to this diff (one
term) or a filed row, given that HEAD's `last_int` convention is what Linux/malta has been consuming all along?

**D4 -- TWO SLAVE REQUESTS WITH THE MANUAL FOLD GONE.**  Astra and Grok walked `bus_isa.c` and found the sequence correct;
GLM Q34 and DeepSeek Q34 could not open the file and called it unresolved ("a CPU-line stall with two slave requests").
The code, verbatim at HEAD, `bus_isa.c` lines 50-141 -- the three cascade functions, every exit path; the IRQ-0 decrement at
133-138 is the dead one of premise 2.2:

```c
 50:  *  isa_interrupt_common():
 51:  */
 52: void isa_interrupt_common(struct bus_isa_data *d, int old_isa_assert)
 53: {
 54: 	int new_isa_assert, x;
 55: 
 56: 	/*  Any interrupt assertions on PIC2 go to irq 2 on PIC1  */
 57: 	/*  (TODO: don't hardcode this here)  */
 58: 	if (d->pic2->irr & ~d->pic2->ier)
 59: 		d->pic1->irr |= 0x04;
 60: 	else
 61: 		d->pic1->irr &= ~0x04;
 62: 
 63: 	/*  printf("ISA: irr=%02x%02x ier=%02x%02x\n",
 64: 	    d->pic2->irr, d->pic1->irr, d->pic2->ier, d->pic1->ier);  */
 65: 
 66: 	new_isa_assert = d->pic1->irr & ~d->pic1->ier;
 67: 
 68: 	if (old_isa_assert == new_isa_assert)
 69: 		return;
 70: 
 71: 	if (!new_isa_assert) {
 72: 		INTERRUPT_DEASSERT(d->irq);
 73: 		return;
 74: 	}
 75: 
 76: 	for (x=0; x<16; x++) {
 77: 		if (x == 2)
 78: 			continue;
 79: 
 80: 		if (x < 8 && (d->pic1->irr & ~d->pic1->ier & (1 << x)))
 81: 			break;
 82: 
 83: 		if (x >= 8 && (d->pic2->irr & ~d->pic2->ier & (1 << (x&7))))
 84: 			break;
 85: 	}
 86: 
 87: 	*d->ptr_to_last_int = x;
 88: 
 89: 	INTERRUPT_ASSERT(d->irq);
 90: }
 91: 
 92: 
 93: /*
 94:  *  isa_interrupt_assert():
 95:  *
 96:  *  Called whenever an ISA device asserts an interrupt (0..15).
 97:  */
 98: void isa_interrupt_assert(struct interrupt *interrupt)
 99: {
100: 	struct bus_isa_data *d = (struct bus_isa_data *) interrupt->extra;
101: 	int old_isa_assert, line = interrupt->line;
102: 	int mask = 1 << (line & 7);
103: 
104: 	old_isa_assert = d->pic1->irr & ~d->pic1->ier;
105: 
106: 	if (line < 8)
107: 		d->pic1->irr |= mask;
108: 	else if (d->pic2 != NULL)
109: 		d->pic2->irr |= mask;
110: 
111: 	isa_interrupt_common(d, old_isa_assert);
112: }
113: 
114: 
115: /*
116:  *  isa_interrupt_deassert():
117:  *
118:  *  Called whenever an ISA device deasserts an interrupt (0..15).
119:  */
120: void isa_interrupt_deassert(struct interrupt *interrupt)
121: {
122: 	struct bus_isa_data *d = (struct bus_isa_data *) interrupt->extra;
123: 	int line = interrupt->line, mask = 1 << (line & 7);
124: 	int old_irr1 = d->pic1->irr, old_isa_assert;
125: 
126: 	old_isa_assert = old_irr1 & ~d->pic1->ier;
127: 
128: 	if (line < 8)
129: 		d->pic1->irr &= ~mask;
130: 	else if (d->pic2 != NULL)
131: 		d->pic2->irr &= ~mask;
132: 
133: 	/*  If IRQ 0 has been cleared, then this is a timer interrupt.
134: 	    Let's ack it here:  */
135: 	if (old_irr1 & 1 && !(d->pic1->irr & 1) &&
136: 	    d->ptr_to_pending_timer_interrupts != NULL &&
137:             (*d->ptr_to_pending_timer_interrupts) > 0)
138:                 (*d->ptr_to_pending_timer_interrupts) --;
139: 
140: 	isa_interrupt_common(d, old_isa_assert);
141: }
```

The helper's recompute (section 3, `pic8259_acknowledge`): `if (d->irr & ~d->ier) INTERRUPT_ASSERT(d->irq); else
INTERRUPT_DEASSERT(d->irq);` -- for pic1 `d->irq` is the bus's CPU-side line, for pic2 it is ISA line 2 (`bus_isa_init` adds the slave as
`"8259 irq=%s.isa.2 addr=..."`, `bus_isa.c:232`).  The walk, lines 8 and 9 pending on pic2 (pic2.irr 0x03), the GT read: master
acknowledge takes line 2 (pic1 IRR bit 2 cleared, ISR bit 2 set; pic1's unmasked set now empty -> DEASSERT the CPU line);
slave acknowledge takes line 8 (pic2 IRR 0x02, ISR 0x01); `0x02 & ~ier` non-zero -> ASSERT pic2's irq = `isa_interrupt_assert`
(line 2): `old_isa_assert` sampled with bit 2 CLEAR, `pic1->irr |= 0x04`, `isa_interrupt_common` re-folds bit 2 from pic2's
unmasked set (still 0x02), `new_isa_assert` = bit 2 != old -> the scan skips x == 2, finds x = 9 -> `last_int = 9`, ASSERT
the CPU line.  Nothing is stranded; the CPU line is low only between the two acknowledges inside one `lw`.
**RULING: CHECKED, no stall.**  **Packet-fed seats: settle it from the inlined code, or name the line that breaks the walk.**

**D5 -- THE RETIRE GUARD'S CONJUNCTS.**  GLM Q12: dropping `d == p->pic1` or `n == 0` from the retire guard is observable
only through a race, so no deterministic row exists; the main loop DISCLOSED both cells under clause (e).  The counter-
argument the floor invites: the guard DOMINATES the retire and its operands are body-tested partitions (pic1 vs pic2; line 0
vs other), so the cells are floor cells and a row is owed.  The main loop's derivation of why no deterministic row exists: a
wrong extra decrement is visible only if the count is >= 2 when the wrong acknowledge lands (count 1 -> 0 has the same
visible effect as the right acknowledge's own retirement), and the count reaches 2 only by two host-timer fires with no
acknowledge between them -- a wall-clock condition the probe cannot make deterministic (the carrier's host-timer rule).
**RULING: disclosed, not rowed.**  **Question for the seats:** is there a deterministic construction I have missed -- e.g. a
counter programmed at a rate where the count is >= 2 within the three-wait budget on any host -- or is a band row (count
>= 2 reached by waiting long enough) acceptable under the rate row's own precedent?

## 7. WHAT IS STILL OWED, and where the main loop may be fooling itself

* **The table of record** is inlined in section 4; escapes beyond the two PRETABLE.out disclosed: **none**.  If
  that is not "none", the ruling in D1 is provisional and the repair chain (one pass per floor-bound diff, closing on the
  first pass with zero breaches) applies to the instrument, not to the fix.
* **Argon** (pass 1, F2 A/B, pass 2 Q12/Q34, this pass A/B) is queued behind the single web-route sender; every one of its
  answers lands by the late-dissent rule when it arrives.  **Fable** is HELD with its question.  **agy** is walled.
* **Clause-(e) debts, disclosed not rowed:** `D_gt_write` (no row writes the IACK register); `D_fold`'s CPU-line observable
  (the owed `i8259cascline` row: two slave sources pending, the CPU line read through the handler); the retire guard's two
  conjuncts (D5); the helper's recompute replaced by a bare DEASSERT (F14).
* **Filed, not this round:** `pit8253pendingptr` (MED: `bus_isa_init` snapshots the pointer before the 8253 publishes it;
  the fix reads the machine field at call time, which is why it does not depend on that row), `pit8253count0`,
  `i8259ocw2nonspec`, `algorisaintclear`, `i8259ltim`, `i8259priority`, `i8259aeoi`, `i8259icwreset`, `i8259cascline`;
  `i8259isrnever` NARROWS; `8259cmdhalt` gains a reachability note.  Cobalt (F8) is disclosed, not measured.
* **The landing is NOT done**: nothing is committed; the probe sits in the working tree (`regress/i8259_eoi_probe.py`,
  md5 4b3e475d == the frozen copy in `fixlegs_090053/`), `gate_hygiene.sh` carries `EXPECT_PTY_PROBES 79 -> 80` and the
  probe grandfathered as promptless -- that pin counts the tree AS IT LIES (one untracked probe of another session is
  included, exactly as HEAD's 79 already included it; the committed count after this landing is 79).  The gate block for
  `gate_arm.sh` is DERIVED from the banked fix leg (84 named rows, four denominators pinned by equality); the probe costs
  about three minutes per leg in the weekly battery (three long-wait sessions and the rate session).
* **Where I may be fooling myself:** (i) every number in section 4 was read from an artifact, but the SENTENCES around them
  are mine -- a wrong sentence next to a right number is this project's commonest records defect; (ii) D4's walk is a
  reading, not a measurement: no row drives two slave sources through the handler (that is the owed `i8259cascline` row);
  (iii) D3 rests on Grok's reading of three Linux files, which the main loop did not re-fetch today; (iv) the v2c and v2d
  tables agree on the twelve mutants they share only if the v2d SCORES says so -- read it, do not assume it.

## 8. The three questions

1. Adjudicate F1..F21 and D1..D5 -- UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.  On D1
   (Astra: your own grounds), D2, D3 and D5 answer the QUESTIONS posed there explicitly.
2. WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?  Of twenty-one findings I overturned NONE (ten accepted without a product
   edit, two repaired, five disclosed or filed, four records corrected) and ruled all five disagreements my own way, one
   against the adjudicating seat.  Name the count you overturn.
3. WHAT DID ALL OF US MISS?  You now have the whole panel's pass-2 output, the diff, the 84 rows, the floor legs and the
   finished table of record.  In particular: is there an edit to the diff that passes all 84 rows AND all sixteen mutants'
   scores and still changes what a malta guest sees (the kind of escape a clean table hides)?  And: the `D_gt_nocasc` kill
   came through a both-columns row reported as CONTROL FAIL -- is the probe's control/symptom classification hiding a
   coverage gap anywhere else?

## 9. Answer format

~~~~
VERDICT: RATIFY | RATIFY WITH CHANGES | NOT RATIFY -- <one line>
WRONG: <F/D numbers, or "none">
~~~~
Then Q1, Q2, Q3 in order; mark claims READ / DERIVED / NOT CHECKABLE, with the single file or fact that would settle anything
you cannot.  Keep hidden reasoning short; put the answer in the response.
