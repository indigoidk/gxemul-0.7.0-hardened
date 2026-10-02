#!/usr/bin/env python3
"""mk_table46.py -- render the 46-entry table FROM THE REPLAY LOGS (never transcribed): per entry, the rows each
latch state's silent decline actually reddened, the disposition, and repair 13's bucket for comparison.
Writes TABLE46.md.  Sentinel: MKTABLE46_DONE."""
import ast, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from predict46 import P, CONTROL_ROWS

src = open(os.path.join(HERE, "r17.2fe7123b.py"), encoding="utf-8").read()
ACCEPTS = ast.literal_eval(re.search(r"^ACCEPTS = (\(.*?\))\nKINDS = ACCEPTS", src, re.S | re.M).group(1))
LAB = {0x00: "REV", 0x08: "CONTROL", 0x10: "INTSTAT", 0x18: "INTMASK", 0x30: "DOG", 0x38: "TIME"}
R13 = {}
for k in (2, 5, 6, 7, 9, 18, 19, 20, 22, 24, 26, 28, 29, 30, 32, 33, 36, 37, 38, 39, 41, 42, 45):
    R13[k] = "23 p-rowed"
for k in (21, 23, 25, 27, 31, 34, 35, 46):
    R13[k] = "8 incidental"
for k in (1, 3, 4, 8, 12, 13, 16, 17, 43, 44):
    R13[k] = "10 EQUIV"
for k in (10, 11, 14, 15, 40):
    R13[k] = "5 HOST-DIAG"
TEXT = {10, 11, 14, 15}
CH = {2: "value 0x11", 5: "PROM-window redirect (pc = ra)", 6: "PROM-window redirect", 7: "PROM-window redirect",
      42: "PROM-window redirect", 9: "value 0x100", 10: "CONTROL-arm fatal() text, counted",
      11: "CONTROL-arm fatal() text, counted", 14: "CONTROL-arm fatal() text, counted",
      15: "CONTROL-arm fatal() text, counted", 18: "reassert raises IP2", 20: "reassert raises IP2",
      19: "value (INTSTAT)", 21: "value (INTSTAT high lane); SET also the reassert (IP2)",
      22: "stored INTMASK: read back, and the IP2 it enables", 23: "value (INTMASK)", 24: "stored lane, read back",
      25: "reassert raises IP2 (CONTROL rows only)", 26: "stored DOG, read back", 27: "value (DOG)",
      28: "stored lane, read back", 29: "value (DOG high lane)", 30: "stored TIME, parity", 31: "value / TIME update",
      32: "TIME update (gapped)", 33: "TIME update (gapped)", 34: "stored slot, read back -- latch SET only",
      35: "value (+0x40)", 36: "stored lane, read back", 37: "value (+0x40 high lane)", 38: "stored lane, read back",
      39: "value (DOG low lane)", 41: "value 0x11; the default-arm READ line", 45: "stored slot, read back",
      46: "value (+0x278)", 1: "derivation E-REV", 3: "derivation E-REV", 4: "derivation E-REV",
      8: "derivation E-CTL4R", 12: "derivation E-CTLW", 13: "derivation E-CTLW", 16: "derivation E-CTLW",
      17: "derivation E-CTLW", 43: "derivation E-CTLW", 44: "derivation E-CTLW",
      40: "derivation H-40: an uncounted debug() WRITE line"}


def measured(k, lt):
    t = open(os.path.join(HERE, "runs", "k%02d%s.raw" % (k, lt)), encoding="latin-1").read()
    res = re.search(r"^CRIMEP_RESULT=(\d+)/(\d+)$", t, re.M).groups()
    fl = re.search(r"^FAILING: ?(.*)$", t, re.M).group(1)
    red = [x.strip() for x in fl.split(",") if x.strip()]
    hits = sum(int(h) for h in re.findall(r"observed_hits=(\d+)", t))
    fc = re.findall(r"^REPLAY46 S(\d+) predicted_matches=\d+ FROMCACHE", t, re.M)
    ok = sorted(red) == sorted(P[k]["CS".index(lt)]) and "MISMATCH" not in t and "REPLAY46_DONE" in t
    return red, res, hits, fc, ok


def fmt(red):
    if not red:
        return "--"
    return ", ".join("`%s`%s" % (r, " [C]" if r in CONTROL_ROWS else "") for r in red)


lines = ["| # | access | label, lane | latch CLEAR: rows red under a silent decline | latch SET: rows red | "
         "disposition NOW | channel / derivation | repair 13's bucket | replay (C / S) |",
         "|---|---|---|---|---|---|---|---|---|"]
disp_count = {}
for k, (op, off, val) in enumerate(ACCEPTS, 1):
    P_ = op.endswith("P")
    bop = op[:2] if P_ else op
    ln = 8 if bop in ("sd", "ld") else 4
    acc = "`%s +0x%x%s`%s" % (bop, off, (" = 0x%04x" % val) if (off == 8 and bop[0] == "s") else "",
                              " from the PROM window" if P_ else "")
    lab = LAB.get(off, "default")
    lane = "" if ln == 8 else (", low lane" if off & 4 else ", high lane")
    if off in (0x04, 0x34):
        lab += " (%s's register)" % ("REV" if off == 4 else "DOG")
    rc, resc, hc, fcc, okc = measured(k, "C")
    rs, ress, hs, fcs, oks = measured(k, "S")
    if not rc and not rs:
        disp = "HOST-DIAGNOSTIC ONLY" if k == 40 else "EQUIVALENT"
    elif k in TEXT:
        disp = "ROWED -- host-text channel, both states"
    elif rc and rs:
        disp = "ROWED -- guest channel, both states"
    else:
        disp = "ROWED -- guest channel, latch %s ONLY" % ("SET" if rs else "CLEAR")
    disp_count[disp] = disp_count.get(disp, 0) + 1
    rep = "%s/%s %s / %s/%s %s" % (resc[0], resc[1], "exact" if okc else "DIFF", ress[0], ress[1],
                                   "exact" if oks else "DIFF")
    lines.append("| %d | %s | %s%s | %s | %s | %s | %s | %s | %s |" % (k, acc, lab, lane, fmt(rc), fmt(rs), disp,
                                                                    CH[k], R13[k], rep))
out = ["# the 46 ACCEPTS entries -- rendered from runs/k<NN><C|S>.raw by mk_table46.py", ""] + lines + [""]
out += ["| disposition NOW | entries |", "|---|---|"]
for d, n in sorted(disp_count.items(), key=lambda x: -x[1]):
    out.append("| %s | %d |" % (d, n))
open(os.path.join(HERE, "TABLE46.md"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out))
print("MKTABLE46_DONE")
