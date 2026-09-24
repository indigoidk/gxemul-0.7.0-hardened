#!/usr/bin/env python3
"""#545: codex-dedicated V1..V10 (codex_ded_q2r.md), anchored; refuses unless the anchor matches once.
Usage: mkmut_codexv.py <tree> <V1..V10>"""
import io, os, sys
T, M = sys.argv[1], sys.argv[2]
p = os.path.join(T, "src", "devices", "dev_footbridge.c")
TAB, NL = "\t", "\n"
def cs(label, cond, brace=""):
    return (TAB + "case " + label + ":" + NL + TAB * 2 + "if (" + cond + ")" + brace + NL)
MUT = {
    "V1": (cs("IRQ_STATUS", "writeflag == MEM_READ"), cs("IRQ_STATUS", "writeflag == MEM_READ && !d->warned_irq_raw_w")),
    "V2": (cs("IRQ_RAW_STATUS", "writeflag == MEM_READ"), cs("IRQ_RAW_STATUS", "writeflag == MEM_READ && len == 4")),
    "V3": (cs("IRQ_STATUS", "writeflag == MEM_READ"), cs("IRQ_STATUS", "writeflag == MEM_READ && d->irq_enable != 0x10")),
    "V4": (cs("FIQ_ENABLE_CLEAR", "writeflag == MEM_WRITE"), cs("FIQ_ENABLE_CLEAR", "writeflag == MEM_WRITE && d->fiq_enable")),
    "V5": (cs("IRQ_ENABLE_SET", "writeflag == MEM_WRITE", " {"), cs("IRQ_ENABLE_SET", "writeflag == MEM_WRITE && d->irq_status", " {")),
    "V6": (TAB * 2 + "else if (!d->warned_irq_status_w) {" + NL, TAB * 2 + "else if (!d->warned_irq_status_w && d->irq_enable) {" + NL),
    "V7": (TAB * 2 + "} else if (!d->warned_irq_clear_r) {" + NL, TAB * 2 + "} else if (!d->warned_irq_clear_r && len == 4) {" + NL),
    "V8": (TAB * 3 + "odata = d->irq_status & d->irq_enable;" + NL, TAB * 3 + "odata = d->irq_status & d->irq_enable & 0xffff;" + NL),
    "V9": (TAB * 3 + "d->irq_enable &= ~idata;" + NL, TAB * 3 + "d->irq_enable &= ~(idata & 0xff);" + NL),
    "V10": (TAB * 3 + "d->irq_enable &= ~idata;" + NL + TAB * 3 + "if (d->irq_status & d->irq_enable)" + NL,
            TAB * 3 + "d->irq_enable &= ~idata;" + NL + TAB * 3 + "if (d->irq_status & idata)" + NL),
}
old, new = MUT[M]
s = io.open(p, encoding="utf-8", newline="").read()
n = s.count(old)
if n != 1:
    print("ANCHOR COUNT %d != 1 for %s -- refusing" % (n, M)); sys.exit(2)
io.open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
print("%s applied" % M)
