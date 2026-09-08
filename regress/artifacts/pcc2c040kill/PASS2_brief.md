# `#512` pcc2c040kill -- PASS 2 on the real diff

**PLEASE DO NOT RATIFY.** Pass 1 was unanimous IMPLEMENT-WITH-REVISIONS and **four of you caught a
defect in my proposal that I would have shipped** (it never stated the deletion of the old block).
This pass exists to find the next one. **The load-bearing question is Q1: which of the dispositions
I ACCEPTED is wrong?**

**Tree under review: `GXEMUL-SEC/src/`.** Other `src/` copies under the project root are pristine
2021 upstream and will give line numbers off by hundreds.

---

## 1. THE DIFF, verbatim (3 hunks, 40 changed lines)

```diff
diff --git a/src/devices/dev_pcc2.c b/src/devices/dev_pcc2.c
index 76245d2..fdb62c9 100644
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
@@ -341,6 +339,37 @@ static void reassert_interrupts(struct pcc2_data *d)
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
+	    already does for the other GENCTL interrupt-control bit; an early return
+	    here would skip the IPL recalculation, the cur_int_vec[] updates and the
+	    INTERRUPT_DEASSERT below.
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

## 2. SETTLED PREMISES (inlined; the packet-fed seats cannot read files)

* **The defect, MEASURED.** `regress/pcc2_c040_probe.py` on the committed build: **3/4**, the RED
  row being the defect. One guest `st.b` of 0x04 to GENCTL (offset 0x02) on unmodified
  `-E mvme88k -e mvme187` ended the host via `fatal()+exit(1)` at the TOP of
  `reassert_interrupts()`. After the fix, **4/4 with the SAME script**; then **7/7** with three
  added rows.
* **`reassert_interrupts()` is a void helper called from TEN sites**, and the GENCTL write arm calls
  it in the SAME access -- which is why one store sufficed.
* **The primary source settled the two questions pass 1 could not.** `_scratchpad/vmesbcp2.txt`
  (MVME187 board manual), General Control Register at `$FFF42002`: `DR0/C040/MIEN/FAST` =
  `0x80/0x04/0x02/0x01`, all four matching this fork's header. A set C040 sends the request *"via
  the EIPL* pins at the level that is programmed ... in the SCSI Interrupt Control Register"*, and
  IPL2-IPL0 *"always reflect the encoded request level"*. **So C040 selects the DELIVERY PIN, not
  the level** -- the IPL recalculation must stay. MIEN by contrast disables *"both the EIPL* pins
  and the INT pin"*, so the two tests are siblings gating one output.
* **KILL TABLE, scratch clone, artifacts preserved:**

        BASE                                   7/7
        M_b_reinstate   the verbatim exit(1)   3/7   floor (b) -- KILLED
        M_d2_silent     announce deleted       4/7   floor (d) -- KILLED
        M_d3_nolatch    announce every call    6/7   floor (d) -- KILLED
        M_d4_collide    latch bit reused       6/7   floor (d) -- KILLED
        M_d1_noassert   `assert = 0' removed   7/7   *** ESCAPES -- CLEAN SWEEP ***

* **Why M_d1 cannot be rowed in this probe shape, verified two ways.** For the tail to print ASSERT,
  an ICR INT bit must be set. Every guest-writable arm masks it out (`TxICR` keeps `idata & 0x17`,
  `SCCICR` keeps `& 0x1f`; `PCC2_IRQ_INT` is 0x20). Its only producer is `pcc_timer_tick`,
  registered by `timer_add(PCC_TIMER_TICK_HZ, ...)` -- a HOST-TIMER callback, and the debugger stops
  host timers for the duration of a `step`.

## 3. THE DISPOSITIONS I ACCEPTED -- attack these

1. **Graded M_d1 a FLOOR BREACH under clause (d), not clause-(e) contract debt.** Reason: `assert =
   0` is the repair's EFFECT, so nulling it is (d)'s canonical "keep the guard, null the repair" and
   sits INSIDE the DEPENDS-ON closure. Calling it disclosed debt would use the contract as an escape
   hatch.
2. **Shipped anyway, with the breach DECLARED in the probe contract, the CHANGELOG and the ledger,
   and the repair filed as its own row** (a free-running probe shape). Reason: the fix removes a live
   host death; withholding it to build a different probe shape leaves the kill in place.
3. **Joined the C040 test to the MIEN test rather than returning early**, keeping the IPL
   recalculation.
4. **Latched with a new `PCC2_W_C040` enumerator appended at the END of the existing enum**, so no
   existing warn bit renumbers.
5. **Left the four original witness rows byte-for-byte alone** and added new rows instead, so the
   red-pre-fix / green-post-fix evidence is not destroyed by re-keying.

## 4. QUESTIONS

**Q1 (THE LOAD-BEARING ONE). Which of the five dispositions above is wrong?** I accepted all five;
a round that accepted everything has either had a good panel or has stopped arguing, and only you
can tell me which. **Be hardest on 1 and 2** -- a ruling that lets a round ship with a declared floor
breach is exactly the kind that gets reused as precedent.

**Q2 (THE NEXT MUTANT).** The table above is CLEAN except for the one declared escape. **What is the
smallest edit to this diff that still passes all 7 rows?** Consider: the enum position, the `(once)`
text, the placement relative to MIEN, and what happens if a future edit reorders the two tests.

**Q3 (THE DIFF ITSELF).** Read the hunks against the enclosing function's control flow. Does the
declining block sit where its comment claims? Is there any path through `reassert_interrupts()` that
now reaches `INTERRUPT_ASSERT` with C040 set? Does deleting the top block change anything for the
other NINE callers?

**Verdict line first** -- RATIFY / RATIFY-WITH-RESIDUALS / DO-NOT-SHIP -- then the body. **A verdict
that merely agrees is the least useful reply**; if you find nothing wrong, say what you CHECKED.
