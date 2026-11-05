#!/usr/bin/env python3
"""pvr_table5.py -- test-variant TABLE 5 for pvrrenderexit (repair 5: the swap body's statement-deletion closure, the right end from
above, a negative span start; the 146-row probe plus any optional rows), 2026-11-05.

Baseline: dev_pvr.c.fix5 (== GXEMUL-SEC src/devices/dev_pvr.c == ../r4_20261105/dev_pvr.c.fix4, checked).
Variants, each COPIED and checked byte-identical to the file already built from it:
  * table 4's 146 (../r4_20261105/variants/*.c, md5-checked against table 4's MD5.txt);
  * repair 5's 44 (meas140/variants/*.c, pvr_variants_5.py, md5-checked against meas140/MD5.txt): the 17 unbuilt deletion cells, N1s,
    and the 26 compound survivors (B2t is table 4's file; its meas140 copy is identical and is not copied twice).
PREDICTIONS, every one an exact red set:
  * the 140 rows that carry over (unchanged) -- MEASURED: table 4's SCORES.txt for its 146 variants and legs, meas140/SCORES.txt for
    the 44;
  * the repair-5 rows -- DERIVED per variant below (NEW5), each Z-on row and its Z-off twin listed BY NAME (no twin rule).
EXCLUDED and named, not built: the 13 compound forms whose arithmetic turns non-finite before a conversion to int (undefined
behaviour), NONFINITE below.
usage: pvr_table5.py write | pretable <base.out> <frozen probe> <head.log> | check <SCORES.txt> <base.out>"""
import glob
import hashlib
import io
import os
import re
import sys

NL = chr(10)
HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.dirname(HERE)
R4 = os.path.join(UP, "r4_20261105")
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


FIX = rd(os.path.join(HERE, "dev_pvr.c.fix5"))
assert FIX == rd(SEC) and FIX == rd(os.path.join(R4, "dev_pvr.c.fix4")), "dev_pvr.c.fix5 is not the fix"
T4V = {os.path.basename(p)[:-2]: p for p in glob.glob(os.path.join(R4, "variants", "*.c"))}
R5V = {os.path.basename(p)[:-2]: p for p in glob.glob(os.path.join(HERE, "meas140", "variants", "*.c"))}
assert rd(R5V.pop("B2t_start_half")) == rd(T4V["B2t_start_half"])
assert len(T4V) == 146 and len(R5V) == 44 and not set(T4V) & set(R5V), (len(T4V), len(R5V))
_M4, _M5 = md5s(os.path.join(R4, "table4", "MD5.txt")), md5s(os.path.join(HERE, "meas140", "MD5.txt"))
for _n, _p in T4V.items():
    assert _M4.get(_n + ".c") == md5(_p), ("table-4 variant differs from the one table 4 built", _n)
for _n, _p in R5V.items():
    assert _M5.get(_n + ".c") == md5(_p), ("repair-5 variant differs from the one meas140 built", _n)
    assert rd(_p) != FIX, _n

UB = {"Y2s_simple_ltm1", "Y2t_tex_ltm1", "Y4s_simple_gt", "Y4t_tex_gt"}
WHY_UB = {"Y2": "y = -1 admitted: the colour store lands before VRAM and the depth read before vram_z -- undefined behaviour, NOT "
                "PREDICTED (tables 2-4 measured the whole y-edges sessions and their Z-off twins red)",
          "Y4": "y = 480 admitted: the depth read vram_z[307200 + x] is past the frame-exact buffer -- undefined behaviour, NOT "
                "PREDICTED (tables 2-4 measured `b out` and its twin red)"}
NONFINITE = [   # DERIVED (this table's derivation; codex pass 5 counted 13 and did not list them): each divides by an operand that is 0
    #             on a swapped span the probe draws -- 0/0 or x/0 -- and the non-finite value reaches `int ri = r` (simpleline) or
    #             `int texturex = u * texture_xsize` (texturedline) at a drawn pixel
    ("simpleline `r1 = r2` -> `r1 /= r2`", "RAMP row 60: r2 = 0 (green) -> 255/0, column 440 drawn"),
    ("simpleline `tmpf = g1` -> `tmpf /= g1`", "a constant-red span: tmpf = r1 = 255, g1 = 0 -> g2 = inf, the second pixel on"),
    ("simpleline `g1 = g2` -> `g1 /= g2`", "a constant-red span: 0/0"),
    ("simpleline `g2 = tmpf` -> `g2 /= tmpf`", "a constant-red span: 0/0"),
    ("simpleline `tmpf = b1` -> `tmpf /= b1`", "a constant-red span: tmpf = g1 = 0, b1 = 0 -> 0/0"),
    ("simpleline `b1 = b2` -> `b1 /= b2`", "a constant-red span: 0/0"),
    ("simpleline `b2 = tmpf` -> `b2 /= tmpf`", "a constant-red span: 0/0"),
    ("texturedline `tmpf = u1` -> `tmpf /= u1`", "SWAP textured (u = v = 0): tmpf = z1 = 2.0, u1 = 0 -> u2 = inf"),
    ("texturedline `u1 = u2` -> `u1 /= u2`", "SWAP textured: 0/0"),
    ("texturedline `u2 = tmpf` -> `u2 /= tmpf`", "SWAP textured: 0/0"),
    ("texturedline `tmpf = v1` -> `tmpf /= v1`", "SWAP textured: tmpf = u1 = 0, v1 = 0 -> 0/0"),
    ("texturedline `v1 = v2` -> `v1 /= v2`", "SWAP textured: 0/0"),
    ("texturedline `v2 = tmpf` -> `v2 /= tmpf`", "SWAP textured: 0/0")]
assert len(NONFINITE) == 13

RH, ZRH, RHL, ZRHL = "ramp8hi_r_end", "zramp8hi_r_end", "ramp8hi_l_end", "zramp8hi_l_end"
NG, ZNG, TN, ZTN = "negx_n_start", "znegx_n_start", "texnegx_n_start", "ztnegx_n_start"
NEWROWS_ALL = [RH, ZRH, RHL, ZRHL, NG, ZNG, TN, ZTN]
OPTIONAL = {RHL, ZRHL}
NEW5 = {   # derivations: PVR5_NOTE.md, "table 5"
    "B1_exit": [ZRH, ZRHL, ZNG, ZTN],                      # every Z-off session ends the process
    "E1s_simple_ltx2": [NG, ZNG], "E1t_tex_ltx2": [TN, ZTN],   # column 1 is the last column of NEGX's row 60: not drawn
    "M11_decline": [ZNG, ZTN], "M12_hoist_simple": [ZNG], "M28_hoist_tex": [ZTN],   # Z-off NEGX not drawn (zramp8hi: BLUE stays)
    "M13_ztest_bypass_simple": [ZRH, ZRHL], "M26_simple_ztest_del": [ZRH, ZRHL],     # the Z-off RAMP8 draws over the stored 4.0
    "M15_simple_never_store": [ZRH, ZRHL], "M3_simple_inv": [ZRH, ZRHL],            # COVERHI stores no depth: RAMP8 passes
    "M6_assign1": [ZRH, ZRHL], "M7_assign_inv": [ZRH, ZRHL],
    "M19_simple_lo_gt1": [NG, ZNG], "M23_tex_lo_gt1": [TN, ZTN],                    # column 1 not drawn
    "O1s_simple_orleft": [NG, ZNG], "O1t_tex_orleft": [TN, ZTN],                    # x1 = -1 < 0: the row returns
    "W4s_left_x2_bpp": [NG, ZNG], "W4t_left_x2_bpp": [TN, ZTN],                     # x1 < 0 && x2 = 1 < 2: the row returns
    "X1s_simple_start1": [NG, ZNG, RHL, ZRHL],             # -1 + 1 -> 0: 0x7be0 at column 1; COVERHI starts at 441: 440 undrawn
    "X1t_tex_start1": [TN, ZTN],                           # u 0.25 at column 1: texel (2,0), never stored
    "At_start_m1": [TN, ZTN],                              # u 0.75 at column 1: texel (6,0), linear 0x500004, never stored
    "B2s_start_half": [NG, ZNG], "B2t_start_half": [TN, ZTN], "N1s_start_q": [NG, ZNG],   # -1 + c truncates to 0
    "Ps_ztest_zp1": [ZRH],                                 # 4.0 <= 3.0 + 1 passes at 448; 4.0 <= 2.0 + 1 fails at 440
    "W1s_inner_zw": [ZNG], "W1t_inner_zw": [ZTN], "V7t_inner_lo_2zw": [ZTN],       # Z-off column 1 not drawn
    "V2t_left_x2_2zw": [ZTN],                              # Z-off: x1 < 0 && x2 = 1 < 2
    "V5t_start_p2zw": [ZTN],                               # Z-off: starts at 1 with u 0: texel (0,0), red
    "V6s_end_m2zw": [ZNG],                                 # Z-off: ends at -1
    "DTs_z": [RH, ZRH],                                    # z2 = the original x1, 448.0
    "CZs_tadd": [RH, ZRH], "CZs_tmul": [RH, ZRH], "CZs_tdiv": [RH, ZRH],            # z2 = 451, 1344, 149.33
    "CZs_z2add": [RH, ZRH], "CZs_z2mul": [RH, ZRH],                                 # z2 = 5, 6
    "CZs_z1add": [RHL, ZRHL], "CZs_z1mul": [RHL, ZRHL],                             # z1 = 5, 6 at column 440
}
ALLV = sorted(T4V) + sorted(R5V)
assert set(NEW5) <= set(ALLV) and not set(NEW5) & UB, sorted(set(NEW5) - set(ALLV))
#  every deletion cell of the swap body, and every texturedline depth compound, is green on the repair-5 rows except those listed
for _n in ALLV:
    for _r in NEW5.get(_n, []):
        assert _r in NEWROWS_ALL, (_n, _r)

GREEN_WHY = {
    "M17_reset_at_end": "EQUIVALENT (tables 1-4): the one early exit after the reset's old position, the frame-outside-VRAM return "
                        "(dev_pvr.c:1166), comes before every header of its render, and the field is zero there",
    "L1s_simple_lt1left": "EQUIVALENT (table 2): no probed span has both ends in [0, 1), and `x > 0` never draws column 0",
    "L1t_tex_lt1left": "EQUIVALENT (table 2): the same",
    "It_end_lt_p1": "EQUIVALENT: texturedline's span ends are ints, so `x < x2 + 1` is `x <= x2`",
    "H65_decode_and65": "EQUIVALENT: (list[1] >> 26) is below 64, so `& 65` is `& 1`",
    "B1t_swap_half": "EQUIVALENT (pass-5 ruling, section 3): both operands are ints, so `x1 > x2 + 0.5` is `x1 > x2`",
    "B13t_right_x1_half": "EQUIVALENT (pass-5 ruling, section 3): `x1 >= xsize - 0.5` is `x1 >= xsize` for an int x1",
    "B14t_right_x2_half": "EQUIVALENT (pass-5 ruling, section 3): the same for x2",
    "B3s_end_q": "clause-(e) DEBT (rule D2-F): a quarter pixel is below the half pixel `swap frac past` pins; SAMPLED, not claimed",
    "B11s_ztest_q": "clause-(e) DEBT (rule D2-F): the depth compare has no unit; `<= z + c` is sampled at 1.0 and 0.5 only",
    "B12t_ztest_q": "clause-(e) DEBT (rule D2-F): the same in texturedline",
}
DEBT_COMPOUND = "clause-(e) DEBT (pass-5 ruling, section 2): a colour or UV compound-assignment substitution in the swap body"
DEBT_CZT = ("clause-(e) DEBT (pass-5 ruling, section 2): a texturedline depth compound -- the ruling predicted it red on ramp8hi, "
            "but ramp8hi is untextured, and it measured green on the candidate rows (meas_cand/SCORES.txt)")


def scores(path):
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
    names = []
    for line in io.open(base_out, encoding="latin-1"):
        m = re.match(r"^(\S.{0,15}?)\s{2,}\S.*\s(ok|FAIL)$", line.rstrip("\n"))
        if m and not line.startswith("row "):
            names.append(m.group(1).strip().replace(" ", "_"))
    assert len(set(names)) == len(names)
    new = [r for r in NEWROWS_ALL if r in names]
    assert set(NEWROWS_ALL) - OPTIONAL <= set(new) and len(names) == 140 + len(new), (len(names), new)
    return names, new


SESSION_ROWS = ("id_session", "zon_session", "zoff_session", "ovoff_session", "behind_session", "texoff_session", "texbeh_session",
                "two_session", "sticky_session")


def predictions(rows, new):
    t4 = scores(os.path.join(R4, "table4", "SCORES.txt"))
    m5 = scores(os.path.join(HERE, "meas140", "SCORES.txt"))
    old = [r for r in rows if r not in new]
    assert len(old) == 140
    P = {}
    for n in ALLV:
        if n in UB:
            P[n] = None
            continue
        carried = t4[n] if n in T4V else m5[n]
        assert isinstance(carried, list) and all(r in old for r in carried), (n, carried)
        P[n] = sorted(set(carried) | {r for r in NEW5.get(n, []) if r in new}, key=rows.index)
    zoffnew = [r for r in (ZRH, ZRHL, ZNG, ZTN) if r in new]
    legs = {"base": [],
            "HEAD": sorted(set(t4["HEAD"]) | set(zoffnew), key=rows.index),
            "null_true": [r for r in rows if r not in SESSION_ROWS],
            "null_absent": list(rows),
            "null_false": [r for r in rows if r != "neg_apparatus"],
            "restored": []}
    return P, legs


def write():
    out = os.path.join(HERE, "variants")
    os.makedirs(out, exist_ok=True)
    for n, p in list(T4V.items()) + list(R5V.items()):
        io.open(os.path.join(out, n + ".c"), "w", encoding="latin-1", newline="").write(rd(p))
    print("%d variants written to %s (%d from table 4, %d from meas140)" % (len(T4V) + len(R5V), out, len(T4V), len(R5V)))


def green_why(n):
    if n in GREEN_WHY:
        return GREEN_WHY[n]
    if n.startswith("CZt_"):
        return DEBT_CZT
    if n.startswith("C"):
        return DEBT_COMPOUND
    raise KeyError(n)


def pretable(base_out, frozen, head_log, channels):
    rows, new = rowlist(base_out)
    P, legs = predictions(rows, new)
    head = set(io.open(head_log, encoding="utf-8").read().split("HEAD PVR_ZWRITE_RED=")[1].split()[0].split(","))
    assert head == set(legs["HEAD"]), "the HEAD prediction is not the measured pre-fix leg"
    npred = sum(1 for v in P.values() if v is not None)
    nred = sum(1 for v in P.values() if v)
    green = sorted(n for n, v in P.items() if v == [])
    for n in green:
        green_why(n)
    L = ["PRETABLE_5 -- pvrrenderexit, test-variant table 5 (repair 5: the swap body's statement-deletion closure, the right end from",
         "above, a negative span start; %d rows)." % len(rows),
         "Written BEFORE table 5 runs: its mtime must precede every RESULT file in table5/ (the frozen probe is copied there first and is",
         "older).  INSTRUMENT: table5/probe%d_frozen.py, cmp-identical to regress/pvr_zwrite_probe.py when this was written." % len(rows),
         "INSTRUMENT_MD5 %s table5/probe%d_frozen.py" % (md5(frozen), len(rows)),
         "Baseline: dev_pvr.c.fix5 (== GXEMUL-SEC src/devices/dev_pvr.c).  Variants: pvr_table5.py -- table 4's 146 and repair 5's 44 (the",
         "17 deletion cells not built before, N1s, the 26 compound survivors).",
         "EVERY prediction is EXACT -- the full red set, none = all %d green -- except Y2s/Y2t/Y4s/Y4t (undefined behaviour, NOT" % len(rows),
         "PREDICTED, counted in no tally).  The 140 rows that carry over: the red set MEASURED by table 4 (../r4_20261105/table4/SCORES.txt)",
         "and, for the 44, by step 1 on the shipped 140-row probe (meas140/SCORES.txt).  The repair-5 rows -- %d of them, the two" % len(new),
         "optional left-end rows included (kept on a measured delta, meas_cand/SCORES.txt) -- DERIVED per variant (pvr_table5.py NEW5),",
         "each Z-on row and Z-off twin listed BY NAME: %s." % ", ".join(new),
         "Of the eleven depth compounds the ruling predicted red, SEVEN are predicted red here (simpleline's) and texturedline's FOUR green.",
         "%d variants: %d predicted, %d predicted red, %d predicted green, 4 NOT PREDICTED." % (len(P), npred, nred, npred - nred),
         "Legs: base %d/%d; HEAD (det_20261104/dev_pvr.c.HEAD) %d/%d SYMPTOM=PRESENT -- MEASURED already, its red set is the one below;"
         % (len(rows), len(rows), len(rows) - len(legs["HEAD"]), len(rows)),
         "null media CONTROL=FAIL: /bin/true 9/%d, an absent binary 0/%d, /bin/false 1/%d." % (len(rows), len(rows), len(rows)),
         "EXCLUDED and named (not built; undefined behaviour, DERIVED -- codex pass 5 counted 13 such forms and did not list them):"]
    L += ["   %-44s %s" % (a, b) for a, b in NONFINITE]
    L += [""] + channels.rstrip(NL).split(NL) + ["", "LEGS:"]
    for k, v in legs.items():
        L.append("   %-24s exactly: %s" % (k, ",".join(v) if v else "none"))
    L += ["", "VARIANTS:"]
    for n in ALLV:
        v = P[n]
        if v is None:
            L.append("   %-24s NOT PREDICTED (%s)" % (n, WHY_UB[n[:2]]))
        elif not v:
            L.append("   %-24s exactly: none -- GREEN (%s)" % (n, green_why(n)))
        else:
            L.append("   %-24s exactly: %s" % (n, ",".join(v)))
    return NL.join(L) + NL


def check(scores_path, base_out):
    rows, new = rowlist(base_out)
    P, legs = predictions(rows, new)
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
        elif set(g) == set(want):
            hit += 1
        else:
            print("PRED=MISS    %s want=%s got=%s" % (n, ",".join(want) or "none", ",".join(sorted(g, key=rows.index)) or "none"))
            miss += 1
    print("TABLE5_CHECK hits=%d misses=%d not_predicted=%d" % (hit, miss, npr))


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        write()
    elif sys.argv[1:2] == ["pretable"] and len(sys.argv) == 5:
        sys.stdout.write(pretable(sys.argv[2], sys.argv[3], sys.argv[4], rd(os.path.join(HERE, "CHANNELS5.txt"))))
    elif sys.argv[1:2] == ["check"] and len(sys.argv) == 4:
        check(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
