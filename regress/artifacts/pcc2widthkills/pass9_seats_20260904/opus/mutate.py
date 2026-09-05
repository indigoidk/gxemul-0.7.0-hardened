import io, sys
path, which = sys.argv[1], sys.argv[2]
s = io.open(path, encoding='utf-8', newline='').read()
GUARD = "if (len != 1 && writeflag == MEM_WRITE) {"
if which == "PENDBOTH":
    old = ("\t\tif (len != 1 && writeflag == MEM_WRITE) {\n"
           "\t\t\tpcc2_width_decline(d, PCC2_W_TXICR_LEN,")
    new = ("\t\tif (len != 1 && writeflag == MEM_WRITE\n"
           "\t\t    && !(d->pending_timer1_interrupts && d->pending_timer2_interrupts)) {\n"
           "\t\t\tpcc2_width_decline(d, PCC2_W_TXICR_LEN,")
    n = s.count(old)
    assert n == 1, "PENDBOTH anchor count %d" % n
    s = s.replace(old, new)
elif which == "IDATA2":
    n = s.count(GUARD)
    assert n == 12, "IDATA2 guard count %d" % n
    s = s.replace(GUARD, "if (len != 1 && idata != 2 && writeflag == MEM_WRITE) {")
else:
    raise SystemExit("unknown mutant " + which)
io.open(path, 'w', encoding='utf-8', newline='').write(s)
print("MUTATOR_OK", which, n)
