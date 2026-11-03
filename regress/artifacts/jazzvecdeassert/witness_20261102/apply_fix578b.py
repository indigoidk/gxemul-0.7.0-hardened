#!/usr/bin/env python3
"""apply_fix578b.py <path-to-dev_jazz.c> -- the FINAL #578 fix (OB-22, `jazzvecdeassert`): the jazzio tail's unconditional
INTERRUPT_DEASSERT(mips_irq_3) is DELETED and a comment stands where it was.  The deletion, not the conditional form the pass-1 brief
proposed: the conditional guard can never fire with an effect (Opus pass 1, invariant I -- the CPU line is high only while the pending
and enable predicate holds, and the assert/deassert handlers and the EXT_IMASK arm already keep it so), and the conditional text would
not compile in the est twin, whose dev_jazz.c keeps the pre-#69 predicate.  Works on SEC's and est's copies alike (the jazzio function
is byte-identical in both).  The find text must occur exactly once (a presence pin)."""
import io
import sys

T = chr(9)
NL = chr(10)
p = sys.argv[1]
s = io.open(p, encoding="utf-8").read()
OLD = (T + "/*  This is needed by Windows NT during startup:  */" + NL +
       T + "INTERRUPT_DEASSERT(d->mips_irq_3);" + NL)
NEW = (T + "/*  #578: no deassert here.  This tail used to deassert the CPU's IRQ3" + NL +
       T + "    unconditionally (\"needed by Windows NT during startup\"), so a" + NL +
       T + "    vector read taken with a second JAZZ line still pending dropped a" + NL +
       T + "    level interrupt until some line was asserted anew (OB-22).  The" + NL +
       T + "    CPU line follows jazz_interrupt_assert()/_deassert() and the" + NL +
       T + "    EXT_IMASK arm, which recompute it from the pending lines and the" + NL +
       T + "    enable mask on every change; a read has no side effect, as in the" + NL +
       T + "    tree's other interrupt controllers.  */" + NL)
n = s.count(OLD)
assert n == 1, n
io.open(p, "w", encoding="utf-8", newline=NL).write(s.replace(OLD, NEW))
print("applied #578 (deletion) to", p)
