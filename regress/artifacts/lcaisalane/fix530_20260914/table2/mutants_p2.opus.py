#!/usr/bin/env python3
"""mutants_p2.py NAME SRC DST -- #530 (lcaisalane) PASS-2 measuring seat (Opus 5), 2026-09-14.
SRC is the FIXED dev_lca.c (the #530 working set).  Each mutant is one or more (find, replace) edits;
every find-text must occur EXACTLY ONCE (a presence pin).  Aimed at the cells kill table 1 did NOT row:
writes at len 4/8 (the canonical real-OS `stl' outb path), reads/writes at a 0-mod-4 port with len > 1,
the read arm's zero-fill, a len-4-only replicate, a len-8-only lane decode, the forwarded address."""
import io, sys

GUARD  = "\tif (len == 0)\n\t\treturn 0;\n"
OFS    = "\tofs = (relative_addr & 3) % len;\n"
WBYTE  = "\t\tbyte = data[ofs];\n"
WARM   = "\tif (writeflag == MEM_WRITE) {\n\t\tbyte = data[ofs];\n"
WADDR  = "\t\treturn cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n\t\t    relative_addr, &byte, 1, writeflag, CACHE_NONE);\n"
PACK   = "\t\tdata[i] = i == ofs? byte : 0x00;\n"
SHIFT  = "\trelative_addr >>= 5;\n\n\t/*\n\t *  #530"

M = {
    "base":        [],
    # write arm drops lane bit 1 (one token): (4,2)(4,3)(8,2)(8,3) stores forward the wrong byte
    "p_wbit1":     [(WBYTE, "\t\tbyte = data[ofs & 1];\n")],
    # canonical clause-(d) form on the DOMINATING predicate of the edited `byte = data[ofs]':
    # if (X) -> if (X && Y), Y on a body-read lvalue.  len 4/8 stores fall through to the READ arm.
    "p_wnarrow":   [(WARM, "\tif (writeflag == MEM_WRITE && len <= 2) {\n\t\tbyte = data[ofs];\n")],
    # decline (return 0) every store wider than a word
    "p_wdrop4":    [(GUARD, "\tif (len == 0 || (len > 2 && writeflag == MEM_WRITE))\n\t\treturn 0;\n")],
    # forwarded ADDRESS: len 4/8 stores go to the neighbouring port
    "p_waddr4":    [(WADDR, "\t\treturn cpu->memory_rw(cpu, cpu->mem, LCA_ISA_BASE +\n\t\t    (relative_addr ^ (len > 2)), &byte, 1, writeflag, CACHE_NONE);\n")],
    # decline every wide (len > 1) access to a 0-mod-4 port, both arms: (2,0)(4,0)(8,0) R and W
    "p_lane0decl": [(GUARD, "\tif (len == 0 || (len > 1 && (relative_addr & 3) == 0))\n\t\treturn 0;\n")],
    # read arm stops zero-filling the other positions -- PREDICTED EQUIVALENT (memory_rw.c's #95 pre-zero)
    "p_nozero":    [(PACK, "\t\tif (i == ofs)\n\t\t\tdata[i] = byte;\n")],
    # len-4-only replicate on the read arm (the len-4 read rows are witness rows MASKED to one lane)
    "p_rep4":      [(PACK, "\t\tdata[i] = (i == ofs || len == 4)? byte : 0x00;\n")],
    # len-8-only lane decode drops bit 1 (both arms) -- len 8 lanes are arguably under the lcaisaqword disclosure
    "p_q8lane":    [(OFS, "\tofs = (relative_addr & (len > 4? 1 : 3)) % len;\n")],
    # OUTSIDE THE FIX: 10-bit ISA port decode (every probed port is < 0x400)
    "p_port10":    [(SHIFT, "\trelative_addr >>= 5;\n\trelative_addr &= 0x3ff;\n\n\t/*\n\t *  #530")],
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
