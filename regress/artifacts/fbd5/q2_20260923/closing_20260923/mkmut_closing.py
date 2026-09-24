#!/usr/bin/env python3
"""#545 closing pass: the seats' S1..S7 readings, anchored; refuses unless the anchor matches once."""
import io, os, sys
T, M = sys.argv[1], sys.argv[2]
p = os.path.join(T, "src", "devices", "dev_footbridge.c")
TAB, NL = "\t", "\n"
def cs(label, cond, brace=""):
    return (TAB + "case " + label + ":" + NL + TAB * 2 + "if (" + cond + ")" + brace + NL)
MUT = {
    "S1": (cs("IRQ_ENABLE_SET", "writeflag == MEM_WRITE", " {"), cs("IRQ_ENABLE_SET", "writeflag == MEM_WRITE && len == 4", " {")),
    "S2": (cs("FIQ_ENABLE_SET", "writeflag == MEM_WRITE"), cs("FIQ_ENABLE_SET", "writeflag == MEM_WRITE && len == 4")),
    "S3": (cs("FIQ_ENABLE_CLEAR", "writeflag == MEM_WRITE"), cs("FIQ_ENABLE_CLEAR", "writeflag == MEM_WRITE && len == 4")),
    "S4": (TAB + "if (writeflag == MEM_WRITE)" + NL + TAB * 2 + "idata = memory_readmax64(cpu, data, len);" + NL,
           TAB + "if (writeflag == MEM_WRITE && (len == 4 || relative_addr == IRQ_ENABLE_CLEAR))" + NL + TAB * 2 + "idata = memory_readmax64(cpu, data, len);" + NL),
    "S5": (TAB + "if (writeflag == MEM_WRITE)" + NL + TAB * 2 + "idata = memory_readmax64(cpu, data, len);" + NL,
           TAB + "if (writeflag == MEM_WRITE && len == 4)" + NL + TAB * 2 + "idata = memory_readmax64(cpu, data, len);" + NL),
    "S6": (TAB * 2 + "else if (!d->warned_irq_status_w) {" + NL,
           TAB * 2 + "else if (!d->warned_irq_status_w && !(d->irq_status == 0 && d->warned_irq_raw_w)) {" + NL),
    "S7": (cs("IRQ_ENABLE_CLEAR", "writeflag == MEM_WRITE", " {"), cs("IRQ_ENABLE_CLEAR", "writeflag == MEM_WRITE && idata != 0x20", " {")),
    "S8": (cs("IRQ_STATUS", "writeflag == MEM_READ"), cs("IRQ_STATUS", "writeflag == MEM_READ && len != 8")),
    "S9": (TAB * 2 + "else if (!d->warned_irq_status_w) {" + NL,
           TAB * 2 + "else if (!d->warned_irq_status_w && len != 8) {" + NL),
    "S10": (cs("FIQ_STATUS", "writeflag == MEM_READ"), cs("FIQ_STATUS", "writeflag == MEM_READ && len != 8")),
    "S11": (TAB * 3 + "d->irq_enable &= ~idata;" + NL + TAB * 3 + "if (d->irq_status & d->irq_enable)" + NL
            + TAB * 4 + "INTERRUPT_ASSERT(d->irq);" + NL + TAB * 3 + "else" + NL + TAB * 4 + "INTERRUPT_DEASSERT(d->irq);" + NL,
            TAB * 3 + "d->irq_enable &= ~idata;" + NL + TAB * 3 + "if (d->irq_status & d->irq_enable)" + NL
            + TAB * 4 + "INTERRUPT_ASSERT(d->irq);" + NL + TAB * 3 + "else" + NL + TAB * 4 + "INTERRUPT_DEASSERT(d->irq);" + NL
            + TAB * 3 + "if (len != 4)" + NL + TAB * 4 + "return 0;" + NL),
    "S12": (cs("IRQ_ENABLE_CLEAR", "writeflag == MEM_WRITE", " {"),
            cs("IRQ_ENABLE_CLEAR", "writeflag == MEM_WRITE && (len == 4 || !d->warned_irq_clear_r)", " {")),
}
old, new = MUT[M]
s = io.open(p, encoding="utf-8", newline="").read()
n = s.count(old)
if n != 1:
    print("ANCHOR COUNT %d != 1 for %s -- refusing" % (n, M)); sys.exit(2)
io.open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
print("%s applied" % M)
