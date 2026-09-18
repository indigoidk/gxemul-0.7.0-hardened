#!/usr/bin/env python3
"""mut530c5c.py NAME SECROOT CLONEROOT -- #530 closing pass 5, Opus seat (2nd instance): the two mutants the walled
seat predicted but never built.  THREE files are rewritten from GXEMUL-SEC first (dev_8253.c joins the set), so a
leg never inherits a previous leg's edit.  Every find-text must occur EXACTLY ONCE.
  python3 mut530c5c.py list"""
import io, sys

LCA = "src/devices/dev_lca.c"
KBC = "src/devices/dev_pckbc.c"
PIT = "src/devices/dev_8253.c"

RFWD = ("\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,\n"
        "\t    &byte, 1, MEM_READ, CACHE_NONE);\n")

M = {
    "base":  [],
    # RWall: the read arm's forward joined by an UNCONDITIONED added MEM_WRITE of the fetched byte -- the fourth cell
    #        of the forward-count class's (arm x added-direction) 2x2.  RWtail is this edit gated to len 3/5/6/7.
    "RWall": [(LCA, RFWD, RFWD + "\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,\n"
                                 "\t    &byte, 1, MEM_WRITE, CACHE_NONE);\n")],
    # noff: dev_8253.c's read/write flip-flops FROZEN (`^= 1' -> `^= 0').  The 8253 channel's mandatory-control
    #       negative control -- the analogue of `nox' for the 8042 stub.  dev_lca.c is UNTOUCHED.
    "noff":  [(PIT, "\t\t\t\td->wr_msb[relative_addr] ^= 1;\n",
                    "\t\t\t\td->wr_msb[relative_addr] ^= 0;\n"),
              (PIT, "\t\t\t\td->rd_msb[relative_addr] ^= 1;\n",
                    "\t\t\t\td->rd_msb[relative_addr] ^= 0;\n")],
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
