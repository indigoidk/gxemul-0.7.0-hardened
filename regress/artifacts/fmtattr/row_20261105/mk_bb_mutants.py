#!/usr/bin/env python3
"""mk_bb_mutants.py -- the two type-compatible mutants of the staged bootblock.c loading line that the compiler cannot see
(GPT-6 Astra, pass 2b), written as full copies beside the stage: bb_mutants/M1_radix.c, bb_mutants/M2_narrow.c."""
import io
import os

O = "C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/codescan/fmtfix/"
src = io.open(O + "stage/src/disk/bootblock.c", encoding="latin-1", newline="").read()
M = {"M1_radix": ('disk offset 0x%" PRIx64', 'disk offset 0x%" PRIu64'),
     "M2_narrow": ("(uint64_t)diskoffset);", "(uint64_t)(uint32_t)diskoffset);")}
os.makedirs(O + "bb_mutants", exist_ok=True)
for lab, (old, new) in M.items():
    assert src.count(old) == 1, (lab, src.count(old))
    io.open(O + "bb_mutants/%s.c" % lab, "w", encoding="latin-1", newline="").write(src.replace(old, new))
print("mutants:", sorted(M))
