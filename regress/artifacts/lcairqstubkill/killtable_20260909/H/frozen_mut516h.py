#!/usr/bin/env python3
#  #516 TABLE H mutator -- the two cells the pass-3 panel found UNSWEPT in the DEPENDS-ON enumeration.
#  The 2 sites x 8 edits product has an ASSIGNMENT family with two members per site (bit swapped;
#  `|=' -> `=').  Table G measured `|=' -> `=' at both sites (M7, M8) and the bit swap at NEITHER site
#  in isolation -- M4 swapped guard AND assignment together on the deassert arm, a composite, not a
#  cell.  So "sixteen mutants cover sixteen cells" was false as accounting: two composites (M2_both,
#  M4) and one joint (M_nonull) inflated the count, and two cells were never built.  This is the
#  pass-2 diagonal collapse one level down -- there on {site} x {guard-only, guard+assignment}, here
#  on {site} x {bit-swap, form-change} -- found by four seats reading the packet's own arithmetic.
import io
import sys

path, name = sys.argv[1], sys.argv[2]
s = io.open(path, encoding='utf-8').read()


def sub(src, old, new, why):
    assert src.count(old) == 1, 'ANCHOR %s: %d occurrences' % (why, src.count(old))
    return src.replace(old, new, 1)


if name == 'base':
    pass
elif name == 'M14_assert_assignswap':
    #  the assert stub's latch-store ORs in the DEASSERT bit; guard and operator untouched.
    #  (kimi's E1, glm's cell 1.)  Predicted killed: the assert bit is never set so every assert
    #  edge announces (`assert once' = 4), and the botched bit suppresses the deassert announce
    #  (`deassert once' = 0) -- a behaviour union no measured mutant reproduces.  PREDICTED, NOT YET
    #  MEASURED, which is why this file exists.
    s = sub(s, 'd->warned |= 1u << LCA_W_IRQ_ASSERT;',
            'd->warned |= 1u << LCA_W_IRQ_DEASSERT;\t/*  M14  */', 'assert assignment -> deassert bit')
elif name == 'M15_deassert_assignswap':
    #  the deassert stub's latch-store ORs in the ASSERT bit; guard and operator untouched.
    #  (kimi's E2 in the reading where M7 is the form change -- which it is.)  Predicted killed:
    #  the deassert bit is never set, so [D]'s drain re-announces (`deassert once' = 2).
    s = sub(s, 'd->warned |= 1u << LCA_W_IRQ_DEASSERT;',
            'd->warned |= 1u << LCA_W_IRQ_ASSERT;\t/*  M15  */', 'deassert assignment -> assert bit')
else:
    sys.stderr.write('unknown mutant %s\n' % name)
    sys.exit(9)

io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
print('  mutant applied: %s' % name)
