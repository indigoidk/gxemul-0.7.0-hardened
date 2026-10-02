#!/usr/bin/env python3
"""b11.py -- ADJUDICATION.  buckets8.py DROPS THE VALUE AXIS.  Re-derive with it.

buckets8.py:88  `for n, (op, off, val) in enumerate(ACCEPTS, 1):'  then :89  `key = (op, off)'.
`val' is unpacked and NEVER USED (grep: one occurrence, the unpack).  ACCEPTS carries five distinct
CONTROL write values -- 0x0201 / 0x0001 / 0 / 0x0200 / 0x0100 -- at `sw +0x08' and again at
`sd +0x08'.  Ten of the 46 entries therefore collapse onto TWO keys and every one of the ten is
reported with the UNION of the five values' drivers.

This tool keys on (op, off, VALUE) for stores, recovering the stored datum from the rt register the
probe loads before the `put w'.  Loads keep the (op, off) key -- a load has no input value.

Sentinel: B11_DONE.
"""
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
BLIND8 = {26, 40}
S, PEND = [], []
RNAME = {}


def _row(name, got, want, note=""):
    PEND.append((name, got, want))


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
            op, rs, rt = w >> 26, (w >> 21) & 0x1f, (w >> 16) & 0x1f
            if op in OPC and rs in (1, 7):
                b = regs.get("at" if rs == 1 else "a3")
                sv = regs.get(RNAME.get(rt)) if OPC[op][2] == "W" else None
                if b is not None:
                    acc.append((OPC[op], b, int(m.group(1), 16), sv))
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
R = G.get("R", {})
RNAME.update({v: k for k, v in R.items()})
NS = len(S) - 1

#  the recorder ran before RNAME was populated, so redo the store-value pass now that R is known
S2 = []
for i in range(len(S)):
    S2.append(S[i])
print("ACCEPTS entries: %d   sessions: %d   register names known: %d" % (len(ACCEPTS), NS, len(RNAME)))

#  second pass: re-exec with RNAME populated so store values are captured
S[:] = []
PEND[:] = []
G2 = {"__name__": "__main__", "_rec": _rec, "_row": _row}
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, SRC, "exec"), G2)
except SystemExit:
    pass
S.append([[], list(PEND)])
NS = len(S) - 1

nsv = sum(1 for i in range(NS) for a in S[i][0] if a[0][2] == "W" and a[3] is not None)
nsw = sum(1 for i in range(NS) for a in S[i][0] if a[0][2] == "W")
print("store accesses with a recovered value: %d of %d" % (nsv, nsw))

#  ---- key collisions in ACCEPTS under buckets8's key vs a value-aware key
k8, kv = {}, {}
for n, (op, off, val) in enumerate(ACCEPTS, 1):
    k8.setdefault((op, off), []).append(n)
    kv.setdefault((op, off, val), []).append(n)
coll = {k: v for k, v in k8.items() if len(v) > 1}
print("")
print("ACCEPTS keys under buckets8's (op,off): %d   under (op,off,val): %d" % (len(k8), len(kv)))
for k, v in sorted(coll.items(), key=lambda x: str(x[0])):
    vals = [ACCEPTS[n - 1][2] for n in v]
    print("  COLLIDING %-16s entries %-24s values %s"
          % (str(k), str(v), [hex(x) for x in vals]))

#  ---------------------------------------------------------------- pre/post index, value aware
pre8, post8, prev, postv = {}, {}, {}, {}
for i in range(NS):
    acc = S[i][0]
    ref = len(acc)
    for j, ((op, ln, d), b, w, sv) in enumerate(acc):
        if ln in (1, 2) and CRIME <= b < CRIME + DEVLEN:
            ref = j
            break
    for k, ((op, ln, d), b, w, sv) in enumerate(acc):
        if ln not in (4, 8) or not (CRIME <= b < CRIME + DEVLEN):
            continue
        off = b - CRIME
        win = (w & 0xffffff00) == 0xbfc05100
        nm = op + ("P" if win else "")
        (pre8 if k < ref else post8).setdefault((nm, off), []).append(i)
        if d == "W":
            (prev if k < ref else postv).setdefault((nm, off, sv), []).append(i)
        else:
            (prev if k < ref else postv).setdefault((nm, off, 0), []).append(i)

print("")
print("%-4s %-5s %-7s %-4s %-10s %-22s %-22s %s"
      % ("#", "op", "off", "lab", "value", "PRE drivers (val-aware)", "POST drivers (val-aware)", "verdict"))
b8p, b8q, vp, vq = [], [], [], []
for n, (op, off, val) in enumerate(ACCEPTS, 1):
    p8 = [s for s in sorted(set(pre8.get((op, off), []))) if s not in BLIND8]
    q8 = [s for s in sorted(set(post8.get((op, off), []))) if s not in BLIND8]
    if pre8.get((op, off)) and not p8:
        b8p.append(n)
    if post8.get((op, off)) and not q8:
        b8q.append(n)
    P = sorted(set(prev.get((op, off, val), [])))
    Q = sorted(set(postv.get((op, off, val), [])))
    Po = [s for s in P if s not in BLIND8]
    Qo = [s for s in Q if s not in BLIND8]
    pb = (not Po)
    qb = (not Qo)
    if pb:
        vp.append(n)
    if qb:
        vq.append(n)
    verdict = ""
    if pb and n not in b8p:
        verdict += " PRE-NEW"
    if qb and n not in b8q:
        verdict += " POST-NEW"
    if verdict or n in b8p or n in b8q:
        print("%-4d %-5s +0x%-4x %-4s 0x%-8x %-22s %-22s%s"
              % (n, op, off, LAB.get(off, "DFL"), val, str(P)[:21], str(Q)[:21], verdict))

print("")
print("buckets8 (op,off)   PRE-BLIND N=%-3d %s" % (len(b8p), b8p))
print("buckets8 (op,off)  POST-BLIND N=%-3d %s" % (len(b8q), b8q))
print("buckets8 UNION N=%-3d %s" % (len(set(b8p) | set(b8q)), sorted(set(b8p) | set(b8q))))
print("buckets8 CARRIER OBLIGATIONS = %d pre + %d post = %d" % (len(b8p), len(b8q), len(b8p) + len(b8q)))
print("")
print("value-aware         PRE-BLIND N=%-3d %s" % (len(vp), vp))
print("value-aware        POST-BLIND N=%-3d %s" % (len(vq), vq))
print("value-aware UNION N=%-3d %s" % (len(set(vp) | set(vq)), sorted(set(vp) | set(vq))))
print("value-aware CARRIER OBLIGATIONS = %d pre + %d post = %d" % (len(vp), len(vq), len(vp) + len(vq)))
print("")
print("ENTRIES buckets8 SCORES COVERED THAT ARE BLIND AT THEIR OWN VALUE:  PRE %s   POST %s"
      % (sorted(set(vp) - set(b8p)), sorted(set(vq) - set(b8q))))
print("B11_DONE")
