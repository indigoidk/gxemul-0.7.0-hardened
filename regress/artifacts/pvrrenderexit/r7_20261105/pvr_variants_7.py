#!/usr/bin/env python3
"""pvr_variants_7.py -- the REGRESS stage's candidate floor cell (regress_20261105/REG_MYTHOS_local.md section 2(d)): a guard's constant 0
swapped for `fb_base` (REG(PVRREG_FB_RENDER_ADDR1), loaded at dev_pvr.c:662 / :735) or `palette_cfg` (:760), and one field swapped for
fb_base as a control.  ONE exact edit of dev_pvr.c.fix7 (== GXEMUL-SEC's dev_pvr.c) each, its anchor line exactly once in its function.
`y < fb_base` in the early return (:658 / :731) names fb_base before its declaration (:662 / :735), so that literal edit does not
compile (LIT/); the variant built instead reads the same value the way the guard can, `(int)REG(PVRREG_FB_RENDER_ADDR1)`, the cast
keeping the compare signed as fb_base's int is.   usage: pvr_variants_7.py write <outdir>"""
import io
import os
import sys

TAB, NL = chr(9), chr(10)
HERE = os.path.dirname(os.path.abspath(__file__))
SEC = next(p for p in ("C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c",
                       "/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c") if os.path.exists(p))
FIX = io.open(os.path.join(HERE, "dev_pvr.c.fix7"), encoding="latin-1", newline="").read()
assert FIX == io.open(SEC, encoding="latin-1", newline="").read()
_S0, _T0 = FIX.index("static void simpleline("), FIX.index("static void texturedline(")
_T1 = FIX.index("// Slow software rendering, for debugging:" + NL + "static void pvr_render_triangle(")
REG = {"s": (_S0, _T0), "t": (_T0, _T1)}
YL = TAB + "if (y < 0 || y >= d->ysize || (x1 < 0 && x2 < 0)" + NL
INX = TAB * 2 + "if (x > 0 && x < d->xsize) {" + NL


def edit(where, line, old, new):
    a, b = REG[where]
    region = FIX[a:b]
    assert region.count(line) == 1 and line.count(old) == 1, (where, line, old)
    return FIX[:a] + region.replace(line, line.replace(old, new)) + FIX[b:]


V = {"FB1s_x_gt_fb": edit("s", INX, "x > 0 &&", "x > fb_base &&"),
     "FB2s_y_lt_fbreg": edit("s", YL, "y < 0 ||", "y < (int)REG(PVRREG_FB_RENDER_ADDR1) ||"),
     "FB1t_x_gt_fb": edit("t", INX, "x > 0 &&", "x > fb_base &&"),
     "FB2t_y_lt_fbreg": edit("t", YL, "y < 0 ||", "y < (int)REG(PVRREG_FB_RENDER_ADDR1) ||"),
     "PC1t_x_gt_pal": edit("t", INX, "x > 0 &&", "x > palette_cfg &&"),
     "CTL1s_x_lt_fb": edit("s", INX, "x < d->xsize", "x < fb_base")}
LIT = {"LITs_y_lt_fb": edit("s", YL, "y < 0 ||", "y < fb_base ||"),
       "LITt_y_lt_fb": edit("t", YL, "y < 0 ||", "y < fb_base ||")}
assert len(set(V.values())) == 6

if __name__ == "__main__":
    out = sys.argv[2]
    os.makedirs(os.path.join(out, "LIT"), exist_ok=True)
    for n, t in V.items():
        io.open(os.path.join(out, n + ".c"), "w", encoding="latin-1", newline="").write(t)
    for n, t in LIT.items():
        io.open(os.path.join(out, "LIT", n + ".c"), "w", encoding="latin-1", newline="").write(t)
    print("%d variants and %d literal forms written to %s" % (len(V), len(LIT), out))
