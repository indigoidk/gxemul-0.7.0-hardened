import sys
p = sys.argv[1]; s = open(p, encoding="utf-8", newline="").read()
old = '\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {'
new = ('\t\tif (writeflag == MEM_WRITE && relative_addr < 0x14)\n'
       '\t\t\td->pcctwo_reg[relative_addr] = idata;\n'
       '\t\tif (!(d->warned_unimpl & (1ULL << relative_addr))) {')
assert s.count(old) == 1, "anchor count %d" % s.count(old)
open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
