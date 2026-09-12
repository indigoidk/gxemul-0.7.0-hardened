#!/usr/bin/env python3
#  #519 PASS-2 mutator (Opus measuring seat).  Same keying convention as the round's own
#  mut519c.py so the mutants are directly comparable to M13/M14/M28.
#  Usage: mut519p2.py <path-to-clone-dev_sgi_re.c> <mutant>    exit 9 = MUTANT-TEXT-NOT-FOUND.
#
#  NOTE ON THE PRESENCE PIN, and it is an apparatus finding worth carrying: the round's own
#  mut519c.py keys `cond()' on the 3-tab "ok = 0;\n" and REPLACES it with a 4-tab "ok = 0;\n".
#  A plain substring count therefore still finds the find-string in the ALREADY-MUTATED text
#  (the 4-tab line contains the 3-tab one), so `count == 1' cannot detect a double application.
#  Latent rather than live -- every leg copies a fresh baseline -- but the pin is weaker than
#  it reads.  The find-strings here are NEWLINE-ANCHORED, which closes it; the negative control
#  in 02_dryrun.sh exercises both directions.
import sys
P, m = sys.argv[1], sys.argv[2]
T = '\t'
NL = '\n'
OK0   = NL + T*3 + "ok = 0;" + NL
GUARD = NL + T*2 + "if (ok)" + T + "/*  #519: a declined type stores nothing  */" + NL

def cond(expr):
    "the M13/M14/M28 shape: condition the decline, so where the condition is FALSE the type is PERMITTED"
    return (OK0, NL + T*3 + "if (" + expr + ")" + NL + T*4 + "ok = 0;" + NL)

def guard(expr):
    "the guard-side shape: widen the store's own guard"
    return (GUARD, NL + T*2 + "if (" + expr + ")" + T + "/*  #519: a declined type stores nothing  */" + NL)

M = {
 #  ---- replication of the round's own disclosed escape, to confirm it on my binary ----
 'M28r_permit_othernib': cond("color_mode == 0xf0 || color_mode == 0x50"),

 #  ---- THE PASS-2 CANDIDATES: the TILE-INDEX axis.  tile_nr is identically 0 at every one
 #       of the 59 rows' cells -- every vertex the probe drives is (0,0) except one (4,1),
 #       and 4>>12 == 0 (linear) and 4/tilewidth == 0 (tiled) -- so a decline conditioned on
 #       it is invisible to the instrument while permitting the store at every other tile.
 'M30_tilenrdecline':  cond("tile_nr == 0"),
 'M31_tilenrguard':    guard("ok || tile_nr"),
 'M32_tilenrxdecline': cond("tile_nr_x == 0"),
 #  ---- a DIFFERENT axis with the same property, so the finding does not rest on one name:
 #       every TILED cell sits at y == 0, and the only non-origin cell (4,1) is LINEAR.
 'M33_tiledorigin':    cond("linear || y == 0"),
}
if m not in M:
    sys.stderr.write("unknown mutant " + m + "\n"); sys.exit(8)
find, repl = M[m]
s = open(P, 'r', newline='').read()
n = s.count(find)
if n != 1:
    sys.stderr.write("MUTANT-TEXT-NOT-FOUND or AMBIGUOUS: " + m + " matches=" + str(n) + "\n")
    sys.exit(9)
open(P, 'w', newline='').write(s.replace(find, repl))
print("applied " + m + " (exactly 1 match)")
