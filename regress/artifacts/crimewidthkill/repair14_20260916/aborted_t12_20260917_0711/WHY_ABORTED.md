# Table 12, run of 2026-09-17 07:11 -- ABORTED AT 4 OF 15 LEGS, DELIBERATELY.

## THE STAGING CHECK FAILED: `base` READ 202/204, NOT 204/204.

    base             202/204      <-- the check required 204/204
    G_clr_ctl4r      202/204
    G_clr_ist4r      201/204
    G_glm_tim4clear  200/204

`probe_base.raw` names its own failures:

    acc ctl0c    got 0xb4000008  want 0x100   FAIL
    p acc ctl0c  got 0xb4000008  want 0x100   FAIL
    FAILING: acc ctl0c, p acc ctl0c

## CAUSE -- A REGISTER COLLISION IN A ROW I ADDED IN REPAIR 14

Both rows load `lw CRIME+0x0c' into **a3** and read it back.  **`st()` USES `a3` AS ITS ADDRESS
REGISTER** (`["a3=0x%x" % addr, "t0=0x%x" % val]`).  Six `st()` calls follow that load in the same
session; the last is `st(sd, CRIME+0x08, 0x01)`, which leaves `a3 = 0xb4000008` -- **exactly the value
read back**.  The paired row `acc ctl4r` passes because it reads `a0`, which `st()` never touches.

## WHY IT WAS ABORTED RATHER THAN LEFT TO FINISH

The two rows are constant-red on EVERY leg, so they can never discriminate -- they are vacuous by
construction, and any score they contribute to is a 202-row score wearing a 204-row label.  Letting
eleven more legs run would have cost about an hour to produce a table that must be re-run anyway.
**The staging check exists to catch exactly this before the table, and it did its job -- one leg late.**

## WHAT THE STATIC PREREQUISITES COULD NOT CATCH, stated plainly

Four static checks passed before this run -- ast.parse, row-name duplicates, definition order, and the
mutant pre-flight.  **NONE of them models REGISTER LIFETIME**, which is what this defect is: a value
loaded into a register that a later helper reuses as scratch.  Catching it statically would need a
checker that knows `ld()` clobbers `at`, `st()` clobbers `a3` and `t0`, and `roundtrip()` clobbers
`at`, `a3`, `t0` and `v1` -- then walks each session in order.  That is buildable and is NOT built
here; it is recorded as the honest gap rather than implied away.

## THE FIX (L1 -- pre-ship construction, so fixing in-round is licensed)

Load into **`s4`** instead: MIPS register 20, referenced NOWHERE else in the probe and used as scratch
by no helper.  `s4` was added to the `R` map and its hand-assembled encoding pinned with an assertion
beside the existing ones, because this probe's own comment records that a wrong register field reads
0 -- and 0 is what a DECLINE answers, so the error would be invisible to an accept row.

    enc("lw", "at", "s4") == 0x8c340000      verified two ways, independently of the probe

Post-fix, all three static checks pass again: NAMEORDER_PASS, ROWEXPAND_CLEAN, ENC_PASS.

---

## THE SIBLING CENSUS: IS THIS A CLASS OR A ONE-OFF?  ANSWER: A ONE-OFF.

The option-set rule says grep the tree for the idiom before deciding, so the same question was asked of
every probe: does any of them LOAD a value into a register that one of its own helpers uses as scratch?

*** THE FIRST CENSUS WAS KEYED ON A CORRELATE AND REPORTED "no hazard anywhere" -- the reassuring
direction, which is the dangerous one. ***  It grepped for the first line matching `"<reg>=0x%x" % addr`
and took that as "the register st() clobbers".  In `crime_width_probe.py` the first such line is
**ld()'s `at`**, not **st()'s `a3`** -- so the census could not see the very defect it was written to
look for.  Keying on *the first helper that builds an address* is not keying on *the register st()
clobbers*.  Rewritten (`regcensus.py`, preserved here) to parse the function definitions with `ast` and
read each helper's own body.

    probes scanned: 9    with a candidate: 1 (crime_width_probe.py)    REGCENSUS_HAZARD

**ALL FOUR OF ITS CANDIDATES ARE FALSE POSITIVES, each for a different structural reason, and every one
was checked by reading rather than dismissed:**

    line  634   `print v0' precedes roundtrip() in the session list -- the clobber happens after the read
    line  694   same shape; the trailing `more' is an ld() clobbering at/v1, and the print precedes it
    line  833   the only nearby st() is the ELSE branch, mutually exclusive with the v0 load; the
                intervening calls are ld()s clobbering at/s1/s2/v1, never v0
    line 1140   v0 is loaded three times in a loop and NEVER READ BACK -- those loads drive refusals

> **SO THE `a3` DEFECT WAS A ONE-OFF.  No other probe in this tree has the shape, and this probe has no
> second instance.**  That is worth knowing before anyone generalises from one bug to a policy.

**AND THE TOOL'S LIMIT IS STATED RATHER THAN IMPLIED: `regcensus.py` FLAGS CANDIDATES, NOT DEFECTS.**  It
models which registers a helper clobbers; it does NOT model REGISTER LIFETIME (is the clobber between
the load and the read?) or BRANCH STRUCTURE (are the two arms mutually exclusive?).  Both were needed
to clear all four candidates here.  A version that decided on its own would have reported four defects
that do not exist -- which is why it prints candidates and leaves the reading to a person.
