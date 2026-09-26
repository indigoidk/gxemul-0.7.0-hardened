#!/usr/bin/env python3
"""Make shipped_cfg2.py: the SHIPPED probe with ONLY its exec line changed to a two-testmips config (machine 1 idle:
the probe's `put w`/register commands address the debugger's focused machine, machine 0, so machine 1 steps nops)."""
import io
import sys

BS = chr(92)
src, dst = sys.argv[1], sys.argv[2]
s = io.open(src, encoding="utf-8", newline="").read()
OLD = '        os.execvp(BIN, [BIN, "-V", "-E", "testmips", "-M", "64", "0x%x:%s" % (STUBADDR, stub)])\n'
body = ("machine(" + BS + "n" + BS + "tname(\"m%d\")" + BS + "n" + BS + "ttype(\"testmips\")" + BS + "n" +
        BS + "tmemory(64)" + BS + "n" + BS + "tload(\"0x%x:%s\")" + BS + "n)" + BS + "n")
NEW = ('        cfgp = stub + ".cfg"\n'
       '        with open(cfgp, "w") as cf:\n'
       '            for mi in range(2):\n'
       "                cf.write('" + body + "' % (mi, STUBADDR, stub))\n"
       '        os.execvp(BIN, [BIN, "-V", "@" + cfgp])\n')
assert s.count(OLD) == 1, "exec line not found exactly once"
io.open(dst, "w", encoding="utf-8", newline="").write(s.replace(OLD, NEW))
print("written", dst)
