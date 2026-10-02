#!/usr/bin/env python3
"""check_pred.py -- compare kill table 8's measured red-row sets (logs/lane*.out) with PRETABLE 8's predictions,
transcribed here from PRETABLE.out (written before the table).  Prints one line per run and a tally."""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
S = lambda s: frozenset(x.strip() for x in s.split(",") if x.strip())
LA, RA = "latch x5", "rearm once"
NEW = {
    "base": "", "c1_deepseek": "",
    "c2_pre_rev": LA, "c2_rearm_dog": RA, "c2_rearm_rev": RA, "c2_rearm_txt": RA,
    "c3_pre_ctl0": LA, "c3_pre_dog": LA, "c3_pre_dogclr": LA, "c3_pre_istat": LA, "c3_pre_revbr": LA,
    "lt_wset": "warm once, hi once, sh08b once",
    "nolatch": "warm once, rearm once, latch x5, imask once, imask said, istat once, istat said, time once, dog once, "
               "hi once, mid once, mid said, sh08b once, sh08b said, rev once",
    "o_ctl_collide": LA, "o_hi_gate": "gate run", "o_pa_gate": "gate run",
    "r_byp_rev": LA, "r_land_b4clr": "lo keeps", "r_pre_ctlrd": LA, "r_pre_dogbr": LA, "r_pre_istat": LA,
    "r_pre_revbr": LA, "r_rearm_ctl0": RA, "r_rearm_ctlrd": RA, "r_rearm_dogclr": RA,
    "rearm": "warm once, imask once, istat once, time once, dog once, hi once, mid once, mid said, rearm once",
    "static_od": "warm v0, gate lb v0, gate lh v0",
    "c2_kimik3": "gate lb v0, gate lh v0",
    "c3_codex_dbg": "free 2r said, free 1w said, free 2w said, free imask said, free time said",
    "c4_kimicli": RA, "c5_codex_b1": "lo keeps", "d1_rearm_dog0200": RA, "d2_pre_dog0200": LA,
    "d3_rearm_wtime": "dog once, rearm once", "d4_pre_wistat": LA, "d6_chan_len2": "free 2r said, free 2w said",
    "d7_rearm_wrev": RA,
    "x_pre_dog4w": LA, "x_rearm_rev8r": RA, "x_pre_time4r": LA, "x_rearm_ctl8w0200": RA,
    "x_chan_rev": "free rev said", "x_chan_write": "free 1w said, free 2w said", "x_rearm_defhi": RA,
    "x_pre_rev_wp": LA,
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
