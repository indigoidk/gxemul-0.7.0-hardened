#!/usr/bin/env python3
"""cmp_table568b.py -- writes KILLTABLE1B.out for #568 kill table 1b (same shape as KILLTABLE1_VS_PRETABLE.out).

usage: python3 -I -B cmp_table568b.py <killtable1 dir>      (reads <dir>/table1b/legs/*.raw and, for the combined
                                                            census, table 1's <dir>/legs/*.raw)

PRED transcribes PRETABLE1B.txt's COORDINATOR predictions verbatim (text) with the scoring rule stated there: every
`must' row red; no red row outside must + `allowed' (the rows computed from the sessions the prediction says may also
fail -- M_DROPIRQEN's "any later row in those sessions"); CONTROL as predicted where named; a named numerator (987/988)
checked against the measured got-value.  SEAT transcribes PRETABLE1B.txt's seat reading.  A raw without its completion
line is refused; every red set is read from VME_DEFAULT_RED and cross-checked against the per-row ok/FAIL column.
"""
import io
import os
import re
import sys

KT = sys.argv[1]
T1B = os.path.join(KT, "table1b")
LEGS_B = os.path.join(T1B, "legs")
LEGS_1 = os.path.join(KT, "legs")

#  leg: (coordinator text, must-red, allowed-extra, CONTROL predicted or None, {row: numerator})
PRED = {
    "M_DROPIRQEN": ("cased wr, cased census (CONTROL=FAIL), and any later row in those sessions",
                    {"cased wr", "cased census"}, {"free neg ctl"}, "FAIL", {}),
    "M_T1CMPWRDROP": ("t1cmp rt and free ctl, both CONTROL rows, so CONTROL=FAIL",
                      {"t1cmp rt", "free ctl"}, set(), "FAIL", {}),
    "M_ADD90": ("p1 fault lo, p1 fault wr, p1 p2 edge, p1 census (987/988)",
                {"p1 fault lo", "p1 fault wr", "p1 p2 edge", "p1 census"}, set(), None, {"p1 census": "987/988"}),
}
SEAT = {"M_DROPIRQEN": ({"cased census", "cased wr"}, "FAIL"), "M_T1CMPWRDROP": ({"t1cmp rt", "free ctl"}, "FAIL"),
        "M_ADD90": ({"p1 fault lo", "p1 fault wr", "p1 p2 edge", "p1 census"}, "OK")}
ORDER = ["M_DROPIRQEN", "M_T1CMPWRDROP", "M_ADD90"]
EDIT = {"M_DROPIRQEN": "delete the label line `case VME2_IRQEN:'",
        "M_T1CMPWRDROP": "T1CMP arm: `if (writeflag == MEM_WRITE)' -> `if (writeflag == MEM_READ)'",
        "M_ADD90": "`case 0x90:' added before `case VME2_SADDR2:'"}
#  table 1's legs, for the combined census (its 24 legs; HEAD / NULL excluded as in table 1)
T1_LEGS = ["M_EXIT", "M_DROPMCTL", "M_DROPMISC", "M_ADD94", "M_LATCHONE", "M_LATCHNOSET", "M_LATCHRDSET", "M_LATCHCLRW",
           "M_LATCHCLRW_POST", "M_WDEBUG", "M_RDEBUG", "M_ANNLEN4", "M_TRUNC", "M_WRFAULT", "M_LENFAULT", "M_STORE",
           "M_ODATA0", "M_SERVED0", "M_FLTBREAK", "M_FLTLEN", "M_FLTWR", "M_NOONCE", "M_DROPTCTL", "M_CAPNARROW"]


def rd(p):
    with io.open(p, "r", encoding="latin-1", newline="") as f:
        return f.read()


#  WANT / NOTE per row from table 1b's BASE (all 34 ok, every got <= 34 columns, so the fixed columns hold)
WANT, NOTE = {}, {}
for _l in rd(os.path.join(LEGS_B, "BASE.raw")).split("\n"):
    if len(_l) > 90 and _l.endswith(" ok") and _l[16] == " " and _l[51] == " " and _l[86] == " ":
        WANT[_l[:16].strip()] = _l[52:86].rstrip()
        NOTE[_l[:16].strip()] = _l[87:-3].rstrip()


def parse(d, label):
    p = os.path.join(d, label + ".raw")
    lines = rd(p).split("\n")
    while lines and lines[-1] == "":
        lines.pop()
    r = {"label": label, "path": p, "head": lines[0] if lines else ""}
    if lines and lines[-1] == "KT568_BUILD_FAILED_RECORDED":
        r["build_failed"] = True
        return r
    if not lines or lines[-1] != "VME_DEFAULT_PROBE_DONE":
        raise SystemExit("REFUSED: %s has no completion line" % p)
    r["build_failed"] = False
    g = lambda k: next((l.split("=", 1)[1] for l in lines if l.startswith(k + "=")), None)
    r["result"], r["control"], r["elapsed"] = g("VME_DEFAULT_RESULT"), g("VME_DEFAULT_CONTROL"), g("VME_DEFAULT_ELAPSED")
    rl = g("VME_DEFAULT_RED")
    red = set(rl.split(",")) if rl else set()
    start = next(i for i, l in enumerate(lines) if l.startswith("row ") and " got " in l)
    rows, got = {}, {}
    for l in lines[start + 1:]:
        if l.startswith("SCORE "):
            break
        if l.startswith("  unasm mismatch"):
            continue
        name, st = l[:16].strip(), l.rsplit(" ", 1)[-1]
        if st in ("ok", "FAIL"):
            rows[name] = (st == "ok")
            sfx = (" " + WANT[name].ljust(34) + " " + NOTE[name].ljust(60) + " " + st) if name in WANT else None
            got[name] = l[17:len(l) - len(sfx)].rstrip() if (sfx and l.endswith(sfx)) else l[17:51].rstrip() + " [?]"
    if {n for n, ok in rows.items() if not ok} != red:
        raise SystemExit("REFUSED: %s RED line disagrees with the row column" % p)
    n_ok, n_all = r["result"].split("/")
    if int(n_all) != len(rows) or int(n_ok) != sum(rows.values()):
        raise SystemExit("REFUSED: %s RESULT disagrees with the rows" % p)
    r["red"], r["rows"], r["got"] = red, rows, got
    return r


base = parse(LEGS_B, "BASE")
ROWORDER = list(base["rows"])
assert len(ROWORDER) == 34 and sorted(WANT) == sorted(ROWORDER)
assert all(base["got"][n] == WANT[n] for n in ROWORDER), "BASE got != want somewhere"
CONTROL_ROWS = ("session", "live", "unasm", "neg apparatus", "vbr reset", "t1cmp rt", "cased census", "free ctl",
                "free quiet", "free neg ctl")


def fmt(s):
    return ", ".join(sorted(s, key=ROWORDER.index)) if s else "-"


out = []
w = out.append
w("KILLTABLE1B -- #568 (vmedefaultkill) kill table 1b, measured 2026-10-20 by the measuring seat (Opus 5.5).  It closes")
w("the two gaps KILLTABLE1_VS_PRETABLE.out named in OBSERVATIONS (c): no leg built \"a cased WRITE path broken\" (t1cmp rt")
w("and cased wr saw no leg) and none built \"a label added AT 0x90\" (p1 p2 edge).")
w("Fix: scratchpad vme/fix/dev_vme.fix568.c md5 4e3e7fc220062b429f7d9d6e140fec9e.  Detector: the SAME frozen copy table 1")
w("used, killtable1/vme_default_probe.frozen.py (md5 19de15b3ea69af28e437cdf92e22c97e), and that copy alone.")
w("Clone: WSL /tmp/gxkt568b from `git archive 1a59a47e' (1a59a47e3ebbb648f06268ab790f901cbc71c88a), configure + make -j4;")
w("each leg = ONE exact find/replace on fix568 (mk_legs568b.py; legs/<LEG>.diff); dev_vme.o + machine_mvme88k.o + gxemul")
w("removed before every build and `[ gxemul -nt <source> ]' checked after it (RUNLOG.txt, build/<LEG>.build.log); driver")
w("kt568b.sh = table 1's kt568.sh with only its locations changed.  This script refuses any raw lacking")
w("VME_DEFAULT_PROBE_DONE.  Predictions = PRETABLE1B.txt (the coordinator's, verbatim), written BEFORE the first build;")
w("MATCH = every predicted row red, no red row outside the predicted rows plus the prediction's own allowance, CONTROL")
w("as predicted where named, and a named numerator (987/988) equal to the measured one.  The seat's reading (also in")
w("PRETABLE1B.txt) is compared in the last field.")
w("")
w("== REFERENCE RUNS ==")
for label in ("BASE", "BASE_FINAL"):
    r = parse(LEGS_B, label)
    w("%-17s | %s | CONTROL=%s | red(%d): %s | predicted: all 34 green | %s"
      % (label, r["result"], r["control"], len(r["red"]), fmt(r["red"]),
         "MATCH" if not r["red"] and r["control"] == "OK" else "MISS"))
w("")
w("== THE TABLE (one line per leg: LEG | score | CONTROL | measured red rows | PRETABLE1B prediction (coordinator) | "
  "MATCH/MISS | seat reading) ==")
measured, nmatch, misses, survivors, seat_same = {}, 0, [], [], 0
for L in ORDER:
    txt, must, allowed, ctl, nums = PRED[L]
    r = parse(LEGS_B, L)
    measured[L] = r
    red = r["red"]
    probs = []
    if must - red:
        probs.append("predicted but GREEN: " + fmt(must - red))
    if red - must - allowed:
        probs.append("unpredicted red: " + fmt(red - must - allowed))
    if ctl and r["control"] != ctl:
        probs.append("CONTROL=%s, predicted %s" % (r["control"], ctl))
    for n, v in nums.items():
        if not r["got"][n].startswith(v):
            probs.append("%s = %s, predicted %s" % (n, r["got"][n], v))
    verdict = "MATCH" if not probs else "MISS (" + "; ".join(probs) + ")"
    if probs:
        misses.append(L)
    else:
        nmatch += 1
    if not red:
        survivors.append(L)
    s_red, s_ctl = SEAT[L]
    same = (s_red == red and s_ctl == r["control"])
    seat_same += same
    w("%-17s | %s | CONTROL=%s | red(%d): %s | predicted: %s | %s | %s"
      % (L, r["result"], r["control"], len(red), fmt(red), txt, verdict,
         "seat reading: SAME" if same else "seat reading: DIFFERENT (seat %s, CONTROL=%s)" % (fmt(s_red), s_ctl)))
w("")
w("== MEASURED GOT-VALUES OF THE RED ROWS ==")
for L in ORDER:
    r = measured[L]
    w("%-17s %s" % (L, "; ".join("%s = %s" % (n, r["got"][n]) for n in ROWORDER if n in r["red"])))
w("")
w("== SURVIVORS (legs scoring 34/34) ==")
w("(none)" if not survivors else "\n".join(survivors))
w("")
w("== MISS NOTES ==")
w("(none)" if not misses else "\n".join(misses))
w("")
w("== PER-ROW KILL CENSUS, TABLES 1 + 1b COMBINED (legs that red each row; HEAD and NULL excluded) ==")
t1 = {L: parse(LEGS_1, L) for L in T1_LEGS}
for n in ROWORDER:
    k1 = [L for L in T1_LEGS if not t1[L]["build_failed"] and n in t1[L]["red"]]
    kb = [L for L in ORDER if n in measured[L]["red"]]
    tag = "" if (k1 or kb) else "-- no leg in either table reds it"
    w("%-16s %2d  %s%s%s%s" % (n, len(k1) + len(kb), ", ".join(k1), " | 1b: " if kb else "", ", ".join(kb), tag))
dead = [n for n in ROWORDER if not any(n in measured[L]["red"] for L in ORDER)
        and not any(not t1[L]["build_failed"] and n in t1[L]["red"] for L in T1_LEGS)]
w("")
w("== OBSERVATIONS ==")
dead1 = [n for n in ROWORDER if not any(not t1[L]["build_failed"] and n in t1[L]["red"] for L in T1_LEGS)]
closed = [n for n in dead1 if n not in dead]
null1 = parse(LEGS_1, "NULL")
w("(a) The gaps: table 1 left %d rows with no killing leg (%s); after table 1b, %d: %s."
  % (len(dead1), ", ".join(dead1), len(dead), ", ".join(dead) or "none"))
w("    Closed by 1b: %s." % "; ".join("%s (by %s)" % (n, ", ".join(L for L in ORDER if n in measured[L]["red"]))
                                     for n in closed))
w("    p1 p2 edge already had kills in table 1 (M_EXIT, M_DROPMISC, M_FLTBREAK), but not from its named mutant \"a label")
w("    added AT 0x90\"; M_ADD90 now reds it%s." % (" (measured: %s)" % measured["M_ADD90"]["got"]["p1 p2 edge"]
                                                if "p1 p2 edge" in measured["M_ADD90"]["red"] else " -- NOT: it stayed green"))
w("    Rows still red under no leg of either table: %s.  Of those, CONTROL rows: %s; the null medium (table 1's NULL.raw)"
  % (", ".join(dead) or "none", ", ".join(n for n in dead if n in CONTROL_ROWS) or "none"))
w("    reds %s.  These are apparatus controls whose job is to stay green; PRETABLE section 4 lists unasm / live / neg"
  % (", ".join(n for n in dead if n in null1["red"]) or "none of them"))
w("    apparatus / vbr reset / free ctl / free quiet as apparatus, and the addendum added session and free neg ctl as")
w("    controls -- none of them is a channel aimed at a dev_vme.c mutant.")
for L in ORDER:
    r = measured[L]
    c_red = [n for n in ROWORDER if n in r["red"] and n in CONTROL_ROWS]
    nc_red = [n for n in ROWORDER if n in r["red"] and n not in CONTROL_ROWS]
    w("(b) %-15s CONTROL=%s; red CONTROL rows: %s; red non-control rows: %s." % (L, r["control"], ", ".join(c_red) or "none",
                                                                              ", ".join(nc_red) or "NONE"))
w("    A leg seen only through CONTROL rows reds a gate (the probe exits 1) under the CONTROL reason, not under a row")
w("    of its own -- the shape table 1's M_DROPTCTL showed for cased census (KILLTABLE1_VS_PRETABLE.out, MISS NOTES).")
el = [(L, measured[L]["elapsed"]) for L in ORDER]
b_el = float(base["elapsed"].rstrip("s"))
slow = [L for L, e in el if float(e.rstrip("s")) > 2 * b_el]
w("(c) ELAPSED: BASE %s; %s; legs over twice BASE: %s." % (base["elapsed"], ", ".join("%s %s" % e for e in el),
                                                           ", ".join(slow) or "none"))
st = rd(os.path.join(T1B, "build", "RESTORE.status")).strip()
bf = parse(LEGS_B, "BASE_FINAL")
md5_of = lambda r: re.search(r"BINARY_MD5 (\S+)", r["head"]).group(1)
when = lambda r: re.search(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)\s*$", r["head"]).group(1)
w("(d) Restore: %s." % st)
w("    BASE binary %s (run %s, %s CONTROL=%s) and BASE_FINAL binary %s (run %s after the restore, %s CONTROL=%s): %s."
  % (md5_of(base), when(base), base["result"], base["control"], md5_of(bf), when(bf), bf["result"], bf["control"],
     "byte-identical" if md5_of(base) == md5_of(bf) else "DIFFERENT"))
same_man = rd(os.path.join(KT, "ref", "archive_1a59a47e.md5")) == rd(os.path.join(T1B, "ref", "archive_1a59a47e.md5"))
same_snap = (rd(os.path.join(KT, "ref", "postbuild_HEAD_regenerated.md5"))
             == rd(os.path.join(T1B, "ref", "postbuild_HEAD_regenerated.md5")))
w("    Against table 1: the 30,795-file archive manifest is %s; the post-HEAD-build snapshot of the two"
  % ("IDENTICAL" if same_man else "DIFFERENT"))
w("    build-regenerated files is %s.  The binaries differ from table 1's (the clone path differs); the sources do not."
  % ("IDENTICAL" if same_snap else "DIFFERENT"))
allruns = ["BASE", "BASE_FINAL"] + ORDER
heads = {x: parse(LEGS_B, x)["head"] for x in allruns}
frozen = [x for x in allruns if "PROBE_MD5 19de15b3ea69af28e437cdf92e22c97e " in heads[x]]
first = [x for x in allruns if " ATTEMPT 1 " in heads[x]]
incompl = [f for f in os.listdir(LEGS_B) if ".incomplete" in f]
w("(e) Probe runs naming the frozen copy's md5 19de15b3...: %d of %d; completed on ATTEMPT 1: %d of %d; .incomplete"
  " files: %d." % (len(frozen), len(allruns), len(first), len(allruns), len(incompl)))
w("")
w("== COUNTS ==")
kill_match = len([L for L in ORDER if L not in misses and L not in survivors])
w("legs: %d; MATCH %d (%d killed as predicted, %d predicted survivors); MISS %d; survivors %d; seat reading identical"
  " (red rows and CONTROL) for %d of %d." % (len(ORDER), nmatch, kill_match, nmatch - kill_match, len(misses),
                                            len(survivors), seat_same, len(ORDER)))
w("VERDICT: TABLE 1B DONE -- %d legs, %d red as predicted, %d misses, %d survivors"
  % (len(ORDER), kill_match, len(misses), len(survivors)))
dst = os.path.join(T1B, "KILLTABLE1B.out")
with io.open(dst, "w", encoding="latin-1", newline="") as f:
    f.write("\n".join(out) + "\n")
print("\n".join(out))
print("CMP_TABLE568B_DONE -> %s" % dst)
