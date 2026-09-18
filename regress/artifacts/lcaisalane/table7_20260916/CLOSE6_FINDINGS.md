# CLOSING PASS 6 -- findings.  PANEL_COMPLETE 2026-09-17 09:09:50, 8/8 scriptable seats.
# Opus seat still running; Fable HELD until all others have answered.

## THE SPLIT, AND IT RESOLVES TO A DEFECT IN MY BRIEF RATHER THAN IN THE REPAIR

    grok    (file-reading)   VERDICT: CLOSES -- 8-cell (d) closed on the composite, no 352/352 mutant
    agy     (file-reading)   VERDICT: GO     -- "the clause-(d) DEPENDS-ON enumeration is closed"
    glm     (PACKET-FED)     VERDICT: this packet does NOT establish a valid closing pass

**glm's argument, reasoning only on the packet's own claims:**

> *"'len 0 has no producer' (A), 'no leg at 352/352' (B), and the claim that the 15 mutants exhaust
> the (d) enumeration (C) cannot all be true as stated: **if A and C hold, a guard-removal mutant is
> observationally identical to base and scores 352/352, contradicting B.**"*

**That is sound.**  `len == 0` is an ADDED predicate, so clause (d) demands a mutant that nulls it, and
no such leg is in the fifteen this pass ran.

## IT IS ALREADY SETTLED IN THE ARTIFACTS -- grok found it, and I verified it rather than taking it

    fix530_20260914/logs/lane0.out:7      m_lenzero LCAISALANE_RESULT=37/37
    fix530_20260914/check_pred.out:13     EXACT    m_lenzero    0 red
    c1_20260914/BRIEF.md:375              m_lenzero 51 (EQUIVALENT)
    regress/lca_isalane_probe.py:137      "len == 0 is refused and DISCLOSED (no producer)"

**The guard-removal mutant WAS built (`m_lenzero`), measured EQUIVALENT on two instruments (37/37 and
51/51), PREDICTED as 0 red and matched exactly, and DISCLOSED in the shipped probe's clause-(e)
contract.**  Equivalence-plus-disclosure is the documented disposition, not a breach -- the same shape
as `G_clr_ctl4r` in `#529`'s table 12.

> **SO THE DEFECT IS IN MY BRIEF: it never inlined the `m_lenzero` equivalence or the contract line.**
> A packet-fed seat cannot settle a repo fact -- and this one did not pretend to.  It named its
> settling fact precisely (*"Settling fact: POSTTABLE.out + CHECKPRED_fixed.out"*) and marked every
> unverifiable claim NOT CHECKABLE.  That is the conditioned answer the doctrine rates ABOVE an
> unconditioned agreement, and it was right at the scope it could see.

**This is the SECOND brief of mine in one day to state a true conclusion on evidence that does not
carry it** -- the first was `pit8253flood` section C1, where minimax caught the same shape.  The
pattern is mine, not the seats': I inline the conclusion and the reasoning that convinced ME, rather
than the artifact that would convince a reader who starts from nothing.

## glm's OTHER OBSERVATION, which is correct and worth keeping

P1 (`fatal()` does not exit) is **not load-bearing for this repair at all**: the diff deletes the
`fatal()` call AND the `exit(1)` together, so "the kill goes" holds whichever one killed.  And the old
code's own shape -- `fatal(...)` immediately followed by `exit(1)` -- is the codebase's own witness
that `fatal()` returns.  I had inlined P1 as a settled premise; it did not need to be settled.

## *** THE "RECORDS DEFECT IN AN EARLIER POSTTABLE" IS A FALSE POSITIVE, AND MY NOTE OF IT WAS
## WRONG.  Corrected in place within the hour, after checking the artifact. ***

I recorded below that the kimi CLI had found a live defect in the fix530-era POSTTABLE and filed
it as an L4 owed by a closed round.  **It was already corrected -- on 2026-09-14, by the kimi CLI
itself, in closing pass 1.**  `fix530_20260914/table2/POSTTABLE.out:19-22` reads:

> *"Every non-equivalent leg DETECTED; of the pass-2 legs, the nine outcome-changing ones
> re-measured here (p_* bar p_nozero, and g_len4w) are red on the rows the repair added; p_nozero
> is EQUIVALENT; p_port10 was NOT re-measured (disclosed).  [Corrected 2026-09-14 from closing
> pass 1 (kimi CLI): this read "every one of the ten pass-2 escapes ... bar the two equivalents"
> -- p_port10 is disclosed and unmeasured here, not an equivalent.]"*

**So the sentence kimi flagged today is the QUOTATION INSIDE ITS OWN EARLIER CORRECTION.**  The
accurate statement, the date, the attribution and the refuted text are all present and correct.

*** THE INSTANCE IS WORTH MORE THAN THE NON-DEFECT, AND IT SHARPENS A RULE THIS PROJECT ALREADY
HAS. ***  The carrier records that a stale-text search cannot tell an ASSERTION from a QUOTATION
OF ONE, and that such searches get steadily MORE wrong as the records get more honest -- because
every correction here quotes what it refutes.  This is that class **in the artifacts rather than
in the carrier**, and with an extra turn of the screw: **the seat that re-flagged the text is the
same seat that corrected it three days earlier.**  A seat carries no memory across panels, so the
quote-what-you-refute discipline makes every corrected error PERMANENTLY RE-FINDABLE by the very
reviewer who fixed it.

**The discipline is still right and should not change.**  The cost is a recurring false positive;
the alternative is deleting the evidence that makes a correction checkable.  What follows is that
**a records finding against an OLD artifact is checked by OPENING it, never by trusting the
quotation a seat hands you** -- I filed this one as live for an hour on exactly that mistake.

*(The original note follows, kept because it states the arithmetic correctly and only its
disposition was wrong.)*

## (SUPERSEDED) A RECORDS DEFECT IN AN EARLIER POSTTABLE, found by the kimi CLI while auditing arithmetic

`fix530_20260914`-era POSTTABLE says *"every one of the ten pass-2 escapes (p_* and g_len4w, bar the
two equivalents) red on the rows the repair added"*.  kimi reconciled that against the tables and it
does not parse: `p_port10` was **NOT RE-MEASURED** (the same POSTTABLE says so), it is not an
equivalent (it changes a guest outcome -- port 0x7ff reads SCR), and the 51-row instrument would not
catch it anyway since every probed port is below 0x400 so `&= 0x3ff` is the identity there.  **The
accurate statement is: nine of the ten outcome-changing legs re-measured red; `p_port10` remains
disclosed-and-not-caught by design; `p_nozero` is equivalent.**  FILED, not fixed here -- it is a
closed round's record and belongs under the late-dissent rule as an L4 correction in its own commit.
