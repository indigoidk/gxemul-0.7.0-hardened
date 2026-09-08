# #513 sgirekills -- PASS 2 on the real diff

**VERDICT LINE FIRST.**  One line at the top saying ship / do not ship, so it survives truncation.

**Please do not simply ratify.**  A recent panel had seven of nine seats confirm a premise a brief
had stated wrongly.  **Check the premises, not just the derivations** -- including the measured
claims below, which are mine and which you should treat as claims.

The tree under review is `GXEMUL-SEC/src/`.  There is another `src/` at the project root which is
pristine 2021 upstream -- ignore it.  Line numbers off by hundreds mean you have that copy.
**Everything you need is inlined; several seats here cannot open files at all.**

## 1. WHAT THE ROUND DID

`dev_sgi_re.c` had SIX read arms of the form

    } else {
            fatal("TODO: read from CRIME_RE_TLB_A\n");
            exit(1);
    }

each on the `else` of a `writeflag == MEM_WRITE` test, in a window whose WRITE path is fully
modelled.  A guest could store a value and reading it back ended the emulator.

**Five became ACCEPT** (member 4 of the option set: the write arm already computes and stores the
value, so the read returns it).  **`CRIME_RE_TEX` became a latched DECLINE** on a new bit
`SGIRE_W_TEX_RD`, because `sgitexindex` records that its write index `>> 3` is a missing factor of
four against a flat `uint16_t[112]`, only 31 of 112 cells are reachable, `re_tex` has NO consumer
anywhere in the file, and `sgitexindex` carries a standing do-not-code ruling.

## 2. SETTLED PREMISES -- measurements, with their logs named

    committed build, re-pinned oracles   30/44    PREFIX_RED_20260908.out
    after the fix, SAME script           44/44   POSTFIX_20260908.out

All red rows on the pre-fix run were NEW rows; every pre-existing row stayed green and all three
controls were green.  A `live64` control was added precisely because on the committed build every
re-pinned ACCEPT row DIES at the load, so a pre-fix run could not otherwise tell a correct
want-string from a mis-formatted one.

**The detector went 35 -> 44 rows** and `gate_arm.sh`'s row list and BOTH denominators were raised
in the same commit.

## 3. THE KILL TABLE -- 12 mutants, scratch clone, frozen instrument

```
# #513 sgirekills -- kill table 1   (scratch clone /tmp/gx513, frozen instrument)
# baseline BASE 44/44   (from BASE.raw, re-derived)
#
# *** THIS LINE READ "42/44" WHEN THE TABLE WAS WRITTEN, WHICH IS M12_linswap's SCORE, NOT THE
# BASELINE'S.  My summary block reused the loop variables `n, d' after the mutant loop had
# reassigned them, so the header printed the LAST mutant's numbers under the baseline's
# label.  Corrected 2026-09-08 by re-deriving from BASE.raw.
#
# The real baseline was provably clean regardless: the driver exits with
#   "*** BASELINE NOT CLEAN -- table uninterpretable"
# unless numerator == denominator, and it did not exit.  BASE.raw confirms 44/44 with its
# completion sentinel present.
#
# Same class as the variable-shadowing bug that made this session's gate-edit script report
# "+616 re-pinned" rows.  Both were caught by checking the OUTPUT against an independent
# source rather than trusting the script that produced it.

mutant          score    floor  verdict   what it is
M1_reinstate6   30/44    (b)    KILLED    restore fatal()+exit(1) at ALL SIX read arms, verbatim
M2_datafill     42/44    (d)    KILLED    fill data[] instead of odata -- the tail overwrites it (the bug I nearly shipped)
M3_noincr       42/44    (d)    KILLED    drop the tlbi++ -- four copies of one cell
M4_readshift    43/44    (d)    KILLED    read-side index re-map >> 1 -> >> 2, write side untouched
M5_shortloop    42/44    (d)    KILLED    shorten the read loop; the guard still tests len != 8
M6_translate    41/44    (f)    KILLED    ANCHOR: +1 translation on BOTH store and read in TLB_A
M7_farbound     43/44    (f)    KILLED    FAR-BOUND shrink of TLB_A -- invisible to a row at the window base
M8_texaccept    40/44    (d)    KILLED    convert TEX to ACCEPT -- what the store-first TEX rows exist to catch
M9_texnolatch   43/44    (d)    KILLED    remove the latch: announce per access instead of per instance
M10_texbit      43/44    (d)    KILLED    CROSS-BIT: give the read decline the WIDTH latch instead of its own
M11_lanerev     42/44    (d)    KILLED    reverse the halfword lane order -- VAL_HI differs in every lane
M12_linswap     42/44    (d)    KILLED    swap the two LINEAR_A words -- the fixed-arity analogue of M11

NOT KILLED: none
KILLTABLE_DONE
```

## 4. THE DIFF

### src/devices/dev_sgi_re.c

```diff
diff --git a/src/devices/dev_sgi_re.c b/src/devices/dev_sgi_re.c
index 2f8b77f..e5a329e 100644
--- a/src/devices/dev_sgi_re.c
+++ b/src/devices/dev_sgi_re.c
@@ -130,6 +130,16 @@ enum {
 	    The next free bit is 1 << 11; the enum ends HERE on purpose, as
 	    above.  */
 	SGIRE_W_BADMODE   = 1 << 10,
+
+	/*
+	    #513: THE TEX READ DECLINE GETS ITS OWN BIT, not SGIRE_W_TEX_LEN.
+	    Sharing one was measured at 23/25 for SGIRE_W_DE_LEN in #498: an
+	    ordinary narrow write fires the width latch, and the read decline is
+	    then silently suppressed for the life of the instance.  The detector
+	    has a row for exactly this (`tex xbit', which fires all six width
+	    latches before reading).
+	 */
+	SGIRE_W_TEX_RD    = 1 << 11,
 };
 
 struct sgi_re_data {
@@ -398,6 +408,12 @@ DEVICE_ACCESS(sgi_re)
 	 *     `rd sent' row exists to pin exactly that.  The six `TODO: read from'
 	 *     arms below DO still exit(1) -- that half is unchanged and is sgirekills. ***
 	 *
+	 *     *** AND THAT HALF IS NOW GONE TOO: #513 REMOVED ALL SIX.  The tail is
+	 *     reached by more than declines now -- five of the six arms ASSIGN odata
+	 *     and let the tail deliver it, so the tail is the ACCEPT path as well as
+	 *     the decline path.  The sentence above is #499's and was true when
+	 *     written; it stands with its correction, as #499's own does. ***
+	 *
 	 *  3. The guards are NOT redundant.  For TLB_A/B/C and TEX the store is a
 	 *     `for (hwi = 0; hwi < len; ...)' loop, so a narrower access simply
 	 *     runs fewer iterations and stays in bounds -- there the guard is
@@ -407,6 +423,12 @@ DEVICE_ACCESS(sgi_re)
 	 *  Only the WIDTH kills change HERE, IN #497.  The six `TODO: read from ...'
 	 *  kills are still untouched.
 	 *
+	 *  *** UNTRUE SINCE #513, WHICH IS THE ROUND THAT TOOK THEM.  Five became
+	 *  ACCEPTs (the read returns what the write stored) and CRIME_RE_TEX became a
+	 *  latched decline.  #497's sentence was accurate for #497 and is kept for the
+	 *  same reason the catch-all correction below is kept: a reader arriving from
+	 *  #497's records has to be able to see which half moved and when. ***
+	 *
 	 *  *** THE CATCH-ALL IS NO LONGER UNTOUCHED: #499 DE-FATALISED IT and that row
 	 *  is CLOSED.  The sentence is #497's and was true when written; it is left
 	 *  standing with its correction rather than rewritten, because a reader
@@ -433,8 +455,28 @@ DEVICE_ACCESS(sgi_re)
 				tlbi++;
 			}
 		} else {
-			fatal("TODO: read from CRIME_RE_TLB_A\n");
-			exit(1);
+			/*
+			 *  #513: ACCEPT.  A guest read of a len == 8 TLB slot ended
+			 *  the host.  The write arm directly above already computes
+			 *  and stores the value, so the disposition is member 4 of
+			 *  the option set -- delete the kill and RETURN THE VALUE --
+			 *  rather than a decline: nothing is unimplemented here.
+			 *  This loop is the exact inverse of the write loop, cell for
+			 *  cell and shift for shift.
+			 *
+			 *  *** IT MUST WRITE odata, NOT data[]. ***  The function's
+			 *  common tail is
+			 *      if (writeflag == MEM_READ)
+			 *              memory_writemax64(cpu, data, len, odata);
+			 *  so anything stored into data[] here is overwritten before
+			 *  it reaches the guest.  A first draft of this fix filled
+			 *  data[] and would have returned zeroes while looking right.
+			 */
+			int tlbi = ((relative_addr & 0x1ff) >> 1) & 0xff;
+			for (size_t hwi = 0; hwi < len; hwi += sizeof(uint16_t)) {
+				odata = (odata << 16) | d->re_tlb_a[tlbi];
+				tlbi++;
+			}
 		}
 	} else if (relative_addr >= CRIME_RE_TLB_B && relative_addr < CRIME_RE_TLB_C) {
 		if (len != 8) {
@@ -452,8 +494,13 @@ DEVICE_ACCESS(sgi_re)
 				tlbi++;
 			}
 		} else {
-			fatal("TODO: read from CRIME_RE_TLB_B\n");
-			exit(1);
+			/*  #513: ACCEPT -- the inverse of the write loop.  See the
+			    CRIME_RE_TLB_A arm for why this sets odata, not data[].  */
+			int tlbi = ((relative_addr & 0x1ff) >> 1) & 0xff;
+			for (size_t hwi = 0; hwi < len; hwi += sizeof(uint16_t)) {
+				odata = (odata << 16) | d->re_tlb_b[tlbi];
+				tlbi++;
+			}
 		}
 	} else if (relative_addr >= CRIME_RE_TLB_C && relative_addr < CRIME_RE_TLB_C + 0x200) {
 		if (len != 8) {
@@ -471,8 +518,13 @@ DEVICE_ACCESS(sgi_re)
 				tlbi++;
 			}
 		} else {
-			fatal("TODO: read from CRIME_RE_TLB_C\n");
-			exit(1);
+			/*  #513: ACCEPT -- the inverse of the write loop.  See the
+			    CRIME_RE_TLB_A arm for why this sets odata, not data[].  */
+			int tlbi = ((relative_addr & 0x1ff) >> 1) & 0xff;
+			for (size_t hwi = 0; hwi < len; hwi += sizeof(uint16_t)) {
+				odata = (odata << 16) | d->re_tlb_c[tlbi];
+				tlbi++;
+			}
 		}
 	} else if (relative_addr >= CRIME_RE_TEX && relative_addr < CRIME_RE_TEX + 0xe0) {
 		if (len != 8) {
@@ -490,8 +542,34 @@ DEVICE_ACCESS(sgi_re)
 				tlbi++;
 			}
 		} else {
-			fatal("TODO: read from CRIME_RE_TEX\n");
-			exit(1);
+			/*
+			 *  #513: DECLINE + LATCHED ANNOUNCE -- and TEX is the ONE arm
+			 *  of the six that is NOT an accept.  The warrant is specific
+			 *  and is recorded as `sgitexindex':
+			 *
+			 *    - the write arm's index is `>> 3' where a flat
+			 *      uint16_t[112] incremented once per halfword needs the
+			 *      register number times four.  The SGI CRIME specification
+			 *      lists TLB.tex[28] as 28 separate 64-bit registers, so
+			 *      `>> 3' is the REGISTER number and the missing factor of
+			 *      four is the defect;
+			 *    - consequently only 31 of the 112 cells are reachable and
+			 *      consecutive registers overlap by three;
+			 *    - `re_tex' has NO consumer anywhere in this file -- it is
+			 *      written and debug-printed, never read back.
+			 *
+			 *  Accepting the read would therefore publish a mapping the
+			 *  project has already recorded as wrong, and turn a future
+			 *  sgitexindex fix into a breaking change to a shipped oracle.
+			 *  Declining costs nothing today (no consumer) and leaves that
+			 *  round free.  sgitexindex carries a standing do-not-code
+			 *  ruling, so this round does not touch the shift.
+			 */
+			if (!(d->warned & SGIRE_W_TEX_RD)) {
+				d->warned |= SGIRE_W_TEX_RD;
+				fatal("[ sgi_re: unimplemented read from "
+				    "CRIME_RE_TEX -- declined.  (once) ]\n");
+			}
 		}
 	} else if (relative_addr >= CRIME_RE_LINEAR_A && relative_addr < CRIME_RE_LINEAR_A + 0x80) {
 		if (len != 8) {
@@ -582,8 +660,20 @@ DEVICE_ACCESS(sgi_re)
 			debug("[ d->re_linear_a[%i] = 0x%08x, [%i] = 0x%08x ]\n",
 				tlbi, d->re_linear_a[tlbi], tlbi+1, d->re_linear_a[tlbi+1]);
 		} else {
-			fatal("TODO: read from CRIME_RE_LINEAR_A\n");
-			exit(1);
+			/*
+			 *  #513: ACCEPT -- the inverse of the fixed-arity write
+			 *  directly above.  See CRIME_RE_TLB_A for the odata note.
+			 *
+			 *  The [tlbi+1] here has the SAME exposure as the write's
+			 *  [tlbi+1] and no more: both are bounded only by the len == 8
+			 *  guard keeping tlbi even, which is `sgilinearoob'.  This fix
+			 *  deliberately does NOT add a clamp -- an unlicensed addition
+			 *  here would change the index behaviour that sgilinearoob is
+			 *  filed to fix across all five arms with ONE design.
+			 */
+			int tlbi = ((relative_addr & 0x7f) >> 2) & 0x1f;
+			odata = ((uint64_t) d->re_linear_a[tlbi] << 32)
+			    | d->re_linear_a[tlbi+1];
 		}
 	} else if (relative_addr >= CRIME_RE_LINEAR_B && relative_addr < CRIME_RE_LINEAR_B + 0x80) {
 		if (len != 8) {
@@ -640,8 +730,20 @@ DEVICE_ACCESS(sgi_re)
 			debug("[ d->re_linear_b[%i] = 0x%08x, [%i] = 0x%08x ]\n",
 				tlbi, d->re_linear_b[tlbi], tlbi+1, d->re_linear_b[tlbi+1]);
 		} else {
-			fatal("TODO: read from CRIME_RE_LINEAR_B\n");
-			exit(1);
+			/*
+			 *  #513: ACCEPT -- the inverse of the fixed-arity write
+			 *  directly above.  See CRIME_RE_TLB_A for the odata note.
+			 *
+			 *  The [tlbi+1] here has the SAME exposure as the write's
+			 *  [tlbi+1] and no more: both are bounded only by the len == 8
+			 *  guard keeping tlbi even, which is `sgilinearoob'.  This fix
+			 *  deliberately does NOT add a clamp -- an unlicensed addition
+			 *  here would change the index behaviour that sgilinearoob is
+			 *  filed to fix across all five arms with ONE design.
+			 */
+			int tlbi = ((relative_addr & 0x7f) >> 2) & 0x1f;
+			odata = ((uint64_t) d->re_linear_b[tlbi] << 32)
+			    | d->re_linear_b[tlbi+1];
 		}
 	} else {
 		if (writeflag == MEM_WRITE) {
```

### regress/sgi_re_width_probe.py

```diff
diff --git a/regress/sgi_re_width_probe.py b/regress/sgi_re_width_probe.py
index f1e45ad..b3b6251 100644
--- a/regress/sgi_re_width_probe.py
+++ b/regress/sgi_re_width_probe.py
@@ -80,6 +80,42 @@ DE_STAT_VAL = "0x1e000000"
 OUTSIDE     = 0xb5001800          # past LINEAR_B -> the final else (straggler)
 ACC_VAL     = "0x1122334455667788"
 
+#  *** THE RE-PIN VALUES (sgirekills).  VAL_HI DIFFERS FROM VAL_LO IN EVERY
+#  HALFWORD LANE, which is the point of having two: a lane-swapping or
+#  lane-duplicating edit cannot round-trip both.  A single value, or two values
+#  sharing any lane, would let such an edit through. ***
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
@@ -206,6 +242,18 @@ t, alive, how = session(store(A, SCRATCH_RAM) + load(A, SCRATCH_RAM)
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
@@ -263,15 +311,87 @@ ordered = all(p >= 0 for p in pos) and pos == sorted(pos)
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
+#        dead.  No row below reads exit status.  SURVIVAL IS IMPLIED BY THE VALUE:
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
+#  rows pin the decline rather than a value -- with the store-first shape from (2)
+#  above, so a future ACCEPT of TEX reddens them instead of sliding past.
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
+A = Addr(CODE)
+cmds = []
+for _nm, _b, _sym, _a in SITES:
+    cmds += store(A, _b, OP_SW_T0_A3, "0x1")
+cmds += load(A, TEX_BASE, OP_LD_V0_AT)
+t, alive, how = session(cmds, spin=2.0)
+row("tex xbit", "%i" % t.count(TEX_RD_DECL) if alive else "died", "1",
+    "CROSSBIT: all six len latches fired first; TEX read still announces once")
 
 A = Addr(CODE)
 #  *** RE-PINNED BY #499, WHICH REMOVED THIS KILL.  Three channels replace one, and
```

### regress/gate_arm.sh

```diff
diff --git a/regress/gate_arm.sh b/regress/gate_arm.sh
index 211a6b7..108d670 100644
--- a/regress/gate_arm.sh
+++ b/regress/gate_arm.sh
@@ -1167,7 +1167,7 @@ else
     #  CONTROLS BY NAME, not by count.  A green-row total lets a control go red while the
     #  sum stays acceptable -- and a run whose controls died is an APPARATUS failure, which
     #  must not be read as a wall of product failures.
-    for c in "live" "devsig stat"; do
+    for c in "live" "live64" "devsig stat"; do
         check "sgi_re control: $c" "$(count "$SGILOG" "^$c  .*ok$")" "1"
     done
     check "sgi_re controls live" \
@@ -1178,13 +1178,20 @@ else
     #  makes a check UNSATISFIABLE and the row quietly stops being tested.
     #  The list is ONE LINE on purpose -- a backslash-continued list assembled through
     #  nested quoting once gained a bogus word `n` and shipped a RED gate.
-    for v in "live" "devsig stat" "tlb_a sw surv" "tlb_a sw lat1" "tlb_a lw surv" "tlb_a accept" "tlb_b sw surv" "tlb_b sw lat1" "tlb_b lw surv" "tlb_b accept" "tlb_c sw surv" "tlb_c sw lat1" "tlb_c lw surv" "tlb_c accept" "tex sw surv" "tex sw lat1" "tex lw surv" "tex accept" "linear_a sw surv" "linear_a sw lat1" "linear_a lw surv" "linear_a accept" "linear_b sw surv" "linear_b sw lat1" "linear_b lw surv" "linear_b accept" "xsite 6msg" "xsite order" "tlb_a ld kill" "tlb_b ld kill" "tlb_c ld kill" "tex ld kill" "linear_a ld kill" "linear_b ld kill" "other decl"; do
+    for v in "live" "devsig stat" "tlb_a sw surv" "tlb_a sw lat1" "tlb_a lw surv" "tlb_a accept" "tlb_b sw surv" "tlb_b sw lat1" "tlb_b lw surv" "tlb_b accept" "tlb_c sw surv" "tlb_c sw lat1" "tlb_c lw surv" "tlb_c accept" "tex sw surv" "tex sw lat1" "tex lw surv" "tex accept" "linear_a sw surv" "linear_a sw lat1" "linear_a lw surv" "linear_a accept" "linear_b sw surv" "linear_b sw lat1" "linear_b lw surv" "linear_b accept" "xsite 6msg" "xsite order" "other decl" "live64" "tlb_a ld lo" "tlb_a ld hi" "tlb_b ld lo" "tlb_b ld hi" "tlb_c ld lo" "tlb_c ld hi" "linear_a ld lo" "linear_a ld hi" "linear_b ld lo" "linear_b ld hi" "tex ld lo" "tex ld hi" "tex rd lat1" "tex xbit"; do
         check "sgi_re row: $v" "$(count "$SGILOG" "^$v  .*ok$")" "1"
     done
 
     #  DENOMINATOR PINNED TO A LITERAL.  A detector that loses rows must not be able to pass
     #  by shrinking, and the count is the only thing that says so.  Raise it DELIBERATELY.
-    #  Both halves pinned: 35 rows emitted AND all 35 green.  Two rows rather than one,
+    #  Both halves pinned: 44 rows emitted AND all 44 green.
+    #  *** RAISED 35 -> 44 BY #513, DELIBERATELY, IN THE SAME COMMIT AS THE FIX. ***
+    #  The six `<arm> ld kill' rows are GONE -- they asserted that a len == 8 READ still
+    #  ends the host at each window, which was true until #513 removed those kills.  They
+    #  are replaced by TWO anchored ACCEPT rows per accepting arm (window base AND last
+    #  slot, because a row at the base tests the near bound twice and the far bound never),
+    #  four CRIME_RE_TEX decline rows, and a 64-bit liveness control.  Arithmetic:
+    #  35 - 6 + 14 + 1 = 44.  Two rows rather than one,
     #  because a single "35 ok" check cannot tell a LOST row from a FAILING one -- and
     #  those need different responses.
     #  *** THE FIRST DRAFT OF THIS BLOCK HAD TWO DEFECTS, BOTH FOUND BY THE PASS-2 SEAT.
@@ -1204,8 +1211,8 @@ else
     #  Summed ARITHMETICALLY instead, which needs no regex dialect at all -- and unlike the
     #  string-concatenation form it replaces, it cannot be satisfied by (3 ok, 50 FAIL).
     check "sgi_re rows emitted" \
-          "$(( $(count "$SGILOG" " ok$") + $(count "$SGILOG" " FAIL$") ))" "35"
-    check "sgi_re rows green"   "$(count "$SGILOG" " ok$")"   "35"
+          "$(( $(count "$SGILOG" " ok$") + $(count "$SGILOG" " FAIL$") ))" "44"
+    check "sgi_re rows green"   "$(count "$SGILOG" " ok$")"   "44"
     check "sgi_re rows red"     "$(count "$SGILOG" " FAIL$")" "0"
 
 fi
```


## 5. QUESTIONS

**Q1. VACUITY FLOOR.**  (a) fails pre-fix -- shown above.  (b) verbatim reinstatement at every fixed
site -- `M1_reinstate6`.  (c) identity rows -- `live`, `live64`, `devsig stat`.  (d) NULL-REPAIR:
keep the guard, null its effect.  **Is the (d) enumeration COMPLETE?**  The DEPENDS-ON closure is
the predicates DOMINATING the edited lines walked to the enclosing function only, plus operand swaps
drawn from fields the guarded BODY reads.  I enumerated: `writeflag` (the arm is its `else`), `len`
(the read loop's bound), `relative_addr` (the index), the arrays, and `d->warned` for TEX.  **Name a
cell I missed, or say the closure is complete and why.**

**Q2. THE ASK-AGAIN.**  The table above is clean.  **Give me one more mutant** -- the smallest edit
that breaks a property this detector claims and still passes.  This is the single capped adversarial
query, and measured yield says it is where the real escapes come from.

**Q3. THE `odata` TRAP.**  The function's common tail is
`if (writeflag == MEM_READ) memory_writemax64(cpu, data, len, odata);`.  A first draft of this fix
filled `data[]` and would have returned zeroes while looking correct; `M2_datafill` is that mutant.
**Is there any OTHER path in this diff where a value is computed and then discarded by the tail?**

**Q4. THE ANCHOR.**  Clause (f): the ACCEPT rows assert the store's own `debug()` naming the INDEX
(`d->re_tlb_a[252] = 0xa1b2`), so they pin WHICH CELL rather than merely that some cell
round-tripped.  **If every address in this device shifted one word, which row reds?**  If the answer
is none, position is unpinned whatever the row count.

**Q5. THE TEX DISPOSITION.**  Is DECLINE right, or should TEX have been an ACCEPT like its five
siblings?  The asymmetry is deliberate and its warrant is in section 1.  **Argue against it if you
can** -- and note the TEX rows STORE a non-zero value before loading, specifically so that a future
ACCEPT would return it and redden them rather than sliding past a load-only `v0 == 0` oracle.

**Q6. RECORDS.**  Two comment paragraphs asserting the read kills were "still untouched" were
corrected in place beside their originals.  **Is anything else in this file now a wrong record?**
