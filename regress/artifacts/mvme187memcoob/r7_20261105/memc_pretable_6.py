#!/usr/bin/env python3
"""memc_pretable_6.py -- PRETABLE_6 and PRED_MAP_6 for mvme187memcoob repair 6 (session R18; regress_20261105/REG_MYTHOS_local.md
section 2(d), regress_20261105/DISPOSITION.md), 2026-11-05.
  memc_pretable_6.py vars | pretable | predmap
vars: the variants table 6 runs -- the eight own-latch variants first, then the other 657 of table 5's 665 green representatives
(r5_20261105/table5/SCORES.txt lines scoring 206/206, base excluded), each once.  pretable: PRETABLE_6.out.  predmap: PRED_MAP_6.txt
(name TAB EXACT TAB comma-joined red rows), the driver's comparison input.
Predictions are the frozen 213-row probe's own verdicts (table6/probe213_frozen.py) on memc_variants_5.py's device model (class
Device and the fake gxemul, used read-only: r5_20261105/memc_variants_5.py is not modified).  B3 (the indexed read) is not a
statement the model expresses; its prediction is table 5's measured set, carried, with the reason given in the output.
"""
import hashlib
import importlib.util
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.dirname(HERE)
NL = chr(10)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mv5 = load("mv5", os.path.join(MD, "r5_20261105", "memc_variants_5.py"))
P213 = os.path.join(HERE, "table6", "probe213_frozen.py")
P206 = os.path.join(MD, "r5_20261105", "table5", "probe206_frozen.py")
SCORES5 = os.path.join(MD, "r5_20261105", "table5", "SCORES.txt")
PRETABLE5 = os.path.join(MD, "r5_20261105", "PRETABLE_5.out")
EIGHT = ["L_MB_M_xori_any", "L_ME_M_xori_any", "L_DB_D_xori_any", "L_DA_D_xori_any", "L_MT_M_xori_M", "L_MW_M_xori_M",
         "L_DT_D_xori_D", "L_DT_D_idat_W.D"]
LEGS = [("base", {}), ("HEAD", {"head": True}), ("null_true", {"media": "true"}), ("null_absent", {"media": "absent"}),
        ("null_false", {"media": "false"}), ("B1_cnf_exit", {"exit_mw": True}), ("B2_def_exit", {"exit_def": True})]
B3 = "B3_idx_read"


def scores5():
    """table 5's measured lines: name -> (score, red list).  Anchored on ' RED=': a bare 'RED=' also matches inside 'PRED='
    (the first version of this parser read every measured set as ['match'] -- caught by the calibration below)."""
    out = {}
    for line in io.open(SCORES5, encoding="utf-8"):
        p = line.split()
        m = re.search(r" RED=(\S+)", line)
        if len(p) > 3 and m:
            red = m.group(1)
            out[p[0]] = (p[3], [] if red == "none" else red.split(","))
    return out


def kinds5():
    """PRETABLE_5's class for each green representative: NOCHANGE / UNFIRED / UNOBSERVED."""
    out = {}
    for line in io.open(PRETABLE5, encoding="utf-8"):
        if "exact: none -- " in line:
            p = line.split()
            out[p[0]] = line.rsplit("-- ", 1)[1].strip()
    return out


def green665():
    s5 = scores5()
    names = [n for n, (sc, _) in s5.items() if sc == "206/206" and n != "base"]
    assert len(names) == 665, len(names)
    assert all(e in names for e in EIGHT)
    return names


def vars6():
    g = green665()
    return EIGHT + [n for n in g if n not in EIGHT]


def predict(variant, probe=P213):
    red, ctl, sym, nrows, got = mv5.predict(variant, probe)
    return red, ctl, sym, nrows, got


def var_of(name):
    return {"cell": mv5.cell_from_name(name)}


HAND = {
    "L_MB_M_xori_any": ["MB runs only when the memconf notice fires.  1st 0x01: announce, M = 1, M ^= 1 -> 0.  2nd 0x01: M == 0,",
                        "announce, M = 1 -> 0.  3rd 0x00: announce, M = 1, M ^= 0 -> 1.  Memconf notices 3, default 1: lines 4."],
    "L_ME_M_xori_any": ["ME runs on every memconf access.  1st 0x01: announce, M = 1, ME -> 0.  2nd 0x01: announce, M = 1 -> 0.",
                        "3rd 0x00: announce, M = 1, ^ 0 -> 1.  Load: ^ 0.  Memconf notices 3, default 1: lines 4."],
    "L_DB_D_xori_any": ["DB runs only when the default notice fires.  1st 0x01: announce, D = 1, D ^= 1 -> 0.  2nd 0x01: announce,",
                        "D = 1 -> 0.  3rd 0x00: announce, D = 1, ^ 0 -> 1.  Load: D == 1, silent.  Default 3, memconf 1: lines 4."],
    "L_DA_D_xori_any": ["DA runs on every default access.  1st 0x01: announce, D = 1, DA -> 0.  2nd 0x01: announce, D = 1 -> 0.",
                        "3rd 0x00: announce, D = 1, ^ 0 -> 1.  Load: silent, ^ 0.  Default 3, memconf 1: lines 4."],
    "L_MT_M_xori_M": ["MT runs on every memconf access before the write block, gated on M.  1st 0x01: M == 0, no toggle; announce,",
                      "M = 1.  2nd 0x01: M ^= 1 -> 0, then announce, M = 1.  3rd 0x00: M ^= 0 -> 1, silent.  Load: ^ 0.  Lines 3."],
    "L_MW_M_xori_M": ["MW runs on every memconf store before the latch test, gated on M.  1st 0x01: no toggle; announce, M = 1.",
                      "2nd 0x01: M -> 0, announce, M = 1.  3rd 0x00: M ^= 0 -> 1, silent.  Lines 3."],
    "L_DT_D_xori_D": ["DT runs on every default access before the latch test, gated on D.  1st 0x01: no toggle; announce, D = 1.",
                      "2nd 0x01: D -> 0, announce, D = 1.  3rd 0x00: D ^= 0 -> 1, silent.  Load: ^ 0, silent.  Lines 3."],
    "L_DT_D_idat_W.D": ["DT, gated on a store with D set.  1st 0x01: D == 0, no assign; announce, D = 1.  2nd 0x01: D = 1.",
                        "3rd 0x00: D = 0, then announce (': 0x0'), D = 1.  Load: not a store, silent.  Lines 3."],
}


def calibration():
    """The model on table 5's frozen 206-row instrument against table 5's MEASURED red sets (legs, B1, B2 and the 665)."""
    s5 = scores5()
    lines = []
    bad = 0
    for n, v in LEGS:
        red = predict(v, P206)[0]
        ok = sorted(red) == sorted(s5[n][1])
        bad += 0 if ok else 1
        lines.append("   %-18s %s" % (n, "MATCH" if ok else "MISMATCH model=%s measured=%s" % (red, s5[n][1])))
    g = green665()
    nmis = 0
    for n in g:
        red = predict(var_of(n), P206)[0]
        if red:
            nmis += 1
            lines.append("   %-34s MISMATCH model=%s measured=none" % (n, ",".join(red)))
    bad += nmis
    lines.append("   the 665 green representatives: %d of 665 modelled green on the 206 rows (measured: 665 green)" % (665 - nmis))
    return bad, lines


def predmap_lines():
    out = []
    s5 = scores5()
    for n, v in LEGS:
        out.append("%s\tEXACT\t%s" % (n, ",".join(predict(v)[0]) or "none"))
    out.append("%s\tEXACT\t%s" % (B3, ",".join(s5[B3][1]) or "none"))
    for n in vars6():
        out.append("%s\tEXACT\t%s" % (n, ",".join(predict(var_of(n))[0]) or "none"))
    return out


def pretable():
    s5 = scores5()
    k5 = kinds5()
    nrows = predict({})[3]
    out = []
    a = out.append
    a("PRETABLE_6 -- mvme187memcoob detector, test-variant table 6 (repair 6: session R18, %d rows).  Written BEFORE table 6 runs" % nrows)
    a("(this file's mtime precedes table6/SCORES.txt).  Instrument: table6/probe213_frozen.py, copied from regress/mvme187_memc_probe.py")
    a("after the R18 edit (md5 %s); base on the clone's restored baseline binary 213/213," %
      hashlib.md5(io.open(P213, "rb").read()).hexdigest())
    a("r7_20261105/base213/probe_base213.out.  Baseline: GXEMUL-SEC/src/devices/dev_mvme187.c (repair 6 changes the probe, not the")
    a("device).  STEP 1 (before any probe edit): the eight own-latch variants measured 206/206 on the 206-row probe in a fresh clone,")
    a("base 206/206 (r7_20261105/step1/SCORES.txt, step1/FRESHNESS.txt).  Legs first, in one fresh clone: base, HEAD")
    a("(det_20261104/dev_mvme187.c.HEAD), three null media, B1-B3; then the eight; then the other 657 of table 5's 665 green")
    a("representatives (`memc_variants_5.py apply`).")
    a("")
    a("METHOD.  Every `exact` prediction is the frozen 213-row probe's own verdict on memc_variants_5.py's device model (class Device,")
    a("the fake gxemul: the probe's m88k words run against DEVICE_ACCESS(mvme187_memc) as written in the fix, with the variant's")
    a("statement inserted).  The eight are also walked by hand below.  B3 is not a statement the model expresses: its prediction")
    a("is table 5's measured set, carried (reason under LEGS).")
    a("")
    bad, cal = calibration()
    a("CALIBRATION (the model on table 5's frozen 206-row instrument against table 5's MEASURED SCORES.txt): %d mismatches" % bad)
    out.extend(cal)
    a("")
    a("THE FOUR CHECKS for R18's seven rows (mandatory: repair 6 extends a kill-table-backed detector):")
    a("  SIBLING PARITY -- R18 is one session with two arms, default (+0x18) then memconf (+0x08), each given the same three stores")
    a("    (0x01, 0x01, 0x00) and one load; each arm has a notice row naming the first value, a readback row, and shares lines/pc.")
    a("  CLAIM -> ROW -- 'one announce per category' -> R18 lines; 'the first store of each category is announced with its value' ->")
    a("    R18 def line, R18 cnf line; 'memconf keeps no store' -> R18 08 r4 (3 after 0x01, 0x01, 0x00); 'the accesses retire' ->")
    a("    R18 pc; 'the session survives' -> R18 session.  R18 18 r2 reads 0 after the default stores, but its last store is 0x00,")
    a("    so it is not a keep detector for the default arm (R5's and R10's readbacks carry that claim).")
    a("  GUARD FIELD vs BODY FIELD -- the memconf guard reads writeflag and warned_memconf (dev_mvme187.c:105, :112); its body reads")
    a("    idata and controller and sets warned_memconf (:113-116).  The default guard reads warned_default (:127); its body reads")
    a("    writeflag, relative_addr, controller and idata and sets warned_default (:128-135).  The eight write the guard's own field")
    a("    from the arm that reads it.  `^= idata` takes a latch of 1 to zero only on idata 0x01; `= idata` takes it to zero on")
    a("    0x00.  The 206 rows make no store of 0x01 in any arm and no non-first default store of 0x00 (step 1 measured the eight")
    a("    green there); R18 makes 0x01 stores (first and second) and a non-first 0x00 store in both arms.")
    a("  CHANNEL (row: the variant it is built to kill -> the observable that differs):")
    a("    R18 lines    -- each of the eight -> the announce count (4 for the four ungated toggles, 3 for the other four).")
    a("    R18 def line -- the default notice's value guard or direction gated off for this store -> the fragment")
    a("                    'unimplemented write to offset 0x18 (controller 0): 0x1 (once) ]' is absent.")
    a("    R18 cnf line -- the memconf notice gated off for 0x01 -> 'memconf write 0x1 (controller 0) ignored, not modelled (once) ]'")
    a("                    is absent.")
    a("    R18 18 r2    -- an exit at any R18 access (HEAD, B1, B2) -> no register dump, r2 reads 'none'.")
    a("    R18 08 r4    -- a memconf keep that one of R18's three memconf stores changes -> memconf reads other than 0x3.")
    a("    R18 pc       -- an exit (no register dump: 'none') or a fault at any of the eight accesses -> pc is not CODE + 32.")
    a("    R18 session  -- an exit (HEAD, B1, B2) -> exit1.")
    a("")
    a("THE EIGHT (step 1: each 206/206 on the 206 rows).  Predicted red on %d rows -- the model's exact set, then the hand walk:" % nrows)
    for n in EIGHT:
        red, ctl, sym, _, got = predict(var_of(n))
        a("   %-18s exact: %s   (R18 lines: %s)" % (n, ",".join(red) or "none (GREEN)", got.get("R18 lines")))
        for h in HAND[n]:
            a("   %-18s   %s" % ("", h))
    a("")
    a("LEGS (exact; %d rows):" % nrows)
    for n, v in LEGS:
        red, ctl, sym, _, _ = predict(v)
        a("   %-18s %3d/%d  CONTROL=%s SYMPTOM=%s  red: %s" % (n, nrows - len(red), nrows, "OK" if ctl else "FAIL",
                                                           "PRESENT" if sym else "ABSENT", ",".join(red) or "none"))
    b3 = s5[B3][1]
    a("   %-18s %3d/%d  CONTROL=OK SYMPTOM=ABSENT  red: %s" % (B3, nrows - len(b3), nrows, ",".join(b3)))
    a("   %-18s   (table 5's measured set, SCORES.txt:8, carried.  B3 changes only what a default-arm READ returns: the struct byte" % "")
    a("   %-18s   at the folded offset.  R18's one default read is at +0x18, memcreg's memc_control byte, which DEVINIT's memset" % "")
    a("   %-18s   leaves 0 and no arm writes; its memconf read is served.  So R18 adds no B3 row: predicted exactly the four.)" % "")
    a("")
    preds = [(n, predict(var_of(n))[0]) for n in vars6()]
    turned = [(n, r) for n, r in preds if r]
    stay = [n for n, r in preds if not r]
    a("TABLE 5's 665 GREEN REPRESENTATIVES on %d rows (the eight included): predicted RED %d, predicted GREEN %d." %
      (nrows, len(turned), len(stay)))
    a("PREDICTED RED (name, PRETABLE_5 class, exact red set):")
    for n, r in turned:
        a("   %-34s %-10s exact: %s" % (n, k5.get(n, "?"), ",".join(r)))
    a("PREDICTED GREEN (name, PRETABLE_5 class):")
    for n in stay:
        a("   %-34s %-10s exact: none" % (n, k5.get(n, "?")))
    by = {}
    for n, r in turned:
        by[k5.get(n, "?")] = by.get(k5.get(n, "?"), 0) + 1
    byg = {}
    for n in stay:
        byg[k5.get(n, "?")] = byg.get(k5.get(n, "?"), 0) + 1
    a("")
    a("SUMMARY: of the 665, predicted red by class %s; predicted green by class %s." %
      (", ".join("%s %d" % kv for kv in sorted(by.items())), ", ".join("%s %d" % kv for kv in sorted(byg.items()))))
    a("A miss is any measured red set that differs from its exact prediction; every miss is reported before any conclusion.")
    return NL.join(out) + NL


def main():
    a = sys.argv[1:]
    if a == ["vars"]:
        print(" ".join(vars6()))
    elif a == ["pretable"]:
        sys.stdout.write(pretable())
    elif a == ["predmap"]:
        sys.stdout.write(NL.join(predmap_lines()) + NL)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
