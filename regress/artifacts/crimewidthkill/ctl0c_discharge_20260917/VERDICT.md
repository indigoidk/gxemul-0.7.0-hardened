# `#529` L1 -- THE `ctl0c` PAIR IS **DISCHARGED**.  The rows stay.

## THE MEASUREMENT (`RUN.out`, sentinel `KILLCTL0C_DONE 2026-09-17 12:53:02`)

    base              CRIMEP_RESULT=204/204
    M_ctl0c_decline   CRIMEP_RESULT=202/204

    acc ctl0c     base ok -> mutant FAIL
    p acc ctl0c   base ok -> mutant FAIL
    acc ctl4r     base ok -> mutant UNMOVED
    p acc ctl4r   base ok -> mutant UNMOVED

**THE PREDICTION WAS WRITTEN INTO `mutants_ctl0c.py` BEFORE THE RUN, so its own mtime proves the
order**, and it read: *"`acc ctl0c` and `p acc ctl0c` RED ... `acc ctl4r` / `p acc ctl4r` UNMOVED
... EXPECTED SCORE 202/204."*  **Exact match on all four rows and on the score.**

## CONTROLS, ALL PASSED

    PROBE FROZEN cmp=clean                      the instrument is the shipped one
    CLONE START: dev_sgi_ip32.c cmp CLEAN       baseline identity before mutant 1
    binary DIFFERS from base                    *** the edit is LIVE IN THE OBJECT ***
    CLONE RESTORED cmp=clean binary-nt-source=yes

That third control is the one that makes 202/204 a result: a mutant that never applied scores
exactly like a clean sweep, and this project has a standing rule that the base/mutant binary `cmp`
is what separates them.

## *** THE ROWS WERE NEVER VACUOUS.  THE MUTANT SET WAS INCOMPLETE. ***

The finding that opened this was *"`acc ctl0c` NEVER REDS under any of the FIFTEEN LEGS of table
12"*, and the honest reading of that was: either the rows are vacuous by construction, or fifteen
legs all missed the shape that moves them.  **It is the second.**

`acc ctl0c` reads `lw +0x0c` and wants `0x100`.  That value is produced by the **WIDTH ARM**
(`} else if (len == 4) { ... odata = d->reg[relative_addr / 8]`, then `if (relative_addr & 4) odata
= (int32_t)odata`), which runs **BEFORE the register switch**.  `+0x0c` has no case label, so it
lands in `default:` -- a debug print only.

> **SO A DECLINE AT `default:` CANNOT MOVE THIS ROW, AND NEITHER CAN `G_clr_ctl4r`'s
> `relative_addr == CRIME_CONTROL` (0x08), WHICH NEVER TOUCHES 0x0c.**  Every one of the fifteen
> legs was aimed where this row's value does not come from.

The discharging mutant therefore has to decline **before** the width arm:

    if (relative_addr == 0x0c) goto crime_declined;

which is the clause-(d) shape -- keep the guard, reroute its effect -- and is a plausible future
edit: someone deciding this device should REFUSE unimplemented offsets rather than answer them out
of the width arm.

## DISPOSITION

**Accept-row failability is satisfied: the pair is discharged BY A MEASURED KILL, not by existing.**
The Fable adjudication's L1 obligation -- *"discharge them or remove them, BEFORE #529 commits"* --
is met by the first branch.  **The rows stay, and `#529`'s L1 is closed.**

*Worth keeping for the next table: the reason fifteen legs missed this is not carelessness but
AIM.  A row whose value is produced before the switch cannot be moved by any mutant that edits the
switch, however many of them you build.*
