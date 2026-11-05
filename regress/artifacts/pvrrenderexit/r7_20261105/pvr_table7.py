#!/usr/bin/env python3
"""pvr_table7.py -- test-variant TABLE 7 for pvrrenderexit (repair 7: the guards' constant 0 against the d->reg values the body
reads; the 164-row probe), 2026-11-05.  Its PRETABLE is PRETABLE_7.out -- the ruling (../adj_reg_20261105/ADJ_MYTHOS_local.md) calls it
PRETABLE_8; this round numbers its tables by repair.
Variants, each COPIED and md5-checked against the file already built from it (or regenerated):
  * table 5's 190 (../r5_20261105/variants/*.c, against table5/MD5.txt);
  * repair 7's 16 cells (cells/*.c, pvr_cells_7.py): five measured in meas7 (FB1s FB2s FB1t FB2t PC1t, checked identical to
    meas7's files by pvr_cells_7.py) and eleven new.
PREDICTIONS, exact red sets over the 164 rows:
  * the 148 rows that carry over -- MEASURED: table 5's SCORES.txt for its 190 and legs, meas7's p148 runs for the five; the eleven
    new cells are predicted green there (each register is 0 in those sessions, equal to the constant);
  * the 16 repair-7 rows -- DERIVED: for the 16 cells per cell (CELL7 below); for table 5's 190 by GEOMETRY: each edge row draws the
    geometry of an existing row at another frame base or other rows (NEWMAP), so it reds exactly when that row red in table 5, and
    the fbhi pair's forward interior pixels red only where a Z-off session dies or draws nothing (FBHI_RED).
usage: pvr_table7.py write | pretable <base.out> <frozen probe> <head.log> | check <SCORES.txt> <base.out>
       | check7b <meas7b SCORES.txt> <base.out>"""
import glob
import hashlib
import io
import os
import re
import sys

NL = chr(10)
HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.dirname(HERE)
R5 = os.path.join(UP, "r5_20261105")
SEC = next(p for p in ("C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c",
                       "/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c") if os.path.exists(p))


def rd(p):
    return io.open(p, encoding="latin-1", newline="").read()


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def md5s(path):
    out = {}
    for line in io.open(path, encoding="utf-8"):
        h, _, f = line.strip().partition("  ")
        out[os.path.basename(f.lstrip("*"))] = h
    return out


FIX = rd(os.path.join(HERE, "dev_pvr.c.fix7"))
assert FIX == rd(SEC)
T5V = {os.path.basename(p)[:-2]: p for p in glob.glob(os.path.join(R5, "variants", "*.c"))}
C7V = {os.path.basename(p)[:-2]: p for p in glob.glob(os.path.join(HERE, "cells", "*.c"))}
assert len(T5V) == 190 and len(C7V) == 16 and not set(T5V) & set(C7V)
_M5 = md5s(os.path.join(R5, "table5", "MD5.txt"))
for _n, _p in T5V.items():
    assert _M5.get(_n + ".c") == md5(_p), ("table-5 variant differs from the one table 5 built", _n)
sys.path.insert(0, HERE)
import pvr_cells_7                                             # noqa: E402  (asserts the five are meas7's files byte for byte)
for _n, _p in C7V.items():
    assert pvr_cells_7.V[_n] == rd(_p), _n
MEAS7 = pvr_cells_7.MEAS7

UB = {"Y2s_simple_ltm1", "Y2t_tex_ltm1", "Y4s_simple_gt", "Y4t_tex_gt"}
WHY_UB = {"Y2": "y = -1 admitted: undefined behaviour, NOT PREDICTED (tables 2-5 measured the whole y-edges sessions red)",
          "Y4": "y = 480 admitted: undefined behaviour, NOT PREDICTED (tables 2-5 measured `b out` and its twin red)"}

FS, FT, ZFS, ZFT = "fbhi_s_px", "fbhi_t_px", "zfbhi_s_px", "zfbhi_t_px"
NEWMAP = {   # a repair-7 edge row -> the existing row whose geometry, rasterizer and Z-state it repeats
    "fbedge_l_tip": "edges2_l_tip", "fbedge_x2_tip": "edges2_x2_tip",
    "zfbedge_l_tip": "zedges2_l_tip", "zfbedge_x2_tip": "zleft_tip",
    "fbtedge_l_tip": "texedges2_l_tip", "fbtedge_x2_tip": "texedges2_x2_tip",
    "zfbtedge_l_tip": "ztedges2_l_tip", "zfbtedge_x2_tip": "texzleft_tip",
    "palcfg_x2_tip": "texedges2_x2_tip", "palcfg_l_tip": "texedges2_l_tip",
    "zpalcfg_x2_tip": "texzleft_tip", "zpalcfg_l_tip": "ztedges2_l_tip"}
NEWROWS = [FS, FT, ZFS, ZFT] + list(NEWMAP)
FBHI_RED = {"B1_exit": [ZFS, ZFT], "M11_decline": [ZFS, ZFT], "M12_hoist_simple": [ZFS], "M28_hoist_tex": [ZFT]}
EDGE_S = ["fbedge_l_tip", "fbedge_x2_tip", "zfbedge_l_tip", "zfbedge_x2_tip"]
EDGE_T = ["fbtedge_l_tip", "fbtedge_x2_tip", "zfbtedge_l_tip", "zfbtedge_x2_tip"]
PAL4 = ["palcfg_x2_tip", "palcfg_l_tip", "zpalcfg_x2_tip", "zpalcfg_l_tip"]
CELL7 = {   # the 16 cells on the repair-7 rows (every register is 0 in the 148 rows' sessions, so none of them reds there)
    "FB1s_x": [FS, ZFS] + EDGE_S, "FB2s_y": [FS, ZFS] + EDGE_S,
    "FB3s_x1": ["fbedge_l_tip", "zfbedge_l_tip"], "FB4s_x2": ["fbedge_x2_tip", "zfbedge_x2_tip"],
    "FB1t_x": [FT, ZFT] + EDGE_T, "FB2t_y": [FT, ZFT] + EDGE_T,
    "FB3t_x1": ["fbtedge_l_tip", "zfbtedge_l_tip"], "FB4t_x2": ["fbtedge_x2_tip", "zfbtedge_x2_tip"],
    "PC1t_x": PAL4, "PC2t_y": ["palcfg_x2_tip", "zpalcfg_x2_tip"],
    "PC3t_x1": ["palcfg_l_tip", "zpalcfg_l_tip"], "PC4t_x2": ["palcfg_x2_tip", "zpalcfg_x2_tip"],
    "PL1t_x": PAL4, "PL2t_y": PAL4, "PL3t_x1": ["palcfg_l_tip", "zpalcfg_l_tip"], "PL4t_x2": ["palcfg_x2_tip", "zpalcfg_x2_tip"]}
assert set(CELL7) == set(C7V)
PARTIAL = {"Nt_inner_or": ["palcfg_x2_tip", "palcfg_l_tip", "zpalcfg_x2_tip", "zpalcfg_l_tip"]}   # rows NOT PREDICTED for that variant
WHY_PARTIAL = ("NOT PREDICTED on %s: `x > 0 || x < d->xsize` draws LEFT3R's row 0 (-3..3) at ofs -3..-1, before vram_z, and at "
               "fbofs -6..-1 (C's %% keeps the sign) before vram -- undefined behaviour")
ALLV = sorted(T5V) + sorted(C7V)
SESSION_ROWS = ("id_session", "zon_session", "zoff_session", "ovoff_session", "behind_session", "texoff_session", "texbeh_session",
                "two_session", "sticky_session")
T5_GREEN = {}   # table 5's green reasons, carried forward unchanged (PRETABLE_5.out)
for line in io.open(os.path.join(R5, "PRETABLE_5.out"), encoding="latin-1"):
    m = re.match(r"^   (\S+)\s+exactly: none -- GREEN \((.*)\)$", line.rstrip("\n"))
    if m:
        T5_GREEN[m.group(1)] = m.group(2)


def scores(path, field=0):
    out = {}
    for line in io.open(path, encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            key = p[0] if field == 0 else (p[0], p[1])
            red = line.split("RED=", 1)[1].split()[0]
            out[key] = [] if red == "none" else red.split(",")
        elif len(p) > 1 and "BUILD-FAILED" in line:
            out[p[0]] = "BUILD-FAILED"
    return out


def rowlist(base_out):
    names = []
    for line in io.open(base_out, encoding="latin-1"):
        m = re.match(r"^(\S.{0,15}?)\s{2,}\S.*\s(ok|FAIL)$", line.rstrip("\n"))
        if m and not line.startswith("row "):
            names.append(m.group(1).strip().replace(" ", "_"))
    assert len(names) == 164 and len(set(names)) == 164 and all(r in names for r in NEWROWS)
    return names


def predictions(rows):
    t5 = scores(os.path.join(R5, "table5", "SCORES.txt"))
    m7 = scores(os.path.join(HERE, "meas7", "SCORES.txt"), field=1)
    old = [r for r in rows if r not in NEWROWS]
    assert len(old) == 148
    P = {}
    for n in ALLV:
        if n in UB:
            P[n] = None
            continue
        if n in T5V:
            carried = t5[n]
            new = {nr for nr, orow in NEWMAP.items() if orow in carried} | set(FBHI_RED.get(n, []))
        else:
            carried = m7[(MEAS7[n], "p148")] if n in MEAS7 else []
            new = set(CELL7[n])
        assert isinstance(carried, list) and all(r in old for r in carried), (n, carried)
        P[n] = sorted(set(carried) | new, key=rows.index)
    legs = {"base": [],
            "HEAD": sorted(set(t5["HEAD"]) | {ZFS, ZFT, "zfbedge_l_tip", "zfbedge_x2_tip", "zfbtedge_l_tip", "zfbtedge_x2_tip",
                                              "zpalcfg_x2_tip", "zpalcfg_l_tip"}, key=rows.index),
            "null_true": [r for r in rows if r not in SESSION_ROWS],
            "null_absent": list(rows),
            "null_false": [r for r in rows if r != "neg_apparatus"],
            "restored": []}
    return P, legs


def write():
    out = os.path.join(HERE, "variants7")
    os.makedirs(out, exist_ok=True)
    for n, p in list(T5V.items()) + list(C7V.items()):
        io.open(os.path.join(out, n + ".c"), "w", encoding="latin-1", newline="").write(rd(p))
    print("%d variants written to %s (%d from table 5, %d cells)" % (len(T5V) + len(C7V), out, len(T5V), len(C7V)))


def pretable(base_out, frozen, head_log, channels):
    rows = rowlist(base_out)
    P, legs = predictions(rows)
    head = set(io.open(head_log, encoding="utf-8").read().split("HEAD PVR_ZWRITE_RED=")[1].split()[0].split(","))
    assert head == set(legs["HEAD"]), "the HEAD prediction is not the measured pre-fix leg"
    npred = sum(1 for v in P.values() if v is not None)
    nred = sum(1 for v in P.values() if v)
    green = [n for n, v in P.items() if v == []]
    for n in green:
        assert n in T5_GREEN, n
    L = ["PRETABLE_7 -- pvrrenderexit, test-variant table 7 (repair 7; the ruling's PRETABLE_8, numbered here by repair; 164 rows).",
         "Written BEFORE meas7b and BEFORE table 7: its mtime must precede every result in meas7b/ and table7/ (the frozen probe is",
         "copied first and is older).  INSTRUMENT: table7/probe164_frozen.py, cmp-identical to cand164_probe.py (the shipped 148 rows plus",
         "the 16 repair-7 rows; base164/: 164/164 on build/, both clearance parts recorded; head164/: 78/164 pre-fix).",
         "INSTRUMENT_MD5 %s table7/probe164_frozen.py" % md5(frozen),
         "Baseline: dev_pvr.c.fix7 (== GXEMUL-SEC src/devices/dev_pvr.c).  Variants: pvr_table7.py -- table 5's 190 and the 16 cells.",
         "EVERY prediction is EXACT -- the full red set, none = all 164 green -- except Y2s/Y2t/Y4s/Y4t (undefined behaviour, NOT",
         "PREDICTED).  148 carried rows: MEASURED (table 5; meas7 for FB1s FB2s FB1t FB2t PC1t; the eleven new cells green there, each",
         "register being 0 = the constant).  16 new rows: DERIVED -- per cell (CELL7), and for table 5's 190 by geometry (NEWMAP:",
         "each edge row repeats an existing row's geometry, rasterizer and Z-state at another frame base or rows) plus FBHI_RED.",
         "ONE per-row exception: Nt_inner_or is predicted on 160 rows and NOT PREDICTED on the four palcfg rows (undefined behaviour,",
         "CHANNELS7 below).",
         "%d variants: %d predicted, %d predicted red, %d predicted green (table 5's 30, reasons carried), 4 NOT PREDICTED."
         % (len(P), npred, nred, npred - nred),
         "Legs: base 164/164; HEAD %d/164 SYMPTOM=PRESENT (MEASURED already, head164/); null media CONTROL=FAIL: /bin/true 9/164, an"
         % (164 - len(legs["HEAD"])),
         "absent binary 0/164, /bin/false 1/164.",
         "",
         "GUARD FIELD vs BODY FIELD (the pre-table check, as the ruling's section 2 states it):",
         "  simpleline -- guard operands of P1-P3 and P7: y, x1, x2, x, d->ysize, d->xsize and the constant 0 (`y < 0`, `x1 < 0`, `x2 < 0`",
         "    at dev_pvr.c:658; `x > 0` at :684).  Body-read lvalues: d->vram_z[ofs], z, d->zwrite_disabled, r g b, d->bytes_per_pixel,",
         "    d->vram[fbofs], and d->reg through ONE spelling: fb_base = REG(PVRREG_FB_RENDER_ADDR1) (:662, read :715).",
         "  texturedline -- the same guard operands at :731 and :769.  Body-read lvalues: as simpleline, and d->reg through THREE",
         "    spellings: fb_base (:735, read :775); palette_cfg = d->reg[PVRREG_PALETTE_CFG / 4] & PVR_PALETTE_CFG_MODE_MASK (:760, read",
         "    :845); d->reg[PVRREG_PALETTE / 4], read directly as the palette base (:842).  The texture parameters are the caller's reads",
         "    (:1047), outside the boundary; ofs, fbofs, bytesperpixel and the slopes are derived inputs, graded by the body's tests on them.",
         "  Partitions the body induces: fb_base -- none, used only in arithmetic (:715, :775); SAMPLED at 0 (every carried session),",
         "    0x200000 (fbhi) and 0x300000 (fbedge, fbtedge).  palette_cfg -- {0, 1, 2, 3} by the switch at :845-868, reached only for pixel",
         "    format 6, which no session renders: SAMPLED at 0 and 3 at the guard; the switch partition is clause-(e) DEBT, disclosed.",
         "    PALETTE[0] -- none, a palette entry (data): SAMPLED at 0 and 0x10000.",
         "  Disagreeing state owed: each register non-zero, which no carried session sets (DEVINIT zeroes d->reg; the probe never wrote",
         "    them) -- the eight repair-7 sessions.  (The ruling places `x2 < 0` at :659 / :732; it is on :658 / :731, with `x1 < 0`.)",
         "",
         "STEP 2 (meas7b, before the rows ship): the eleven unmeasured cells -- FB3s FB4s FB3t FB4t PC2t PC3t PC4t PL1t PL2t PL3t PL4t --",
         "  on probe148_frozen.py: 148/148 each; on table7/probe164_frozen.py: exactly the sets their VARIANTS lines below give",
         "  (pvr_table7.py check7b).",
         ""] + channels.rstrip(NL).split(NL) + ["", "LEGS:"]
    for k, v in legs.items():
        L.append("   %-24s exactly: %s" % (k, ",".join(v) if v else "none"))
    L += ["", "VARIANTS:"]
    for n in ALLV:
        v = P[n]
        if v is None:
            L.append("   %-24s NOT PREDICTED (%s)" % (n, WHY_UB[n[:2]]))
        elif n in PARTIAL:
            rest = [r for r in v if r not in PARTIAL[n]]
            L.append("   %-24s exactly: %s on the other %d rows; %s" % (n, ",".join(rest) or "none", len(rows) - len(PARTIAL[n]),
                                                                    WHY_PARTIAL % ",".join(PARTIAL[n])))
        elif not v:
            L.append("   %-24s exactly: none -- GREEN (%s)" % (n, T5_GREEN[n]))
        else:
            L.append("   %-24s exactly: %s" % (n, ",".join(v)))
    return NL.join(L) + NL


def check(scores_path, base_out):
    rows = rowlist(base_out)
    P, legs = predictions(rows)
    got = scores(scores_path)
    hit = miss = npr = 0
    for n, want in list(legs.items()) + [(k, P[k]) for k in ALLV]:
        g = got.get(n)
        if g is None:
            print("PRED=ABSENT  %s (no score line)" % n)
            miss += 1
        elif g == "BUILD-FAILED":
            print("PRED=MISS    %s BUILD-FAILED" % n)
            miss += 1
        elif want is None:
            print("PRED=NOTPRED %s red=%s" % (n, ",".join(sorted(g, key=rows.index)) or "none"))
            npr += 1
        elif n in PARTIAL:
            ex = set(PARTIAL[n])
            if set(g) - ex == set(want) - ex:
                hit += 1
                print("PRED=HIT-PARTIAL %s (on %d rows); its NOT PREDICTED rows: %s" % (
                    n, len(rows) - len(ex), ", ".join("%s %s" % (r, "red" if r in g else "green") for r in PARTIAL[n])))
            else:
                print("PRED=MISS    %s want=%s got=%s (outside %s)" % (n, ",".join(r for r in want if r not in ex) or "none",
                      ",".join(r for r in sorted(g, key=rows.index) if r not in ex) or "none", ",".join(PARTIAL[n])))
                miss += 1
        elif set(g) == set(want):
            hit += 1
        else:
            print("PRED=MISS    %s want=%s got=%s" % (n, ",".join(want) or "none", ",".join(sorted(g, key=rows.index)) or "none"))
            miss += 1
    print("TABLE7_CHECK hits=%d misses=%d not_predicted=%d" % (hit, miss, npr))


def check7b(scores_path, base_out):
    """Step 2: the eleven unmeasured cells -- 148/148 on probe148_frozen.py, CELL7's set exactly on the frozen 164-row probe."""
    rows = rowlist(base_out)
    got = scores(scores_path, field=1)
    hit = miss = 0
    for n in sorted(set(C7V) - set(MEAS7)):
        for tag, want in (("p148", []), ("p164", sorted(CELL7[n], key=rows.index))):
            g = got.get((n, tag))
            if g is None or g == "BUILD-FAILED":
                print("PRED=MISS    %s %s %s" % (n, tag, "no score line" if g is None else g))
                miss += 1
            elif set(g) == set(want):
                hit += 1
            else:
                print("PRED=MISS    %s %s want=%s got=%s" % (n, tag, ",".join(want) or "none", ",".join(sorted(g)) or "none"))
                miss += 1
    print("MEAS7B_CHECK hits=%d misses=%d (of 22: eleven cells x two probes)" % (hit, miss))


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        write()
    elif sys.argv[1:2] == ["pretable"] and len(sys.argv) == 5:
        sys.stdout.write(pretable(sys.argv[2], sys.argv[3], sys.argv[4], rd(os.path.join(HERE, "CHANNELS7.txt"))))
    elif sys.argv[1:2] == ["check"] and len(sys.argv) == 4:
        check(sys.argv[2], sys.argv[3])
    elif sys.argv[1:2] == ["check7b"] and len(sys.argv) == 4:
        check7b(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
