#!/usr/bin/env python3
"""buckets8.py -- QUESTION 3, answered by a script rather than by eye.

For each of the 46 ACCEPTS entries the contract buckets (23 ROWED post-latch / 8 ALREADY PINNED / 10 EQUIVALENT /
5 HOST-DIAGNOSTIC), report which sessions drive that exact (op, offset) kind in each LATCH STATE, and -- crucially
-- whether any of those sessions is something OTHER than the two that carry no value oracle:

    session 26  `rearm once' / `rearm surv'   -- an announce COUNT and a RAM round trip.  Runs all 46 ACCEPTS
                                                 entries POST-latch and can observe none of them.
    session 40  `latch x5' / `latch surv' / `latch said'  -- two announce counts and a RAM round trip.  Runs all
                                                 46 ACCEPTS entries PRE-latch and can observe none of them.

A cell whose ONLY driver in a latch state is 26 (post) or 40 (pre) is UNOBSERVED in that state, whatever bucket the
contract puts it in.  Sentinel: BUCKETS8_DONE.
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
BLIND = {26: "rearm once/surv", 40: "latch x5/surv/said"}
S, PEND, ACC = [], [], []


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
print("ACCEPTS entries: %d" % len(ACCEPTS))

#  index every accepted CRIME access by (op, off) and latch state
pre, post = {}, {}
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
        off = b - CRIME
        win = (w & 0xffffff00) == 0xbfc05100
        key = (op + ("P" if win else ""), off)
        (pre if k < ref else post).setdefault(key, []).append(i)

print("")
print("%-5s %-6s %-8s %-6s %-30s %-30s" % ("#", "op", "off", "label", "PRE-latch sessions", "POST-latch sessions"))
open_pre, open_post = [], []
for n, (op, off, val) in enumerate(ACCEPTS, 1):
    key = (op, off)
    p = sorted(set(pre.get(key, [])))
    q = sorted(set(post.get(key, [])))
    p_other = [s for s in p if s not in BLIND]
    q_other = [s for s in q if s not in BLIND]
    lab = LAB.get(off, "DFL")
    mark = ""
    if p and not p_other:
        mark += " PRE-BLIND"
        open_pre.append((n, op, off, lab))
    if q and not q_other:
        mark += " POST-BLIND"
        open_post.append((n, op, off, lab))
    print("%-5d %-6s +0x%-5x %-6s %-30s %-30s%s"
          % (n, op, off, lab, str(p)[:29], str(q)[:29], mark))

print("")
print("=== ENTRIES DRIVEN IN THE LATCH-CLEAR STATE **ONLY** BY session 40 (`latch x5') ===")
for n, op, off, lab in open_pre:
    print("   entry %-3d %-5s +0x%-4x %s" % (n, op, off, lab))
print("N_PRE_BLIND=%d" % len(open_pre))
print("")
print("=== ENTRIES DRIVEN IN THE LATCH-SET STATE **ONLY** BY session 26 (`rearm once') ===")
for n, op, off, lab in open_post:
    print("   entry %-3d %-5s +0x%-4x %s" % (n, op, off, lab))
print("N_POST_BLIND=%d" % len(open_post))
print("BUCKETS8_DONE")
