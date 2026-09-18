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
    #  ---- TABLE 7: the ten-cell floor.  MUST DIE. ----
    #  E1, measured 39/39 by the pass-D seat: the PUSH half of pass C's own
    #  M_SBIT_NONE, which was built both-sites and observed only on the load side.
    "M_PUSHS_NONE":  [(PUSH, swap(PUSH, "(s_bit ? addr : (addr & 0xfffffffc))"))],
    #  The ~2 strength: every pass-C closure row sat at bit 0 CLEAR, so this
    #  escaped BY ARITHMETIC until the rows moved to residue 7.
    "M_POPP_MASK2":  [(POP,  swap(POP,  "addr & (p_bit ? 0xfffffffd : 0xfffffffc)"))],
    #  The two store modes that had NO ROW AT ALL -- p/u are one selector, and
    #  STM rows were all IA while Thumb PUSH is hardcoded DB.
    "M_PUSH_IB_WEAK":[(PUSH, swap(PUSH, "addr & ((p_bit && u_bit) ? 0xfffffffe : 0xfffffffc)"))],
    "M_PUSH_DA_WEAK":[(PUSH, swap(PUSH, "addr & ((!p_bit && !u_bit) ? 0xfffffffe : 0xfffffffc)"))],
    #  The tenth cell: i == ARM_PC flows into `value` on the store side.
    "M_PUSHPC_NONE": [(PUSH, swap(PUSH, "((regs & 0x8000) ? addr : (addr & 0xfffffffc))"))],
    #  E4: p-conditioned OVER-alignment at push -- Thumb PUSH accesses are
    #  bit2-clear, so this was invisible until the pc row put one at 0x21007.
    "M_PUSHP_OVER7": [(PUSH, swap(PUSH, "addr & (p_bit ? 0xfffffff8 : 0xfffffffc)"))],
    #  ---- DISCLOSED under clause (e).  EXPECTED TO ESCAPE.  A leg that escapes
    #  and is NOT in this list is a floor breach. ----
    "D_POPSW_WEAK":  [(POP,  swap(POP,  "addr & ((s_bit && w_bit) ? 0xfffffffe : 0xfffffffc)"))],
    "D_PUW_WEAK":    [(POP,  swap(POP,  "addr & ((p_bit && u_bit && w_bit) ? 0xfffffffe : 0xfffffffc)")),
                      (PUSH, swap(PUSH, "addr & ((p_bit && u_bit && w_bit) ? 0xfffffffe : 0xfffffffc)"))],
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
