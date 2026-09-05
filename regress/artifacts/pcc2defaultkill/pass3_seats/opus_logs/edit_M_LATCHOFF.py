import sys
p = sys.argv[1]; s = open(p, encoding="utf-8", newline="").read()
old = "\t\t\td->warned_unimpl |= 1ULL << relative_addr;"
new = ("\t\t\tif (relative_addr == PCCTWO_IEICR ||\n"
       "\t\t\t    relative_addr == PCCTWO_IEERR)\n"
       "\t\t\t\td->warned_unimpl |= 1ULL << relative_addr;")
assert s.count(old) == 1, "anchor count %d" % s.count(old)
open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
