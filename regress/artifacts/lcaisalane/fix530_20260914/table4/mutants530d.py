#!/usr/bin/env python3
"""mutants530d.py NAME SRC DST -- #530 kill table 4 (closing pass 2: the split-TAIL cells and the phantom read, 93 rows).
Table 1's conventions for `base'/`head' (`head' is copied by the driver).  The Opus closing-pass-2 seat's two measured
77/77 escapes, its swapmod, and one mutant per new row's channel -- including a DECLINE of a mid-sequence tail store,
which only the per-phase command-byte reset lets the `tailw' rows see.  Every find-text must occur EXACTLY ONCE."""
import io, sys

GUARD = "\tif (len == 0)\n\t\treturn 0;\n"
OFS   = "\tofs = (relative_addr & 3) % len;\n"
WBYTE = "\t\tbyte = data[ofs];\n"
WRET  = ("\t\treturn cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
         "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")
PACK  = "\t\tdata[i] = i == ofs? byte : 0x00;\n"

M = {
    "base": [],
    # the Opus closing-pass-2 seat, measured 77/77 each on the 77-row instrument
    "t_tails": [(OFS, OFS + "\tif ((relative_addr & 3) == 0 && len > 2 && (len & 3))\n\t\tofs = 1;\n")],
    "x_wfallthru": [(WRET, "\t\tcpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n"
                           "\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n")],
    "swapmod": [(OFS, "\tofs = (relative_addr % len) & 3;\n")],
    # a lane-0 len-3 decline, both arms (h5 ldq's 0x400 tail and the 0x60 t3 cells)
    "d_len3lane0": [(GUARD, "\tif (len == 0 || (len == 3 && (relative_addr & 3) == 0))\n\t\treturn 0;\n")],
    # one tail length mis-placed on ONE arm
    "t_w7": [(WBYTE, "\t\tbyte = data[(len == 7 && ofs == 0)? 1 : ofs];\n")],
    "t_r6": [(PACK, "\t\tdata[i] = i == ((len == 6 && ofs == 0)? 1 : ofs)? byte : 0x00;\n")],
    # a DECLINED tail store in mid-sequence: without the per-phase reset its row reads t7's 0x44 and passes
    "d_w6tail": [(GUARD, "\tif (len == 0 || (writeflag == MEM_WRITE && len == 6 && (relative_addr & 3) == 0))\n"
                         "\t\treturn 0;\n")],
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
