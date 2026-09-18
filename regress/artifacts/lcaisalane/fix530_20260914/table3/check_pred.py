#!/usr/bin/env python3
"""check_pred.py -- #530 kill table 3: compare each measured red-row set to PRETABLE.out's prediction, EXACTLY."""
import io, os, re, sys
K = os.path.dirname(os.path.abspath(__file__))
pt = io.open(os.path.join(K, "PRETABLE.out"), encoding="utf-8").read()
sec = pt[pt.index("PREDICTED RED ROWS"):pt.index("A red row outside")]
pred, cur = {}, None
for line in sec.splitlines()[1:]:
    m = re.match(r"^   (\w+)\s+(.*)$", line)
    if m and not line.startswith("    "):
        cur = m.group(1); pred[cur] = m.group(2)
    elif cur and line.startswith("      "):            # continuation: any indent deeper than an entry's 3
        pred[cur] += " " + line.strip()
def rows_of(txt):
    if txt.startswith("(none)"):                     # base, and the two PREDICTED-EQUIVALENT mutants
        return set()
    txt = re.sub(r"\(.*?\)", "", txt)                 # parenthetical notes
    txt = re.sub(r"\d+/77", "", txt)
    txt = txt.replace("-- PREDICTED EQUIVALENT", "")
    return set(x.strip() for x in txt.split(",") if x.strip() and x.strip() != "none" and x.strip() != "--")
P = {m: rows_of(t) for m, t in pred.items()}
exact = differ = pend = 0
for m in P:
    log = os.path.join(K, "logs", "probe_%s.raw" % m)
    if not os.path.exists(log) or "LCAISALANE_DONE" not in io.open(log, encoding="utf-8", errors="replace").read():
        print("PENDING  %s" % m); pend += 1; continue
    got = set(l[:14].strip() for l in io.open(log, encoding="utf-8", errors="replace").read().splitlines()
              if l.rstrip().endswith(" FAIL") and len(l) > 14)
    if got == P[m]:
        exact += 1; print("EXACT    %-16s %d red" % (m, len(got)))
    else:
        differ += 1
        print("DIFFERS  %-16s extra=%s missing=%s" % (m, sorted(got - P[m]), sorted(P[m] - got)))
print("CHECKPRED exact=%d differs=%d of %d measured (%d predicted)" % (exact, differ, exact + differ, len(P)))
