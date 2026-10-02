#!/usr/bin/env python3
"""check_pred.py -- compare kill table 5's measured red-row sets (logs/lane*.out) with PRETABLE 5's predictions,
transcribed here from PRETABLE.out (written before the table, before the table).  Prints one line per run and a tally."""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
S = lambda s: frozenset(x.strip() for x in s.split(",") if x.strip())
IM4 = "imask lb, imask sb, imask lh, imask sh"
IS4 = "istat lb, istat sb, istat lh, istat sh"
TOP5 = "top4 anchor, top said, top4 rhi, top4 rlo, top4 w"
NEW = {
    "base": "", "dogft": "", "ctlrdft": "",
    "acc4low": TOP5, "x_mc4": TOP5,
    "x_mc8": "top8 anchor, top said, top8 st+ld, top4 rhi, top4 rlo, top4 w",
    "imaskft": IM4, "a_istat": IS4,
    "istat2": "istat lh, istat sh", "imask2": "imask lh, imask sh", "h_imask": "imask lh, imask sh", "istatsh": "istat sh",
    "remap": "top8 anchor, top4 anchor",
    "lt_len": "latch x5, sh08b once", "c_dog": "sh08b msg, sh08b run",
    "o_rearm4": "rearm once, imask once, istat once", "o_pre4": "latch x5, top said", "o_ctl_collide": "latch x5",
    "o_rd_hi": "top rd v0, top rd2 v0", "o_hi_gate": "gate run", "o_pa_gate": "gate run", "o_acc4_210": "top said",
    "lt_ctl": "sh08b once", "c_endian": "sh08b run", "istat_od1": "istat lb v0, istat lh v0",
    "c2_lbl_imask": "imask once", "c2_lbl_istat": "istat once", "c2_lbl_ctl": "sh08b once, dog once",
    "c2_dog100": "dog lh v0", "c2_reg_imask": "imask lb v0, imask lh v0", "c2_reg_istat": "istat lb v0, istat lh v0",
    "c2_reg_dog": "dog v0, dog lh v0", "c2_land_or": "imask keeps",
    "c2_rearm_dog": "rearm once", "c2_rearm_txt": "rearm once", "c2_rearm_rev": "rearm once",
    "c2_pre_irq": "imask once, istat once", "c2_pre_rev": "latch x5",
    "c2_bit7_ans": "mid lb v0, mid lh v0", "c2_bit8_land": "mid keeps", "c2_bit7_quiet": "mid said, mid once",
    "c2_bit8_ft": "mid nodflt", "c2_bit8_rearm": "mid once", "c2_bit8_latch": "mid said, mid once",
    "p_rd_hi_lh": "top rd2 v0", "p_rd_hi_lb": "top rd v0",
    "p_rd_lh_all": "lh v0, lhu v0, lh rev v0, imask lh v0, istat lh v0, time lh v0, ctl v0, dog lh v0, top rd2 v0, mid lh v0",
    "p_soft_gate": "lb nodflt, lh nodflt, sb nodflt, sh nodflt, sh08 pc, sh08 run, sb08 msg, sh08b msg, sh08b run, "
                   "lb rev pc, lh rev pc, sb rev pc, sh rev pc, time lb, time sb, time lh, time sh, hi nodflt, mid nodflt",
}
T3 = {m: "" for m in "c2_lbl_imask c2_lbl_istat c2_dog100 c2_rearm_dog c2_reg_imask c2_reg_istat c2_reg_dog c2_land_or c2_bit7_ans c2_pre_rev".split()}
T3["c2_pre_irq"] = "imask once, istat once"
T3["c2_lbl_ctl"] = "dog once"
CONTROL_FAIL = set()
N_NEW, N_T3 = 121, 111

got = {}
for f in ("lane0.out", "lane1.out", "lane2.out"):
    p = os.path.join(HERE, "logs", f)
    if not os.path.exists(p):
        continue
    for ln in io.open(p, encoding="utf-8"):
        m = re.match(r"(NEW|T4INSTR) (\S+) CRIMEP_RESULT=(\d+)/(\d+) CRIMEP_CONTROL=(\w+) (\d+) FAILING:(.*)$", ln.strip())
        if m:
            got[(m.group(1), m.group(2))] = (int(m.group(3)), int(m.group(4)), m.group(5), int(m.group(6)), S(m.group(7)))
ok = bad = 0
for tag, table, n in (("NEW", NEW, N_NEW), ("T4INSTR", T3, N_T3)):
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
