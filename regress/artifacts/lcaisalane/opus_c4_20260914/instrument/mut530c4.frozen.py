#!/usr/bin/env python3
"""mut530c4.py NAME SRC DST -- #530 closing pass 4 mutants of the FIXED dev_lca.c.
Every find-text must occur EXACTLY ONCE.  Baseline = GXEMUL-SEC working-tree src/devices/dev_lca.c."""
import io, sys

WRET = ("\t\treturn cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
        "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")
FWD  = ("\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
        "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")

M = {
    "base": [],
    # Wpure: pure fallthrough -- write arm forwards, no return; falls into read arm (phantom read).
    #        Expect CAUGHT (the c3 rows iir/kbcq).
    "Wpure": [(WRET, FWD)],
    # dataA: fallthrough fires ONLY when the stored byte is nonzero (return when byte==0).
    #        Every iir/kbcq row stores 0 -> byte==0 -> return -> no phantom -> GREEN.  Expect ESCAPE.
    "dataA": [(WRET, FWD + "\t\tif (byte == 0)\n\t\t\treturn 1;\n")],
    # dataB: fallthrough fires ONLY when the stored byte is zero (return when byte!=0).
    #        The rows store 0 -> byte==0 -> fall through -> phantom -> RED.  Expect CAUGHT (cross-control).
    "dataB": [(WRET, FWD + "\t\tif (byte != 0)\n\t\t\treturn 1;\n")],
    # L1gate: fallthrough fires ONLY at lane 1.  No lane-1 row exists (disclosed).  Expect ESCAPE.
    "L1gate": [(WRET, FWD + "\t\tif ((relative_addr & 3) != 1)\n\t\t\treturn 1;\n")],
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
