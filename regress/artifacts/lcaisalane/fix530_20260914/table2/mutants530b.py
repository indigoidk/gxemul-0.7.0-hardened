#!/usr/bin/env python3
"""mutants530b.py NAME SRC DST -- #530 kill table 2 (the pass-2 repair, 51 rows).  Imports table 1's mutator and the
Opus pass-2 seat's (exec'd from their frozen copies beside this file) and adds the panel's remaining shapes."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))

def load(path):
    ns = {}
    src = io.open(path, encoding="utf-8").read()
    exec(src.split("if __name__")[0], ns)
    return ns

T1 = load(os.path.join(HERE, "mutants530.table1.py"))
OP = load(os.path.join(HERE, "mutants_p2.opus.py"))
WBYTE, OFS = T1["WBYTE"], T1["OFS"]
EXIT = T1["EXIT"]

M = dict(T1["M"])                                            # base, m_* (table 1)
M.update({k: v for k, v in OP["M"].items() if k != "base"})  # p_* (Opus pass 2)
M.update({
    # grok, pass 2: the write arm takes position 0 for every access of len >= 4
    "g_len4w":     [(WBYTE, "\t\tbyte = data[len >= 4 ? 0 : ofs];\n")],
    # kimi-k3, pass 2: EQUIVALENT BY CONSTRUCTION -- the dead `% len' restored; the exit after the fold
    "e_deadmod":   [(WBYTE, "\t\tbyte = data[ofs % len];\n")],
    "e_exitafter": [(OFS, OFS + EXIT.replace("(relative_addr & 3)", "ofs"))],
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
