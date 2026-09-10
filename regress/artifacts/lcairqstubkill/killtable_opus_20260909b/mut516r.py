#!/usr/bin/env python3
#  #516 pass-2-repair measuring seat -- Q3 mutators (the kbc attrib WIDENING).
#  SCRATCH CLONE ONLY.  Backslashes via chr(92) per the carrier's rule.
import sys
BS = chr(92); NL = BS + "n"
L  = "/tmp/gxo516q/src/devices/dev_lca.c"
K  = "/tmp/gxo516q/src/devices/dev_pckbc.c"
which = sys.argv[1]

def edit(path, needle, repl):
    s = open(path).read()
    if s.count(needle) != 1:
        print("TEXT NOT UNIQUE/NOT FOUND (%d) in %s: %r" % (s.count(needle), path, needle[:70]))
        sys.exit(9)
    open(path, "w").write(s.replace(needle, repl))

D_GUARD_BLOCK = ('\tif (d != NULL && !(d->warned & (1u << LCA_W_IRQ_DEASSERT))) {\t/*  #516  */'
                 + chr(10) + '\t\td->warned |= 1u << LCA_W_IRQ_DEASSERT;')

if which == "M14_silentdeath":
    #  Q3 FAILABILITY TEST: the host dies INSIDE the deassert stub with NO diagnostic at all.
    #  The ASSERT announce has already printed -- and it does NOT contain the string
    #  `lca_interrupt', so the widened operand must still red.  If it greens, the widening
    #  destroyed the row's failability.
    edit(L, D_GUARD_BLOCK, '\texit(1);' + chr(10) + D_GUARD_BLOCK)
elif which == "M15_dieoutside":
    #  Q3 PURPOSE TEST: the host dies OUTSIDE dev_lca.c entirely, in dev_pckbc.c, before any
    #  interrupt edge.  Nothing lca_* is ever printed, so `kbc attrib' must red.
    edit(K, '\t\t\tdebug("[ pckbc: write to CTL:");',
            '\t\t\tdebug("[ pckbc: write to CTL:");' + chr(10) + '\t\t\texit(1);')
elif which == "M16_narrowdeassert":
    #  Q3 COVERAGE TEST: the verbatim deassert reinstatement (M2d) again, so I can re-score it
    #  with a NARROW-operand copy of the probe and measure exactly what the widening cost.
    edit(L, D_GUARD_BLOCK,
         '\tfatal("lca_interrupt_deassert: TODO' + NL + '");' + chr(10) + '\texit(1);'
         + chr(10) + D_GUARD_BLOCK)
else:
    print("unknown %s" % which); sys.exit(9)
print("APPLIED %s" % which)
