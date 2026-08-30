p = "/tmp/gxopus_497/src/devices/dev_sgi_re.c"
s = open(p).read()
old = "\t\tif (len != 8) {\n"
new = "\t\tif (len != 8 && writeflag == MEM_WRITE) {\n"
c = s.count(old)
assert c == 6, "expected 6 guards, found %d" % c
s = s.replace(old, new)
open(p, "w").write(s)
print("MUTANT_M1_APPLIED sites=%d  (one added conjunct per site)" % c)
