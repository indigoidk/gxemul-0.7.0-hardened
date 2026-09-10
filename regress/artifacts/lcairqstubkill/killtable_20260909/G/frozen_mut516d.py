#!/usr/bin/env python3
#  #516 table D mutator.  Applies ONE named mutant to the clone's dev_lca.c, which the driver has
#  already restored from the FIXED baseline.  Every mutant is a single edit except the two verbatim
#  reinstatements, which are licensed multi-part (floor clause (b): "however many edits the
#  historical diff took") and are SPLICED FROM A FILE so no backslash crosses a heredoc.
#
#  A mutant whose anchor is NOT FOUND is a HARD FAILURE, never a silent no-op: that turns every
#  find-text into a presence pin, so the table also proves each feature it edits still exists.
import io
import sys

path, name = sys.argv[1], sys.argv[2]
s = io.open(path, encoding='utf-8').read()

ORIG_ASSERT = ('void lca_interrupt_assert(struct interrupt *interrupt)\n'
               '{\n'
               '\tfatal("lca_interrupt_assert: TODO\\n");\n'
               '\texit(1);\n'
               '}\n')
ORIG_DEASSERT = ('void lca_interrupt_deassert(struct interrupt *interrupt)\n'
                 '{\n'
                 '\tfatal("lca_interrupt_deassert: TODO\\n");\n'
                 '\texit(1);\n'
                 '}\n')


def splice(src, signature, body):
    """Replace one whole function, signature to the first closing brace in COLUMN 0."""
    i = src.index(signature)
    end = src.index('\n}\n', i) + 3
    return src[:i] + body + src[end:]


def sub(src, old, new, why):
    assert src.count(old) == 1, 'ANCHOR %s: %d occurrences -- %s' % (why, src.count(old), why)
    return src.replace(old, new, 1)


A_GUARD = 'if (d != NULL && !(d->warned & (1u << LCA_W_IRQ_ASSERT))) {\t/*  #516  */'
D_GUARD = 'if (d != NULL && !(d->warned & (1u << LCA_W_IRQ_DEASSERT))) {\t/*  #516  */'
A_TEXT = '"[ lca: ISA interrupt assert not implemented (Alpha has no "'
D_TEXT = '"[ lca: ISA interrupt deassert not implemented (Alpha has no "'

if name == 'base':
    pass

#  ---- clause (b): VERBATIM REINSTATEMENT of the removed defect ------------------------------
elif name == 'M2_both':
    s = splice(s, 'void lca_interrupt_assert(struct interrupt *interrupt)', ORIG_ASSERT)
    s = splice(s, 'void lca_interrupt_deassert(struct interrupt *interrupt)', ORIG_DEASSERT)
elif name == 'M2d_deassert':
    #  *** THE ONE THAT ESCAPED THE SHIPPED SIX-ROW DETECTOR 6/6. ***  Clause (b) is "at EVERY
    #  fixed site", and this is the site that had no coverage at all.
    s = splice(s, 'void lca_interrupt_deassert(struct interrupt *interrupt)', ORIG_DEASSERT)
elif name == 'M2a_assert':
    s = splice(s, 'void lca_interrupt_assert(struct interrupt *interrupt)', ORIG_ASSERT)

#  ---- clause (d): the guard kept, its repair nulled -------------------------------------------
elif name == 'M3_deassertoff':
    s = sub(s, D_GUARD, 'if (0) {\t/*  M3  */', 'deassert guard')
elif name == 'M3a_assertoff':
    s = sub(s, A_GUARD, 'if (0) {\t/*  M3a  */', 'assert guard')
elif name == 'M4_sharedlatch':
    #  ONE IDENTIFIER.  The fix's own comment says the bits are separate "so the two are
    #  distinguishable"; this collapses them, which is a clause-(d) breach against that claim.
    s = sub(s, D_GUARD,
            'if (d != NULL && !(d->warned & (1u << LCA_W_IRQ_ASSERT))) {\t/*  M4  */',
            'deassert guard -> assert bit')
    s = sub(s, 'd->warned |= 1u << LCA_W_IRQ_DEASSERT;',
            'd->warned |= 1u << LCA_W_IRQ_ASSERT;', 'deassert set -> assert bit')

#  ---- the HONESTY rows: the announce fires but stops saying WHY -------------------------------
elif name == 'M5_assertdishonest':
    s = sub(s, A_TEXT, '"[ lca: ISA interrupt assert not implemented (TODO "', 'assert text')
elif name == 'M6_deassertdishonest':
    s = sub(s, D_TEXT, '"[ lca: ISA interrupt deassert not implemented (TODO "', 'deassert text')

#  ---- the LATCH rows --------------------------------------------------------------------------
elif name == 'M7_deassert_assign':
    #  `|=' -> `=' : the deassert CLEARS the assert latch, so a driver cycling IRQs re-announces
    #  forever.  floodclass reopened by one character.
    s = sub(s, 'd->warned |= 1u << LCA_W_IRQ_DEASSERT;',
            'd->warned = 1u << LCA_W_IRQ_DEASSERT;', 'deassert |= -> =')
elif name == 'M8_assert_assign':
    s = sub(s, 'd->warned |= 1u << LCA_W_IRQ_ASSERT;',
            'd->warned = 1u << LCA_W_IRQ_ASSERT;', 'assert |= -> =')
elif name == 'M9_deassert_nolatch':
    s = sub(s, D_GUARD, 'if (d != NULL) {\t/*  M9  */', 'deassert latch removed')
elif name == 'M10_assert_nolatch':
    s = sub(s, A_GUARD, 'if (d != NULL) {\t/*  M10  */', 'assert latch removed')

#  ---- THE PANEL'S OWN MUTANT (minimax, pass-2 on the repair): the MIRROR of M4. -------------
#  M4 swapped guard AND assignment on the DEASSERT side.  This swaps the GUARD ONLY, on the
#  ASSERT side, leaving the assignment intact -- so the assert latch comes to depend on the
#  DEASSERT bit.  A real defect: a driver asserting twice before any deassert re-announces.
elif name == 'M12_assertguard_swap':
    s = sub(s, A_GUARD,
            'if (d != NULL && !(d->warned & (1u << LCA_W_IRQ_DEASSERT))) {	/*  M12  */',
            'assert guard reads the DEASSERT bit')
elif name == 'M13_deassertguard_swap':
    s = sub(s, D_GUARD,
            'if (d != NULL && !(d->warned & (1u << LCA_W_IRQ_ASSERT))) {	/*  M13  */',
            'deassert guard reads the ASSERT bit')

#  ---- the ONE CELL THE PASS-2 MEASURING SEAT NAMED AS UNMEASURED --------------------------
#  `d != NULL' is a DOMINATING predicate of the diff, so it is inside the clause-(d) enumeration,
#  and no row pins it.  Probably equivalent (interrupt->extra is always the lca_data), but
#  "probably equivalent" is the assertion this project keeps having to retract -- so it is
#  MEASURED, and whatever it does is a RESULT.
elif name == 'M_nonull':
    s = sub(s, A_GUARD, 'if (!(d->warned & (1u << LCA_W_IRQ_ASSERT))) {	/*  Mnn  */',
            'assert guard drops the NULL test')
    s = sub(s, D_GUARD, 'if (!(d->warned & (1u << LCA_W_IRQ_DEASSERT))) {	/*  Mnn  */',
            'deassert guard drops the NULL test')

#  ---- clause (c): NULL MEDIUM ------------------------------------------------------------------
elif name == 'M11_null':
    s = '/*  null medium  */\n'

else:
    sys.stderr.write('unknown mutant %s\n' % name)
    sys.exit(9)

io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
print('  mutant applied: %s' % name)
