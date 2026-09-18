#!/usr/bin/env python3
"""mut530c5b.py NAME SECROOT CLONEROOT -- #530 closing pass 5 (Opus), SECOND batch: the coordinator's panel findings.
Same contract as mut530c5.py: both files rewritten from GXEMUL-SEC first; every find-text must occur EXACTLY ONCE.
  python3 mut530c5b.py list"""
import io, sys

LCA = "src/devices/dev_lca.c"
KBC = "src/devices/dev_pckbc.c"

WRET = ("\t\treturn cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
        "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")
WFWD = ("\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
        "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")
FILL = "\t\tdata[i] = i == ofs? byte : 0x00;\n"

M = {
    "base":    [],
    # WW6 (glm): the write forward DUPLICATED at len 6 only.
    "WW6":     [(LCA, WRET, "\t\tif (len == 6)\n"
                            "\t\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
                            "\t\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n" + WRET)],
    # RD2post (codex): the read forward duplicated AFTER the packing loop -- the guest keeps the FIRST read's byte.
    "RD2post": [(LCA, FILL, FILL + "\n\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,\n"
                                   "\t    &byte, 1, MEM_READ, CACHE_NONE);\n")],
    # cdxZL3 (codex, exact): a post-store read iff lane 3 and the correct byte is zero, preserving the write result.
    "cdxZL3":  [(LCA, WRET, "\t\ti = cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
                            "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n"
                            "\t\tif ((relative_addr & 3) == 3 && data[ofs] == 0)\n"
                            "\t\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
                            "\t\t\t    relative_addr, &byte, 1, MEM_READ, CACHE_NONE);\n"
                            "\t\treturn i;\n")],
    # Wpure: the unconditioned x_wfallthru (table 5/6's cross-control), built here ONLY as a discriminator subject for
    #        the 8253 channel (phantom read after the store); no probe leg.
    "Wpure":   [(LCA, WRET, WFWD)],
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
