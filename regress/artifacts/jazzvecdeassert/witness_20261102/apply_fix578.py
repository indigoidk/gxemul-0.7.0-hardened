#!/usr/bin/env python3
"""apply_fix578.py <path-to-dev_jazz.c> -- the tentative #578 fix (OB-22, `jazzvecdeassert`): the jazzio access's
unconditional INTERRUPT_DEASSERT(mips_irq_3) becomes conditional on no enabled JAZZ line being pending, the same predicate
jazz_interrupt_deassert() already uses.  The find text must occur exactly once (a presence pin)."""
import io
import sys

T = chr(9)
p = sys.argv[1]
s = io.open(p, encoding="utf-8").read()
OLD = (T + "/*  This is needed by Windows NT during startup:  */" + chr(10) +
       T + "INTERRUPT_DEASSERT(d->mips_irq_3);" + chr(10))
NEW = (T + "/*  #578: this access used to deassert the CPU's IRQ3 unconditionally" + chr(10) +
       T + "    (\"needed by Windows NT during startup\").  With a second JAZZ line" + chr(10) +
       T + "    still pending, the vector read for the first dropped a level" + chr(10) +
       T + "    interrupt until some line was asserted anew (OB-22).  Deassert" + chr(10) +
       T + "    only when no enabled line is pending -- the predicate" + chr(10) +
       T + "    jazz_interrupt_deassert() uses -- so the nothing-pending case the" + chr(10) +
       T + "    old comment describes behaves as before.  */" + chr(10) +
       T + "if (!((d->int_asserted & 0x7fff) && (d->int_enable_mask & R4030_EXT_IP3)))" + chr(10) +
       T + T + "INTERRUPT_DEASSERT(d->mips_irq_3);" + chr(10))
n = s.count(OLD)
assert n == 1, n
io.open(p, "w", encoding="utf-8", newline=chr(10)).write(s.replace(OLD, NEW))
print("applied #578 to", p)
