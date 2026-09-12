#!/usr/bin/env python3
"""ppcrlwimiwidth table-2 mutator.  usage: mut_rlwimi_t2.py <SEC cpu_ppc_instr.c> <out> <LEG>

WHY A WRAPPER.  The table-1 / null-medium mutator (../killtable_nullmedium_20260911/mutate_rlwimi.py)
anchors on a FIXED_BLOCK containing the one-line comment `/*  A wrapping MASK(MB+32, ME+32) includes the
high word.  */`, which a 2026-09-12 L4 replaced with a 19-line comment -- so every leg now refuses with
"FIXED_BLOCK not found".  This wrapper takes that file's MUTANT BLOCKS VERBATIM (so each leg is the same
edit table 1 measured), rebuilds the anchor from the old FIXED_BLOCK by swapping in the CURRENT comment
read from the source itself, and refuses unless the rebuilt anchor occurs exactly once.  A leg's
replacement therefore carries the OLD one-line comment -- comment-only, and immaterial to the build.

NULL_MEDIUM is the CORRECTED definition from the null-medium table (decode and retire, insert nothing),
NOT table 1's, which mapped NULL_MEDIUM to the fixed block and measured 28/28 -- a vacuous leg.
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(HERE, "..", "killtable_nullmedium_20260911", "mutate_rlwimi.py")
OLD_COMMENT = "\t/*  A wrapping MASK(MB+32, ME+32) includes the high word.  */\n"

def blocks():
    s = io.open(OLD, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r'^([A-Z_]+_BLOCK) = """(.*?)"""', s, re.S | re.M):
        out[m.group(1)] = eval('"""' + m.group(2) + '"""')
    return out

LEGMAP = {"NULL_MEDIUM": "NULL_MEDIUM_BLOCK", "M_REV_COND": "M_REV_COND_BLOCK",
          "M_ONLY_CAST": "M_ONLY_CAST_BLOCK", "M_ONLY_HIGH": "M_ONLY_HIGH_BLOCK",
          "M_POST_LOOP": "M_POST_LOOP_BLOCK", "M_ORIG": "M_ORIG_BLOCK"}

src, dst, leg = sys.argv[1:4]
t = io.open(src, encoding="utf-8").read()
if leg != "BASE":
    B = blocks()
    old_fixed = B["FIXED_BLOCK"]
    if old_fixed.count(OLD_COMMENT) != 1:
        sys.exit("old FIXED_BLOCK does not carry the expected one-line comment -- REFUSING")
    head, tail = old_fixed.split(OLD_COMMENT)
    i = t.index(head) + len(head) if t.count(head) == 1 else -1
    if i < 0:
        sys.exit("pre-comment half of the anchor not found exactly once -- REFUSING")
    j = t.index("\tif (mb > me)\n", i)
    cur_fixed = head + t[i:j] + tail
    if t.count(cur_fixed) != 1 or leg not in LEGMAP:
        sys.stderr.write("rebuilt anchor occurs %d times (or unknown leg %s) -- REFUSING\n" % (t.count(cur_fixed), leg))
        sys.exit(3)
    t = t.replace(cur_fixed, B[LEGMAP[leg]])
io.open(dst, "w", encoding="utf-8", newline="\n").write(t)
print("MUTATED %s" % leg)
