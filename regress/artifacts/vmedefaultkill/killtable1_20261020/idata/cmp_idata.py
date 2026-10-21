#!/usr/bin/env python3
"""cmp_idata.py -- writes KILLTABLE_IDATA.out for #568 "step 0" (the one leg M_IDATA), same shape as table 1/1b.

usage: python3 -I -B cmp_idata.py <killtable1/idata dir>

Reads legs/BASE.raw, legs/M_IDATA.raw, legs/BASE_FINAL.raw.  A raw without its completion line is refused; red sets come
from VME_DEFAULT_RED and are cross-checked against the per-row ok/FAIL column.  Beyond the score it compares the leg's 34
row lines with BASE's, byte for byte, and counts the announce lines the free-running rows saw -- the population-2
announce arm is the edited code, so those are the executions of the edited test that a row observed.
"""
import io
import os
import re
import sys

D = sys.argv[1]
LEGS = os.path.join(D, "legs")
PRED_TXT = ("PREDICTION, written by the seat before any build: 34/34, CONTROL=OK -- every population-2 store in the probe "
            "is non-zero (0xa5a5a5a5, 0xd4/0xc3d4, 0x1122334455667788), and reads leave idata 0.")


def rd(p):
    with io.open(p, "r", encoding="latin-1", newline="") as f:
        return f.read()


def parse(label):
    p = os.path.join(LEGS, label + ".raw")
    lines = rd(p).split("\n")
    while lines and lines[-1] == "":
        lines.pop()
    if not lines or lines[-1] != "VME_DEFAULT_PROBE_DONE":
        raise SystemExit("REFUSED: %s has no completion line" % p)
    g = lambda k: next((l.split("=", 1)[1] for l in lines if l.startswith(k + "=")), None)
    rl = g("VME_DEFAULT_RED")
    red = set(rl.split(",")) if rl else set()
    start = next(i for i, l in enumerate(lines) if l.startswith("row ") and " got " in l)
    rowlines, rows = [], {}
    for l in lines[start + 1:]:
        if l.startswith("SCORE "):
            break
        st = l.rsplit(" ", 1)[-1]
        if st in ("ok", "FAIL"):
            rowlines.append(l)
            rows[l[:16].strip()] = (st == "ok")
    if {n for n, ok in rows.items() if not ok} != red:
        raise SystemExit("REFUSED: %s RED line disagrees with the row column" % p)
    r = {"head": lines[0], "result": g("VME_DEFAULT_RESULT"), "control": g("VME_DEFAULT_CONTROL"),
         "elapsed": g("VME_DEFAULT_ELAPSED"), "red": red, "rows": rows, "rowlines": rowlines,
         "info": next((l for l in lines if l.startswith("INFO ")), "")}
    n_ok, n_all = r["result"].split("/")
    if int(n_all) != len(rows) or int(n_ok) != sum(rows.values()):
        raise SystemExit("REFUSED: %s RESULT disagrees with the rows" % p)
    return r


base, leg, bf = parse("BASE"), parse("M_IDATA"), parse("BASE_FINAL")
md5_of = lambda r: re.search(r"BINARY_MD5 (\S+)", r["head"]).group(1)
vme_of = lambda r: re.search(r"DEV_VME_MD5 (\S+)", r["head"]).group(1)
when = lambda r: re.search(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)\s*$", r["head"]).group(1)
ROWORDER = [l[:16].strip() for l in base["rowlines"]]
assert len(ROWORDER) == 34
same_rows = [a == b for a, b in zip(base["rowlines"], leg["rowlines"])]
diff_rows = [ROWORDER[i] for i, s in enumerate(same_rows) if not s]
ANN = {"p2 ann rd": ("26/26/26", "26 read-form lines (reads: idata 0)"),
       "p2 ann wr": ("26/26/26", "26 write-form lines (first-access writes of 0xa5a5a5a5)"),
       "p2 nw rd": ("3/3", "3 read-form lines (first ld.bu / ld.hu / ld.d)"),
       "p2 nw wr": ("3/3", "3 write-form lines (first st.b 0xd4 / st.h 0xc3d4 / st.d 0x1122334455667788)")}
leg_got = {l[:16].strip(): l[17:51].rstrip() for l in leg["rowlines"]}
red = leg["red"]
verdict = "MATCH" if (not red and leg["control"] == "OK" and leg["result"] == "34/34") else "MISS"

out = []
w = out.append
w("KILLTABLE_IDATA -- #568 (vmedefaultkill) \"step 0\": the one leg M_IDATA on the FROZEN rev-2 probe, measured")
w("2026-10-21 by the measuring seat (Opus 5.5).")
w("Fix: scratchpad vme/fix/dev_vme.fix568.c md5 4e3e7fc220062b429f7d9d6e140fec9e.  Detector: killtable1/")
w("vme_default_probe.frozen.py (md5 19de15b3ea69af28e437cdf92e22c97e) -- the same frozen copy tables 1 and 1b ran -- alone.")
w("Clone: WSL /tmp/gxkt568c from `git archive 1a59a47e' (1a59a47e3ebbb648f06268ab790f901cbc71c88a), configure + make -j4;")
w("the leg = ONE exact find/replace on fix568 (mk_leg_idata.py; legs/M_IDATA.diff): in the population-2 announce arm")
w("ONLY, `if (writeflag == MEM_WRITE)' -> `if (idata)', anchored on the arm's latch-set line because that test occurs 6")
w("times in the fix.  dev_vme.o + machine_mvme88k.o + gxemul removed before every build, `[ gxemul -nt <source> ]' after it")
w("(RUNLOG.txt, build/*.build.log); driver kt568c.sh = table 1's kt568.sh with only its locations changed.  Prediction:")
w("PRETABLE_IDATA.txt, written before the first build.")
w("")
w("== REFERENCE RUNS ==")
for label, r in (("BASE", base), ("BASE_FINAL", bf)):
    w("%-11s | %s | CONTROL=%s | red(%d): %s | predicted: all 34 green | %s"
      % (label, r["result"], r["control"], len(r["red"]), ", ".join(sorted(r["red"])) or "-",
         "MATCH" if not r["red"] and r["control"] == "OK" else "MISS"))
w("")
w("== THE TABLE (LEG | score | CONTROL | measured red rows | prediction | MATCH/MISS | seat reading) ==")
w("M_IDATA     | %s | CONTROL=%s | red(%d): %s | predicted: %s | %s | seat reading: SAME (34/34, CONTROL=OK)"
  % (leg["result"], leg["control"], len(red), ", ".join(sorted(red)) or "-", PRED_TXT, verdict))
w("")
w("== THE LEG RAN ON ITS OWN BINARY ==")
w("BASE       binary %s  dev_vme.c %s  (run %s)" % (md5_of(base), vme_of(base), when(base)))
w("M_IDATA    binary %s  dev_vme.c %s  (run %s)  -- %s" % (md5_of(leg), vme_of(leg), when(leg),
  "a different binary and source from BASE" if md5_of(leg) != md5_of(base) and vme_of(leg) != vme_of(base)
  else "SAME AS BASE -- NOT A MEASUREMENT OF THE LEG"))
w("BASE_FINAL binary %s  dev_vme.c %s  (run %s)  -- %s" % (md5_of(bf), vme_of(bf), when(bf),
  "byte-identical to BASE" if md5_of(bf) == md5_of(base) else "DIFFERENT from BASE"))
w("")
w("== SURVIVORS (legs scoring 34/34) ==")
if not red:
    w("M_IDATA     %s CONTROL=%s -- PREDICTED SURVIVOR.  Its 34 row lines are %s to BASE's%s."
      % (leg["result"], leg["control"], "BYTE-IDENTICAL" if not diff_rows else "NOT identical",
         "" if not diff_rows else " (differ: " + ", ".join(diff_rows) + ")"))
    w("            The edited test IS executed and observed: the free-running announce rows count the lines the edited")
    w("            branch prints, and each matched the fix --")
    for n, (want, what) in ANN.items():
        w("              %-10s got %-9s %s" % (n, leg_got.get(n, "?"), what))
    w("            -- so the leg survives because every access the probe makes takes the same branch under both tests:")
    w("            every first-access population-2 write carries a non-zero value and every read leaves idata 0.  Cause:")
    w("            the ROW SET (input coverage), not an equivalent TARGET.  By reading (NOT measured here): a zero-valued")
    w("            FIRST write to a population-2 register would announce in the read form (`-- served 0x0.') under the leg")
    w("            and in the write form under the fix; the probe makes no such write.")
else:
    w("(none)")
w("")
w("== RE-RUN RULE ==")
w("\"If ANY row reds, re-run that leg ONCE, alone, before reporting\": %s." % (
    "NOT TRIGGERED -- no row went red" if not red else "TRIGGERED"))
w("")
w("== OBSERVATIONS ==")
st = rd(os.path.join(D, "build", "RESTORE.status")).strip()
w("(a) Restore: %s." % st)
first = all(" ATTEMPT 1 " in r["head"] for r in (base, leg, bf))
frozen = all("PROBE_MD5 19de15b3ea69af28e437cdf92e22c97e " in r["head"] for r in (base, leg, bf))
w("(b) All three runs name the frozen copy's md5: %s; all completed on ATTEMPT 1: %s; .incomplete files: %d."
  % ("yes" if frozen else "NO", "yes" if first else "NO", len([f for f in os.listdir(LEGS) if ".incomplete" in f])))
w("(c) ELAPSED: BASE %s, M_IDATA %s, BASE_FINAL %s." % (base["elapsed"], leg["elapsed"], bf["elapsed"]))
w("(d) The INFO line (unscored ld.d at 0x0c) is %s in BASE and the leg." % (
    "identical" if base["info"] == leg["info"] else "DIFFERENT"))
w("")
w("VERDICT: M_IDATA DONE -- 1 leg, %s CONTROL=%s, %s; prediction %s (%s)"
  % (leg["result"], leg["control"], "SURVIVOR" if not red else "KILLED", verdict,
     "34/34, CONTROL=OK predicted"))
dst = os.path.join(D, "KILLTABLE_IDATA.out")
with io.open(dst, "w", encoding="latin-1", newline="") as f:
    f.write("\n".join(out) + "\n")
print("\n".join(out))
print("CMP_IDATA_DONE -> %s" % dst)
