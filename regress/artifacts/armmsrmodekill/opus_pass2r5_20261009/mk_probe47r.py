#!/usr/bin/env python3
"""mk_probe47r.py <frozen 47-row probe> <out> -- PROTOTYPE of the zero-observation L2 repair for the
latch-clear restore cells: in grid_obs(), for the DPI and POP paths only, MOVE the first polarity-2
accept and the first polarity-2 decline to the front of the session (accept first), so the site's
latch-CLEAR accept and decline both see NEW bits 31:5 = 0 against OLD bits 31:6 = 1.  The observation
MULTISET is unchanged (counts 56/52/58, every want unchanged), so grid cov's union is unchanged; only
which observations run with the latch clear changes.  The anchor must occur exactly once."""
import io
import sys

src = io.open(sys.argv[1], newline="").read()
A = ("    if path == \"pop\":                            # G4 the three non-restoring enclosing cells\n"
     "        for kind in (\"ldm_pc\", \"ldm_r0_s\", \"ldm_r0\"):\n"
     "            for pol in (1, 2):\n"
     "                add(kind, 0x13 if pol == 1 else 0x12, 0x1F, pol)\n"
     "    return obs\n")
B = A.replace("    return obs\n",
              "    if path != \"msr\":                            # OPUS PROTOTYPE: latch-CLEAR at p2\n"
              "        ia = [i for i, o in enumerate(obs) if o[0] == \"acc\" and o[2] >> 6 == 0x3FFFFFF][0]\n"
              "        acc = obs.pop(ia)\n"
              "        idd = [i for i, o in enumerate(obs) if o[0] == \"dec\" and o[2] >> 6 == 0x3FFFFFF][0]\n"
              "        obs = [acc, obs.pop(idd)] + obs\n"
              "    return obs\n")
if src.count(A) != 1:
    print("ANCHOR-NOT-UNIQUE count=%d" % src.count(A))
    sys.exit(3)
io.open(sys.argv[2], "w", newline="").write(src.replace(A, B))
print("PROBE47R-WRITTEN")
