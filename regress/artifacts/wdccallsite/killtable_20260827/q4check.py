"""Settle #480's Q4 and Q2 by MEASUREMENT, not by argument.

Two seats refuted the round's Q4 reasoning by DIFFERENT routes, so both get built:

  D1_renumber   (kimi-k3:cloud)  delete the sole-carrier row's call AND renumber the
                identity pin 83 -> 82 in the same edit.  "rows == 82", zero failures.
  D2_rowsplusplus (codex)        replace the call with `rows++;` -- no renumber needed
                at all.  Sharper: `rows == 83` still holds, the pass token still
                prints, and the sole M4 carrier is gone.

If either produces a GREEN detector, the round's claim that "the delta was checked and
is zero" is FALSE and naming the rows in gate_offline.sh has a measured warrant.

  E1_pkt        (kimi-k3:cloud)  `if (idata != ATAPI_PKT_CMD)` in front of the helper
                call -- a PRODUCT mutant, proposed as the smallest edit that re-opens
                #479's residue class and still passes all 83 rows.

NOTE THE ASYMMETRY, which is the point kimi made about this round: D1/D2 mutate the
DETECTOR, E1 mutates the PRODUCT.  This round had only ever done the second kind.
"""
import io, os, shutil

S = r"C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC"
O = (r"C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-CC-GXEMUL"
     r"\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\q4")

NL, T = chr(10), chr(9)
det = io.open(os.path.join(S, "regress", "diff_wdc_identify.c"),
              encoding="utf-8", newline="").read()
prod = io.open(os.path.join(S, "src", "devices", "dev_wdc.c"),
               encoding="utf-8", newline="").read()

CALLROW = T + "row_rejected_cmd_resets();" + NL
assert det.count(CALLROW) == 1, "row call %d" % det.count(CALLROW)


def d1(d):
    d = d.replace(CALLROW, "", 1)
    for a, b in [("if (rows != 83) {", "if (rows != 82) {"),
                 ("rows = %i, want 83", "rows = %i, want 82")]:
        assert d.count(a) == 1, "%r %d" % (a, d.count(a))
        d = d.replace(a, b, 1)
    return d


def d2(d):
    return d.replace(CALLROW, T + "rows ++;" + NL, 1)


CALL = T + "wdc_new_command_reset(d);" + NL


def e1(p):
    assert p.count(CALL) == 1, "helper call %d" % p.count(CALL)
    return p.replace(CALL, T + "if (idata != ATAPI_PKT_CMD)" + NL + T + CALL, 1)


CASES = {"D1_renumber": (d1, None), "D2_rowsplusplus": (d2, None),
         "E1_pkt": (None, e1)}

if os.path.isdir(O):
    shutil.rmtree(O)
for name, (df, pf) in CASES.items():
    t = os.path.join(O, name)
    os.makedirs(os.path.join(t, "regress"))
    os.makedirs(os.path.join(t, "src", "devices"))
    nd = df(det) if df else det
    npd = pf(prod) if pf else prod
    assert (nd != det) or (npd != prod), "MUTANT %s CHANGED NOTHING" % name
    io.open(os.path.join(t, "regress", "diff_wdc_identify.c"),
            "w", encoding="utf-8", newline="").write(nd)
    io.open(os.path.join(t, "src", "devices", "dev_wdc.c"),
            "w", encoding="utf-8", newline="").write(npd)
    print("  built", name)
