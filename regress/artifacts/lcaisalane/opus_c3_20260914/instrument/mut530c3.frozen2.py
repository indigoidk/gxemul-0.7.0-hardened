#!/usr/bin/env python3
"""mut530c3.py NAME SRC DST -- #530 closing pass 3 mutants applied to the FIXED dev_lca.c.
Every find-text must occur EXACTLY ONCE.  Baseline = GXEMUL-SEC working-tree src/devices/dev_lca.c."""
import io, sys

SHIFT = "\trelative_addr >>= 5;\n"
GUARD = "\tif (len == 0)\n\t\treturn 0;\n"
OFS   = "\tofs = (relative_addr & 3) % len;\n"
WBYTE = "\t\tbyte = data[ofs];\n"
WRET  = ("\t\treturn cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
         "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")
RREAD = ("\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,\n"
         "\t    &byte, 1, MEM_READ, CACHE_NONE);\n")

# W1: write arm forwards, then falls into read arm ONLY for len==8 stores (phantom read at len 8)
W1 = ("\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
      "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n"
      "\t\tif (len != 8)\n\t\t\treturn 1;\n")
# W2: same, phantom read only for len==2 stores
W2 = ("\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
      "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n"
      "\t\tif (len != 2)\n\t\t\treturn 1;\n")

M = {
    "base": [],
    "W1":   [(WRET, W1)],
    "W2":   [(WRET, W2)],
    # D1 / deepseek: data-keyed forward on the write arm (the disclosed data class, general form)
    "D1":   [(WBYTE, "\t\tbyte = data[ofs] ? data[ofs] : data[0];\n")],
    # H1a: keyed on the POST-shift low 5 bits (== port & 0x1f); 0x1c is lane 0 so forcing ofs=0 is a no-op
    "H1a":  [(OFS, OFS + "\tif ((relative_addr & 0x1f) == 0x1c)\n\t\tofs = 0;\n")],
    # H1b: keyed on the PRE-shift discarded low 5 bits (the sparse byte offset) -- the lcaisasize class
    "H1b":  [(SHIFT, "\tunsigned int lo5 = relative_addr & 0x1f;\n" + SHIFT),
             (OFS, OFS + "\tif (lo5 == 0x1c)\n\t\tofs = 0;\n")],
    # r_fwdret: read arm honours the inner forward's return (re-measured on the 93-row probe)
    "r_fwdret": [(RREAD, "\tif (!cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE + relative_addr,\n"
                         "\t    &byte, 1, MEM_READ, CACHE_NONE))\n\t\treturn 0;\n")],
    # ---- own hunt (table 2) ----
    # W3: fallthrough gated on LANE: only lane-0 stores make the phantom read (0x3f8 RBR, 0x60 8042 data)
    "W3":   [(WRET, "\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
                    "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n"
                    "\t\tif ((relative_addr & 3) != 0)\n\t\t\treturn 1;\n")],
    # W4: fallthrough everywhere EXCEPT the two widths the iir rows use
    "W4":   [(WRET, "\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
                    "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n"
                    "\t\tif (len == 1 || len == 4)\n\t\t\treturn 1;\n")],
    # RD2: the READ arm forwards twice (statement duplication) -- a phantom read on the read arm
    "RD2":  [(RREAD, RREAD + RREAD)],
    # w_ret0 (kimi CLI Q3.3): the write arm forwards, then reports failure
    "w_ret0": [(WRET, "\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
                      "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n"
                      "\t\treturn 0;\n")],
    # dd_decl (kimi CLI Q3.1): a data-keyed DECLINE on the write arm
    "dd_decl": [(WBYTE, "\t\tif (!data[ofs])\n\t\t\treturn 0;\n" + WBYTE)],
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
