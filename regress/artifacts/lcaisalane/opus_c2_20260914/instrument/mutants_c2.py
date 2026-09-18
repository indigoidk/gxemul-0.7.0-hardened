#!/usr/bin/env python3
"""mutants_c2.py NAME SRC DST -- Opus closing-pass-2 sweep on the FIXED dev_lca.c (77-row instrument).
Every find-text must occur EXACTLY ONCE (a presence pin)."""
import io, sys

OFS   = "\tofs = (relative_addr & 3) % len;\n"
WRET  = ("\t\treturn cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
         "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")
RFWD  = ("\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,\n"
         "\t    &byte, 1, MEM_READ, CACHE_NONE);\n")

M = {
    "base": [],
    # the four split-TAIL cells (3,0) (5,0) (6,0) (7,0): position 1 instead of 0, both arms
    "t_tails": [(OFS, OFS + "\tif ((relative_addr & 3) == 0 && len > 2 && (len & 3))\n\t\tofs = 1;\n")],
    # kimi-k3's shape, re-measured: the write arm falls through into a phantom READ of the same port
    "x_wfallthru": [(WRET, "\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
                           "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")],
    # operator order swapped: (P % len) & 3 -- differs from (P & 3) % len only at the split heads/tails
    "swapmod": [(OFS, "\tofs = (relative_addr % len) & 3;\n")],
    # every len >= 2 cell rotated one position: the CHANNEL check for the whole enumerated cross in one run
    "x_rot": [(OFS, "\tofs = ((relative_addr & 3) + 1) % len;\n")],
    # return-value shapes (predicted EQUIVALENT on alphabook1: no ISA device there fails an access)
    "r_fwdret": [(RFWD, "\tif (!cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,\n"
                        "\t    &byte, 1, MEM_READ, CACHE_NONE))\n\t\treturn 0;\n")],
    "w_ret1": [(WRET, "\t\treturn 1 | cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
                      "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")],
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
