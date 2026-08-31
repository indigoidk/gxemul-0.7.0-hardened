#!/usr/bin/env python3
#  #497: move `warned' to the END of struct sgi_re_data.
#
#  WHY THIS IS A CORRECTNESS FIX AND NOT TIDYING.  The first draft placed the new
#  field between re_linear_b and de_reg.  Measured with offsetof:
#     before the field move:  re_linear_b[32] IS warned      (NOT de_reg[0])
#     after  the field move:  re_linear_b[32] IS de_reg[0]
#  Two independent problems with the first placement:
#    1. the LINEAR site comments assert re_linear_b[32] IS de_reg[0], which the
#       insertion made FALSE -- an L4 wrong record in product code;
#    2. worse as engineering: a LINEAR_B over-run would then set WARNING LATCH
#       BITS, silencing this device's own diagnostics -- a strictly nastier
#       failure than clobbering a DE register, and a self-inflicted one.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gx497_fix_src.c"
s = open(p).read()

old = ("\tuint32_t\tre_linear_b[32];\n"
       "\n"
       "\t/*  #497: width-guard decline latches; see the enum above.  */\n"
       "\tuint32_t\twarned;\n")
assert s.count(old) == 1, "field-insertion anchor not found"
s = s.replace(old, "\tuint32_t\tre_linear_b[32];\n", 1)

tail = ("\tuint32_t\tmte_reg[DEV_SGI_MTE_LENGTH / sizeof(uint32_t)];\n"
        "};\n")
assert s.count(tail) == 1, "struct tail anchor not found"
new_tail = (
    "\tuint32_t\tmte_reg[DEV_SGI_MTE_LENGTH / sizeof(uint32_t)];\n"
    "\n"
    "\t/*\n"
    "\t *  #497: width-guard decline latches; see the enum above.\n"
    "\t *\n"
    "\t *  PLACED LAST, DELIBERATELY, AND THE ORDER IS LOAD-BEARING.\n"
    "\t *  re_linear_a/b are written at [tlbi] AND [tlbi+1] with tlbi able to\n"
    "\t *  reach 31, so index 32 of either array lands on whichever field\n"
    "\t *  FOLLOWS it.  An earlier draft of this change put `warned' between\n"
    "\t *  re_linear_b and de_reg; measured with offsetof, that made\n"
    "\t *  re_linear_b[32] alias `warned' rather than de_reg[0] -- which both\n"
    "\t *  falsified the adjacency the two LINEAR site comments cite, and made\n"
    "\t *  an over-run SET WARNING LATCH BITS and silence this device's own\n"
    "\t *  diagnostics.  Keeping the latch after mte_reg restores the\n"
    "\t *  documented adjacency: re_linear_a[32] is re_linear_b[0] and\n"
    "\t *  re_linear_b[32] is de_reg[0].\n"
    "\t */\n"
    "\tuint32_t\twarned;\n"
    "};\n")
s = s.replace(tail, new_tail, 1)
open(p, "w").write(s)
print("WARNED_MOVED_TO_END=1")
