"""#483 L1: three defects in this round's own new rows, all named by the kimi-k3:cloud seat.

  1. THE SWEEP REPORTS A LITERAL DENOMINATOR.  `if (d.inbuf == NULL) continue;` then an
     unconditional `rows++` and a hardcoded "256 of 256".  Zero iterations reports a full
     pass -- and unlike both sibling rows it does not `return`, so the row-count tripwire
     cannot catch a sweep-local allocation failure either.
     *** THE ROW'S OWN COMMENT WARNS ABOUT THIS SHAPE AND THE ROW REPRODUCES IT. ***

  2. THE ORPHAN ROW'S LIVENESS CONTROL GUARDS THE WRONG THREAT.  It excludes "the bytes
     were never staged" but NOT "the device purges on ANY altstatus write" -- the live leg
     performs no altstatus access at all, so a purge-on-bare-nIEN mutant sails through.
     The missing third leg: the same stores, then a WDCTL_4BIT-only write (bit 2 CLEAR),
     asserting the bytes SURVIVE.

  3. A THRESHOLD ESCAPE: the row stages exactly 16 bytes, so `occ > 8` passes everything
     while leaving any small orphan ring stale.  Closed by staging TWO sizes -- the same
     move the sweep makes against the mask family: pin a SPACE, not a point.

The filename carries `author_` because a seat destroyed an unprefixed generator of mine
last round.
"""
import io

NL, T, BS = chr(10), chr(9), chr(92)
N = BS + "n"
P = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\regress\diff_wdc_identify.c"
s = io.open(P, encoding="utf-8", newline="").read()


def within(fn, nxt, old, new, label):
    global s
    a = s.index("static void %s(void)" % fn)
    b = s.index("static void %s(void)" % nxt)
    body = s[a:b]
    c = body.count(old)
    assert c == 1, "%s: anchor occurs %d times inside %s" % (label, c, fn)
    s = s[:a] + body.replace(old, new, 1) + s[b:]
    print("  %s" % label)


#  ---- (1) the sweep: a REAL denominator, and no silent skip -------------------
within("row_reset_bit_iff", "row_arm_overrun",
 T + "int v, wide = -1, narrow = -1;" + NL,
 T + "int v, ran = 0, wide = -1, narrow = -1;" + NL,
 "(1a) sweep: iteration counter declared")

within("row_reset_bit_iff", "row_arm_overrun",
 T*2 + "altctl_fresh(&d);" + NL +
 T*2 + "if (d.inbuf == NULL)" + NL +
 T*3 + "continue;" + NL,
 T*2 + "altctl_fresh(&d);" + NL +
 T*2 + "if (d.inbuf == NULL)" + NL +
 T*3 + "continue;" + NL +
 T*2 + "ran ++;" + NL,
 "(1b) sweep: count the iterations that actually ran")

within("row_reset_bit_iff", "row_arm_overrun",
 T + "if (wide >= 0 || narrow >= 0) {" + NL +
 T*2 + "printf(\"  FAIL %-38s wide 0x%02x narrow 0x%02x" + BS + "n\"," + NL +
 T*2 + "    \"reset latches IFF bit 2 is set\", wide, narrow);" + NL +
 T*2 + "failures ++;" + NL +
 T + "} else {" + NL +
 T*2 + "printf(\"  ok   %-38s 256 of 256" + BS + "n\"," + NL +
 T*2 + "    \"reset latches IFF bit 2 is set\");" + NL +
 T + "}" + NL,
 T + "/*  *** THE DENOMINATOR IS COUNTED, NOT WRITTEN.  An earlier version printed a" + NL +
 T + "    LITERAL \"256 of 256\" after an unconditional rows++, with the NULL case" + NL +
 T + "    doing `continue` rather than `return` -- so a sweep in which every" + NL +
 T + "    allocation failed would have reported a full pass, and the row-count" + NL +
 T + "    tripwire could not have caught it either.  The comment above warns about" + NL +
 T + "    exactly that shape and the row reproduced it.  Named by the" + NL +
 T + "    kimi-k3:cloud seat.  A hardcoded denominator is a denominator that" + NL +
 T + "    cannot fail. ***  */" + NL +
 T + "if (wide >= 0 || narrow >= 0 || ran != 256) {" + NL +
 T*2 + "printf(\"  FAIL %-38s %i of 256, wide 0x%02x narrow 0x%02x" + BS + "n\"," + NL +
 T*2 + "    \"reset latches IFF bit 2 is set\", ran, wide, narrow);" + NL +
 T*2 + "failures ++;" + NL +
 T + "} else {" + NL +
 T*2 + "printf(\"  ok   %-38s %i of 256" + BS + "n\"," + NL +
 T*2 + "    \"reset latches IFF bit 2 is set\", ran);" + NL +
 T + "}" + NL,
 "(1c) sweep: the denominator is now measured and asserted")

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("  sweep repaired")
