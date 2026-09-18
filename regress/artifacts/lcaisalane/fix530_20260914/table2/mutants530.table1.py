#!/usr/bin/env python3
"""mutants530.py NAME SRC DST -- #530 (lcaisalane) kill table 1.  SRC is the FIXED dev_lca.c (the #530 working set).
Each mutant is one or more (find, replace) edits; every find-text must occur EXACTLY ONCE -- a presence pin.
`head' is not an edit: the driver copies HEAD's file (the pre-fix defect verbatim, clause (a)/(b))."""
import io, sys

GUARD  = "\tif (len == 0)\n\t\treturn 0;\n"
OFS    = "\tofs = (relative_addr & 3) % len;\n"
WBYTE  = "\t\tbyte = data[ofs];\n"
PACK   = "\t\tdata[i] = i == ofs? byte : 0x00;\n"
TAIL   = PACK + "\n\treturn 1;\n"
EXIT   = ("\tif ((relative_addr & 3) > len) {\n"
          "\t\tfatal(\"[ ofs=%i len=%i in lca_isa access function. \"\n"
          "\t\t    \"aborting ]\\n\", (int)(relative_addr & 3), (int)len);\n"
          "\t\texit(1);\n"
          "\t}\n")

M = {
    "base":           [],
    # (b) the removed exit reinstated in the fixed code, same predicate, same text
    "m_exit":         [(OFS, EXIT + OFS)],
    # (d) growth mutants of the accept: decline beyond the width (variant C) / at-and-beyond (variant A)
    "m_declbeyond":   [(OFS, "\tif ((relative_addr & 3) > len)\n\t\treturn 0;\n" + OFS)],
    "m_decleq":       [(OFS, "\tif ((relative_addr & 3) >= len)\n\t\treturn 0;\n" + OFS)],
    # one arm folds, the other does not
    "m_writeonlyfold":[(PACK, "\t\tdata[i] = i == (relative_addr & 3)? byte : 0x00;\n")],
    "m_readonlyfold": [(WBYTE, "\t\tbyte = data[relative_addr & 3];\n")],
    # glm's clamp: position 0 for every lane at or beyond the width
    "m_clamp":        [(OFS, "\tofs = relative_addr & 3;\n\tif (ofs >= len)\n\t\tofs = 0;\n")],
    # lane-decode edits
    "m_lane1":        [(OFS, "\tofs = (relative_addr & 1) % len;\n")],
    "m_nomask":       [(OFS, "\tofs = relative_addr % len;\n")],
    "m_replicate":    [(PACK, "\t\tdata[i] = byte;\n")],
    # the read arm's success return
    "m_retzero":      [(TAIL, PACK + "\n\treturn 0;\n")],
    # PREDICTED EQUIVALENT on every probed cell (disclosed): no len-0 producer; & (len-1) == % len for len 1/2/4/8
    "m_lenzero":      [(GUARD, "")],
    "m_andmask":      [(OFS, "\tofs = (relative_addr & 3) & (len - 1);\n")],
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
