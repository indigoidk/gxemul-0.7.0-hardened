#!/usr/bin/env python3
"""Generate the six one-edit variants of DEVICE_ACCESS(lca_isa) from the 8bd97e4 blob.

Every edit is an exact-string replacement that must match EXACTLY ONCE, or the script dies.
"""
import os, sys, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "ref", "src_devices_dev_lca.c")
OUT  = os.path.join(HERE, "variants")
os.makedirs(OUT, exist_ok=True)
src = open(BASE, encoding="latin-1").read()

SHIFT = "\trelative_addr >>= 5;\n\n\t/*\n\t *  #530: the byte for ISA port P"
WARM  = "\tif (writeflag == MEM_WRITE) {\n\t\tbyte = data[ofs];\n"
GUARD = "\tif (len == 0)\n\t\treturn 0;\n\tofs = (relative_addr & 3) % len;\n"

VARIANTS = {
    # (a) the write arm takes len <= 16 only; a wider store falls into the READ arm
    "va": (WARM, "\tif (writeflag == MEM_WRITE && len <= 16) {\n\t\tbyte = data[ofs];\n"),
    # (c) the write arm takes a wide store at lane 3 only
    "vc": (WARM, "\tif (writeflag == MEM_WRITE && (len <= 8 || (relative_addr & 3) == 3)) {\n\t\tbyte = data[ofs];\n"),
    # (e) the guard refuses a wide access to a port below 0x200 (relative_addr is the PORT here)
    "ve": (GUARD, "\tif (len == 0 || (len > 8 && relative_addr < 0x200))\n\t\treturn 0;\n\tofs = (relative_addr & 3) % len;\n"),
    # (g) inserted BEFORE the shift, so relative_addr is the sparse address A = 32P + k: refuse k = 16
    "vg": (SHIFT, "\tif (len > 8 && (relative_addr & 0x10)) return 0;\n" + SHIFT),
    # LADDER (measures which widths arrive whole): the write arm takes len <= 64 / len <= 256 only
    "vw64":  (WARM, "\tif (writeflag == MEM_WRITE && len <= 64) {\n\t\tbyte = data[ofs];\n"),
    "vw256": (WARM, "\tif (writeflag == MEM_WRITE && len <= 256) {\n\t\tbyte = data[ofs];\n"),
    # (b) the guard refuses len > 16
    "vb": (GUARD, "\tif (len == 0 || len > 16)\n\t\treturn 0;\n\tofs = (relative_addr & 3) % len;\n"),
    # (d) the lane modulus clamped at 8
    "vd": (GUARD, "\tif (len == 0)\n\t\treturn 0;\n\tofs = (relative_addr & 3) % (len > 8 ? 8 : len);\n"),
    # (f) a wide store forwards data[0]
    "vf": ("\t\tbyte = data[ofs];\n", "\t\tbyte = data[len > 8 ? 0 : ofs];\n"),
    # (h) the read-arm packing loop stops at 8
    "vh": ("\tfor (i=0; i<len; i++)\n", "\tfor (i=0; i<len && i<8; i++)\n"),
    # T1 (teammate, "aligned destinations only"): refuse a wide access unless the sparse address
    #    is 32-byte aligned, i.e. the discarded a<4:0> is zero.  Inserted BEFORE the shift.
    "vt1": (SHIFT, "\tif (len > 8 && (relative_addr & 0x1f)) return 0;\n" + SHIFT),
    # T2 (teammate, "first 16-byte chunk only"): refuse a wide access that CONTINUES the previous
    #    access to this handler -- i.e. every chunk of a multi-chunk store_buf write after the
    #    first.  Inserted BEFORE the shift, so it compares sparse addresses.
    "vt2": (SHIFT, "\t{ static uint64_t cont = 1; int c = len > 8 && relative_addr == cont;"
                   " cont = relative_addr + len; if (c) return 0; }\n" + SHIFT),
}

for name, (old, new) in VARIANTS.items():
    n = src.count(old)
    if n != 1:
        sys.exit("VARIANT %s: anchor matched %d times, want 1" % (name, n))
    v = src.replace(old, new, 1)
    path = os.path.join(OUT, "dev_lca.c." + name)
    open(path, "w", encoding="latin-1", newline="\n").write(v)
    d = "".join(difflib.unified_diff(src.splitlines(True), v.splitlines(True),
                                     "a/src/devices/dev_lca.c", "b/src/devices/dev_lca.c", n=2))
    open(os.path.join(OUT, name + ".diff"), "w", encoding="latin-1", newline="\n").write(d)
    print("== %s" % name)
    print(d)
print("MKVARIANTS_DONE")
