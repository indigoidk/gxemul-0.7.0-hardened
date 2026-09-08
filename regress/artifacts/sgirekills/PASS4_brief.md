# #513 pass 4 -- the CLOSING pass.  Verify the ENUMERATION, do not hunt cells.

**VERDICT LINE FIRST:** does the chain close?

## 0. WHAT THIS PASS IS, AND WHY IT IS DIFFERENT

Passes 2 and 3 both found breaches **of one class** -- a latch-collision on the edited line.  That
triggers the repair-chain rule's class-closure amendment:

> *When two consecutive passes find breaches of one class, the next repair owes the CLASS CLOSURE:
> enumerate the full space from the function's own inputs, close every cell in ONE diff, and write
> into the contract which cells are covered and which are deliberately not.  **The closing pass then
> VERIFIES THE ENUMERATION rather than hunting cells.***

**So the question is not "find me another mutant."**  It is: **is the enumeration complete and is
the closure real?**

*** A ZERO DOES NOT CLOSE THE CHAIN UNLESS IT CARRIES ITS DENOMINATOR. ***  If you find nothing,
say what you SWEPT -- which cells, which mutant shapes.  *"Zero found"* and *"zero looked for"* must
not render the same.

**Please do not simply ratify.**  Four of five seats said DO NOT CLOSE last pass and they were right.

Tree: `GXEMUL-SEC/src/`.  Everything needed is inlined; several seats here cannot read files.

## 1. THE ENUMERATION BEING CLAIMED

`d->warned` has **twelve bits in use, 0 through 11**:

    0-5  SGIRE_W_{TLBA,TLBB,TLBC,TEX,LINA,LINB}_LEN   the six width latches
    6    SGIRE_W_DE_LEN         7  SGIRE_W_UNMAP_WR    8  SGIRE_W_UNMAP_RD
    9    SGIRE_W_PRIM_OP       10  SGIRE_W_BADMODE    11  SGIRE_W_TEX_RD   <- the one #513 added

**THE CLASS:** `SGIRE_W_TEX_RD` aliased onto any already-used bit.  Eleven cells.

**THE CLAIMED COVERAGE:**

    bits 0-5   M10, via `tex xbit` (it fired these before this round)
    bit 8      `tex/unmap` and `unmap/tex` -- both orderings, same instance
    bits 6,7,9,10   the WIDENED `tex xbit`, which now fires all eleven other latches

## 2. THE MEASUREMENTS -- every one from a log with a completion sentinel

### the first closure attempt (bits 0-8 only)
```
# #513 pass 3 -- LATCH-COLLISION CLASS CLOSURE  (clone /tmp/gx513c)

BASE_pass3   46/46   widened tex xbit (bits 0-8), CLEAN

M_bit6     45/46   KILLED   SGIRE_W_TEX_RD -> that bit
M_bit7     45/46   KILLED   SGIRE_W_TEX_RD -> that bit
M_bit9     46/46   ESCAPED  SGIRE_W_TEX_RD -> that bit
M_bit10    46/46   ESCAPED  SGIRE_W_TEX_RD -> that bit

# EXPECTED: bits 6 and 7 KILLED (the widened row co-fires them).
# bits 9 and 10 ESCAPE BY DESIGN and are DISCLOSED in the probe: they are set only from
# the drawing-engine path, which a TEX-read session never enters.  Measuring them is what
# makes the disclosure a FACT rather than a claim.
CLASSVERIFY_DONE
```

### after widening to bits 0-10 and making the row SELF-CHECKING
```
# #513 pass 3 -- LATCH-COLLISION CLASS CLOSURE  (clone /tmp/gx513e)

BASE_fixed   46/46   tex xbit widened to bits 0-10 AND made SELF-CHECKING, CLEAN
#
# *** THE 46/46 ABOVE MEANS MORE THAN THE EARLIER ONES.  The row now wants `1/11' -- the TEX
# decline once, AND all eleven other latch announces present -- so a CLEAN run PROVES the setup
# fired.  The previous 46/46 did not: it was scored against a row whose six drawing-engine stores
# passed their VALUE as the OPCODE and therefore did nothing. ***

M_bit9     45/46   KILLED   SGIRE_W_TEX_RD -> that bit
M_bit10    45/46   KILLED   SGIRE_W_TEX_RD -> that bit

# *** THIS FOOTER IS THE DRIVER'S TEMPLATE TEXT FROM THE PREVIOUS RUN AND IT IS NOW FALSE.
# It said bits 9 and 10 "ESCAPE BY DESIGN and are DISCLOSED".  THEY ARE KILLED -- see the two
# rows above it.  Left in place with this correction rather than deleted, so the sequence is
# legible; a footer contradicting the results directly above it is exactly the wrong-record
# class this round has been correcting all evening, and it appeared in a MEASUREMENT LOG. ***
#
# THE ACTUAL SEQUENCE, and the before/after is the point:
#
#   CLASSVERIFY.txt   bits 6,7 KILLED   bits 9,10 ESCAPED 46/46, disclosed in the contract
#   CLASSVERIFY2      bit 9 ESCAPED again -- but that run scored the BROKEN row (see above),
#                     so its escape is evidence of the bug, NOT of an open cell
#   CLASSVERIFY3      bits 9 and 10 BOTH KILLED 45/46 against the fixed, self-checking row
#
# So the disclosure was withdrawn and REPLACED BY COVERAGE.  Two seats had called a
# measured-open cell on the edited line a breach whatever the contract says; closing it beat
# defending it, and the settling fact I had recorded as unknown was one grep away in a shipped
# probe that already drives the drawing engine.
#
# THE CLASS IS NOW CLOSED: SGIRE_W_TEX_RD aliased onto each of the eleven other used bits of
# `d->warned' is killed -- bits 0-5 by M10, bit 8 by `tex/unmap' and `unmap/tex', and bits
# 6, 7, 9, 10 by the widened `tex xbit'.
CLASSVERIFY_DONE
```

### the bit-8 repair from pass 2
```
# #513 pass-2 L2 verification  (scratch clone /tmp/gx513b, frozen instrument)

BASE_pass2        46/46   repaired detector, CLEAN
M13_latchcollide  44/46   KILLED   SGIRE_W_TEX_RD 1<<11 -> 1<<8 (= SGIRE_W_UNMAP_RD)

# The panel PREDICTED this mutant at 44/44 against the PRE-REPAIR 44-row detector.
# That prediction is not re-measured here -- the 44-row form no longer exists.  What is
# measured is that the REPAIRED detector kills it.
L2VERIFY_DONE
```

## 3. THE REPAIR DIFF (the probe)

```diff
diff --git a/regress/sgi_re_width_probe.py b/regress/sgi_re_width_probe.py
index f1e45ad..ae5c239 100644
--- a/regress/sgi_re_width_probe.py
+++ b/regress/sgi_re_width_probe.py
@@ -28,6 +28,15 @@
 #      * silent removal of the six READ kills or of the final catch-all, which
 #        this round deliberately does NOT touch  (`<s> ld kill' x6, `other kill').
 #
+#    *** THE TWO PARAGRAPHS ABOVE ARE #497's AND #499's AND ARE NO LONGER TRUE OF THIS
+#        FILE.  #513 REMOVED ALL SIX READ KILLS -- five arms became ACCEPTs and
+#        CRIME_RE_TEX became a latched decline -- so `<s> ld kill' x6 NO LONGER EXIST
+#        as row names, and an 8-byte `ld' to those windows no longer ends the host.
+#        The contract below is the LIVE one; the text above is kept, with this
+#        correction beside it, because a reader arriving from #497's or #499's records
+#        needs to see which half moved and when.  Found by the pass-2 panel, which read
+#        the contract against the diff and reported it stale. ***
+#
 #    *** AND IT PINS THE ROUND'S CENTRAL DISCLOSURE, RATHER THAN ASSERTING IT.
 #        The width guard is evaluated FIRST, so after #497 a 4-byte read
 #        DECLINES -- but an ordinary 8-byte `ld' to each of the six windows
@@ -48,6 +57,9 @@
 #        unreachable one (filed sgimtewidth);
 #      * the LINEAR out-of-bounds index itself.  Observing re_linear_b[0] being
 #        clobbered needs a READ path, and every read arm here still exit(1)s.
+#        *** THAT CLAUSE IS #497's AND IS FALSE SINCE #513: five read arms ACCEPT and
+#        CRIME_RE_TEX declines, so a READ PATH NOW EXISTS.  Whether that makes the
+#        aliasing rowable is a QUESTION FOR sgilinearoob, not a claim made here.
 #        The aliasing is pinned by offsetof in PRETABLE.out section 1.2, not by
 #        a row.  Owed to sgirekills.
 #
@@ -75,11 +87,70 @@ if not os.path.exists(DUMMY):
 CODE        = 0x80001000
 SCRATCH_RAM = 0xa0001800
 LIVE_VAL    = 0x12345678
+DE_BASE     = 0xb5002000          # DEVICE_ACCESS(sgi_de); a BYTE access fires DE_LEN
+#  Drawing-engine registers, to fire the last two latch bits.  Addresses and values COPIED from
+#  regress/sgi_re_randompixel_probe.py, which drives this path as a shipped rung-3 witness --
+#  not invented here.
+DE_MODE_DST = 0xb5002008
+DE_DRAWMODE = 0xb5002018
+DE_XVERT_0  = 0xb5002070
+DE_XVERT_1  = 0xb5002074
+DE_PRIM_ST  = 0xb5002860          # CRIME_DE_PRIMITIVE | CRIME_DE_START -- the store fires the draw
+MODE_LIN_B  = 0x1620              # LIN_B | BUFDEPTH_32 | TYPE_RGBA -> dst_mode 5, the default arm
+DRAWMODE    = 0x002000f8
+PRIM_RECT   = 0x03020000          # DE_PRIM_RECTANGLE | DE_PRIM_TB -- an IMPLEMENTED op
+PRIM_BAD    = 0x05020000          # an UNIMPLEMENTED op: only LINE and RECTANGLE of 256 exist
 DE_STATUS   = 0xb5004000
 DE_STAT_VAL = "0x1e000000"
 OUTSIDE     = 0xb5001800          # past LINEAR_B -> the final else (straggler)
 ACC_VAL     = "0x1122334455667788"
 
+#  *** THE RE-PIN VALUES (sgirekills).  VAL_HI differs from VAL_LO in every
+#  halfword lane.
+#
+#  AN EARLIER WORDING CALLED THAT "the point of having two", claiming a single
+#  value, or two sharing any lane, "would let such an edit through".  THAT
+#  OVERCLAIMED, and the pass-2 panel caught it: VAL_LO ALONE already has four
+#  DISTINCT halfwords (1122 3344 5566 7788), so it by itself reddens under a
+#  pure read-side lane permutation or duplication -- M11_lanerev reds the lo
+#  row as well as the hi one, which is the measurement that settles it.
+#
+#  What the SECOND value actually buys is narrower and still worth having: two
+#  rows cannot both be satisfied by a mutant returning one fixed constant, and
+#  the hi row exercises the window's LAST SLOT -- which is what M4 and M7
+#  measured, and neither is a lane property at all. ***
+VAL_LO      = 0x1122334455667788
+VAL_HI      = 0xa1b2c3d4e5f60718
+
+#  Each ACCEPT window gets TWO rows: one at the window BASE and one at its LAST
+#  8-byte slot.  #499 measured on THIS DEVICE that one row per arm cannot do the
+#  job -- an accept row written at a base tests the near bound twice and the far
+#  bound never, and moving it to the top merely swaps which bound is blind.
+#
+#         nm          base          array          lo_off  lo_i  hi_off  hi_i  kind
+REPIN = [
+ ("tlb_a",    0xb5001000, "re_tlb_a",    0x000, 0, 0x1f8, 252, "hw"),
+ ("tlb_b",    0xb5001200, "re_tlb_b",    0x000, 0, 0x1f8, 252, "hw"),
+ ("tlb_c",    0xb5001400, "re_tlb_c",    0x000, 0, 0x1f8, 252, "hw"),
+ ("linear_a", 0xb5001700, "re_linear_a", 0x000, 0, 0x078,  30, "w"),
+ ("linear_b", 0xb5001780, "re_linear_b", 0x000, 0, 0x078,  30, "w"),
+]
+
+TEX_BASE    = 0xb5001600
+TEX_HI_OFF  = 0x0d8               # the last 8-byte slot inside CRIME_RE_TEX + 0xe0
+TEX_RD_DECL = "unimplemented read from CRIME_RE_TEX -- declined."
+
+def anchor(arr, idx, val, kind):
+    """*** THE ANCHOR CHANNEL, clause (f). ***  The store's OWN debug() names the
+    INDEX it wrote, so this literal pins WHICH CELL the address resolved to --
+    not merely that some cell round-tripped.  A translation that slides the whole
+    window keeps every value distinct and still reddens here.  Nothing is added to
+    the READ path to make this work: the channel already exists on the write."""
+    if kind == "hw":
+        return "d->%s[%i] = 0x%04x" % (arr, idx, (val >> 48) & 0xffff)
+    return "[ d->%s[%i] = 0x%08x, [%i] = 0x%08x ]" % (
+        arr, idx, (val >> 32) & 0xffffffff, idx + 1, val & 0xffffffff)
+
 #            name        base          symbol               accept-probe text
 SITES = [
  ("tlb_a",    0xb5001000, "CRIME_RE_TLB_A",    "d->re_tlb_a[4] = 0x1122"),
@@ -99,6 +170,7 @@ def decl(sym):
 
 OP_NOP      = 0x00000000
 OP_B_SELF   = 0x1000ffff
+OP_SB_T0_A3 = 0xa0e80000          # sb   $t0, 0($a3)   -- narrow, fires a _LEN latch
 OP_SW_T0_A3 = 0xace80000          # sw   $t0, 0($a3)
 OP_SD_T0_A3 = 0xfce80000          # sd   $t0, 0($a3)
 OP_LW_V0_AT = 0x8c220000          # lw   $v0, 0($at)
@@ -206,6 +278,18 @@ t, alive, how = session(store(A, SCRATCH_RAM) + load(A, SCRATCH_RAM)
 row("live", printed(t, "v0") if alive else "died", "0x%x" % LIVE_VAL,
     "LIVENESS: guest store then load, through RAM")
 
+#  *** THE 64-BIT LIVENESS CONTROL, AND IT IS NOT DECORATION. ***  Every re-pinned
+#  ACCEPT row below asserts a 64-bit value read back through `print v0'.  On the
+#  COMMITTED build all of those rows DIE at the load, so a pre-fix run cannot tell
+#  a correct want-string from a mis-formatted one -- the red is explained by the
+#  kill either way.  This row exercises the identical sd/ld/print path through RAM,
+#  where nothing kills, so the format is pinned BEFORE the fix rather than after.
+A = Addr(CODE)
+t, alive, how = session(store(A, SCRATCH_RAM, OP_SD_T0_A3, "0x%016x" % VAL_LO)
+                        + load(A, SCRATCH_RAM, OP_LD_V0_AT) + ["print v0"])
+row("live64", printed(t, "v0") if alive else "died", "0x%x" % VAL_LO,
+    "LIVENESS: 64-bit sd/ld through RAM -- pins the re-pin want format")
+
 A = Addr(CODE)
 t, alive, how = session(load(A, DE_STATUS) + ["print v0"])
 row("devsig stat", printed(t, "v0") if alive else "died", DE_STAT_VAL,
@@ -233,6 +317,8 @@ for nm, base, sym, acctext in SITES:
     #    NOTE: the width arm is evaluated BEFORE the read arm, so a len=4 read
     #    takes the (now declining) width arm and never reaches the still-live
     #    read kill.  An 8-byte read still dies -- see `ld readkill' below.
+    #    *** BOTH HALVES FALSE SINCE #513: the 8-byte read is ACCEPTED (or, at TEX,
+    #    declined), and `ld readkill' no longer exists -- it is `<arm> ld lo|hi'.
     #    This row is what kills M1 (`len != 8 && writeflag == MEM_WRITE').
     A = Addr(CODE)
     t, alive, how = session(load(A, base) + ["print v0"])
@@ -263,15 +349,155 @@ ordered = all(p >= 0 for p in pos) and pos == sorted(pos)
 row("xsite order", "1" if ordered else "0", "1",
     "ANCHOR: message order == the order the guest issued them")
 
-# ------------------------------------------------ contract / non-regression
-#  THE LEFTOVER, MEASURED AT EVERY WINDOW rather than argued from the pairing:
-#  len == 8 passes the width guard and reaches the still-live read kill.
-for nm, base, sym, _a in SITES:
+# ------------------------------------------------ the read arms  (sgirekills)
+#
+#  *** RE-PINNED FOR sgirekills.  SIX DEATH-ONLY ROWS BECOME FOURTEEN. ***
+#
+#  THE OLD ROWS were `row(nm + " ld kill", how + txt, "exit1+txt")' -- they asserted
+#  that a len == 8 READ still ends the host at each of the six windows.  That was a
+#  true and useful pin while the kills stood.  It cannot survive the fix, which is
+#  exactly the situation the oracle-correction rule governs: the rows are re-pinned
+#  FIRST and the committed build is measured RED under the new expectations, and only
+#  then is the device edited.  Same script, opposite colour.
+#
+#  *** WHAT REPLACED THEM, AND WHY IT IS NOT THE OBVIOUS SET. ***  My first design was
+#  one row per window at the window BASE, plus a #499-style decline row for TEX.  The
+#  design panel refused it with two floor-shaped holes and one oracle this file had
+#  already measured wrong:
+#
+#    (1) THE FAR BOUND WAS UNPINNED.  An accept row at a window's base tests the near
+#        bound twice and the far bound never -- so a shrink of the window's upper limit
+#        is invisible to it.  #499 measured that on this same device.  Hence TWO rows
+#        per ACCEPT arm, base and LAST SLOT.
+#
+#    (2) A LOAD-ONLY TEX DECLINE ROW WOULD HAVE BEEN VACUOUS, and this is the sharp one.
+#        Such a row wants `v0 == 0'.  If a later round converts TEX to an ACCEPT, it will
+#        read back the ZEROED array and yield 0 as well -- so the row could not redden at
+#        the very edit it exists to catch.  The TEX rows therefore STORE a non-zero value
+#        first: an ACCEPT would return it, and the row goes red.
+#
+#    (3) `how == "exit0"' IS THE WRONG ORACLE and #499 measured why -- an exit(0)
+#        reinstatement prints its message and then dies, scoring green with the process
+#        dead.  NO RE-PINNED READ ROW below reads exit status.  (An earlier wording said
+#        "no row below", which is FALSE: the pre-existing `other decl' row DOES read `how'
+#        and wants `exit0/txt/0x0'.  That row is #499's and is out of scope here; the claim
+#        belongs to the rows this round re-pinned.)  SURVIVAL IS IMPLIED BY THE VALUE:
+#        a dead session cannot print one.
+#
+for nm, base, arr, lo_off, lo_i, hi_off, hi_i, kind in REPIN:
+    for tag, off, idx, val in (("lo", lo_off, lo_i, VAL_LO),
+                               ("hi", hi_off, hi_i, VAL_HI)):
+        A = Addr(CODE)
+        addr = base + off
+        t, alive, how = session(store(A, addr, OP_SD_T0_A3, "0x%016x" % val)
+                                + load(A, addr, OP_LD_V0_AT) + ["print v0"])
+        anc = anchor(arr, idx, val, kind)
+        got = (printed(t, "v0") if alive else "died") + ("+anc" if anc in t else "-anc")
+        row("%s ld %s" % (nm, tag), got, "0x%x+anc" % val,
+            "ACCEPT %s[%i]: value round-trips AND the store names the cell" % (arr, idx))
+
+#  *** TEX IS THE ONE ARM THAT IS NOT AN ACCEPT. ***  The other five windows have a
+#  write path that already computes and stores the value, so reading it back is the
+#  ACCEPT member of the option set.  TEX's read is DECLINED instead, and these four
+#  rows pin the decline rather than a value.  *** THE STORE-FIRST SHAPE FROM (2) ABOVE IS
+#  ON TWO OF THEM, NOT FOUR: `tex ld lo' and `tex ld hi' store a non-zero value before
+#  loading, so a future ACCEPT of TEX reddens THEM.  `tex rd lat1' is two bare loads and
+#  `tex xbit' is a latch-collision row; neither stores, and neither would redden on an
+#  ACCEPT.  An earlier wording said "these four ... with the store-first shape". ***
+for tag, off in (("lo", 0x000), ("hi", TEX_HI_OFF)):
     A = Addr(CODE)
-    t, alive, how = session(load(A, base, OP_LD_V0_AT))
-    ok_txt = ("TODO: read from " + sym) in t
-    row(nm + " ld kill", how + ("+txt" if ok_txt else "-txt"), "exit1+txt",
-        "len=8 READ STILL KILLS THE HOST here -- untouched (sgirekills)")
+    addr = TEX_BASE + off
+    val = VAL_LO if tag == "lo" else VAL_HI
+    t, alive, how = session(store(A, addr, OP_SD_T0_A3, "0x%016x" % val)
+                            + load(A, addr, OP_LD_V0_AT) + ["print v0"])
+    got = (printed(t, "v0") if alive else "died")
+    got += "+1msg" if t.count(TEX_RD_DECL) == 1 else "+%imsg" % t.count(TEX_RD_DECL)
+    row("tex ld " + tag, got, "0x0+1msg",
+        "DECLINE: reads 0 after a real store -- an ACCEPT would return the store")
+
+#  THE LATCH: one announce per instance, not one per access.  Two reads at DIFFERENT
+#  offsets, so a latch keyed on the address rather than on the arm also reddens.
+A = Addr(CODE)
+t, alive, how = session(load(A, TEX_BASE, OP_LD_V0_AT)
+                        + load(A, TEX_BASE + TEX_HI_OFF, OP_LD_V0_AT))
+row("tex rd lat1", "%i" % t.count(TEX_RD_DECL) if alive else "died", "1",
+    "LATCH: two TEX reads at two offsets announce exactly once")
+
+#  *** THE CROSS-BIT ROW.  #498 measured a latch shared between two arms scoring 23/25,
+#  and #490 measured the same collision in another file, so it is pinned here BEFORE it
+#  can bite: fire all SIX width latches -- CRIME_RE_TEX's own included -- with narrow
+#  writes, then read TEX.  If the read decline is given an existing bit rather than its
+#  own, its message is already suppressed and this row reds. ***
+#  *** CLASS CLOSURE ON THE LATCH-COLLISION AXIS -- pass 3. ***
+#
+#  This row USED TO fire only the six width latches (bits 0-5), and pass 3 showed why that is
+#  not enough: the mutation operator is `SGIRE_W_TEX_RD := <an already-used bit>' ON THE EDITED
+#  LINE, so bits 6, 7, 9 and 10 were the SAME operator on the SAME line and swept by nothing.
+#  Pass 2 found the bit-8 cell; pass 3 found the rest.  TWO CONSECUTIVE PASSES FINDING ONE CLASS
+#  is the trigger for closing the whole space in one diff rather than one cell per pass.
+#
+#      bit  latch              fired here by
+#      ---  -----------------  ---------------------------------------------------------
+#       0-5 *_LEN x6           a narrow (byte) store to each of the six RE windows
+#       6   SGIRE_W_DE_LEN     a BYTE store to the DE window -- its accept set is {4,8}
+#       7   SGIRE_W_UNMAP_WR   a store to OUTSIDE
+#       8   SGIRE_W_UNMAP_RD   a load  from OUTSIDE
+#       9   SGIRE_W_PRIM_OP    an unimplemented drawing op stored to PRIMITIVE|START
+#      10   SGIRE_W_BADMODE    an unimplemented DST MODE driven through a real rectangle
+#
+#  *** THE CLASS IS CLOSED, AND BITS 9 AND 10 WERE MEASURED OPEN BEFORE THEY WERE CLOSED. ***
+#  An earlier form of this row fired bits 0-8 and DISCLOSED 9 and 10 as unreachable-in-session,
+#  on the ground that a TEX-read session never enters the drawing-engine path.  That disclosure
+#  was MEASURED rather than asserted -- `M_bit9' and `M_bit10' both scored 46/46, a clean escape
+#  (CLASSVERIFY.txt) -- and two seats had called a measured-open cell on the edited line a breach
+#  whatever the contract says.  They were right, and the disclosure was answering the wrong
+#  question: not "does a TEX session normally draw?" but "CAN one?"  It can, in six stores.
+#  The settling fact I had written down as unknown turned out to be one grep away, in a shipped
+#  probe that already drives this path.
+A = Addr(CODE)
+cmds = []
+for _nm, _b, _sym, _a in SITES:
+    cmds += store(A, _b, OP_SB_T0_A3, "0x1")          # bits 0-5
+cmds += store(A, DE_BASE, OP_SB_T0_A3, "0x1")         # bit 6
+cmds += store(A, OUTSIDE, OP_SB_T0_A3, "0x1")         # bit 7
+cmds += load(A, OUTSIDE, OP_LW_V0_AT)                 # bit 8
+#  *** THE SIX CALLS BELOW ONCE PASSED THEIR VALUE AS THE OPCODE. ***  `store()' is
+#  `store(A, addr, op=OP_SW_T0_A3, val="0x12345678")', so `store(A, DE_MODE_DST, MODE_LIN_B)'
+#  assembled MODE_LIN_B as an INSTRUCTION and wrote the default value to the register.  All six
+#  were wrong the same way, and **the row still scored 46/46**, because its oracle is only the TEX
+#  decline count -- which garbage stores do not disturb.  A row that passes while doing nothing it
+#  claims is exactly the vacuity the floor exists to prevent; it was caught by a reading seat, not
+#  by a measurement.  Pass the value as `val', never positionally as `op'.
+#
+#  bit 10 SGIRE_W_BADMODE -- an unimplemented DST MODE driven through a REAL rectangle, so
+#  horrible_getputpixel is actually entered.  The vertex pair is (0,0)-(0,3): the HEIGHT is what
+#  makes the primitive iterate, which sgi_re_randompixel_probe.py measured and documents.
+cmds += store(A, DE_MODE_DST, OP_SW_T0_A3, "0x%x" % MODE_LIN_B)
+cmds += store(A, DE_DRAWMODE, OP_SW_T0_A3, "0x%x" % DRAWMODE)
+cmds += store(A, DE_XVERT_0,  OP_SW_T0_A3, "0x0")
+cmds += store(A, DE_XVERT_1,  OP_SW_T0_A3, "0x3")
+cmds += store(A, DE_PRIM_ST,  OP_SW_T0_A3, "0x%x" % PRIM_RECT)
+#  bit 9 SGIRE_W_PRIM_OP -- an unimplemented drawing OP.  draw_primitive's switch rejects it
+#  before any pixel work, so this needs no vertex setup of its own.
+cmds += store(A, DE_PRIM_ST,  OP_SW_T0_A3, "0x%x" % PRIM_BAD)
+cmds += load(A, TEX_BASE, OP_LD_V0_AT)
+t, alive, how = session(cmds, spin=4.0)
+
+#  *** THE ROW PROVES ITS OWN SETUP.  This is the repair for the defect that made it vacuous. ***
+#  Counting only the TEX decline cannot distinguish "ten latches fired and TEX still announced"
+#  from "the setup did nothing and TEX announced".  Both give 1.  So the row also reports HOW MANY
+#  of the other announces it actually saw, and wants ALL of them: a setup that silently fails --
+#  a mistyped call, a moved register, a changed message -- now REDS this row instead of passing it.
+SETUP_LIT = ([decl(sym) for _n, _b, sym, _a in SITES] +          # bits 0-5, the six *_LEN
+             ["[ sgi_de: unimplemented len=",                    # bit 6  DE_LEN
+              "unimplemented write to address 0x1800",           # bit 7  UNMAP_WR
+              "unimplemented read from address 0x1800",          # bit 8  UNMAP_RD
+              "UNIMPLEMENTED drawing op",                        # bit 9  PRIM_OP
+              "unimplemented dst_mode"])                         # bit 10 BADMODE
+fired = sum(1 for lit in SETUP_LIT if lit in t)
+row("tex xbit", "%i/%i" % (t.count(TEX_RD_DECL), fired) if alive else "died",
+    "1/%i" % len(SETUP_LIT),
+    "CROSSBIT: all 11 other latches PROVEN fired; TEX read still announces once")
 
 A = Addr(CODE)
 #  *** RE-PINNED BY #499, WHICH REMOVED THIS KILL.  Three channels replace one, and
@@ -320,6 +546,33 @@ got = "%s/%s/%s" % (how, "txt" if t.count(DECL_W) == 1 else "notxt",
 row("other decl", got, "exit0/txt/0x0",
     "#499: declines, announces once, declined read lands a defined 0")
 
+#  *** L2 -- A FLOOR BREACH FOUND BY THE PASS-2 PANEL, REPAIRED IN-ROUND. ***
+#
+#  Clause (d)'s DEPENDS-ON closure includes `d->warned', and -- AT THE TIME OF PASS 2 --
+#  `tex xbit' swept the six *_LEN bits only.  (It now fires bits 0-10; see that row.  The
+#  past tense is deliberate: this paragraph records why the repair was needed.)  The panel named the escape and predicted its score: give the TEX
+#  read decline an ALREADY-USED NON-LEN bit --
+#
+#      SGIRE_W_TEX_RD = 1 << 11   ->   1 << 8   (= SGIRE_W_UNMAP_RD)
+#
+#  -- and the 44-row detector scores a CLEAN SWEEP, because its four TEX-read scenarios
+#  and its unmapped-read scenario NEVER SHARE AN EMULATOR INSTANCE.  `tex xbit' sets bits
+#  0-5, so bit 8 is clear in every session that reads TEX.  M10 established detection of a
+#  WIDTH-bit collision, not of every existing-bit collision.
+#
+#  The repair is a SAME-INSTANCE sequence in BOTH orderings: whichever announce fires
+#  first must not suppress the other.  One ordering alone would leave the mirror open --
+#  the `#499' shape, where a repair closes the cell the mutant used and leaves its twin.
+DECL_R = "unimplemented read from address 0x1800 -- declined.  (once) ]"
+
+for nm, first, second in (("tex/unmap", TEX_BASE, OUTSIDE),
+                          ("unmap/tex", OUTSIDE, TEX_BASE)):
+    A = Addr(CODE)
+    t, alive, how = session(load(A, first, OP_LD_V0_AT) + load(A, second, OP_LD_V0_AT))
+    got = "%i/%i" % (t.count(TEX_RD_DECL), t.count(DECL_R)) if alive else "died"
+    row(nm, got, "1/1",
+        "LATCH INDEPENDENCE: both announces fire in ONE instance, either order")
+
 ok = sum(1 for _, o in rows if o)
 print("")
 print("OPUS497T_RESULT=%d/%d" % (ok, len(rows)))
```

## 4. QUESTIONS

**Q1. IS THE ENUMERATION COMPLETE?**  Twelve bits, eleven cells.  **Is `d->warned` really the only
lvalue in this closure that admits an aliasing mutant** -- or is there a second field with the same
shape that I have not enumerated at all?

**Q2. IS THE CLOSURE REAL, or does it only look real?**  `tex xbit` now asserts `1/11`: the TEX
decline once, and all eleven other announces present.  **Can that row pass while the latch behaviour
is wrong?**  Note what it replaced: a version whose six drawing-engine stores passed their VALUE as
the OPCODE, did nothing, and still scored 46/46 -- caught by a reading seat, invisible to every
mutant, because all mutants scored against the same broken row.

**Q3. Is the SELF-CHECK itself sound?**  It counts literal substrings in the session log.  **Name a
way that count could read 11 while a latch did not actually fire** -- a message emitted from
elsewhere, a substring that matches two sites, an announce from a previous row leaking in.

**Q4. Did closing bits 9 and 10 COST anything?**  The row now drives the drawing engine -- a mode
write, a drawmode, two vertices, and two PRIMITIVE|START stores -- inside the same session as the
TEX read.  **Does that make the row load-sensitive, order-dependent, or coupled to `sgirandomcolour`
and `sgirebufuninit`, which are open rows against that very path?**

**Q5. DOES THE CHAIN CLOSE?**  If yes, say so with your denominator.  If no, the finding is L2 and
gets repaired in-round however late it is.
