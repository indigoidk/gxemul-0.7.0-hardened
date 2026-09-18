#!/usr/bin/env python3
"""mutants530f.py NAME SRC DST -- #530 kill table 6 (closing pass 4's repair 5, the forward-count CLASS CLOSURE, 185
rows).  The Opus closing-pass-4 seat's mutants copied as run (mut530c4_opus.py, exec'd: Wpure dataA dataB L1gate L3gate
WT6 WTsplit R2w R2w2 RD2L0), the two the flagship ruling said were "covered by construction" and must be BUILT (RD2 gated
to lane 1 and to lane 3 -- part B, RB3), and table 5's unconditional RD2 as the read-side cross-control.  Every find-text
must occur EXACTLY ONCE."""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
_ns = {}
exec(io.open(os.path.join(HERE, "mut530c4_opus.py"), encoding="utf-8").read().split("if __name__")[0], _ns)
M = dict(_ns["M"])
RREAD, RREAD2 = _ns["RREAD"], _ns["RREAD2"]
M.update({
    "RD2L1": [(RREAD, RREAD + "\tif ((relative_addr & 3) == 1)\n" + RREAD2)],
    "RD2L3": [(RREAD, RREAD + "\tif ((relative_addr & 3) == 3)\n" + RREAD2)],
    "RD2": [(RREAD, RREAD + RREAD)],
})

if __name__ == "__main__":
    if sys.argv[1:2] == ["list"]:
        print(" ".join(M)); sys.exit(0)
    name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    s = io.open(src, newline="").read()
    for find, repl in M[name]:
        n = s.count(find)
        if n != 1:
            sys.stderr.write("MUTANT %s: find-text occurs %d times (want 1)\n" % (name, n)); sys.exit(2)
        s = s.replace(find, repl, 1)
    io.open(dst, "w", newline="").write(s)
    print("APPLIED %s (%d edit(s))" % (name, len(M[name])))
