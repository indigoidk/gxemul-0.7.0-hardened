#!/usr/bin/env python3
"""b10.py -- ADJUDICATION.  buckets8.py's SUFFICIENCY, with TWO apparatus errors of b9.py fixed.

b9.py had two defects, both recorded rather than hidden:
  (1) ROW-TO-SESSION OFF-BY-ONE.  row() fires AFTER session() returns, so PEND at the moment
      session i is called holds session i-1's rows.  Rows of session i live at S[i+1][1].
      VERIFIED against the packet's own naming: S[27][1] == [('rearm once',..), ('rearm surv',..)]
      and the packet calls those session 26's rows.
      *** buckets8.py is UNAFFECTED: it never reads S[i][1].  S[i][0] (accesses) is correct. ***
  (2) THE ORACLE CLASSIFIER KEYED ON A CORRELATE AND INVERTED IT.  b9 treated string `want's as
      non-value.  In this probe the DEVICE-VALUE rows are the hex-STRING wants and the announce
      COUNTS are the int wants.

The test below is buckets8.py's OWN stated criterion for why 26 and 40 are blind, applied to every
session instead of to two hardcoded ones:

    a session is VALUE-BLIND iff every row it emits is either
        (i)  an int want                -- an announce COUNT, or
        (ii) the RAM canary             -- a RAM round trip, or
        (iii) a survival/liveness token -- 'small'/'large'/'alive'/'survived'

Sentinel: B10_DONE.
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
BLIND8 = {26, 40}                       # buckets8.py's hardcoded set
RAM_CANARY = {"0x12345678", "0x12345678deadbeef", "0xdeadbeef"}
TOKENS = {"small", "large", "alive", "survived", "absent", "ok"}
S, PEND = [], []


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
NS = len(S) - 1
print("ACCEPTS entries: %d      sessions: %d" % (len(ACCEPTS), NS))

#  ---- rows of session i are at S[i+1][1].  Prove the shift against the packet's own naming.
r26 = [n for n, g, w in S[27][1]]
r26_wrong = [n for n, g, w in S[26][1]]
print("")
print("OFF-BY-ONE CONTROL   S[27][1] names = %s" % r26)
print("                     S[26][1] names = %s" % r26_wrong[:4])
print("                     packet calls session 26 `rearm once'/`rearm surv'  -> S[i+1] is correct: %s"
      % ("YES" if any(n.startswith("rearm") for n in r26) else "NO"))


def rows_of(i):
    return S[i + 1][1] if i + 1 < len(S) else []


def value_blind(i):
    rs = rows_of(i)
    if not rs:
        return True, "no rows at all"
    for name, got, want in rs:
        if isinstance(want, bool) or isinstance(want, int):
            continue                                   # announce COUNT
        w = str(want).lower()
        if w in TOKENS or w in RAM_CANARY:
            continue                                   # RAM round trip / liveness token
        return False, "device-value row %r want=%r" % (name, want)
    return True, "count/RAM rows only"


print("")
print("PER-SESSION ORACLE CLASS  (buckets8's own criterion, applied to all %d)" % NS)
blind = []
for i in range(NS):
    b, why = value_blind(i)
    if b:
        blind.append(i)
        print("  session %-3d VALUE-BLIND  (%-22s)  rows=%s"
              % (i, why, [n for n, g, w in rows_of(i)][:5]))
print("")
print("  buckets8's hardcoded BLIND set : %s" % sorted(BLIND8))
print("  derived VALUE-BLIND set        : %s" % blind)
missed = sorted(set(blind) - BLIND8)
print("  *** BLIND SESSIONS buckets8 TREATS AS SIGHTED: %s" % (missed if missed else "NONE"))
notblind = sorted(BLIND8 - set(blind))
print("  *** SESSIONS buckets8 CALLS BLIND THAT THIS TEST SAYS ARE SIGHTED: %s"
      % (notblind if notblind else "NONE"))

#  ---------------------------------------------------------------- pre/post index (buckets8 logic)
pre, post = {}, {}
for i in range(NS):
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
print("ENTRIES: buckets8 verdict vs the wider blind set")
print("%-5s %-6s %-8s %-6s %-24s %-24s %s" % ("#", "op", "off", "lab", "PRE drivers", "POST drivers", "delta"))
b8p, b8q, wp, wq = [], [], [], []
for n, (op, off, val) in enumerate(ACCEPTS, 1):
    p = sorted(set(pre.get((op, off), [])))
    q = sorted(set(post.get((op, off), [])))
    p8 = [s for s in p if s not in BLIND8]
    q8 = [s for s in q if s not in BLIND8]
    pw = [s for s in p if s not in blind]
    qw = [s for s in q if s not in blind]
    if p and not p8:
        b8p.append(n)
    if q and not q8:
        b8q.append(n)
    if p and not pw:
        wp.append(n)
    if q and not qw:
        wq.append(n)
    d = ""
    if p and p8 and not pw:
        d += " PRE-NEW"
    if q and q8 and not qw:
        d += " POST-NEW"
    if d:
        print("%-5d %-6s +0x%-5x %-6s %-24s %-24s%s" % (n, op, off, LAB.get(off, "DFL"),
                                                        str(p)[:23], str(q)[:23], d))

print("")
print("buckets8   PRE-BLIND N=%-3d %s" % (len(b8p), b8p))
print("buckets8  POST-BLIND N=%-3d %s" % (len(b8q), b8q))
print("buckets8       UNION N=%-3d %s" % (len(set(b8p) | set(b8q)), sorted(set(b8p) | set(b8q))))
print("buckets8 CARRIER OBLIGATIONS = %d pre + %d post = %d" % (len(b8p), len(b8q), len(b8p) + len(b8q)))
print("")
print("wider      PRE-BLIND N=%-3d %s" % (len(wp), wp))
print("wider     POST-BLIND N=%-3d %s" % (len(wq), wq))
print("wider          UNION N=%-3d %s" % (len(set(wp) | set(wq)), sorted(set(wp) | set(wq))))
print("wider CARRIER OBLIGATIONS = %d pre + %d post = %d" % (len(wp), len(wq), len(wp) + len(wq)))
print("")
print("NEW PRE  (blind, buckets8 missed) : %s" % sorted(set(wp) - set(b8p)))
print("NEW POST (blind, buckets8 missed) : %s" % sorted(set(wq) - set(b8q)))
print("SUFFICIENT: %s" % ("NO -- a third blind session exists and buckets8 scores its cells covered"
                          if (set(wp) - set(b8p)) or (set(wq) - set(b8q)) or missed
                          else "YES on this criterion"))
print("B10_DONE")
