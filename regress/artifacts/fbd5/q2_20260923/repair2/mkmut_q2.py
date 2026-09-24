#!/usr/bin/env python3
"""#545 Fable-adjudication Q2 (2026-09-23): the reset-state family.  Q1..Q5 each add ONE conjunct to the
DIRECTION predicate that dominates an edited decline, using an operand the guarded bodies read, so a LEGAL
access from the all-zero reset state takes the decline branch.  W1/W2 are CONTROLS for the wide-state axis
the repair adds (PRETABLE_Q2.out): W1 is insertion-class (a decline store on bits 8-31), W2 is B1-class (a
latch clearer in the same case's read branch keyed on bits 16-31).  Anchored; refuses unless the anchor
matches exactly once.  Usage: mkmut_q2.py <tree> <Q1..Q5|W1|W2>"""
import io, os, sys
T, M = sys.argv[1], sys.argv[2]
p = os.path.join(T, "src", "devices", "dev_footbridge.c")
TAB, NL = "\t", "\n"
MUT = {
    "Q1": (TAB + "case IRQ_STATUS:" + NL + TAB * 2 + "if (writeflag == MEM_READ)" + NL,
           TAB + "case IRQ_STATUS:" + NL + TAB * 2 + "if (writeflag == MEM_READ && d->irq_enable)" + NL),
    "Q2": (TAB + "case IRQ_RAW_STATUS:" + NL + TAB * 2 + "if (writeflag == MEM_READ)" + NL,
           TAB + "case IRQ_RAW_STATUS:" + NL + TAB * 2 + "if (writeflag == MEM_READ && d->irq_status)" + NL),
    "Q3": (TAB + "case FIQ_STATUS:" + NL + TAB * 2 + "if (writeflag == MEM_READ)" + NL,
           TAB + "case FIQ_STATUS:" + NL + TAB * 2 + "if (writeflag == MEM_READ && d->fiq_enable)" + NL),
    "Q4": (TAB + "case FIQ_RAW_STATUS:" + NL + TAB * 2 + "if (writeflag == MEM_READ)" + NL,
           TAB + "case FIQ_RAW_STATUS:" + NL + TAB * 2 + "if (writeflag == MEM_READ && d->fiq_status)" + NL),
    "Q5": (TAB + "case IRQ_ENABLE_CLEAR:" + NL + TAB * 2 + "if (writeflag == MEM_WRITE) {" + NL,
           TAB + "case IRQ_ENABLE_CLEAR:" + NL + TAB * 2 + "if (writeflag == MEM_WRITE && d->irq_enable) {" + NL),
    "W1": (TAB * 3 + "d->warned_irq_status_w = 1;" + NL,
           TAB * 3 + "d->warned_irq_status_w = 1;" + NL + TAB * 3 + "d->irq_status &= 0xffff;" + NL),
    "W2": (TAB * 2 + "if (writeflag == MEM_READ)" + NL + TAB * 3 + "odata = d->irq_status & d->irq_enable;" + NL
           + TAB * 2 + "else if (!d->warned_irq_status_w) {" + NL,
           TAB * 2 + "if (writeflag == MEM_READ) {" + NL + TAB * 3 + "odata = d->irq_status & d->irq_enable;" + NL
           + TAB * 3 + "if (d->irq_status >> 16)" + NL + TAB * 4 + "d->warned_irq_status_w = 0;" + NL
           + TAB * 2 + "} else if (!d->warned_irq_status_w) {" + NL),
}
old, new = MUT[M]
s = io.open(p, encoding="utf-8", newline="").read()
n = s.count(old)
if n != 1:
    print("ANCHOR COUNT %d != 1 for %s -- refusing" % (n, M)); sys.exit(2)
io.open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
print("%s applied" % M)
