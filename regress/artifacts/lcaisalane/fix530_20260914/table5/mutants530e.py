#!/usr/bin/env python3
"""mutants530e.py NAME SRC DST -- #530 kill table 5 (closing pass 3's repair 4, 111 rows).  The Opus closing-pass-3 seat's
fallthrough-class mutants (find-texts and edits copied from opus_c3_20260914/instrument/mut530c3.py as run), the
unconditional x_wfallthru, and W5 -- the kbcq q row's own kill.  Every find-text must occur EXACTLY ONCE.  `head' is
copied by the driver."""
import io, sys

WRET  = ("\t\treturn cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
         "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")
RREAD = ("\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,\n"
         "\t    &byte, 1, MEM_READ, CACHE_NONE);\n")
BARE  = ("\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
         "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")


def gated(cond):
    """The write arm forwards, then falls into the read arm (a phantom read) UNLESS cond holds."""
    return BARE + "\t\tif (" + cond + ")\n\t\t\treturn 1;\n"


M = {
    "base": [],
    # closing pass 2's measured escape, unconditional (table 4: iir stb, iir stl)
    "x_wfallthru": [(WRET, BARE)],
    # the Opus closing-pass-3 seat's W1-W4 and RD2 (93/93 each on the 93-row probe)
    "W1": [(WRET, gated("len != 8"))],
    "W2": [(WRET, gated("len != 2"))],
    "W3": [(WRET, gated("(relative_addr & 3) != 0"))],
    "W4": [(WRET, gated("len == 1 || len == 4"))],
    "RD2": [(RREAD, RREAD + RREAD)],
    # the kbcq q row's own kill: a phantom read only after a lane-0 8-byte store
    "W5": [(WRET, gated("!((relative_addr & 3) == 0 && len == 8)"))],
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
