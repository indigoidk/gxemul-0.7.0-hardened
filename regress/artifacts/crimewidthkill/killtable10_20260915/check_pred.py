#!/usr/bin/env python3
"""check_pred.py -- compare kill table 10's measured red-row sets (logs/lane*.out) with PRETABLE 10's predictions,
transcribed here from PRETABLE.out (written before the table).  Prints one line per run and a tally."""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
S = lambda s: frozenset(x.strip() for x in s.split(",") if x.strip())
LA, RA = "latch x5", "rearm once"
NEW = {
    "base": "",
    "c2_pre_rev": LA + ", latch said",
    "c3_pre_ctl0": LA + ", latch said",
    "c3_pre_dog": LA + ", latch said",
    "c3_pre_dogclr": LA + ", latch said",
    "c3_pre_istat": LA + ", latch said",
    "c3_pre_revbr": LA + ", latch said",
    "d2_pre_dog0200": LA + ", latch said",
    "d4_pre_wistat": LA + ", latch said",
    "o_ctl_collide": LA + ", latch said",
    "r_pre_ctlrd": LA + ", latch said",
    "r_pre_dogbr": LA + ", latch said",
    "r_pre_istat": LA + ", latch said",
    "r_pre_revbr": LA + ", latch said",
    "x_pre_dog4w": LA + ", latch said",
    "x_pre_rev_wp": LA + ", latch said",
    "x_pre_time4r": LA + ", latch said",
    "r_byp_rev": LA,
    "C1_ctl4r": "latch said",
    "C2_chan_win": "free revP said",
    "G1_acc8_ctl": "latch said, acc ctl ld, acc ctl sd",
    "G2_acc8_istat": "latch said, acc istat ld, istw sd",
    "G3_acc4_time": "latch said",
    "G4_acc4w_rev": "latch said, revP sw pc",
    "G5_acc4w_imask": "latch said, acc imask sw",
    "G6_skip8_ctl": "acc ctl ld, acc ctl sd",
    "S_revPsw": "revP sw pc", "S_revPsd": "revP sd pc", "S_revPld": "acc8 near, revP ld pc",
    "S_ctlld": "acc ctl ld", "S_ctlsd": "acc ctl sd", "S_istld": "acc istat ld", "S_istsd": "istw sd",
    "S_istsw": "istw sw", "S_imsw": "acc imask sw", "S_timesd": "acc time sd", "S_40sw": "acc 40 lw, acc 40 sw",
    "S_40lw": "acc 40 lw",
    "W_8r": "sb keeps, sh keeps, lo keeps, hi keeps, mid keeps, imask keeps, top8 st+ld, top4 w, time lb ctl, "
            "time sb ctl, time lh ctl, time sh ctl",
    "W_8w": "lo keeps",
}
CTL_FAIL = {"W_8r"}                 # predicted CRIMEP_CONTROL=FAIL (its four time ctl rows are CONTROL rows)
N_NEW = 157

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
    good = (reds == want and b == N_NEW and ctl == ("FAIL" if mname in CTL_FAIL else "OK") and done == 1
            and a == N_NEW - len(want))
    if good:
        ok += 1
        print("EXACT    %-18s %d/%d OK" % (mname, a, b))
    else:
        bad += 1
        print("DIFFERS  %-18s %d/%d %s done=%d  extra=%s missing=%s" % (mname, a, b, ctl, done,
              sorted(reds - want), sorted(want - reds)))
print("CHECKPRED exact=%d differs=%d of %d measured (%d predicted)" % (ok, bad, ok + bad, len(NEW)))
