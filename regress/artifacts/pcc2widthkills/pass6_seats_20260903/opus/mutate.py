import sys, re
TAB = chr(9)
mode = sys.argv[1]
path = "/tmp/gxopus_p6/src/devices/dev_pcc2.c"
src = open(path).read()
n = 0
if mode == "M1":
    # the `break;' that FOLLOWS each pcc2_width_decline() call -> conditioned on width
    lines = src.split("\n")
    out = []
    for i, l in enumerate(lines):
        if l == TAB*3 + "break;" and i > 0 and "pcc2_width_decline(" in lines[i-1]:
            out.append(TAB*3 + "if (len < 4) break;")
            n += 1
        else:
            out.append(l)
    src = "\n".join(out)
elif mode == "M2":
    # ONE conjunct at the TxICR guard, drawn from a field the guarded body reads
    old = (TAB*2 + "if (len != 1 && writeflag == MEM_WRITE) {\n"
           + TAB*3 + 'pcc2_width_decline(d, PCC2_W_TXICR_LEN, "PCCTWO_TxICR", len);')
    new = (TAB*2 + "if (len != 1 && writeflag == MEM_WRITE\n"
           + TAB*2 + "    && d->pending_timer1_interrupts == 0) {\n"
           + TAB*3 + 'pcc2_width_decline(d, PCC2_W_TXICR_LEN, "PCCTWO_TxICR", len);')
    n = src.count(old)
    src = src.replace(old, new)
elif mode == "M3":
    # negative control: guard DELETED at GENCTL (must red known rows)
    old = (TAB*2 + "if (len != 1 && writeflag == MEM_WRITE) {\n"
           + TAB*3 + 'pcc2_width_decline(d, PCC2_W_GENCTL_LEN, "PCCTWO_GENCTL", len);\n'
           + TAB*3 + "break;\n" + TAB*2 + "}\n")
    n = src.count(old)
    src = src.replace(old, "")
else:
    sys.exit("bad mode")
if n == 0:
    sys.exit("MUTANT TEXT NOT FOUND -- FAIL")
open(path, "w").write(src)
print("MUT_SITES=%d" % n)
