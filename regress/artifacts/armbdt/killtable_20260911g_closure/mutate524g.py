#!/usr/bin/env python3
"""Mutator for the #524 CLASS-CLOSURE table (table 6/g).

Every leg is built from the NAMED BASELINE -- the round's post-fix working set
GXEMUL-SEC/src/cpus/cpu_arm_instr.c -- passed in, never from a previous leg.

The two fix sites are distinguished by the MEM_READ / MEM_WRITE argument on the
continuation line, which is what makes each anchor unique.  A mutator that
cannot find its anchor EXITS NONZERO rather than writing an unmutated file:
MUTANT-TEXT-NOT-FOUND is a FAIL, which turns every find-text into a presence pin.
"""
import io, sys

if len(sys.argv) < 4:
    sys.exit("usage: mutate524g.py <leg> <target> <baseline>")
leg, tgt, baseline = sys.argv[1], sys.argv[2], sys.argv[3]
NL = "\n"

POP = ("\t\t\tif (!cpu->memory_rw(cpu, cpu->mem, addr & 0xfffffffc, data," + NL +
       "\t\t\t    sizeof(data), MEM_READ, CACHE_DATA)) {")
PUSH = ("\t\t\tif (!cpu->memory_rw(cpu, cpu->mem, addr & 0xfffffffc, data," + NL +
        "\t\t\t    sizeof(data), MEM_WRITE, CACHE_DATA)) {")


def swap(site, expr):
    """Replace the address expression at one site."""
    return site.replace("addr & 0xfffffffc", expr, 1)


#  The five measured escapes from pass C (killtable_20260911f_opus/SCORES.txt),
#  each 32/32 against the 32-row instrument.
MUT = {
    "BASE":        [],
    "M_POPP_NONE": [(POP,  swap(POP,  "(p_bit ? addr : (addr & 0xfffffffc))"))],
    "M_POPP_WEAK": [(POP,  swap(POP,  "addr & (p_bit ? 0xfffffffe : 0xfffffffc)"))],
    "M_POPW_WEAK": [(POP,  swap(POP,  "addr & (w_bit ? 0xfffffffe : 0xfffffffc)"))],
    "M_NPMASK":    [(POP,  swap(POP,  "(*np) & 0xfffffffc"))],
    "M_POPU_WEAK": [(POP,  swap(POP,  "addr & (u_bit ? 0xfffffffc : 0xfffffffe)"))],
    #  s_bit conditioning at BOTH sites, exactly as measured
    "M_SBIT_NONE": [(POP,  swap(POP,  "(s_bit ? addr : (addr & 0xfffffffc))")),
                    (PUSH, swap(PUSH, "(s_bit ? addr : (addr & 0xfffffffc))"))],
}

if leg not in MUT:
    sys.exit("ERROR: unknown leg %s" % leg)

text = io.open(baseline, encoding="utf-8").read()

#  PRESENCE PIN: both sites must exist in the baseline, every leg, including BASE.
for nm, site in (("pop", POP), ("push", PUSH)):
    if text.count(site) != 1:
        sys.exit("ERROR: %s site matched %d times in the baseline -- refusing"
                 % (nm, text.count(site)))

for old, new in MUT[leg]:
    if text.count(old) != 1:
        sys.exit("ERROR: anchor matched %d times -- refusing to guess" % text.count(old))
    text = text.replace(old, new, 1)

io.open(tgt, "w", encoding="utf-8", newline=NL).write(text)
print("%s applied (%d edit(s))" % (leg, len(MUT[leg])))
