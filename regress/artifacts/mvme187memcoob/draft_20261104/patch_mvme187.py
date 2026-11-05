#!/usr/bin/env python3
# Byte-level patcher for dev_mvme187.c.  Usage: patch_mvme187.py <variant> <file>
# Variants: A1 (intermediate, task-literal: exits->declines answering 0, NO bound),
#           A2 (draft-minus-bound: exits->declines, default lets the line-68 value flow),
#           A3 (the DRAFT: bound added, reads moved into arms, warn-once declines).
import sys

variant, path = sys.argv[1], sys.argv[2]
b = open(path, "rb").read()

ANCHOR_S = b"\todata = ((uint8_t*)&d->memcreg)[relative_addr];"
ANCHOR_E = b"\n\n\tif (writeflag == MEM_READ)"
s = b.find(ANCHOR_S)
e = b.find(ANCHOR_E)
assert s >= 0 and e > s, "block anchors not found (%d,%d)" % (s, e)

A1 = (
    b"\todata = ((uint8_t*)&d->memcreg)[relative_addr];\n"
    b"\n"
    b"\tswitch (relative_addr) {\n"
    b"\n"
    b"\tcase 0x00:\t/* chipid */\n"
    b"\tcase 0x04:\t/* chiprev */\n"
    b"\t\tbreak;\n"
    b"\n"
    b"\tcase 0x08:\t/*  memconf  */\n"
    b"\t\tif (writeflag == MEM_WRITE) {\n"
    b"\t\t\t/*  A1: write ignored (decline); no bound  */\n"
    b"\t\t}\n"
    b"\t\tbreak;\n"
    b"\n"
    b"\tdefault:\n"
    b"\t\t/*  A1: declined read answers 0; no bound  */\n"
    b"\t\todata = 0;\n"
    b"\t\tbreak;\n"
    b"\t}"
)

A2 = (
    b"\todata = ((uint8_t*)&d->memcreg)[relative_addr];\n"
    b"\n"
    b"\tswitch (relative_addr) {\n"
    b"\n"
    b"\tcase 0x00:\t/* chipid */\n"
    b"\tcase 0x04:\t/* chiprev */\n"
    b"\t\tbreak;\n"
    b"\n"
    b"\tcase 0x08:\t/*  memconf  */\n"
    b"\t\tif (writeflag == MEM_WRITE) {\n"
    b"\t\t\t/*  A2: write ignored (decline); no bound  */\n"
    b"\t\t}\n"
    b"\t\tbreak;\n"
    b"\n"
    b"\tdefault:\n"
    b"\t\t/*  A2: decline; line-68 value flows out (no bound, no zero)  */\n"
    b"\t\tbreak;\n"
    b"\t}"
)

A3 = (
    b"\tswitch (relative_addr) {\n"
    b"\n"
    b"\tcase 0x00:\t/* chipid */\n"
    b"\tcase 0x04:\t/* chiprev */\n"
    b"\t\todata = ((uint8_t*)&d->memcreg)[relative_addr];\n"
    b"\t\tbreak;\n"
    b"\n"
    b"\tcase 0x08:\t/*  memconf  */\n"
    b"\t\todata = d->memcreg.memc_memconf;\n"
    b"\t\tif (writeflag == MEM_WRITE) {\n"
    b"\t\t\tif (!d->warned_memconf) {\n"
    b'\t\t\t\tfatal("[ mvme187_memc: memconf write 0x%x declined"\n'
    b'\t\t\t\t    " (once) ]\\n", (int)idata);\n'
    b"\t\t\t\td->warned_memconf = 1;\n"
    b"\t\t\t}\n"
    b"\t\t}\n"
    b"\t\tbreak;\n"
    b"\n"
    b"\tdefault:\n"
    b"\t\tif (!d->warned_default) {\n"
    b'\t\t\tfatal("[ mvme187_memc: unimplemented %s offset 0x%x"\n'
    b'\t\t\t    " (once) ]\\n", writeflag == MEM_WRITE? "write to" :\n'
    b'\t\t\t    "read from", (int) relative_addr);\n'
    b"\t\t\td->warned_default = 1;\n"
    b"\t\t}\n"
    b"\t\tbreak;\n"
    b"\t}"
)

NEW = {"A1": A1, "A2": A2, "A3": A3}[variant]
out = b[:s] + NEW + b[e:]

if variant == "A3":
    head_anchor = b"DEVICE_ACCESS(mvme187_memc)"
    hi = out.find(head_anchor)
    assert hi > 0
    j = out.rfind(b"};", 0, hi)
    assert j > 0, "struct close not found"
    field = b"\tint\t\t\twarned_memconf, warned_default;\t/*  draft: (once) latches  */\n"
    out = out[:j] + field + out[j:]

open(path, "wb").write(out)
sys.stdout.write("PATCHED %s -> %s (%d -> %d bytes)\n" % (variant, path, len(b), len(out)))
