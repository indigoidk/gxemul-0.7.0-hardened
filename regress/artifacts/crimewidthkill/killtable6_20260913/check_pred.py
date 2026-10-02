#!/usr/bin/env python3
"""check_pred.py -- compare kill table 6's measured red-row sets (logs/lane*.out) with PRETABLE 6's predictions,
transcribed here from PRETABLE.out (written before the table, before the table).  Prints one line per run and a tally."""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
S = lambda s: frozenset(x.strip() for x in s.split(",") if x.strip())
IM4 = "imask lb, imask sb, imask lh, imask sh"
IS4 = "istat lb, istat sb, istat lh, istat sh"
NEW = {
    "base": "", "l_rev": "", "l_ctl": "", "l_time": "",
    "imaskft": IM4, "a_istat": IS4,
    "istat2": "istat lh, istat sh", "imask2": "imask lh, imask sh", "h_imask": "imask lh, imask sh", "istatsh": "istat sh",
    "istat_od1": "istat lb v0, istat lh v0",
    "c2_lbl_imask": "imask once", "c2_lbl_istat": "istat once",
    "c2_reg_imask": "imask lb v0, imask lh v0", "c2_reg_istat": "istat lb v0, istat lh v0",
    "c2_land_or": "imask keeps", "c2_pre_irq": "imask once, istat once",
    "o_hi_gate": "gate run", "o_pa_gate": "gate run",
    "q_istat_leak": "istat lb v0, istat lh v0", "q_istat_lane": "istat lb v0, istat lh v0",
    "q_dog_leak": "dog v0, dog lh v0", "l_imask": "imask lb v0, imask lh v0", "l_dog": "dog v0, dog lh v0",
}
T3 = {"l_imask": "", "l_dog": "dog v0, dog lh v0", "q_dog_leak": "dog v0, dog lh v0"}
CONTROL_FAIL = set()
N_NEW, N_T3 = 121, 121

got = {}
for f in ("lane0.out", "lane1.out", "lane2.out"):
    p = os.path.join(HERE, "logs", f)
    if not os.path.exists(p):
        continue
    for ln in io.open(p, encoding="utf-8"):
        m = re.match(r"(NEW|T5INSTR) (\S+) CRIMEP_RESULT=(\d+)/(\d+) CRIMEP_CONTROL=(\w+) (\d+) FAILING:(.*)$", ln.strip())
        if m:
            got[(m.group(1), m.group(2))] = (int(m.group(3)), int(m.group(4)), m.group(5), int(m.group(6)), S(m.group(7)))
ok = bad = 0
for tag, table, n in (("NEW", NEW, N_NEW), ("T5INSTR", T3, N_T3)):
    for mname, pred in table.items():
        k = (tag, mname)
        if k not in got:
            print("PENDING  %-8s %s" % (tag, mname))
            continue
        a, b, ctl, done, reds = got[k]
        want = S(pred)
        wctl = "FAIL" if (tag == "NEW" and mname in CONTROL_FAIL) else "OK"
        exact = reds == want and b == n and a == n - len(want) and ctl == wctl and done == 1
        ok += exact
        bad += not exact
        print("%s  %-8s %-14s %d/%d %s%s" % ("EXACT  " if exact else "DIFFERS", tag, mname, a, b, ctl,
              "" if exact else "   extra=%s missing=%s" % (sorted(reds - want), sorted(want - reds))))
print("CHECKPRED exact=%d differs=%d of %d measured (%d predicted)" % (ok, bad, ok + bad, len(NEW) + len(T3)))
