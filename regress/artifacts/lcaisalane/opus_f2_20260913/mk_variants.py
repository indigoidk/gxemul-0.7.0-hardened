#!/usr/bin/env python3
#  lcaisalane F2 (Opus measuring seat, 2026-09-13): build the three candidate dev_lca.c files
#  from HEAD's text by EXACT replacement.  Every replacement asserts its old text occurs exactly
#  once, so a drifted HEAD refuses rather than producing a silently different variant.
#
#  Usage: mk_variants.py <HEAD dev_lca.c> <outdir>
#  Writes <outdir>/dev_lca.{A,B,C}.c.  Nothing else is touched.
import sys, os

src, out = sys.argv[1], sys.argv[2]
head = open(src, encoding="latin-1").read()

def rep(text, old, new):
    n = text.count(old)
    assert n == 1, "old text found %d times (want 1): %r" % (n, old[:60])
    return text.replace(old, new)

GUARD = (
    "\tofs = relative_addr & 3;\n"
    "\tif (ofs > len) {\n"
    "\t\tfatal(\"[ ofs=%i len=%i in lca_isa access function. \"\n"
    "\t\t    \"aborting ]\\n\", ofs, len);\n"
    "\t\texit(1);\n"
    "\t}\n")

DECL = ("DEVICE_ACCESS(lca_isa)\n{\n\tunsigned int ofs, i;\n\tuint8_t byte;\n")
DECL_D = ("DEVICE_ACCESS(lca_isa)\n{\n\tunsigned int ofs, i;\n\tuint8_t byte;\n"
          "\tstruct lca_data *d = (struct lca_data *) extra;\t/*  F2 variant  */\n")

LATCHDEF_OLD = "#define\tLCA_W_IOC_DEF_R\t7\t/*  #518: default-arm read answered with zero  */\n"
LATCHDEF_NEW = LATCHDEF_OLD + "#define\tLCA_W_ISA_LANE\t8\t/*  F2 variant: lane outside the access, declined  */\n"

def declined(pred):
    return (
        "\tofs = relative_addr & 3;\n"
        "\tif (" + pred + ") {\t/*  F2 variant  */\n"
        "\t\tif (!(d->warned & (1u << LCA_W_ISA_LANE))) {\n"
        "\t\t\td->warned |= 1u << LCA_W_ISA_LANE;\n"
        "\t\t\tfatal(\"[ lca_isa: byte lane %u does not fit a %u-byte \"\n"
        "\t\t\t    \"access; declined  (once) ]\\n\", ofs, (unsigned) len);\n"
        "\t\t}\n"
        "\t\treturn 0;\n"
        "\t}\n")

# ---- A: decline all five (ofs >= len), latched announce, return 0 both directions ----------
A = rep(head, LATCHDEF_OLD, LATCHDEF_NEW)
A = rep(A, DECL, DECL_D)
A = rep(A, GUARD, declined("ofs >= len"))

# ---- B: accept all five by folding: guard deleted, ofs = (r & 3) % len on BOTH arms --------
#  The write arm's `data[ofs % len]' is left textually as it is -- with ofs already reduced the
#  second modulo is idempotent -- so the only edit is the one the dispute is about.
B = rep(head, GUARD, "\tofs = (relative_addr & 3) % len;\t/*  F2 variant: fold, no guard  */\n")

# ---- C: decline only the three cells that exit today (ofs > len); equality cells unchanged --
C = rep(head, LATCHDEF_OLD, LATCHDEF_NEW)
C = rep(C, DECL, DECL_D)
C = rep(C, GUARD, declined("ofs > len"))

for tag, text in (("A", A), ("B", B), ("C", C)):
    # sanity: the isa handler's CODE no longer calls exit().  Check the executable line, not
    # the prose comments (lca_ioc_announce's comment quotes "fatal()+exit(1)" as history).
    isa = text.split("DEVICE_ACCESS(lca_isa)")[1].split("DEVICE_ACCESS(lca_ioc)")[0]
    assert "\texit(1);\n" not in isa, tag
    with open(os.path.join(out, "dev_lca.%s.c" % tag), "w", encoding="latin-1", newline="\n") as f:
        f.write(text)
print("MK_VARIANTS_DONE")
