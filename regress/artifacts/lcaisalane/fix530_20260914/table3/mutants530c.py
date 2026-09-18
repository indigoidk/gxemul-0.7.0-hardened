#!/usr/bin/env python3
"""mutants530c.py NAME SRC DST -- #530 kill table 3 (closing pass 1's class closure, 77 rows).  Table 1's mutator for
`base'/`head' conventions; the Opus closing seat's three measured escapes and one mutant per closing-pass reading-seat
shape.  Every find-text must occur EXACTLY ONCE (a presence pin).  `head' is copied by the driver."""
import io, sys

GUARD = "\tif (len == 0)\n\t\treturn 0;\n"
OFS   = "\tofs = (relative_addr & 3) % len;\n"
WBYTE = "\t\tbyte = data[ofs];\n"
WRET  = ("\t\treturn cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
         "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")
PACK  = "\t\tdata[i] = i == ofs? byte : 0x00;\n"
RET1  = PACK + "\n\treturn 1;\n"

M = {
    "base": [],
    # the Opus closing seat (measured 51/51 each on the 51-row instrument)
    "c1_w2":  [(WBYTE, "\t\tbyte = data[ofs == 2? 0 : ofs];\n")],
    "c1_w1w": [(WBYTE, "\t\tbyte = data[(ofs == 1 && len > 2)? 0 : ofs];\n")],
    "c1_r4":  [(PACK, "\t\tdata[i] = (i == ofs || (len == 4 && ofs >= 2 && i == 0))? byte : 0x00;\n")],
    # deepseek: a decline keyed on len 6
    "x_len6": [(GUARD, "\tif (len == 0 || len == 6)\n\t\treturn 0;\n")],
    # codex: the read arm fails a len-8 read at lane 0
    "x_len8lane0": [(RET1, PACK + "\n\treturn len != 8 || ofs;\n")],
    # glm: lane 2 clamped to position 0, both arms
    "x_lane2clamp": [(OFS, OFS + "\tif (ofs == 2)\n\t\tofs = 0;\n")],
    # minimax: wide stores at lane 1 dropped
    "x_w1drop": [(GUARD, "\tif (len == 0 || (writeflag == MEM_WRITE && len > 2 && (relative_addr & 3) == 1))\n"
                         "\t\treturn 0;\n")],
    # kimi-k3: the write arm falls through into a phantom READ of the same port (PREDICTED EQUIVALENT here)
    "x_wfallthru": [(WRET, "\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
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
