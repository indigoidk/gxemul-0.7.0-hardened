#!/usr/bin/env python3
# usage: patch.py <file> <old_marker_unique> <replacement>  (reads replacement from stdin block file)
import sys
f, oldf, newf = sys.argv[1], sys.argv[2], sys.argv[3]
src = open(f).read()
old = open(oldf).read()
new = open(newf).read()
n = src.count(old)
if n != 1:
    sys.stderr.write("MARKER COUNT %d (need 1) for %s\n" % (n, oldf))
    sys.exit(3)
open(f, "w").write(src.replace(old, new))
print("PATCH OK")
