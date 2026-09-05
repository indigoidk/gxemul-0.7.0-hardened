#  Apply ONE named mutant to /tmp/gxopus_p8/src/devices/dev_pcc2.c.
#  The file must be cmp-clean against SEC when this runs (the caller checks).
#  Usage: python3 mutate.py <NAME>
import io, sys

P = "/tmp/gxopus_p8/src/devices/dev_pcc2.c"
name = sys.argv[1]
src = io.open(P, encoding="utf-8").read()
GUARD = "\t\tif (len != 1 && writeflag == MEM_WRITE) {\n"
assert src.count(GUARD) == 12, ("expected 12 guards, got", src.count(GUARD))


def guard_after(text, case_label):
    i = text.index(case_label)
    j = text.index(GUARD, i)
    return j


if name == "M_IPLR":
    #  part 1 -- hoist a function-scope static (INERT: a declaration move)
    a = "\tuint64_t idata = 0;\n"
    assert src.count(a) == 1
    src = src.replace(a, a + "\tstatic int w_r = 0;\t/* M_IPLR part 1 */\n")
    #  part 2 -- delete the READ branch's block static and rename its uses (INERT: a rename)
    b = ("\t\t\t\tstatic int w = 0;\t/* #119: was exit(1) */\n"
         "\t\t\t\tif (!w) { fatal(\"[ pcc2: IPL == 0 on read ]\\n\");\n"
         "\t\t\t\t    w = 1; }\n")
    assert src.count(b) == 1, "anchor b (read-branch static)"
    src = src.replace(b,
                      "\t\t\t\tif (!w_r) { fatal(\"[ pcc2: IPL == 0 on read ]\\n\");\n"
                      "\t\t\t\t    w_r = 1; }\n")
    #  part 3 -- the LIVE edit: the IPL width guard reads it
    j = guard_after(src, "\tcase PCCTWO_IPL:\n")
    src = (src[:j] + "\t\tif (len != 1 && writeflag == MEM_WRITE && !w_r) {\n"
           + src[j + len(GUARD):])

elif name == "M_WARNX":
    #  the pass-5 canonical `&& !(d->warned & (1u << bit))' at GENCTL with ONE token
    #  changed: MASK's enum member instead of GENCTL's.
    j = guard_after(src, "\tcase PCCTWO_GENCTL:\n")
    src = (src[:j]
           + "\t\tif (len != 1 && writeflag == MEM_WRITE &&\n"
             "\t\t    !(d->warned & (1u << PCC2_W_MASK_LEN))) {\n"
           + src[j + len(GUARD):])

else:
    raise SystemExit("unknown mutant %r" % name)

io.open(P, "w", encoding="utf-8").write(src)
print("APPLIED", name)
