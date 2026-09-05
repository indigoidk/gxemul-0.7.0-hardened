import sys
p = sys.argv[1]; s = open(p, encoding="utf-8", newline="").read()
old = '(int) relative_addr, (int) len, data[0]);'
new = '(int) relative_addr, (int) len, d->pcctwo_reg[relative_addr]);'
assert s.count(old) == 1, "anchor count %d" % s.count(old)
open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
