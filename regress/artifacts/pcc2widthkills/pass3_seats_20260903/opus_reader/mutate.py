import sys
tag = sys.argv[1]
p = "/tmp/gxopus_p3/src/devices/dev_pcc2.c"
s = open(p).read()
G = "if (len != 1 && writeflag == MEM_WRITE) {"

def one(old, new):
    global s
    n = s.count(old)
    assert n == 1, "PATTERN COUNT %d (want 1) for %r" % (n, old[:80])
    s = s.replace(old, new)

if tag == "BASE":
    pass
elif tag == "MA":                       # M_FALL_VECBASE: announce, then LAND
    one('pcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);\n\t\t\tbreak;\n',
        'pcc2_width_decline(d, PCC2_W_VECBASE_LEN, "PCCTWO_VECBASE", len);\n')
elif tag == "MB":                       # M_FALL_IPL
    one('pcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);\n\t\t\tbreak;\n',
        'pcc2_width_decline(d, PCC2_W_IPL_LEN, "PCCTWO_IPL", len);\n')
elif tag == "MC":                       # M_NOWRITEFLAG: one character, all twelve
    n = s.count(G)
    assert n == 12, "GUARD COUNT %d (want 12)" % n
    s = s.replace(G, "if (len != 1 && writeflag <= MEM_WRITE) {")
elif tag == "MD":                       # control: MA at GENCTL instead (must be CAUGHT)
    one('pcc2_width_decline(d, PCC2_W_GENCTL_LEN, "PCCTWO_GENCTL", len);\n\t\t\tbreak;\n',
        'pcc2_width_decline(d, PCC2_W_GENCTL_LEN, "PCCTWO_GENCTL", len);\n')
else:
    raise SystemExit("unknown tag " + tag)
open(p, "w").write(s)
print("  mutated: " + tag)
