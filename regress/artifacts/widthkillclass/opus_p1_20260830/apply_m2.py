# M2: latch-bit COLLISION -- TLB_B shares TLB_A's bit.  One character class
# of edit; the kind a careless enum extension produces.
p = "/tmp/gxopus_497/src/devices/dev_sgi_re.c"
s = open(p).read()
old = "\tSGIRE_W_TLBB_LEN\t= 1 << 1,"
new = "\tSGIRE_W_TLBB_LEN\t= 1 << 0,"
assert s.count(old) == 1, "found %d" % s.count(old)
s = s.replace(old, new, 1)
open(p, "w").write(s)
print("MUTANT_M2_APPLIED: TLBB bit collides with TLBA (1 << 0)")
