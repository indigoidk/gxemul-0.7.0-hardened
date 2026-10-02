#!/usr/bin/env python3
"""check_pred.py -- compare kill table 9's measured red-row sets (logs/lane*.out) with PRETABLE 9's predictions,
transcribed here from PRETABLE.out (written before the table).  Prints one line per run and a tally."""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
S = lambda s: frozenset(x.strip() for x in s.split(",") if x.strip())
LA, RA = "latch x5", "rearm once"
NEW = {
    "base": "",
    "c2_pre_rev": LA,
    "c3_pre_ctl0": LA,
    "c3_pre_dog": LA,
    "c3_pre_dogclr": LA,
    "c3_pre_istat": LA,
    "c3_pre_revbr": LA,
    "d2_pre_dog0200": LA,
    "d4_pre_wistat": LA,
    "o_ctl_collide": LA,
    "r_byp_rev": LA,
    "r_pre_ctlrd": LA,
    "r_pre_dogbr": LA,
    "r_pre_istat": LA,
    "r_pre_revbr": LA,
    "x_pre_dog4w": LA,
    "x_pre_rev_wp": LA,
    "x_pre_time4r": LA,
    "c2_rearm_dog": RA,
    "c2_rearm_rev": RA,
    "c2_rearm_txt": RA,
    "c4_kimicli": RA,
    "d1_rearm_dog0200": RA,
    "d7_rearm_wrev": RA,
    "r_rearm_ctl0": RA,
    "r_rearm_ctlrd": RA,
    "r_rearm_dogclr": RA,
    "x_rearm_ctl8w0200": RA,
    "x_rearm_defhi": RA,
    "x_rearm_rev8r": RA,
    "d3_rearm_wtime": "dog once, rearm once",
    "nolatch": "warm once, rearm once, latch x5, imask once, imask said, istat once, istat said, time once, dog once, "
               "hi once, mid once, mid said, sh08b once, sh08b said, rev once",
    "rearm": "warm once, imask once, istat once, time once, dog once, hi once, mid once, mid said, rearm once",
    "P1_win8r_rearm": RA, "P1b_win8r_preset": LA, "P2_ctl_endi_rearm": RA, "P2b_ctl_endi_preset": LA,
}
N_NEW = 141

got = {}
for f in ("lane0.out", "lane1.out", "lane2.out", "lane3.out"):
    p = os.path.join(HERE, "logs", f)
    if not os.path.exists(p):
        continue
    for ln in io.open(p, encoding="utf-8"):
        m = re.match(r"NEW (\S+) CRIMEP_RESULT=(\d+)/(\d+) CRIMEP_CONTROL=(\w+) (\d+) FAILING:(.*)$", ln.strip())
        if m:
            got[m.group(1)] = (int(m.group(2)), int(m.group(3)), m.group(4), int(m.group(5)), S(m.group(6)))
ok = bad = 0
for mname, pred in NEW.items():
    if mname not in got:
        print("PENDING  %s" % mname)
        continue
    a, b, ctl, done, reds = got[mname]
    want = S(pred)
    good = (reds == want and b == N_NEW and ctl == "OK" and done == 1 and a == N_NEW - len(want))
    if good:
        ok += 1
        print("EXACT    %-18s %d/%d OK" % (mname, a, b))
    else:
        bad += 1
        print("DIFFERS  %-18s %d/%d %s done=%d  extra=%s missing=%s" % (mname, a, b, ctl, done,
              sorted(reds - want), sorted(want - reds)))
print("CHECKPRED exact=%d differs=%d of %d measured (%d predicted)" % (ok, bad, ok + bad, len(NEW)))
