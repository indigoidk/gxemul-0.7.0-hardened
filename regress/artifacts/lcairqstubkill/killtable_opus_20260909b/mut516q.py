#!/usr/bin/env python3
#  #516 pass-2-repair measuring seat -- mutator.  Writes into a SCRATCH CLONE only.
#  Backslashes are built with chr(92) per the carrier's Bash->heredoc->Python rule.
import sys
BS = chr(92)
NL = BS + "n"                     # the two characters  \ n  , inside a C string literal
F  = "/tmp/gxo516q/src/devices/dev_lca.c"
which = sys.argv[1]

src = open(F).read()
orig = src

A_GUARD = "\tif (d != NULL && !(d->warned & (1u << LCA_W_IRQ_ASSERT))) {\t/*  #516  */"
D_GUARD = "\tif (d != NULL && !(d->warned & (1u << LCA_W_IRQ_DEASSERT))) {\t/*  #516  */"
A_ASSIGN = "\t\td->warned |= 1u << LCA_W_IRQ_ASSERT;"
D_ASSIGN = "\t\td->warned |= 1u << LCA_W_IRQ_DEASSERT;"
A_DECL = ("void lca_interrupt_assert(struct interrupt *interrupt)" + chr(10) + "{" + chr(10) +
          "\tstruct lca_data *d = (struct lca_data *) interrupt->extra;\t/*  #516  */")
D_DECL = ("void lca_interrupt_deassert(struct interrupt *interrupt)" + chr(10) + "{" + chr(10) +
          "\tstruct lca_data *d = (struct lca_data *) interrupt->extra;\t/*  #516  */")

def must(needle):
    if src.count(needle) != 1:
        print("MUTANT TEXT NOT UNIQUE/NOT FOUND (%d): %r" % (src.count(needle), needle[:60]))
        sys.exit(9)

if which == "TRACE":
    #  INSTRUMENT, not a mutant: an unconditional edge trace above each guard.
    must(A_DECL); must(D_DECL)
    trc = ('\tfatal("[ LCAEDGE %d assert warned=0x%x ]' + NL + '", ++lca_edge_seq,'
           ' d ? (int)d->warned : -1);')
    trd = ('\tfatal("[ LCAEDGE %d deassert warned=0x%x ]' + NL + '", ++lca_edge_seq,'
           ' d ? (int)d->warned : -1);')
    src = src.replace(A_DECL, A_DECL + chr(10) + trc)
    src = src.replace(D_DECL, D_DECL + chr(10) + trd)
    anchor = "/*  #516: warn-once latch bits, one per stub."
    must(anchor)
    src = src.replace(anchor, "static int lca_edge_seq = 0;\t/*  MEASURING-SEAT INSTRUMENT  */"
                      + chr(10) + chr(10) + anchor)
elif which == "M12":
    #  minimax's mutant: swap the bit in the ASSERT if-guard ONLY; assignment unchanged.
    must(A_GUARD)
    src = src.replace(A_GUARD,
        "\tif (d != NULL && !(d->warned & (1u << LCA_W_IRQ_DEASSERT))) {\t/*  M12  */")
elif which == "M12T":
    #  M12 *plus* the trace instrument, so the edges are visible under the mutant too.
    must(A_GUARD)
    src = src.replace(A_GUARD,
        "\tif (d != NULL && !(d->warned & (1u << LCA_W_IRQ_DEASSERT))) {\t/*  M12  */")
    must(A_DECL); must(D_DECL)
    trc = ('\tfatal("[ LCAEDGE %d assert warned=0x%x ]' + NL + '", ++lca_edge_seq,'
           ' d ? (int)d->warned : -1);')
    trd = ('\tfatal("[ LCAEDGE %d deassert warned=0x%x ]' + NL + '", ++lca_edge_seq,'
           ' d ? (int)d->warned : -1);')
    src = src.replace(A_DECL, A_DECL + chr(10) + trc)
    src = src.replace(D_DECL, D_DECL + chr(10) + trd)
    anchor = "/*  #516: warn-once latch bits, one per stub."
    src = src.replace(anchor, "static int lca_edge_seq = 0;\t/*  MEASURING-SEAT INSTRUMENT  */"
                      + chr(10) + chr(10) + anchor)
else:
    print("unknown: %s" % which); sys.exit(9)

if src == orig:
    print("NO CHANGE -- refusing"); sys.exit(9)
open(F, "w").write(src)
print("APPLIED %s" % which)
