#!/usr/bin/env python3
#  #516 pass-2-repair measuring seat -- re-builds of the round's own mutants, so the
#  PROPOSED repair probe can be shown to lose none of their kills.  SCRATCH CLONE ONLY.
import sys
F = "/tmp/gxo516q/src/devices/dev_lca.c"
which = sys.argv[1]
s = open(F).read(); orig = s

A_GUARD  = "\tif (d != NULL && !(d->warned & (1u << LCA_W_IRQ_ASSERT))) {\t/*  #516  */"
D_GUARD  = "\tif (d != NULL && !(d->warned & (1u << LCA_W_IRQ_DEASSERT))) {\t/*  #516  */"
A_ASSIGN = "\t\td->warned |= 1u << LCA_W_IRQ_ASSERT;"
D_ASSIGN = "\t\td->warned |= 1u << LCA_W_IRQ_DEASSERT;"

def must(n):
    if s.count(n) != 1:
        print("TEXT NOT UNIQUE/NOT FOUND (%d): %r" % (s.count(n), n[:60])); sys.exit(9)

if which == "M4_sharedlatch":
    must(D_GUARD); must(D_ASSIGN)
    s = s.replace(D_GUARD, "\tif (d != NULL && !(d->warned & (1u << LCA_W_IRQ_ASSERT))) {\t/*  M4  */")
    s = s.replace(D_ASSIGN, "\t\td->warned |= 1u << LCA_W_IRQ_ASSERT;\t/*  M4  */")
elif which == "M7_deassert_assign":
    must(D_ASSIGN); s = s.replace(D_ASSIGN, "\t\td->warned = 1u << LCA_W_IRQ_DEASSERT;\t/*  M7  */")
elif which == "M8_assert_assign":
    must(A_ASSIGN); s = s.replace(A_ASSIGN, "\t\td->warned = 1u << LCA_W_IRQ_ASSERT;\t/*  M8  */")
elif which == "M9_deassert_nolatch":
    must(D_GUARD); s = s.replace(D_GUARD, "\tif (d != NULL) {\t/*  M9  */")
elif which == "M10_assert_nolatch":
    must(A_GUARD); s = s.replace(A_GUARD, "\tif (d != NULL) {\t/*  M10  */")
elif which == "M12_assertguard_swap":
    must(A_GUARD)
    s = s.replace(A_GUARD, "\tif (d != NULL && !(d->warned & (1u << LCA_W_IRQ_DEASSERT))) {\t/*  M12  */")
elif which == "M2d_deassert":
    #  clause-(b) VERBATIM reinstatement at the deassert site
    must(D_GUARD)
    s = s.replace(D_GUARD, '\tfatal("lca_interrupt_deassert: TODO' + chr(92) + 'n");' + chr(10)
                  + "\texit(1);" + chr(10) + D_GUARD)
else:
    print("unknown %s" % which); sys.exit(9)
if s == orig: print("NO CHANGE -- refusing"); sys.exit(9)
open(F, "w").write(s); print("APPLIED %s" % which)
