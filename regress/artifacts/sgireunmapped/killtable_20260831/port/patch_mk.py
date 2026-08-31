#!/usr/bin/env python3
"""Add M6 (index re-map), M7 (window translation) and mret0 to mkvariant499.py."""
import io

P = ("/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-cc-GXEMUL/"
     "8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/o499/mkvariant499.py")
s = io.open(P, encoding="utf-8").read()

# 1. give apply_fix a `tail' so the return-0 mutant can be built
old_af = ('def apply_fix(text, wr_bit=7, rd_bit=8):\n'
          '    text = sub1(text, ENUM_OLD, enum_new(wr_bit, rd_bit), "enum")\n'
          '    text = sub1(text, OLD, announce("SGIRE_W_UNMAP_WR", '
          '"SGIRE_W_UNMAP_RD", ""), "catchall")\n'
          '    return text\n')
new_af = ('def apply_fix(text, wr_bit=7, rd_bit=8, tail=""):\n'
          '    text = sub1(text, ENUM_OLD, enum_new(wr_bit, rd_bit), "enum")\n'
          '    text = sub1(text, OLD, announce("SGIRE_W_UNMAP_WR", '
          '"SGIRE_W_UNMAP_RD", tail), "catchall")\n'
          '    return text\n')
assert s.count(old_af) == 1, "apply_fix anchor: %d" % s.count(old_af)
s = s.replace(old_af, new_af)

# 2. three new variants, inserted before the final else
TAB = chr(9)
IDX_OLD = (TAB * 3 + "int tlbi = ((relative_addr & 0x1ff) >> 1) & 0xff;\n"
           + TAB * 3 + "for (size_t hwi = 0; hwi < len; hwi += sizeof(uint16_t)) {\n"
           + TAB * 4 + "d->re_tlb_a[tlbi] = data[hwi]*256 + data[hwi+1];\n")
IDX_NEW = (TAB * 3 + "int tlbi = (((relative_addr & 0x1ff) >> 1) + 1) & 0xff;\n"
           + TAB * 3 + "for (size_t hwi = 0; hwi < len; hwi += sizeof(uint16_t)) {\n"
           + TAB * 4 + "d->re_tlb_a[tlbi] = data[hwi]*256 + data[hwi+1];\n")

add = '''elif variant == "mret0":
    # the decline uses `return 0`, which memory_rw.c coerces to -1 and turns
    # into a guest EXCEPTION_DBE.  Kills `rd sent` and `rd nodbe`.
    s = apply_fix(s, tail="\\t\\treturn 0;\\n")
elif variant == "m6_idxshift":
    # INDEX RE-MAP, TLB_A only: tlbi + 1.  The window decode is untouched, so
    # every "did not reach the catch-all" oracle stays green by construction;
    # only an ANCHORED oracle that names the cell can see it.  It is also a
    # real defect: the loop then writes re_tlb_a[256], one past the array.
    s = apply_fix(s)
    s = sub1(s, IDX_OLD, IDX_NEW, "m6")
elif variant == "m7_wintrans":
    # WINDOW TRANSLATION, TLB_A: both bounds + 0x100.  The top-slot accept row
    # stays inside the moved window and cannot see it; the BASE-slot row falls
    # out of TLB_A entirely, and TLB_B's base is swallowed by TLB_A -- which an
    # anchored row reports as the WRONG ARRAY, and an unanchored one cannot.
    s = apply_fix(s)
    s = sub1(s, C_TLBA,
             "relative_addr >= CRIME_RE_TLB_A + 0x100 && "
             "relative_addr < CRIME_RE_TLB_B + 0x100", "m7")
'''
anchor = 'else:\n    die("unknown variant " + variant)\n'
assert s.count(anchor) == 1
s = s.replace(anchor, add + anchor)

# IDX_OLD/IDX_NEW must be defined before use
decl = 'E_TLBA = "\\tSGIRE_W_TLBA_LEN  = 1 << 0,\\n"\n'
assert s.count(decl) == 1
s = s.replace(decl, decl
              + "IDX_OLD = " + repr(IDX_OLD) + "\n"
              + "IDX_NEW = " + repr(IDX_NEW) + "\n")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("patched mkvariant499.py")
