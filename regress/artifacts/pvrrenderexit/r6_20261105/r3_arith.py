#!/usr/bin/env python3
"""r3_arith.py -- the pass-6 R3 arithmetic, re-done in IEEE binary64 (Python floats: round-to-nearest-even, as the build's SSE2
doubles; gate_offline.sh refuses fast-math).  Mirrors dev_pvr.c: the flat-top sweep adds dx13 per row (:964-978), simpleline's
`int x = x1` truncates toward zero (:683), the colour advances at the end of every pass (:721), the RGB565 pack (:707-713)."""
import math

def pack(r, g, b):
    c = lambda v: max(0, min(255, int(v)))
    return ((c(r) >> 3) << 11) + ((c(g) >> 2) << 5) + (c(b) >> 3)

e53, e54 = 2.0 ** -53, 2.0 ** -54
print("-1 + 2^-54 ==", -1.0 + e54, "(tie to even -1.0):", -1.0 + e54 == -1.0)
print("-1 + 2^-54 * 1.5 ==", repr(-1.0 + 1.5 * e54), "== -1 + 2^-53:", -1.0 + 1.5 * e54 == -1.0 + e53, "-> int", int(-1.0 + 1.5 * e54))
print("int(-1 + 0.25) =", int(-1.0 + 0.25), "; int(-1 + 1.0) =", int(-1.0 + 1.0), "; int(-1 + 1.5) =", int(-1.0 + 1.5), "; int(-1 + 2.0) =", int(-1.0 + 2.0))
# codex's (B) witness: [(0,50),(3,50),(3,80)], green / red / green, z 2.0
x1 = 0.0
dx13 = (3 - 0) / float(80 - 50)
for _ in range(10):
    x1 += dx13
print("row 60 start x1 =", repr(x1), "== 1 - 2^-53:", x1 == 1.0 - e53)
r1, g1, b1 = 0.0, 255.0, 0.0                       # start edge v1 -> v3: green -> green
r2, g2 = 255.0 + 10 * ((0 - 255) / 30.0), 0.0 + 10 * ((255 - 0) / 30.0)   # stop edge v2 -> v3 after ten rows
x2 = 3.0
print("stop end (r2, g2) =", (r2, g2), "; x2 - x1 =", repr(x2 - x1))
for name, start in (("fix", x1), ("variant x1 + 2^-54", x1 + e54)):
    dr, dg = (r2 - r1) / (x2 - x1), (g2 - g1) / (x2 - x1)
    r, g, b, x = r1, g1, b1, int(start)
    while x <= x2:
        if x == 1:
            print("%-20s starts at %d; (1,60) = (%g, %g, %g) -> 0x%04x" % (name, int(start), r, g, b, pack(r, g, b)))
        r += dr; g += dg; x += 1
# which x1 does c = 2^-54 move?  (int)(x1 + 2^-54) != (int)(x1) only at 1 - 2^-53 among the doubles just below each integer 1..4
for n in (1, 2, 3, 4):
    below = math.nextafter(float(n), 0.0)
    print("x1 = nextafter(%d, 0): int(x1 + 2^-54) = %d vs int(x1) = %d" % (n, int(below + e54), int(below)))
print("texturedline: int(0 + 2^-54) =", int(0 + e54), "; int(-1 + 2^-54) =", int(-1 + e54), "; int(-2 + 2^-54) =", int(-2 + e54))
print("R3_ARITH_DONE")
