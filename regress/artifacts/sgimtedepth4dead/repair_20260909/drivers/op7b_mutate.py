#!/usr/bin/env python3
"""Apply ONE mutant edit to a copy of dev_sgi_re.c.

Refuses unless the anchor occurs EXACTLY ONCE.  A replacement that matched nothing, or
matched twice, would otherwise produce a clean, confident, wrong measurement -- and the
score would look like a result.

usage: op7b_mutate.py <file> <replace|delete> <old> <new>
"""
import sys

path, kind, old, new = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

lines = open(path, encoding="utf-8", newline="\n").read().split("\n")
hits = [i for i, l in enumerate(lines) if old in l]
print("ANCHOR %r occurrences=%d at 1-based lines %s" % (old, len(hits), [i + 1 for i in hits]))
if len(hits) != 1:
    print("MUT-FAIL: want exactly one occurrence")
    sys.exit(9)
i = hits[0]

if kind == "replace":
    lines[i] = lines[i].replace(old, new)
    print("NEW LINE %d: %s" % (i + 1, lines[i]))
elif kind == "delete":
    print("DELETED LINE %d: %s" % (i + 1, lines[i]))
    del lines[i]
else:
    print("MUT-FAIL: unknown kind %r" % kind)
    sys.exit(9)

open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("MUT_OK")
