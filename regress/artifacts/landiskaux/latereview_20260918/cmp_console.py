#!/usr/bin/env python3
"""Strip the emulator's own `[ memory ... ]` warnings (which interleave mid-word)
and the banner lines naming the binary/overlay, then diff the guest console."""
import re, sys, difflib
def clean(p):
    t = open(p, "rb").read().decode("latin-1")
    n_warn = len(re.findall(r"\[ memory (?:READ|WRITE): [^\]]*\]\r?\n?", t))
    t = re.sub(r"\[ memory (?:READ|WRITE): [^\]]*\]\r?\n?", "", t)
    t = re.sub(r"GXemul [^\n]*Copyright[^\n]*", "GXemul <banner>", t)
    t = re.sub(r"/tmp/gxemul\.[^\s]+", "/tmp/<tmpfile>", t)
    return t.splitlines(), n_warn
a, na = clean(sys.argv[1]); b, nb = clean(sys.argv[2])
d = list(difflib.unified_diff(a, b, "base", "fix", lineterm="", n=0))
print("warnings stripped: base=%d fix=%d; console lines: base=%d fix=%d" % (na, nb, len(a), len(b)))
print("DIFF_LINES=%d" % sum(1 for x in d if x[:1] in "+-" and x[:3] not in ("+++", "---")))
for x in d[:40]:
    print(x)
