#!/usr/bin/env python3
"""pvr_variants_3.py -- test-variant TABLE 3 for pvrrenderexit (repair 3: the class closure completed; the 128-row probe), 2026-11-05.

Baseline: dev_pvr.c.fix3, a copy of the fixed source (== GXEMUL-SEC src/devices/dev_pvr.c == ../det_20261104/dev_pvr.c.fix, checked).
Variants (128):
  * table 2's 62, re-created by COPY from ../r2_20261105/variants/ (each is an edit of the same baseline, checked non-trivial);
  * codex pass 3's A-I (16: As At Bs Bt Cs Ct Ds Dt Es Et Fs Ft G H Is, and It, the claimed-EQUIVALENT texturedline twin of I) and
    the swap-body cells of both Gemini pass-3 readings (9: Zs Rs Gs Bs_swap_nob Xs, Zt Ut Vt Xt) -- regenerated here and checked
    byte-identical to the files MEASURED in step 2 (meas_AI/variants, meas_SW/variants);
  * one representative per further closure family (19, CLOSURE3.md): the right clause's x1 and x2 compares tightened alone (R1as
    R1at R2s R2t); the inner x test's `&&` made `||` (Ns Nt -- the pass-2 rulings' P6 asked for these and table 2 never built them);
    xsize/ysize field swaps (Q1s Q2s Q2t: the right clause's x1 / x2 operand; Q3s: the inner x bound); the depth test's bound moved
    by +1 / -1 (Ps Pms Pt); the decode mask widened to bit 29, 30, 31 (H9 H17 H33) and past bit 31 (H65, EQUIVALENT); the decode
    reading list[3] (D3) and shifted by 27 (S27);
  * the closure's own operand-swap / edge cells (8, measured in step 2c, meas_W/variants): `x > d->zwrite_disabled` (W1s W1t), `y <
    d->zwrite_disabled` (W2s W2t), the left clause's x1 / x2 compare moved up by 2 (`< d->bytes_per_pixel`: W3s W3t, W4s W4t);
  * one MULTI-TOKEN representative per geometry predicate per rasterizer (14, the Z-off twins' family -- the coordinator's ruling):
    a bound of P1-P7 moved by 2 * d->zwrite_disabled, so Z-on polygons are untouched and Z-off ones meet a moved edge (V1s-V7t).
Every new variant is ONE exact-text edit: its text must occur exactly once inside the function it edits (simpleline, texturedline,
or the whole file for the case-4 decode), or the script refuses.
usage: pvr_variants_3.py write | pretable <base.out> | check <SCORES.txt>"""
import glob
import io
import os
import re
import sys

TAB, NL = chr(9), chr(10)
HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.dirname(HERE)
#  the same file from Windows python ("C:/...") or WSL python ("/mnt/c/..."): table3_pvr.sh runs `check` under WSL
SEC = next(p for p in ("C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c",
                       "/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_pvr.c") if os.path.exists(p))
FIX3P = os.path.join(HERE, "dev_pvr.c.fix3")


def rd(p):
    return io.open(p, encoding="latin-1", newline="").read()


FIX = rd(FIX3P)
assert FIX == rd(SEC), "dev_pvr.c.fix3 is not GXEMUL-SEC's dev_pvr.c"
assert FIX == rd(os.path.join(UP, "det_20261104", "dev_pvr.c.fix")), "dev_pvr.c.fix3 is not table 1/2's baseline"

#  function regions: an edit's text must occur exactly once inside its function
_S0 = FIX.index("static void simpleline(")
_T0 = FIX.index("static void texturedline(")
_T1 = FIX.index("// Slow software rendering, for debugging:" + NL + "static void pvr_render_triangle(")
assert FIX.count("static void simpleline(") == 1 and FIX.count("static void texturedline(") == 1 and _S0 < _T0 < _T1
REG = {"s": (_S0, _T0), "t": (_T0, _T1), "f": (0, len(FIX))}


def edit(where, old, new):
    """ONE exact-text edit of the baseline: `old` must occur exactly once in the region `where` (s, t, or f = the file)."""
    a, b = REG[where]
    region = FIX[a:b]
    assert region.count(old) == 1, ("NOT EXACTLY ONCE", where, old[:70], region.count(old))
    out = FIX[:a] + region.replace(old, new) + FIX[b:]
    assert out != FIX
    return out


YL = TAB + "if (y < 0 || y >= d->ysize || (x1 < 0 && x2 < 0)" + NL
XL = TAB + "     || (x1 >= d->xsize && x2 >= d->xsize))" + NL
LOOPX = TAB + "for (int x = x1; x <= x2; ++x) {" + NL
SWAPL = TAB + "if (x1 > x2) {" + NL
INX = TAB * 2 + "if (x > 0 && x < d->xsize) {" + NL
ZT = TAB * 3 + "if (d->vram_z[ofs] <= z) {" + NL
ZBIT = TAB * 3 + "zwrite = ! ((list[1] >> 26) & 1);" + NL
T2 = TAB * 2

NEW = {}
for r in ("s", "t"):
    NEW["A%s_start_m1" % r] = edit(r, LOOPX, LOOPX.replace("int x = x1;", "int x = x1 - 1;"))
    NEW["B%s_swap_gt_p1" % r] = edit(r, SWAPL, SWAPL.replace("(x1 > x2)", "(x1 > x2 + 1)"))
    NEW["C%s_swap_ge" % r] = edit(r, SWAPL, SWAPL.replace("(x1 > x2)", "(x1 >= x2)"))
    NEW["D%s_left_x2x2" % r] = edit(r, YL, YL.replace("(x1 < 0 && x2 < 0)", "(x2 < 0 && x2 < 0)"))
    NEW["E%s_right_x1x1" % r] = edit(r, XL, XL.replace("(x1 >= d->xsize && x2 >= d->xsize)", "(x1 >= d->xsize && x1 >= d->xsize)"))
    NEW["F%s_zoff_eq_refused" % r] = edit(r, ZT, ZT.replace("d->vram_z[ofs] <= z",
                                                            "d->vram_z[ofs] < z || (!d->zwrite_disabled && d->vram_z[ofs] == z)"))
    NEW["I%s_end_lt_p1" % r] = edit(r, LOOPX, LOOPX.replace("x <= x2;", "x < x2 + 1;"))
NEW["G_decode_eq1"] = edit("f", ZBIT, ZBIT.replace(">> 26) & 1)", ">> 26) == 1)"))
NEW["H_decode_and5"] = edit("f", ZBIT, ZBIT.replace(">> 26) & 1)", ">> 26) & 5)"))
#  the swap body (Gemini x2): one exchange deleted; a declaring line keeps its declaration so the block compiles
NEW["Zs_swap_noz"] = edit("s", T2 + "tmpf = z1; z1 = z2; z2 = tmpf;" + NL, "")
NEW["Rs_swap_nor"] = edit("s", T2 + "tmpf = r1; r1 = r2; r2 = tmpf;" + NL, "")
NEW["Gs_swap_nog"] = edit("s", T2 + "tmpf = g1; g1 = g2; g2 = tmpf;" + NL, "")
NEW["Bs_swap_nob"] = edit("s", T2 + "tmpf = b1; b1 = b2; b2 = tmpf;" + NL, "")
NEW["Xs_swap_nox"] = edit("s", T2 + "double tmpf = x1; x1 = x2; x2 = tmpf;" + NL, T2 + "double tmpf = x1;" + NL)
NEW["Zt_swap_noz"] = edit("t", T2 + "double tmpf = z1; z1 = z2; z2 = tmpf;" + NL, T2 + "double tmpf = z1;" + NL)
NEW["Ut_swap_nou"] = edit("t", T2 + "tmpf = u1; u1 = u2; u2 = tmpf;" + NL, "")
NEW["Vt_swap_nov"] = edit("t", T2 + "tmpf = v1; v1 = v2; v2 = tmpf;" + NL, "")
NEW["Xt_swap_nox"] = edit("t", T2 + "int tmp = x1; x1 = x2; x2 = tmp;" + NL, T2 + "int tmp = x1; (void) tmp;" + NL)
#  further closure families, one representative each (CLOSURE3.md)
for r in ("s", "t"):
    NEW["R1a%s_right_x1_m1" % r] = edit(r, XL, XL.replace("(x1 >= d->xsize && x2", "(x1 >= d->xsize - 1 && x2"))
    NEW["R2%s_right_x2_m1" % r] = edit(r, XL, XL.replace("x2 >= d->xsize))", "x2 >= d->xsize - 1))"))
    NEW["N%s_inner_or" % r] = edit(r, INX, INX.replace("x > 0 && x <", "x > 0 || x <"))
NEW["Q1s_right_x1_ysize"] = edit("s", XL, XL.replace("(x1 >= d->xsize && x2", "(x1 >= d->ysize && x2"))
NEW["Q2s_right_x2_ysize"] = edit("s", XL, XL.replace("x2 >= d->xsize))", "x2 >= d->ysize))"))
NEW["Q2t_right_x2_ysize"] = edit("t", XL, XL.replace("x2 >= d->xsize))", "x2 >= d->ysize))"))
NEW["Q3s_inner_ysize"] = edit("s", INX, INX.replace("x < d->xsize", "x < d->ysize"))
NEW["Ps_ztest_zp1"] = edit("s", ZT, ZT.replace("<= z)", "<= z + 1)"))
NEW["Pms_ztest_zm1"] = edit("s", ZT, ZT.replace("<= z)", "<= z - 1)"))
NEW["Pt_ztest_zp1"] = edit("t", ZT, ZT.replace("<= z)", "<= z + 1)"))
NEW["H9_decode_and9"] = edit("f", ZBIT, ZBIT.replace(">> 26) & 1)", ">> 26) & 9)"))
NEW["H17_decode_and17"] = edit("f", ZBIT, ZBIT.replace(">> 26) & 1)", ">> 26) & 17)"))
NEW["H33_decode_and33"] = edit("f", ZBIT, ZBIT.replace(">> 26) & 1)", ">> 26) & 33)"))
NEW["H65_decode_and65"] = edit("f", ZBIT, ZBIT.replace(">> 26) & 1)", ">> 26) & 65)"))
NEW["D3_decode_list3"] = edit("f", ZBIT, ZBIT.replace("list[1] >> 26", "list[3] >> 26"))
NEW["S27_decode_shift27"] = edit("f", ZBIT, ZBIT.replace(">> 26) & 1)", ">> 27) & 1)"))
#  the closure's own cells (step 2c): operand swaps from fields the body reads, and the left clause's compares at their +2 edge
for r in ("s", "t"):
    NEW["W1%s_inner_zw" % r] = edit(r, INX, INX.replace("x > 0 &&", "x > d->zwrite_disabled &&"))
    NEW["W2%s_y_zw" % r] = edit(r, YL, YL.replace("y < 0 ||", "y < d->zwrite_disabled ||"))
    NEW["W3%s_left_x1_bpp" % r] = edit(r, YL, YL.replace("(x1 < 0 &&", "(x1 < d->bytes_per_pixel &&"))
    NEW["W4%s_left_x2_bpp" % r] = edit(r, YL, YL.replace("&& x2 < 0)", "&& x2 < d->bytes_per_pixel)"))
#  the Z-off twins' family: one multi-token edit per geometry predicate per rasterizer, a bound moved by 2 * d->zwrite_disabled
ZW2 = "2 * d->zwrite_disabled"
NEW["V1s_y_lo_2zw"] = edit("s", YL, YL.replace("y < 0 ||", "y < " + ZW2 + " ||"))
NEW["V1t_y_hi_2zw"] = edit("t", YL, YL.replace("y >= d->ysize ||", "y >= d->ysize - " + ZW2 + " ||"))
NEW["V2s_left_x1_2zw"] = edit("s", YL, YL.replace("(x1 < 0 &&", "(x1 < " + ZW2 + " &&"))
NEW["V2t_left_x2_2zw"] = edit("t", YL, YL.replace("&& x2 < 0)", "&& x2 < " + ZW2 + ")"))
NEW["V3s_right_x1_2zw"] = edit("s", XL, XL.replace("(x1 >= d->xsize && x2", "(x1 >= d->xsize - " + ZW2 + " && x2"))
NEW["V3t_right_x2_2zw"] = edit("t", XL, XL.replace("x2 >= d->xsize))", "x2 >= d->xsize - " + ZW2 + "))"))
NEW["V4s_swap_p2zw"] = edit("s", SWAPL, SWAPL.replace("(x1 > x2)", "(x1 > x2 + " + ZW2 + ")"))
NEW["V4t_swap_m2zw"] = edit("t", SWAPL, SWAPL.replace("(x1 > x2)", "(x1 > x2 - " + ZW2 + ")"))
NEW["V5s_start_m2zw"] = edit("s", LOOPX, LOOPX.replace("int x = x1;", "int x = x1 - " + ZW2 + ";"))
NEW["V5t_start_p2zw"] = edit("t", LOOPX, LOOPX.replace("int x = x1;", "int x = x1 + " + ZW2 + ";"))
NEW["V6s_end_m2zw"] = edit("s", LOOPX, LOOPX.replace("x <= x2;", "x <= x2 - " + ZW2 + ";"))
NEW["V6t_end_p2zw"] = edit("t", LOOPX, LOOPX.replace("x <= x2;", "x <= x2 + " + ZW2 + ";"))
NEW["V7s_inner_hi_2zw"] = edit("s", INX, INX.replace("x < d->xsize) {", "x < d->xsize - " + ZW2 + ") {"))
NEW["V7t_inner_lo_2zw"] = edit("t", INX, INX.replace("x > 0 &&", "x > " + ZW2 + " &&"))
assert len(NEW) == 66 and len(set(NEW.values())) == 66, len(NEW)
#  the step-2 measured files must be byte-identical to their table-3 re-creations
for d in ("meas_AI", "meas_SW", "meas_W"):
    for p in glob.glob(os.path.join(HERE, d, "variants", "*.c")):
        n = os.path.basename(p)[:-2]
        assert NEW[n] == rd(p), "%s differs from its measured step-2 file %s" % (n, p)

OLD = sorted(os.path.basename(p)[:-2] for p in glob.glob(os.path.join(UP, "r2_20261105", "variants", "*.c")))
assert len(OLD) == 62, len(OLD)
for n in OLD:
    assert rd(os.path.join(UP, "r2_20261105", "variants", n + ".c")) != FIX, n
assert not set(OLD) & set(NEW)

# ---- predictions.  Table 2's MEASURED red sets on the 68 rows that carry over (the rows did not change; texyedges dropped only the
# ---- green texel it never samples), plus the red set DERIVED for the 23 repair-3 rows (CLOSURE3.md, "predictions").
UB = {"Y2s_simple_ltm1", "Y2t_tex_ltm1", "Y4s_simple_gt", "Y4t_tex_gt"}
WHY_UB = {"Y2": "y = -1 admitted: the colour store lands before VRAM (FB_RENDER_ADDR1 is 0 here) and the depth read is vram_z[x - "
                "640], before the buffer: undefined behaviour, NOT PREDICTED (table 2 measured the whole y-edges session red)",
          "Y4": "y = 480 admitted: the depth read vram_z[307200 + x] is past the frame-exact buffer: undefined behaviour, NOT "
                "PREDICTED (table 2 measured `b out` red)"}
NEWROWS_OLD = {   # table 2's variants on the 23 repair-3 rows
    "B1_exit": ["zeq_overlap", "texzeq_overlap", "maskoff_overlap", "zleft_tip", "texzleft_tip"],
    "M11_decline": ["zeq_overlap", "texzeq_overlap", "zleft_tip", "texzleft_tip"],
    "M12_hoist_simple": ["zeq_overlap", "zleft_tip"],
    "M15_simple_never_store": ["maskhi_overlap", "ramp_l_end"],
    "M16_tex_never_store": ["texramp_l_end"],
    "M19_simple_lo_gt1": ["edges2_l_rev", "edges2_l_tip", "zleft_tip"],
    "M1_simple_unguarded": ["maskoff_overlap"],
    "M21_simple_hi_lt1": ["edges2_r_rev"],
    "M23_tex_lo_gt1": ["texedges2_l_rev", "texedges2_l_tip", "texzleft_tip"],
    "M25_tex_hi_lt1": ["texedges2_r_rev"],
    "M26_simple_ztest_del": ["maskhi_overlap", "ramp_l_end"],
    "M26b_tex_ztest_del": ["texramp_l_end"],
    "M27_tex_zon_bypass": ["texramp_l_end"],
    "M27b_simple_zon_bypass": ["maskhi_overlap", "ramp_l_end"],
    "M28_hoist_tex": ["texzeq_overlap", "texzleft_tip"],
    "M29_simple_lt": ["zeq_overlap"],
    "M30_tex_lt": ["texzeq_overlap"],
    "M31_bit25": ["maskoff_overlap"],
    "M33_reset_in_loop": ["maskoff_overlap"],
    "M3_simple_inv": ["maskhi_overlap", "maskoff_overlap", "ramp_l_end"],
    "M4_tex_inv": ["texramp_l_end"],
    "M5_assign0": ["maskoff_overlap"],
    "M6_assign1": ["maskhi_overlap", "ramp_l_end", "texramp_l_end"],
    "M7_assign_inv": ["maskhi_overlap", "maskoff_overlap", "ramp_l_end", "texramp_l_end"],
    "E1s_simple_ltx2": ["swap_vert", "edges2_l_tip", "zleft_tip"],
    "E1t_tex_ltx2": ["texswap_s_tip", "texswap_vert", "texedges2_l_tip", "texzleft_tip"],
    "E2s_simple_lex2p1": ["swap_frac_past"],
    "O1s_simple_orleft": ["edges2_l_rev", "edges2_l_tip", "zleft_tip"],
    "O1t_tex_orleft": ["texedges2_l_rev", "texedges2_l_tip", "texzleft_tip"],
    "O2s_simple_orright": ["edges2_r_rev"],
    "O2t_tex_orright": ["texedges2_r_rev"],
    "R1s_simple_gem1right": ["edges2_r_rev"],
    "R1t_tex_gem1right": ["texedges2_r_rev"],
    "S1s_simple_noswap": ["swap_s_tip", "ramp_l_end", "edges2_l_rev", "edges2_r_rev", "edges2_l_tip"],
    "S1t_tex_noswap": ["texswap_s_tip", "texramp_l_end", "texedges2_l_rev", "texedges2_r_rev", "texedges2_l_tip"],
    "X1s_simple_start1": ["swap_vert", "ramp_l_end", "edges2_r_rev"],
    "X1t_tex_start1": ["texswap_vert", "texramp_l_end", "texedges2_r_rev"],
}
PNEW = {   # the 66 new variants on the 91-row probe's rows less zleft/texzleft row 0 (the A-I, swap-body and W variants were MEASURED
    #          green on the 68 old rows except Xs/Xt); the Z-off twin rows are added by twins() below.  Derivations: CLOSURE3.md
    "As_start_m1": ["swap_s_before", "ramp_l_end"],
    "At_start_m1": ["texswap_s_before", "texramp_l_end"],
    "Bs_swap_gt_p1": ["swap_s_tip"],
    "Bt_swap_gt_p1": ["texswap_s_tip"],
    "Cs_swap_ge": ["swap_vert"],
    "Ct_swap_ge": ["texswap_vert"],
    "Ds_left_x2x2": ["edges2_l_rev", "edges2_l_tip"],
    "Dt_left_x2x2": ["texedges2_l_rev", "texedges2_l_tip"],
    "Es_right_x1x1": ["edges2_r_rev"],
    "Et_right_x1x1": ["texedges2_r_rev"],
    "Fs_zoff_eq_refused": ["zeq_overlap"],
    "Ft_zoff_eq_refused": ["texzeq_overlap"],
    "G_decode_eq1": ["maskoff_overlap"],
    "H_decode_and5": ["maskhi_overlap"],
    "Is_end_lt_p1": ["swap_frac_past"],
    "It_end_lt_p1": [],
    "Zs_swap_noz": ["ramp_l_end"],
    "Rs_swap_nor": ["ramp_l_end"],
    "Gs_swap_nog": ["ramp_l_end"],
    "Bs_swap_nob": ["ramp_l_end"],
    "Xs_swap_nox": ["yedges_swap", "yedges_s_end", "swap_s_tip", "ramp_l_end", "edges2_l_rev", "edges2_r_rev", "edges2_l_tip"],
    "Zt_swap_noz": ["texramp_l_end"],
    "Ut_swap_nou": ["texramp_l_end"],
    "Vt_swap_nov": ["texramp_l_end"],
    "Xt_swap_nox": ["texyedges_swap", "texyedges_s_end", "texswap_s_tip", "texramp_l_end", "texedges2_l_rev", "texedges2_r_rev",
                    "texedges2_l_tip"],
    "R1as_right_x1_m1": ["edges_rspan"],
    "R1at_right_x1_m1": ["texedges_rspan"],
    "R2s_right_x2_m1": ["edges2_r_rev"],
    "R2t_right_x2_m1": ["texedges2_r_rev"],
    "Ns_inner_or": ["edges_l_out", "edges_r_out"],
    "Nt_inner_or": ["texedges_l_out", "texedges_r_out"],
    "Q1s_right_x1_ysize": ["edges_r_in", "edges_rspan"],
    "Q2s_right_x2_ysize": ["edges2_r_rev"],
    "Q2t_right_x2_ysize": ["texedges2_r_rev"],
    "Q3s_inner_ysize": ["edges_r_in", "edges_rspan", "edges2_r_rev"],
    "Ps_ztest_zp1": ["ovon_overlap", "behind_overlap", "two_overlap", "sticky_overlap", "mask_overlap", "mask25_overlap",
                     "maskhi_overlap", "ramp_l_end"],
    "Pms_ztest_zm1": ["equal_overlap", "zeq_overlap"],
    "Pt_ztest_zp1": ["texbeh_overlap", "texon_overlap", "texramp_l_end"],
    "H9_decode_and9": ["maskhi_overlap"],
    "H17_decode_and17": ["maskhi_overlap"],
    "H33_decode_and33": ["maskhi_overlap"],
    "H65_decode_and65": [],
    "D3_decode_list3": ["ovoff_overlap", "texbeh_overlap", "texon_overlap", "texramp_l_end", "maskoff_overlap"],
    "S27_decode_shift27": ["ovoff_overlap", "texoff_overlap", "mask_overlap"],
    "W1s_inner_zw": ["zleft_tip"],
    "W1t_inner_zw": ["texzleft_tip"],
    "W2s_y_zw": [],
    "W2t_y_zw": [],
    "W3s_left_x1_bpp": ["edges2_l_tip"],
    "W3t_left_x1_bpp": ["texedges2_l_tip"],
    "W4s_left_x2_bpp": ["zleft_tip"],
    "W4t_left_x2_bpp": ["texzleft_tip"],
    #  the V family: Z-off geometry only, so every red row is a Z-off twin (or zleft/texzleft tip) -- listed in full here, and
    #  twins() adds nothing to a Z-specific variant
    "V1s_y_lo_2zw": ["zyedges_t_in"],
    "V1t_y_hi_2zw": ["ztyedges_b_in"],
    "V2s_left_x1_2zw": ["zedges2_l_tip"],
    "V2t_left_x2_2zw": ["texzleft_tip"],
    "V3s_right_x1_2zw": ["zedges_rspan"],
    "V3t_right_x2_2zw": ["ztedges2_r_rev"],
    "V4s_swap_p2zw": ["zswap_s_tip", "zedges2_l_tip"],
    "V4t_swap_m2zw": ["ztswap_vert"],
    "V5s_start_m2zw": ["zswap_s_before", "zramp_l_end"],
    "V5t_start_p2zw": ["ztedges_rspan", "ztswap_s_tip", "ztswap_vert", "ztedges2_r_rev", "ztramp_l_end"],
    "V6s_end_m2zw": ["zyedges_s_end", "zswap_s_tip", "zswap_vert", "zedges2_l_tip", "zleft_tip"],
    "V6t_end_p2zw": ["ztyedges_s_past"],
    "V7s_inner_hi_2zw": ["zedges_r_in", "zedges_rspan", "zedges2_r_rev"],
    "V7t_inner_lo_2zw": ["ztedges_l_in", "ztedges2_l_rev", "ztedges2_l_tip", "texzleft_tip"],
}
assert set(PNEW) == set(NEW), set(PNEW) ^ set(NEW)
assert set(NEWROWS_OLD) <= set(OLD), set(NEWROWS_OLD) - set(OLD)
EQUIV = {"M17_reset_at_end": "EQUIVALENT (table 1/2): no early exit after the reset's old position; DEVINIT zeroes the field",
         "L1s_simple_lt1left": "EQUIVALENT (table 2): no probed span has both ends in [0, 1), and `x > 0` never draws column 0",
         "L1t_tex_lt1left": "EQUIVALENT (table 2): the same",
         "It_end_lt_p1": "EQUIVALENT: texturedline's span ends are ints, so `x < x2 + 1` is `x <= x2`",
         "H65_decode_and65": "EQUIVALENT: (list[1] >> 26) is below 64, so `& 65` is `& 1`"}
# ---- the Z-OFF TWINS (the coordinator's ruling): each single-layer geometry row and its Z-off twin.  A Z-off polygon draws exactly
# ---- what a Z-on one draws over the cleared frame (only the depth store differs), so for every variant that does not treat Z-off
# ---- geometry differently a twin reds exactly when its Z-on row does -- and for those that do (ZSPECIFIC) the twin rows are
# ---- derived one by one (CLOSURE3.md section 8).
_TW = [("edges_" + k, "zedges_" + k) for k in ("l_in", "l_out", "r_in", "r_out", "rspan")]
_TW += [("yedges_" + k, "zyedges_" + k) for k in ("t_in", "b_in", "b_out", "swap", "s_end", "s_past")]
_TW += [("swap_" + k, "zswap_" + k) for k in ("s_before", "s_tip", "vert", "frac_past")]
_TW += [("edges2_" + k, "zedges2_" + k) for k in ("l_rev", "r_rev", "l_tip")]
_TWT = [("tex" + a, "zt" + b[1:]) for a, b in _TW if a != "swap_frac_past"]   # texturedline has no frac past (EQUIVALENT there)
ZOFF_S = [b for a, b in _TW] + ["zramp_l_end"]             # rows of the simpleline Z-off twin sessions (19)
ZOFF_T = [b for a, b in _TWT] + ["ztramp_l_end"]           # rows of the texturedline ones (18)
_TW += _TWT + [("zleft_tip", "edges2_x2_tip"), ("texzleft_tip", "texedges2_x2_tip")]   # the last two: the Z-ON twin of a Z-off row
TWIN = dict(_TW)
assert len(TWIN) == 37 and len(set(TWIN.values())) == 37, (len(TWIN), len(set(TWIN.values())))
assert len(ZOFF_S) == 19 and len(ZOFF_T) == 18
BLACKWANT = {"zedges_l_out", "zedges_r_out", "zyedges_b_out", "zyedges_s_past", "zswap_s_before", "zswap_frac_past",
             "ztedges_l_out", "ztedges_r_out", "ztyedges_b_out", "ztyedges_s_past", "ztswap_s_before"}
#  zramp / ztramp (two layers: a Z-on COVER at 1.5 stored first, then the Z-off RAMP tested against it), non-Z-specific variants:
ZRAMP_RED = {"As_start_m1", "X1s_simple_start1", "S1s_simple_noswap", "Xs_swap_nox", "Zs_swap_noz", "Rs_swap_nor", "Gs_swap_nog",
             "Bs_swap_nob", "Pms_ztest_zm1"}
ZTRAMP_RED = {"At_start_m1", "X1t_tex_start1", "S1t_tex_noswap", "Xt_swap_nox", "Zt_swap_noz", "Ut_swap_nou", "Vt_swap_nov"}
ZSPECIFIC = {   # variants that treat Z-off geometry differently: their twin rows, derived one by one
    "B1_exit": ZOFF_S + ZOFF_T,                                                    # every Z-off session ends the process
    "M11_decline": [r for r in ZOFF_S + ZOFF_T if r not in BLACKWANT],             # Z-off triangles are not drawn
    "M12_hoist_simple": [r for r in ZOFF_S if r not in BLACKWANT],                 # simpleline draws nothing for Z-off
    "M28_hoist_tex": [r for r in ZOFF_T if r not in BLACKWANT],                    # texturedline draws nothing for Z-off
    "W1s_inner_zw": ["zedges_l_in", "zedges2_l_rev", "zedges2_l_tip"],             # Z-off column 1 lost
    "W1t_inner_zw": ["ztedges_l_in", "ztedges2_l_rev", "ztedges2_l_tip"],
    "W2s_y_zw": ["zyedges_t_in"],                                                  # Z-off row 0 lost
    "W2t_y_zw": ["ztyedges_t_in"],
}
ZSPECIFIC.update({n: [] for n in NEW if n.startswith("V")})                        # listed in full in PNEW
NEWROWS = (["swap_s_before", "swap_s_tip", "swap_vert", "swap_frac_past", "texswap_s_before", "texswap_s_tip", "texswap_vert",
            "ramp_l_end", "texramp_l_end", "edges2_l_rev", "edges2_r_rev", "texedges2_l_rev", "texedges2_r_rev", "zeq_overlap",
            "texzeq_overlap", "maskoff_overlap", "maskhi_overlap", "edges2_l_tip", "texedges2_l_tip", "zleft_tip", "texzleft_tip",
            "edges2_x2_tip", "texedges2_x2_tip"] + ZOFF_S + ZOFF_T)
assert len(NEWROWS) == 60 and len(set(NEWROWS)) == 60
for _v in list(NEWROWS_OLD.values()) + list(PNEW.values()) + list(ZSPECIFIC.values()):
    for _r in _v:
        assert _r in NEWROWS or not _r.startswith(("swap_", "texswap_", "ramp_", "texramp_", "edges2_", "texedges2_", "zeq_",
                                                   "texzeq_", "maskoff_", "maskhi_", "zleft_", "texzleft_", "zedges", "zyedges",
                                                   "zswap", "zramp", "ztedges", "ztyedges", "ztswap", "ztramp")), _r


def twins(n, red):
    """The Z-off twin rows (and zleft/texzleft tip's Z-on twins) variant n reds, given its red set on the other rows."""
    if n in ZSPECIFIC:
        return set(ZSPECIFIC[n])
    out = {TWIN[r] for r in red if r in TWIN}
    if n in ZRAMP_RED:
        out.add("zramp_l_end")
    if n in ZTRAMP_RED:
        out.add("ztramp_l_end")
    return out


def t2scores():
    out = {}
    for line in io.open(os.path.join(UP, "r2_20261105", "table2", "SCORES.txt"), encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.rsplit("RED=", 1)[1].strip()
            out[p[0]] = [] if red == "none" else red.split(",")
    return out


def rowlist(base_out):
    """The 128 row names in the base run's order (spaces as underscores, as PVR_ZWRITE_RED prints them)."""
    names = []
    for line in io.open(base_out, encoding="latin-1"):
        m = re.match(r"^(\S.{0,15}?)\s{2,}\S.*\s(ok|FAIL)$", line.rstrip("\n"))
        if m and not line.startswith("row "):
            names.append(m.group(1).strip().replace(" ", "_"))
    assert len(names) == 128, len(names)
    return names


def predictions(rows):
    t2 = t2scores()
    P = {}
    for n in OLD:
        if n in UB:
            P[n] = None
        else:
            red = set(t2[n]) | set(NEWROWS_OLD.get(n, []))
            P[n] = sorted(red | twins(n, red), key=rows.index)
    for n in NEW:
        red = set(PNEW[n])
        P[n] = sorted(red | twins(n, red), key=rows.index)
    legs = {"base": [],
            "HEAD": sorted(set(t2["HEAD"]) | {"zeq_overlap", "texzeq_overlap", "maskoff_overlap", "zleft_tip", "texzleft_tip"}
                           | set(ZOFF_S + ZOFF_T), key=rows.index),
            "null_true": [r for r in rows if r not in ("id_session", "zon_session", "zoff_session", "ovoff_session", "behind_session",
                                                       "texoff_session", "texbeh_session", "two_session", "sticky_session")],
            "null_absent": list(rows),
            "null_false": [r for r in rows if r != "neg_apparatus"],
            "restored": []}
    for k, v in list(P.items()) + list(legs.items()):
        assert v is None or all(r in rows for r in v), (k, [r for r in v if r not in rows])
    return P, legs


def write():
    out = os.path.join(HERE, "variants")
    os.makedirs(out, exist_ok=True)
    for n in OLD:
        io.open(os.path.join(out, n + ".c"), "w", encoding="latin-1", newline="").write(
            rd(os.path.join(UP, "r2_20261105", "variants", n + ".c")))
    for n, t in NEW.items():
        io.open(os.path.join(out, n + ".c"), "w", encoding="latin-1", newline="").write(t)
    print("%d variants written to %s (%d copied from table 2, %d new)" % (len(OLD) + len(NEW), out, len(OLD), len(NEW)))


def pretable(base_out):
    rows = rowlist(base_out)
    P, legs = predictions(rows)
    npred = sum(1 for v in P.values() if v is not None)
    nred = sum(1 for v in P.values() if v)
    L = ["PRETABLE_3 -- pvrrenderexit, test-variant table 3 (repair 3: the class closure completed, with the Z-off twins; 128 rows).",
         "Written BEFORE table 3 runs: its mtime must precede every RESULT file in table3/ (the frozen probe is copied there first and is",
         "older).  Instrument: table3/probe128_frozen.py, cmp-identical to regress/pvr_zwrite_probe.py when this was written (128/128 on",
         "build/ in base128/).  Baseline: dev_pvr.c.fix3 (== GXEMUL-SEC src/devices/dev_pvr.c == ../det_20261104/dev_pvr.c.fix).",
         "Variants: pvr_variants_3.py.  EVERY prediction is EXACT -- the full red set, none = all 128 green -- except Y2s/Y2t/Y4s/Y4t",
         "(undefined behaviour, NOT PREDICTED, counted in no tally).  Old rows: table 2's MEASURED red set (the 68 rows carry over",
         "unchanged); the 60 new rows: DERIVED (CLOSURE3.md); a Z-off twin reds exactly when its Z-on row does, except under the variants",
         "that treat Z-off geometry differently (B1, M11, M12, M28, W1, W2, V*), whose twin rows are derived one by one.",
         "%d variants: %d predicted, %d predicted red, %d predicted green (EQUIVALENT), 4 NOT PREDICTED." % (len(P), npred, nred, npred - nred),
         "Legs: base 128/128 CONTROL=OK SYMPTOM=ABSENT; HEAD (det_20261104/dev_pvr.c.HEAD, the exit) 60/128 SYMPTOM=PRESENT CONTROL=OK --",
         "table 2's 26 plus every new row whose session carries a Z-off header and so ends the process (42): MEASURED already,",
         "r3_20261105/head128/; null media CONTROL=FAIL: /bin/true 9/128 (only the nine `session` rows, which want exit 0), an absent",
         "binary 0/128, /bin/false 1/128 (`neg apparatus`).",
         "CHANNELS of the 60 new rows (each row's variants and the observable that differs; derivations in CLOSURE3.md):",
         "  swap s before (364,180) BLACK -- A: SWAP row 180 starts at 365.0 after its swap; `x1 - 1` draws 364 red.",
         "  swap s tip (400,249) RED -- B: row 249 arrives 400.5 / 399.5; `x1 > x2 + 1` leaves it reversed: nothing drawn.",
         "  swap vert (300,150) GREEN -- C: VERT row 150 arrives 300.0 / 300.0, start end green (v1), stop end red (v2): `>=` swaps to red.",
         "  swap frac past (151,101) BLACK -- I: FRAC row 101 ends at 150.5; `x < x2 + 1` draws 151.",
         "  texswap s before / s tip / vert -- A / B / C through texturedline (int ends; VERT's start end u 0.5 = the green texel).",
         "  ramp l end (440,60) GREEN -- the swap body: RAMP row 60 arrives 520.0 (v1: z 1.0, magenta) / 440.0 (v2: z 2.0, green); COVER",
         "    (z 1.5, blue, after) fails at 440.  No z exchange: blue.  No r / g / b exchange: 0xffe0 / 0x0000 / 0x07ff.",
         "  texramp l end (440,60) BLUE -- texturedline: v2's (u,v) (0, 0.125) = texel (0,1), stored blue.  No z exchange: COVER's red;",
         "    no u exchange: texel (4,1), never stored, 0x0000; no v exchange: texel (0,0), red.",
         "  edges2 l rev (1,230) RED -- D: LREV row 230 arrives 30.0 / -30.0 (x1 >= 0, x2 < 0); `(x2 < 0 && x2 < 0)` returns early.",
         "  edges2 r rev (639,400) RED -- E and R2: RREV row 400 arrives 700.0 / 639.0; `(x1 >= xsize && x1 >= xsize)` and",
         "    `x2 >= xsize - 1` return early.",
         "  edges2 l tip (1,259) RED -- W3: LREV row 259 arrives 1.0 / -1.0, swapped it draws column 1; `x1 < d->bytes_per_pixel` (2)",
         "    returns early.",
         "  edges2 x2 tip (1,159) RED -- W4: LEFT3 row 159 spans -1.0..1.0, forward; `x2 < d->bytes_per_pixel` returns early.",
         "  texedges2 l rev / r rev / l tip / x2 tip -- the same through texturedline (ints).",
         "  zleft tip, texzleft tip (1,159) RED -- `x2 tip` drawn Z-off (LEFT3 under a Z-off header).",
         "  zeq overlap (220,180) GREEN -- F: a Z-off T2 at z 2.0 over T1's stored 2.0 passes `<=`; F refuses it.  texzeq: textured.",
         "  maskoff overlap (220,180) GREEN -- G: header word 1 0x0c000000; `& 1` disables T1's store, `== 1` does not.",
         "  maskhi overlap (220,180) RED -- H, H9, H17, H33: header word 1 0xf0000000; `& 1` keeps T1's store, `& 5/9/17/33` drop it.",
         "  zedges / zyedges / zswap / zedges2 (18 rows) and ztedges / ztyedges / ztswap / ztedges2 (17) -- the Z-OFF TWINS: each the row",
         "    of the same name without the z drawn by a Z-off polygon, same pixel, same want.  They red under every edit that moves a",
         "    geometry edge for Z-off polygons only -- W1 (`x > d->zwrite_disabled`: zedges l in, zedges2 l rev, l tip), W2 (`y <",
         "    d->zwrite_disabled`: zyedges t in), and the V family (a bound moved by 2 * d->zwrite_disabled) -- and under M11 / M12 / M28",
         "    (Z-off not drawn: every twin that wants a colour) and B1 (every Z-off session ends).",
         "  zramp l end (440,60) GREEN -- the swap body for a Z-off span: COVER (Z-on, z 1.5, blue) FIRST, then RAMP Z-off: v2's z 2.0 passes",
         "    `1.5 <= 2.0` and draws green.  No z exchange: z 1.0 fails, blue; no r / g / b exchange: 0xffe0 / 0x0000 / 0x07ff; `<= z - 1`",
         "    (Pms): 1.5 <= 1.0 fails, blue.  ztramp l end (440,60) BLUE -- textured: no z exchange leaves COVER's red, no u 0x0000, no v red.",
         "",
         "LEGS:"]
    for k, v in legs.items():
        L.append("   %-24s exactly: %s" % (k, ",".join(v) if v else "none"))
    L += ["", "VARIANTS:"]
    for n in OLD + list(NEW):
        v = P[n]
        if v is None:
            L.append("   %-24s NOT PREDICTED (%s)" % (n, WHY_UB[n[:2]]))
        elif not v:
            L.append("   %-24s exactly: none -- GREEN (%s)" % (n, EQUIV.get(n, "no row can see it")))
        else:
            L.append("   %-24s exactly: %s" % (n, ",".join(v)))
    return NL.join(L) + NL


def check(scores_path, base_out):
    """Score a finished table against this script's own predictions (the ones PRETABLE_3.out records)."""
    rows = rowlist(base_out)
    P, legs = predictions(rows)
    got = {}
    for line in io.open(scores_path, encoding="utf-8"):
        p = line.split()
        if len(p) > 1 and "RED=" in line:
            red = line.split("RED=", 1)[1].split()[0]
            got[p[0]] = set() if red == "none" else set(red.split(","))
        elif len(p) > 1 and "BUILD-FAILED" in line:
            got[p[0]] = "BUILD-FAILED"
    hit = miss = npr = 0
    for n, want in list(legs.items()) + [(k, P[k]) for k in OLD + list(NEW)]:
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
        elif g == set(want):
            hit += 1
        else:
            print("PRED=MISS    %s want=%s got=%s" % (n, ",".join(want) or "none", ",".join(sorted(g, key=rows.index)) or "none"))
            miss += 1
    print("TABLE3_CHECK hits=%d misses=%d not_predicted=%d" % (hit, miss, npr))


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        write()
    elif sys.argv[1:2] == ["pretable"] and len(sys.argv) == 3:
        sys.stdout.write(pretable(sys.argv[2]))
    elif sys.argv[1:2] == ["check"] and len(sys.argv) == 4:
        check(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
