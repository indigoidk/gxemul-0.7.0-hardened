#!/usr/bin/env python3
"""mutants_c1.py NAME SRC DST -- #530 CLOSING PASS 1 (Opus 5 measuring seat), 2026-09-14.
SRC is the FIXED dev_lca.c.  Aimed at the cells the 51-row detector does NOT row:
write-arm lanes 1/2 at len 4/8 (st4/st8 rows pin only lane 3 and lane 0), a len-2 store
at lane 0, and a read-arm full-register mis-fill at len-4 ofs>=2 (only the single lane is
read there).  Each edit changes a guest-visible (P&3)%len byte and preserves every rowed cell."""
import io, sys

WBYTE = "\t\tbyte = data[ofs];\n"
PACK  = "\t\tdata[i] = i == ofs? byte : 0x00;\n"

M = {
    "base": [],
    # WRITE arm diverges from the shared position rule ONLY at computed ofs == 2:
    # (4,2)(8,2)(3,2 head)(5,2 head) stores forward data[0] instead of data[2].
    # No write row has computed ofs == 2 (w22 is (2,2) -> ofs 0); st4/st8 pin lane 3 and lane 0.
    "c1_w2":   [(WBYTE, "\t\tbyte = data[ofs == 2? 0 : ofs];\n")],
    # WRITE arm diverges ONLY at computed ofs == 1 for len >= 4 (len-2 ofs1 rows w21/w23 kept):
    # (4,1)(8,1) stores forward data[0].  st4/st8 pin only lane 3 and lane 0; no (4,1)/(8,1) store row.
    "c1_w1w": [(WBYTE, "\t\tbyte = data[(ofs == 1 && len > 2)? 0 : ofs];\n")],
    # READ arm: at len 4 and ofs >= 2 ALSO write the byte into lane 0.  The (4,2)/(4,3) reads are
    # observed only at their single lane (ofs2 wide / ofs3 wide MASK to that lane); no full-register
    # (4,>=2) read row exists.  Guarded len==4 so the len-8 full reads (ld8) do not see it.
    "c1_r4":  [(PACK, "\t\tdata[i] = (i == ofs || (len == 4 && ofs >= 2 && i == 0))? byte : 0x00;\n")],
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
