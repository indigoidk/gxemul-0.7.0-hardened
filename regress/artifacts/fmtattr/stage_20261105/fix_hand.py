#!/usr/bin/env python3
"""fix_hand.py -- the main loop's hand fixes on top of apply_fmt.py's staged files, each an exact anchor asserted once.
  x11.c      Gemini's edit broke the call (a comma moved, an argument duplicated: `expected ')'`); rebuilt from HEAD with ONLY
             the stray comma after "This is not really\\n" removed, so the literals concatenate and %i takes the depth.
  cpu_mips.c the edit Gemini drafted did not match the source; the ASID is masked to a byte, so an (int) cast is rule 3."""
import io
import os
import subprocess

REPO = "C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC"
ST = "C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/codescan/fmtfix/stage/"
BS = chr(92)


def head(f):
    return subprocess.run(["git", "-C", REPO, "show", "HEAD:" + f], capture_output=True).stdout.decode("latin-1")


def cur(f):
    p = ST + f
    return io.open(p, encoding="latin-1", newline="").read() if os.path.exists(p) else head(f)


def put(f, t):
    os.makedirs(os.path.dirname(ST + f), exist_ok=True)
    io.open(ST + f, "w", encoding="latin-1", newline="").write(t)


f = "src/console/x11.c"
t = head(f)
old = '"color mode. This is not really' + BS + 'n",'
assert t.count(old) == 1, t.count(old)
put(f, t.replace(old, '"color mode. This is not really' + BS + 'n"'))

f = "src/cpus/cpu_mips.c"
t = cur(f)
old = "vaddr_asid, reg[COP0_ENTRYHI] & ENTRYHI_ASID);"
assert t.count(old) == 1, t.count(old)
put(f, t.replace(old, "vaddr_asid, (int)(reg[COP0_ENTRYHI] & ENTRYHI_ASID));"))
print("hand fixes staged: x11.c (from HEAD, the stray comma removed), cpu_mips.c (the ASID cast)")
