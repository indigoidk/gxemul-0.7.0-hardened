#!/usr/bin/env python3
"""norm_objdump.py <objdump -d output> -- one line per instruction, `<function>: mnemonic operands`, with addresses,
raw bytes and branch-target addresses removed (a target keeps only its symbol, `<f+off>` -> `<f+*>`), so two objects
whose code moved can be compared instruction by instruction."""
import re, sys
out, fn = [], "?"
for ln in open(sys.argv[1], encoding="latin-1"):
    ln = ln.rstrip("\n")
    m = re.match(r"^[0-9a-f]+ <([^>]+)>:$", ln)
    if m:
        fn = m.group(1); out.append("== " + fn); continue
    m = re.match(r"^\s+[0-9a-f]+:\t(?:[0-9a-f]{2} )+\s*\t(.*)$", ln)
    if not m:
        continue
    ins = m.group(1)
    ins = re.sub(r"\b[0-9a-f]+ <([^>+]+)(\+0x[0-9a-f]+)?>", lambda x: "<%s+*>" % x.group(1), ins)
    out.append("%s: %s" % (fn, re.sub(r"\s+", " ", ins).strip()))
print("\n".join(out))
