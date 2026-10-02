#!/usr/bin/env python3
"""mutants529i.py NAME SRC DST -- #529 kill table 9 (repair 11).  Imports table 8's mutator (every earlier mutant by name)
and adds the Opus fifth-closing seat's four 141/141 survivors from its mutator, copied as run (mutants_c5_opus.py, exec'd,
only the four).  Every find-text occurs EXACTLY ONCE."""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
for t in ("killtable8_20260914", "killtable7_20260913", "killtable6_20260913", "killtable5_20260913",
          "killtable4_20260913", "killtable3_20260913", "killtable2_20260913"):
    sys.path.insert(0, os.path.join(HERE, "..", t))
import mutants529h as H                                    # noqa: E402

M = dict(H.M)
_ns = {}
exec(io.open(os.path.join(HERE, "mutants_c5_opus.py"), encoding="utf-8").read().split("if __name__")[0], _ns)
M.update({k: v for k, v in _ns["M"].items()
          if k in ("P1_win8r_rearm", "P1b_win8r_preset", "P2_ctl_endi_rearm", "P2b_ctl_endi_preset")})

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
