#!/usr/bin/env python3
"""mk_probe48.py <frozen 47-row probe> <loop_row.py> <out> -- the PROTOTYPE 48-row probe (Q2).
Inserts loop_row.py before the `row count' identity row, raises the identity to 48 and appends
`msr loop' (dead on HEAD) to the HEAD tally.  Every anchor must occur exactly once."""
import io
import sys

src = io.open(sys.argv[1], newline="").read()
loop = io.open(sys.argv[2], newline="").read()
A = 'row("row count", len(rows) + 1, 47, "identity row (floor clause (c)): the row set is complete.")'
B = '",msr lbl,tbit,encl2,msr wide,grid msr,grid dpi,grid pop")'
for a in (A, B):
    if src.count(a) != 1:
        print("ANCHOR-NOT-UNIQUE %r count=%d" % (a[:40], src.count(a)))
        sys.exit(3)
src = src.replace(A, loop + "\n" + A.replace(", 47,", ", 48,"))
src = src.replace(B, B.replace('grid pop")', 'grid pop,msr loop")'))
io.open(sys.argv[3], "w", newline="").write(src)
print("PROBE48-WRITTEN")
