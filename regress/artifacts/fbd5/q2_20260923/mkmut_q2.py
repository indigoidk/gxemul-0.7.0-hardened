#!/usr/bin/env python3
"""#545 Fable-adjudication Q2 (2026-09-23): the reset-state family.  Each mutant adds ONE conjunct to the
DIRECTION predicate that dominates an edited decline, using an operand the guarded bodies read, so a LEGAL
access from the all-zero reset state takes the decline branch.  Anchored on the case label; refuses unless
the anchor matches exactly once.  Usage: mkmut_q2.py <tree> <Q1..Q5>"""
import io, os, sys
T, M = sys.argv[1], sys.argv[2]
p = os.path.join(T, "src", "devices", "dev_footbridge.c")
MUT = {
    "Q1": ("\tcase IRQ_STATUS:\n\t\tif (writeflag == MEM_READ)\n",
           "\tcase IRQ_STATUS:\n\t\tif (writeflag == MEM_READ && d->irq_enable)\n"),
    "Q2": ("\tcase IRQ_RAW_STATUS:\n\t\tif (writeflag == MEM_READ)\n",
           "\tcase IRQ_RAW_STATUS:\n\t\tif (writeflag == MEM_READ && d->irq_status)\n"),
    "Q3": ("\tcase FIQ_STATUS:\n\t\tif (writeflag == MEM_READ)\n",
           "\tcase FIQ_STATUS:\n\t\tif (writeflag == MEM_READ && d->fiq_enable)\n"),
    "Q4": ("\tcase FIQ_RAW_STATUS:\n\t\tif (writeflag == MEM_READ)\n",
           "\tcase FIQ_RAW_STATUS:\n\t\tif (writeflag == MEM_READ && d->fiq_status)\n"),
    "Q5": ("\tcase IRQ_ENABLE_CLEAR:\n\t\tif (writeflag == MEM_WRITE) {\n",
           "\tcase IRQ_ENABLE_CLEAR:\n\t\tif (writeflag == MEM_WRITE && d->irq_enable) {\n"),
}
old, new = MUT[M]
s = io.open(p, encoding="utf-8", newline="").read()
n = s.count(old)
if n != 1:
    print("ANCHOR COUNT %d != 1 for %s -- refusing" % (n, M)); sys.exit(2)
io.open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
print("%s applied" % M)
