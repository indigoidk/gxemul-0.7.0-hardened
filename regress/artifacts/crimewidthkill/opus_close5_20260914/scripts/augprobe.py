#!/usr/bin/env python3
"""augprobe.py SRC DST -- copy the probe, adding ldP(8R REV-window) and CONTROL 0x0100 writes to ACCEPTS.
Row count is UNCHANGED (ACCEPTS feeds loops, not row() calls)."""
import io, sys
src, dst = sys.argv[1], sys.argv[2]
s = io.open(src, newline="").read()
NEEDLE = '           ("sd", 0x278, 0), ("ld", 0x278, 0))\n'
ADD = ('           ("ldP", 0x00, 0), ("sw", 0x08, 0x0100), ("sd", 0x08, 0x0100),\n'
       '           ("sd", 0x278, 0), ("ld", 0x278, 0))\n')
n = s.count(NEEDLE)
if n != 1:
    sys.stderr.write("NEEDLE occurs %d times (want 1)\n" % n); sys.exit(2)
s = s.replace(NEEDLE, ADD, 1)
io.open(dst, "w", newline="").write(s)
print("AUG written")
