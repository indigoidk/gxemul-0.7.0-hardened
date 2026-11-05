#!/usr/bin/env python3
"""pvr_variants_L.py -- pvrrenderexit repair 4 (2026-11-05): the LEFT clause's compares at the HALF pixel, which the pass-4 ruling
derived need no row (`x1 < 0.5` EQUIVALENT, `x1 < 1.5` caught by `edges2 l tip`).  Built here so the contract's sentence about them
rests on a measurement, not on the derivation alone.  ONE exact edit of simpleline in dev_pvr.c.fix4 each, or the script refuses:
  L15s_x1  `(x1 < 0 && x2 < 0)` -> `(x1 < 1.5 && x2 < 0)`   predicted red: edges2 l tip, zedges2 l tip (LREV row 259 ends at 1.0)
  L15s_x2  `(x1 < 0 && x2 < 0)` -> `(x1 < 0 && x2 < 1.5)`   predicted red: edges2 x2 tip, zleft tip (LEFT3 row 159 ends at 1.0)
  L05s_x1  `(x1 < 0 && ...`     -> `(x1 < 0.5 && ...`       predicted green: the span it newly refuses draws at most column 0
  L05s_x2  `... && x2 < 0)`     -> `... && x2 < 0.5)`       predicted green: the same
(texturedline's ends are ints: `< 1.5` there is `< 2`, table 3's W3t / W4t, and `< 0.5` is `< 1`, table 2's L1t -- both measured.)
usage: pvr_variants_L.py write <outdir>"""
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
YL = TAB + "if (y < 0 || y >= d->ysize || (x1 < 0 && x2 < 0)" + NL


def edit(old, new):
    region = FIX[_S0:_T0]
    assert region.count(old) == 1, ("NOT EXACTLY ONCE", old[:70], region.count(old))
    out = FIX[:_S0] + region.replace(old, new) + FIX[_T0:]
    assert out != FIX
    return out


V = {"L15s_x1": edit(YL, YL.replace("(x1 < 0 &&", "(x1 < 1.5 &&")),
     "L15s_x2": edit(YL, YL.replace("&& x2 < 0)", "&& x2 < 1.5)")),
     "L05s_x1": edit(YL, YL.replace("(x1 < 0 &&", "(x1 < 0.5 &&")),
     "L05s_x2": edit(YL, YL.replace("&& x2 < 0)", "&& x2 < 0.5)"))}
assert len(set(V.values())) == 4

if __name__ == "__main__":
    if sys.argv[1:2] != ["write"] or len(sys.argv) != 3:
        sys.exit(__doc__)
    os.makedirs(sys.argv[2], exist_ok=True)
    for n, t in sorted(V.items()):
        io.open(os.path.join(sys.argv[2], n + ".c"), "w", encoding="latin-1", newline="").write(t)
    print("%d variants written to %s" % (len(V), sys.argv[2]))
