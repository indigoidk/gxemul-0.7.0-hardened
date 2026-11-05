#!/usr/bin/env python3
"""pvr_variants_4.py -- test-variant TABLE 4 for pvrrenderexit (repair 4: rule D2-F's half-pixel rows and the swap body's far end;
the 140-row probe), 2026-11-05.

Baseline: dev_pvr.c.fix4, a copy of the fixed source (== GXEMUL-SEC src/devices/dev_pvr.c == ../r3_20261105/dev_pvr.c.fix3, checked).
Variants (146), each COPIED and checked byte-identical to the file already built from it:
  * table 3's 128 (../r3_20261105/variants/*.c, as table 3 measured them -- its MD5.txt);
  * codex pass 4's 18 (meas_B/variants/*.c, pvr_variants_B.py, measured on the 128-row probe in meas_B/): B1s B2s B13s B14s and the
    seven half-exchange deletions B4s-B10t (rule D2-F FLOOR), B3s B11s B12t (clause-(e) DEBT), B1t B2t B13t B14t (EQUIVALENT).
PREDICTIONS, every one an exact red set over the 140 rows:
  * the 128 rows that carry over (unchanged: swap and zswap gained one pixel read at the END of their reads) -- the red set MEASURED
    by table 3 (../r3_20261105/table3/SCORES.txt) for its 128 variants and legs, and by meas_B/SCORES.txt for the 18 (all none);
  * the 12 repair-4 rows -- DERIVED per variant below (NEW4), every Z-on row and its Z-off twin listed by name, never added by a rule:
    the table-3 miss (Vt) was a twin dropped by a name-prefix rule, so this table has no twin rule at all.
usage: pvr_variants_4.py write | pretable <base.out> <frozen probe> | check <SCORES.txt> <base.out>"""
import glob
import hashlib
import io
import os
import re
import sys

NL = chr(10)
HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.dirname(HERE)
R3 = os.path.join(UP, "r3_20261105")
SEC = next(p for p in ("C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c",
                       "/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c") if os.path.exists(p))


def rd(p):
    return io.open(p, encoding="latin-1", newline="").read()


FIX = rd(os.path.join(HERE, "dev_pvr.c.fix4"))
assert FIX == rd(SEC), "dev_pvr.c.fix4 is not GXEMUL-SEC's dev_pvr.c"
assert FIX == rd(os.path.join(R3, "dev_pvr.c.fix3")), "dev_pvr.c.fix4 is not table 3's baseline"

T3V = {os.path.basename(p)[:-2]: p for p in glob.glob(os.path.join(R3, "variants", "*.c"))}
BV = {os.path.basename(p)[:-2]: p for p in glob.glob(os.path.join(HERE, "meas_B", "variants", "*.c"))}
assert len(T3V) == 128 and len(BV) == 18 and not set(T3V) & set(BV), (len(T3V), len(BV))
for _n, _p in list(T3V.items()) + list(BV.items()):
    assert rd(_p) != FIX, _n


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


#  each table-3 variant is the file table 3 built (its MD5.txt), each B variant the file meas_B built (its MD5.txt)
def _md5s(path):
    out = {}
    for line in io.open(path, encoding="utf-8"):
        h, _, f = line.strip().partition("  ")
        out[os.path.basename(f.lstrip("*"))] = h
    return out


_M3, _MB = _md5s(os.path.join(R3, "table3", "MD5.txt")), _md5s(os.path.join(HERE, "meas_B", "MD5.txt"))
for _n, _p in T3V.items():
    assert _M3.get(_n + ".c") == md5(_p), ("table-3 variant differs from the one table 3 built", _n)
for _n, _p in BV.items():
    assert _MB.get(_n + ".c") == md5(_p), ("B variant differs from the one meas_B built", _n)

UB = {"Y2s_simple_ltm1", "Y2t_tex_ltm1", "Y4s_simple_gt", "Y4t_tex_gt"}
WHY_UB = {"Y2": "y = -1 admitted: the colour store lands before VRAM and the depth read before vram_z -- undefined behaviour, NOT "
                "PREDICTED (tables 2 and 3 measured the whole y-edges sessions and their Z-off twins red)",
          "Y4": "y = 480 admitted: the depth read vram_z[307200 + x] is past the frame-exact buffer -- undefined behaviour, NOT "
                "PREDICTED (tables 2 and 3 measured `b out` and its twin red)"}

# ---- the 12 repair-4 rows, and the red set each variant gives them (derivations: r4_20261105/PVR4_NOTE.md, "table 4")
NEWROWS = ["swap_s_start", "zswap_s_start", "half_swap", "half_r_x1", "half_r_x2", "zhalf_swap", "zhalf_r_x1", "zhalf_r_x2",
           "ramp8_r_end", "zramp8_r_end", "texramp8_r_end", "ztramp8_r_end"]
ZOFF4 = ["zswap_s_start", "zhalf_swap", "zhalf_r_x1", "zhalf_r_x2", "zramp8_r_end", "ztramp8_r_end"]   # every row in a Z-off session
RIGHT = ["half_r_x1", "half_r_x2", "zhalf_r_x1", "zhalf_r_x2"]
UNSWAPPED = ["swap_s_start", "zswap_s_start", "half_swap", "zhalf_swap", "half_r_x2", "zhalf_r_x2", "ramp8_r_end", "zramp8_r_end"]
RAMPS = ["ramp8_r_end", "zramp8_r_end"]
TRAMPS = ["texramp8_r_end", "ztramp8_r_end"]
NEW4 = {
    # table 2's variants
    "B1_exit": ZOFF4,                                      # every Z-off session ends the process
    "E1s_simple_ltx2": RAMPS,                              # 448 is RAMP8's last column: not drawn; COVER8's blue
    "E1t_tex_ltx2": TRAMPS,
    "E2s_simple_lex2p1": [], "E2t_tex_lex2p1": [],
    "K1_mask26_and3": [], "K2_mask25_and3": [],            # no repair-4 header sets word 1 bit 25 or 27
    "L1s_simple_lt1left": [], "L1t_tex_lt1left": [],
    "M10_reset_in_resetta": [], "M17_reset_at_end": [], "M32_reset1": [], "M33_reset_in_loop": [], "M9_noreset": [],
    "M11_decline": ZOFF4,                                  # Z-off polygons not drawn
    "M12_hoist_simple": ["zswap_s_start", "zhalf_swap", "zhalf_r_x1", "zhalf_r_x2", "zramp8_r_end"],   # simpleline Z-off: nothing
    "M28_hoist_tex": ["ztramp8_r_end"],
    "M13_ztest_bypass_simple": [], "M14_ztest_bypass_tex": [],
    "M15_simple_never_store": ["ramp8_r_end"], "M16_tex_never_store": ["texramp8_r_end"],
    "M18_simple_lo_ge": [], "M19_simple_lo_gt1": [], "M1_simple_unguarded": [], "M2_tex_unguarded": [],
    "M20_simple_hi_le": [],                                # column 640 lands at (0, y + 1): no row reads there
    "M21_simple_hi_lt1": RIGHT,                            # column 639 not drawn
    "M22_tex_lo_ge": [], "M23_tex_lo_gt1": [], "M24_tex_hi_le": [], "M25_tex_hi_lt1": [],
    "M26_simple_ztest_del": ["ramp8_r_end"], "M26b_tex_ztest_del": ["texramp8_r_end"],
    "M27_tex_zon_bypass": ["texramp8_r_end"], "M27b_simple_zon_bypass": ["ramp8_r_end"],
    "M29_simple_lt": [], "M30_tex_lt": [], "M31_bit25": [],
    "M3_simple_inv": ["ramp8_r_end"], "M4_tex_inv": ["texramp8_r_end"],
    "M5_assign0": [], "M6_assign1": ["ramp8_r_end", "texramp8_r_end"], "M7_assign_inv": ["ramp8_r_end", "texramp8_r_end"],
    "M8_sticky": [],
    "O1s_simple_orleft": [], "O1t_tex_orleft": [],
    "O2s_simple_orright": RIGHT, "O2t_tex_orright": [],    # 670.0 >= 640: the row returns
    "R1s_simple_gem1right": RIGHT, "R1t_tex_gem1right": [],
    "S1s_simple_noswap": UNSWAPPED, "S1t_tex_noswap": TRAMPS,
    "X1s_simple_start1": ["swap_s_start", "zswap_s_start"] + RIGHT + RAMPS,   # 399.5 + 1 -> 400; 639.5 + 1 -> 640; 448 at 1.875
    "X1t_tex_start1": TRAMPS,                              # 448 samples texel (3,0), never stored
    "Y1s_simple_lt1": [], "Y1t_tex_lt1": [], "Y3s_simple_gem1": [], "Y3t_tex_gem1": [],
    # table 3's new variants
    "As_start_m1": [], "At_start_m1": [],                  # 448 at 2.125: colour clamps to magenta / texel (4,0) still green
    "Bs_swap_gt_p1": ["swap_s_start", "zswap_s_start", "half_swap", "zhalf_swap"], "Bt_swap_gt_p1": [],
    "Cs_swap_ge": [], "Ct_swap_ge": [], "Ds_left_x2x2": [], "Dt_left_x2x2": [],
    "Es_right_x1x1": ["half_r_x2", "zhalf_r_x2"], "Et_right_x1x1": [],
    "Fs_zoff_eq_refused": [], "Ft_zoff_eq_refused": [], "G_decode_eq1": [], "H_decode_and5": [],
    "Is_end_lt_p1": [], "It_end_lt_p1": [],
    "Zs_swap_noz": RAMPS, "Rs_swap_nor": RAMPS, "Gs_swap_nog": RAMPS, "Bs_swap_nob": RAMPS,
    "Xs_swap_nox": UNSWAPPED,
    "Zt_swap_noz": TRAMPS, "Ut_swap_nou": TRAMPS, "Vt_swap_nov": TRAMPS, "Xt_swap_nox": TRAMPS,
    "R1as_right_x1_m1": ["half_r_x1", "zhalf_r_x1"], "R1at_right_x1_m1": [],
    "R2s_right_x2_m1": ["half_r_x2", "zhalf_r_x2"], "R2t_right_x2_m1": [],
    "Ns_inner_or": [], "Nt_inner_or": [],
    "Q1s_right_x1_ysize": ["half_r_x1", "zhalf_r_x1"], "Q2s_right_x2_ysize": ["half_r_x2", "zhalf_r_x2"], "Q2t_right_x2_ysize": [],
    "Q3s_inner_ysize": RIGHT,
    "Ps_ztest_zp1": ["ramp8_r_end"], "Pms_ztest_zm1": ["zramp8_r_end"], "Pt_ztest_zp1": ["texramp8_r_end"],
    "H9_decode_and9": [], "H17_decode_and17": [], "H33_decode_and33": [], "H65_decode_and65": [],
    "D3_decode_list3": ["texramp8_r_end"],                 # textured headers (word 3 bit 26 set) store no depth
    "S27_decode_shift27": [],
    "W1s_inner_zw": [], "W1t_inner_zw": [], "W2s_y_zw": [], "W2t_y_zw": [],
    "W3s_left_x1_bpp": [], "W3t_left_x1_bpp": [], "W4s_left_x2_bpp": [], "W4t_left_x2_bpp": [],
    "V1s_y_lo_2zw": [], "V1t_y_hi_2zw": [], "V2s_left_x1_2zw": [], "V2t_left_x2_2zw": [],
    "V3s_right_x1_2zw": ["zhalf_r_x1"], "V3t_right_x2_2zw": [],
    "V4s_swap_p2zw": ["zswap_s_start", "zhalf_swap"], "V4t_swap_m2zw": [],
    "V5s_start_m2zw": [],                                  # zramp8: 448 at 2.25, colour clamps to magenta
    "V5t_start_p2zw": ["ztramp8_r_end"],                   # 448 samples texel (3,0), never stored
    "V6s_end_m2zw": ["zswap_s_start", "zhalf_swap", "zramp8_r_end"], "V6t_end_p2zw": [],
    "V7s_inner_hi_2zw": ["zhalf_r_x1", "zhalf_r_x2"], "V7t_inner_lo_2zw": [],
    # codex pass 4's
    "B1s_swap_half": ["half_swap", "zhalf_swap"],
    "B2s_start_half": ["swap_s_start", "zswap_s_start"] + RIGHT,   # 399.5 + 0.5 -> 400; 639.5 + 0.5 -> 640
    "B13s_right_x1_half": ["half_r_x1", "zhalf_r_x1"], "B14s_right_x2_half": ["half_r_x2", "zhalf_r_x2"],
    "B4s_noz2": RAMPS, "B5s_nor2": RAMPS, "B6s_nog2": RAMPS, "B7s_nob2": RAMPS,
    "B8t_noz2": TRAMPS, "B9t_nou2": TRAMPS, "B10t_nov2": TRAMPS,
    "B3s_end_q": [], "B11s_ztest_q": [], "B12t_ztest_q": [],
    "B1t_swap_half": [], "B2t_start_half": [], "B13t_right_x1_half": [], "B14t_right_x2_half": [],
}
assert set(NEW4) | UB == set(T3V) | set(BV), sorted((set(NEW4) | UB) ^ (set(T3V) | set(BV)))
assert not set(NEW4) & UB
for _n, _v in NEW4.items():
    assert all(r in NEWROWS for r in _v) and len(set(_v)) == len(_v), _n
#  the swap-body exchange deletions (whole and half) red BOTH twins -- the Vt lesson, written out rather than derived by a rule
for _n in ("Zs_swap_noz", "Rs_swap_nor", "Gs_swap_nog", "Bs_swap_nob", "B4s_noz2", "B5s_nor2", "B6s_nog2", "B7s_nob2"):
    assert set(NEW4[_n]) == set(RAMPS), _n
for _n in ("Zt_swap_noz", "Ut_swap_nou", "Vt_swap_nov", "B8t_noz2", "B9t_nou2", "B10t_nov2"):
    assert set(NEW4[_n]) == set(TRAMPS), _n

GREEN_WHY = {
    "M17_reset_at_end": "EQUIVALENT (tables 1-3): the one early exit after the reset's old position, the frame-outside-VRAM return "
                        "(dev_pvr.c:1166), comes before every header of its render, and the field is zero there, from DEVINIT or the "
                        "previous render's end -- the reason as the pass-4 ruling corrected it (F8); the class unchanged",
    "L1s_simple_lt1left": "EQUIVALENT (table 2): no probed span has both ends in [0, 1), and `x > 0` never draws column 0",
    "L1t_tex_lt1left": "EQUIVALENT (table 2): the same",
    "It_end_lt_p1": "EQUIVALENT: texturedline's span ends are ints, so `x < x2 + 1` is `x <= x2`",
    "H65_decode_and65": "EQUIVALENT: (list[1] >> 26) is below 64, so `& 65` is `& 1`",
    "B1t_swap_half": "EQUIVALENT (rule D2-F (iv)): texturedline's ends are ints, so `x1 > x2 + 0.5` is `x1 > x2`",
    "B2t_start_half": "EQUIVALENT (rule D2-F (iv)): x1 is an int, so (int)(x1 + 0.5) is x1",
    "B13t_right_x1_half": "EQUIVALENT (rule D2-F (iv)): x1 is an int, so `x1 >= xsize - 0.5` is `x1 >= xsize`",
    "B14t_right_x2_half": "EQUIVALENT (rule D2-F (iv)): x2 is an int, so `x2 >= xsize - 0.5` is `x2 >= xsize`",
    "B3s_end_q": "clause-(e) DEBT (rule D2-F (ii)): a quarter pixel is below the half pixel `swap frac past` pins; SAMPLED, not "
                 "claimed (measured green on 140 rows, meas_B140/)",
    "B11s_ztest_q": "clause-(e) DEBT (rule D2-F (iii)): the depth compare has no unit; `<= z + c` is sampled at 1.0 and 0.5 only "
                    "(measured green on 140 rows, meas_B140/)",
    "B12t_ztest_q": "clause-(e) DEBT (rule D2-F (iii)): the same in texturedline (measured green on 140 rows, meas_B140/)",
}


def scores(path):
    """{leg: [red rows]} from a SCORES.txt (table 3's, meas_B's, or this table's)."""
    out = {}
    for line in io.open(path, encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.split("RED=", 1)[1].split()[0]
            out[p[0]] = [] if red == "none" else red.split(",")
        elif len(p) > 1 and "BUILD-FAILED" in line:
            out[p[0]] = "BUILD-FAILED"
    return out


def rowlist(base_out):
    """The 140 row names in the base run's order (spaces as underscores, as PVR_ZWRITE_RED prints them)."""
    names = []
    for line in io.open(base_out, encoding="latin-1"):
        m = re.match(r"^(\S.{0,15}?)\s{2,}\S.*\s(ok|FAIL)$", line.rstrip("\n"))
        if m and not line.startswith("row "):
            names.append(m.group(1).strip().replace(" ", "_"))
    assert len(names) == 140 and len(set(names)) == 140, len(names)
    assert all(r in names for r in NEWROWS)
    return names


SESSION_ROWS = ("id_session", "zon_session", "zoff_session", "ovoff_session", "behind_session", "texoff_session", "texbeh_session",
                "two_session", "sticky_session")


def predictions(rows):
    t3 = scores(os.path.join(R3, "table3", "SCORES.txt"))
    mb = scores(os.path.join(HERE, "meas_B", "SCORES.txt"))
    assert all(isinstance(t3.get(n), list) for n in T3V) and all(isinstance(mb.get(n), list) for n in BV)
    old = [r for r in rows if r not in NEWROWS]
    assert len(old) == 128
    P = {}
    for n in sorted(T3V) + sorted(BV):
        if n in UB:
            P[n] = None
            continue
        carried = t3[n] if n in T3V else mb[n]
        assert all(r in old for r in carried), (n, carried)
        P[n] = sorted(set(carried) | set(NEW4[n]), key=rows.index)
    legs = {"base": [],
            "HEAD": sorted(set(t3["HEAD"]) | set(ZOFF4), key=rows.index),
            "null_true": [r for r in rows if r not in SESSION_ROWS],
            "null_absent": list(rows),
            "null_false": [r for r in rows if r != "neg_apparatus"],
            "restored": []}
    return P, legs


def write():
    out = os.path.join(HERE, "variants")
    os.makedirs(out, exist_ok=True)
    for n, p in list(T3V.items()) + list(BV.items()):
        io.open(os.path.join(out, n + ".c"), "w", encoding="latin-1", newline="").write(rd(p))
    print("%d variants written to %s (%d from table 3, %d from meas_B)" % (len(T3V) + len(BV), out, len(T3V), len(BV)))


CHANNELS = """CHANNELS of the 12 repair-4 rows (pixel, want; the variants that move it and the observable; every end below is exact):
  swap s start (399,249) RED -- SWAP row 249 arrives 400.5 / 399.5, swapped: x1 = 399.5, `int x = x1` draws 399 and 400.  B2s
    (`x1 + 0.5`) and X1s (`x1 + 1`) start at 400; Bs (`x1 > x2 + 1`), S1s and Xs leave the row reversed: nothing drawn.
  half swap (101,103) RED -- HALF row 103 arrives 101.25 / 100.75, reversed by 0.5: swapped, it draws 100 and 101.  B1s (`x1 > x2
    + 0.5`), Bs, S1s and Xs leave it reversed; B2s starts at (int) 101.25 = 101 and X1s at (int) 101.75 = 101: both still draw it.
  half r x1 (639,401) RED -- HALFR1 row 401 arrives 639.5 / 670.0, drawn from (int) 639.5 = 639.  B13s (`x1 >= xsize - 0.5`), R1as
    (`x1 >= xsize - 1`), Q1s (`x1 >= ysize`), R1s and O2s return early; M21, Q3s and (Z-off) V7s do not draw column 639; B2s and
    X1s start at 640; V3s (Z-off: `x1 >= xsize - 2`) returns.
  half r x2 (639,411) RED -- HALFR2 row 411 arrives 670.0 / 639.5: not rejected (639.5 < 640), swapped, drawn from 639.  B14s, R2s,
    Q2s, Es (`x1 >= xsize && x1 >= xsize`), R1s and O2s return early; M21, Q3s, V7s, B2s, X1s as above; S1s and Xs leave it reversed.
  zswap s start, zhalf swap / r x1 / r x2 -- the Z-off twins: the same pixels and wants under a Z-off header; also red under B1_exit
    (the process ends), M11 (Z-off not drawn), M12 (simpleline draws nothing Z-off), and the V family where it moves a Z-off edge:
    V4s (`x1 > x2 + 2`) and V6s (`x <= x2 - 2`) on zswap s start and zhalf swap, V3s and V7s as above.
  ramp8 r end (448,60) 0xf81f -- RAMP8 (z 2, 1, 2; magenta, green, magenta) row 60 arrives 448.0 / 440.0, swapped: column 448 is
    eight exact steps (dz 0.125, dr 31.875) from 440 and carries vertex 1's z 2.0 and magenta; COVER8 (Z-on, z 1.5, blue) after it
    fails there.  The z exchange deleted whole (Zs) or half (B4s): z 1.0 there, COVER8 draws blue.  r / g / b deleted whole (Rs Gs
    Bs_swap_nob) or half (B5s B6s B7s): 0x001f / 0xffff / 0xf800.  The depth test loosened or bypassed for COVER8 (Ps, M26, M27b),
    or RAMP8 storing no depth (M15, M3, M6, M7): COVER8's blue.  E1s (`x < x2`): 448 not drawn by RAMP8, COVER8's blue; S1s / Xs:
    RAMP8 not drawn; X1s: 448 at z 1.875, colour 0xd8fb.  As (`x1 - 1`): 448 at z 2.125 and colour (286.875, -31.875, 286.875),
    which CLAMPS to magenta -- green.
  zramp8 r end (448,60) 0xf81f -- COVER8 (Z-on, z 1.5, blue) FIRST, then RAMP8 Z-off: 2.0 passes over the stored 1.5 and draws
    magenta.  Zs / B4s: z 1.0 fails, blue stays; Rs-Bs / B5s-B7s: the colours above; Pms (`<= z - 1`): 1.5 <= 1.0 fails; E1s, V6s
    (Z-off end - 2): 448 not drawn; S1s, Xs: nothing drawn; X1s: 0xd8fb at 1.875 (passes 1.5); M11, M12, B1_exit: Z-off not drawn
    or the process ends.  V5s (Z-off `x1 - 2`): 448 at 2.25, the colour clamps to magenta -- green.
  texramp8 r end (448,60) GREEN -- RAMP8 textured, (u,v) (0.5,0) (0,0.125) (0.5,0): 448 samples (0.5, 0), texel (4,0), green, at z
    2.0; COVER8 textured through TEX_01 (texel (0,0) = TEXEL01, blue) fails there.  Zt / B8t: z 1.0, COVER8's blue; Ut / B9t: texel
    (0,0), red; Vt / B10t: texel (4,1), never stored, 0x0000; E1t, S1t, Xt: 448 not drawn by RAMP8, COVER8's blue; X1t: texel
    (3,0), 0x0000 (linear 0x500002, never stored); Pt, M26b, M27, M16, M4, M6, M7, D3 (textured headers store no depth): COVER8's
    blue.  At (`x1 - 1`): (0.5625, -0.015625) is still texel (4,0) -- green.
  ztramp8 r end (448,60) GREEN -- COVER8 textured (Z-on, 1.5, blue) FIRST, then RAMP8 textured Z-off: 2.0 passes, texel (4,0).
    Zt / B8t: 1.0 fails, blue stays; Ut / B9t red; Vt / B10t 0x0000; E1t, S1t, Xt: blue; X1t, V5t (Z-off `x1 + 2`): texel (3,0),
    0x0000; M11, M28, B1_exit: not drawn / the process ends."""


def pretable(base_out, frozen):
    rows = rowlist(base_out)
    P, legs = predictions(rows)
    npred = sum(1 for v in P.values() if v is not None)
    nred = sum(1 for v in P.values() if v)
    green = sorted(n for n, v in P.items() if v == [])
    assert set(green) == set(GREEN_WHY), sorted(set(green) ^ set(GREEN_WHY))
    L = ["PRETABLE_4 -- pvrrenderexit, test-variant table 4 (repair 4: rule D2-F's half-pixel rows and the swap body's far end; 140 rows).",
         "Written BEFORE table 4 runs: its mtime must precede every RESULT file in table4/ (the frozen probe is copied there first and is",
         "older).  INSTRUMENT: table4/probe140_frozen.py, cmp-identical to regress/pvr_zwrite_probe.py when this was written (140/140 on",
         "build/ in base140f/, with both clearance parts recorded in base140f/CLEARANCE.txt).  Baseline: dev_pvr.c.fix4 (== GXEMUL-SEC",
         "src/devices/dev_pvr.c == ../r3_20261105/dev_pvr.c.fix3).  Variants: pvr_variants_4.py (table 3's 128 + codex pass 4's 18).",
         "INSTRUMENT_MD5 %s table4/probe140_frozen.py" % md5(frozen),
         "EVERY prediction is EXACT -- the full red set, none = all 140 green -- except Y2s/Y2t/Y4s/Y4t (undefined behaviour, NOT",
         "PREDICTED, counted in no tally).  The 128 rows that carry over: the red set MEASURED by table 3 (../r3_20261105/table3/SCORES.txt;",
         "for the 18 B variants, meas_B/SCORES.txt: none).  The 12 repair-4 rows: DERIVED per variant (pvr_variants_4.py NEW4), each Z-on",
         "row and each Z-off twin listed BY NAME -- no twin rule: table 3's one miss (Vt) was a twin a name-prefix rule dropped.  The",
         "swap-body exchange deletions, whole and half, red BOTH twins (Zs Rs Gs Bs_swap_nob B4s-B7s: ramp8 and zramp8; Zt Ut Vt",
         "B8t-B10t: texramp8 and ztramp8).",
         "%d variants: %d predicted, %d predicted red, %d predicted green, 4 NOT PREDICTED.  The green ones, named: five EQUIVALENT from"
         % (len(P), npred, nred, npred - nred),
         "tables 1-3 (M17, L1s, L1t, It, H65); the four textured fractional moves, EQUIVALENT by rule D2-F (iv) (B1t, B2t, B13t, B14t); and",
         "the three clause-(e) DEBT variants (B3s, B11s, B12t), already measured green on these 140 rows in meas_B140/SCORES.txt.",
         "Legs: base 140/140 CONTROL=OK SYMPTOM=ABSENT; HEAD (det_20261104/dev_pvr.c.HEAD, the exit) 66/140 SYMPTOM=PRESENT CONTROL=OK --",
         "table 3's 68 red rows plus the six repair-4 rows in Z-off sessions: MEASURED already, head140/; null media CONTROL=FAIL:",
         "/bin/true 9/140 (only the nine `session` rows, which want exit 0), an absent binary 0/140, /bin/false 1/140 (`neg apparatus`).",
         ""] + CHANNELS.split(NL) + ["", "LEGS:"]
    for k, v in legs.items():
        L.append("   %-24s exactly: %s" % (k, ",".join(v) if v else "none"))
    L += ["", "VARIANTS:"]
    for n in sorted(T3V) + sorted(BV):
        v = P[n]
        if v is None:
            L.append("   %-24s NOT PREDICTED (%s)" % (n, WHY_UB[n[:2]]))
        elif not v:
            L.append("   %-24s exactly: none -- GREEN (%s)" % (n, GREEN_WHY[n]))
        else:
            L.append("   %-24s exactly: %s" % (n, ",".join(v)))
    return NL.join(L) + NL


def check(scores_path, base_out):
    """Score a finished table against this script's own predictions (the ones PRETABLE_4.out records)."""
    rows = rowlist(base_out)
    P, legs = predictions(rows)
    got = scores(scores_path)
    hit = miss = npr = 0
    for n, want in list(legs.items()) + [(k, P[k]) for k in sorted(T3V) + sorted(BV)]:
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
        elif set(g) == set(want):
            hit += 1
        else:
            print("PRED=MISS    %s want=%s got=%s" % (n, ",".join(want) or "none", ",".join(sorted(g, key=rows.index)) or "none"))
            miss += 1
    print("TABLE4_CHECK hits=%d misses=%d not_predicted=%d" % (hit, miss, npr))


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        write()
    elif sys.argv[1:2] == ["pretable"] and len(sys.argv) == 4:
        sys.stdout.write(pretable(sys.argv[2], sys.argv[3]))
    elif sys.argv[1:2] == ["check"] and len(sys.argv) == 4:
        check(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
