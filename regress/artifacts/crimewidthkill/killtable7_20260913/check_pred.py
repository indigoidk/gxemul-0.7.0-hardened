#!/usr/bin/env python3
"""check_pred.py -- compare kill table 7's measured red-row sets (logs/lane*.out) with PRETABLE 7's predictions,
transcribed here from PRETABLE.out (written before the table, before the table).  Prints one line per run and a tally."""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
S = lambda s: frozenset(x.strip() for x in s.split(",") if x.strip())
IM4 = "imask lb, imask sb, imask lh, imask sh"
IS4 = "istat lb, istat sb, istat lh, istat sh"
LA = "latch x5"
NEW = {
    "base": "", "dogft": "", "ctlrdft": "", "l_ctl": "", "l_time": "", "c3_soft_land": "",
    "wstore": "sb keeps, sh keeps, lo keeps, imask keeps, hi keeps, mid keeps",
    "imaskft": IM4, "a_istat": IS4,
    "istat2": "istat lh, istat sh", "imask2": "imask lh, imask sh", "h_imask": "imask lh, imask sh", "istatsh": "istat sh",
    "istat_od1": "istat lb v0, istat lh v0", "static_od": "warm v0",
    "wst_mc": "hi keeps", "o_wst_mc2": "hi keeps", "o_lt_blk": "hi once",
    "o_rearm4": "rearm once, imask once, istat once", "o_ctl_collide": LA,
    "o_hi_gate": "gate run", "o_pa_gate": "gate run",
    "lt_rng": "hi once, mid once, mid said, warm once", "lt_par": "warm once, rearm once, hi once, mid once",
    "c2_lbl_imask": "imask once", "c2_lbl_istat": "istat once", "c2_dog100": "dog lh v0",
    "c2_reg_imask": "imask lb v0, imask lh v0", "c2_reg_istat": "istat lb v0, istat lh v0", "c2_reg_dog": "dog v0, dog lh v0",
    "c2_land_or": "imask keeps", "c2_rearm_dog": "rearm once", "c2_rearm_txt": "rearm once", "c2_rearm_rev": "rearm once",
    "c2_pre_irq": "imask once, imask said, istat once, istat said, latch x5", "c2_pre_rev": LA,
    "c2_bit7_ans": "mid lb v0, mid lh v0", "c2_bit8_land": "mid keeps", "c2_bit7_quiet": "mid said",
    "c2_bit8_ft": "mid nodflt", "c2_bit8_rearm": "mid said, mid once", "c2_bit8_latch": "mid said, mid once",
    "q_istat_leak": "istat lb v0, istat lh v0", "q_istat_lane": "istat lb v0, istat lh v0",
    "q_dog_leak": "dog v0, dog lh v0", "l_imask": "imask lb v0, imask lh v0", "l_dog": "dog v0, dog lh v0",
    "c3_lat_b7": "mid once", "c3_lat_b8": "mid once",
    "c3_quiet_b1": "rev said, sh08b said, imask said, istat said, time said, dog said", "c3_quiet_imask": "imask said",
    "c3_pre_dog": LA, "c3_pre_revbr": LA, "c3_pre_istat": LA, "c3_far_and": "hi keeps",
    "c3_half_istat": "istat lb v0, istat lh v0", "c3_half_imask": "imask lb v0, imask lh v0",
    "c3_pre_ctl0": LA, "c3_pre_dogclr": LA,
    "r_rearm_ctlrd": "rearm once", "r_rearm_dogclr": "rearm once", "r_rearm_ctl0": "rearm once",
    "r_pre_istat": LA, "r_pre_revbr": LA, "r_pre_dogbr": LA, "r_byp_rev": LA, "r_byp_time": "latch x5, dog once",
    "r_ans_hi32_b5": "imask lb v0, imask lh v0, istat lb v0, istat lh v0", "r_land_b4clr": "lo keeps",
    "r_ans_ctl_lb": "ctl lb v0", "r_pre_ctlrd": LA,
}
T3 = {m: "" for m in "c3_lat_b7 c3_lat_b8 c3_quiet_b1 c3_quiet_imask c3_far_and c3_half_istat c3_half_imask".split()}
CONTROL_FAIL = set()
N_NEW, N_T3 = 131, 121

got = {}
for f in ("lane0.out", "lane1.out", "lane2.out", "lane3.out"):
    p = os.path.join(HERE, "logs", f)
    if not os.path.exists(p):
        continue
    for ln in io.open(p, encoding="utf-8"):
        m = re.match(r"(NEW|T6INSTR) (\S+) CRIMEP_RESULT=(\d+)/(\d+) CRIMEP_CONTROL=(\w+) (\d+) FAILING:(.*)$", ln.strip())
        if m:
            got[(m.group(1), m.group(2))] = (int(m.group(3)), int(m.group(4)), m.group(5), int(m.group(6)), S(m.group(7)))
ok = bad = 0
for tag, table, n in (("NEW", NEW, N_NEW), ("T6INSTR", T3, N_T3)):
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
