import sys
p = sys.argv[1]; s = open(p, encoding="utf-8", newline="").read()
old = "(int) len, (int) idata);"
new = "(int) len, 0);"
assert s.count(old) == 1, "anchor count %d" % s.count(old)
open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
