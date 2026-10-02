#!/usr/bin/env python3
"""b9.py -- ADJUDICATION PASS.  Attacks buckets8.py's SUFFICIENCY.

buckets8.py's blindness test is "is the only driver session 26 or 40?"  That is a test on the
DRIVER'S IDENTITY against a HARDCODED two-element set.  It never asks whether the driver has an
ORACLE.  buckets8.py in fact COLLECTS the per-session row list (PEND -> S[i][1]) and then never
reads it -- S[i][1] appears nowhere in its analysis loop.

This tool consumes that discarded data and asks the question the main loop asked:

    CAN A THIRD SESSION WITH NO ORACLE FOR A CHANNEL PASS buckets8.py's TEST?

Two escalating tests:
  T1  ZERO-ROW DRIVERS  -- a session that emits no row at all cannot observe anything.
  T2  ORACLE-CLASS      -- classify every session's rows into the classes 26/40 were excluded
                           for (announce COUNT, RAM round trip, host-survival) versus a DEVICE
                           VALUE readback.  A session whose rows are all in the former classes is
                           blind for value purposes exactly as 26 and 40 are.

Sentinel: B9_DONE.  Read-only; writes nothing outside this scratch dir.
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
print("ACCEPTS entries: %d      sessions recorded: %d" % (len(ACCEPTS), len(S) - 1))

# ---------------------------------------------------------------- pre/post index (buckets8 logic)
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

# ---------------------------------------------------------------- T2: classify each session's rows
#  A row is a VALUE oracle if its `want' is an integer that is not a pure count/flag -- i.e. the row
#  asserts a device-supplied datum.  A row is COUNT/SURVIVAL if its want is a small int (an announce
#  tally), a bool, or one of the survival/liveness strings.
NONVALUE_WANT = ("survived", "alive", "large", "ok", True, False, None)


def classify(rowlist):
    """return (n_rows, n_value_oracle_rows)"""
    nv = 0
    for name, got, want in rowlist:
        if isinstance(want, str):
            continue                      # survived / alive / large / token rows
        if isinstance(want, bool):
            continue
        if want is None:
            continue
        if isinstance(want, int):
            #  a small non-negative integer is an announce COUNT; a wide value is a device datum
            if 0 <= want <= 16:
                continue
            nv += 1
        else:
            nv += 1
    return len(rowlist), nv


prof = {}
for i in range(len(S) - 1):
    prof[i] = classify(S[i][1])

zero_row = sorted(i for i in prof if prof[i][0] == 0)
no_value = sorted(i for i in prof if prof[i][0] > 0 and prof[i][1] == 0)
print("")
print("SESSION PROFILE  (rows, value-oracle rows)")
print("  sessions with ZERO rows            : %s" % (zero_row if zero_row else "none"))
print("  sessions with rows but NO value row: %s" % (no_value if no_value else "none"))
print("  buckets8's hardcoded BLIND set     : %s" % sorted(BLIND))
print("  26 profile=%s   40 profile=%s" % (prof.get(26), prof.get(40)))
extra = sorted(set(zero_row + no_value) - set(BLIND))
print("  *** SESSIONS AS BLIND AS 26/40 THAT buckets8 TREATS AS SIGHTED: %s" % (extra if extra else "NONE"))

# ---------------------------------------------------------------- T1/T2 applied to the 46 entries
print("")
print("ENTRIES THAT PASS buckets8's TEST BUT WHOSE ONLY NON-{26,40} DRIVERS ARE BLIND ANYWAY")
print("%-5s %-6s %-8s %-6s %-26s %-26s" % ("#", "op", "off", "label", "PRE other-drivers", "POST other-drivers"))
extra_pre, extra_post = [], []
b8_pre, b8_post = [], []
for n, (op, off, val) in enumerate(ACCEPTS, 1):
    key = (op, off)
    p = sorted(set(pre.get(key, [])))
    q = sorted(set(post.get(key, [])))
    p_other = [s for s in p if s not in BLIND]
    q_other = [s for s in q if s not in BLIND]
    if p and not p_other:
        b8_pre.append(n)
    if q and not q_other:
        b8_post.append(n)
    #  the sufficiency question: other-drivers exist, but are they all blind?
    p_sighted = [s for s in p_other if prof.get(s, (0, 0))[1] > 0]
    q_sighted = [s for s in q_other if prof.get(s, (0, 0))[1] > 0]
    flag = ""
    if p and p_other and not p_sighted:
        flag += " PRE-BLIND-MISSED"
        extra_pre.append((n, op, off, p_other))
    if q and q_other and not q_sighted:
        flag += " POST-BLIND-MISSED"
        extra_post.append((n, op, off, q_other))
    if flag:
        print("%-5d %-6s +0x%-5x %-6s %-26s %-26s%s"
              % (n, op, off, LAB.get(off, "DFL"), str(p_other)[:25], str(q_other)[:25], flag))

print("")
print("buckets8 PRE-BLIND  = %s  (N=%d)" % (b8_pre, len(b8_pre)))
print("buckets8 POST-BLIND = %s  (N=%d)" % (b8_post, len(b8_post)))
print("buckets8 UNION      = %s  (N=%d)" % (sorted(set(b8_pre) | set(b8_post)), len(set(b8_pre) | set(b8_post))))
print("CARRIER OBLIGATIONS = %d pre + %d post = %d  (an entry blind in BOTH states owes TWO)"
      % (len(b8_pre), len(b8_post), len(b8_pre) + len(b8_post)))
print("")
print("MISSED BY buckets8, PRE  : %s  (N=%d)" % ([e[0] for e in extra_pre], len(extra_pre)))
print("MISSED BY buckets8, POST : %s  (N=%d)" % ([e[0] for e in extra_post], len(extra_post)))
newpre = sorted(set(e[0] for e in extra_pre) - set(b8_pre))
newpost = sorted(set(e[0] for e in extra_post) - set(b8_post))
print("NEW ENTRIES (not already in buckets8's lists): PRE %s  POST %s" % (newpre, newpost))
print("SUFFICIENCY VERDICT: %s"
      % ("buckets8's test is INSUFFICIENT -- blind-but-unflagged cells exist"
         if (newpre or newpost or extra) else "no blind-but-unflagged cell found by these two tests"))
print("B9_DONE")
