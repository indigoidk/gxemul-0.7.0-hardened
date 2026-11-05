#!/usr/bin/env python3
"""pvr_variants_W.py -- pvrrenderexit repair 3, step 2c (2026-11-05): the cells the CLASS CLOSURE found beyond codex and Gemini,
built so they are MEASURED on the 68-row probe before rows are added for them (CLOSURE3.md, family A4 / A3):
  W1 `x > 0` -> `x > d->zwrite_disabled`   (inner x bound; a single-token operand swap from a field the body reads: Z-off polygons
                                            lose column 1, Z-on ones are unchanged)
  W2 `y < 0` -> `y < d->zwrite_disabled`   (y bound; Z-off polygons lose row 0)
  W3 `x1 < 0` -> `x1 < d->bytes_per_pixel` (the left clause's x1 compare moved up by 2 -- by 1 it is EQUIVALENT -- so a reversed span
                                            from [1, 2) to below 0 returns early and loses column 1)
  W4 `x2 < 0` -> `x2 < d->bytes_per_pixel` (the x2 compare moved up by 2: a forward span from below 0 to [1, 2) loses column 1)
per rasterizer (s = simpleline, t = texturedline); ONE exact edit each, its text exactly once inside its function.
usage: pvr_variants_W.py write"""
import io
import os
import sys

TAB, NL = chr(9), chr(10)
HERE = os.path.dirname(os.path.abspath(__file__))
FIX = io.open(os.path.join(HERE, "dev_pvr.c.fix3"), encoding="latin-1", newline="").read()
assert FIX == io.open("C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c", encoding="latin-1", newline="").read()
_S0, _T0 = FIX.index("static void simpleline("), FIX.index("static void texturedline(")
_T1 = FIX.index("// Slow software rendering, for debugging:" + NL + "static void pvr_render_triangle(")
REG = {"s": (_S0, _T0), "t": (_T0, _T1)}
YL = TAB + "if (y < 0 || y >= d->ysize || (x1 < 0 && x2 < 0)" + NL
INX = TAB * 2 + "if (x > 0 && x < d->xsize) {" + NL


def edit(where, old, new):
    a, b = REG[where]
    region = FIX[a:b]
    assert region.count(old) == 1, ("NOT EXACTLY ONCE", where, old[:70], region.count(old))
    return FIX[:a] + region.replace(old, new) + FIX[b:]


V = {}
for r in ("s", "t"):
    V["W1%s_inner_zw" % r] = edit(r, INX, INX.replace("x > 0 &&", "x > d->zwrite_disabled &&"))
    V["W2%s_y_zw" % r] = edit(r, YL, YL.replace("y < 0 ||", "y < d->zwrite_disabled ||"))
    V["W3%s_left_x1_bpp" % r] = edit(r, YL, YL.replace("(x1 < 0 &&", "(x1 < d->bytes_per_pixel &&"))
    V["W4%s_left_x2_bpp" % r] = edit(r, YL, YL.replace("&& x2 < 0)", "&& x2 < d->bytes_per_pixel)"))
assert len(V) == 8 and len(set(V.values())) == 8 and all(t != FIX for t in V.values())

if __name__ == "__main__":
    if sys.argv[1:] != ["write"]:
        sys.exit(__doc__)
    out = os.path.join(HERE, "meas_W", "variants")
    os.makedirs(out, exist_ok=True)
    for n, t in sorted(V.items()):
        io.open(os.path.join(out, n + ".c"), "w", encoding="latin-1", newline="").write(t)
    print("%d variants written to %s" % (len(V), out))
