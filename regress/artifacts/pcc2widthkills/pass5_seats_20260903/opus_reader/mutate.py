import re, sys
F = "/tmp/gxopus_p5/src/devices/dev_pcc2.c"
which = sys.argv[1]
src = open(F).read()
GUARD = "\t\tif (len != 1 && writeflag == MEM_WRITE) {\n"
#  map each guard to the bit constant on the line that follows it
pat = re.compile(r"\t\tif \(len != 1 && writeflag == MEM_WRITE\) \{\n(\t\t\tpcc2_width_decline\(d, (PCC2_W_\w+),)")
hits = pat.findall(src)
print("GUARDS FOUND: %d -> %s" % (len(hits), [h[1] for h in hits]))
n = 0
if which in ("M1", "M2"):
    only = "PCC2_W_GENCTL_LEN" if which == "M2" else None
    def repl(m):
        global n
        bit = m.group(2)
        if only and bit != only:
            return m.group(0)
        n += 1
        return ("\t\tif (len != 1 && writeflag == MEM_WRITE\n"
                "\t\t    && !(d->warned & (1u << %s))) {\n" % bit) + m.group(1)
    src = pat.sub(repl, src)
elif which == "M3":       #  negative control: guard DELETED at GENCTL
    old = ("\t\tif (len != 1 && writeflag == MEM_WRITE) {\n"
           "\t\t\tpcc2_width_decline(d, PCC2_W_GENCTL_LEN, \"PCCTWO_GENCTL\", len);\n"
           "\t\t\tbreak;\n\t\t}\n")
    assert old in src, "GENCTL guard text not found"
    src = src.replace(old, "", 1); n = 1
elif which == "M4":       #  the len ARGUMENT nulled in every announce
    src, n = re.subn(r'(pcc2_width_decline\(d, PCC2_W_\w+, "PCCTWO_\w+", )len\)', r'\g<1>1)', src)
else:
    sys.exit("unknown mutant " + which)
assert n > 0, "MUTANT TEXT NOT FOUND -- FAIL"
open(F, "w").write(src)
print("MUTANT %s APPLIED at %d site(s)" % (which, n))
