#!/usr/bin/env python3
"""Make fbctrl_port_probe.f2proto_d4inP.py: the prototype with D4's DATA write + NOP placed INSIDE session P, right after
the first refusal's read-back (the F2 brief's own placement), instead of in its own session R."""
import io
import sys

src, dst = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8", newline="").read()
OLD = ('    PROG_P.append((w, r, 0, "r%d" % k))\n'
       '    PROG_P.append(("lw", READ_P[k], 0, None))\n')
NEW = OLD + ('    if k == 0:\n'
             '        PROG_P += [("sw", "a1", 16, None), ("sw", "zr", 0, None), ("sw", "zr", 16, None)]\n')
assert s.count(OLD) == 1
s = s.replace(OLD, NEW)
OLD2 = '    row("announce: still exactly 1 after twelve refusals [D9]", P["once_after"].get("rtail"), 1)\n'
NEW2 = OLD2 + '    row("D4-in-P announce still 1 at the refusal after the DATA write + NOP", P["once_after"].get("r1"), 1)\n'
assert s.count(OLD2) == 1
s = s.replace(OLD2, NEW2)
io.open(dst, "w", encoding="utf-8", newline="").write(s)
print("written", dst)
