#!/usr/bin/env python3
"""mut530c5d.py NAME SECROOT CLONEROOT -- #530 closing pass 5, Opus seat (2nd instance): the FOUR unbuilt cells of the
eight-cell forward-count space ({write, read} x {DROP, SWAP, DUPLICATE, ADD-OTHER}).  Three files are rewritten from
GXEMUL-SEC first.  Every find-text must occur EXACTLY ONCE.
  python3 mut530c5d.py list"""
import io, sys

LCA = "src/devices/dev_lca.c"
KBC = "src/devices/dev_pckbc.c"
PIT = "src/devices/dev_8253.c"

WRET = ("\t\treturn cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
        "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")
RFWD = ("\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,\n"
        "\t    &byte, 1, MEM_READ, CACHE_NONE);\n")

M = {
    "base":  [],
    # 1  write x DROP  -- the store never reaches the bus.
    "Wdrop": [(LCA, WRET, "\t\treturn 1;\n")],
    # 2  write x SWAP  -- ONE TOKEN: the store arm performs a bus READ and never writes.
    "WXR":   [(LCA, WRET, "\t\treturn cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
                          "\t\t    relative_addr, &byte, 1, MEM_READ, CACHE_NONE);\n")],
    # 6  read x SWAP   -- ONE TOKEN: the load arm WRITES the uninitialised byte and performs no read.
    "RXW":   [(LCA, RFWD, "\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,\n"
                          "\t    &byte, 1, MEM_WRITE, CACHE_NONE);\n")],
    # 5  read x DROP   -- the read forward deleted; `byte' is uninitialised and the fill loop publishes it.
    "Rdrop": [(LCA, RFWD, "")],
}

if __name__ == "__main__":
    if sys.argv[1:2] == ["list"]:
        print(" ".join(M)); sys.exit(0)
    name, sec, clone = sys.argv[1], sys.argv[2], sys.argv[3]
    files = {}
    for f in (LCA, KBC, PIT):
        files[f] = io.open(sec + "/" + f, newline="").read()
    for f, find, repl in M[name]:
        n = files[f].count(find)
        if n != 1:
            sys.stderr.write("MUTANT %s: find-text occurs %d times in %s (want 1)\n" % (name, n, f)); sys.exit(2)
        files[f] = files[f].replace(find, repl, 1)
    for f in (LCA, KBC, PIT):
        io.open(clone + "/" + f, "w", newline="").write(files[f])
    print("APPLIED %s (%d edit(s))" % (name, len(M[name])))
