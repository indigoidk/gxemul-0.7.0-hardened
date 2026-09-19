#!/usr/bin/env python3
"""#538 kill table: apply ONE named variant to dev_lca.c.  Usage: mk538.py <name> <src dev_lca.c> <dst dev_lca.c>
Every edit is an EXACT-ONCE replacement against the committed (8bd97e4) file -- a find-text that matches zero or two
times is a FAIL, which also makes each variant a presence pin on the code it edits.  The table lives HERE, in Python, so
no escape sequence passes through a shell argument (a `\\n' in argv arrives as two characters and matches nothing)."""
import io, sys

W   = "if (writeflag == MEM_WRITE) {"
LZ  = "if (len == 0)"
PRE = "\tuint8_t byte;\n\n\trelative_addr >>= 5;"
def pre(stmt): return "\tuint8_t byte;\n\n\t" + stmt + "\n\trelative_addr >>= 5;"
def lane(op, l): return "if (writeflag == MEM_WRITE && (len <= 8 || (relative_addr & 3) %s %d)) {" % (op, l)

VARIANTS = {
    "M2_len8":  (W,  "if (writeflag == MEM_WRITE && len <= 8) {"),
    "KILLLEN8": (LZ, "if (len == 0 || len > 8)"),
    "vc":       (W,  lane("==", 3)),
    "vc_ne0":   (W,  lane("!=", 0)),
    "vc_ne1":   (W,  lane("!=", 1)),
    "vc_ne2":   (W,  lane("!=", 2)),
    "vc_ne3":   (W,  lane("!=", 3)),
    "vf":       ("byte = data[ofs];", "byte = data[len > 8 ? 0 : ofs];"),
    "va":       (W,  "if (writeflag == MEM_WRITE && len <= 16) {"),
    "vb":       (LZ, "if (len == 0 || len > 16)"),
    "ve":       (LZ, "if (len == 0 || (len > 8 && relative_addr < 0x200))"),
    "vg":       (PRE, pre("if (len > 8 && (relative_addr & 0x10)) return 0;")),
    "vt1":      (PRE, pre("if (len > 8 && (relative_addr & 0x1f)) return 0;")),
    "vt2":      (PRE, pre("{ static uint64_t cont = 1; int c = len > 8 && relative_addr == cont; "
                          "cont = relative_addr + len; if (c) return 0; }")),
    "vd":       ("ofs = (relative_addr & 3) % len;", "ofs = (relative_addr & 3) % (len > 8 ? 8 : len);"),
    "vh":       ("for (i=0; i<len; i++)", "for (i=0; i<len && i<8; i++)"),
}

if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in VARIANTS:
        sys.exit("usage: mk538.py <%s> <src> <dst>" % "|".join(VARIANTS))
    name, src, dst = sys.argv[1:]
    find, repl = VARIANTS[name]
    s = io.open(src, newline="").read()
    n = s.count(find)
    if n != 1:
        sys.exit("MUTANT %s: find-text occurs %d times (want 1): %r" % (name, n, find))
    io.open(dst, "w", newline="").write(s.replace(find, repl, 1))
    print("MUTANT %s applied" % name)
