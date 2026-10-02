#!/usr/bin/env python3
"""augprobe6.py SRC DST -- copy the shipped 141-row probe and APPEND (never alter) rows, so the original 141 rows are
computed from UNCHANGED command lists:
  latch said     -- codex's proposed repair: in latch x5, the first GENUINE refusal (lh +0x06) carries its own announce
  free revP said -- a free-running refused lb at CRIME_REV issued FROM the PROM window (glm's C2)
  dg *           -- DIAGNOSTIC rows (guest-visible discriminators), one extra session each"""
import io, sys
src, dst = sys.argv[1], sys.argv[2]
s = io.open(src, newline="").read()

N1 = 'row("latch surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives all five")\n'
ADD1 = N1 + r'''row("latch said", said(t, 2, 0x6, clean), 1, "AUG: lh +0x06, latch x5's first genuine refusal: own announce")

# ==== OPUS CLOSE-6 AUGMENTATION (appended sessions; no shipped session's command list is changed) ====
A = Addr(CODE)
c = ["ra=0x%x" % RA, "at=0x%x" % CRIME, "v0=0x%x" % SENT,
     "put w 0x%x, 0x%08x" % (PROBE_PC, enc("lb", "at", "v0")),
     "put w 0x%x, 0x%08x" % (PROBE_PC + 4, OP_NOP),
     "put w 0x%x, 0x%08x" % (PROBE_PC + 8, OP_B_SELF),
     "put w 0x%x, 0x%08x" % (PROBE_PC + 12, OP_NOP),
     "pc=0x%x" % PROBE_PC, "<RUN>", "print v0"]
t, clean = session(c)
ran = t.split("continue", 1)[1] if "continue" in t else ""
row("free revP said", ran.count("unimplemented len=1 at 0x0 -- declined.  (once) ]"), 1,
    "AUG: free-running lb +0x00 FROM the PROM window")

A = Addr(CODE)
c = ["ra=0x%x" % RA]
x, _ = ld(A, "ld", CRIME + 0x08, "s0"); c += x          # 8R CONTROL (ENDIANESS 0x100, the prelude writes it)
x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x            # SOFTINT = BIT (default arm)
x, _ = ld(A, "ld", CRIME + 0x10, "s1"); c += x          # 8R INTSTAT = SOFTINT | HARDINT
x, _ = st(A, "sw", CRIME + 0x18, 0x10000000); c += x    # 4W INTMASK high half
x, _ = ld(A, "ld", CRIME + 0x18, "s2"); c += x
x, _ = ld(A, "lw", CRIME + 0x08, "s3"); c += x          # 4R CONTROL (C1's cell)
x, _ = ld(A, "lb", CRIME + 0x07, "v0"); c += x          # the session's first genuine refusal
t, clean = session(c + ["print s0", "print s1", "print s2", "print s3"])
row("dg ld ctl", pr(t, "s0"), "0x100", "DIAG: accepted ld +0x08 answers CONTROL")
row("dg ld istat", pr(t, "s1"), "0x%x" % BIT, "DIAG: accepted ld +0x10 answers INTSTAT")
row("dg sw imask", pr(t, "s2"), "0x1000000000000000", "DIAG: accepted sw +0x18 lands (ld +0x18)")
row("dg lw ctl", pr(t, "s3"), "0x0", "DIAG: accepted lw +0x08 (C1's cell) answers 0")
row("dg first said", said(t, 1, 7, clean), 1, "DIAG: lb +0x07 is the first refusal: own announce")

A = Addr(CODE)
x, _ = st(A, "sw", CRIME + 0, 0, at=PROBE_PC)
t, clean = session(["ra=0x%x" % RA] + x + AFTER)
row("dg swP pc", pr(t, "pc"), "0x%x" % RA, "DIAG: accepted sw +0x00 from the window: pc = ra")
'''
n = s.count(N1)
if n != 1:
    sys.stderr.write("N1 occurs %d times\n" % n); sys.exit(2)
s = s.replace(N1, ADD1, 1)
io.open(dst, "w", newline="").write(s)
print("AUG6 written")
