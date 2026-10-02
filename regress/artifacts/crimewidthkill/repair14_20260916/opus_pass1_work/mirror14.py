#!/usr/bin/env python3
"""mirror14.py -- PART A's REAL DENOMINATOR, derived rather than asserted.

The repair-14 brief says Part A must "drive every OPEN guest-visible cell in a session that does
NOT open with POST(A)", and puts the floor at 23.  23 is the count of cells ROWED POST-latch by the
`p *' sessions -- it is not the count of cells that LACK a pre-latch observer, which is what Part A
is actually buying.  This prints, per ACCEPTS entry, every PRE-latch driving session that is not
`latch x5' (40) together with THAT SESSION'S ROW NAMES, so the mirror's width is read off the probe
instead of off the bucket table.

Reuses close-8's buckets8.py machinery, WITH ONE CORRECTION: `_rec' snapshots PEND at the START
of a session, so PEND then holds the PREVIOUS session's rows -- S[i] = [accesses_i, rows_{i-1}].
A first draft of this script printed S[s][1] and its row column was shifted by one.  Verified
empirically rather than reasoned: session 40 has 55 accesses (it is `latch x5') and the names
`latch x5, latch surv, latch said' sit at index 41.  buckets8.py is UNAFFECTED -- its BLIND test
keys on the ACCESS index, not on rows, so N_PRE_BLIND=8 stands.  Sentinel: MIRROR14_DONE."""
import io
import re
import sys
import contextlib

SRC = "/mnt/c/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/crime_width_probe.py"
src = open(SRC).read().replace("t, clean = session(", "t, clean = _rec(")
src = re.sub(r"(?m)^(\s*)row\(", lambda m: m.group(1) + "_row(", src)
OPC = {0x20: ("lb", 1, "R"), 0x21: ("lh", 2, "R"), 0x23: ("lw", 4, "R"), 0x24: ("lbu", 1, "R"),
       0x25: ("lhu", 2, "R"), 0x37: ("ld", 8, "R"), 0x28: ("sb", 1, "W"), 0x29: ("sh", 2, "W"),
       0x2b: ("sw", 4, "W"), 0x3f: ("sd", 8, "W")}
CRIME, DEVLEN = 0xb4000000, 0x280
LAB = {0x00: "REV", 0x08: "CTL", 0x10: "IST", 0x18: "IMK", 0x30: "DOG", 0x38: "TIM"}
S, PEND = [], []


def _row(name, got, want, note=""):
    PEND.append(name)


def _rec(cmds, settle=1.5, spin=1.2):
    regs, acc = {}, []
    for c in cmds:
        m = re.match(r"^([a-z0-9]+)=0x([0-9a-f]+)$", c)
        if m:
            regs[m.group(1)] = int(m.group(2), 16)
            continue
        m = re.match(r"^put w 0x([0-9a-f]+), 0x([0-9a-f]{8})$", c)
        if m:
            w = int(m.group(2), 16)
            op, rs = w >> 26, (w >> 21) & 0x1f
            if op in OPC and rs in (1, 7):
                b = regs.get("at" if rs == 1 else "a3")
                if b is not None:
                    acc.append((OPC[op], b, int(m.group(1), 16)))
    S.append([acc, list(PEND)])
    del PEND[:]
    return "", True


sys.argv = ["crime_width_probe.py", "/nonexistent", "map"]
G = {"__name__": "__main__", "_rec": _rec, "_row": _row}
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, SRC, "exec"), G)
except SystemExit:
    pass
S.append([[], list(PEND)])
ACCEPTS = G.get("ACCEPTS", ())
print("ACCEPTS entries: %d      sessions: %d" % (len(ACCEPTS), len(S) - 1))

pre = {}
for i in range(len(S) - 1):
    acc = S[i][0]
    ref = len(acc)
    for j, ((op, ln, d), b, w) in enumerate(acc):
        if ln in (1, 2) and CRIME <= b < CRIME + DEVLEN:
            ref = j
            break
    for k, ((op, ln, d), b, w) in enumerate(acc):
        if ln not in (4, 8) or not (CRIME <= b < CRIME + DEVLEN):
            continue
        if k >= ref:
            continue
        win = (w & 0xffffff00) == 0xbfc05100
        pre.setdefault((op + ("P" if win else ""), b - CRIME), []).append(i)

print("")
print("PER ENTRY: the PRE-latch (latch-CLEAR) driving sessions OTHER than 40, with their rows.")
print("A blank right-hand column is a cell whose ONLY latch-CLEAR driver is `latch x5', whose three")
print("rows are an announce count, a RAM round trip and an announce text -- all blind to a SILENT decline.")
print("")
nblind = 0
for n, (op, off, val) in enumerate(ACCEPTS, 1):
    others = sorted(set(s for s in pre.get((op, off), []) if s != 40))
    lab = LAB.get(off, "DFL")
    if not others:
        nblind += 1
        print("%-4d %-5s +0x%-5x %-4s  *** NO PRE-LATCH OBSERVER OTHER THAN latch x5 ***" % (n, op, off, lab))
    else:
        for s in others:
            print("%-4d %-5s +0x%-5x %-4s  sess %-3d rows: %s"
                  % (n, op, off, lab, s, ", ".join(S[s + 1][1]) or "(none)"))
print("")
print("N_ENTRIES_WITH_NO_PRELATCH_OBSERVER=%d of %d" % (nblind, len(ACCEPTS)))
print("MIRROR14_DONE")
