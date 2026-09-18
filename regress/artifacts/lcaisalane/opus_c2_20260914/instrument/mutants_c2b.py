#!/usr/bin/env python3
"""mutants_c2b.py NAME SRC DST -- the PANEL MUTANTS relayed by the main loop (closing pass 2), on the FIXED dev_lca.c.
Every find-text must occur EXACTLY ONCE (a presence pin)."""
import io, sys

GUARD = "\tif (len == 0)\n\t\treturn 0;\n"
SHIFT = "\trelative_addr >>= 5;\n"
WBYTE = "\t\tbyte = data[ofs];\n"

M = {
    "base": [],
    "G1":  [(WBYTE, "\t\tbyte = data[(len == 5 && ofs == 3) ? 0 : ofs];\n")],
    "G2":  [(GUARD, "\tif (len == 0 || (len == 5 && writeflag == MEM_WRITE))\n\t\treturn 0;\n")],
    "K1":  [(SHIFT, SHIFT + "\tif (relative_addr == 0x400 && len == 4)\n\t\treturn 0;\n")],
    "C1":  [(WBYTE, "\t\tbyte = data[ofs == 2 && !data[2] ? 0 : ofs];\n")],
    "K2a": [(WBYTE, "\t\tbyte = data[(ofs == 3 && len == 4) ? 0 : ofs];\n")],
    "K2b": [(WBYTE, "\t\tbyte = data[(ofs == 3 && len == 8) ? 0 : ofs];\n")],
}

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
