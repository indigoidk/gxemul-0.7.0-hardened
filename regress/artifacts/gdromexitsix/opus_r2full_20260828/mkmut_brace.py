import sys
src = sys.argv[1]
s = open(src).read()
#  THE BRACE SLIP.  `#489`'s own probe header records this exact shape being
#  MEASURED to sweep an 18-row version of the TOC detector CLEAN, at the sibling
#  arm of this very switch.  `break` moves INSIDE the latch block, so the latch
#  bit gates the GUARD rather than the DIAGNOSTIC: the first bad format declines,
#  every later one FALLS THROUGH to the sector arithmetic.
old = ('\t\t\t\t    d->cmd[1]);\n'
       '\t\t\t}\n'
       '\t\t\tbreak;\n')
new = ('\t\t\t\t    d->cmd[1]);\n'
       '\t\t\t\tbreak;\n'
       '\t\t\t}\n')
n = s.count(old)
assert n == 1, "MUTANT TEXT NOT FOUND: count=%d" % n
open(src, 'w').write(s.replace(old, new, 1))
print("MUTANT M_braceA APPLIED OK")
