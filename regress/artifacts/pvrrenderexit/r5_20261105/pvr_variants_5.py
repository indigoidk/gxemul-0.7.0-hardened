#!/usr/bin/env python3
"""pvr_variants_5.py -- pvrrenderexit repair 5 (2026-11-05): the variants the pass-5 ruling (../adj_p5_20261105/ADJ_MYTHOS_local.md)
owes, each ONE exact edit of dev_pvr.c.fix5 (== GXEMUL-SEC src/devices/dev_pvr.c), its anchor line occurring exactly once inside the
function it edits (s = simpleline, t = texturedline), or the script refuses.
  * the 17 statement-deletion cells of the swap bodies not built before (section 1):
      6 temporaries   DTs_z DTs_r DTs_g DTs_b (simpleline `tmpf = z1;` ... `tmpf = b1;`), DTt_u DTt_v (texturedline `tmpf = u1;`,
                      `tmpf = v1;`);
      7 a1 = a2       DAs_z DAs_r DAs_g DAs_b (simpleline `z1 = z2;` ... `b1 = b2;`), DAt_z DAt_u DAt_v (texturedline);
      4 x halves      DXs_x1 DXs_x2 (simpleline `x1 = x2;`, `x2 = tmpf;`), DXt_x1 DXt_x2 (texturedline `x1 = x2;`, `x2 = tmp;`);
    (the 7 `a2 = tmp` halves are table 4's B4s-B10t, copied unchanged into table 5 with the rest of table 4)
  * N1s: simpleline `int x = x1` -> `int x = x1 + 0.25` (section 3);
  * the 26 compound-assignment substitutions codex pass 5 derived as survivors (section 2):
      depth 11  CZs_tadd CZs_tmul CZs_tdiv (`tmpf = z1` -> `tmpf += / *= / /= z1`), CZs_z1add CZs_z1mul (`z1 = z2` -> `+=`, `*=`),
                CZs_z2add CZs_z2mul (`z2 = tmpf` -> `+=`, `*=`), and texturedline's CZt_z1add CZt_z1mul CZt_z2add CZt_z2mul;
      RGB 9     CRs_tadd CRs_tmul CRs_r2add, CGs_tmul CGs_g1add CGs_g2mul, CBs_tadd CBs_b1mul CBs_b2add;
      UV 6      CUt_u1mul CUt_u2add CUt_u2sub, CVt_tmul CVt_v1add CVt_v2mul.
  * DECL: the three declarations, deleted alone (`double tmpf = x1;` simpleline, `int tmp = x1;` and `double tmpf = z1;`
    texturedline) -- NOT table variants: written only for the syntax check, which must REFUSE them (the temporary is used later).
B2t (texturedline `int x = x1 + 0.5`) is table 4's file, copied by the table, not regenerated here.
usage: pvr_variants_5.py write <outdir> | decl <outdir>"""
import io
import os
import sys

TAB, NL = chr(9), chr(10)
HERE = os.path.dirname(os.path.abspath(__file__))
SEC = next(p for p in ("C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c",
                       "/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c") if os.path.exists(p))
FIX = io.open(os.path.join(HERE, "dev_pvr.c.fix5"), encoding="latin-1", newline="").read()
assert FIX == io.open(SEC, encoding="latin-1", newline="").read(), "dev_pvr.c.fix5 is not GXEMUL-SEC's dev_pvr.c"
_S0, _T0 = FIX.index("static void simpleline("), FIX.index("static void texturedline(")
_T1 = FIX.index("// Slow software rendering, for debugging:" + NL + "static void pvr_render_triangle(")
REG = {"s": (_S0, _T0), "t": (_T0, _T1)}
T2 = TAB * 2
SX, SZ = T2 + "double tmpf = x1; x1 = x2; x2 = tmpf;" + NL, T2 + "tmpf = z1; z1 = z2; z2 = tmpf;" + NL
SR, SG, SB = (T2 + "tmpf = %s1; %s1 = %s2; %s2 = tmpf;" % (c, c, c, c) + NL for c in "rgb")
TX, TZ = T2 + "int tmp = x1; x1 = x2; x2 = tmp;" + NL, T2 + "double tmpf = z1; z1 = z2; z2 = tmpf;" + NL
TU, TV = (T2 + "tmpf = %s1; %s1 = %s2; %s2 = tmpf;" % (c, c, c, c) + NL for c in "uv")
LOOPX = TAB + "for (int x = x1; x <= x2; ++x) {" + NL


def edit(where, line, new):
    """Replace the whole anchor `line` (exactly once in the function `where`) by `new`."""
    a, b = REG[where]
    region = FIX[a:b]
    assert region.count(line) == 1, ("NOT EXACTLY ONCE", where, line, region.count(line))
    assert new != line
    return FIX[:a] + region.replace(line, new) + FIX[b:]


def sub(line, old, new):
    """`line` with its one occurrence of the statement `old` replaced by `new` (statements are `; `-separated)."""
    assert line.count(old) == 1, (line, old)
    return line.replace(old, new)


V = {}
# ---- deletion cells
V["DTs_z"] = edit("s", SZ, sub(SZ, "tmpf = z1; ", ""))
V["DTs_r"] = edit("s", SR, sub(SR, "tmpf = r1; ", ""))
V["DTs_g"] = edit("s", SG, sub(SG, "tmpf = g1; ", ""))
V["DTs_b"] = edit("s", SB, sub(SB, "tmpf = b1; ", ""))
V["DTt_u"] = edit("t", TU, sub(TU, "tmpf = u1; ", ""))
V["DTt_v"] = edit("t", TV, sub(TV, "tmpf = v1; ", ""))
V["DAs_z"] = edit("s", SZ, sub(SZ, "z1 = z2; ", ""))
V["DAs_r"] = edit("s", SR, sub(SR, "r1 = r2; ", ""))
V["DAs_g"] = edit("s", SG, sub(SG, "g1 = g2; ", ""))
V["DAs_b"] = edit("s", SB, sub(SB, "b1 = b2; ", ""))
V["DAt_z"] = edit("t", TZ, sub(TZ, "z1 = z2; ", ""))
V["DAt_u"] = edit("t", TU, sub(TU, "u1 = u2; ", ""))
V["DAt_v"] = edit("t", TV, sub(TV, "v1 = v2; ", ""))
V["DXs_x1"] = edit("s", SX, sub(SX, "x1 = x2; ", ""))
V["DXs_x2"] = edit("s", SX, sub(SX, " x2 = tmpf;", ""))
V["DXt_x1"] = edit("t", TX, sub(TX, "x1 = x2; ", ""))
V["DXt_x2"] = edit("t", TX, sub(TX, " x2 = tmp;", ""))
# ---- N1s
V["N1s_start_q"] = edit("s", LOOPX, LOOPX.replace("int x = x1;", "int x = x1 + 0.25;"))
# ---- the 26 compound survivors (codex pass 5, section 1)
for n, (w, line, old, new) in {
        "CZs_tadd": ("s", SZ, "tmpf = z1;", "tmpf += z1;"), "CZs_tmul": ("s", SZ, "tmpf = z1;", "tmpf *= z1;"),
        "CZs_tdiv": ("s", SZ, "tmpf = z1;", "tmpf /= z1;"),
        "CZs_z1add": ("s", SZ, "z1 = z2;", "z1 += z2;"), "CZs_z1mul": ("s", SZ, "z1 = z2;", "z1 *= z2;"),
        "CZs_z2add": ("s", SZ, "z2 = tmpf;", "z2 += tmpf;"), "CZs_z2mul": ("s", SZ, "z2 = tmpf;", "z2 *= tmpf;"),
        "CZt_z1add": ("t", TZ, "z1 = z2;", "z1 += z2;"), "CZt_z1mul": ("t", TZ, "z1 = z2;", "z1 *= z2;"),
        "CZt_z2add": ("t", TZ, "z2 = tmpf;", "z2 += tmpf;"), "CZt_z2mul": ("t", TZ, "z2 = tmpf;", "z2 *= tmpf;"),
        "CRs_tadd": ("s", SR, "tmpf = r1;", "tmpf += r1;"), "CRs_tmul": ("s", SR, "tmpf = r1;", "tmpf *= r1;"),
        "CRs_r2add": ("s", SR, "r2 = tmpf;", "r2 += tmpf;"),
        "CGs_tmul": ("s", SG, "tmpf = g1;", "tmpf *= g1;"), "CGs_g1add": ("s", SG, "g1 = g2;", "g1 += g2;"),
        "CGs_g2mul": ("s", SG, "g2 = tmpf;", "g2 *= tmpf;"),
        "CBs_tadd": ("s", SB, "tmpf = b1;", "tmpf += b1;"), "CBs_b1mul": ("s", SB, "b1 = b2;", "b1 *= b2;"),
        "CBs_b2add": ("s", SB, "b2 = tmpf;", "b2 += tmpf;"),
        "CUt_u1mul": ("t", TU, "u1 = u2;", "u1 *= u2;"), "CUt_u2add": ("t", TU, "u2 = tmpf;", "u2 += tmpf;"),
        "CUt_u2sub": ("t", TU, "u2 = tmpf;", "u2 -= tmpf;"),
        "CVt_tmul": ("t", TV, "tmpf = v1;", "tmpf *= v1;"), "CVt_v1add": ("t", TV, "v1 = v2;", "v1 += v2;"),
        "CVt_v2mul": ("t", TV, "v2 = tmpf;", "v2 *= tmpf;")}.items():
    V[n] = edit(w, line, sub(line, old, new))
assert len(V) == 44 and len(set(V.values())) == 44, len(V)
DECL = {"DECLs_x": edit("s", SX, sub(SX, "double tmpf = x1; ", "")),
        "DECLt_x": edit("t", TX, sub(TX, "int tmp = x1; ", "")),
        "DECLt_z": edit("t", TZ, sub(TZ, "double tmpf = z1; ", ""))}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("write", "decl"):
        sys.exit(__doc__)
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for n, t in sorted((V if sys.argv[1] == "write" else DECL).items()):
        io.open(os.path.join(out, n + ".c"), "w", encoding="latin-1", newline="").write(t)
    print("%d files written to %s" % (len(V) if sys.argv[1] == "write" else len(DECL), out))
