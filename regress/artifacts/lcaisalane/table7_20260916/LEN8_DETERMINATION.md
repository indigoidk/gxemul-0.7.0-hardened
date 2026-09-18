# `#530` -- THE len8 LEG IS IN.  **MEASURED TOTAL ESCAPE -> L2, FLOOR BREACH, FIX IN-ROUND.**

## THE MEASUREMENT (`KILLLEN8_RUN.out`, finished 2026-09-17 10:49:00, sentinel `KILLLEN8_DONE`)

    base    LCAISALANE_RESULT=352/352   LCAISALANE_DONE
    W_len8  LCAISALANE_RESULT=352/352   LCAISALANE_DONE     <-- TOTAL ESCAPE

The mutant is `len == 0` -> `len == 0 || len > 8`: one added disjunct on the guard the repair
introduced, i.e. clause (d)'s canonical *keep the guard, null its repair* form.

**THREE APPARATUS CONTROLS PASSED, and they are why this is a result rather than a non-event:**

    CLONE START: src/devices/dev_lca.c cmp CLEAN against SEC     -- baseline identity
    NOTE W_len8 binary DIFFERS from base                          -- *** the edit is LIVE in the
                                                                      object, so 352/352 is an
                                                                      ESCAPE and not a mutant that
                                                                      never applied ***
    CLONE RESTORED cmp=clean binary-nt-source=yes                 -- two-part clearance, in-clone

*That middle control is the one that matters.  A mutant table's commonest silent failure is a mutant
that did not build in, and it presents as a perfect score -- identical to a clean sweep.*

## THE DISPOSITION WAS PRE-SPECIFIED, SO APPLYING IT IS MECHANICAL

`CLOSE6_VERDICT.md:77-79`, written BEFORE this leg ran:

> * **escapes AND len>8 is guest-reachable -> L2**, add a len>8 row in-round
> * **escapes but unreachable -> clause-(e) DEBT**, disclose the `store_buf`-reachable width cell

*Writing the rule before the measurement is what stops the result being argued into whichever
disposition is cheapest -- the oracle-correction rule's order discriminator, applied to a
disposition instead of to a pin.*

## BOTH LIMBS ARE SATISFIED

**ESCAPE: measured above, 352/352.**

**REACHABILITY: verified in source, not reasoned.**

    src/core/memory.c:837,:839,:841-853     store_buf() issues memory_rw at psize in
                                            {1024, 256, 64, 16, 4, 1} -- every one of them > 8
    src/cpus/cpu_alpha_palcode.c:144        PROM GETENV calls store_buf(cpu, a2, s, len)
                                            with **a2 GUEST-SUPPLIED**

So a guest choosing `a2` inside the LCA ISA window reaches this handler at len 16/64/256/1024.
**No probe row drives that today and the reason is structural:** the probe is INSTRUCTION-driven and
the widest Alpha store is STQ at 8 bytes, so *no instruction-driven row can ever reach this cell.*

## => **L2.  FLOOR BREACH.  FIX IN-ROUND, however late.**

**WHAT IS OWED IS A DETECTOR ROW, NOT A PRODUCT CHANGE.**  The shipped code is CORRECT at wide
widths: for len 16, `ofs = (relative_addr & 3) % 16` is just `relative_addr & 3`, which is in [0,3]
and indexes safely inside the buffer.  It is the MUTANT that misbehaves, by declining a legal wide
access.  **Do not touch `dev_lca.c` for this.**

**The row must drive a NON-INSTRUCTION path** -- a PROM GETENV whose `a2` lands in the ISA window --
because the instruction path cannot express len > 8.  That is the whole difficulty and it is why the
cell was empty.

## AND THE CONTRACT IS A WRONG RECORD REGARDLESS -- L4, independent of the above

The probe header's contract claims the covered widths are *"1/2/4/8 plus the 1 KB split"*.  It
**OMITS 16/64/256/1024**, which `store_buf` demonstrably issues.  That is an L4 wrong record whether
or not the row lands, and `CLOSE6_VERDICT.md:67` already said so before this leg ran.
