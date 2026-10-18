#!/usr/bin/env python3
"""mutants_564.py <fixed dev_sgi_re.c> <out dir> -- write the #564 kill table's one-edit mutants of the FIXED file,
one <name>.c each.  Every edit is anchored on text that must occur EXACTLY ONCE in the fixed file; a missing or
ambiguous anchor is a FAIL (it would otherwise be a mutant that silently equals the fix).  Each entry names the rows
predicted to catch it -- predictions, checked against the table, never copied into a measured column."""
import io, os, sys

S1R = '"0x%08x) -- transfer declined (once) ]\\n", mode);\n\t\t}\n\t\treturn;'
S2R = '"declined (once) ]\\n", src);\n\t\t}\n\t\treturn;'
S3R = '" ]\\n", dst_tlb);\n\t\t\t}\n\t\t\treturn;'
S4R = '"(once) ]\\n", depth, dst_tlb);\n\t\t\t}\n\t\t\treturn;'
S5R = '" ]\\n", (int)bytemask, dst_tlb);\n\t\t\t}\n\t\t\treturn;'
G1 = 'if (mode & MTE_MODE_STIPPLE) {\n\t\tif (!(d->warned & SGIRE_W_MTE_STIPPLE))'
G2 = 'if (src > MTE_TLB_C) {'
G3 = 'if (mode & MTE_MODE_COPY) {\n\t\t\tif (!(d->warned & SGIRE_W_MTE_COPY))'
G4 = 'if (depth != 8) {'
G5 = 'if (bytemask != 0xffffffff) {'
DSTX = '((mode & MTE_MODE_DST_BUF_MASK) >> MTE_DST_TLB_SHIFT)'     # dst_tlb is declared AFTER S1

def sub(a, b):
    return [(a, b)]
def ret_to_exit(anchor):
    return sub(anchor, anchor.replace("return;", "exit(1);"))
def drop_ret(anchor, ind):
    return sub(anchor, anchor[:anchor.rindex("\n" + ind + "return;")])
def ret_inside(anchor, ind):
    inner = anchor[:anchor.rindex("\n" + ind[:-1] + "}")]       # up to the latch block's closing brace
    return sub(anchor, inner + "\n" + ind + "return;\n" + ind[:-1] + "}")

M = [
    # ---- floor clause (b): the terminating call put back, per site
    ("b1", ret_to_exit(S1R), "stip *"), ("b2", ret_to_exit(S2R), "src *"), ("b3", ret_to_exit(S3R), "copy *"),
    ("b4", ret_to_exit(S4R), "depth *"), ("b5", ret_to_exit(S5R), "mask *"),
    # ---- clause (d): the guard kept, the decline nulled -- announce and continue
    ("d1", drop_ret(S1R, "\t\t"), "stip a/b/c/copy/lin"), ("d2", drop_ret(S2R, "\t\t"), "src 3-7 (tiled fill lands), src 3 lin"),
    ("d3", drop_ret(S3R, "\t\t\t"), "copy lin a/b"), ("d4", drop_ret(S4R, "\t\t\t"), "depth a/b *"),
    ("d5", drop_ret(S5R, "\t\t\t"), "mask * incl. unwritten"),
    # ---- the return moved INSIDE the latch: the first refusal declines, the rest proceed
    ("r1", ret_inside(S1R, "\t\t\t"), "stip b (second refusal), latch paint"),
    ("r5", ret_inside(S5R, "\t\t\t\t"), "mask fffffffe etc. (second and later refusals)"),
    # ---- guards scoped to fewer cells than today's
    ("s1copy", sub(G1, G1.replace("(mode & MTE_MODE_STIPPLE)", "((mode & MTE_MODE_STIPPLE) && !(mode & MTE_MODE_COPY))")), "stip copy"),
    ("s1tiled", sub(G1, G1.replace("(mode & MTE_MODE_STIPPLE)", "((mode & MTE_MODE_STIPPLE) && %s <= MTE_TLB_C)" % DSTX)), "stip lin a/b"),
    ("s2up", sub(G2, "if (src > MTE_TLB_C + 1) {"), "src 3, src 3 copy, src 3 lin, latch texts"),
    ("s2down", sub(G2, "if (src >= MTE_TLB_C) {"), "src c fill, src c copy (ACCEPT)"),
    ("s2no7", sub(G2, "if (src > MTE_TLB_C && src != 7) {"), "src 7"),
    ("s2copy", sub(G2, "if (src > MTE_TLB_C && (mode & MTE_MODE_COPY)) {"), "src 3-7, src 3 lin"),
    ("s2tiled", sub(G2, "if (src > MTE_TLB_C && dst_tlb <= MTE_TLB_C) {"), "src 3 lin"),
    ("s3laba", sub(G3, G3.replace("(mode & MTE_MODE_COPY)", "((mode & MTE_MODE_COPY) && dst_tlb == MTE_TLB_LIN_A)")), "copy lin b"),
    ("s4one", sub(G4, "if (depth == 16) {"), "depth a/b 32, 64"),
    ("s4laba", sub(G4, "if (depth != 8 && dst_tlb == MTE_TLB_LIN_A) {"), "depth b *"),
    ("s5zero", sub(G5, "if (bytemask != 0xffffffff && bytemask != 0) {"), "mask unwritten"),
    ("s5low", sub(G5, "if ((bytemask & 0xffff) != 0xffff) {"), "mask 7fffffff, mask sweep"),
    ("s5hi", sub(G5, "if ((bytemask >> 16) != 0xffff) {"), "mask fffffffe, mask sweep"),
    ("s5inner", sub(G5, "if ((bytemask | 0x00ff0000) != 0xffffffff) {"), "mask sweep ONLY"),
    ("s5laba", sub(G5, "if (bytemask != 0xffffffff && dst_tlb == MTE_TLB_LIN_A) {"), "mask lin b"),
    # ---- the ACCEPT side: guards grown to refuse legal transfers
    ("eccgrow", sub(G5, "if (bytemask != 0xffffffff || (mode & MTE_MODE_DST_ECC)) {"), "lin fill ecc"),
    ("s4grow", sub(G4, "if (depth != 8 || dst_tlb == MTE_TLB_LIN_B) {"), "lin fill b"),
    ("s5hoist", sub("\tswitch (dst_tlb) {\n\tcase MTE_TLB_A:", "\tif (bytemask != 0xffffffff)\n\t\treturn;\n\tswitch (dst_tlb) {\n\tcase MTE_TLB_A:"),
     "tile mask, tile copy mask"),
    # ---- the latch
    ("shared", sub("SGIRE_W_MTE_SRC      = 1 << 14,", "SGIRE_W_MTE_SRC      = 1 << 13,"), "latch texts (S2 silenced by S1)"),
    ("assign", sub("d->warned |= SGIRE_W_MTE_COPY;", "d->warned = SGIRE_W_MTE_COPY;"), "latch old bit, latch texts"),
    ("nolatch", sub("if (!(d->warned & SGIRE_W_MTE_DEPTH)) {", "if (1) {"), "depth once"),
    ("wrongbit", sub("if (!(d->warned & SGIRE_W_MTE_BYTEMASK)) {", "if (!(d->warned & SGIRE_W_MTE_DEPTH)) {"), "mask once, latch texts"),
]

def main():
    src, out = sys.argv[1], sys.argv[2]
    t = io.open(src, encoding="utf-8", newline="").read()
    os.makedirs(out, exist_ok=True)
    names = []
    for name, edits, pred in M:
        m = t
        for a, b in edits:
            n = m.count(a)
            if n != 1:
                print("MUTANT ANCHOR FAIL %s: %d occurrences of %r" % (name, n, a[:70])); sys.exit(9)
            m = m.replace(a, b)
        assert m != t, name
        io.open(os.path.join(out, name + ".c"), "w", encoding="utf-8", newline="").write(m)
        names.append(name)
        print("%-9s predicted: %s" % (name, pred))
    print("mutants written: %d" % len(names))

if __name__ == "__main__":
    main()
