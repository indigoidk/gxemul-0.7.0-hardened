"""L4 IN PRODUCT CODE: the shipped comment's warrant for B4 is MEASURABLY FALSE.

I wrote, into dev_wdc.c: "it escaped every row with a BYTE-IDENTICAL scenario differential:
edge and level are indistinguishable here."

The opus seat built the discriminating scenario with REGISTER WRITES ONLY -- no struct
poking, every step a real dev_wdc_altstatus_access or dev_wdc_access call:

    R1  assert 0x0e -> 8 guest stores to DATA -> rewrite 0x0e -> negate 0x08
          LEVEL (shipped):  occ=0  DRQ=0     <- the ring is purged
          EDGE:             occ=8  DRQ=1     <- 8 stale bytes survive the whole reset,
                                                and the status byte still reports DRQ
    R2  LIVENESS: same traffic, no reset  -> occ=8   (so R1's 0 is the reset working)
    R3  single assert, bytes after        -> occ=8 BOTH  <- WHY THE ROUND SAW NO DELTA
    R4  dirty ring, then assert           -> occ=0 BOTH

*** R3 IS THE DIAGNOSIS: the round's differential only ever asserted SRST ONCE. ***  Edge
and level differ exactly when a driver HOLDS SRST across two control writes and anything
accrues in between.

THE DECISION STANDS -- level is correct, because a channel held in reset must not carry
bytes out the far side.  What was wrong is the reason recorded for it.  The honest warrant
is "the measurable difference FAVOURS level", which is stronger than "there is no
measurable difference" and does not collapse the moment someone builds R1.

TWO SUPPORTING CLAIMS IN THAT COMMENT ARE ALSO WRONG, and both are worth correcting rather
than deleting:

  * "the abort is idempotent" is TRUE of the helper and does not license the inference.
    Idempotence means REPEATING is harmless; it does not mean SKIPPING THE REPEAT is
    harmless, because state accrues between the writes.
  * "no protocol-following driver issues commands while holding SRST" -- R1 ISSUES NO
    COMMAND.  Plain data-register stores suffice.  And in a hardening fork the guest need
    not be protocol-following at all.

AND THE OPTION SET WAS INCOMPLETE: `Mo_edgefree` is an edge form with NO NEW FIELD --
`if (d->cur_command != COMMAND_RESET) wdc_new_command_reset(d);` -- which escapes all 94
rows and reproduces R1.  The prev_ctl/m7 argument does not reach it, so "adding state is
unwarranted" was never the whole answer.
"""
import io

NL, T = chr(10), chr(9)
P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\src\devices\dev_wdc.c"
s = io.open(P, encoding="utf-8", newline="").read()

OLD = (T*2 + "    LEVEL-TRIGGERED, DELIBERATELY, AND THE EDGE WAS DECLINED ON A" + NL +
 T*2 + "    MEASUREMENT.  A seat built the edge-dropped mutant and it escaped" + NL +
 T*2 + "    every row with a BYTE-IDENTICAL scenario differential: edge and" + NL +
 T*2 + "    level are indistinguishable here, because the abort is idempotent" + NL +
 T*2 + "    and no protocol-following driver issues commands while holding" + NL +
 T*2 + "    SRST.  A measured delta of zero is not a licence to add state --" + NL +
 T*2 + "    and a prev_ctl update mis-scoped by one brace makes every LATER" + NL +
 T*2 + "    reset be ignored, a failure this form cannot have." + NL)

assert s.count(OLD) == 1, "warrant anchor occurs %d times" % s.count(OLD)

NEW = (T*2 + "    LEVEL-TRIGGERED, DELIBERATELY, AND THE MEASURED DIFFERENCE" + NL +
 T*2 + "    FAVOURS THIS FORM.  A channel held in reset must not carry bytes" + NL +
 T*2 + "    out the far side, and an edge-triggered abort lets it:" + NL +
 T*2 + "" + NL +
 T*2 + "        assert 0x0e, 8 guest stores to DATA, rewrite 0x0e, release" + NL +
 T*2 + "          LEVEL (this form):  occ 0, DRQ 0   -- the ring is purged" + NL +
 T*2 + "          EDGE:               occ 8, DRQ 1   -- the bytes survive the" + NL +
 T*2 + "                                                 whole reset, and the" + NL +
 T*2 + "                                                 status byte still" + NL +
 T*2 + "                                                 advertises DRQ" + NL +
 T*2 + "" + NL +
 T*2 + "    Measured through register writes only, with a liveness control (the" + NL +
 T*2 + "    same traffic without a reset leaves occ 8, so the 0 is the reset" + NL +
 T*2 + "    working and not a dead path)." + NL +
 T*2 + "" + NL +
 T*2 + "    *** AN EARLIER VERSION OF THIS COMMENT SAID edge and level were" + NL +
 T*2 + "    \"indistinguishable here, because the abort is idempotent and no" + NL +
 T*2 + "    protocol-following driver issues commands while holding SRST\"." + NL +
 T*2 + "    THAT WAS MEASURED FALSE.  Three things were wrong with it:" + NL +
 T*2 + "" + NL +
 T*2 + "      * the differential behind it only ever asserted SRST ONCE, and" + NL +
 T*2 + "        the forms differ only when a driver HOLDS it across two" + NL +
 T*2 + "        control writes with something accruing in between;" + NL +
 T*2 + "      * IDEMPOTENCE OF THE HELPER DOES NOT LICENCE THE INFERENCE." + NL +
 T*2 + "        It means repeating the abort is harmless.  It says nothing" + NL +
 T*2 + "        about SKIPPING the repeat, which is what an edge does, and" + NL +
 T*2 + "        state accrues between the writes;" + NL +
 T*2 + "      * the scenario above ISSUES NO COMMAND.  Plain data-register" + NL +
 T*2 + "        stores suffice -- and in a hardening fork the guest need not" + NL +
 T*2 + "        be protocol-following at all." + NL +
 T*2 + "" + NL +
 T*2 + "    The decision is unchanged and now rests on evidence that does not" + NL +
 T*2 + "    collapse when someone builds the discriminating case. ***" + NL +
 T*2 + "" + NL +
 T*2 + "    Note also that a prev_ctl update mis-scoped by one brace makes" + NL +
 T*2 + "    every LATER reset be ignored -- a failure this form cannot have --" + NL +
 T*2 + "    but that is a secondary argument, not the reason." + NL)

io.open(P, "w", encoding="utf-8", newline="").write(s.replace(OLD, NEW, 1))
print("  dev_wdc.c: the B4 warrant replaced with the measured one (L4)")
