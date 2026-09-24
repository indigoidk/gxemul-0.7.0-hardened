# Opus f2 (repair-pass) mutants for #545: ONE edit each on the FIXED dev_footbridge.c; each find must match EXACTLY ONCE.
import io, sys, os
root, mut = sys.argv[1], sys.argv[2]
p = os.path.join(root, 'src', 'devices', 'dev_footbridge.c')
s = io.open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
BS = chr(92)
EOLQ = ' ]' + BS + 'n");'
def rep(old, new):
    global s
    o, n = old.replace('\n', nl), new.replace('\n', nl)
    assert s.count(o) == 1, (mut, o[:70], s.count(o))
    s = s.replace(o, n)
IRQ_ST_TAIL = '\t\t\tfatal("[ WARNING: footbridge write to irq status? "\n\t\t\t    "(once)' + EOLQ + '\n\t\t}\n'
if mut == 'F1':    # Q2 cand 1: latch guard conditioned on a field X4 never seeds nonzero (timer_control)
    rep('else if (!d->warned_irq_raw_w) {', 'else if (!d->warned_irq_raw_w && !d->timer_control[0]) {')
elif mut == 'F1b': # guard conditioned on irq_enable (a write before interrupts are enabled is silent)
    rep('else if (!d->warned_irq_status_w) {', 'else if (!d->warned_irq_status_w && d->irq_enable) {')
elif mut == 'F1c': # same at FIQ_STATUS on fiq_enable
    rep('else if (!d->warned_fiq_status_w) {', 'else if (!d->warned_fiq_status_w && d->fiq_enable) {')
elif mut == 'F2':  # Q2 cand 2: a REPEATED (latched) IRQ_STATUS write decline drops the interrupt line
    rep(IRQ_ST_TAIL, IRQ_ST_TAIL[:-4] + '\t\t} else\n\t\t\tINTERRUPT_DEASSERT(d->irq);\n')
elif mut == 'F2b': # a NARROW FIRST decline at FIQ_RAW_STATUS drops the IRQ line
    rep('\t\t\td->warned_fiq_raw_w = 1;\n', '\t\t\td->warned_fiq_raw_w = 1;\n\t\t\tif (len != 4) INTERRUPT_DEASSERT(d->irq);\n')
elif mut == 'F3':  # Q2 cand 3: a legal NONZERO EnableSet write re-arms the +0x18c read latch
    rep('\t\t\td->irq_enable |= idata;\n', '\t\t\td->irq_enable |= idata;\n\t\t\tif (idata) d->warned_irq_clear_r = 0;\n')
elif mut == 'F3b': # a legal NONZERO EnableClear write re-arms the IRQ_STATUS write latch
    rep('\t\t\td->irq_enable &= ~idata;\n', '\t\t\td->irq_enable &= ~idata;\n\t\t\tif (idata) d->warned_irq_status_w = 0;\n')
elif mut == 'F4':  # X1 blind spot: a NARROW FIRST FIQ_STATUS write STORES (announce unchanged)
    rep('\t\t\td->warned_fiq_status_w = 1;\n', '\t\t\td->warned_fiq_status_w = 1;\n\t\t\tif (len != 4) d->fiq_status = idata;\n')
elif mut == 'F4b': # X1 blind spot: a NARROW FIRST +0x18c read clears IRQEnable
    rep('\t\t\td->warned_irq_clear_r = 1;\n', '\t\t\td->warned_irq_clear_r = 1;\n\t\t\tif (len != 4) d->irq_enable = 0;\n')
elif mut == 'F4c': # X1 blind spot: a NARROW FIRST IRQ_RAW_STATUS write stores
    rep('\t\t\td->warned_irq_raw_w = 1;\n', '\t\t\td->warned_irq_raw_w = 1;\n\t\t\tif (len != 4) d->irq_status = idata;\n')
elif mut == 'F5':  # a legal IRQ_STATUS read re-arms its latch only when it reads ZERO (comma form: keeps the if/else)
    rep('\t\t\todata = d->irq_status & d->irq_enable;\n', '\t\t\todata = d->irq_status & d->irq_enable, (void)(odata || (d->warned_irq_status_w = 0));\n')
elif mut == 'F5b': # a legal IRQ_RAW_STATUS read re-arms the IRQ_STATUS latch when it reads ZERO (arm S's own between-read)
    rep('\t\t\todata = d->irq_status;\n', '\t\t\todata = d->irq_status, (void)(odata || (d->warned_irq_status_w = 0));\n')
elif mut == 'F7':  # the removed value reinstated on every LATCHED +0x18c read (floor b-shape under a different predicate)
    rep('\t\t\t    "ENABLE CLEAR? (once)' + EOLQ + '\n\t\t}\n', '\t\t\t    "ENABLE CLEAR? (once)' + EOLQ + '\n\t\t} else\n\t\t\todata = d->irq_enable;\n')
elif mut == 'F7b': # ... only on a latched NARROW +0x18c read
    rep('\t\t\t    "ENABLE CLEAR? (once)' + EOLQ + '\n\t\t}\n', '\t\t\t    "ENABLE CLEAR? (once)' + EOLQ + '\n\t\t} else if (len != 4)\n\t\t\todata = d->irq_enable;\n')
else:
    sys.exit('unknown ' + mut)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('applied', mut)
