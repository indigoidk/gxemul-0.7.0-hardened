# #545 pass-2 repair -- the mutants the panel named after the X1-X3 repair, each ONE edit on the FIXED dev_footbridge.c.
#   python mkmut_p2b.py <tree-root> <mutant>          every find must match EXACTLY ONCE
import io, sys, os
root, mut = sys.argv[1], sys.argv[2]
p = os.path.join(root, 'src', 'devices', 'dev_footbridge.c')
s = io.open(p, encoding='utf-8', newline='').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, (mut, old[:70], s.count(old))
    s = s.replace(old, new)

EXIT = '\t\t\texit(1);\n'
if mut == 'Z1':      # codex R1: the IRQ_STATUS latch guard conditioned on the data
    rep('else if (!d->warned_irq_status_w) {', 'else if (!d->warned_irq_status_w && idata) {')
elif mut == 'Z1b':   # codex R1 at FIQ_RAW_STATUS
    rep('else if (!d->warned_fiq_raw_w) {', 'else if (!d->warned_fiq_raw_w && idata) {')
elif mut == 'Z2':    # codex R1: the 18c read latch guard conditioned on irq_enable
    rep('} else if (!d->warned_irq_clear_r) {', '} else if (!d->warned_irq_clear_r && d->irq_enable) {')
elif mut == 'Z3':    # codex R2: the IRQ_STATUS direction test rewritten on the data
    rep('\tcase IRQ_STATUS:\n\t\tif (writeflag == MEM_READ)', '\tcase IRQ_STATUS:\n\t\tif (!idata)')
elif mut == 'Z4':    # codex R2: the EnableClear direction test rewritten on the data
    rep('\tcase IRQ_ENABLE_CLEAR:\n\t\tif (writeflag == MEM_WRITE) {', '\tcase IRQ_ENABLE_CLEAR:\n\t\tif (idata) {')
elif mut == 'Z5':    # codex R3: the IRQ_STATUS read's status field swapped for the FIQ one
    rep('odata = d->irq_status & d->irq_enable;', 'odata = d->fiq_status & d->irq_enable;')
elif mut == 'Z6':    # codex R3: the IRQ_STATUS read's enable field swapped for fiq_status
    rep('odata = d->irq_status & d->irq_enable;', 'odata = d->irq_status & d->fiq_status;')
elif mut == 'Z7':    # consolidation F4: a legal VENDOR_ID read clears the IRQ_STATUS latch
    rep('\tcase VENDOR_ID:\n', '\tcase VENDOR_ID:\n\t\td->warned_irq_status_w = 0;\n')
elif mut == 'Z7b':   # consolidation F4: a legal IRQEnableSet WRITE clears the FIQ_RAW_STATUS latch
    rep('\t\tif (writeflag == MEM_WRITE) {\n\t\t\td->irq_enable |= idata;\n',
        '\t\tif (writeflag == MEM_WRITE) {\n\t\t\td->warned_fiq_raw_w = 0;\n\t\t\td->irq_enable |= idata;\n')
elif mut == 'Z8':    # consolidation F6: a NARROW declined 18c read leaks irq_enable
    rep('\t\t} else if (!d->warned_irq_clear_r) {', '\t\t} else if ((len < 4 ? (odata = d->irq_enable) : 0), !d->warned_irq_clear_r) {')
elif mut == 'Z9':    # codex R4 (GUEST-only): IRQ_STATUS and IRQ_RAW_STATUS exchange their announce texts
    rep('"[ WARNING: footbridge write to irq status? "\n\t\t\t    "(once) ]\\n"', '"[ footbridge write to irq_raw_status "\n\t\t\t    "(once) ]\\n"')
    rep('fatal("[ footbridge write to irq_raw_status (once) ]\\n");', 'fatal("[ WARNING: footbridge write to irq status? (once) ]\\n");')
elif mut in ('M1b', 'M1c', 'M1d', 'M1e'):   # floor (b) at the other four sites: verbatim reinstatement of exit(1)
    site = {'M1b': 'warned_irq_status_w', 'M1c': 'warned_irq_raw_w', 'M1d': 'warned_irq_clear_r', 'M1e': 'warned_fiq_status_w'}[mut]
    i = s.index('d->%s = 1;\n' % site)
    j = s.index(');\n', s.index('fatal(', i)) + 3
    assert s.count('d->%s = 1;\n' % site) == 1
    s = s[:j] + EXIT + s[j:]
else:
    raise SystemExit('unknown mutant ' + mut)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('MUTANT', mut)
