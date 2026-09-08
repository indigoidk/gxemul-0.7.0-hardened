# pcc2c040assertrow -- DESIGN REVIEW BEFORE BUILDING.  An in-round L2 repair.

**PLEASE DO NOT RATIFY.**  This row exists because I gave it a WRONG REASON twice: first that its
observation channel was invisible (false -- it prints while stepping), then that its required state
was unreachable (false -- another device's store creates it).  **The conclusion "no row today" was
right both times and neither reason was.**  So attack the reasoning below, not just the code.

**Tree under review: `GXEMUL-SEC/src/`.**

---

## 1.  WHY THE ROW IS OWED

Round `#512` de-fatalised a host kill in `reassert_interrupts()` and shipped a 7-row detector.  A
kill table measured **one clause-(d) escape**: removing the repair's effect (`assert = 0`) scores
**7/7**.  A pass-2 seat then found a **one-token** variant that also scores 7/7 --
`assert = 0;` -> `return;` -- and ruled that grading the escape (d) while filing the repair is *"the
(e) remedy applied to a (d) grade"*, so the round does not close until this row exists.

## 2.  THE SHIPPED CODE UNDER TEST, verbatim

```c
 325| 	}
 326| 
 327| 	/*  TODO: Other interrupt sources.  */
 328| 
 329| 	/*  Assert interrupt on the CPU if the IPL is higher than the mask:  */
 330| 	if ((d->pcctwo_reg[PCCTWO_IPL] & INTERRUPT_LEVEL_MASK) >
 331| 	    (d->pcctwo_reg[PCCTWO_MASK] & INTERRUPT_LEVEL_MASK))
 332| 		assert = 1;
 333| 
 334| 	debug("[ pcc2: IPL = %i, MASK = %i => %s ]\n", d->pcctwo_reg[PCCTWO_IPL]& INTERRUPT_LEVEL_MASK,
 335| 		d->pcctwo_reg[PCCTWO_MASK] & INTERRUPT_LEVEL_MASK,
 336| 		assert ? "ASSERT" : "no assert");
 337| 
 338| 	/*  ... but only allow interrupts if Master Interrupt Enable is on:  */
 339| 	if (!(d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_MIEN))
 340| 		assert = 0;
 341| 
 342| 	/*  #512: ... and not while C040 selects a delivery pin this model does not
 343| 	    have.  This was a fatal()+exit(1) at the TOP of this function, and
 344| 	    reassert_interrupts() is called from ten sites -- the GENCTL write arm
 345| 	    calls it in the SAME access -- so ONE legal guest `st.b' of 0x04 to
 346| 	    GENCTL ended the host, with no driver and no interrupt involved
 347| 	    (witness: regress/pcc2_c040_probe.py).
 348| 
 349| 	    DECLINING TO ASSERT, rather than returning, is what the MIEN test above
 350| 	    already does for the other GENCTL interrupt-control bit.  A `return' AT
 351| 	    THIS SITE would skip only the INTERRUPT_DEASSERT below -- the IPL
 352| 	    recalculation and the cur_int_vec[] updates have already run by here.
 353| 	    (It is a return at the OLD site, above the recalculation, that would skip
 354| 	    all three; an earlier draft of this comment attached that reason to this
 355| 	    placement, which is a wrong reason for a right position, and a wrong
 356| 	    reason gets reused -- `assert = 0' -> `return' at THIS line is a
 357| 	    one-token mutant every shipped row passes.)
 358| 
 359| 	    VMESBCP2 (the MVME187 board manual) settles the shape in two places.
 360| 	    The General Control Register page ($FFF42002) puts C040 at bit 10 of the
 361| 	    word view -- 0x04, matching this fork's header -- and says a set C040
 362| 	    sends the request "via the EIPL* pins at the level that is programmed
 363| 	    ... in the SCSI Interrupt Control Register"; the Interrupt Priority
 364| 	    Level Register page adds that IPL2-IPL0 "always reflect the encoded
 365| 	    request level".  So C040 selects the DELIVERY PIN and not the level,
 366| 	    which is why the recalculation above must stay.  MIEN, by contrast,
 367| 	    disables "both the EIPL* pins and the INT pin" -- so the two tests are
 368| 	    siblings gating one output, not a nest.  */
 369| 	if (d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_C040) {
 370| 		if (!(d->warned & (1u << PCC2_W_C040))) {
 371| 			d->warned |= (1u << PCC2_W_C040);
 372| 			fatal("[ pcc2: C040 (MC68040 EIPL) interrupt delivery not "
 373| 			    "implemented; assertion suppressed  (once) ]\n");
 374| 		}
 375| 		assert = 0;
 376| 	}
 377| 
 378| 	if (assert)
 379| 		INTERRUPT_ASSERT(d->cpu_irq);
 380| 	else
 381| 		INTERRUPT_DEASSERT(d->cpu_irq);
```

## 3.  ESTABLISHED FACTS (each verified in source on this machine)

* **The only difference between fix and mutant is `INTERRUPT_ASSERT` vs `INTERRUPT_DEASSERT` on
  `d->cpu_irq`.**  `cpu->cd.m88k.irq_asserted` is a HOST-side field with no guest-readable
  reflection, so the only guest-visible consequence is DELIVERY.
* **The `debug("[ pcc2: IPL = %i, MASK = %i => %s ]")` line CANNOT be the oracle**: it executes
  BEFORE both the MIEN and C040 suppressions, so it prints the pre-suppression value and is green
  under the very mutant it would be chosen to catch.
* **A guest CANNOT set an ICR INT bit directly** -- `TxICR` keeps `idata & 0x17`, `SCCICR`/`SCCTX`
  keep `& 0x1f`, `SCCRX`/`SCSIICR` keep `& 0xdf`; `PCC2_IRQ_INT` is `0x20`.
* **But a guest CAN cause one, synchronously, from a DIFFERENT device.**
  `pcctwo_interrupt_common()` ORs `PCC2_IRQ_INT` onto SCCTX/SCCRX/SCSIICR when those lines assert,
  and `dev_clmpcc.c:88-89` does `if ((d->reg[CLMPCC_REG_IER] & 3) != 0) INTERRUPT_ASSERT(d->irq_scc_tx);`
  inside the guest's own store.  `machine_mvme88k.c` constructs clmpcc at `0xfff45000` with its irq
  wired to pcc2.  **So the state is reachable while single-stepping.**
* **DELIVERY still needs FREE-RUNNING**: `cpu_dyntrans.c` suppresses interrupt dispatch while
  single-stepping by design (*"Do not cause interrupts while single-stepping"*).
* **The probe's `session()` ALREADY supports free-running** -- its `(cmd, wait, until)` tuple form
  exists so *"`continue` waits for its breakpoint"*, and it reports `how = "no-breakpoint"` when the
  `until` text never arrives.

**Constants, all taken from working in-tree code rather than derived:**

    PCC2 base 0xfff42000   PCCTWO_GENCTL 0x02   PCCTWO_SCCTX 0x1e
    clmpcc base 0xfff45000   CLMPCC_REG_IER 0x11
    PCC2_C040 0x04   PCC2_MIEN 0x02   PCC2_IRQ_IEN 0x10   PCC2_IRQ_IPL 0x07
    STCR_R5_CR1 0x80058025 (stcr r5,cr1)   PSR_INDCLR 0x80000000 (MODE only, IND CLEAR)
    SELF 0xc0000000 (br .)   m88k EXCEPTION_INTERRUPT = 1, so the vector entry is 8*1 = 0x8

## 4.  THE PROPOSED TWO ROWS

Both plant `br .` at `0x8`, `breakpoint add 0x8`, then `("continue", grace, <prompt token>)`.

* **`irq live` -- THE POSITIVE CONTROL.**  `stcr` PSR = `0x80000000` (IND clear, interrupts on);
  `st.b` `IEN|3` to SCCTX; `st.b` to clmpcc IER; `st.b` **`0x02` (MIEN only, C040 CLEAR)** to
  GENCTL.  **The breakpoint MUST fire.**  Without this row, "no breakpoint" is indistinguishable
  from "my setup never created a pending interrupt", which is the vacuity shape in its purest form.
* **`c040 noassert` -- THE DEFECT ROW.**  Identical, except GENCTL = **`0x06` (MIEN|C040)**.  The
  breakpoint must NOT fire (`how == "no-breakpoint"`).  Under `assert = 0` removed, or under
  `assert = 0` -> `return`, the line stays asserted and the breakpoint FIRES.

## 5.  QUESTIONS

**Q1.  Will the positive control actually fire?**  Specifically: is `PSR = 0x80000000` sufficient to
enable interrupt delivery on this CPU, is the vector base really 0 (VBR at reset), is `8 * 1 = 0x8`
the right entry, and does `IEN|3` in SCCTX plus an IER write really drive
`pcctwo_interrupt_common` -> INT -> `IPL > MASK`?  **MASK resets to 0 -- is IL 3 above it?**

**Q2.  What mutants still escape these two rows?**  I expect at least: a fix that suppresses
delivery by some route other than `assert` (so the rows pass while the code is wrong for a different
reason), and anything that makes the CONTROL fail in the same way as the defect row -- which would
read as a green pair.

**Q3.  PREMISE AUDIT.**  Which fact in section 3 is wrong?  I have already been wrong twice on this
exact question, in opposite directions, so treat section 3 as the most suspect part of this brief.

**Verdict line first** -- BUILD-AS-PROPOSED / BUILD-WITH-REVISIONS / REFUSE -- then the body.  **A
verdict that merely agrees is the least useful reply.**
