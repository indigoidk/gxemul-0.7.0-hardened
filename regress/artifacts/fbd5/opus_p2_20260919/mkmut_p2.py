# Opus pass-2 mutants for #545, each ONE edit on the FIXED dev_footbridge.c; every find must match EXACTLY ONCE.
import io, sys, os
root, mut = sys.argv[1], sys.argv[2]
p = os.path.join(root, 'src', 'devices', 'dev_footbridge.c')
s = io.open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
BS = chr(92)
def rep(old, new):
    global s
    o, n = old.replace('\n', nl), new.replace('\n', nl)
    assert s.count(o) == 1, (mut, o[:70], s.count(o))
    s = s.replace(o, n)
if mut == 'A1':    # (a) len==4 conjunct on the FIQ_RAW_STATUS write decline
    rep('else if (!d->warned_fiq_raw_w) {', 'else if (len == 4 && !d->warned_fiq_raw_w) {')
elif mut == 'A2':  # (a) len==4 conjunct on the IRQ_ENABLE_CLEAR read decline
    rep('} else if (!d->warned_irq_clear_r) {', '} else if (len == 4 && !d->warned_irq_clear_r) {')
elif mut == 'A3':  # (a) len==4 conjunct on the IRQ_RAW_STATUS write decline
    rep('else if (!d->warned_irq_raw_w) {', 'else if (len == 4 && !d->warned_irq_raw_w) {')
elif mut == 'B1':  # (b) the LEGAL IRQ_STATUS read clears the IRQ_STATUS write latch (its own register's read)
    rep('\t\t\todata = d->irq_status & d->irq_enable;\n',
        '\t\t\todata = d->irq_status & d->irq_enable, d->warned_irq_status_w = 0;\n')
elif mut == 'B2':  # (b) the LEGAL IRQEnable (+0x188) read clears the IRQ_RAW_STATUS write latch
    rep('\t\t\todata = d->irq_enable;\n\t\t}\n\t\tbreak;\n\n\tcase IRQ_ENABLE_CLEAR:',
        '\t\t\todata = d->irq_enable;\n\t\t\td->warned_irq_raw_w = 0;\n\t\t}\n\t\tbreak;\n\n\tcase IRQ_ENABLE_CLEAR:')
elif mut == 'B3':  # (b) the LEGAL FIQ_RAW_STATUS read clears the FIQ_STATUS write latch
    rep('\t\t\todata = d->fiq_status;\n', '\t\t\todata = d->fiq_status, d->warned_fiq_status_w = 0;\n')
elif mut == 'C1':  # (c) the IRQ_STATUS decline stores into the FIQ family's status
    rep('\t\t\td->warned_irq_status_w = 1;\n', '\t\t\td->warned_irq_status_w = 1;\n\t\t\td->fiq_status = idata;\n')
elif mut == 'C2':  # (c) the FIQ_RAW_STATUS decline stores into the IRQ family's status
    rep('\t\t\td->warned_fiq_raw_w = 1;\n', '\t\t\td->warned_fiq_raw_w = 1;\n\t\t\td->irq_status |= idata;\n')
elif mut == 'D1':  # (d) the IRQ_RAW_STATUS announce drops "(once)"
    rep('fatal("[ footbridge write to irq_raw_status (once) ]' + BS + 'n");',
        'fatal("[ footbridge write to irq_raw_status ]' + BS + 'n");')
elif mut == 'D2':  # (d) the IRQ_ENABLE_CLEAR announce drops "(once)" (wrapped literal)
    rep('"ENABLE CLEAR? (once) ]' + BS + 'n");', '"ENABLE CLEAR? ]' + BS + 'n");')
elif mut == 'G1':  # extra: the DOMINATING predicate narrowed -- a BYTE/HALF legal IRQ_STATUS read falls into the decline
    rep('\t\tif (writeflag == MEM_READ)\n\t\t\todata = d->irq_status & d->irq_enable;\n',
        '\t\tif (writeflag == MEM_READ && len == 4)\n\t\t\todata = d->irq_status & d->irq_enable;\n')
elif mut == 'G2':  # extra: same at FIQ_RAW_STATUS
    rep('\t\tif (writeflag == MEM_READ)\n\t\t\todata = d->fiq_status;\n',
        '\t\tif (writeflag == MEM_READ && len == 4)\n\t\t\todata = d->fiq_status;\n')
else:
    raise SystemExit("unknown mutant " + mut)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print("MUTANT", mut, "applied")
