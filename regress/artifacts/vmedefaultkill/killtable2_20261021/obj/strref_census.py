#!/usr/bin/env python3
"""strref_census.py <obj.o> -- count code references per STRING CONTENT (never per .LCn label: the numbering is not
stable across two compiles -- in this pair .LC2 is the default: READ debug string in fix568 and the read announce in
fix568b).  Uses objdump -t (label -> section+offset), objdump -s (section bytes) and objdump -dr (relocations)."""
import re, subprocess, sys
o = sys.argv[1]
run = lambda *a: subprocess.run(("objdump",) + a + (o,), stdout=subprocess.PIPE, check=True).stdout.decode("latin-1")
labels = {}
for ln in run("-t").splitlines():
    m = re.match(r"^([0-9a-f]+) l\s+(\.rodata\S*)\s+[0-9a-f]+ (\.LC\d+)$", ln)
    if m:
        labels[m.group(3)] = (m.group(2), int(m.group(1), 16))
secs, cur = {}, None
for ln in run("-s", "-j", ".rodata.str1.1", "-j", ".rodata.str1.8").splitlines():
    m = re.match(r"^Contents of section (\S+):$", ln)
    if m:
        cur = m.group(1); secs[cur] = bytearray(); continue
    m = re.match(r"^ ([0-9a-f]{4,}) ((?:[0-9a-f]{2,8} ?){1,4})", ln)
    if m and cur:
        secs[cur] += bytes.fromhex(m.group(2).replace(" ", ""))
def text(lab):
    s, off = labels[lab]
    b = secs[s][off:]
    return b[:b.index(0)].decode("latin-1").replace("\n", "\n")
refs = {}
for ln in run("-dr").splitlines():
    m = re.search(r"R_X86_64_PC32\s+(\.LC\d+)", ln)
    if m:
        refs[text(m.group(1))] = refs.get(text(m.group(1)), 0) + 1
calls = sum(1 for ln in run("-dr").splitlines() if re.search(r"R_X86_64_PLT32\s+fatal", ln))
for t in sorted(refs):
    print("%2d  %s" % (refs[t], t))
print("fatal() call relocations: %d" % calls)
