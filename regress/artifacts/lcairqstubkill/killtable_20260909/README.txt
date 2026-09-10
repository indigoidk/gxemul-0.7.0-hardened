#516 KILL TABLE D -- the SHIPPED 11-row instrument, 2026-09-09.  Log: TABLE_D.out (this dir).

WHY THIS TABLE EXISTS.  The measuring seat built and measured an 11-row instrument (probe5, also
preserved, in ../killtable_opus_20260909/).  The main loop then WIDENED `kbc attrib' on top of it.
A changed instrument no longer matches the seat's table, so the seat's numbers stopped describing
the deliverable.  Predicting the new scores would be the frozen-number class; this run measures
them.  Driver + mutator + instrument were all FROZEN into /tmp/kill516d before mutant 1.

BASELINE NAMED: the GXEMUL-SEC working tree (the round's post-fix set), cmp'd CLEAN against the
clone before mutant 1.  Clone /tmp/gxopus516, clone-local .MUTANT sentinel, restore verified by
cmp against SEC plus a rebuild, sentinel cleared.  No project tree was mutated.

    mutant                 score   what it tests
    ---------------------  -----   -------------------------------------------------------------
    base                   11/11   the fix itself
    M2_both                 3/11   (b) verbatim reinstatement, BOTH sites
    M2d_deassert            6/11   (b) verbatim reinstatement, DEASSERT ONLY   *** was 6/6 ***
    M2a_assert              3/11   (b) verbatim reinstatement, ASSERT ONLY
    M3_deassertoff          8/11   (d) deassert guard -> if (0)                *** was 6/6 ***
    M3a_assertoff           8/11   (d) assert guard -> if (0)
    M4_sharedlatch          8/11   (d) the two latch bits collapsed onto one   *** was 6/6 ***
    M5_assertdishonest     10/11   the assert announce stops saying WHY
    M6_deassertdishonest   10/11   the deassert announce stops saying WHY
    M7_deassert_assign     10/11   `|=' -> `=' on the DEASSERT arm
    M8_assert_assign       11/11   `|=' -> `=' on the ASSERT arm -- EQUIVALENT, see below
    M9_deassert_nolatch    10/11   the deassert latch guard removed
    M10_assert_nolatch     10/11   the assert latch guard removed
    M11_null                0/11   (c) null medium

*** THE THREE 6/6 ESCAPES ARE CLOSED.  That is what this table was for. ***  Against the SHIPPED
SIX-ROW detector (../killtable_opus_20260909/*_shipped.raw) M2d, M3_deassertoff and M4_sharedlatch
each scored 6/6 -- a clean sweep.  M2d is the sharp one: a VERBATIM REINSTATEMENT of
`fatal(); exit(1)' at the deassert site, which floor clause (b) requires the detector to fail on
"at EVERY fixed site", and that site had no coverage at all.

WHICH ROWS CARRY THE KILLS -- checked, not inferred:
    M2d              kbc kill, drain sig, deassert ann, deassert honest, deassert once
    M4_sharedlatch   deassert ann, deassert honest, deassert once
    M7               assert once (counted 2, want 1)

`kbc attrib' is NOT among M2d's reds, and that is the widening working as designed.  Before it,
the row reported `died-elsewhere' on a death in the SIBLING stub -- a true red with a false label,
sending a reader outside a file where the death was four lines away.  It now accepts either stub's
diagnostic and reds only on a death carrying neither.

*** M8 IS A MEASURED EQUIVALENT MUTANT, NOT AN ESCAPE, AND THE ASYMMETRY WITH M7 HAS A
DERIVATION. ***  A mutant that will not die is a RESULT, and silently re-aiming it picks one of the
three explanations without measuring which.  Here:
    M7 (`=' on the DEASSERT arm) KILLS -- by then `warned' already holds the ASSERT bit, so `='
       CLEARS it, [D]'s assert re-announces, and `assert once' counts 2.  MEASURED: got 2, want 1.
    M8 (`=' on the ASSERT arm) is EQUIVALENT -- the assert arm's assignment only ever executes on
       the FIRST assert, when `warned' is still 0, and `=' and `|=' are identical on a zero
       operand.  A deassert cannot precede the first assert, because nothing sets a PIC IRR bit
       but an assert.  So no sequence this device admits can distinguish the two.
This is why M7 and M8 are BOTH kept: the pair is what makes the equivalence a finding rather than
a gap.  MEASURED: M8's `assert once' and `deassert once' both read 1.

*** AN APPARATUS DEFECT OF MINE, IN THIS DRIVER, RECORDED BECAUSE THE COLUMN LOOKS LIKE DATA. ***
TABLE_D.out carries `ann_a=' and `ann_d=' columns, from
`grep -c "ISA interrupt assert not implemented" probe_<m>.raw'.  **They read 0 on EVERY row,
including base, and they always would.**  The probe prints ROWS, not the raw pty capture, and its
EVIDENCE loop filters on "lca_interrupt" -- which the announce text does not contain (it reads
"[ lca: ISA interrupt assert ..."), so the string is never in the .raw at all.  The column is a
CHECK THAT CANNOT FAIL: it returns the same answer whether or not the announce fired.  It misled
nobody because the ROW SCORES carry that information and the row set is printed, but it is
decoration presented as measurement, and the honest disposition is to say so rather than to leave
a reader to trust it.  The load-bearing counts are `assert once' / `deassert once', which are
computed INSIDE the probe from the pty text and are shown per row.


================================================================================================
TABLE E -- THE ADDENDUM THE PASS-2 PANEL BOUGHT, AND IT FOUND A TOTAL ESCAPE.  Log: TABLE_E.out
================================================================================================

    base                     11/11   assert_once=1  deassert_once=1
    M12_assertguard_swap     11/11   assert_once=1  deassert_once=1   *** TOTAL ESCAPE ***
    M13_deassertguard_swap    8/11   assert_once=1  deassert_once=0   killed (deassert ann,
                                                                      deassert honest, deassert once)

M12 is the pass-2 panel's own mutant (minimax): **swap the bit in the ASSERT if-guard ONLY, with
the assignment left alone** --

    if (d != NULL && !(d->warned & (1u << LCA_W_IRQ_DEASSERT))) {   /* guard swapped */
            d->warned |= 1u << LCA_W_IRQ_ASSERT;                    /* assignment NOT swapped */

It is the MIRROR of M4_sharedlatch, which swapped guard AND assignment on the DEASSERT side.  M4
is killed 8/11; its mirror is invisible.  **M12's output is BYTE-IDENTICAL to base on all eleven
rows** (checked field by field, not by score).

WHY IT ESCAPES, derived and then confirmed by the identical output: over the probe's
[B]assert [C]deassert [D]assert+deassert sequence, M12's first assert sees `warned == 0` and
announces; the first deassert sees the DEASSERT bit clear and announces; both [D] edges see
DEASSERT set and stay silent.  Counts 1 and 1 -- exactly the fix's own behaviour.
**THE DIFFERENCE APPEARS ONLY WITH TWO ASSERT EDGES AND NO INTERVENING DEASSERT**, where M12
re-announces (DEASSERT still clear) and the fix stays silent.  That is a genuine log-flood defect
of the class this project already tracks as `floodclass`, and no row here can see it.

*** THE PANEL EARNED ITS KEEP EXACTLY WHERE THE CARRIER SAYS IT DOES, and the split is worth
stating exactly rather than as "the panel found it". ***  Of the four packet-fed seats, THREE
(deepseek, glm, the kimi substitute) attacked the M8 equivalence claim -- and were refuted, below.
The FOURTH, minimax, went past the question it was asked and named a mutant the author had not
built, which is the one that escaped.  So the seats that were WRONG on the question asked and the
seat that was RIGHT on a question nobody asked are different seats, and a summary saying "four
seats challenged the table" would have merged them.  The ask-again's cap counts ASKS, never
FINDINGS -- so this is disposed of on its own merits rather than deferred.  The ask-again's cap counts ASKS, never
FINDINGS -- so this is disposed of on its own merits rather than deferred.

--- AND THOSE THREE SEATS' CHALLENGE WAS CHECKED AND REFUTED, WHICH IS THE HONEST OTHER HALF ---
deepseek, glm and the kimi substitute all called M8_assert_assign (11/11) a clean sweep waved off
as "equivalent".  Checked in `dev_8259.c` rather than defended: all THREE direct deassert sites
are guarded by an aggregate-CHANGE test -- `(old_irr & ~ier) != (irr & ~ier)` at the EOI (:111)
and specific-EOI (:125) arms, `(irr & ~old_ier) != (irr & ~ier)` at the IMR arm (:217).  With
`irr == 0` both sides are zero at every one, so **no deassert can precede the first assert**, and
`d->isr` is confirmed never set (cleared at :108/:123, read at :148).  M8's equivalence stands.
*The seats were right to demand it be SHOWN rather than asserted; they were wrong that it fails.*

--- THE OPEN QUESTION, DELIBERATELY NOT SETTLED BY THE AUTHOR ---
Whether M12 is a FLOOR BREACH (L2, fix in-round) or clause-(e) debt turns on ONE fact: is there a
SECOND ISA line on `alphabook1` that a STEPPED probe can make assert synchronously?  Ruled out by
reading: the mouse (host-input path only; `0xd4` is a bare debug TODO), the LPT (`dev_lpt_tick` is
empty -- it is the control precisely because it never asserts), and the PIT/RTC (host-timer driven,
so invisible to a stepped probe).  An IMR mask/unmask gives assert -> deassert -> assert, and the
middle deassert sets the bit, so it does not discriminate.  Remaining candidates: the ns16550 UART
on IRQ 4 (installed unconditionally, but every observed assert so far is tick-driven), and the WDC
on IRQ 14/15 (which exists only if an IDE image is attached, so using it changes the probe's
machine configuration).
**Referred to the measuring seat WITH the note that the author has an interest in the answer**, since
"no second line exists" is the finding that lets the round ship.

--- THE PASS-2 REVIEW'S "ZERO BREACHES" DOES NOT CLOSE THE CHAIN, AND THE REASON IS TIMING ---
The 2026-09-09 pass-2 review seat answered Q1 with **no clean-sweep mutant in the clause-(d)
enumeration**, and it enumerated honestly and by reading, mapping each operand swap to a measured
row.  Its list contains: guard -> if(0) (M3/M3a); latch guard removed (M9/M10); **"tested-bit
collapse (deassert tests/sets assert bit): M4"**; assignment |= -> = (M7/M8); announce text
(M5/M6); verbatim reinstatement (M2/M2a/M2d); null medium (M11).

**M12 IS NOT IN THAT LIST.**  M4 is the deassert-side swap of BOTH guard and assignment; M12 is
the ASSERT-side swap of the GUARD ALONE.  The enumeration collapsed a two-by-two -- {assert site,
deassert site} x {guard only, guard and assignment} -- into one cell, and the open cell is the one
that escapes.  *That is the `#499` shape again: a cell of one state space left empty, in the
enumeration written to prove no cell was empty.*

The seat was fired BEFORE table E existed, so this is not a fault of its answer; it is a fact
about what the answer could see.  But the repair-chain stop condition is explicit that **a closing
pass must be a VALID pass and its zero must carry a DENOMINATOR** -- and a denominator that omits
a measured escape does not close a chain.

  *** SO THE CHAIN IS OPEN.  #516 DOES NOT COMMIT UNTIL M12 IS DISPOSED OF. ***

And the disposition is NOT "add a row" by default: whether M12 is a floor breach or clause-(e)
debt turns on whether ANY rung-3 probe on `alphabook1` can produce two assert edges with no
intervening deassert -- referred to the measuring seat, with the author's interest in the answer
disclosed.  Adding a row that cannot be driven would be worse than disclosing the gap honestly.
