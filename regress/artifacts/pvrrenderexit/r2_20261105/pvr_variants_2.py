#!/usr/bin/env python3
"""pvr_variants_2.py -- test-variant TABLE 2 for pvrrenderexit (repair 2: the class closure, 68 rows), 2026-11-05.
Table 1's 36 variants are reused VERBATIM from ../det_20261104/variants/*.c (same baseline: GXEMUL-SEC dev_pvr.c == ../det_20261104/
dev_pvr.c.fix, cmp-checked here).  Twenty-six new ones, ONE exact-text edit each (the class-closure cells the pass-2 adjudication
enumerated, per rasterizer: s = simpleline, t = texturedline):
  Y1 `y < 0` -> `y < 1`;  Y2 `y < 0` -> `y < -1`;  Y3 `y >= d->ysize` -> `y >= d->ysize - 1`;  Y4 `y >= d->ysize` -> `y > d->ysize`;
  O1 `(x1 < 0 && x2 < 0)` -> `||`;  L1 `(x1 < 0 && x2 < 0)` -> `(x1 < 1 && x2 < 1)`;  O2 `(x1 >= xsize && x2 >= xsize)` -> `||`;
  R1 `(x1 >= xsize && x2 >= xsize)` -> `xsize - 1` both;  E1 `x <= x2` -> `x < x2`;  E2 `x <= x2` -> `x <= x2 + 1`;
  X1 `int x = x1` -> `int x = x1 + 1`;  S1 the swap `if (x1 > x2)` -> `if (0)`;  K1 the decode `(list[1] >> 26) & 1` -> `& 3`;
  K2 the decode -> `(list[1] >> 25) & 3`.
  pvr_variants_2.py write | pretable"""
import glob
import io
import os
import sys

TAB, NL = chr(9), chr(10)
HERE = os.path.dirname(os.path.abspath(__file__))
DET = os.path.join(os.path.dirname(HERE), "det_20261104")
SEC = "C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c"
FIX = io.open(os.path.join(DET, "dev_pvr.c.fix"), encoding="latin-1", newline="").read()
assert FIX == io.open(SEC, encoding="latin-1", newline="").read(), "SEC dev_pvr.c is not table 1's baseline"
YL = TAB + "if (y < 0 || y >= d->ysize || (x1 < 0 && x2 < 0)" + NL
XL = TAB + "     || (x1 >= d->xsize && x2 >= d->xsize))" + NL
LOOPX = TAB + "for (int x = x1; x <= x2; ++x) {" + NL
SWAPL = TAB + "if (x1 > x2) {" + NL
ZBIT = TAB * 3 + "zwrite = ! ((list[1] >> 26) & 1);" + NL


def nth(s, old, new, n, count):
    assert s.count(old) == count, (old[:60], s.count(old), count)
    i = -1
    for _ in range(n + 1):
        i = s.index(old, i + 1)
    return s[:i] + new + s[i + len(old):]


NEW = {}
for k, r in ((0, "s"), (1, "t")):
    rr = "simple" if r == "s" else "tex"
    NEW["Y1%s_%s_lt1" % (r, rr)] = nth(FIX, YL, YL.replace("y < 0 ||", "y < 1 ||"), k, 2)
    NEW["Y2%s_%s_ltm1" % (r, rr)] = nth(FIX, YL, YL.replace("y < 0 ||", "y < -1 ||"), k, 2)
    NEW["Y3%s_%s_gem1" % (r, rr)] = nth(FIX, YL, YL.replace("y >= d->ysize", "y >= d->ysize - 1"), k, 2)
    NEW["Y4%s_%s_gt" % (r, rr)] = nth(FIX, YL, YL.replace("y >= d->ysize", "y > d->ysize"), k, 2)
    NEW["O1%s_%s_orleft" % (r, rr)] = nth(FIX, YL, YL.replace("(x1 < 0 && x2 < 0)", "(x1 < 0 || x2 < 0)"), k, 2)
    NEW["L1%s_%s_lt1left" % (r, rr)] = nth(FIX, YL, YL.replace("(x1 < 0 && x2 < 0)", "(x1 < 1 && x2 < 1)"), k, 2)
    NEW["O2%s_%s_orright" % (r, rr)] = nth(FIX, XL, XL.replace(" && ", " || "), k, 2)
    NEW["R1%s_%s_gem1right" % (r, rr)] = nth(FIX, XL, XL.replace("x1 >= d->xsize && x2 >= d->xsize",
                                                              "x1 >= d->xsize - 1 && x2 >= d->xsize - 1"), k, 2)
    NEW["E1%s_%s_ltx2" % (r, rr)] = nth(FIX, LOOPX, LOOPX.replace("x <= x2", "x < x2"), k, 2)
    NEW["E2%s_%s_lex2p1" % (r, rr)] = nth(FIX, LOOPX, LOOPX.replace("x <= x2", "x <= x2 + 1"), k, 2)
    NEW["X1%s_%s_start1" % (r, rr)] = nth(FIX, LOOPX, LOOPX.replace("int x = x1;", "int x = x1 + 1;"), k, 2)
    NEW["S1%s_%s_noswap" % (r, rr)] = nth(FIX, SWAPL, SWAPL.replace("(x1 > x2)", "(0)"), k, 2)
NEW["K1_mask26_and3"] = nth(FIX, ZBIT, ZBIT.replace("& 1)", "& 3)"), 0, 1)
NEW["K2_mask25_and3"] = nth(FIX, ZBIT, ZBIT.replace(">> 26) & 1)", ">> 25) & 3)"), 0, 1)
assert len(NEW) == 26 and all(t != FIX for t in NEW.values())
OLD = sorted(os.path.basename(p)[:-2] for p in glob.glob(os.path.join(DET, "variants", "*.c")))
assert len(OLD) == 36, len(OLD)

# exact predictions for the 26 (row names as the probe prints them in PVR_ZWRITE_RED); None = NOT PREDICTED (undefined behaviour)
P = {}
for r, pre in (("s", ""), ("t", "tex")):
    rr = "simple" if r == "s" else "tex"
    P["Y1%s_%s_lt1" % (r, rr)] = [pre + "yedges_t_in"]
    P["Y2%s_%s_ltm1" % (r, rr)] = None
    P["Y3%s_%s_gem1" % (r, rr)] = [pre + "yedges_b_in"]
    P["Y4%s_%s_gt" % (r, rr)] = None
    P["O1%s_%s_orleft" % (r, rr)] = [pre + "edges_l_in"]
    P["L1%s_%s_lt1left" % (r, rr)] = []
    P["O2%s_%s_orright" % (r, rr)] = [pre + "edges_r_in", pre + "edges_rspan"]
    P["R1%s_%s_gem1right" % (r, rr)] = [pre + "edges_rspan"]
    P["E1%s_%s_ltx2" % (r, rr)] = [pre + "yedges_s_end"]
    P["E2%s_%s_lex2p1" % (r, rr)] = [pre + "yedges_s_past"]
    P["X1%s_%s_start1" % (r, rr)] = [pre + "edges_rspan"]
    P["S1%s_%s_noswap" % (r, rr)] = [pre + "yedges_swap", pre + "yedges_s_end"]
P["K1_mask26_and3"] = ["mask_overlap"]
P["K2_mask25_and3"] = ["mask25_overlap"]
WHY = {
    "Y2": "y = -1 admitted: the colour store lands before the frame (a negative VRAM offset when FB_RENDER_ADDR1 < 1280) and the depth "
          "read is vram_z[x - 640], before the buffer: undefined behaviour, NOT PREDICTED, counted in neither tally",
    "Y4": "y = 480 admitted: the depth read vram_z[307200 + x] is past the frame-exact buffer (malloc of xsize*ysize doubles): "
          "`b out` RED, a fault, or nothing -- NOT PREDICTED, counted in neither tally",
    "L1": "EQUIVALENT: no probed span has both ends in [0, 1), and `x > 0` never draws column 0",
}


def write():
    out = os.path.join(HERE, "variants")
    os.makedirs(out, exist_ok=True)
    for n in OLD:
        io.open(os.path.join(out, n + ".c"), "w", encoding="latin-1", newline="").write(
            io.open(os.path.join(DET, "variants", n + ".c"), encoding="latin-1", newline="").read())
    for n, t in NEW.items():
        io.open(os.path.join(out, n + ".c"), "w", encoding="latin-1", newline="").write(t)
    print("%d variants written (%d reused from table 1, %d new)" % (len(OLD) + len(NEW), len(OLD), len(NEW)))


def pretable():
    t1 = {}
    for line in io.open(os.path.join(DET, "table1", "SCORES.txt"), encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.rsplit("RED=", 1)[1].strip()
            t1[p[0]] = [] if red == "none" else red.split(",")
    L = ["PRETABLE_2 -- pvrrenderexit, test-variant table 2 (repair 2: the class closure; 68 rows).  Written BEFORE table 2 runs (its",
         "mtime precedes every file in table2/).  Instrument: table2/probe68_frozen.py (the in-tree probe after apply_pvr_r2.py, run",
         "68/68 on build/ in base68/).  Baseline: the fix (GXEMUL-SEC dev_pvr.c == ../det_20261104/dev_pvr.c.fix).",
         "Table 1's 36: predicted AT LEAST their table-1 red sets (the 17 new rows informational).  The 26 new: predicted EXACTLY, except",
         "Y2 and Y4 (undefined behaviour, NOT PREDICTED, counted in neither tally).  HEAD (no fix): the Z-off sessions end the process, as",
         "in table 1.  Null media: CONTROL=FAIL.",
         "CHANNELS (each row's variant and the observable that differs): yedges/texyedges t in = Y1 (row 0 pixel 300 black); b in = Y3",
         "(row 479 black); b out = Y4 (row 480 drawn -- or a fault; not predicted); swap = S1 (the reversed span draws nothing); s end =",
         "E1 and S1 (pixel 435 = x2 exactly: SWAP's slopes are +-0.5, so 365.0..435.0 is exact); s past = E2 (pixel 436 drawn);",
         "edges/texedges rspan = R1, X1 and O2 (RSPAN's row 430 starts at exactly 639.0); edges l in = O1; edges r in = O2; mask overlap",
         "= K1 (bit 27 read as Z-write disable); mask25 overlap = K2 (bit 25 read as Z-write disable -- the rulings said texon already",
         "catches K2; MEASURED FALSE by reading: no probe header sets word 1 bit 25, so without mask25 K2 is green on every row).",
         "", "VARIANTS:"]
    for n in OLD:
        L.append("   %-24s at least: %s" % (n, ",".join(t1.get(n, [])) or "none (green in table 1)"))
    for n in NEW:
        tag = n[:2]
        if P[n] is None:
            L.append("   %-24s NOT PREDICTED (%s)" % (n, WHY[tag]))
        elif not P[n]:
            L.append("   %-24s exactly: none -- GREEN (%s)" % (n, WHY.get(tag, "")))
        else:
            L.append("   %-24s exactly: %s" % (n, ",".join(P[n])))
    return NL.join(L) + NL


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        write()
    elif sys.argv[1:] == ["pretable"]:
        sys.stdout.write(pretable())
    else:
        sys.exit(__doc__)
