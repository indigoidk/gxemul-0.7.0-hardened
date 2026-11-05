#!/usr/bin/env python3
"""pvr_variants_B.py -- pvrrenderexit repair 4 (2026-11-05): codex pass 4's B1-B14 as test variants, as the ruling
(../adj_p4_20261105/ADJ_MYTHOS_local.md section 4) lists them -- ONE exact edit of dev_pvr.c.fix4 (== GXEMUL-SEC dev_pvr.c), its text
occurring exactly once inside the function it edits (s = simpleline, t = texturedline), or the script refuses:
  FLOOR (rule D2-F):   B1s `x1 > x2` -> `x1 > x2 + 0.5`;  B2s `int x = x1` -> `int x = x1 + 0.5`;  B13s `x1 >= d->xsize` -> `x1 >=
                       d->xsize - 0.5`;  B14s `x2 >= d->xsize` -> `x2 >= d->xsize - 0.5`;  and the seven HALF-exchange deletions, the final
                       `a2 = tmpf;` of one swap-body exchange: B4s z, B5s r, B6s g, B7s b (simpleline), B8t z, B9t u, B10t v (texturedline)
  DEBT (clause e):     B3s `x <= x2` -> `x <= x2 + 0.25`;  B11s / B12t `vram_z[ofs] <= z` -> `<= z + 0.25`
  EQUIVALENT (int ends): B1t, B2t, B13t, B14t -- the same fractional moves in texturedline
usage: pvr_variants_B.py write <outdir>"""
import io
import os
import sys

TAB, NL = chr(9), chr(10)
HERE = os.path.dirname(os.path.abspath(__file__))
SEC = next(p for p in ("C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c",
                       "/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c") if os.path.exists(p))
FIX = io.open(os.path.join(HERE, "dev_pvr.c.fix4"), encoding="latin-1", newline="").read()
assert FIX == io.open(SEC, encoding="latin-1", newline="").read(), "dev_pvr.c.fix4 is not GXEMUL-SEC's dev_pvr.c"
_S0, _T0 = FIX.index("static void simpleline("), FIX.index("static void texturedline(")
_T1 = FIX.index("// Slow software rendering, for debugging:" + NL + "static void pvr_render_triangle(")
REG = {"s": (_S0, _T0), "t": (_T0, _T1)}
XL = TAB + "     || (x1 >= d->xsize && x2 >= d->xsize))" + NL
LOOPX = TAB + "for (int x = x1; x <= x2; ++x) {" + NL
SWAPL = TAB + "if (x1 > x2) {" + NL
ZT = TAB * 3 + "if (d->vram_z[ofs] <= z) {" + NL
T2 = TAB * 2


def edit(where, old, new):
    a, b = REG[where]
    region = FIX[a:b]
    assert region.count(old) == 1, ("NOT EXACTLY ONCE", where, old[:70], region.count(old))
    out = FIX[:a] + region.replace(old, new) + FIX[b:]
    assert out != FIX
    return out


V = {}
for r in ("s", "t"):
    V["B1%s_swap_half" % r] = edit(r, SWAPL, SWAPL.replace("(x1 > x2)", "(x1 > x2 + 0.5)"))
    V["B2%s_start_half" % r] = edit(r, LOOPX, LOOPX.replace("int x = x1;", "int x = x1 + 0.5;"))
    V["B13%s_right_x1_half" % r] = edit(r, XL, XL.replace("(x1 >= d->xsize && x2", "(x1 >= d->xsize - 0.5 && x2"))
    V["B14%s_right_x2_half" % r] = edit(r, XL, XL.replace("x2 >= d->xsize))", "x2 >= d->xsize - 0.5))"))
V["B3s_end_q"] = edit("s", LOOPX, LOOPX.replace("x <= x2;", "x <= x2 + 0.25;"))
V["B4s_noz2"] = edit("s", T2 + "tmpf = z1; z1 = z2; z2 = tmpf;" + NL, T2 + "tmpf = z1; z1 = z2;" + NL)
V["B5s_nor2"] = edit("s", T2 + "tmpf = r1; r1 = r2; r2 = tmpf;" + NL, T2 + "tmpf = r1; r1 = r2;" + NL)
V["B6s_nog2"] = edit("s", T2 + "tmpf = g1; g1 = g2; g2 = tmpf;" + NL, T2 + "tmpf = g1; g1 = g2;" + NL)
V["B7s_nob2"] = edit("s", T2 + "tmpf = b1; b1 = b2; b2 = tmpf;" + NL, T2 + "tmpf = b1; b1 = b2;" + NL)
V["B8t_noz2"] = edit("t", T2 + "double tmpf = z1; z1 = z2; z2 = tmpf;" + NL, T2 + "double tmpf = z1; z1 = z2;" + NL)
V["B9t_nou2"] = edit("t", T2 + "tmpf = u1; u1 = u2; u2 = tmpf;" + NL, T2 + "tmpf = u1; u1 = u2;" + NL)
V["B10t_nov2"] = edit("t", T2 + "tmpf = v1; v1 = v2; v2 = tmpf;" + NL, T2 + "tmpf = v1; v1 = v2;" + NL)
V["B11s_ztest_q"] = edit("s", ZT, ZT.replace("<= z)", "<= z + 0.25)"))
V["B12t_ztest_q"] = edit("t", ZT, ZT.replace("<= z)", "<= z + 0.25)"))
assert len(V) == 18 and len(set(V.values())) == 18

if __name__ == "__main__":
    if sys.argv[1:2] != ["write"] or len(sys.argv) != 3:
        sys.exit(__doc__)
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for n, t in sorted(V.items()):
        io.open(os.path.join(out, n + ".c"), "w", encoding="latin-1", newline="").write(t)
    print("%d variants written to %s" % (len(V), out))
