# `pcc2c040kill` ASSESS STAGE -- the missing seats, by OWNER DECISION 2026-09-18 (a LATE assess of a SHIPPED round)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
The tree under review is `GXEMUL-SEC/src/`; ignore any other `src/`.  Everything needed is inlined.  **VERDICT LINE FIRST**
(REAL-AND-RIGHTLY-FIXED / REAL-BUT-MIS-FIXED / NOT-REAL).  The assess stage ran with three seats (codex, grok, fable5); the
owner ordered every missing seat fired.  The round has since SHIPPED as `9fa07fe` (#512) with a 16-row detector; a late agy
review of that detector is recorded separately.  Assess the DEFECT and the SHIPPED FIX against the code below.

## THE ROW (premises stated as questions -- check them)
"dev_pcc2.c: a LEGAL byte write to GENCTL with the C040 bit set ends the host in reassert_interrupts() -- the sibling kill
the width fix exposed rather than removed."
P1. Is a byte store to the PCC2 General Control register with the C040 bit set LEGAL guest behaviour (an MVME187
    driver may program it), so that ending the host was a defect and not a guard?
P2. Did the shipped fix keep the guest's C040 write, suppress interrupt ASSERTION while C040 is set (because the model has
    no 68040 EIPL path), and announce it once via a per-device latch bit -- and is that the right disposition, versus
    implementing EIPL delivery or declining the write?
P3. Is anything in the enclosing function still able to end the host on a guest-controlled value?

## THE SHIPPED FIX (git show --format= 9fa07fe -- src/devices/dev_pcc2.c)
```diff
diff --git a/src/devices/dev_pcc2.c b/src/devices/dev_pcc2.c
index 76245d2..adc6c60 100644
--- a/src/devices/dev_pcc2.c
+++ b/src/devices/dev_pcc2.c
@@ -129,6 +129,7 @@ enum {
 	PCC2_W_SCSIICR_LEN,
 	PCC2_W_IPL_LEN,		/*  was a #119 function-static: process-global  */
 	PCC2_W_MASK_LEN,	/*  was a #119 function-static: process-global  */
+	PCC2_W_C040,		/*  #512: not a _LEN -- the C040 delivery decline  */
 	PCC2_W_NBITS
 };
 
@@ -268,13 +269,10 @@ static void reassert_interrupts(struct pcc2_data *d)
 {
 	int assert = 0;
 
-	if (d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_C040) {
-		/*  The M68000 interrupt mechanism involves outputting
-		    interrupt level on pins EIPL<2..0>. Not implemented
-		    yet.  */
-		fatal("pcc2: C040 interrupt assertions... TODO\n");
-		exit(1);
-	}
+	/*  #512: the C040 test used to sit HERE and was a fatal()+exit(1), so one
+	    legal guest byte write of 0x04 to GENCTL ended the host.  It now lives
+	    beside the MIEN test at the foot of this function, where declining to
+	    assert does not skip the recalculation below.  */
 
 	/*
 	 *  Recalculate current interrupt level:
@@ -341,6 +339,42 @@ static void reassert_interrupts(struct pcc2_data *d)
 	if (!(d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_MIEN))
 		assert = 0;
 
+	/*  #512: ... and not while C040 selects a delivery pin this model does not
+	    have.  This was a fatal()+exit(1) at the TOP of this function, and
+	    reassert_interrupts() is called from ten sites -- the GENCTL write arm
+	    calls it in the SAME access -- so ONE legal guest `st.b' of 0x04 to
+	    GENCTL ended the host, with no driver and no interrupt involved
+	    (witness: regress/pcc2_c040_probe.py).
+
+	    DECLINING TO ASSERT, rather than returning, is what the MIEN test above
+	    already does for the other GENCTL interrupt-control bit.  A `return' AT
+	    THIS SITE would skip only the INTERRUPT_DEASSERT below -- the IPL
+	    recalculation and the cur_int_vec[] updates have already run by here.
+	    (It is a return at the OLD site, above the recalculation, that would skip
+	    all three; an earlier draft of this comment attached that reason to this
+	    placement, which is a wrong reason for a right position, and a wrong
+	    reason gets reused -- `assert = 0' -> `return' at THIS line is a
+	    one-token mutant every shipped row passes.)
+
+	    VMESBCP2 (the MVME187 board manual) settles the shape in two places.
+	    The General Control Register page ($FFF42002) puts C040 at bit 10 of the
+	    word view -- 0x04, matching this fork's header -- and says a set C040
+	    sends the request "via the EIPL* pins at the level that is programmed
+	    ... in the SCSI Interrupt Control Register"; the Interrupt Priority
+	    Level Register page adds that IPL2-IPL0 "always reflect the encoded
+	    request level".  So C040 selects the DELIVERY PIN and not the level,
+	    which is why the recalculation above must stay.  MIEN, by contrast,
+	    disables "both the EIPL* pins and the INT pin" -- so the two tests are
+	    siblings gating one output, not a nest.  */
+	if (d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_C040) {
+		if (!(d->warned & (1u << PCC2_W_C040))) {
+			d->warned |= (1u << PCC2_W_C040);
+			fatal("[ pcc2: C040 (MC68040 EIPL) interrupt delivery not "
+			    "implemented; assertion suppressed  (once) ]\n");
+		}
+		assert = 0;
+	}
+
 	if (assert)
 		INTERRUPT_ASSERT(d->cpu_irq);
 	else
```

## THE ENCLOSING FUNCTION AT HEAD (reassert_interrupts in src/devices/dev_pcc2.c)
```c
static void reassert_interrupts(struct pcc2_data *d)
{
	int assert = 0;

	/*  #512: the C040 test used to sit HERE and was a fatal()+exit(1), so one
	    legal guest byte write of 0x04 to GENCTL ended the host.  It now lives
	    beside the MIEN test at the foot of this function, where declining to
	    assert does not skip the recalculation below.  */

	/*
	 *  Recalculate current interrupt level:
	 */
	d->pcctwo_reg[PCCTWO_IPL] = 0;

	/*  Timer interrupts?  */
	if (d->pending_timer1_interrupts > 0 &&
	    d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_IEN)
		d->pcctwo_reg[PCCTWO_T1ICR] |= PCC2_TTIRQ_INT;
	if (d->pending_timer2_interrupts > 0 &&
	    d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_IEN)
		d->pcctwo_reg[PCCTWO_T2ICR] |= PCC2_TTIRQ_INT;

	if (d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_T1ICR] & PCC2_TTIRQ_IL;
		d->cur_int_vec[intlevel] = PCC2V_TIMER1;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}
	if (d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_T2ICR] & PCC2_TTIRQ_IL;
		d->cur_int_vec[intlevel] = PCC2V_TIMER2;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	if (d->pcctwo_reg[PCCTWO_SCCTX] & PCC2_IRQ_IEN &&
	    d->pcctwo_reg[PCCTWO_SCCTX] & PCC2_IRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_SCCTX] & PCC2_IRQ_IPL;
		d->cur_int_vec[intlevel] = PCC2V_SCC_TX;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	if (d->pcctwo_reg[PCCTWO_SCCRX] & PCC2_IRQ_IEN &&
	    d->pcctwo_reg[PCCTWO_SCCRX] & PCC2_IRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_SCCRX] & PCC2_IRQ_IPL;
		d->cur_int_vec[intlevel] = PCC2V_SCC_RX;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	if (d->pcctwo_reg[PCCTWO_SCSIICR] & PCC2_IRQ_IEN &&
	    d->pcctwo_reg[PCCTWO_SCSIICR] & PCC2_IRQ_INT) {
		int intlevel = d->pcctwo_reg[PCCTWO_SCSIICR] & PCC2_IRQ_IPL;
		d->cur_int_vec[intlevel] = PCC2V_SCSI;
		if (d->pcctwo_reg[PCCTWO_IPL] < intlevel)
			d->pcctwo_reg[PCCTWO_IPL] = intlevel;
	}

	/*  TODO: Other interrupt sources.  */

	/*  Assert interrupt on the CPU if the IPL is higher than the mask:  */
	if ((d->pcctwo_reg[PCCTWO_IPL] & INTERRUPT_LEVEL_MASK) >
	    (d->pcctwo_reg[PCCTWO_MASK] & INTERRUPT_LEVEL_MASK))
		assert = 1;

	debug("[ pcc2: IPL = %i, MASK = %i => %s ]\n", d->pcctwo_reg[PCCTWO_IPL]& INTERRUPT_LEVEL_MASK,
		d->pcctwo_reg[PCCTWO_MASK] & INTERRUPT_LEVEL_MASK,
		assert ? "ASSERT" : "no assert");

	/*  ... but only allow interrupts if Master Interrupt Enable is on:  */
	if (!(d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_MIEN))
		assert = 0;

	/*  #512: ... and not while C040 selects a delivery pin this model does not
	    have.  This was a fatal()+exit(1) at the TOP of this function, and
	    reassert_interrupts() is called from ten sites -- the GENCTL write arm
	    calls it in the SAME access -- so ONE legal guest `st.b' of 0x04 to
	    GENCTL ended the host, with no driver and no interrupt involved
	    (witness: regress/pcc2_c040_probe.py).

	    DECLINING TO ASSERT, rather than returning, is what the MIEN test above
	    already does for the other GENCTL interrupt-control bit.  A `return' AT
	    THIS SITE would skip only the INTERRUPT_DEASSERT below -- the IPL
	    recalculation and the cur_int_vec[] updates have already run by here.
	    (It is a return at the OLD site, above the recalculation, that would skip
	    all three; an earlier draft of this comment attached that reason to this
	    placement, which is a wrong reason for a right position, and a wrong
	    reason gets reused -- `assert = 0' -> `return' at THIS line is a
	    one-token mutant every shipped row passes.)

	    *** THAT LAST SENTENCE IS FALSE, AND IT WAS FALSE AS OF THE COMMIT THAT WROTE IT.
	    Corrected 2026-09-17 after the Opus 5 seat BUILT the mutant and scored it. ***

	    `assert = 0' -> `return' scores **14/16 -- KILLED**, by `c040 noassert' and
	    `c040 noassert2', which are two of the assert rows THIS SAME COMMIT added.  The
	    measurement is preserved at
	    regress/artifacts/pcc2c040kill/ctlq_20260909/repaired_M_return.raw and has read
	    RESULT=14/16 since 2026-09-09 -- the sentence has sat next to its own refutation
	    in this repo for nine days.

	    The TRUE statement is the narrower one: the `return' variant WAS an escape of the
	    seven PRE-REPAIR rows, and is KILLED by the assert rows the repair added.

	    *** AND THE IRONY IS THE LESSON: this paragraph's own subject is "a wrong reason
	    gets reused".  The wrong sentence was then reused -- by three packet-fed panel
	    seats on 2026-09-17, which re-derived it from this comment and could not build to
	    check it, and by the main loop, which filed a queue row on it.  A comment that
	    states a MEASURED-sounding negative owes its artifact path, exactly as a score
	    claim does. ***

	    VMESBCP2 (the MVME187 board manual) settles the shape in two places.
	    The General Control Register page ($FFF42002) puts C040 at bit 10 of the
	    word view -- 0x04, matching this fork's header -- and says a set C040
	    sends the request "via the EIPL* pins at the level that is programmed
	    ... in the SCSI Interrupt Control Register"; the Interrupt Priority
	    Level Register page adds that IPL2-IPL0 "always reflect the encoded
	    request level".  So C040 selects the DELIVERY PIN and not the level,
	    which is why the recalculation above must stay.  MIEN, by contrast,
	    disables "both the EIPL* pins and the INT pin" -- so the two tests are
	    siblings gating one output, not a nest.  */
	if (d->pcctwo_reg[PCCTWO_GENCTL] & PCC2_C040) {
		if (!(d->warned & (1u << PCC2_W_C040))) {
			d->warned |= (1u << PCC2_W_C040);
			fatal("[ pcc2: C040 (MC68040 EIPL) interrupt delivery not "
			    "implemented; assertion suppressed  (once) ]\n");
		}
		assert = 0;
	}

	if (assert)
		INTERRUPT_ASSERT(d->cpu_irq);
	else
		INTERRUPT_DEASSERT(d->cpu_irq);
}
```

## QUESTIONS
Q1. P1-P3: confirm or refute each from the code.
Q2. Severity: host termination on one legal guest byte store -- where should it rank, and was the fix the right member of the
    option set (accept / decline / decline+latched announce / implement)?
Q3. Anything the shipped fix still gets wrong?


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
