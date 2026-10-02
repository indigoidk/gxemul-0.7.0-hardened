#!/usr/bin/env python3
"""check_pred.py -- compare kill table 4's measured red-row sets (logs/lane*.out) with PRETABLE 4's predictions,
transcribed here from PRETABLE.out (written 13:03, before the table).  Prints one line per run and a tally."""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
S = lambda s: frozenset(x.strip() for x in s.split(",") if x.strip())
IM4 = "imask lb, imask sb, imask lh, imask sh"
IS4 = "istat lb, istat sb, istat lh, istat sh"
TOP4 = "top4 anchor, top said, top4 rhi, top4 rlo, top4 w"
NEW = {
    "base": "", "dogft": "", "ctlrdft": "", "time_land": "",
    "len2only": "lb nodflt, sb nodflt, sb08 msg, lb rev pc, sb rev pc, %s, %s, time lb, time sb, hi nodflt" % (IM4, IS4),
    "acc8dog": "acc8 near, gate hardint, gate line, imask ctl, istat ctl, time lb ctl, time sb ctl, time lh ctl, "
               "time sh ctl, top8 anchor, top said, top8 st+ld, top4 rhi, top4 rlo, top4 w",
    "acc4low": TOP4, "x_mc4": TOP4,
    "annlow": "hi said, top said", "l_addrmask": "hi said, top said",
    "timeft": "time lb, time sb, time lh, time sh", "imaskft": IM4, "a_istat": IS4,
    "x_mc8": "top8 anchor, top said, top8 st+ld, top4 rhi, top4 rlo, top4 w",
    "istat2": "istat lh, istat sh", "imask2": "imask lh, imask sh", "time2": "time lh, time sh", "istatsh": "istat sh",
    "remap": "top8 anchor, top4 anchor", "h_imask": "imask lh, imask sh",
    "h_lbl": "imask lh, imask sh, istat lh, istat sh, time lh, time sh",
    "lt_len": "latch x5, sh08b once",
    "lt_addr": "latch x5, sh08b once, imask once, istat once, rev once, time once, dog once",
    "wst_mc": "hi keeps", "c_dog": "sh08b msg, sh08b run", "c_hrclr": "sb08 msg, sh08b msg",
    "o_rearm4": "rearm once", "o_pre4": "latch x5, top said", "o_rearm_time": "rearm once, time once",
    "o_ctl_collide": "latch x5", "o_wst_mc2": "hi keeps", "o_rd_hi": "top rd v0", "o_lt_blk": "hi once",
    "o_lt_wl": "latch x5, warm once, imask once, istat once, hi once, dog once",
    "o_wnz_lbl": "imask sb, imask lh, imask sh, istat sb, istat lh, istat sh, time sb, time sh",
    "o_hi_gate": "gate run", "o_pa_gate": "gate run", "o_acc4_210": "top said",
    "near8": "acc8 near", "lt_ctl": "sh08b once", "lt_rng": "hi once",
    "lt_par": "warm once, rearm once, hi once", "c_endian": "sh08b run",
    "c_bit1": "sb08 msg, sh08b msg, sh08b run",
    "rev_od1": "lb rev v0, lh rev v0", "istat_od1": "istat lb v0, istat lh v0", "time_od1": "time lb v0, time lh v0",
}
T3 = {m: "" for m in "near8 lt_ctl lt_rng c_endian c_bit1 rev_od1 istat_od1 time_od1 time_land".split()}
T3["lt_par"] = "warm once"
CONTROL_FAIL = {"acc8dog"}
N_NEW, N_T3 = 111, 85

got = {}
for f in ("lane0.out", "lane1.out"):
    p = os.path.join(HERE, "logs", f)
    if not os.path.exists(p):
        continue
    for ln in io.open(p, encoding="utf-8"):
        m = re.match(r"(NEW|T3INSTR) (\S+) CRIMEP_RESULT=(\d+)/(\d+) CRIMEP_CONTROL=(\w+) (\d+) FAILING:(.*)$", ln.strip())
        if m:
            got[(m.group(1), m.group(2))] = (int(m.group(3)), int(m.group(4)), m.group(5), int(m.group(6)), S(m.group(7)))
ok = bad = 0
for tag, table, n in (("NEW", NEW, N_NEW), ("T3INSTR", T3, N_T3)):
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
