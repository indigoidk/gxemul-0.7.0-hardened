#!/usr/bin/env python3
"""mut530c5.py NAME SECROOT CLONEROOT -- #530 closing pass 5 (Opus measuring seat) mutants.
Baseline = GXEMUL-SEC working-tree src/devices/dev_lca.c (the FIXED handler, md5 8084ff07) and
src/devices/dev_pckbc.c (md5 ba7df2cb).  Every find-text must occur EXACTLY ONCE, and BOTH files are
always rewritten from SEC first, so a leg never inherits a previous leg's edit.
  python3 mut530c5.py list"""
import io, sys

LCA = "src/devices/dev_lca.c"
KBC = "src/devices/dev_pckbc.c"

WRET = ("\t\treturn cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
        "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")
WFWD = ("\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
        "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")
RFWD = ("\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,\n"
        "\t    &byte, 1, MEM_READ, CACHE_NONE);\n")
TAILW = "(len == 3 || len == 5 || len == 6 || len == 7)"

def rd_extra(cond, flag):
    return ("\tif " + cond + "\n"
            "\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,\n"
            "\t\t    &byte, 1, " + flag + ", CACHE_NONE);\n")

def wr_extra(cond):
    return ("\t\tif " + cond + "\n"
            "\t\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
            "\t\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")

M = {
    "base":    [],
    # RD2z: the contract-named RD2 (the read forward duplicated) GATED ON THE DATA -- only when the
    #       fetched byte is ZERO.  Every rowed RD2 read fetches a nonzero byte (0x55, 0x0f, 0x02, 0x21/0x31).
    "RD2z":    [(LCA, RFWD, RFWD + rd_extra("(byte == 0)", "MEM_READ"))],
    # WWtail: the write arm's forward DUPLICATED (a second STORE), at the split-TAIL widths only.
    "WWtail":  [(LCA, WRET, wr_extra(TAILW) + WRET)],
    # WWall: the write arm's forward duplicated, unconditioned.
    "WWall":   [(LCA, WRET, wr_extra("(1)") + WRET)],
    # dNZtail: x_wfallthru gated JOINTLY on a tail width and a NONZERO stored byte.
    "dNZtail": [(LCA, WRET, WFWD + "\t\tif (byte == 0 || !" + TAILW + ")\n\t\t\treturn 1;\n")],
    # W23: x_wfallthru at the single cell (2,3) -- a stub row the table built only as part of L3gate.
    "W23":     [(LCA, WRET, WFWD + "\t\tif (len != 2 || (relative_addr & 3) != 3)\n\t\t\treturn 1;\n")],
    # RWtail: the read arm followed by a phantom WRITE of the fetched byte, at the tail widths only.
    "RWtail":  [(LCA, RFWD, RFWD + rd_extra(TAILW, "MEM_WRITE"))],
    # nox: dev_pckbc.c's stub loses its counter bump -- "port 0x61 implemented" as the liveness row
    #      exists to detect.  dev_lca.c untouched.
    "nox":     [(KBC, "static int x = 0;\nx++;\nif (x&1)\n", "static int x = 0;\nif (x&1)\n")],
}

if __name__ == "__main__":
    if sys.argv[1:2] == ["list"]:
        print(" ".join(M)); sys.exit(0)
    name, sec, clone = sys.argv[1], sys.argv[2], sys.argv[3]
    files = {}
    for f in (LCA, KBC):
        files[f] = io.open(sec + "/" + f, newline="").read()
    for f, find, repl in M[name]:
        n = files[f].count(find)
        if n != 1:
            sys.stderr.write("MUTANT %s: find-text occurs %d times in %s (want 1)\n" % (name, n, f)); sys.exit(2)
        files[f] = files[f].replace(find, repl, 1)
    for f in (LCA, KBC):
        io.open(clone + "/" + f, "w", newline="").write(files[f])
    print("APPLIED %s (%d edit(s))" % (name, len(M[name])))
