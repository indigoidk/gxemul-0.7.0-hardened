# pcc2c040assertrow -- the held REVIEW stage, re-fired on the REAL material (owner decision 2026-09-18)

Open your answer with ONE verdict line:
`VERDICT: CLOSED (no escape found -- name the edits you checked) / ROW OWED (<the edit>, <the row>) / NOT CHECKABLE (<why>)`

**Please do not simply ratify.**  On 2026-09-17 this stage's packet gave you the device's stale comment instead of the
detector, and three of you still named the right mutant from it.  This packet carries the detector itself: the shipped
code, the 13-row instrument's output and four measured mutant tables, below, verbatim.  You cannot read files; every
fact you need is here.  If a premise cannot be settled from this packet, say so in a line of its own starting
`NOT CHECKABLE:` rather than guessing.

## THE ONE QUESTION

Round #512 de-fatalised the C040 arm of `reassert_interrupts()` in `dev_pcc2.c` (an MVME187 interrupt controller) into
`assert = 0;` (decline to assert, announce once).  Its detector is `regress/pcc2_c040_probe.py`, 13 rows on the
unmodified `-E mvme88k -e mvme187` machine; the four rows `irq pending`, `irq live`, `c040 noassert`, `c040 noassert2`
were added so a FREE-RUNNING guest observes interrupt DELIVERY (single-stepping suppresses delivery by design).

**Is there a ONE-TOKEN edit of the shipped lines 369-381 below that passes all 13 rows?**  For each candidate you
consider, say which row (if any) goes red and why, from the rows' got/want values below.  If you find one that every row
passes, name the guest-visible behaviour it changes and the smallest row that would see it.  The two mutants the
2026-09-17 panel named -- deleting `assert = 0;`, and `assert = 0;` -> `return;` -- are in the tables: check whether the
row that killed them is still in the shipped 13 (`M_return.raw` ran when the instrument had 10 rows).

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


## THE MEASUREMENTS (preserved at regress/artifacts/pcc2c040kill/killtable_20260908/, quoted verbatim)

### THE SHIPPED 13-ROW INSTRUMENT ON THE FIX (base)

```
pcc2_c040_probe -- binary=/tmp/gx512/gxemul label=BASE4 machine=mvme88k/mvme187
row            got                    want                   note                                               
genctl ctl       alive        alive        CONTROL: same st.b, same GENCTL, benign value -- must survive ok
genctl ctlq      no           no           CONTROL: the benign write must NOT reach the C040 arm ok
c040 kill        alive        alive        one legal guest st.b of 0x04 to GENCTL must NOT end the host ok
c040 attrib      yes          yes          ATTRIBUTION: a death here must carry the C040 arm's unique diagnostic ok
  EVIDENCE: [ pcc2: C040 (MC68040 EIPL) interrupt delivery not implemented; assertion suppressed  (once) ]
c040 says        yes          yes          the decline must ANNOUNCE -- a silent decline is a different disposition ok
c040 once        1            1            TWO C040 writes must announce EXACTLY ONCE -- the (once) latch, not just presence ok
c040 predirty    yes          yes          a DIFFERENT warned bit set first must not silence the C040 announce (bit-collision mutant) ok
irq pending      0x33         0x33         LIVENESS: the clmpcc IER store must set SCCTX's INT bit -- without this the pair is vacuous ok
irq live         0x8          0x8          POSITIVE CONTROL: C040 CLEAR, line asserted -- the interrupt vector MUST be reached ok
c040 noassert    0x10020      0x10020      C040 SET on an ALREADY-ASSERTED line: must reach completion, NOT the interrupt vector ok
c040 noassert2   0x10024      0x10024      the SECOND C040 encounter, latch already set, must ALSO suppress -- the encounter axis ok
c040 recover     0x8          0x8          C040 CLEARED after the latch fired: assertion must RESUME -- the fourth product cell ok
c040 genctl      0x06         0x06         GENCTL must read back MIEN|C040: suppression by clobbering MIEN would pass every other row ok

PCC2C040_RESULT=13/13
PCC2C040_WITNESS=PASS
PCC2C040_DONE
```

### MUTANT: the `assert = 0;` line deleted (the clause-(d) null repair) -- run on the 10-row stage

```
pcc2_c040_probe -- binary=/tmp/gx512/gxemul label=M_d1_noassert machine=mvme88k/mvme187
row            got                    want                   note                                               
genctl ctl       alive        alive        CONTROL: same st.b, same GENCTL, benign value -- must survive ok
genctl ctlq      no           no           CONTROL: the benign write must NOT reach the C040 arm ok
c040 kill        alive        alive        one legal guest st.b of 0x04 to GENCTL must NOT end the host ok
c040 attrib      yes          yes          ATTRIBUTION: a death here must carry the C040 arm's unique diagnostic ok
  EVIDENCE: [ pcc2: C040 (MC68040 EIPL) interrupt delivery not implemented; assertion suppressed  (once) ]
c040 says        yes          yes          the decline must ANNOUNCE -- a silent decline is a different disposition ok
c040 once        1            1            TWO C040 writes must announce EXACTLY ONCE -- the (once) latch, not just presence ok
c040 predirty    yes          yes          a DIFFERENT warned bit set first must not silence the C040 announce (bit-collision mutant) ok
irq pending      0x33         0x33         LIVENESS: the clmpcc IER store must set SCCTX's INT bit -- without this the pair is vacuous ok
irq live         0x8          0x8          POSITIVE CONTROL: C040 CLEAR, line asserted -- the interrupt vector MUST be reached ok
c040 noassert    0x8          0x1001c      C040 SET on an ALREADY-ASSERTED line: must reach completion, NOT the interrupt vector FAIL

PCC2C040_RESULT=9/10
PCC2C040_WITNESS=FAIL
PCC2C040_DONE
```

### MUTANT: `assert = 0;` -> `return;` (skips INTERRUPT_DEASSERT) -- run on the 10-row stage

```
pcc2_c040_probe -- binary=/tmp/gx512/gxemul label=M_return machine=mvme88k/mvme187
row            got                    want                   note                                               
genctl ctl       alive        alive        CONTROL: same st.b, same GENCTL, benign value -- must survive ok
genctl ctlq      no           no           CONTROL: the benign write must NOT reach the C040 arm ok
c040 kill        alive        alive        one legal guest st.b of 0x04 to GENCTL must NOT end the host ok
c040 attrib      yes          yes          ATTRIBUTION: a death here must carry the C040 arm's unique diagnostic ok
  EVIDENCE: [ pcc2: C040 (MC68040 EIPL) interrupt delivery not implemented; assertion suppressed  (once) ]
c040 says        yes          yes          the decline must ANNOUNCE -- a silent decline is a different disposition ok
c040 once        1            1            TWO C040 writes must announce EXACTLY ONCE -- the (once) latch, not just presence ok
c040 predirty    yes          yes          a DIFFERENT warned bit set first must not silence the C040 announce (bit-collision mutant) ok
irq pending      0x33         0x33         LIVENESS: the clmpcc IER store must set SCCTX's INT bit -- without this the pair is vacuous ok
irq live         0x8          0x8          POSITIVE CONTROL: C040 CLEAR, line asserted -- the interrupt vector MUST be reached ok
c040 noassert    0x8          0x1001c      C040 SET on an ALREADY-ASSERTED line: must reach completion, NOT the interrupt vector FAIL

PCC2C040_RESULT=9/10
PCC2C040_WITNESS=FAIL
PCC2C040_DONE
```

### MUTANT: suppress by clearing MIEN in GENCTL instead -- run on the 13-row instrument

```
pcc2_c040_probe -- binary=/tmp/gx512/gxemul label=M_mienclobber machine=mvme88k/mvme187
row            got                    want                   note                                               
genctl ctl       alive        alive        CONTROL: same st.b, same GENCTL, benign value -- must survive ok
genctl ctlq      no           no           CONTROL: the benign write must NOT reach the C040 arm ok
c040 kill        alive        alive        one legal guest st.b of 0x04 to GENCTL must NOT end the host ok
c040 attrib      yes          yes          ATTRIBUTION: a death here must carry the C040 arm's unique diagnostic ok
  EVIDENCE: [ pcc2: C040 (MC68040 EIPL) interrupt delivery not implemented; assertion suppressed  (once) ]
c040 says        yes          yes          the decline must ANNOUNCE -- a silent decline is a different disposition ok
c040 once        1            1            TWO C040 writes must announce EXACTLY ONCE -- the (once) latch, not just presence ok
c040 predirty    yes          yes          a DIFFERENT warned bit set first must not silence the C040 announce (bit-collision mutant) ok
irq pending      0x33         0x33         LIVENESS: the clmpcc IER store must set SCCTX's INT bit -- without this the pair is vacuous ok
irq live         0x8          0x8          POSITIVE CONTROL: C040 CLEAR, line asserted -- the interrupt vector MUST be reached ok
c040 noassert    0x10020      0x10020      C040 SET on an ALREADY-ASSERTED line: must reach completion, NOT the interrupt vector ok
c040 noassert2   0x10024      0x10024      the SECOND C040 encounter, latch already set, must ALSO suppress -- the encounter axis ok
c040 recover     0x8          0x8          C040 CLEARED after the latch fired: assertion must RESUME -- the fourth product cell ok
c040 genctl      0x04         0x06         GENCTL must read back MIEN|C040: suppression by clobbering MIEN would pass every other row FAIL

PCC2C040_RESULT=12/13
PCC2C040_WITNESS=FAIL
PCC2C040_DONE
```

### MUTANT: the suppression made sticky once the latch fires -- run on the 12-row stage

```
pcc2_c040_probe -- binary=/tmp/gx512/gxemul label=M_sticky machine=mvme88k/mvme187
row            got                    want                   note                                               
genctl ctl       alive        alive        CONTROL: same st.b, same GENCTL, benign value -- must survive ok
genctl ctlq      no           no           CONTROL: the benign write must NOT reach the C040 arm ok
c040 kill        alive        alive        one legal guest st.b of 0x04 to GENCTL must NOT end the host ok
c040 attrib      yes          yes          ATTRIBUTION: a death here must carry the C040 arm's unique diagnostic ok
  EVIDENCE: [ pcc2: C040 (MC68040 EIPL) interrupt delivery not implemented; assertion suppressed  (once) ]
c040 says        yes          yes          the decline must ANNOUNCE -- a silent decline is a different disposition ok
c040 once        1            1            TWO C040 writes must announce EXACTLY ONCE -- the (once) latch, not just presence ok
c040 predirty    yes          yes          a DIFFERENT warned bit set first must not silence the C040 announce (bit-collision mutant) ok
irq pending      0x33         0x33         LIVENESS: the clmpcc IER store must set SCCTX's INT bit -- without this the pair is vacuous ok
irq live         0x8          0x8          POSITIVE CONTROL: C040 CLEAR, line asserted -- the interrupt vector MUST be reached ok
c040 noassert    0x1001c      0x1001c      C040 SET on an ALREADY-ASSERTED line: must reach completion, NOT the interrupt vector ok
c040 noassert2   0x10020      0x10020      the SECOND C040 encounter, latch already set, must ALSO suppress -- the encounter axis ok
c040 recover     0x10020      0x8          C040 CLEARED after the latch fired: assertion must RESUME -- the fourth product cell FAIL

PCC2C040_RESULT=11/12
PCC2C040_WITNESS=FAIL
PCC2C040_DONE
```

## WHAT A GOOD ANSWER LOOKS LIKE

The verdict line; then the edits you enumerated (the operator or constant changed, the line), each with the row that
reds or `ESCAPES`; then any `NOT CHECKABLE:` lines.  An answer that only agrees is the least useful one.
