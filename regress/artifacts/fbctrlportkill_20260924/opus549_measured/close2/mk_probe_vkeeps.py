#!/usr/bin/env python3
"""ROW PROTOTYPE: the shipped 94-row probe plus ONE step and ONE row -- a PORT read right after V's last refusal, into a0
(which held 9 and is spent by then, so a read that never ran cannot pass): "V PORT keeps 7 after its later refusals".
usage: mk_probe_vkeeps.py <shipped probe> <out>"""
import io
import sys

src, dst = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8", newline="").read()
EDITS = [('           ("sw", "t9", 0, "vlast")]\n',
          '           ("sw", "t9", 0, "vlast"), ("lw", "a0", 0, None)]\n'),
         ('READS_V = ["s0", "v0", "v1"] + ["s%d" % p for p in range(1, 8)]\n',
          'READS_V = ["s0", "v0", "v1", "a0"] + ["s%d" % p for p in range(1, 8)]\n'),
         ('    row("V announce still exactly 1 after its six refusals", V["once_after"].get("vlast"), 1)\n',
          '    row("V announce still exactly 1 after its six refusals", V["once_after"].get("vlast"), 1)\n'
          '    row("V PORT keeps 7 after its later refusals", hx(V["vals"].get("a0")), "0x7")\n')]
for old, new in EDITS:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
io.open(dst, "w", encoding="utf-8", newline="").write(s)
print("written", dst)
