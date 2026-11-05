#!/usr/bin/env python3
"""pvr_variants_AI.py -- pvrrenderexit repair 3, step 2 (2026-11-05): codex pass 3's A-I as test variants, ONE exact-text edit of the
fix each (GXEMUL-SEC dev_pvr.c == ../det_20261104/dev_pvr.c.fix, checked here), per rasterizer where codex named two
(s = simpleline, the first occurrence; t = texturedline, the second):
  A  `int x = x1` -> `int x = x1 - 1` (span start widened left)
  B  `if (x1 > x2)` -> `if (x1 > x2 + 1)` (swap threshold tightened)
  C  `if (x1 > x2)` -> `if (x1 >= x2)` (swap admits equality)
  D  `(x1 < 0 && x2 < 0)` -> `(x2 < 0 && x2 < 0)` (left clause: first operand copied from the second)
  E  `(x1 >= d->xsize && x2 >= d->xsize)` -> `(x1 >= d->xsize && x1 >= d->xsize)` (right clause: second operand copied from the first)
  F  `if (d->vram_z[ofs] <= z)` -> `if (d->vram_z[ofs] < z || (!d->zwrite_disabled && d->vram_z[ofs] == z))` (Z-off equality refused)
  G  decode `(list[1] >> 26) & 1` -> `(list[1] >> 26) == 1`        H  decode `& 1` -> `& 5` (bit 28 read as well)
  I  span end `x <= x2` -> `x < x2 + 1` (simpleline; It = the same edit in texturedline, which codex calls EQUIVALENT -- built to
     measure that claim, not one of the fifteen)
usage: pvr_variants_AI.py write"""
import io
import os
import sys

TAB, NL = chr(9), chr(10)
HERE = os.path.dirname(os.path.abspath(__file__))
DET = os.path.join(os.path.dirname(HERE), "det_20261104")
SEC = "C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c"
FIX = io.open(os.path.join(DET, "dev_pvr.c.fix"), encoding="latin-1", newline="").read()
assert FIX == io.open(SEC, encoding="latin-1", newline="").read(), "SEC dev_pvr.c is not the fix"

YL = TAB + "if (y < 0 || y >= d->ysize || (x1 < 0 && x2 < 0)" + NL
XL = TAB + "     || (x1 >= d->xsize && x2 >= d->xsize))" + NL
LOOPX = TAB + "for (int x = x1; x <= x2; ++x) {" + NL
SWAPL = TAB + "if (x1 > x2) {" + NL
ZT = TAB * 3 + "if (d->vram_z[ofs] <= z) {" + NL
ZBIT = TAB * 3 + "zwrite = ! ((list[1] >> 26) & 1);" + NL


def nth(s, old, new, n, count):
    """Replace the n-th (0-based) of exactly `count` occurrences of `old`; refuse if the count differs."""
    assert s.count(old) == count, (old[:60], s.count(old), count)
    i = -1
    for _ in range(n + 1):
        i = s.index(old, i + 1)
    return s[:i] + new + s[i + len(old):]


V = {}
for k, r in ((0, "s"), (1, "t")):
    V["A%s_start_m1" % r] = nth(FIX, LOOPX, LOOPX.replace("int x = x1;", "int x = x1 - 1;"), k, 2)
    V["B%s_swap_gt_p1" % r] = nth(FIX, SWAPL, SWAPL.replace("(x1 > x2)", "(x1 > x2 + 1)"), k, 2)
    V["C%s_swap_ge" % r] = nth(FIX, SWAPL, SWAPL.replace("(x1 > x2)", "(x1 >= x2)"), k, 2)
    V["D%s_left_x2x2" % r] = nth(FIX, YL, YL.replace("(x1 < 0 && x2 < 0)", "(x2 < 0 && x2 < 0)"), k, 2)
    V["E%s_right_x1x1" % r] = nth(FIX, XL, XL.replace("(x1 >= d->xsize && x2 >= d->xsize)",
                                                     "(x1 >= d->xsize && x1 >= d->xsize)"), k, 2)
    V["F%s_zoff_eq_refused" % r] = nth(FIX, ZT, ZT.replace("d->vram_z[ofs] <= z",
                                                           "d->vram_z[ofs] < z || (!d->zwrite_disabled && d->vram_z[ofs] == z)"), k, 2)
    V["I%s_end_lt_p1" % r] = nth(FIX, LOOPX, LOOPX.replace("x <= x2;", "x < x2 + 1;"), k, 2)
V["G_decode_eq1"] = nth(FIX, ZBIT, ZBIT.replace(">> 26) & 1)", ">> 26) == 1)"), 0, 1)
V["H_decode_and5"] = nth(FIX, ZBIT, ZBIT.replace(">> 26) & 1)", ">> 26) & 5)"), 0, 1)
assert len(V) == 16 and all(t != FIX for t in V.values()) and len(set(V.values())) == 16


def write():
    out = os.path.join(HERE, "meas_AI", "variants")
    os.makedirs(out, exist_ok=True)
    for n, t in sorted(V.items()):
        io.open(os.path.join(out, n + ".c"), "w", encoding="latin-1", newline="").write(t)
    print("%d variants written to %s" % (len(V), out))


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        write()
    else:
        sys.exit(__doc__)
