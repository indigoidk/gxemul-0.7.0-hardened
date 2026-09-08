# `#512` L2 repair -- PASS 2.  A repair made in response to a pass 2 owes its own pass.

**PLEASE DO NOT RATIFY.**  Pass 2 on the original diff refused this round's closing disposition and
was RIGHT.  A design review then found that my FIRST version of these rows **would have passed the
very mutant they exist to catch**.  So the prior on this material is bad, and the useful reply is
the next defect, not agreement.

**Tree under review: `GXEMUL-SEC/`.**

---

## 1.  WHAT THIS REPAIR IS

`#512` de-fatalised a host kill in `reassert_interrupts()`.  Its 7-row detector was measured with a
**clause-(d) floor breach**: removing the repair's effect scored 7/7.  Pass 2 ruled that grading (d)
while FILING the repair is *"the (e) remedy applied to a (d) grade"*, so the round could not close.

**This diff is the in-round repair: four rows added to `regress/pcc2_c040_probe.py`.  NO PRODUCT
CODE CHANGED.**

## 2.  THE ADDED ROWS, verbatim

```python
 351| #  #512 L2 REPAIR -- the non-suppressing mutant, which the seven rows above CANNOT see.
 352| #
 353| #  MEASURED: removing `assert = 0' scores 7/7 (killtable_20260907/M_d1_noassert.raw), and a pass-2
 354| #  seat named a ONE-TOKEN variant, `assert = 0;' -> `return;', that also scores 7/7.
 355| #
 356| #  *** THE DESIGN BELOW IS A REVISION.  MY FIRST ONE WOULD HAVE PASSED THE `return' MUTANT. ***
 357| #  The codex design review (artifacts/pcc2c040kill/codex_assertrow_20260908.txt) found why:
 358| #
 359| #      GENCTL resets to ZERO, so MIEN is clear through the setup and every recalculation DEASSERTS
 360| #      the CPU line.  At the final write the repair deasserts (no interrupt), deleting `assert = 0'
 361| #      asserts (caught) -- but `return' LEAVES THE ALREADY-DEASSERTED LINE UNCHANGED, so it also
 362| #      shows no interrupt and PASSES.  *"Deleting the assignment permits assertion; returning
 363| #      preserves the incoming line state."*
 364| #
 365| #  THE FIX IS A PRECONDITION, NOT AN ORACLE: both rows write MIEN-ONLY GENCTL FIRST, so the line is
 366| #  ALREADY ASSERTED before the operation under test.  Then `return' leaves it asserted and reddens.
 367| #
 368| #  AND THE OBVIOUS ORACLE IS A CHECK THAT CANNOT FAIL: rd() tests `until in buf' against the WHOLE
 369| #  accumulated transcript, and the settle drain has already buffered a `GXemul>' prompt -- so
 370| #  ("continue", grace, "GXemul>") returns True with ZERO READS.  `how == "no-breakpoint"' is no
 371| #  better: it proves a MISSING TOKEN, not execution-without-delivery, and a hang satisfies it.
 372| #  So BOTH rows stop at a breakpoint and the discriminator is WHICH PC, never a timeout.
 373| #  ================================================================================================
 374| 
 375| IRQ_ENTRY = 0x8        #  m88k EXCEPTION_INTERRUPT is vector 1; entry = VBR + 8*vector, and VBR is
 376|                        #  0 because mvmeprom.c EXPLICITLY sets it -- not an assumed reset value.
 377| STCR_R5_CR1 = 0x80058025   #  stcr r5,cr1 -- copied from m88k_exc_probe.py and decoder-checked by
 378|                            #  the review, NOT hand-assembled (the encoding trap this project records)
 379| PSR_INDCLR = 0x80000000    #  MODE only, IND CLEAR: dispatch needs `irq_asserted && !(PSR & IND)'
 380| CLMPCC = 0xfff45000
 381| CLMPCC_IER = 0x11
 382| SCCTX_ARM = 0x13       #  PCC2_IRQ_IEN | level 3.  The device ORs in INT (0x20) -> 0x33; MASK
 383|                        #  resets to 0, so IPL 3 wins the comparison.
 384| IER_ON = 0x03          #  clmpcc asserts SCC TX when (IER & 3) != 0
 385| 
 386| 
 387| def ST_B7(rs, off):    #  store via r7 (the clmpcc base); ST_B is hardwired to r2 (PCC2)
 388|     return enc(0x0b, rs, 7, off)
 389| 
 390| 
 391| def assert_row(label, final_genctl, repeat=1):
 392|     #  Setup runs under `step' -- dispatch is suppressed while single-stepping BY DESIGN, so the
 393|     #  line can be armed without the interrupt being taken early.
 394|     insns = [
 395|         STCR_R5_CR1,               # 0  PSR: interrupts enabled
 396|         ST_B(6, SCCTX),            # 1  SCCTX = 0x13   (IEN | level 3)
 397|         ST_B7(8, CLMPCC_IER),      # 2  clmpcc IER -> INTERRUPT_ASSERT(irq_scc_tx), synchronous
 398|         LD_BU(11, SCCTX),          # 3  read back: must be 0x33, proving INT arrived
 399|         ST_B(9, GENCTL),           # 4  MIEN only -- THE PRECONDITION: the line is now ASSERTED
 400|     ] + [ST_B(10, GENCTL)] * repeat  # 5..  the operation under test, ONCE or TWICE
 401| 
 402|     #  6 is a harmless RAM store (I_ST_SCR = st r5,r3,0, already defined by the scaffolding) purely
 403|     #  so the COMPLETION breakpoint at 7 is an address the guest ARRIVES AT rather than one it is
 404|     #  already sitting on after `step'.  Do NOT hand-assemble an instruction here: `enc()' builds
 405|     #  the IMMEDIATE form, and a triadic register op needs a different encoder.
 406|     words = insns + [I_ST_SCR, I_BR_SELF, 0]     # harmless, then br . = COMPLETION
 407|     #  DERIVED, never hardcoded: `repeat' changes the instruction count, and a stale literal here
 408|     #  would put the completion breakpoint on the wrong word and make the row unfalsifiable.
 409|     completion = CODE + 4 * (len(insns) + 1)
 410|     cmds = ["put w 0x%x, 0x%08x" % (CODE + 4 * i, w) for i, w in enumerate(words)]
 411|     cmds += ["put w 0x%x, 0x%08x" % (IRQ_ENTRY, I_BR_SELF)]     # the vector spins, not zeros
 412|     cmds += ["r2=0x%x" % PCC2, "r5=0x%x" % PSR_INDCLR, "r6=0x%x" % SCCTX_ARM,
 413|              "r7=0x%x" % CLMPCC, "r8=0x%x" % IER_ON, "r9=0x02",
 414|              "r10=0x%x" % final_genctl, "r11=0x0", "r12=0x0"]
 415|     cmds += ["breakpoint add 0x%x" % IRQ_ENTRY,
 416|              "breakpoint add 0x%x" % completion]
 417|     cmds += ["pc=0x%x" % CODE, "step %d" % len(insns),
 418|              ("continue", 6.0), "reg"]
 419|     t, alive, how = session(cmds, spin=2.0)
 420|     pcs = re.findall(r"pc\s*=\s*0x([0-9a-f]{8})", t)
 421|     r11 = re.findall(r"r11\s*=\s*0x([0-9a-f]+)", t)
 422|     return (t, alive, how, (int(pcs[-1], 16) if pcs else None),
 423|             (int(r11[-1], 16) if r11 else None), completion)
 424| 
 425| #  ---- LIVENESS + POSITIVE CONTROL: with C040 CLEAR the interrupt MUST be delivered -------------
 426| tc, alivec, howc, pcc, r11c, compc = assert_row("live", 0x02)
 427| 
 428| row("irq pending", ("0x%02x" % r11c) if r11c is not None else "no-readback", "0x33",
 429|     "LIVENESS: the clmpcc IER store must set SCCTX's INT bit -- without this the pair is vacuous")
 430| 
 431| row("irq live", ("0x%x" % pcc) if pcc is not None else "no-pc(%s)" % howc, "0x%x" % IRQ_ENTRY,
 432|     "POSITIVE CONTROL: C040 CLEAR, line asserted -- the interrupt vector MUST be reached")
 433| 
 434| #  ---- THE DEFECT ROW: same sequence, C040 SET -- delivery must be suppressed --------------------
 435| #  Affirmative negative evidence: it must REACH THE COMPLETION BREAKPOINT, not merely fail to
 436| #  reach the vector.  A timeout, an unexpected stop or a death is a FAILURE, never the answer.
 437| td, alived, howd, pcd, r11d, compd = assert_row("c040", 0x06)
 438| 
 439| row("c040 noassert", ("0x%x" % pcd) if pcd is not None else "no-pc(%s)" % howd,
 440|     "0x%x" % compd,
 441|     "C040 SET on an ALREADY-ASSERTED line: must reach completion, NOT the interrupt vector")
 442| 
 443| #  ---- THE SECOND ENCOUNTER.  This closes the ENCOUNTER axis rather than chasing one mutant. -----
 444| #  MEASURED: with only the row above, `assert = 0' moved INSIDE the latch scores 10/10
 445| #  (killtable_20260908/M_latchinside.raw).  It suppresses correctly on the FIRST C040 encounter --
 446| #  the latch is unset, so the body runs -- and skips the suppression on EVERY LATER ONE.  The codex
 447| #  pass-1 seat predicted exactly this: *"The first encounter suppresses correctly; later encounters
 448| #  can assert the CPU line.  The announcement count remains exactly one."*
 449| #
 450| #  The axis has two cells, FIRST and LATER, and the rows above held only the first.  A second
 451| #  identical C040 write closes it: under the shipped fix `assert = 0' is outside the latch and runs
 452| #  both times; under the mutant the second call leaves the line asserted and the interrupt lands.
 453| t2, alive2b, how2b, pc2b, r112b, comp2b = assert_row("c040x2", 0x06, repeat=2)
 454| 
 455| row("c040 noassert2", ("0x%x" % pc2b) if pc2b is not None else "no-pc(%s)" % how2b,
 456|     "0x%x" % comp2b,
 457|     "the SECOND C040 encounter, latch already set, must ALSO suppress -- the encounter axis")
 458| 

```

## 3.  THE MEASUREMENTS (scratch clone, artifacts preserved)

    BASE            11/11
    M_d1_noassert    9/10   `assert = 0' DELETED          -- WAS 7/7, a clean sweep   KILLED
    M_return         9/10   `assert = 0' -> `return;'     -- the pass-2 mutant        KILLED
    M_latchinside   10/11   `assert = 0' INSIDE the latch -- WAS 10/10                KILLED

**The first two redden `c040 noassert` (pc = 0x8, the interrupt vector).  The third reddens only
`c040 noassert2`** -- it suppresses correctly on the FIRST C040 encounter and skips suppression on
every later one, which is why the encounter axis needed closing rather than one more mutant-specific
row.

## 4.  THE DISPOSITIONS I ACCEPTED -- attack these

1. **Closed the ENCOUNTER AXIS with a repeated write** rather than adding a row per mutant, citing
   the class-closure rule.  **Is two cells (FIRST / LATER) the whole axis, or is there a third?**
2. **Made the negative case AFFIRMATIVE** -- both outcomes stop at a breakpoint and the
   discriminator is WHICH PC -- because a timeout oracle is satisfied by a hang, and because
   `rd()` matches `until` against the WHOLE accumulated buffer, so a prompt token returns True with
   zero reads.
3. **Kept `irq pending` and `irq live` as controls** on the grounds that without them "no interrupt"
   is indistinguishable from "no request was ever created".
4. **DERIVED the completion address** from the instruction count rather than hardcoding it, after
   `repeat` made a literal wrong.
5. **Declared the residual** rather than implying coverage: one source, one priority, two
   encounters; no recovery observation; no MASK/MIEN/pending-corruption coverage.

## 5.  QUESTIONS

**Q1 (LOAD-BEARING).  Which of the five dispositions is wrong?**  I accepted all five, and a round
that accepted everything has either had a good panel or stopped arguing.  **Be hardest on 1** -- an
axis I have declared closed is exactly the claim that gets reused.

**Q2.  What is the smallest edit to the SHIPPED FIX that still scores 11/11?**  The previous three
answers to this question were all real and all missed by me.  Consider: suppression that also
clears MASK or MIEN; suppression that never recovers when C040 is cleared; a guard reordered so
C040 is tested before MIEN.

**Q3.  Is the apparatus sound?**  Specifically: is `pc` after `reg` a trustworthy attribution of
WHICH breakpoint stopped the guest, given both are set in the same session?  And does anything in
the setup sequence perturb the state it is meant to establish -- in particular, does re-writing
GENCTL twice disturb the pending SCC TX request?

**Verdict line first** -- RATIFY / RATIFY-WITH-RESIDUALS / DO-NOT-SHIP -- then the body.
