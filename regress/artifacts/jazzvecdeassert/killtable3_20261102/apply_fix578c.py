#!/usr/bin/env python3
"""apply_fix578c.py <path-to-dev_jazz.c> -- the FINAL #578 fix (OB-22, `jazzvecdeassert`): the jazzio tail's unconditional
INTERRUPT_DEASSERT(mips_irq_3) is DELETED and a comment stands where it was.  Same code as apply_fix578b.py; the comment is the pass-2 text, made twin-neutral at F2 (agy change 5: est keeps a per-line enable predicate, so "EXT_IMASK.IP3" was false of est)
text (Opus C3, GLM/DeepSeek/minimax/kimi Q1: every access, lines pending, the EXT_IMASK transition, "kept equal to", no claim about the
tree's other controllers).  The deletion, not the conditional form the pass-1 brief proposed: the guard can never fire with an effect
(invariant I: the line is kept equal to the pending-and-enabled predicate by its three writers), and the conditional's text would not
compile in the est twin, whose dev_jazz.c keeps the pre-#69 predicate.  Works on SEC's and est's copies alike (the jazzio function is
byte-identical in both).  The find text must occur exactly once (a presence pin)."""
import io
import sys

T = chr(9)
NL = chr(10)
p = sys.argv[1]
s = io.open(p, encoding="utf-8").read()
OLD = (T + "/*  This is needed by Windows NT during startup:  */" + NL +
       T + "INTERRUPT_DEASSERT(d->mips_irq_3);" + NL)
NEW = (T + "/*  #578: no deassert here.  This tail used to deassert the CPU's IRQ3" + NL +
       T + "    on every access (\"needed by Windows NT during startup\"), dropping" + NL +
       T + "    a level interrupt while JAZZ lines were still pending until a line" + NL +
       T + "    was asserted anew or the enable mask re-admitted it (OB-22).  The" + NL +
       T + "    CPU line is kept equal to \"a JAZZ line pending and enabled\" by" + NL +
       T + "    jazz_interrupt_assert()/_deassert() and the EXT_IMASK arm; an" + NL +
       T + "    access to this register no longer touches it.  */" + NL)
n = s.count(OLD)
assert n == 1, n
io.open(p, "w", encoding="utf-8", newline=NL).write(s.replace(OLD, NEW))
print("applied #578 (deletion, final comment) to", p)
