#!/usr/bin/env python3
"""q4_check.py -- Q4 re-derived independently of check14.py: parse PRETABLE14.out's PREDICTIONS block and each
table-14 raw log's own row lines (not its FAILING summary), and compare red sets, scores and CRIMEP_CONTROL."""
import os, re

T = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "table14_20260926")
pre = open(os.path.join(T, "PRETABLE14.out"), encoding="latin-1").read()
blk = pre.split("PREDICTIONS -- exact red sets")[1].split("Every pre-existing row's colour")[0]
pred, cur = {}, None
for line in blk.splitlines()[1:]:
    m = re.match(r"  (base|[A-Z]\w+)\s{2,}(.*)$", line)
    if m:
        cur = m.group(1)
        pred[cur] = {"text": m.group(2)}
    elif cur and line.strip():
        pred[cur]["text"] += " " + line.strip()
for leg, p in pred.items():
    m = re.search(r"(\d+)/218\s+(OK|FAIL)", p["text"])
    p["score"], p["ctl"] = int(m.group(1)), m.group(2)
    p["text"] = p["text"][:m.start()]
T12 = ["sb08 msg", "sh08b run", "imask sb", "imask lh", "imask sh", "istat sb", "istat lh", "istat sh", "gate run",
       "mid nodflt"]
ROWS = ["tl lb", "tl sb", "tl lh", "tl sh", "rl lb pc", "rl lh pc", "rl sb pc", "rl sh pc", "time lb", "time sb",
        "time lh", "time sh", "ctldog sw msg", "ctldog sd msg", "gate line", "acc istat lw", "c t4w gap", "c t4r gap",
        "p acc ctl4r", "rst 4w", "rst 8w", "top8 clear", "p acc ctl msg"] + T12
ok_all = True
for leg in sorted(pred):
    p = pred[leg]
    want = set()
    if "table 12's ten" in p["text"]:
        want |= set(T12)
    for r in ROWS:
        if re.search(r"(^|[ ,(])" + re.escape(r) + r"($|[ ,)])", p["text"].replace("table 12's ten", "")):
            want.add(r)
    raw = open(os.path.join(T, "logs", "probe_%s.raw" % leg), encoding="latin-1").read().splitlines()
    got = set(l[:16].strip() for l in raw if l.endswith(" FAIL"))
    score = int(re.search(r"CRIMEP_RESULT=(\d+)/218", "\n".join(raw)).group(1))
    ctl = re.search(r"CRIMEP_CONTROL=(\w+)", "\n".join(raw)).group(1)
    done = raw[-1] == "CRIMEP_DONE"
    good = (want == got and score == p["score"] and ctl == p["ctl"] and done and score == 218 - len(got))
    ok_all &= good
    print("%-20s pred %3d/218 %-4s | got %3d/218 %-4s reds=%2d done=%s  %s%s" % (
        leg, p["score"], p["ctl"], score, ctl, len(got), done, "EXACT" if good else "*** DIFFERS ***",
        "" if good else "  want-only=%s got-only=%s" % (sorted(want - got), sorted(got - want))))
print("Q4_CHECK %s over %d legs" % ("ALL EXACT" if ok_all else "MISMATCH", len(pred)))
