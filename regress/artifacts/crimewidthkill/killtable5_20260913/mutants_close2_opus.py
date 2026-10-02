#!/usr/bin/env python3
"""#529 SECOND closing pass (Opus seat) -- NEW mutants of dev_sgi_ip32.c not in kill table 4.
usage: mutants_c2.py <name> <file>   (edits in place; every find-text must occur EXACTLY once, else exit 1)

Hunt: #499-style symmetric cells the 111-row repair may have left open, and state-floor confirmations.
"""
import sys

GOTO = "\t\t}\n\t\tgoto crime_declined;\n\t}\n\n\tswitch (relative_addr) {\n"


def goto_with(prefix):
    return GOTO.replace("\t\tgoto crime_declined;\n", "\t\t" + prefix + "goto crime_declined;\n")


M = {
    "base": [],
    # PRIME candidate: a declined 2-byte READ >= 0x200 answers the register (leaks it).  The repair closed the
    # store-landing width symmetry (hi keeps checks sb +0x27f AND sh +0x27c) but rowed the far-block READ answer with
    # lb only (top rd v0).  So a len==2-only read-answer in the far block has no row.  #499 symmetric cell.
    "rd_hi_lh": [(GOTO, goto_with("if (writeflag == MEM_READ && len == 2 && relative_addr >= 0x200) "
                                  "odata = d->reg[relative_addr / 8]; "))],
    # CONTROL: gate the decline on SOFTINT (a field the tail's INTSTAT recompute reads -- in-function DEPENDS-ON).
    # Predicted CAUGHT by sh08 run: in CONTROL sessions SOFTINT==0, so !SOFTINT true -> ... wait, polarity below.
    # decline ONLY WHEN SOFTINT set: in sh08 SOFTINT==0 -> fall through -> CPUs stop -> sh08 run RED.
    "soft_gate": [(GOTO, goto_with("if (d->reg[CRIME_SOFTINT / sizeof(uint64_t)]) "))],
    # symmetric partner check: a declined 1-byte READ >= 0x200 answers the register (this IS o_rd_hi, caught by
    # top rd v0) -- run only if budget allows, as a positive control that the far-block read channel works.
    "rd_hi_lb": [(GOTO, goto_with("if (writeflag == MEM_READ && len == 1 && relative_addr >= 0x200) "
                                  "odata = d->reg[relative_addr / 8]; "))],
    # a declined 2-byte read answers the register at ANY offset (not just >=0x200): should be caught at named labels
    # (istat lh v0 / time lh v0 read lh and want 0). Positive control that width-narrowed read-answer is caught where
    # a row exists.
    "rd_lh_all": [(GOTO, goto_with("if (writeflag == MEM_READ && len == 2) "
                                   "odata = d->reg[relative_addr / 8]; "))],
}

name, path = sys.argv[1], sys.argv[2]
src = open(path).read()
for find, repl in M[name]:
    n = src.count(find)
    if n != 1:
        print("MUTANT_TEXT_COUNT %s = %d (want 1)" % (name, n))
        sys.exit(1)
    src = src.replace(find, repl)
open(path, "w").write(src)
print("MUTANT_APPLIED %s (%d edits)" % (name, len(M[name])))
