#!/usr/bin/env python3
"""cmp_table568.py -- writes KILLTABLE1_VS_PRETABLE.out for #568 kill table 1 from legs/*.raw.

usage: python3 -I -B cmp_table568.py <killtable1 dir> <probe dir (run2_HEAD.out / run2_NULL.out)>

PRED transcribes PRETABLE_ADDENDUM_v2.out section 4 VERBATIM (the text) and parses it into a row set by ONE stated
rule: `a/b' expands to the named rows; a second-pass row (`p2 ann rd 2', `p2 ann wr 2') is predicted ONLY where the
text names it (M_LATCHNOSET names them, M_DROPMCTL says "+ their 2nd passes"), so "p2 ann rd/wr" is the two FIRST-pass
rows.  HEAD and NULL are predicted by their earlier measured runs (run2_HEAD.out / run2_NULL.out: same probe md5).
SEAT transcribes SEAT_PREDICTIONS_prerun.txt (written before any build).  Every red set is read from the probe's own
VME_DEFAULT_RED line and cross-checked against the per-row ok/FAIL column; a raw without its completion line is refused.
"""
import io
import os
import re
import sys

KT, PD = sys.argv[1], sys.argv[2]
LEGS_DIR = os.path.join(KT, "legs")

P1_10 = {"p1 fault lo", "p1 fault hi", "p1 fault mid", "p1 fault wr", "p1 census", "p1 widths", "p1 p2 edge",
         "p3 interim", "p2 int byte", "p2 int half"}
ANN4 = {"p2 ann rd", "p2 ann wr", "p2 ann rd 2", "p2 ann wr 2"}

#  (addendum section 4 text, predicted red set | "BUILD_FAILS")
PRED = {
    "M_EXIT": ("p1 fault lo/hi/mid/wr, p1 census, p1 widths, p1 p2 edge, p3 interim, p2 int byte/half die", P1_10),
    "M_DROPMCTL": ("p2 rd census, p2 wr census, p2 ann rd, p2 ann wr (+ their 2nd passes not completed)",
                   {"p2 rd census", "p2 wr census"} | ANN4),
    "M_DROPMISC": ("p2 rd census, p2 wr census, p2 ann rd/wr, p1 p2 edge",
                   {"p2 rd census", "p2 wr census", "p2 ann rd", "p2 ann wr", "p1 p2 edge"}),
    "M_ADD94": ("p1 census (987/988), p1 fault mid", {"p1 census", "p1 fault mid"}),
    "M_LATCHONE": ("p2 ann rd, p2 ann wr (1 line each)", {"p2 ann rd", "p2 ann wr"}),
    "M_LATCHNOSET": ("p2 ann rd, p2 ann wr (52 lines), p2 ann rd 2, p2 ann wr 2", ANN4),
    "M_LATCHRDSET": ("p2 ann wr (each write-first register re-announces on its read)", {"p2 ann wr"}),
    "M_LATCHCLRW": ("p2 ann rd (each read-first register re-announces on its write)", {"p2 ann rd"}),
    "M_LATCHCLRW_POST": ("[variant: inherits M_LATCHCLRW's] p2 ann rd (each read-first register re-announces on its write)",
                         {"p2 ann rd"}),
    "M_WDEBUG": ("p2 ann wr, p2 nw wr", {"p2 ann wr", "p2 nw wr"}),
    "M_RDEBUG": ("p2 ann rd, p2 nw rd", {"p2 ann rd", "p2 nw rd"}),
    "M_ANNLEN4": ("p2 nw rd, p2 nw wr", {"p2 nw rd", "p2 nw wr"}),
    "M_TRUNC": ("p2 nw wr", {"p2 nw wr"}),
    "M_WRFAULT": ("p2 wr census, p2 st widths, p2 ann wr, p2 nw wr", {"p2 wr census", "p2 st widths", "p2 ann wr", "p2 nw wr"}),
    "M_LENFAULT": ("p2 ld widths, p2 st widths, p2 nw rd, p2 nw wr", {"p2 ld widths", "p2 st widths", "p2 nw rd", "p2 nw wr"}),
    "M_STORE": ("p2 wr census", {"p2 wr census"}),
    "M_FLTBREAK": ("p1 fault lo/hi/mid/wr, p1 census, p1 widths, p1 p2 edge, p3 interim, p2 int byte/half", P1_10),
    "M_FLTLEN": ("p1 widths, p3 interim, p2 int byte, p2 int half", {"p1 widths", "p3 interim", "p2 int byte", "p2 int half"}),
    "M_FLTWR": ("p1 fault wr, p1 widths", {"p1 fault wr", "p1 widths"}),
    "M_NOONCE": ("p2 ann rd (tail literal)", {"p2 ann rd"}),
    "M_DROPTCTL": ("cased census, tctl rt", {"cased census", "tctl rt"}),
    "M_CAPNARROW": ("BUILD FAILS (the typedef) -- killed by construction", "BUILD_FAILS"),
    "M_ODATA0": ("predicted SURVIVOR (equivalent today)", set()),
    "M_SERVED0": ("predicted SURVIVOR (equivalent today -- section 2 (i))", set()),
}
ORDER = ["M_EXIT", "M_DROPMCTL", "M_DROPMISC", "M_ADD94", "M_LATCHONE", "M_LATCHNOSET", "M_LATCHRDSET", "M_LATCHCLRW",
         "M_LATCHCLRW_POST", "M_WDEBUG", "M_RDEBUG", "M_ANNLEN4", "M_TRUNC", "M_WRFAULT", "M_LENFAULT", "M_STORE",
         "M_ODATA0", "M_SERVED0", "M_FLTBREAK", "M_FLTLEN", "M_FLTWR", "M_NOONCE", "M_DROPTCTL", "M_CAPNARROW"]
assert sorted(ORDER) == sorted(PRED)

SEAT = {
    "M_EXIT": P1_10,
    "M_DROPMCTL": {"p2 rd census", "p2 wr census", "p2 ld widths", "p2 st widths"} | ANN4,
    "M_DROPMISC": {"p2 rd census", "p2 wr census", "p1 p2 edge"} | ANN4,
    "M_ADD94": {"p1 census", "p1 fault mid"},
    "M_LATCHONE": {"p2 ann rd", "p2 ann wr", "p2 nw rd", "p2 nw wr"},
    "M_LATCHNOSET": ANN4,
    "M_LATCHRDSET": {"p2 ann wr"},
    "M_LATCHCLRW": {"p2 ann rd", "p2 ann rd 2", "p2 ann wr 2"},
    "M_LATCHCLRW_POST": {"p2 ann wr", "p2 ann rd 2", "p2 ann wr 2"},
    "M_WDEBUG": {"p2 ann wr", "p2 ann wr 2", "p2 nw wr"},
    "M_RDEBUG": {"p2 ann rd", "p2 ann rd 2", "p2 nw rd"},
    "M_ANNLEN4": {"p2 nw rd", "p2 nw wr"},
    "M_TRUNC": {"p2 nw wr"},
    "M_WRFAULT": {"p2 wr census", "p2 st widths", "p2 nw rd", "p2 nw wr"} | ANN4,
    "M_LENFAULT": {"p2 ld widths", "p2 st widths", "p2 nw rd", "p2 nw wr"},
    "M_STORE": {"p2 wr census", "p2 st widths"},
    "M_ODATA0": set(),
    "M_SERVED0": set(),
    "M_FLTBREAK": P1_10,
    "M_FLTLEN": {"p1 widths", "p3 interim", "p2 int byte", "p2 int half"},
    "M_FLTWR": {"p1 fault wr", "p1 widths"},
    "M_NOONCE": {"p2 ann rd", "p2 nw rd"},
    "M_DROPTCTL": {"cased census", "tctl rt", "vbr rt", "t1count inc"},
    "M_CAPNARROW": "BUILD_FAILS",
}

#  Why each MISS happened -- written from reading each leg's diff and the frozen probe, then checked against the
#  measured got-values printed beside it.  cause: EDIT (mis-built / mistranslated), TARGET (equivalent code), ROW
#  (cannot see it), or PREDICTION (none of the three: the leg is built as described, it was killed, and the extra red
#  rows CAN see it -- the PRETABLE row list for the leg omitted them).
NOTES = {
    "M_DROPMCTL": ("PREDICTION", "p2 ld widths / p2 st widths access 0x28 itself with ld.bu+ld.hu / st.b+st.h; the switch "
                   "keys on relative_addr, not len, so `case VME2_MASTERCTL' declines those today and, dropped, they reach "
                   "default: and FAULT (0/4 pc=0x18, 0/3 pc=0x18)."),
    "M_DROPMISC": ("PREDICTION", "p2 ann rd 2 / p2 ann wr 2 read \"pass 1 not completed\" whenever pass 1 stops on a fault "
                   "(here at 0x8c, after 25 lines) -- the mechanical consequence the addendum names for M_DROPMCTL "
                   "(\"+ their 2nd passes not completed\") and omits for this leg."),
    "M_LATCHONE": ("PREDICTION", "the nonword session's six FIRST accesses also share the one latch: only its first "
                   "access (ld.bu 0x04) announces, so p2 nw rd = 1/1 and p2 nw wr = 0/0."),
    "M_LATCHCLRW": ("PREDICTION", "built as the addendum describes it (a write clears its bit BEFORE the check, so a "
                    "read-first register re-announces on its write: p2 ann rd 52/26/26 as predicted); every later write "
                    "re-announces too, so both second passes print 26 lines (p2 ann rd 2 = 26, p2 ann wr 2 = 26)."),
    "M_LATCHCLRW_POST": ("EDIT (translation, not a defect)", "the VARIANT: PRETABLE.out section 5 says \"the write clears; "
                         "later reads\", i.e. the clear AFTER the check.  Then the predicted row p2 ann rd stays GREEN "
                         "(26/26/26: the read announces before the write clears it) and the rows that see it are p2 ann wr "
                         "(52/26/26: each write-first register re-announces on its read) and both second passes (26 each).  "
                         "The prediction text belongs to the pre-check form (M_LATCHCLRW); the detector kills both forms."),
    "M_WDEBUG": ("PREDICTION", "p2 ann wr 2 reads \"pass 1 silent (FAILED FOR SOME OTHER REASON)\" whenever pass 1 printed "
                 "no vme text -- a mechanical consequence of the predicted p2 ann wr 0/0/0."),
    "M_RDEBUG": ("PREDICTION", "p2 ann rd 2 reads \"pass 1 silent (FAILED FOR SOME OTHER REASON)\" -- the same mechanical "
                 "consequence of the predicted p2 ann rd 0/0/0."),
    "M_WRFAULT": ("PREDICTION", "p2 ann rd's pass 1 WRITES each register right after reading it, so its first write faults "
                  "(1/1/1 stopped pc=0x18) and both second passes read \"pass 1 not completed\"; the nonword session's "
                  "first store (st.b 0x14) faults and stops the session, so p2 nw rd fails with p2 nw wr "
                  "(\"stopped pc=0x18\")."),
    "M_STORE": ("PREDICTION", "p2 st widths reads 0x28, 0x08 and 0x0c back after st.h 0x28 / st.d 0x08: a storing decline "
                "returns 0xc3d4 and 0x55667788 (1/3) -- that row sees a store exactly as p2 wr census does."),
    "M_NOONCE": ("PREDICTION", "p2 nw rd's three first reads are matched against the same full read-form literal, so a "
                 "dropped `(once)' fails it too (0/3)."),
    "M_DROPTCTL": ("PREDICTION", "tctl rt, vbr rt and t1count inc share ONE stepped session whose first store is to TCTL "
                   "(0x60); the fault stops it at 0x18, so all three accept rows go red, not tctl rt alone.  CONTROL=FAIL "
                   "because cased census is a control row: detected, under the control reason (as the addendum's section "
                   "2 (iii) records for a dropped VBR label)."),
}


def rd(p):
    with io.open(p, "r", encoding="latin-1", newline="") as f:
        return f.read()


def parse(label):
    p = os.path.join(LEGS_DIR, label + ".raw")
    t = rd(p)
    lines = t.split("\n")
    while lines and lines[-1] == "":
        lines.pop()
    r = {"label": label, "path": p, "head": lines[0] if lines else ""}
    if lines and lines[-1] == "KT568_BUILD_FAILED_RECORDED":
        r["build_failed"] = True
        r["error"] = next((l for l in lines if "error:" in l), "?")
        return r
    if not lines or lines[-1] != "VME_DEFAULT_PROBE_DONE":
        raise SystemExit("REFUSED: %s has no completion line" % p)
    r["build_failed"] = False
    g = lambda k: next((l.split("=", 1)[1] for l in lines if l.startswith(k + "=")), None)
    r["result"], r["control"], r["elapsed"] = g("VME_DEFAULT_RESULT"), g("VME_DEFAULT_CONTROL"), g("VME_DEFAULT_ELAPSED")
    red_line = g("VME_DEFAULT_RED")
    red = set(red_line.split(",")) if red_line else set()
    #  per-row column, cross-checked against the RED line
    rows, got = {}, {}
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith("row ") and " got " in l)
    except StopIteration:
        raise SystemExit("REFUSED: %s has no row header" % p)
    for l in lines[start + 1:]:
        if l.startswith("SCORE "):
            break
        if l.startswith("  unasm mismatch"):
            continue
        name = l[:16].strip()
        st = l.rsplit(" ", 1)[-1]
        if st in ("ok", "FAIL"):
            rows[name] = (st == "ok")
            #  the probe prints "%-16s %-34s %-34s %-60s %s": strip the KNOWN want/note suffix (from BASE, where every
            #  row is ok and got == want) so an over-long got is recovered whole; else the 34-column slice
            sfx = (" " + WANT[name].ljust(34) + " " + NOTE[name].ljust(60) + " " + st) if name in WANT else None
            if sfx and l.endswith(sfx):
                got[name] = l[17:len(l) - len(sfx)].rstrip()
            else:
                got[name] = l[17:51].rstrip() + (" [?]" if WANT else "")
    col_red = {n for n, ok in rows.items() if not ok}
    if col_red != red:
        raise SystemExit("REFUSED: %s RED line %s != row column %s" % (p, sorted(red), sorted(col_red)))
    n_ok, n_all = r["result"].split("/")
    if int(n_all) != len(rows) or int(n_ok) != sum(rows.values()):
        raise SystemExit("REFUSED: %s RESULT %s disagrees with %d parsed rows" % (p, r["result"], len(rows)))
    r["red"], r["rows"], r["got"] = red, rows, got
    return r


def red_from_run2(fn):
    t = rd(os.path.join(PD, fn))
    m = re.search(r"^VME_DEFAULT_RED=(.*)$", t, re.M)
    res = re.search(r"^VME_DEFAULT_RESULT=(.*)$", t, re.M).group(1)
    ctl = re.search(r"^VME_DEFAULT_CONTROL=(.*)$", t, re.M).group(1)
    return (set(m.group(1).split(",")) if m else set()), res, ctl


def fmt(s):
    return ", ".join(sorted(s, key=ROWORDER.index)) if s else "-"


#  WANT / NOTE per row from BASE (all 34 ok, every got <= 34 columns, so the fixed columns hold)
WANT, NOTE = {}, {}
for _l in rd(os.path.join(LEGS_DIR, "BASE.raw")).split("\n"):
    if len(_l) > 90 and _l.endswith(" ok") and _l[16] == " " and _l[51] == " " and _l[86] == " ":
        WANT[_l[:16].strip()] = _l[52:86].rstrip()
        NOTE[_l[:16].strip()] = _l[87:-3].rstrip()
base = parse("BASE")
ROWORDER = list(base["rows"])
assert len(ROWORDER) == 34, len(ROWORDER)
assert sorted(WANT) == sorted(ROWORDER), (sorted(WANT), sorted(ROWORDER))
assert all(base["got"][n] == WANT[n] for n in ROWORDER), "BASE got != want somewhere"

out = []
w = out.append
w("KILLTABLE1_VS_PRETABLE -- #568 (vmedefaultkill) kill table 1, measured 2026-10-20 by the measuring seat (Opus 5.5).")
w("Fix: scratchpad vme/fix/dev_vme.fix568.c md5 4e3e7fc220062b429f7d9d6e140fec9e.  Detector: vme_default_probe.py revision 2,")
w("FROZEN as killtable1/vme_default_probe.frozen.py (md5 19de15b3ea69af28e437cdf92e22c97e) and that copy alone ran every leg.")
w("Clone: WSL /tmp/gxkt568 from `git archive 1a59a47e' (1a59a47e3ebbb648f06268ab790f901cbc71c88a), configure + make -j4;")
w("each leg = ONE exact find/replace on fix568 (mk_legs568.py; legs/<LEG>.diff), dev_vme.o + machine_mvme88k.o + gxemul")
w("removed before every build, `[ gxemul -nt <source> ]' checked after it (RUNLOG.txt, build/<LEG>.build.log).  This script")
w("refuses any raw lacking VME_DEFAULT_PROBE_DONE; first-attempt and frozen-md5 counts are in OBSERVATIONS (f).")
w("Predictions = PRETABLE_ADDENDUM_v2.out section 4, quoted verbatim, parsed by one rule: `a/b' expands to the named rows; a")
w("second-pass row (p2 ann rd 2 / p2 ann wr 2) counts as predicted ONLY where the text names it.  MATCH = measured red set ==")
w("predicted set; MISS = a predicted row stayed green or an unpredicted row went red.  The pre-run seat reading")
w("(SEAT_PREDICTIONS_prerun.txt, mtime before the first build) is compared in the last field.")
w("")
w("== REFERENCE RUNS ==")
h_pred, h_res, h_ctl = red_from_run2("run2_HEAD.out")
n_pred, n_res, n_ctl = red_from_run2("run2_NULL.out")
for label, pred_txt, pred_set in (("HEAD", "14/34 (measured, run2_HEAD.out)", h_pred), ("BASE", "all 34 green", set()),
                                  ("NULL", "5/34, CONTROL=FAIL (measured, run2_NULL.out)", n_pred),
                                  ("BASE_FINAL", "all 34 green (after the restore)", set())):
    r = parse(label)
    v = "MATCH" if r["red"] == pred_set else "MISS"
    w("%-17s | %s | CONTROL=%s | red(%d): %s | predicted: %s | %s" % (label, r["result"], r["control"], len(r["red"]),
                                                                    fmt(r["red"]), pred_txt, v))
w("")
w("== THE TABLE (one line per leg: LEG | score | CONTROL | measured red rows | PRETABLE addendum section 4 prediction | "
  "MATCH/MISS | seat pre-run reading) ==")
summary = {"match_kill": [], "match_surv": [], "miss": [], "surv": [], "seat_ok": 0}
seat_bad = []
measured = {}
for L in ORDER:
    txt, pset = PRED[L]
    r = parse(L)
    measured[L] = r
    if r["build_failed"]:
        ok = (pset == "BUILD_FAILS")
        seat = "seat reading: SAME" if SEAT[L] == "BUILD_FAILS" else "seat reading: DIFFERENT"
        if SEAT[L] == "BUILD_FAILS":
            summary["seat_ok"] += 1
        else:
            seat_bad.append(L)
        w("%-17s | BUILD FAILED | - | %s | predicted: %s | %s | %s" % (L, r["error"].strip(), txt,
                                                                     "MATCH" if ok else "MISS", seat))
        (summary["match_kill"] if ok else summary["miss"]).append(L)
        continue
    red = r["red"]
    if pset == "BUILD_FAILS":
        verdict = "MISS (predicted a build failure; it built)"
        summary["miss"].append(L)
    else:
        missing, extra = pset - red, red - pset
        if not missing and not extra:
            verdict = "MATCH"
            (summary["match_kill"] if red else summary["match_surv"]).append(L)
        else:
            parts = []
            if missing:
                parts.append("predicted but GREEN: " + fmt(missing))
            if extra:
                parts.append("unpredicted red: " + fmt(extra))
            verdict = "MISS (" + "; ".join(parts) + ")"
            summary["miss"].append(L)
    if not red:
        summary["surv"].append(L)
    if SEAT[L] == red:
        summary["seat_ok"] += 1
        seat = "seat reading: SAME"
    else:
        seat_bad.append(L)
        seat = "seat reading: DIFFERENT (seat %s)" % fmt(SEAT[L])
    w("%-17s | %s | CONTROL=%s | red(%d): %s | predicted: %s | %s | %s" % (L, r["result"], r["control"], len(red),
                                                                         fmt(red), txt, verdict, seat))
w("")
w("== SURVIVORS (legs scoring 34/34) ==")
for L in summary["surv"]:
    w("%-17s %s CONTROL=%s -- PRETABLE: %s.  %s" % (L, measured[L]["result"], measured[L]["control"], PRED[L][0],
      "PREDICTED SURVIVOR: an equivalent-today edit (no population-2 word is ever non-zero, so a read is 0 and its "
      "announce prints 0x0 with or without the edit); a result about the TARGET, not a detector gap -- the probe's "
      "contract discloses it (\"a served value other than 0 in the read announce\")."))
if not summary["surv"]:
    w("(none)")
w("")
w("== MISS NOTES (cause: EDIT = the leg is mis-built or mistranslated; TARGET = equivalent code; ROW = the row cannot see "
  "it; PREDICTION = none of the three: the leg is built as described, it was killed, and the extra red rows can see it) ==")
for L in summary["miss"]:
    cause, why = NOTES.get(L, ("?", "NO NOTE WRITTEN"))
    r = measured[L]
    gots = "; ".join("%s = %s" % (n, r["got"][n]) for n in ROWORDER
                     if n in (r["red"] ^ (PRED[L][1] if isinstance(PRED[L][1], set) else set())))
    w("%-17s cause: %s.  %s  [measured: %s]" % (L, cause, why, gots))
w("")
w("== PER-ROW KILL CENSUS (which legs of this table red each row; HEAD and NULL excluded) ==")
for n in ROWORDER:
    killers = [L for L in ORDER if not measured[L]["build_failed"] and n in measured[L]["red"]]
    w("%-16s %2d  %s" % (n, len(killers), ", ".join(killers) if killers else "-- no leg in this table reds it"))
w("")
w("== OBSERVATIONS ==")
#  (a) wall time
b_el = float(base["elapsed"].rstrip("s"))
slow = [(L, measured[L]["elapsed"]) for L in ORDER if not measured[L]["build_failed"]
        and float(measured[L]["elapsed"].rstrip("s")) > 2 * b_el]
w("(a) ELAPSED: BASE %s; legs over twice that: %s.  Each is +60 s = the probe's two 30-s `continue' budgets (t_run): in"
  % (base["elapsed"], ", ".join("%s %s" % s for s in slow) or "none"))
w("    both two-pass announce sessions pass 1 stops on the vector breakpoint with no rte, and pass 2's `continue' never")
w("    reaches a breakpoint (the probe's own docstring: a second data-access exception while PSR.SFRZ is set becomes")
w("    ERROR), so the probe kills that child after 30 s.  INFERRED from the arithmetic and the docstring, NOT measured;")
w("    no row value depends on it -- both pass-2 rows are computed from pass 1 (\"pass 1 not completed\").")
#  (b) red rows whose own got-text disclaims the reason
dis = []
for L in ORDER:
    r = measured[L]
    if r["build_failed"]:
        continue
    for n in ROWORDER:
        if n in r["red"] and "FAILED FOR SOME OTHER REASON" in r["got"][n]:
            dis.append("%s/%s" % (L, n))
w("(b) Red rows whose own got-text says \"(FAILED FOR SOME OTHER REASON)\" although the stop IS the leg's edit: %d -- %s."
  % (len(dis), ", ".join(dis) or "none"))
w("    They are kills (the row reds, the score drops), but a reader of the row text alone would discount them.  Two")
w("    shapes: a second-pass row (\"pass 1 not completed\" / \"pass 1 silent\") that only restates pass 1, and the")
w("    nonword rows' \"stopped pc=0x18\" under M_WRFAULT and M_LENFAULT -- for M_LENFAULT those two rows ARE the")
w("    channel PRETABLE named, so the CHANNEL claim holds while the row's text disowns it.")
#  (c) channel claims with no leg here
dead = [n for n in ROWORDER if not any(n in measured[L]["red"] for L in ORDER if not measured[L]["build_failed"])]
w("(c) CHANNEL check (PRETABLE section 4's last line asks the table to say whether each named channel varied): every row")
w("    PRETABLE section 4 names against a leg built here went red under that leg.  Rows NO leg reds (%d): %s."
  % (len(dead), ", ".join(dead)))
w("    Nine are CONTROL rows; `cased wr' is not.  PRETABLE section 4 aims t1cmp rt, tctl rt, vbr rt, t1count inc and")
w("    cased wr at \"a cased WRITE path broken\" and NO leg of this table builds that edit: tctl rt, vbr rt and")
w("    t1count inc red only because M_DROPTCTL's label drop stops their shared session at its first store, and t1cmp")
w("    rt / cased wr see no leg at all.  Likewise \"a label added AT 0x90\" (p1 p2 edge) was not built (M_ADD94 adds")
w("    0x94).  Not measured here -- a gap in the TABLE, not a demonstrated detector gap.")
#  (d) restore record
st = rd(os.path.join(KT, "build", "RESTORE.status")).strip()
bf = parse("BASE_FINAL")
md5_of = lambda r: re.search(r"BINARY_MD5 (\S+)", r["head"]).group(1)
w("(d) Restore: %s." % st)
when = lambda r: re.search(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)\s*$", r["head"]).group(1)
w("    BASE binary %s (run %s, %s CONTROL=%s) and BASE_FINAL binary %s (run %s after the restore, %s CONTROL=%s): %s."
  % (md5_of(base), when(base), base["result"], base["control"], md5_of(bf), when(bf), bf["result"], bf["control"],
     "byte-identical" if md5_of(base) == md5_of(bf) else "DIFFERENT"))
w("    The sentinel was cleared only after that (RUNLOG.txt).  The build itself regenerates two TRACKED files,")
w("    src/devices/.index and src/machines/.index (configure + make on the pristine archive changes them), so a")
w("    whole-tree cmp of any BUILT clone against the archive flags those two; the restore checked them against their")
w("    post-HEAD-build snapshot.")
w("(e) M_LATCHCLRW: PRETABLE.out section 5 (\"the write clears; later reads\") and the addendum (\"each read-first")
w("    register re-announces on its write\") describe two different edits.  Both were built (M_LATCHCLRW = clear before")
w("    the check, the addendum's; M_LATCHCLRW_POST = clear after it, section 5's) and both are killed (%s and %s)."
  % (measured["M_LATCHCLRW"]["result"], measured["M_LATCHCLRW_POST"]["result"]))
allruns = ["HEAD", "BASE", "NULL", "BASE_FINAL"] + [L for L in ORDER if not measured[L]["build_failed"]]
frozen = [x for x in allruns if "PROBE_MD5 19de15b3ea69af28e437cdf92e22c97e " in parse(x)["head"]]
incompl = [f for f in os.listdir(LEGS_DIR) if ".incomplete" in f]
first = [x for x in allruns if " ATTEMPT 1 " in parse(x)["head"]]
w("(f) Probe runs whose raw first line names the frozen copy's md5 19de15b3...: %d of %d; completed on ATTEMPT 1: %d of"
  " %d; .incomplete files: %d.  M_CAPNARROW's" % (len(frozen), len(allruns), len(first), len(allruns), len(incompl)))
w("    make exited 2 and left no binary (removed before the build), so no stale binary could be measured.")
w("")
k = len(summary["match_kill"])
w("== COUNTS ==")
w("legs: %d (the 23 PRETABLE legs + M_LATCHCLRW_POST, a second translation of M_LATCHCLRW); MATCH %d (%d killed as "
  "predicted, incl. M_CAPNARROW's build failure; %d predicted survivors); MISS %d; survivors %d; seat pre-run reading "
  "identical to the measured red set for %d of %d legs%s." % (len(ORDER), k + len(summary["match_surv"]), k,
                                                            len(summary["match_surv"]), len(summary["miss"]),
                                                            len(summary["surv"]), summary["seat_ok"], len(ORDER),
                                                            (" (different: " + ", ".join(seat_bad) + ")") if seat_bad else ""))
w("VERDICT: TABLE DONE -- %d legs, %d red as predicted, %d misses, %d survivors" % (len(ORDER), k, len(summary["miss"]),
                                                                                 len(summary["surv"])))
dst = os.path.join(KT, "KILLTABLE1_VS_PRETABLE.out")
with io.open(dst, "w", encoding="latin-1", newline="") as f:
    f.write("\n".join(out) + "\n")
print("\n".join(out))
print("CMP_TABLE568_DONE -> %s" % dst)
