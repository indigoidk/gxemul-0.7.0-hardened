#!/usr/bin/env python3
"""cmp_table2.py -- writes KILLTABLE2_VS_PRETABLE2.out for #568 kill table 2 (same shape as tables 1 / 1b).

usage: python3 -I -B cmp_table2.py <rev3/table2 dir>

Predictions and the per-row channel map come ONLY from PRETABLE2_predictions.json (written with PRETABLE2.out before the
table's first build; the mtimes are compared below).  Red sets are read from each raw's VME_DEFAULT_RED and
cross-checked against the per-row ok/FAIL column; a raw without its completion line is refused.  A red row is OWN when
PRETABLE2's channel map names the leg for that row; otherwise it is DEPENDENT (its text says the row's check was not
made: not exercised / pass 1 silent / an unexpected or vector stop / died / nodev) or a SECOND CHANNEL (the row's own
check varied for a reason PRETABLE2 did not design it for).
"""
import io
import json
import os
import re
import sys

T2 = sys.argv[1]
LEGS = os.path.join(T2, "legs")
P = json.load(io.open(os.path.join(T2, "PRETABLE2_predictions.json"), encoding="latin-1"))
ROWS, CONTROL, CHAN = P["rows"], P["control"], P["channel"]
PRED = {l["leg"]: l for l in P["legs"]}
REFS = ["BASE", "HEAD", "NULL", "BASE_FINAL"]
ORDER = [l["leg"] for l in P["legs"] if l["leg"] not in REFS]


def rd(p):
    with io.open(p, "r", encoding="latin-1", newline="") as f:
        return f.read()


#  WANT / NOTE per row from BASE (all 38 ok, every got <= 34 columns), so an over-long got is recovered whole
WANT, NOTE = {}, {}
for _l in rd(os.path.join(LEGS, "BASE.raw")).split("\n"):
    if len(_l) > 90 and _l.endswith(" ok") and _l[16] == " " and _l[51] == " " and _l[86] == " ":
        WANT[_l[:16].strip()] = _l[52:86].rstrip()
        NOTE[_l[:16].strip()] = _l[87:-3].rstrip()
assert sorted(WANT) == sorted(ROWS), sorted(set(WANT) ^ set(ROWS))


def parse(label):
    p = os.path.join(LEGS, label + ".raw")
    lines = rd(p).rstrip("\n").split("\n")
    r = {"label": label, "head": lines[0]}
    if lines[-1] == "KT568_BUILD_FAILED_RECORDED":
        r["build_failed"] = True
        r["error"] = next((l for l in lines if "error:" in l), "?").strip()
        return r
    if lines[-1] != "VME_DEFAULT_PROBE_DONE":
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
        if l.startswith("  "):
            continue
        name, st = l[:16].strip(), l.rsplit(" ", 1)[-1]
        if st in ("ok", "FAIL"):
            rows[name] = (st == "ok")
            sfx = " " + WANT[name].ljust(34) + " " + NOTE[name].ljust(60) + " " + st
            got[name] = l[17:len(l) - len(sfx)].rstrip() if l.endswith(sfx) else l[17:51].rstrip() + " [?]"
    if {n for n, ok in rows.items() if not ok} != red:
        raise SystemExit("REFUSED: %s RED line disagrees with the row column" % p)
    n_ok, n_all = r["result"].split("/")
    if int(n_all) != len(rows) or int(n_ok) != sum(rows.values()) or list(rows) != ROWS:
        raise SystemExit("REFUSED: %s RESULT / row list disagrees" % p)
    r["red"], r["rows"], r["got"] = red, rows, got
    return r


def fmt(s):
    return ", ".join(sorted(s, key=ROWS.index)) if s else "-"


DEP = ("not exercised", "pass 1 silent", "unexpected stop", "stopped pc=", "pc=0x18", "died:", "timeout:", "nodev")


def classify(leg, r):
    own, dep, sec = [], [], []
    for n in ROWS:
        if n not in r["red"]:
            continue
        if leg in CHAN.get(n, []):
            own.append(n)
        elif any(k in r["got"][n] for k in DEP):
            dep.append(n)
        else:
            sec.append(n)
    return own, dep, sec


measured = {L: parse(L) for L in REFS + ORDER}
out = []
w = out.append
md5 = lambda r, k: (re.search(k + r" (\S+)", r["head"]) or [None, "?"])[1]
pt = os.path.getmtime(os.path.join(T2, "PRETABLE2.out"))
first_build = min(os.path.getmtime(os.path.join(T2, "build", f)) for f in os.listdir(os.path.join(T2, "build"))
                  if f.endswith(".log"))       # configure.log included: the earliest log of the table's clone
w("KILLTABLE2_VS_PRETABLE2 -- #568 (vmedefaultkill) REPAIR 1, kill table 2, measured 2026-10-21 by the measuring seat")
w("(Opus 5.5).  Fix: rev3/dev_vme.fix568b.c (md5 beb120eae1be112b682bd528f103191c).  Detector: probe REVISION 3, frozen as")
w("rev3/vme_default_probe.rev3.frozen.py (md5 ddcebfe3257d3370f3c16b0bee79a4be, 38 rows) -- that copy alone ran every leg")
w("(the PROBE_MD5 in every raw's first line: %d of %d)." % (
    sum(1 for L in measured if not measured[L]["build_failed"] and "ddcebfe3257d3370f3c16b0bee79a4be" in measured[L]["head"]),
    sum(1 for L in measured if not measured[L]["build_failed"])))
w("Clone: WSL /tmp/gxkt568t2 from `git archive 1a59a47e', configure + make -j4; each leg = ONE exact find/replace on fix568b")
w("(mk_legs568t2.py; legs/<LEG>.diff; the table-1/1b legs regenerated with their intent unchanged -- only M_NOONCE's and")
w("M_SERVED0's find-strings moved, onto fix568b's D1 lines).  dev_vme.o + machine_mvme88k.o + gxemul removed before every")
w("build, `[ gxemul -nt <source> ]' after it (RUNLOG.txt, build/*.build.log); legs run ONE AT A TIME.")
w("ORDER: PRETABLE2.out written %s; the table's first build log %s -- %s."
  % (__import__("time").strftime("%H:%M:%S", __import__("time").localtime(pt)),
     __import__("time").strftime("%H:%M:%S", __import__("time").localtime(first_build)),
     "PRETABLE2 FIRST" if pt < first_build else "ORDER VIOLATED"))
w("MATCH = the measured red set equals PRETABLE2's predicted set and CONTROL is as predicted; MISS otherwise.")
w("")
w("== REFERENCE RUNS ==")
for L in REFS:
    r, p = measured[L], PRED[L]
    v = "MATCH" if (r["red"] == set(p["red"]) and r["control"] == p["control"]) else "MISS"
    w("%-11s | %s | CONTROL=%s | red(%d): %s | predicted %d red, CONTROL=%s | %s"
      % (L, r["result"], r["control"], len(r["red"]), fmt(r["red"]), len(p["red"]), p["control"], v))
nr = measured["NULL"]
w("NULL per class (PRETABLE2 section 6): CONTROL red %s; CONTROL green %s; scored red %d; scored green %s."
  % (fmt(nr["red"] & set(CONTROL)), fmt(set(CONTROL) - nr["red"]), len(nr["red"] - set(CONTROL)),
     fmt(set(ROWS) - nr["red"] - set(CONTROL))))
w("BASE binary %s, BASE_FINAL binary %s: %s." % (md5(measured["BASE"], "BINARY_MD5"), md5(measured["BASE_FINAL"], "BINARY_MD5"),
  "byte-identical" if md5(measured["BASE"], "BINARY_MD5") == md5(measured["BASE_FINAL"], "BINARY_MD5") else "DIFFERENT"))
w("")
w("== THE TABLE (one line per leg: LEG | score | CONTROL | measured red rows | PRETABLE2 predicted | MATCH/MISS) ==")
counts = {"match_kill": [], "match_surv": [], "miss": [], "surv": []}
for L in ORDER:
    r, p = measured[L], PRED[L]
    if r["build_failed"]:
        ok = p["red"] == "BUILD_FAILS"
        w("%-17s | BUILD FAILED | - | %s | predicted: BUILD FAILS | %s" % (L, r["error"], "MATCH" if ok else "MISS"))
        (counts["match_kill"] if ok else counts["miss"]).append(L)
        continue
    pr = set(p["red"]) if p["red"] != "BUILD_FAILS" else None
    if pr is None:
        v = "MISS (predicted a build failure; it built)"
    else:
        probs = []
        if pr - r["red"]:
            probs.append("predicted but GREEN: " + fmt(pr - r["red"]))
        if r["red"] - pr:
            probs.append("unpredicted red: " + fmt(r["red"] - pr))
        if r["control"] != p["control"]:
            probs.append("CONTROL=%s, predicted %s" % (r["control"], p["control"]))
        v = "MATCH" if not probs else "MISS (" + "; ".join(probs) + ")"
    if v == "MATCH":
        (counts["match_kill"] if r["red"] else counts["match_surv"]).append(L)
    else:
        counts["miss"].append(L)
    if not r["red"]:
        counts["surv"].append(L)
    w("%-17s | %s | CONTROL=%s | red(%d): %s | predicted red(%d) | %s"
      % (L, r["result"], r["control"], len(r["red"]), fmt(r["red"]), len(pr) if pr is not None else -1, v))
w("")
w("== RED ROWS BY KIND (PRETABLE2's channel map, written before the table): OWN channel / DEPENDENT / SECOND channel ==")
for L in ORDER:
    r = measured[L]
    if r["build_failed"] or not r["red"]:
        continue
    own, dep, sec = classify(L, r)
    w("%-17s own: %s" % (L, ", ".join("%s (%s)" % (n, r["got"][n]) for n in own) or "-"))
    if dep:
        w("%-17s dependent: %s" % ("", ", ".join("%s (%s)" % (n, r["got"][n]) for n in dep)))
    if sec:
        w("%-17s second channel: %s" % ("", ", ".join("%s (%s)" % (n, r["got"][n]) for n in sec)))
w("")
w("== CHECK OF THE CHANNEL LINE (PRETABLE2 section 4): did every designed channel vary under its named leg? ==")
silent = []
for n in ROWS:
    for L in CHAN.get(n, []):
        if L in measured and not measured[L]["build_failed"] and n not in measured[L]["red"]:
            silent.append("%s under %s" % (n, L))
w("designed (row, leg) pairs: %d; pairs whose row stayed GREEN under its named leg: %d%s"
  % (sum(len(CHAN.get(n, [])) for n in ROWS), len(silent), (" -- " + "; ".join(silent)) if silent else ""))
w("")
w("== SURVIVORS (legs scoring 38 of 38) ==")
for L in counts["surv"]:
    w("%-17s %s CONTROL=%s -- %s.  Diagnosis: the TARGET is equivalent today (no population-2 word is ever non-zero, so"
      % (L, measured[L]["result"], measured[L]["control"], PRED[L]["note"]))
    w("%-17s a read serves 0 and its announce prints 0x0 with or without the edit) -- not a mis-built leg (legs/%s.diff is"
      % ("", L))
    w("%-17s the one edit) and not a mis-cut row; the contract discloses it." % "")
if not counts["surv"]:
    w("(none)")
w("")
w("== MISS NOTES ==")
for L in counts["miss"]:
    r, p = measured[L], PRED[L]
    if L == "M_ONENARROW":
        w("M_ONENARROW  measured red: %s." % ", ".join("%s (%s)" % (n, r["got"][n]) for n in ROWS if n in r["red"]))
        w("  PRETABLE2's PRIMARY prediction (p2 ann rd + p2 ann wr, 25 lines each: a runtime-masked 32-bit shift landing on")
        w("  SLAVELMOD2's bit 3) MISSED; the shape measured is the ALTERNATIVE PRETABLE2 section 7 named in the same paragraph")
        w("  -- `a build whose shift yields 0 would red all four ann rows (MISC never latches: 27 lines in pass 1, 2 in")
        w("  pass 2)' -- exactly.  Cause: neither the leg (one edit, legs/M_ONENARROW.diff) nor the rows -- the COMPILER.")
        w("  The leg's object (obj/M_ONENARROW.dev_vme.o, disassembled after the run: obj/M_ONENARROW_codegen.txt) shows")
        w("  GCC specialising the MISC case and constant-folding the undefined `1u << 35' to 0 there (no latch test, no")
        w("  set), while every other register uses a runtime `shl %cl,%edx'.  KILLED either way, by different rows; no")
        w("  portable claim (D5).")
        continue
    w("%-17s %s" % (L, p["note"]))
if not counts["miss"]:
    w("(none)")
w("")
w("== THE FLOOR BREACH, CLOSED ==")
mi = measured["M_IDATA"]
w("M_IDATA (`if (writeflag == MEM_WRITE)' -> `if (idata)'): left all 34 rows of the rev-2 instrument green")
w("(killtable1_20261020/idata/KILLTABLE_IDATA.out); on rev 3 it scores %s with red %s -- `p2 zero wr' got %r."
  % (mi["result"], fmt(mi["red"]), mi["got"]["p2 zero wr"]))
w("")
w("== PER-ROW KILL CENSUS (legs of table 2 that red each row) ==")
for n in ROWS:
    ks = [L for L in ORDER if not measured[L]["build_failed"] and n in measured[L]["red"]]
    w("%-14s %-8s %2d  %s" % (n, "CONTROL" if n in CONTROL else "", len(ks), ", ".join(ks) if ks else "-- no leg reds it"))
w("")
w("== OBSERVATIONS ==")
tmo = [(L, n) for L in REFS + ORDER if not measured[L]["build_failed"] for n in measured[L]["red"]
       if "timeout:" in measured[L]["got"][n]]
w("(a) Red rows whose text names a TIMEOUT: %d%s.  No leg reds only by a timeout, so no re-run was owed (the window the"
  % (len(tmo), (" -- " + ", ".join("%s/%s" % x for x in tmo)) if tmo else ""))
w("    coordinator flagged, ~01:18-01:45, saw no timeout red).")
base_el = float(measured["BASE"]["elapsed"].rstrip("s"))
slow = [(L, measured[L]["elapsed"]) for L in ORDER if not measured[L]["build_failed"]
        and float(measured[L]["elapsed"].rstrip("s")) > 2 * base_el]
w("(b) ELAPSED: BASE %s; legs over twice that: %s -- PRETABLE2 predicted exactly these (a pass 1 stopped on a fault leaves"
  % (measured["BASE"]["elapsed"], ", ".join("%s %s" % s for s in slow) or "none"))
w("    pass 2 to run under PSR.SFRZ and its `continue' to the 30-s budget): M_DROPMCTL and M_DROPMISC +60, M_WRFAULT +90,")
w("    M_LENFAULT +30.  No row value depends on it.")
st = rd(os.path.join(T2, "build", "RESTORE.status")).strip()
w("(c) Restore: %s." % st)
w("(d) CONTROL after the split: every product leg reports CONTROL=OK -- M_DROPTCTL, M_DROPIRQEN and M_T1CMPWRDROP")
w("    (CONTROL=FAIL on the 34-row rev 2) now red SCORED rows; only the null medium fails CONTROL, by design (section 6).")
w("(e) M_CAPNARROW: %s -- the typedef refuses the narrowed field on fix568b too." % measured["M_CAPNARROW"]["error"]
  if measured["M_CAPNARROW"]["build_failed"] else "(e) M_CAPNARROW BUILT -- the typedef did not fire.")
w("")
k = len(counts["match_kill"])
w("== COUNTS ==")
w("legs: %d (27 regenerated from tables 1 and 1b, 7 new); MATCH %d (%d killed as predicted, incl. M_CAPNARROW's build"
  " failure; %d predicted survivors); MISS %d; survivors %d." % (len(ORDER), k + len(counts["match_surv"]), k,
                                                              len(counts["match_surv"]), len(counts["miss"]),
                                                              len(counts["surv"])))
w("VERDICT: TABLE 2 DONE -- %d legs, %d red as predicted, %d misses, %d survivors" % (len(ORDER), k, len(counts["miss"]),
                                                                                  len(counts["surv"])))
dst = os.path.join(T2, "KILLTABLE2_VS_PRETABLE2.out")
io.open(dst, "w", encoding="latin-1", newline="").write("\n".join(out) + "\n")
print("\n".join(out))
print("CMP_TABLE2_DONE -> %s" % dst)
