#!/usr/bin/env python3
"""pvr_variants_SW.py -- pvrrenderexit repair 3, step 2b (2026-11-05): the SWAP-BODY cells both Gemini pass-3 readings raised
(p3_20261105/gemini_p3_pvr{,_r2}.md, handed on by the coordinator): inside `if (x1 > x2) { ... }` delete ONE attribute exchange, so
x is swapped and that attribute is not.  ONE exact-text edit of the fix each (GXEMUL-SEC dev_pvr.c == ../det_20261104/dev_pvr.c.fix):
  simpleline   (dev_pvr.c `if (x1 > x2)` block, 663-669):  Zs `tmpf = z1; z1 = z2; z2 = tmpf;` deleted;  Rs the r1/r2 line deleted;
               Gs the g1/g2 line;  Bs the b1/b2 line;  Xs `double tmpf = x1; x1 = x2; x2 = tmpf;` -> `double tmpf = x1;` (x NOT swapped,
               the attributes still are -- the declaration is kept so the block compiles)
  texturedline (736-741):  Zt `double tmpf = z1; z1 = z2; z2 = tmpf;` -> `double tmpf = z1;` (declaration kept);  Ut the u1/u2 line
               deleted;  Vt the v1/v2 line deleted;  Xt `int tmp = x1; x1 = x2; x2 = tmp;` -> `int tmp = x1; (void) tmp;`
The texturedline lines also occur in pvr_render_triangle{,_textured}'s y sort (920, 1002-1004): each edit is anchored on the FIRST
occurrence of the exact two-tab line, which is texturedline's, and the occurrence count is checked.
usage: pvr_variants_SW.py write"""
import io
import os
import sys

TAB, NL = chr(9), chr(10)
HERE = os.path.dirname(os.path.abspath(__file__))
DET = os.path.join(os.path.dirname(HERE), "det_20261104")
SEC = "C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c"
FIX = io.open(os.path.join(DET, "dev_pvr.c.fix"), encoding="latin-1", newline="").read()
assert FIX == io.open(SEC, encoding="latin-1", newline="").read(), "SEC dev_pvr.c is not the fix"
T2 = TAB * 2


def nth(s, old, new, n, count):
    """Replace the n-th (0-based) of exactly `count` occurrences of `old`; refuse if the count differs."""
    assert s.count(old) == count, (old[:60], s.count(old), count)
    i = -1
    for _ in range(n + 1):
        i = s.index(old, i + 1)
    return s[:i] + new + s[i + len(old):]


V = {}
V["Zs_swap_noz"] = nth(FIX, T2 + "tmpf = z1; z1 = z2; z2 = tmpf;" + NL, "", 0, 1)
V["Rs_swap_nor"] = nth(FIX, T2 + "tmpf = r1; r1 = r2; r2 = tmpf;" + NL, "", 0, 1)
V["Gs_swap_nog"] = nth(FIX, T2 + "tmpf = g1; g1 = g2; g2 = tmpf;" + NL, "", 0, 1)
V["Bs_swap_nob"] = nth(FIX, T2 + "tmpf = b1; b1 = b2; b2 = tmpf;" + NL, "", 0, 1)
V["Xs_swap_nox"] = nth(FIX, T2 + "double tmpf = x1; x1 = x2; x2 = tmpf;" + NL, T2 + "double tmpf = x1;" + NL, 0, 1)
V["Zt_swap_noz"] = nth(FIX, T2 + "double tmpf = z1; z1 = z2; z2 = tmpf;" + NL, T2 + "double tmpf = z1;" + NL, 0, 3)
V["Ut_swap_nou"] = nth(FIX, T2 + "tmpf = u1; u1 = u2; u2 = tmpf;" + NL, "", 0, 2)
V["Vt_swap_nov"] = nth(FIX, T2 + "tmpf = v1; v1 = v2; v2 = tmpf;" + NL, "", 0, 2)
V["Xt_swap_nox"] = nth(FIX, T2 + "int tmp = x1; x1 = x2; x2 = tmp;" + NL, T2 + "int tmp = x1; (void) tmp;" + NL, 0, 3)
assert len(V) == 9 and all(t != FIX for t in V.values()) and len(set(V.values())) == 9
# every edit lands inside its rasterizer's swap block: simpleline 654-723, texturedline 725-904 (1-based lines of the fix)
_SPAN = {"s": (654, 723), "t": (725, 904)}
for _n, _t in V.items():
    _a, _b = FIX.split(NL), _t.split(NL)
    _first = next(i for i in range(min(len(_a), len(_b))) if _a[i] != _b[i]) + 1
    _lo, _hi = _SPAN[_n[1]]
    assert _lo <= _first <= _hi, (_n, _first)


def write():
    out = os.path.join(HERE, "meas_SW", "variants")
    os.makedirs(out, exist_ok=True)
    for n, t in sorted(V.items()):
        io.open(os.path.join(out, n + ".c"), "w", encoding="latin-1", newline="").write(t)
    print("%d variants written to %s" % (len(V), out))


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        write()
    else:
        sys.exit(__doc__)
