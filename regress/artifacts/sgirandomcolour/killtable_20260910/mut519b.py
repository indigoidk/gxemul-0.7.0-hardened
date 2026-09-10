#!/usr/bin/env python3
#  #519 kill table 1 -- the MEASURING SEAT'S OWN mutants (M13, M14), written from the (d) DEPENDS-ON
#  enumeration rather than from PRETABLE section 5.  Separate file from mut519.py ON PURPOSE: mut519.py
#  is re-read by the driver between mutants, and editing a script a run keeps re-reading changes the
#  instrument mid-table.
#  Usage: mut519b.py <path-to-clone-dev_sgi_re.c> <mutant>     exit 9 = MUTANT-TEXT-NOT-FOUND
import io, sys
P, m = sys.argv[1], sys.argv[2]
T = '\t'
OK0 = T*3 + "ok = 0;\n"
M = {
 #  M13: the repair CONDITIONED on the store's own width.  `bufdepth' is a body-read lvalue -- the
 #  guarded memory_rw() reads it as the store length -- so this is the clause-(d) operand-swap form.
 #  Every declined row in the instrument drives BUFDEPTH_32 (mode 0x12f0 / 0x1250), so the cell
 #  {declined type} x {bufdepth != 4} is EMPTY.  At bufdepth 1/2/8 an unhandled type stores again.
 'M13_widthdecline': (OK0, T*3 + "if (bufdepth == 4)\n" + T*4 + "ok = 0;\n"),
 #  M14: the repair CONDITIONED on the addressing mode.  `tileptr'/`ofs' are body-read lvalues and
 #  both are computed from tlb_mode; `linear' is the switch's own partition of it.  Every row drives
 #  LIN_A (or LIN_B, which returns earlier), so the cell {declined type} x {tiled} is EMPTY.
 'M14_lineardecline': (OK0, T*3 + "if (linear)\n" + T*4 + "ok = 0;\n"),
}
if m not in M:
    print('unknown mutant', m); sys.exit(9)
s = io.open(P, encoding='utf-8', newline='').read()
old, new = M[m]
c = s.count(old)
if c != 1:
    print('MUTANT-TEXT-NOT-FOUND: %s matched %d times' % (m, c)); sys.exit(9)
io.open(P, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
print('applied', m)
