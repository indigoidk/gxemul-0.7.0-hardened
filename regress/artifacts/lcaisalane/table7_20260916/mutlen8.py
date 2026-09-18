#!/usr/bin/env python3
"""mutlen8.py <name> <src> <dst> -- #530 closing pass 6+1: the mutant CODEX named and FABLE ordered built.

    W_len8    if (writeflag == MEM_WRITE)  ->  if (writeflag == MEM_WRITE && len <= 8)

WHY IT IS INSIDE THE (d) DEPENDS-ON ENUMERATION, by the mechanical rule rather than by analogy:
`writeflag == MEM_WRITE' DOMINATES the edited line `byte = data[ofs]' (dev_lca.c:300, which IS the
repair's own hunk), and `len' is a body-read lvalue.  The joint-cell ruling's own worked example is
this exact shape -- "a condition qualified (if (X) -> if (X && writeflag == MEM_WRITE))".

PREDICTION, recorded BEFORE the run so it cannot be fitted afterwards: **352/352, A CLEAN SWEEP.**
It diverges from the fix ONLY at len > 8, and the probe is instruction-driven so its widest access is
STQ = 8.  No row can drive the divergent cell.

AND THE REACHABILITY HALF IS ALREADY SETTLED IN SOURCE (Fable 5.1, verified independently of codex):
    memory.c:839, :841-853       store_buf issues memory_rw at psize in {1024, 256, 64, 16, 4, 1}
    memory_rw.c:150-151, :187    the split granule is 1024, NOT 8 (MRW_SPLIT_MASK = 0x3ff)
    memory_rw.c:587-589          the device is called with that len
    dev_lca.c:547-548            lca_isa is registered over 2 MB, so no clamp bites below 1024
    cpu_alpha_palcode.c:121,:144 PROM GETENV: store_buf(cpu, a2, s, len), a2 GUEST-SUPPLIED
So len > 8 IS guest-reachable, and by Fable's stated branch rule a sweep here is **L2, fixed in-round**,
not clause-(e) debt.

The anchor carries its brace and is UNIQUE in dev_lca.c (grep -c == 1); `if (writeflag == MEM_WRITE)'
without the brace occurs three more times in OTHER handlers, which is exactly the ambiguity that would
have made a looser anchor edit the wrong function.
"""
import io
import sys

ANCHOR = "\tif (writeflag == MEM_WRITE) {\n"
M = {
    "base": [],
    "W_len8": [(ANCHOR, "\tif (writeflag == MEM_WRITE && len <= 8) {\n", 1)],
}

if len(sys.argv) == 2 and sys.argv[1] == "list":
    print(" ".join(sorted(M)))
    sys.exit(0)

if len(sys.argv) != 4:
    print(__doc__)
    sys.exit(2)

name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
if name not in M:
    print("unknown mutant %r; known: %s" % (name, " ".join(sorted(M))))
    sys.exit(2)

txt = io.open(src, encoding="utf-8", newline="").read()
n = 0
for find, repl, want in M[name]:
    got = txt.count(find)
    if got != want:
        #  ANCHOR MISMATCH IS A FAIL, never a silent skip -- that turns the anchor into a PRESENCE PIN
        #  on the feature it edits.
        print("ANCHOR MISMATCH in %s: expected %d occurrence(s), found %d" % (name, want, got))
        sys.exit(1)
    txt = txt.replace(find, repl, want)
    n += want

#  newline='' IS LOAD-BEARING on Windows python: without it every LF becomes CRLF and the mutant
#  differs from its source in EVERY line.
io.open(dst, "w", encoding="utf-8", newline="").write(txt)
print("APPLIED_LEN8 %s (%d edit(s))" % (name, n))
