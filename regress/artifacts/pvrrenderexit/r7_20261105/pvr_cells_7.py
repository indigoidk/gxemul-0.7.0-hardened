#!/usr/bin/env python3
"""pvr_cells_7.py -- repair 7's 16 register-swap variants: 12 FLOOR cells plus 4 measured checks outside the class (PL1t-PL4t: the
PALETTE register at :842 is an ADDRESS, not a read -- codex pass 8, p8_20261105/; corrected 2026-11-05, recp8_20261105/; the ruling
said "16 FLOOR cells") (ruling ../adj_reg_20261105/ADJ_MYTHOS_local.md section 2, and its erratum): a guard's constant 0 swapped
for a d->reg value the guarded body reads -- fb_base (REG(PVRREG_FB_RENDER_ADDR1), dev_pvr.c:662 / :735), palette_cfg (:760) or the
first PALETTE register (`&d->reg[PVRREG_PALETTE / sizeof(uint32_t)]`, :842) -- at the four guard sites per rasterizer: `y < 0`, `x1 < 0`,
`x2 < 0` (all three on :658 / :731) and `x > 0` (:684 / :769).  In the early return the locals are not yet declared, so those swaps are
spelled with the same value (the literal `y < fb_base` does not compile, ../r7_20261105/syntax_check_7.out).  ONE exact edit of
dev_pvr.c.fix7 each; the five meas7 measured are regenerated here and checked byte-identical to the files meas7 built.
usage: pvr_cells_7.py write <outdir>"""
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
FBR = "(int)REG(PVRREG_FB_RENDER_ADDR1)"
PALR = "(int)(d->reg[PVRREG_PALETTE_CFG / sizeof(uint32_t)] & PVR_PALETTE_CFG_MODE_MASK)"
PLT = "(int)d->reg[PVRREG_PALETTE / sizeof(uint32_t)]"


def edit(where, line, old, new):
    a, b = REG[where]
    region = FIX[a:b]
    assert region.count(line) == 1 and line.count(old) == 1, (where, line, old)
    return FIX[:a] + region.replace(line, line.replace(old, new)) + FIX[b:]


def four(r, early, inner, tag):
    return {"%s1%s_x" % (tag, r): edit(r, INX, "x > 0 &&", "x > %s &&" % inner),
            "%s2%s_y" % (tag, r): edit(r, YL, "y < 0 ||", "y < %s ||" % early),
            "%s3%s_x1" % (tag, r): edit(r, YL, "(x1 < 0 &&", "(x1 < %s &&" % early),
            "%s4%s_x2" % (tag, r): edit(r, YL, "&& x2 < 0)", "&& x2 < %s)" % early)}


V = {}
V.update(four("s", FBR, "fb_base", "FB"))
V.update(four("t", FBR, "fb_base", "FB"))
V.update(four("t", PALR, "palette_cfg", "PC"))
V.update(four("t", PLT, PLT, "PL"))
assert len(V) == 16 and len(set(V.values())) == 16
MEAS7 = {"FB1s_x": "FB1s_x_gt_fb", "FB2s_y": "FB2s_y_lt_fbreg", "FB1t_x": "FB1t_x_gt_fb", "FB2t_y": "FB2t_y_lt_fbreg",
         "PC1t_x": "PC1t_x_gt_pal"}
for n, m in MEAS7.items():
    assert V[n] == io.open(os.path.join(HERE, "variants", m + ".c"), encoding="latin-1", newline="").read(), (n, m)
NEW11 = sorted(set(V) - set(MEAS7))
assert len(NEW11) == 11

if __name__ == "__main__":
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for n, t in V.items():
        io.open(os.path.join(out, n + ".c"), "w", encoding="latin-1", newline="").write(t)
    print("16 cells written to %s (5 identical to meas7's, 11 new: %s)" % (out, " ".join(NEW11)))
